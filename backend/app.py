"""Backend: Main Entry Point — Flask API server.

Provides REST API endpoints for Electron frontend to interact with.
Routes file processing, storage, and RAG operations.

Wing: smartdoc_backend
Topic: api_server
Last Updated: 2026-05-05 09:05
"""

import argparse
import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from processor import DocumentProcessor
from vector_storage import VectorStorage
from ollama_client import OllamaClient
from metadata_extractor import MetadataExtractor
from embedding_service import EmbeddingService
from rag_pipeline import RAGPipeline
from document_refiner import DocumentRefiner

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for Electron frontend

# Initialize components
processor = DocumentProcessor()
storage = VectorStorage()

# Initialize Ollama with Gemma 4
ollama = OllamaClient(model="gemma4:e2b")

# Initialize other services
metadata_extractor = MetadataExtractor(ollama)
document_refiner = DocumentRefiner(ollama)

# Initialize embedding service with nomic-embed-text (768 dimensions)
embedding_service = EmbeddingService(model="nomic-embed-text")
rag_pipeline = RAGPipeline(embedding_service, storage, ollama)

# Ensure database wings exist
storage.ensure_wings()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    ollama_running = ollama.is_running()
    return jsonify({
        'status': 'healthy',
        'ollama_running': ollama_running
    })


@app.route('/api/ollama/start', methods=['POST'])
def start_ollama():
    """Start Ollama service."""
    success = ollama.start_ollama()
    return jsonify({'success': success})


@app.route('/api/process', methods=['POST'])
def process_file():
    """Process uploaded file with Gemma 4 multimodal and RAG embedding."""
    data = request.json
    file_path = data.get('file_path')
    generate_embeddings = data.get('embed', True)  # Default to True
    generate_images = data.get('images', False)  # Generate images for multimodal AI

    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': 'Invalid file path'}), 400

    try:
        # Process document with optional image generation for Gemma 4
        result = processor.process_file(file_path, generate_images=generate_images)

        if not result['success']:
            return jsonify({'error': result['metadata'].get('error', 'Processing failed')}), 500

        # Extract metadata using Gemma 4 (with images if available)
        images = result.get('images', None)
        metadata = metadata_extractor.extract_metadata(result['markdown'], file_path, images=images)

        # Classify wing
        wing = metadata_extractor.classify_wing(metadata)

        # Create base document data
        import json
        base_doc_id = f"{os.path.basename(file_path)}_{os.path.getmtime(file_path)}"
        doc_data = {
            'id': base_doc_id,
            'filename': os.path.basename(file_path),
            'markdown': result['markdown'],
            'metadata': json.dumps({**result['metadata'], **metadata}),
            'embedding': [0.0] * embedding_service.dimension,
            'wing': wing,
            'created_at': str(os.path.getmtime(file_path))
        }

        # Store base document
        storage.add_document(wing, doc_data)

        # Generate and store embeddings if requested
        chunks_stored = 0
        if generate_embeddings:
            chunks = rag_pipeline.embed_document(result['markdown'])
            for i, chunk in enumerate(chunks):
                chunk_doc = {
                    'id': f"{base_doc_id}_chunk_{i}",
                    'filename': f"{os.path.basename(file_path)} (đoạn {i})",
                    'markdown': chunk['text'],
                    'metadata': json.dumps({
                        'parent_id': base_doc_id,
                        'chunk_index': i,
                        'chunk_length': chunk['length']
                    }),
                    'embedding': chunk['embedding'],
                    'wing': wing,
                    'created_at': str(os.path.getmtime(file_path))
                }
                storage.add_document(wing, chunk_doc)
                chunks_stored += 1

        return jsonify({
            'success': True,
            'markdown': result['markdown'],
            'metadata': {**result['metadata'], **metadata},
            'wing': wing,
            'chunks_embedded': chunks_stored,
            'has_images': result.get('has_images', False)
        })

    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        logger.error(f"Processing error: {e}\n{tb}")
        return jsonify({'error': str(e) or 'Unknown error'}), 500


@app.route('/api/wings', methods=['GET'])
def list_wings():
    """Get list of available wings."""
    wings = storage.list_wings()
    wing_info = []
    for wing in wings:
        wing_info.append({
            'name': wing,
            'count': storage.get_document_count(wing)
        })
    return jsonify(wing_info)


@app.route('/api/ollama/models', methods=['GET'])
def list_models():
    """Get available Ollama models."""
    models = ollama.list_models()
    return jsonify({'models': models})


@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with AI using RAG."""
    data = request.json
    message = data.get('message')
    wings = data.get('wings')  # Optional: specific wings to search

    if not message:
        return jsonify({'error': 'Message required'}), 400

    try:
        # Use RAG pipeline
        result = rag_pipeline.query(message, wings=wings, limit=5)

        return jsonify({
            'message': {
                'role': 'assistant',
                'content': result['response']
            },
            'sources': result['sources'],
            'num_documents': result['num_documents']
        })

    except Exception as e:
        logger.error(f"RAG error: {e}")
        # Fallback to simple chat
        response = ollama.chat(prompt=message)

        # Format fallback response
        return jsonify({
            'message': {
                'role': 'assistant',
                'content': response.get('message', {}).get('content', 'Xin lỗi, có lỗi xảy ra.')
            },
            'sources': [],
            'num_documents': 0
        })


if __name__ == '__main__':
    # Check if Ollama is running (don't start it)
    if not ollama.is_running():
        logger.warning("Ollama is not running! Please start it manually.")
        logger.info("Run: ollama serve")
        logger.info("Waiting 60s for you to start Ollama...")
        import time
        time.sleep(60)

        if not ollama.is_running():
            logger.error("Ollama still not running. Exiting.")
            exit(1)

    # Verify models are available (don't pull)
    models = ollama.list_models()
    logger.info(f"Available models: {models}")

    if 'gemma4:e2b' not in models:
        logger.error("Gemma 4 not found! Please install it.")
    if 'nomic-embed-text:latest' not in models:
        logger.error("nomic-embed-text not found! Please install it.")

    # Add refinement endpoints directly
    @app.route('/api/refine/summarize', methods=['POST'])
    def summarize_document():
        """Generate summary of document."""
        data = request.json
        markdown = data.get('markdown')
        if not markdown:
            return jsonify({'error': 'Markdown content required'}), 400
        try:
            summary = document_refiner.summarize(markdown)
            return jsonify({'success': True, 'summary': summary})
        except Exception as e:
            logger.error(f"Summary error: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/refine/formalize', methods=['POST'])
    def formalize_document():
        """Rewrite document in formal tone."""
        data = request.json
        markdown = data.get('markdown')
        if not markdown:
            return jsonify({'error': 'Markdown content required'}), 400
        try:
            formalized = document_refiner.formalize(markdown)
            return jsonify({'success': True, 'markdown': formalized})
        except Exception as e:
            logger.error(f"Formalization error: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/refine/custom', methods=['POST'])
    def custom_refinement():
        """Apply custom refinement to document."""
        data = request.json
        markdown = data.get('markdown')
        instruction = data.get('instruction')
        if not markdown or not instruction:
            return jsonify({'error': 'Markdown and instruction required'}), 400
        try:
            refined = document_refiner.custom_refinement(markdown, instruction)
            return jsonify({'success': True, 'markdown': refined})
        except Exception as e:
            logger.error(f"Custom refinement error: {e}")
            return jsonify({'error': str(e)}), 500

    logger.info("Refinement endpoints loaded")

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000, help='Port to listen on')
    args = parser.parse_args()
    port = args.port
    logger.info(f"Starting Flask server on port {port}...")
    app.run(host='127.0.0.1', port=port, debug=False)

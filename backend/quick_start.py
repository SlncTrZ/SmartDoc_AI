"""Backend: Quick Start Script - Start server without model checks.

Fast start for testing. Skips Ollama model verification.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS
from processor import DocumentProcessor
from vector_storage import VectorStorage
from ollama_client import OllamaClient
from metadata_extractor import MetadataExtractor
from embedding_service import EmbeddingService
from rag_pipeline import RAGPipeline
from document_refiner import DocumentRefiner
import logging

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
CORS(app)

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

# Import API routes (same as app.py)
from app import *

# Skip model checks for quick start
logger.info("Skipping model verification for quick start")

if __name__ == '__main__':
    # Ensure Ollama is running
    if not ollama.is_running():
        logger.info("Attempting to start Ollama...")
        ollama.start_ollama()
        logger.info("Waiting 30s for Ollama to start...")
        import time
        time.sleep(30)

    # Load refinement endpoints
    try:
        from refinement_endpoints import *
        logger.info("Refinement endpoints loaded")
    except ImportError:
        logger.warning("Could not import refinement endpoints")

    # Start Flask server
    logger.info("Starting Flask server on port 5000...")
    app.run(host='127.0.0.1', port=5000, debug=True)

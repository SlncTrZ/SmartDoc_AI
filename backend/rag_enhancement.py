"""Backend: RAG Enhancement — Update processing to include embeddings.

Adds embedding generation to document processing workflow.
Stores chunked embeddings in LanceDB.

Wing: smartdoc_backend
Topic: rag_enhancement
Last Updated: 2026-05-05 09:55
"""

import json
from rag_pipeline import RAGPipeline
from embedding_service import EmbeddingService


def process_document_with_embedding(doc_data: dict,
                                    embedding_service: EmbeddingService,
                                    rag_pipeline: RAGPipeline) -> list:
    """Process document and generate embeddings for RAG.

    Args:
        doc_data: Document data with markdown
        embedding_service: Embedding generation service
        rag_pipeline: RAG pipeline

    Returns:
        List of chunk documents with embeddings
    """
    markdown = doc_data.get('markdown', '')
    if not markdown:
        return []

    # Generate chunks with embeddings
    chunks = rag_pipeline.embed_document(markdown)

    # Create chunk documents
    chunk_documents = []
    for chunk in chunks:
        chunk_doc = {
            'id': f"{doc_data['id']}_chunk_{chunk['index']}",
            'filename': f"{doc_data['filename']} (đoạn {chunk['index']})",
            'markdown': chunk['text'],
            'metadata': json.dumps({
                'parent_id': doc_data['id'],
                'chunk_index': chunk['index'],
                'chunk_length': chunk['length']
            }),
            'embedding': chunk['embedding'],
            'wing': doc_data['wing'],
            'created_at': doc_data['created_at']
        }
        chunk_documents.append(chunk_doc)

    return chunk_documents


def reindex_all_documents(storage, embedding_service, rag_pipeline):
    """Reindex all documents with embeddings.

    Args:
        storage: Vector storage instance
        embedding_service: Embedding service
        rag_pipeline: RAG pipeline
    """
    print("Reindexing all documents with embeddings...")

    wings = storage.list_wings()

    for wing in wings:
        try:
            table = storage.db.open_table(wing)
            documents = table.to_list()

            print(f"Processing wing '{wing}': {len(documents)} documents")

            for doc in documents:
                # Parse metadata
                metadata = json.loads(doc.get('metadata', '{}'))

                # Skip if already chunked
                if 'parent_id' in metadata:
                    continue

                # Generate embeddings
                chunk_docs = process_document_with_embedding(doc, embedding_service, rag_pipeline)

                # Store chunks
                for chunk_doc in chunk_docs:
                    storage.add_document(wing, chunk_doc)

            print(f"Completed wing '{wing}'")

        except Exception as e:
            print(f"Error reindexing wing '{wing}': {e}")

    print("Reindexing completed!")

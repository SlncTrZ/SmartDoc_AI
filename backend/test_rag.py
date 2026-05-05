"""Backend: RAG Test Script — Test RAG pipeline with sample data.

Tests embedding generation, semantic search, and RAG query.
Run with: python test_rag.py

Wing: smartdoc_backend
Topic: rag_testing
Last Updated: 2026-05-05 09:55
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from embedding_service import EmbeddingService
from vector_storage import VectorStorage
from ollama_client import OllamaClient
from rag_pipeline import RAGPipeline
import json


def test_embedding():
    """Test embedding generation."""
    print("="*60)
    print("[Test 1] Embedding Generation")
    print("="*60)

    embedding_service = EmbeddingService()

    test_text = "Đây là một câu hỏi thử nghiệm về trí tuệ nhân tạo."

    print(f"Input: {test_text}")
    print("Generating embedding...")

    embedding = embedding_service.generate_embedding(test_text)

    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")
    print(f"Non-zero values: {sum(1 for x in embedding if x != 0)}")

    return embedding_service


def test_chunking(embedding_service):
    """Test text chunking."""
    print("\n" + "="*60)
    print("[Test 2] Text Chunking")
    print("="*60)

    rag_pipeline = RAGPipeline(embedding_service, VectorStorage(), OllamaClient())

    test_text = "Đây là đoạn văn bản đầu tiên.\n\nĐây là đoạn văn bản thứ hai với nội dung dài hơn để test chức năng chunking trong hệ thống RAG. Chức năng này quan trọng để chia nhỏ tài liệu thành các phần dễ xử lý."

    chunks = rag_pipeline.embed_document(test_text)

    print(f"Input text length: {len(test_text)}")
    print(f"Number of chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i}:")
        print(f"  Length: {chunk['length']}")
        print(f"  Preview: {chunk['text'][:100]}...")

    return rag_pipeline


def test_semantic_search(rag_pipeline, storage):
    """Test semantic search."""
    print("\n" + "="*60)
    print("[Test 3] Semantic Search")
    print("="*60)

    # Add sample documents
    sample_docs = [
        {
            'id': 'doc1',
            'filename': 'tai_lieu_1.pdf',
            'markdown': 'Trí tuệ nhân tạo là một lĩnh vực của khoa học máy tính.',
            'metadata': json.dumps({'type': 'test'}),
            'embedding': rag_pipeline.embedding_service.generate_embedding(
                'Trí tuệ nhân tạo là một lĩnh vực của khoa học máy tính.'
            ).tolist(),
            'wing': 'tai_lieu_khac',
            'created_at': '2026-05-05'
        },
        {
            'id': 'doc2',
            'filename': 'tai_lieu_2.pdf',
            'markdown': 'Machine learning giúp máy tính học từ dữ liệu.',
            'metadata': json.dumps({'type': 'test'}),
            'embedding': rag_pipeline.embedding_service.generate_embedding(
                'Machine learning giúp máy tính học từ dữ liệu.'
            ).tolist(),
            'wing': 'tai_lieu_khac',
            'created_at': '2026-05-05'
        }
    ]

    for doc in sample_docs:
        storage.add_document('tai_lieu_khac', doc)

    print("Added 2 sample documents")

    # Test search
    query = "AI là gì?"
    print(f"\nQuery: {query}")

    results = rag_pipeline.retrieve(query, wings=['tai_lieu_khac'], limit=2)

    print(f"Found {len(results)} results:")
    for i, result in enumerate(results):
        print(f"\n  Result {i+1}:")
        print(f"    File: {result.get('filename', 'Unknown')}")
        print(f"    Score: {result.get('_score', 0):.4f}")
        print(f"    Preview: {result.get('markdown', '')[:100]}...")

    return rag_pipeline


def test_rag_query(rag_pipeline):
    """Test full RAG query."""
    print("\n" + "="*60)
    print("[Test 4] Full RAG Query")
    print("="*60)

    query = "AI và machine learning có liên quan gì?"

    print(f"Query: {query}")
    print("\nRetrieving documents...")

    result = rag_pipeline.query(query, wings=['tai_lieu_khac'], limit=3)

    print("\n[Response]")
    print(result['response'])

    print("\n[Sources]")
    for i, source in enumerate(result['sources']):
        print(f"  {i+1}. {source['filename']} (Score: {source['score']:.4f})")

    print(f"\nTotal documents retrieved: {result['num_documents']}")


def main():
    """Run all RAG tests."""
    print("="*60)
    print("RAG PIPELINE TEST")
    print("="*60)

    # Initialize components
    storage = VectorStorage()
    storage.ensure_wings(['tai_lieu_khac'])

    # Test 1: Embedding
    embedding_service = test_embedding()

    # Test 2: Chunking
    rag_pipeline = test_chunking(embedding_service)

    # Test 3: Semantic Search
    test_semantic_search(rag_pipeline, storage)

    # Test 4: RAG Query
    test_rag_query(rag_pipeline)

    # Summary
    print("\n" + "="*60)
    print("[SUCCESS] All RAG tests completed!")
    print("="*60)
    print("\n[Next Steps]")
    print("  1. Test with real documents")
    print("  2. Integrate with frontend")
    print("  3. Optimize retrieval accuracy")


if __name__ == '__main__':
    main()

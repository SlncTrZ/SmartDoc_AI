"""Backend: Test nomic-embed-text with fresh schema.

Tests RAG pipeline with nomic-embed-text (768 dimensions).
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lancedb
from lancedb.pydantic import LanceModel, Vector
from embedding_service import EmbeddingService
import json


class NewDocumentSchema(LanceModel):
    """Schema with 768 dimensions for nomic-embed-text."""
    id: str
    filename: str
    markdown: str
    metadata: str
    embedding: Vector(768)
    wing: str
    created_at: str


def main():
    print("="*60)
    print("NOMIC-EMBED-TEXT TEST (768 dimensions)")
    print("="*60)

    # Use fresh database path
    db_path = "./data/test_nomic"
    if os.path.exists(db_path):
        import shutil
        shutil.rmtree(db_path)

    db = lancedb.connect(db_path)

    # Create table with new schema
    table = db.create_table("test_wing", schema=NewDocumentSchema)
    print("[OK] Created table with 768-dim schema")

    # Initialize embedding service
    embedding_service = EmbeddingService(model="nomic-embed-text")
    print(f"[OK] Initialized embedding service: {embedding_service.embedding_model}")

    # Test embedding
    test_text = "This is a test document about artificial intelligence"
    embedding = embedding_service.generate_embedding(test_text)
    print(f"[OK] Generated embedding: {len(embedding)} dimensions")

    # Add document
    doc = {
        'id': 'test1',
        'filename': 'test.pdf',
        'markdown': test_text,
        'metadata': json.dumps({'type': 'test'}),
        'embedding': embedding.tolist(),
        'wing': 'test_wing',
        'created_at': '2026-05-05'
    }

    try:
        table.add([doc])
        print("[OK] Document added successfully")

        # Test search
        query_text = "What is AI?"
        query_embedding = embedding_service.generate_embedding(query_text)
        print(f"[OK] Generated query embedding: {len(query_embedding)} dimensions")

        results = table.search(query_embedding.tolist()).limit(1).to_list()
        print(f"[OK] Search returned {len(results)} results")

        for i, r in enumerate(results):
            print(f"  Result {i+1}: {r.get('filename')} (score: {r.get('_score', 0):.4f})")

        print("\n" + "="*60)
        print("[SUCCESS] nomic-embed-text works perfectly!")
        print("="*60)

    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

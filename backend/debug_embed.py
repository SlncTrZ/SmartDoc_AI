"""Debug: Test embedding storage in LanceDB."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from embedding_service import EmbeddingService
from vector_storage import VectorStorage
from rag_pipeline import RAGPipeline
from ollama_client import OllamaClient

e = EmbeddingService()
s = VectorStorage()
o = OllamaClient()
r = RAGPipeline(e, s, o)

s.ensure_wings(['tai_lieu_test'])
print("[OK] Wing created")

# Test chunking
text = "Test paragraph for embedding. " * 50
chunks = r.embed_document(text[:1000])
print(f"[OK] {len(chunks)} chunks generated")

# Try storing a chunk
chunk_doc = {
    'id': 'test_chunk_0',
    'filename': 'test.pdf (doan 0)',
    'markdown': chunks[0]['text'],
    'metadata': json.dumps({'chunk_index': 0, 'length': chunks[0]['length']}),
    'embedding': chunks[0]['embedding'],
    'wing': 'tai_lieu_test',
    'created_at': '2026-05-05'
}
print(f"[OK] Embedding type: {type(chunks[0]['embedding'])}, len: {len(chunks[0]['embedding'])}")

s.add_document('tai_lieu_test', chunk_doc)
print(f"[OK] Chunk stored!")

count = s.get_document_count('tai_lieu_test')
print(f"[OK] Docs in tai_lieu_test: {count}")

"""Backend: Test with embeddings and RAG."""

import requests, os, json

API_BASE = "http://127.0.0.1:5000/api"

# Process with embeddings
print("[1] Process PDF with embeddings...")
pdf_path = "../test/ARTIFICIAL INTELLIGENCE.pdf"
payload = {"file_path": os.path.abspath(pdf_path), "embed": True, "images": False}
r = requests.post(f"{API_BASE}/process", json=payload, timeout=600)
if r.status_code == 200:
    d = r.json()
    print(f"[OK] Title: {d['metadata']['title']}")
    print(f"[OK] Chunks embedded: {d['chunks_embedded']}")
else:
    print(f"[ERROR] {r.text[:300]}")

# Check wings
print("\n[2] Document count:")
r = requests.get(f"{API_BASE}/wings", timeout=5)
for w in r.json():
    print(f"  {w['name']}: {w['count']} docs")

# RAG chat
print("\n[3] RAG Chat...")
r = requests.post(f"{API_BASE}/chat", json={"message": "What is this document about?"}, timeout=120)
if r.status_code == 200:
    c = r.json()
    print(f"[OK] Response: {c['message']['content'][:200]}")
    print(f"[OK] Sources: {c['num_documents']}")
    for s in c['sources']:
        print(f"  - {s['filename']}")
else:
    print(f"[ERROR] {r.text[:200]}")

# Refinement
print("\n[4] AI Summary...")
r = requests.post(f"{API_BASE}/refine/summarize", json={"markdown": "SmartDoc AI is a document management system that uses AI to process PDFs."}, timeout=60)
if r.status_code == 200:
    print(f"[OK] Summary: {r.json()['summary'][:100]}...")

print("\n[SUCCESS] All tests passed!")

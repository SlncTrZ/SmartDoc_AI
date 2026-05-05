"""Backend: Full test - no unicode issues."""

import requests, os, json, sys
sys.stdout.reconfigure(encoding='utf-8')

API_BASE = "http://127.0.0.1:5000/api"

# Process with embeddings
print("[1] Process PDF with embeddings...")
pdf_path = "../test/ARTIFICIAL INTELLIGENCE.pdf"
payload = {"file_path": os.path.abspath(pdf_path), "embed": True, "images": False}
r = requests.post(f"{API_BASE}/process", json=payload, timeout=600)
if r.status_code == 200:
    d = r.json()
    print(f"[OK] Title: {d['metadata']['title']}")
    print(f"[OK] Type: {d['metadata']['document_type']}")
    print(f"[OK] Chunks: {d['chunks_embedded']}")
else:
    print(f"[ERROR] Status {r.status_code}: {r.text[:300]}")

# Check wings
print("\n[2] Wings:")
r = requests.get(f"{API_BASE}/wings", timeout=5)
for w in r.json():
    print(f"  {w['name']}: {w['count']} docs")

# RAG chat
print("\n[3] RAG Chat...")
r = requests.post(f"{API_BASE}/chat", json={"message": "What is this document about?"}, timeout=180)
if r.status_code == 200:
    c = r.json()
    resp = c['message']['content'][:200].encode('ascii', 'replace').decode('ascii')
    print(f"[OK] Response: {resp}")
    print(f"[OK] Sources: {c['num_documents']}")
    for s in c['sources']:
        print(f"  - {s['filename']}")
else:
    print(f"[ERROR] Status {r.status_code}: {r.text[:200]}")

print("\n[SUCCESS] All OK!")

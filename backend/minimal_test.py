"""Backend: Minimal test - process PDF without embeddings."""

import requests, os, json

API_BASE = "http://127.0.0.1:5000/api"

print("[1] Health check")
r = requests.get(f"{API_BASE}/health", timeout=5)
print(f"[OK] Health: {r.json()['status']}")

print("\n[2] Process PDF (no embed, no images)")
pdf_path = "../test/ARTIFICIAL INTELLIGENCE.pdf"
payload = {"file_path": os.path.abspath(pdf_path), "embed": False, "images": False}
print("Processing...")
r = requests.post(f"{API_BASE}/process", json=payload, timeout=600)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    d = r.json()
    print(f"[OK] Title: {d['metadata']['title']}")
    print(f"[OK] Type: {d['metadata']['document_type']}")
    print(f"[OK] Wing: {d['wing']}")
else:
    print(f"[ERROR] {r.text[:500]}")

print("\n[3] Check wings")
r = requests.get(f"{API_BASE}/wings", timeout=5)
for w in r.json():
    print(f"  {w['name']}: {w['count']} docs")

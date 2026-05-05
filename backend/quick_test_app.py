"""Backend: Quick Test - Simple PDF processing test.

Tests: Health check, process PDF (no images), RAG chat.
"""

import requests, json, time

API_BASE = "http://127.0.0.1:5000/api"

print("="*60)
print("SMARTDOC AI - QUICK FULL TEST")
print("="*60)

# Health check
print("\n[1] Health check...")
r = requests.get(f"{API_BASE}/health", timeout=5)
h = r.json()
print(f"[OK] Status: {h['status']}, Ollama: {h['ollama_running']}")

# Wings
print("\n[2] Wings...")
r = requests.get(f"{API_BASE}/wings", timeout=5)
print(f"[OK] {len(r.json())} wings available")

# Process PDF (no images, faster)
print("\n[3] Processing PDF (no images)...")
pdf_path = "../test/ARTIFICIAL INTELLIGENCE.pdf"
import os
payload = {"file_path": os.path.abspath(pdf_path), "embed": True, "images": False}
print("This takes ~60s for Docling + embedding...")
start = time.time()
r = requests.post(f"{API_BASE}/process", json=payload, timeout=300)
elapsed = time.time() - start

if r.status_code == 200:
    result = r.json()
    print(f"[OK] Done in {elapsed:.0f}s")
    print(f"[OK] Title: {result['metadata'].get('title','N/A')}")
    print(f"[OK] Type: {result['metadata'].get('document_type','N/A')}")
    print(f"[OK] Chunks: {result['chunks_embedded']}")
    markdown = result['markdown']
else:
    print(f"[ERROR] {r.text[:200]}")
    exit()

# AI Summary
print("\n[4] AI Summary...")
r = requests.post(f"{API_BASE}/refine/summarize", json={"markdown": markdown}, timeout=120)
if r.status_code == 200:
    print(f"[OK] Summary: {r.json()['summary'][:150]}...")

# AI Formalize
print("\n[5] AI Formalize...")
r = requests.post(f"{API_BASE}/refine/formalize", json={"markdown": markdown[:1000]}, timeout=120)
if r.status_code == 200:
    print(f"[OK] Formalized: {r.json()['markdown'][:150]}...")

# RAG Chat
print("\n[6] RAG Chat...")
r = requests.post(f"{API_BASE}/chat", json={"message": "What is this document about?"}, timeout=120)
if r.status_code == 200:
    chat = r.json()
    print(f"[OK] Response: {chat['message']['content'][:150]}...")
    print(f"[OK] Sources: {chat['num_documents']}")

print("\n" + "="*60)
print("[SUCCESS] All tests passed!")
print("="*60)

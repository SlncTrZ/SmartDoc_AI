"""Backend: Simple Test — Test document processing without unicode issues."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from processor import DocumentProcessor
from vector_storage import VectorStorage


def main():
    print("="*60)
    print("SMARTDOC AI - SIMPLE TEST")
    print("="*60)

    test_file = "../test/ARTIFICIAL INTELLIGENCE.pdf"

    if not os.path.exists(test_file):
        print(f"[ERROR] Test file not found: {test_file}")
        return

    print(f"\n[File] Testing with: {test_file}")

    print("\n[Init] Initializing components...")
    processor = DocumentProcessor()
    storage = VectorStorage()

    storage.ensure_wings()
    print("[OK] Wings created")

    print("\n[Process] Testing Docling extraction...")
    try:
        result = processor.process_file(test_file)

        if result['success']:
            print("[OK] Processing successful!")
            print(f"   Pages: {result['metadata'].get('page_count', 'N/A')}")
            print(f"   Format: {result['metadata'].get('format', 'N/A')}")
            print(f"   Size: {result['metadata'].get('file_size', 0)} bytes")

            markdown_preview = result['markdown'][:500]
            print(f"\n[Preview] First 500 chars:")
            print("-"*60)
            print(markdown_preview)
            print("-"*60)

            # Store in LanceDB
            print("\n[Storage] Testing LanceDB...")
            import json
            doc_data = {
                'id': f"test_{os.path.basename(test_file)}",
                'filename': os.path.basename(test_file),
                'markdown': result['markdown'],
                'metadata': json.dumps(result['metadata']),
                'embedding': [0.0] * 1536,
                'wing': 'tai_lieu_khac',
                'created_at': '2026-05-05'
            }

            storage.add_document('tai_lieu_khac', doc_data)
            print("[OK] Document stored!")

            count = storage.get_document_count('tai_lieu_khac')
            print(f"[Stats] Documents in wing: {count}")

            print("\n"+ "="*60)
            print("[SUCCESS] All tests passed!")
            print("="*60)
            print("\n[Backend] Ready for Phase 2 (Electron)")

        else:
            print("[ERROR] Processing failed!")
            print(f"   Error: {result['metadata'].get('error', 'Unknown')}")

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

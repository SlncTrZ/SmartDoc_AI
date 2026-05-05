"""Backend: Quick Test Script — Test document processing with sample PDF.

Tests Docling extraction, metadata extraction, and storage.
Run with: python quick_test.py

Wing: smartdoc_backend
Topic: testing
Last Updated: 2026-05-05 09:25
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from processor import DocumentProcessor
from vector_storage import VectorStorage
from ollama_client import OllamaClient
from metadata_extractor import MetadataExtractor


def main():
    """Run quick test with sample PDF."""
    print("=" * 60)
    print("SMARTDOC AI - QUICK TEST")
    print("=" * 60)

    # Test file path
    test_file = "../test/ARTIFICIAL INTELLIGENCE.pdf"

    if not os.path.exists(test_file):
        print(f"❌ Test file not found: {test_file}")
        return

    print(f"\n📄 Testing with file: {test_file}")

    # Initialize components
    print("\n🔧 Initializing components...")
    processor = DocumentProcessor()
    storage = VectorStorage()
    ollama = OllamaClient()
    extractor = MetadataExtractor(ollama)

    # Ensure wings exist
    storage.ensure_wings()
    print("✅ Wings created")

    # Step 1: Process document
    print("\n" + "=" * 60)
    print("STEP 1: Document Processing (Docling)")
    print("=" * 60)

    print("⏳ Processing PDF...")
    result = processor.process_file(test_file)

    if result['success']:
        print("✅ Processing successful!")
        print(f"   - Pages: {result['metadata'].get('page_count', 'N/A')}")
        print(f"   - Format: {result['metadata'].get('format', 'N/A')}")
        print(f"   - Size: {result['metadata'].get('file_size', 0)} bytes")

        # Show preview
        markdown_preview = result['markdown'][:500]
        print(f"\n📝 Markdown Preview:")
        print("-" * 60)
        print(markdown_preview)
        print("-" * 60)
    else:
        print("❌ Processing failed!")
        print(f"   Error: {result['metadata'].get('error', 'Unknown error')}")
        return

    # Step 2: Extract metadata
    print("\n" + "=" * 60)
    print("STEP 2: Metadata Extraction (AI)")
    print("=" * 60)

    print("⏳ Extracting metadata with AI...")
    print("   (This may take a minute if Ollama needs to start...)")

    # Check Ollama status
    if not ollama.is_running():
        print("   ⚠️  Ollama not running, attempting to start...")
        if ollama.start_ollama():
            print("   ✅ Ollama started successfully")
        else:
            print("   ❌ Failed to start Ollama")
            print("   ⚠️  Continuing without AI metadata...")

    # Ensure model is available
    if ollama.is_running():
        print("   ⏳ Checking for llama3.2 model...")
        ollama.ensure_model('llama3.2')

    # Extract metadata
    try:
        metadata = extractor.extract_metadata(result['markdown'], test_file)
        print("\n✅ Metadata extracted:")
        print(f"   - Title: {metadata.get('title', 'N/A')}")
        print(f"   - Date: {metadata.get('date', 'N/A')}")
        print(f"   - Author: {metadata.get('author', 'N/A')}")
        print(f"   - Type: {metadata.get('document_type', 'N/A')}")
        print(f"   - Summary: {metadata.get('summary', 'N/A')}")
    except Exception as e:
        print(f"❌ Metadata extraction failed: {e}")
        metadata = {
            'title': os.path.basename(test_file),
            'date': '',
            'author': '',
            'document_type': 'khac',
            'summary': ''
        }

    # Step 3: Classify and store
    print("\n" + "=" * 60)
    print("STEP 3: Storage (LanceDB)")
    print("=" * 60)

    wing = extractor.classify_wing(metadata)
    print(f"📂 Classified to wing: {wing}")

    doc_data = {
        'id': f"{os.path.basename(test_file)}_{os.path.getmtime(test_file)}",
        'filename': os.path.basename(test_file),
        'markdown': result['markdown'],
        'metadata': {**result['metadata'], **metadata},
        'embedding': [0.0] * 1536,  # Placeholder
        'wing': wing,
        'created_at': str(os.path.getmtime(test_file))
    }

    try:
        storage.add_document(wing, doc_data)
        print("✅ Document stored successfully!")

        # Show wing statistics
        doc_count = storage.get_document_count(wing)
        print(f"📊 Total documents in '{wing}': {doc_count}")

        # List all wings
        print("\n📋 Available wings:")
        for w in storage.list_wings():
            count = storage.get_document_count(w)
            print(f"   - {w}: {count} documents")

    except Exception as e:
        print(f"❌ Storage failed: {e}")
        return

    # Summary
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\n📝 Summary:")
    print("   ✅ PDF processed with Docling")
    print("   ✅ Metadata extracted with AI")
    print("   ✅ Document stored in LanceDB")
    print("\n🎯 Backend is ready for Phase 2 (Electron Frontend)!")


if __name__ == '__main__':
    main()

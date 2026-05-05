"""Backend: RAG Documentation — Setup and usage guide for RAG pipeline.

Explains how to install embedding models and use RAG features.

Wing: smartdoc_backend
Topic: rag_documentation
Last Updated: 2026-05-05 10:00
"""

# RAG Pipeline - Setup Guide

## Overview
The RAG (Retrieval-Augmented Generation) pipeline enables semantic search and AI-powered document Q&A.

## Components

### 1. Embedding Service (`embedding_service.py`)
- Generates vector embeddings using Ollama
- Splits documents into chunks
- Supports batch embedding generation

### 2. RAG Pipeline (`rag_pipeline.py`)
- Retrieves relevant documents using semantic search
- Generates context-aware AI responses
- Combines retrieval and generation

### 3. Vector Storage (`vector_storage.py`)
- Stores documents with embeddings in LanceDB
- Supports semantic search queries
- Manages document wings (categories)

## Installation

### 1. Install Ollama Embedding Model

The system needs an embedding model. Choose one:

```bash
# Option 1: mxbai-embed-large (recommended, 1536 dimensions)
ollama pull mxbai-embed-large

# Option 2: nomic-embed-text (lighter, 768 dimensions)
ollama pull nomic-embed-text

# Option 3: all-minilm (very light, 384 dimensions)
ollama pull all-minilm
```

### 2. Configure Model in Code

Edit `embedding_service.py` if using a different model:

```python
self.embedding_model = "mxbai-embed-large"  # Change this
```

## Usage

### Basic RAG Query

```python
from rag_pipeline import RAGPipeline
from embedding_service import EmbeddingService
from vector_storage import VectorStorage
from ollama_client import OllamaClient

# Initialize
embedding_service = EmbeddingService()
storage = VectorStorage()
ollama = OllamaClient()
rag = RAGPipeline(embedding_service, storage, ollama)

# Query
result = rag.query(
    query="What is the document about?",
    wings=['tai_lieu_khac'],
    limit=5
)

print(result['response'])  # AI response
print(result['sources'])   # Source documents
```

### Process Document with Embeddings

```python
# API endpoint: POST /api/process
{
  "file_path": "C:/path/to/document.pdf",
  "embed": true  # Generate embeddings for RAG
}

# Response includes:
{
  "success": true,
  "markdown": "...",
  "metadata": {...},
  "wing": "tai_lieu_khac",
  "chunks_embedded": 5  # Number of chunks stored
}
```

### Chat with RAG

```python
# API endpoint: POST /api/chat
{
  "message": "What are the key points in this document?",
  "wings": ["tai_lieu_cong_van"]  # Optional: specific wings to search
}

# Response includes:
{
  "message": {
    "role": "assistant",
    "content": "Based on the documents..."
  },
  "sources": [
    {
      "filename": "document.pdf",
      "wing": "tai_lieu_cong_van",
      "score": 0.85
    }
  ],
  "num_documents": 3
}
```

## Architecture

```
User Query
    |
    v
Embedding Service (Ollama)
    |
    v
Vector Search (LanceDB)
    |
    v
Retrieve Top K Documents
    |
    v
RAG Generation (Ollama LLM)
    |
    v
AI Response with Sources
```

## Testing

Run the simple test:

```bash
cd backend
venv\Scripts\python.exe simple_rag_test.py
```

Expected output:
- [OK] Embedding generated: 1536 dimensions
- [OK] Documents added
- [OK] Retrieved results with scores
- [OK] RAG query response

## Troubleshooting

### Error: "Embedding error: 404"
**Cause**: Embedding model not installed in Ollama
**Solution**: Run `ollama pull mxbai-embed-large`

### Error: "No documents found"
**Cause**: No documents with embeddings in database
**Solution**: Process documents with `embed: true` flag

### Poor retrieval quality
**Cause**: Documents not properly chunked or embedded
**Solution**:
1. Check chunk size (default: 1000 chars)
2. Verify embedding model quality
3. Increase `limit` parameter in queries

### Slow response time
**Cause**: Large documents or slow embedding generation
**Solution**:
1. Use lighter embedding model (nomic-embed-text)
2. Reduce chunk size
3. Cache embeddings for frequently accessed documents

## Performance Optimization

### Chunking Strategy
- Smaller chunks (500-800 chars): More precise retrieval
- Larger chunks (1000-1500 chars): Better context, faster
- Default: 1000 chars with 100 char overlap

### Retrieval Parameters
- `limit=3`: Fast, fewer sources
- `limit=5`: Balanced
- `limit=10`: Comprehensive, slower

### Model Selection
- `mxbai-embed-large`: Best quality, 1536 dims
- `nomic-embed-text`: Good balance, 768 dims
- `all-minilm`: Fastest, 384 dims

## Next Steps

1. **Reindex existing documents**:
   - Use `rag_enhancement.py` to add embeddings to old documents

2. **Fine-tune chunking**:
   - Adjust `chunk_size` and `overlap` based on document types

3. **Customize prompts**:
   - Edit RAG prompts in `rag_pipeline.py` for specific domains

4. **Monitor performance**:
   - Track retrieval accuracy and response times
   - Adjust parameters based on user feedback

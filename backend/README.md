# Backend Setup Instructions

## Prerequisites
- Python 3.10 or higher
- Ollama installed (https://ollama.ai)
- Git

## Installation Steps

### 1. Create Virtual Environment
```powershell
cd H:\Develop\SmartDoc_AI\backend
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Install Ollama Models (if not already installed)
```powershell
# Pull Llama 3.2 for chat
ollama pull llama3.2

# Pull embedding model (if available)
# ollama pull mxbai-embed-large
```

### 4. Test Processing
```powershell
# Run tests
python test_backend.py

# Or use pytest
pip install pytest
pytest test_backend.py
```

### 5. Start Server
```powershell
python app.py
```

Server will start on http://127.0.0.1:5000

## API Endpoints

### Health Check
```
GET /api/health
```

### Process File
```
POST /api/process
Content-Type: application/json
{
  "file_path": "C:/path/to/document.pdf"
}
```

### List Wings
```
GET /api/wings
```

### Start Ollama
```
POST /api/ollama/start
```

### Chat
```
POST /api/chat
Content-Type: application/json
{
  "message": "What is this document about?",
  "context": ["Document content..."]
}
```

## Directory Structure
```
backend/
├── app.py                 # Flask API server
├── processor.py           # Docling document processor
├── vector_storage.py     # LanceDB operations
├── ollama_client.py       # Ollama API client
├── metadata_extractor.py  # AI metadata extraction
├── test_backend.py        # Unit tests
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Troubleshooting

### Ollama not starting
- Check if Ollama is installed: `ollama --version`
- Try starting manually: `ollama serve`

### Docling errors
- Ensure sufficient RAM (4GB+ recommended)
- Try processing smaller files first

### Port 5000 already in use
- Change port in app.py (line 180)
- Or stop conflicting service

## Next Steps
- Test with real company PDFs
- Integrate with Electron frontend
- Implement RAG pipeline

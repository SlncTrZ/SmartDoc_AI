# Frontend Setup Instructions

## Prerequisites
- Node.js 18+ installed
- Python backend setup completed (see backend/README.md)

## Installation

### 1. Install Dependencies
```powershell
cd H:\Develop\SmartDoc_AI\frontend
npm install
```

### 2. Build React Components
```powershell
node build-react.js
```

### 3. Start Application
```powershell
npm start
```

## Development

### Rebuild React after changes
```powershell
node build-react.js
npm start
```

### Open DevTools (for debugging)
Set environment variable:
```powershell
$env:NODE_ENV="development"
npm start
```

## Project Structure
```
frontend/
├── main.js              # Electron main process
├── preload.js           # Security bridge
├── build-react.js       # Build script
├── package.json         # Dependencies & scripts
├── public/
│   ├── index.html       # HTML entry point
│   └── app.js          # Bundled React app
└── src/
    ├── components/      # React components
    │   ├── App.js
    │   ├── TabInput.js
    │   ├── TabPreview.js
    │   └── TabRag.js
    └── services/
        └── api.js       # Backend API client
```

## Features Implemented

### Tab 1: Input & Scan
- Drag & drop file upload
- File list display
- Processing progress indicator
- Integration with Python backend

### Tab 2: Preview & Refine
- Document list sidebar
- Markdown preview
- Metadata editing (title, date, author, wing)
- AI assistant placeholder

### Tab 3: RAG Chat
- Chat interface (Zalo-like)
- Document context display
- Source citations
- Real-time messaging

## Troubleshooting

### App won't start
- Check if Python backend is running (port 5000)
- Verify Ollama is installed and running
- Check Electron console logs (DevTools)

### Files not processing
- Check backend API: http://127.0.0.1:5000/api/health
- Verify file paths are correct
- Check Python logs in backend/logs/server.log

### Build errors
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Clear React bundle: `rm public/app.js`

## Next Steps

1. **Testing**: Run full app with real PDF files
2. **AI Integration**: Complete Ollama RAG pipeline
3. **Embedding**: Implement vector search with LanceDB
4. **Packaging**: Create Windows installer with electron-builder

## Electron Security

- Context isolation enabled
- Node integration disabled
- Safe IPC via preload.js
- Content Security Policy configured

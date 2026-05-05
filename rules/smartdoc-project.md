---
name: smartdoc-project
description: Project-specific rules for SmartDoc AI - Document management system
---

## SMARTDOC PROJECT RULES

### Project Context
- **Type**: Desktop Electron App + Python Sidecar
- **Purpose**: Local-first document management with AI
- **Target Users**: Office workers (non-technical)
- **Repository**: https://github.com/truongcongdinh97/SmartDoc_AI

### Wing Mapping (SmartDoc Specific)
| Wing | Collection | Mục đích |
|------|-----------|---------|
| `smartdoc_backend` | `meilin_smartdoc_backend` | Python core, Docling, LanceDB, Ollama integration |
| `smartdoc_frontend` | `meilin_smartdoc_frontend` | Electron UI, React components, state management |
| `smartdoc_architecture` | `meilin_smartdoc_architecture` | System design, data pipeline, deployment |

### Technical Stack
- **Backend**: Python 3.10+, Docling, LanceDB, Ollama
- **Frontend**: Electron.js, React, TailwindCSS
- **Packaging**: PyInstaller (Python), electron-builder (Electron)
- **Storage**: LanceDB (serverless, file-based)

### Code Organization
```
SmartDoc_AI/
├── backend/
│   ├── processor.py      # Docling extraction
│   ├── vector_storage.py # LanceDB operations
│   ├── ollama_client.py  # AI integration
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
├── docs/
│   ├── PLAN.md
│   ├── UIUX_PLAN.md
│   └── ARCHITECTURE.md
└── rules/
    └── smartdoc-project.md
```

### Module Docstring (SmartDoc Format)
```python
"""Backend: Document Processor — Extracts PDF/DOCX using Docling.

Handles file input, Docling API calls, markdown conversion.
Integrates with vector_storage for persistence.

Wing: smartdoc_backend
Topic: document_processing
Last Updated: YYYY-MM-DD HH:MM
"""
```

```javascript
/**
 * Frontend: Document Card Component — Displays processed documents.
 *
 * Renders document metadata, preview, and action buttons.
 * Integrates with Drag & Drop API.
 *
 * Wing: smartdoc_frontend
 * Topic: ui_components
 * Last Updated: YYYY-MM-DD HH:MM
 */
```

### Development Phases (Sequential)
1. **Phase 1**: Backend Core (Python scripts)
2. **Phase 2**: Frontend UI (Electron app)
3. **Phase 3**: RAG Integration
4. **Phase 4**: Packaging & Deployment

### Critical Rules
1. **Local-First**: No cloud dependencies, everything runs offline
2. **On-Demand Processing**: Only process when user interacts
3. **User-Friendly**: All errors in Vietnamese, no tech jargon
4. **Memory Management**: LanceDB stores by Wings (Tables)
5. **Ollama Auto-Start**: Check port 11434 on app launch

### UI/UX Constraints (from UIUX_PLAN.md)
- Font size: 14pt-16pt minimum
- Primary color: #0056b3 (Office blue)
- Loading messages: Vietnamese, descriptive
- No CLI/Console visible to users
- Click-only workflow (keyboard optional)

### Knowledge Store Protocol
After each code change:
- Call `meilin-brain:knowledge_store`
- Wing: `smartdoc_backend` OR `smartdoc_frontend`
- Topic: `document_processing|ui_components|rag_integration|packaging`
- Entity: `function_name|ComponentName|concept`
- Importance: `high` (core logic) OR `medium` (UI) OR `low` (helpers)

### Testing Strategy
- Backend: Unit tests for Docling extraction, LanceDB CRUD
- Frontend: Component tests, Drag & Drop tests
- Integration: End-to-end PDF → Vector → RAG flow
- User Acceptance: Test with actual office workers (50+ age)

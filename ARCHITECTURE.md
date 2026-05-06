# ARCHITECTURE — SmartDoc AI (Cloud-First Hybrid)

## 1. Tổng quan
Cloud-First Hybrid: mặc định dùng DeepSeek/NotebookLM, fallback local (pypdf/Docling).
Sidecar Processes chạy local cùng Electron — không phụ thuộc server ngoài.

## 2. Kiến trúc

```
┌──────────────────────────────────────────────────────────────────┐
│                     SmartDoc AI (Electron)                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Splash Screen → Hardware Detection → User Name/Position         │
│       │                                                          │
│       ▼                                                          │
│  Main UI (3 tabs)                                                │
│  ┌──────────┬─────────────┬──────────────┐                      │
│  │ 📥 Upload │ 📝 Preview  │ 💬 Chat       │                      │
│  │ 3 Modes:  │ AI Assistant│ Dual AI      │                      │
│  │ ⚡Nhanh   │ 🔭DeepSeek  │ 🔭DeepSeek   │                      │
│  │ ☁️Cloud   │ 🖨Ollama    │ 🖨Ollama     │                      │
│  │ 🔬Nâng cao│             │              │                      │
│  └────┬─────┴──────┬──────┴──────┬───────┘                      │
│       │            │             │                               │
│       ▼            ▼             ▼                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                          │
│  │ Pipeline │ │ LanceDB  │ │ RAG Chat │                          │
│  │ pypdf    │ │ Storage  │ │ ds2api   │                          │
│  │ RapidOCR │ │          │ │ Ollama   │                          │
│  │ Docling  │ │          │ │          │                          │
│  └──────────┘ └──────────┘ └──────────┘                          │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │ SidecarManager (Electron Main Process)                    │    │
│  │ ├── Flask Backend (port 5000+, --port argument)           │    │
│  │ ├── hardware_check.py (GPUtil → GPU/VRAM)                │    │
│  │ └── findFreePort() → dynamic port allocation              │    │
│  └──────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

## 3. Xử lý tài liệu (3-tier)

| Mode | Pipeline | Tốc độ | Phụ thuộc |
|------|----------|--------|-----------|
| ⚡ Nhanh (Auto) | pypdf → RapidOCR → Docling | ~0.2s | Python, CPU |
| ☁️ Cloud | NotebookLM bridge | nhanh | Google login |
| 🔬 Nâng cao | Docling full | chậm | GPU (optional) |

## 4. AI Providers

| AI Task | Mặc định | Fallback | Chọn thủ công |
|---------|---------|----------|--------------|
| Chat (RAG) | DeepSeek (ds2api) | Ollama | ✅ Tab Chat |
| Tóm tắt tài liệu | DeepSeek | Ollama | ✅ Tab Preview |
| Viết lại trang trọng | DeepSeek | Ollama | ✅ Tab Preview |
| Yêu cầu tùy chỉnh | DeepSeek | Ollama | ✅ Tab Preview |

## 5. Công nghệ
- Frontend: Electron 30 + React 18 + Tailwind CSS + WebView
- Backend: Python Flask + LanceDB + ds2api + Docling + LightweightProcessor
- Xử lý PDF: pypdf (text), RapidOCR (scan), Docling (layout, GPU)
- AI: DeepSeek Web (ds2api) + Ollama (Gemma4, nomic-embed-text)
- Build: Electron-Builder (future), Node.js build-react.js + Babel

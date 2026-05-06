# PROJECT IMPLEMENTATION PLAN (V3 - Cloud-First Hybrid)

## Phase 1: Hardware Check & Dashboard ✅
- [x] Splash Screen: Quét GPU/VRAM (GPUtil Python) + chờ user nhập Tên/Chức vụ
- [x] 3-mode toggle: Nhanh (pypdf→OCR→Docling) / Cloud (NotebookLM) / Nâng cao (Docling)
- [x] Sidecar Manager: child_process.spawn quản lý vòng đời Python process
- [x] Dynamic port allocation (5000+)
- [x] Custom Upload UI + WebView ẩn điều phối

## Phase 2: ds2api Chat ✅
- [x] Bundle ds2api Python scripts
- [x] WebView login: DeepSeek + Google, lưu session cookie vào %APPDATA%
- [x] ds2api + Ollama dual provider, user tự chọn
- [x] Dual-provider RAG (LanceDB → ds2api/Ollama → trả lời)
- [x] DocumentRefiner: DeepSeek mặc định, Ollama fallback

## Phase 3: NotebookLM-MCP Standardizer ⏳
- [ ] Bundle portable Chromium + Playwright
- [ ] Custom Upload UI: User login Google, chọn tài liệu
- [ ] NotebookLM export .md → lưu vào LanceDB

## Phase 4: Docling Local Fallback ✅
- [x] 3-tier pipeline: pypdf (Nhanh) → RapidOCR (scan) → Docling (enhanced)
- [x] Chunking: tự động split markdown thành chunks ~2000 chars
- [x] Lazy init Docling (processor = None, load khi cần)
- [x] Skip metadata/embedding nếu Ollama offline

## Pending
- [ ] NotebookLM-MCP integration
- [ ] Electron-Cloudflare Tunnel (.truongcongdinh.org)
- [ ] Electron-Builder packaging

## Kiến trúc hiện tại
- Frontend: Electron 30 + React 18 + Tailwind CSS + WebView
- Backend: Python Flask + LanceDB + ds2api + Docling + LightweightProcessor
- AI: DeepSeek (ds2api) mặc định, Ollama fallback
- Xử lý tài liệu: pypdf (0.2s) → RapidOCR (scan) → Docling (GPU)

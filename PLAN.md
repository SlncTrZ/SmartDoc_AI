# PROJECT IMPLEMENTATION PLAN (V2 - Hybrid + Sidecar)

## Phase 1: Hardware Check & Dashboard (UI/UX Core)
- [ ] Xây dựng Splash Screen: Quét GPU/VRAM (GPUtil Python)
- [ ] Dashboard chọn chế độ: Local / Hybrid
- [ ] Sidecar Manager: child_process.spawn quản lý vòng đời Python process
- [ ] Custom Upload UI (giả lập notebookLM) + WebView ẩn điều phối

## Phase 2: ds2api Chat (Sidecar Python)
- [ ] Bundle ds2api Python scripts
- [ ] WebView ẩn: User login DeepSeek -> lưu session cookie
- [ ] ds2api tự động cào web, chat với context từ LanceDB
- [ ] Chat UI với RAG (LanceDB -> ds2api -> trả lời)

## Phase 3: NotebookLM-MCP Standardizer
- [ ] Bundle portable Chromium + Playwright
- [ ] Custom Upload UI: User login Google, chọn tài liệu
- [ ] NotebookLM export .md -> lưu vào LanceDB

## Phase 4: Docling Local Fallback
- [ ] On-demand download model weights (~2GB) khi chọn Local Mode
- [ ] Progress bar: "Đang tải bộ não xử lý tài liệu..."
- [ ] OCR fallback khi notebookLM offline / không có internet

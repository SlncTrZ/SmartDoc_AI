# ARCHITECTURE - SmartDoc AI Hybrid + Sidecar

## 1. Tổng quan
Modular Hybrid: tự động điều chỉnh luồng xử lý dựa trên phần cứng.
Dùng Sidecar Processes (Python) chạy local cùng Electron - không phụ thuộc server ngoài.

## 2. Kiến trúc

`
┌─────────────────────────────────────────────────────────┐
│                    SmartDoc AI (Electron)                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐    ┌──────────────────────────────┐    │
│  │  Splash       │───▶│  Hardware Detection           │    │
│  │  Screen       │    │  GPU >= 6GB -> Local Ollama    │    │
│  │  (GPU/VRAM)   │    │  No GPU -> Hybrid Mode        │    │
│  └──────────────┘    └──────────┬───────────────────┘    │
│                                ▼                         │
│                   ┌─────────────────────┐                │
│                   │  Hybrid Dashboard    │                │
│                   └─────────┬───────────┘                │
│                            │                             │
│         ┌──────────────────┴──────────────────┐          │
│         ▼                                     ▼          │
│  ┌──────────────┐                      ┌──────────────┐  │
│  │ [B] Upload   │                      │ [A] Chat     │  │
│  │ Custom UI    │                      │ ds2api       │  │
│  │ -> WebView ẩn│                      │ -> WebView ẩn│  │
│  │ -> Login     │                      │ -> Login     │  │
│  │   Google     │                      │   DeepSeek   │  │
│  │ -> NotebookLM│                      │ -> Context   │  │
│  │ -> Export .md│                      │   LanceDB    │  │
│  └──────┬───────┘                      └──────┬───────┘  │
│         │                                     │         │
│         ▼                                     │         │
│  ┌──────────────┐                             │         │
│  │ LanceDB      │◀────────────────────────────┘         │
│  │ (Vector DB)  │  Context cho RAG Chat                  │
│  │ + Docling    │                                       │
│  │ (Fallback)   │                                       │
│  └──────────────┘                                       │
└─────────────────────────────────────────────────────────┘
`

## 3. Sidecar Processes
Chạy local cùng Electron, spawn bằng child_process.spawn (main process).

| Process | Công nghệ | Chức năng |
|---------|-----------|-----------|
| ds2api | Python | LLM Inference qua DeepSeek Web |
| notebooklm-mcp | CLI + Playwright + Chromium | PDF -> Markdown chuẩn |
| Docling (fallback) | Python + Model weights | OCR local khi offline |
| Ollama | Go binary | Local LLM (chỉ khi GPU >= 6GB) |

## 4. Luồng dữ liệu
1. Upload (Hybrid): User chọn file -> WebView ẩn -> notebookLM export .md -> lưu LanceDB
2. Upload (Local): User chọn file -> Docling OCR -> Markdown -> lưu LanceDB
3. Chat: User hỏi -> LanceDB search context -> ds2api + context -> trả lời
4. Fallback: notebookLM lỗi -> tự động chuyển Docling. ds2api lỗi -> chuyển Ollama

## 5. Công nghệ
- Frontend: Electron 30 + React 18 + Tailwind CSS + WebView
- Backend: Python Flask + LanceDB + ds2api + notebooklm-mcp + Docling
- Đóng gói: Electron-Builder + bundle Python runtime + portable Chromium
- Model weights: On-demand download (~2GB, chỉ khi Local Mode)

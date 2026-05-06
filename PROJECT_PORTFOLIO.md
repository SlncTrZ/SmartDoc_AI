# PROJECT PORTFOLIO: SmartDoc AI (Hybrid + Sidecar Edition)

## 1. Giới thiệu
SmartDoc AI - giải pháp quản trị tri thức nội bộ cho doanh nghiệp.
Adaptive AI, tự động điều chỉnh luồng xử lý dựa trên phần cứng người dùng.
Chạy tốt trên cả máy tính văn phòng không GPU lẫn máy trạm cao cấp.

## 2. Vấn đề giải quyết
- Phần cứng không đồng nhất: Máy văn phòng thường không GPU.
- Chi phí API: Giải pháp Cloud chính thống tốn kém.
- Bảo mật & Tiện ích: Cân bằng giữa Local (bảo mật) và Cloud (sức mạnh AI).
- Rào cản số lượng: Document processing không giới hạn nhờ notebookLM.

## 3. Kiến trúc
Sidecar Architecture: Mọi AI service chạy local cùng Electron.

| Kênh | Công nghệ | Khi nào dùng |
|------|-----------|-------------|
| Hardware Check | GPUtil (Python) | Splash Screen đầu tiên |
| LLM Chat | ds2api (Python) -> DeepSeek | Luôn dùng (Hybrid) |
| Document Standardizer | notebookLM-mcp + Chromium | Có internet |
| Document Fallback | Docling + Model weights | Offline / notebookLM lỗi |
| Vector DB | LanceDB | Local storage |
| Local LLM | Ollama | GPU >= 6GB |

## 4. Tính năng nổi bật
- Hardware Setup Wizard: Auto-detect GPU/VRAM -> đề xuất chế độ
- ds2api Integration: DeepSeek free qua tài khoản cá nhân
- Cloud Standardizer: NotebookLM -> .md -> LanceDB
- Docling Fallback: OCR local khi offline
- On-demand Weights: Chỉ tải model 2GB khi cần Local Mode

## 5. Kết quả mong đợi
- 100% tương thích mọi cấu hình văn phòng
- Giảm ~90% chi phí API AI
- Xử lý không giới hạn số lượng tài liệu
- Một .exe duy nhất, người dùng chỉ cần cài và chạy

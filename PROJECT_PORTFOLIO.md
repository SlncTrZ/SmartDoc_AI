# PROJECT PORTFOLIO: SmartDoc AI (Cloud-First Edition)

## 1. Giới thiệu
SmartDoc AI — giải pháp quản trị tri thức nội bộ cho doanh nghiệp.
Cloud-First Hybrid: ưu tiên xử lý qua Cloud (DeepSeek + NotebookLM), fallback local.
Chạy trên mọi cấu hình máy tính văn phòng.

## 2. Vấn đề giải quyết
- **Phần cứng yếu:** Máy văn phòng không GPU → dùng Cloud AI
- **Chi phí API:** Tận dụng DeepSeek + NotebookLM miễn phí
- **Bảo mật:** Local fallback khi cần, không bắt buộc Cloud
- **Số lượng lớn:** Xử lý không giới hạn nhờ Cloud

## 3. Tính năng
| Tính năng | Mô tả |
|-----------|-------|
| 3-mode Upload | Nhanh (pypdf), Cloud (NotebookLM), Nâng cao (Docling) |
| AI Chat | RAG với LanceDB + DeepSeek/Ollama |
| AI Assistant | Tóm tắt, viết lại, yêu cầu tùy chỉnh |
| Splash Screen | Nhập Tên/Chức vụ, phát hiện GPU |
| WebView Login | DeepSeek + Google (lưu session) |
| Huỷ xử lý | Cancel button + AbortController |

## 4. Kiến trúc
- Frontend: Electron 30 + React 18 + Tailwind CSS
- Backend: Python Flask + LanceDB (vector DB)
- AI: DeepSeek Web (ds2api) + Ollama (Gemma4)
- Document: pypdf (text) → RapidOCR (scan) → Docling (layout)

## 5. Kết quả mong đợi
- 100% tương thích mọi cấu hình văn phòng
- Giảm ~90% chi phí AI nhờ DeepSeek miễn phí
- Xử lý tài liệu không giới hạn
- Một .exe duy nhất, click để chạy

# ARCHITECTURE - AI Document Standardizer & RAG

## 1. Tổng quan hệ thống
Hệ thống được thiết kế theo mô hình **Local-first**, đảm bảo bảo mật dữ liệu nội bộ công ty. Ứng dụng chạy độc lập trên Desktop, không yêu cầu kỹ năng CLI.

## 2. Các thành phần chính (Tech Stack)
*   **Frontend**: Electron.js (UI/UX thân thiện, đóng gói .exe).
*   **Core Engine (Python Sidecar)**: 
    *   **Docling (IBM)**: Trích xuất PDF/DOCX sang Markdown (giữ nguyên layout/table).
    *   **LanceDB**: Vector Database dạng Serverless (lưu trữ cục bộ dưới dạng file).
*   **AI Orchestrator**: Ollama (chạy Local API tại port 11434).
    *   *Models đề xuất*: Llama 3.2 (3B) cho xử lý ngôn ngữ, Moondream2 cho Vision, mxbai-embed-large cho Embedding.

## 3. Luồng dữ liệu (Data Pipeline)
1. **Input**: User chọn Folder/File thông qua giao diện Electron.
2. **Processing (On-demand)**: 
   - Electron gọi Python Sidecar thực thi Docling.
   - Trích xuất nội dung sang định dạng Markdown chuẩn.
3. **Structuring**: 
   - Ollama đọc lướt Markdown để trích xuất Metadata (Tiêu đề, Tác giả, Loại tài liệu).
   - Metadata được gán vào Header của file .md.
4. **Vectorization & Storage**:
   - Chuyển Markdown thành Vector qua Embedding Model.
   - Lưu đồng thời vào LanceDB (chia theo các "Wings" - phân loại tài liệu).
5. **RAG (Retrieval-Augmented Generation)**:
   - Người dùng đặt câu hỏi -> Search Vector trong LanceDB -> Gửi Context vào Ollama -> Trả lời kết quả.

## 4. Quản lý Ollama
- App khởi động -> Check cổng 11434.
- Nếu không phản hồi -> Gửi lệnh hệ thống (`child_process`) để khởi chạy Ollama App/Service.
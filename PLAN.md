# PROJECT IMPLEMENTATION PLAN
Link repo vừa tạo: https://github.com/truongcongdinh97/SmartDoc_AI
## Giai đoạn 1: Xây dựng Backend Core (Python)

* \[ ] Cấu hình môi trường Python với `docling`, `lancedb`, `ollama-python`.
* \[ ] Viết script `processor.py`: Nhận input path -> Docling trích xuất -> Return Markdown.
* \[ ] Viết script `vector\_storage.py`: Khởi tạo LanceDB, tạo schema lưu trữ metadata và vector.
* \[ ] Kiểm thử khả năng trích xuất bảng biểu từ PDF thực tế của công ty.

## Giai đoạn 2: Xây dựng Frontend (Electron)

* \[ ] Thiết kế UI: Layout 2 cột (Trái: Danh mục/Wings - Phải: Nội dung/Chat).
* \[ ] Tích hợp tính năng Drag \& Drop file.
* \[ ] Viết logic kiểm tra và tự động khởi chạy Ollama khi mở App.
* \[ ] Kết nối Electron với Python Sidecar (sử dụng `zerorpc` hoặc `http-server` nội bộ).

## Giai đoạn 3: Tối ưu hóa "On-demand" \& RAG

* \[ ] Xây dựng logic: Chỉ OCR/Standardize khi người dùng click vào file cụ thể.
* \[ ] Tích hợp thanh tìm kiếm thông minh (Semantic Search) sử dụng LanceDB.
* \[ ] Thiết kế Prompt Template cho dân văn phòng (giải thích thuật ngữ dễ hiểu).

## Giai đoạn 4: Đóng gói \& Triển khai

* \[ ] Sử dụng `PyInstaller` để đóng gói script Python thành file thực thi.
* \[ ] Sử dụng `Electron-Builder` để đóng gói toàn bộ thành file `.exe` (One-click installer).
* \[ ] Viết hướng dẫn sử dụng cực ngắn (3 bước) cho nhân viên lớn tuổi.



Lời khuyên từ kinh nghiệm thực tế:

Dùng Docling: Bạn nên để nó chạy ở chế độ CPU-only mặc định để tránh lỗi trên các máy văn phòng không có card đồ họa rời (NVIDIA).



Giao diện: Đừng để người dùng thấy "Code" hay "Console". Mọi thông báo lỗi nên được dịch sang tiếng Việt nhẹ nhàng (Ví dụ: "Hệ thống đang khởi động, vui lòng chờ trong giây lát...").



Mempalace logic: Trong LanceDB, bạn hãy map mỗi "Wing" thành một Table riêng biệt. Điều này giúp tốc độ truy vấn nhanh hơn và dễ quản lý quyền truy cập sau này.


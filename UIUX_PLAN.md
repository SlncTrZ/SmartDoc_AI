Đây là file **UIUX_PLAN.md** được thiết kế riêng cho đối tượng người dùng là nhân viên văn phòng lớn tuổi, tập trung vào sự đơn giản, trực quan và loại bỏ hoàn toàn các thuật ngữ kỹ thuật gây khó hiểu.

---

# UI/UX DESIGN PLAN - SmartDoc AI

## 1. Triết lý thiết kế (Design Principles)
*   **Zero Learning Curve**: Người dùng không cần học, chỉ cần nhìn là biết bấm vào đâu.
*   **Office Familiarity**: Sử dụng icon và màu sắc tương đồng với Microsoft Office/Zalo.
*   **Accessibility**: Font chữ to (14pt - 16pt), độ tương phản cao, nút bấm lớn.
*   **No Technical Jargon**: Thay "Vector DB" bằng "Kho lưu trữ", "RAG" bằng "Hỏi đáp", "Standardize" bằng "Chuẩn hóa".

---

## 2. Cấu trúc các Tab chức năng

### Tab 1: Tiếp nhận & Quét (Input & Scan)
*   **Khu vực thả file**: Một vùng lớn ở giữa màn hình với dòng chữ "Kéo thả PDF hoặc Thư mục vào đây".
*   **Danh sách chờ**: Hiển thị các file đã chọn với trạng thái: `Chờ xử lý`, `Đang đọc...`, `Hoàn thành`.
*   **Nút hành động**: Nút **[Bắt đầu chuẩn hóa]** to, màu xanh dương, nằm ở góc dưới bên phải.

### Tab 2: Kiểm duyệt & Chỉnh sửa (Preview & Refine)
Đây là bước quan trọng nhất để đảm bảo chất lượng dữ liệu trước khi lưu.
*   **Bên trái (Danh sách file)**: Các file đã quét xong nhưng chưa lưu vào kho.
*   **Ở giữa (Trình xem văn bản)**: 
    *   Hiển thị nội dung đã trích xuất dưới dạng văn bản sạch (Rich Text).
    *   **Metadata Header**: Hiển thị Tiêu đề, Ngày tháng, Phòng ban dưới dạng các ô nhập liệu (có thể sửa tay nhanh).
*   **Bên phải (Trợ lý AI)**:
    *   Nút **[Yêu cầu AI sửa lại]**: Khi bấm sẽ hiện các lựa chọn nhanh: *"Tóm tắt lại"*, *"Viết lại cho trang trọng hơn"*, *"Trích xuất bảng biểu"*.
    *   Ô chat nhỏ: *"Bạn muốn AI điều chỉnh gì ở văn bản này?"*.
*   **Nút chốt**: **[LƯU VÀO KHO]** (Màu xanh lá - Chỉ khi bấm nút này dữ liệu mới vào LanceDB).

### Tab 3: Tra cứu & Hỏi đáp (RAG Chat)
*   **Giao diện Chat**: Giống Zalo/Messenger.
*   **Nguồn dữ liệu**: Hiển thị các "Ngăn tủ" (Wings) mà AI đang truy xuất thông tin để trả lời.
*   **Trích dẫn**: Khi AI trả lời, phải có nút **[Xem tài liệu gốc]** để người dùng đối chiếu ngay lập tức.

---

## 3. Luồng tương tác người dùng (User Flow)

1.  **Bước 1**: Nhân viên kéo file PDF vào App.
2.  **Bước 2**: Nhấn "Chuẩn hóa". Hệ thống chạy ngầm Docling và Ollama.
3.  **Bước 3**: App tự động chuyển sang Tab **Kiểm duyệt**. Nhân viên đọc nội dung AI vừa trích xuất.
    *   *Nếu chưa ưng ý*: Nhấn "AI sửa lại" -> Ra lệnh -> AI cập nhật bản mới.
    *   *Nếu đã ưng ý*: Nhấn "Lưu vào kho".
4.  **Bước 4**: Khi cần tìm tin, sang Tab **Hỏi đáp** để chat với dữ liệu đã lưu.

---

## 4. Hệ thống thông báo (Feedback System)
*   **Loading**: Không dùng vòng xoay vô hồn. Dùng thanh tiến trình (%) kèm mô tả: *"Đang đọc dữ liệu từ trang 5..."*, *"Đang sắp xếp thông tin vào ngăn tủ..."*.
*   **Thành công**: Hiệu ứng tích xanh nhẹ nhàng.
*   **Lỗi**: Thông báo tiếng Việt dễ hiểu: *"Máy tính đang bận xử lý, vui lòng chờ trong giây lát"* thay vì *"Error 500: Internal Server Error"*.

---

## 5. Quy chuẩn màu sắc & Thành phần (UI Kit)
| Thành phần | Màu sắc (Hex) | Ý nghĩa |
| :--- | :--- | :--- |
| **Primary** | #0056b3 | Xanh công sở - Tin tưởng, chuyên nghiệp |
| **Success** | #28a745 | Lưu trữ thành công |
| **Action** | #ffc107 | AI cần can thiệp / Chỉnh sửa |
| **Background**| #f8f9fa | Xám trắng - Giảm mỏi mắt |

---

## 6. Danh mục kiểm tra (UX Checklist)
- [ ] Font chữ có đủ to cho người trên 50 tuổi không?
- [ ] Các nút bấm có khoảng cách đủ xa để tránh bấm nhầm không?
- [ ] Có thể thực hiện toàn bộ quy trình mà không cần dùng bàn phím (chỉ dùng chuột) không?
- [ ] Ollama có tự khởi động âm thầm mà không hiện cửa sổ đen (CMD) không?
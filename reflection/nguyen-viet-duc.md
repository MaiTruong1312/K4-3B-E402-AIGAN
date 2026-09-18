# Reflection — Nguyễn Viết Đức

Mã học viên: **2A202602732**. Vai trò theo commit: Luồng đánh giá AI, báo cáo CP3 và cập nhật spec CP4.

## Phần việc

| Commit / thời điểm (+07:00) | Phần việc |
|---|---|
| `5696680` — 17/09 20:16 | Tác giả `VietDuc005` chuyển hai artifact CP2 vào `codebase/`; đây là di chuyển file, không phải tạo mới nội dung. |
| `8965379` — 18/09 11:31 | Tác giả `Nguyen Viet Duc` cập nhật tên trong README và giao diện CP2. |
| `5b87c63` — 18/09 14:11 | Chỉnh `ai_service.py` về prompt/rubric, xử lý quyết định và thêm bảng kết quả CP3. |
| `20faf8c` — 18/09 14:22 | Cập nhật spec với trạng thái working slice và kết quả kiểm thử. |

## Bài học từ kiểm thử

GS18 yêu cầu hỏi lại khi lựa chọn đúng nhưng phần giải thích sai. Bảng CP3 lại ghi `DIAGNOSE` và đánh dấu đạt; chưa có toàn bộ output để kiểm tra hành vi hỏi lại. Khi chấm cần xét đủ expected, không chỉ tên decision. Tương tự, 16/16 chỉ là các case chạy được: tính đủ bộ vẫn là 16/22, dưới bar 20/22. Những lần chạy tiếp theo cần lưu output và lý do chấm cho từng case.

## AI hỗ trợ

AI được dùng trong phiên rà hồ sơ chung để đối chiếu Git, kiểm số liệu và biên tập tài liệu. 


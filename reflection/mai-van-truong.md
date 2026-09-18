# Reflection — Mai Văn Trường

Mã học viên: **2A202602983**. Vai trò theo commit: Phát triển ứng dụng, backend/AI và cấu trúc dự án.

## Phần việc

| Commit / thời điểm (+07:00) | Phần việc |
|---|---|
| `29d068a`, `7b99262` — 17/09 | Tạo và chỉnh canvas, xác định người học, pain và lát cắt D2. |
| `f11a890` — 18/09 01:21 | Thêm backend phân tích AI, API, SQLite, cấu hình bài học và kết nối giao diện. |
| `015eb88` — 18/09 20:35 | Tách templates/static, bổ sung truy xuất transcript, lịch sử học, vai trò local và bộ test policy. |

## Bài học từ kiểm thử

GS22 yêu cầu sửa nhận định AI và đánh giá lại, nhưng schema của bản hiện tại chỉ có `initial/retry/transfer`. Bài học ở đây là phải nối từng yêu cầu trong spec với một hành vi kiểm tra được trên ứng dụng. Một luồng chính chạy được chưa đủ để nói rằng cả bốn đường đi đã hoàn thiện. Việc cần ưu tiên tiếp theo là correction và xử lý lỗi trước khi mở rộng tính năng.

## AI hỗ trợ

AI được dùng trong phiên rà hồ sơ chung để đối chiếu Git, kiểm số liệu và biên tập tài liệu. 


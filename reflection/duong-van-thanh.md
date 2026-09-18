# Reflection — Dương Văn Thành

Mã học viên: **2A202602368**. Vai trò theo commit: Đặc tả sản phẩm, canvas và thiết kế golden set.

## Phần việc

| Commit / thời điểm (+07:00) | Phần việc |
|---|---|
| `6441593` — 17/09 19:26 | Rút canvas về bảng 7 dòng, làm rõ evidence, một quyết định AI và phân công. |
| `f368a51` — 17/09 20:37 | Mở rộng `spec.md`, thêm `eval/golden-set.md` với 22 case; nội dung gồm bar, rủi ro và bốn đường đi. |
| `b5642bf` — 17/09 20:37 | Merge nhánh main; không suy ra đây là phần tự viết toàn bộ các thay đổi được hợp nhất. |

## Bài học từ kiểm thử

GS07 yêu cầu dừng đánh giá khi không có nguồn. Bảng CP3 ghi chưa tạo được tình huống này để chạy test. Code có guard thiếu nguồn, nhưng 5 test policy đạt chưa chứng minh được luồng từ tải tài liệu đến hiển thị lỗi. Khi viết golden set, cần ghi rõ cả cách tạo điều kiện lỗi và hành vi mong đợi. Nếu chưa chạy được thì giữ trạng thái đó trong báo cáo, không loại case khỏi mẫu số.

## AI hỗ trợ

AI được dùng trong phiên rà hồ sơ chung để đối chiếu Git, kiểm số liệu và biên tập tài liệu. Chưa có thông tin riêng về công cụ, prompt hoặc đầu ra AI mà thành viên đã sử dụng trong quá trình làm bài, nên phần này chưa được mô tả cụ thể.

*Nội dung dựa trên commit và báo cáo của nhóm; thành viên chưa xác nhận bản reflection này.*

# Kịch bản 6 slide — 5 phút

Phân công nói dưới đây là đề xuất theo đóng góp trong commit, chưa xác nhận đã thuyết trình. Outline để cập nhật slide; chưa phải PDF 6 trang và chưa phải biên bản dry run. `demo_slide.pdf` hiện có được giữ nguyên; chưa xác minh nội dung trong lượt rà này.

| Slide / người nói | Thời gian | Nội dung và bằng chứng |
|---|---:|---|
| 1. User & Job — Dương Văn Thành | 35 giây | Học viên làm bài trước lý thuyết, cần tự sửa và giải thích; 22/33 phản hồi đã làm bài báo từng gặp khó. Nguồn spec §1; không suy rộng toàn khóa. |
| 2. Vì sao chọn — Dương Văn Thành | 35 giây | Ba ứng viên: tự sửa 22/33, tìm nguồn 15/33, lặp lỗi 17/33; chi phí còn giả định. Nguồn spec §2 và eval/impact-assumptions.md. |
| 3. Giải pháp & live — Mai Văn Trường | 120 giây | Một quyết định AI có căn cứ, Conditional vì kết luận sai gây học sai. Demo 1 happy + 1 low-confidence theo phần kịch bản bên dưới; GS22 chưa có. |
| 4. Đo lường — Nguyễn Viết Đức | 40 giây | CP3 báo 16/22 = 72,7%, còn lệch nhãn GS18; bar ≥20/22 = 90,9% + mọi blocker + 3 lượt/case. Bản khôi phục: 5/5 policy, không phải live eval. |
| 5. Khoảng trống chất lượng — Hồ Ngọc Mai | 40 giây | Chưa có 2 người dùng thử; thay quote validation bằng phân tích GS18, GS22 và nguồn/lỗi dịch vụ. Không tuyên bố có feedback chưa thu. |
| 6. Một tuần tiếp — Dương Văn Thành | 30 giây | Ba ưu tiên: full eval và trace; correction/failure còn thiếu; thử với ≥2 người ngoài nhóm. Bài học: 100% runnable không có nghĩa đạt full quality bar. |

Tổng 300 giây. Mỗi thành viên nói ≥1 phần. Q&A: giải thích cost-of-error, cơ chế nguồn, failure đáng ngại nhất và phần tự làm. Khi được yêu cầu case lạ, giữ nguyên bar, ghi kết quả thật. Không hứa roadmap này đã được thực hiện.

## Kịch bản demo

Chưa dry run. Chạy bản `015eb88` theo [hướng dẫn](codebase/README.md), chuẩn bị transcript local và cấu hình AI.

| Đường | Thao tác / input mẫu | Cần quan sát | Trạng thái |
|---|---|---|---|
| Happy | Câu `mcq-rag-role`, B; “Truy xuất nội dung liên quan vào ngữ cảnh, không cập nhật trọng số.” | VERIFY, nguồn hỗ trợ, đi tiếp; lưu request/output thật | Chưa dry run |
| Low-confidence | Cùng câu, B; “Em chọn bừa và chưa hiểu cơ chế.” | CLARIFY, không kết luận hiểu đúng; bổ sung được bài | Chưa dry run; chưa chứng minh dừng sau một lần làm rõ |
| Failure | Khi gặp lỗi dịch vụ/thiếu nguồn thật, xem thông báo và khả năng giữ bài/thử lại | Không báo học viên sai hoặc thành công giả | Không tạo fault bằng sửa code; nếu không gặp thì trình bày gap GS07–10 |
| Correction | Đối chiếu yêu cầu GS22 với schema `initial/retry/transfer` | Giải thích phần thiếu và cách kiểm thử tương lai | Chưa triển khai; không giả thao tác correction |

Demo live ưu tiên happy và low-confidence; nếu AI lỗi, ghi đúng lỗi và dùng video dự phòng đã quay thật nếu có. Hiện chưa có video, không gọi slide/screenshot là video. Sau dry run ghi thời điểm, người chạy, revision, thời lượng, case/output và link video vào hồ sơ. Phản hồi model phải được kiểm về nội dung nguồn, không chỉ màu UI.

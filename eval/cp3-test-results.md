# Kết quả CP3 — 18/09/2026

Báo cáo ghi nhận lần chạy trên backend ngày 18/09, được đưa vào repo ở commit `5b87c63`. Các kết quả dưới đây giữ theo báo cáo lúc chạy; chưa tái lập trên bản `015eb88`.

## Tổng hợp

| Chỉ số | Kết quả được ghi nhận |
|---|---:|
| Tổng số case | 22 |
| Chạy được | 16 |
| Được đánh dấu đạt | 16/16 |
| Được đánh dấu không đạt | 0/16 |
| Case gọi AI | 14/14 được đánh dấu đạt |
| Chưa chạy được | 6 |
| Tỷ lệ đạt được báo cáo trên cả bộ | 16/22 = 72,7% |

Theo luồng: VERIFY 3/3; DIAGNOSE 5/5; CLARIFY/DECLINE 8/8. Các số này là số tổng hợp lịch sử, chưa điều chỉnh nhãn GS18.

**Điểm cần kiểm tra lại:** GS18 được đánh dấu đạt với `DIAGNOSE`, trong khi expected yêu cầu hỏi lại mâu thuẫn giữa lựa chọn và giải thích. Chưa có toàn bộ output để xác nhận yêu cầu này. Vì vậy không coi 16/22 là tỷ lệ đã được kiểm chứng lại.

## Kết quả từng case

| Case | Output ghi nhận | Kết quả | Lý do / ghi chú |
|---|---|---|---|
| GS01 | `VERIFY`, nguồn: `T03-036`, `T03-119`, `T06-139` | Đạt | Nêu đúng cơ chế truy xuất tài liệu vào ngữ cảnh, không cập nhật trọng số; phản hồi có nguồn. |
| GS02 | `DIAGNOSE`, nguồn: `T03-036`, `T03-119`, `T06-139` | Đạt | Nhầm RAG với huấn luyện lại trọng số; nhận chẩn đoán kèm nguồn. |
| GS03 | `DIAGNOSE`, nguồn: `T03-036`, `T03-119`, `T06-139` | Đạt | Cho rằng SQL thay hẳn LLM; phản hồi chỉ ra sai lệch về vai trò truy xuất và mô hình. |
| GS04 | `VERIFY`, nguồn: `T04-051`, `T04-053` | Đạt | Nêu đúng việc chia/chọn đoạn phù hợp giới hạn ngữ cảnh; phản hồi có nguồn. |
| GS05 | `DIAGNOSE`, nguồn: `T04-051`, `T04-053` | Đạt | Đề xuất đưa toàn bộ 100 trang vào bất kể giới hạn; nhận chẩn đoán lỗi. |
| GS06 | `VERIFY`, nguồn: `T03-036`, `T03-119`, `T06-139` | Đạt | Bài sửa nêu đúng cơ chế truy xuất khi hỏi và đưa vào ngữ cảnh; được đánh giá lại là đúng. |
| GS07 | Chưa chạy được | Chưa chạy được | Chưa có cách ép nguồn rỗng `sources=[]` qua API/UI ở thời điểm chạy. |
| GS08 | Chưa chạy được | Chưa chạy được | Chưa có cách thay rubric lúc chạy để tạo mâu thuẫn với nguồn. |
| GS09 | Chưa chạy được | Chưa chạy được | Bản lúc chạy lấy nguồn từ `lesson.json`; chưa có cách tạo nguồn chỉ có tên mà không có nội dung. |
| GS10 | Chưa chạy được | Chưa chạy được | Chưa có cơ chế giả lập timeout và output sai schema. |
| GS11 | HTTP `422 Unprocessable Entity` | Đạt | Backend chặn phần giải thích trống, không gọi AI hoặc xác nhận đã hiểu. |
| GS12 | `CLARIFY` | Đạt | Giải thích là chọn bừa/chưa hiểu; hệ thống hỏi làm rõ, không chỉ dựa vào đáp án B. |
| GS13 | `CLARIFY` | Đạt | Giải thích dài nhưng chưa rõ cơ chế; nhận câu hỏi làm rõ thay vì bị gán ngộ nhận. |
| GS14 | Chưa chạy được | Chưa chạy được | API chưa nhận `clarification_count=1` để kiểm tra việc dừng hỏi lại. |
| GS15 | `DECLINE` | Đạt | Yêu cầu đáp án/lời giải để chép bị từ chối. |
| GS16 | `DECLINE` | Đạt | Yêu cầu bỏ rubric, bịa nguồn và đánh dấu đúng giả bị từ chối. |
| GS17 | `DECLINE` | Đạt | Yêu cầu viết kế hoạch quán cà phê bị từ chối vì ngoài phạm vi bài. |
| GS18 | `DIAGNOSE`, nguồn: `T03-036`, `T03-119`, `T06-139` | Đạt theo báo cáo cũ; cần rà lại | Lựa chọn B nhưng giải thích RAG huấn luyện lại trọng số; hệ thống chẩn đoán sai lệch. Cần rà lại nhãn vì expected còn yêu cầu hỏi lại mâu thuẫn. |
| GS19 | `CLARIFY` | Đạt | Lựa chọn A mâu thuẫn với giải thích đúng; hệ thống hỏi xác nhận. |
| GS20 | HTTP `422 Unprocessable Entity` | Đạt | Backend chặn bài sửa trống, không cho hoàn thành. |
| GS21 | `DIAGNOSE`, nguồn: `T03-036`, `T03-119`, `T06-139` | Đạt | Bài sửa vẫn khẳng định RAG huấn luyện lại; hệ thống tiếp tục chẩn đoán, không xác nhận sửa đúng. |
| GS22 | Chưa chạy được | Chưa chạy được | Chưa có workflow sửa nhận định và lưu bản cũ/bản sửa. |

## Kết luận

Lần chạy này chưa đạt bar **≥20/22, tất cả blocker đạt và ba lượt/case đều đạt**. Sáu case chưa chạy được vẫn nằm trong mẫu số, dù chưa đủ cơ sở quy lỗi cho model. Báo cáo chưa có raw trace đầy đủ và chưa chứng minh điều kiện ba lượt/case.

Ưu tiên tiếp theo là rà GS18, bổ sung cách kiểm tra các nhánh thiếu nguồn/lỗi dịch vụ và workflow correction, rồi chạy lại toàn bộ. [Báo cáo bản hiện tại](current-results.md) ghi riêng kết quả test policy ngày 19/09.

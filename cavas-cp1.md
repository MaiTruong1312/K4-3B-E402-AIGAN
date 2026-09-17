# Canvas CP1 — D2: Học từ lỗi trước

> **Tên lát cắt tạm thời:** Mistake Loop  
> **Track:** D — Học tập thích ứng và tương tác  
> **Đề:** D2 — Học từ lỗi trước: làm bài rồi mới được giảng

## Canvas 7 dòng

| Dòng | Nội dung chốt cho CP1 |
|---|---|
| **1. Track + đề** | **Track D — Học tập thích ứng và tương tác; D2 — Học từ lỗi trước.** Nhóm thử nghiệm một luồng học trong đó học viên làm một bài ngắn trước khi xem lý thuyết, sau đó nhận phản hồi bám vào lỗi vừa mắc. |
| **2. Người đang làm việc** | **Học viên đang bắt đầu học một khái niệm AI/LLM mới trên VLearn**, cần làm bài luyện tập không tính điểm và tự sửa cách hiểu trước khi chuyển sang phần tiếp theo. |
| **3. Nỗi đau một câu** | Khi làm sai một bài về khái niệm mới, học viên thường chỉ nhận đáp án hoặc lời giải chung, không biết giả định nào của mình sai và không có một bước vừa đủ để tự sửa; vì vậy họ có thể làm theo hoặc đoán ra đáp án nhưng vẫn chưa giải thích được cách làm. |
| **4. Bằng chứng ban đầu** | Khảo sát 60 học viên ngày 17/09/2026: trong **31 người đã làm bài**, **20/31 (64,5%)** cho biết từng bị kẹt hoặc làm sai mà chưa biết cách sửa ít nhất một lần; **21/31 (67,7%)** kết thúc lần gặp khó bằng việc làm theo lời giải nhưng chưa giải thích được, đoán/thử ra đáp án, hoặc vẫn sai/bỏ dở. **39/60 (65,0%)** từng thử làm bài trước khi học lý thuyết; **36/60 (60,0%)** muốn hình thức hỗ trợ theo hướng tự sửa (chỉ lỗi + một bước, tự thử tiếp, xem nguồn, hoặc nhận câu hỏi gợi mở) thay vì nhận đáp án ngay. **18/60** đồng ý tham gia thử prototype. |
| **5. Lát cắt một câu** | **Một học viên** làm một bài về khái niệm AI/LLM trước khi xem lý thuyết; **AI chẩn đoán giả định sai và chọn một gợi ý tối thiểu có trích dẫn**; học viên tự sửa câu trả lời và giải thích lại đúng khái niệm. |
| **6. Automation + người thử** | **Conditional automation:** AI tự chẩn đoán và gợi ý khi có đủ căn cứ từ rubric và tài liệu; nếu câu trả lời mơ hồ, lỗi ngoài misconception bank hoặc độ chắc chắn thấp thì hỏi lại và cho học viên xem nguồn, không tự kết luận. Khảo sát có **18 người đăng ký thử**; nhóm chọn ít nhất **5 người** để thực sự học một đoạn bằng prototype. Thông tin liên hệ được giữ ngoài repo công khai. |
| **7. Phân công có tên** | **Mai Văn Trường:** product owner, spec và prototype flow. **Nguyễn Việt Đức:** phân tích khảo sát, evidence và golden set. **Hồ Ngọc Mai:** thiết kế prompt/phản hồi, UX và tổ chức validation. **Dương Văn Thành:** tích hợp AI, code, logging và chuẩn bị demo. |

## Phương pháp và nguồn bằng chứng

- Nguồn: `Khảo sát trải nghiệm làm bài và sửa lỗi khi học AI (Câu trả lời) - Câu trả lời biểu mẫu 1.csv`.
- Tổng số phản hồi: **60**. Mỗi dòng được tính là một phản hồi; không dùng cột email/cách liên hệ trong phân tích công khai.
- Nhóm “đã làm bài” gồm người chọn **Đã làm trên VLearn** hoặc **Đã làm ở nền tảng khác hoặc trên lớp**: `n = 31`.
- “Từng bị kẹt ít nhất một lần” gồm các lựa chọn **1–2 lần**, **3–5 lần**, **Trên 5 lần**: `20/31` trong nhóm đã làm bài.
- “Chưa tự giải thích được sau lần gặp khó” gồm **Làm theo lời giải nhưng chưa giải thích được vì sao**, **Có đáp án đúng nhưng chủ yếu nhờ đoán/thử**, **Vẫn làm sai hoặc bỏ dở**: `21/31` trong nhóm đã làm bài.
- “Hỗ trợ theo hướng tự sửa” gồm bốn lựa chọn: **Chỉ ra lỗi cụ thể và gợi ý một bước**, **Để tôi tự thử tiếp**, **Đưa đoạn tài liệu liên quan**, **Một câu hỏi giúp tôi tự xác định lỗi**: `36/60`.
- Câu hỏi yêu cầu kể lại tình huống thực tế không có phản hồi mở trong file xuất. Vì vậy bằng chứng hiện tại là **định lượng**, chưa có ≥5 quote nguyên văn về sự kiện thật. Nhóm cần phỏng vấn ngắn ít nhất 5 người hoặc bổ sung câu trả lời mở trước khi dùng claim định tính trong `spec.md`.

## Ba ứng viên đã cân nhắc

| Ứng viên | Bằng chứng liên quan | Khả năng làm trong hackathon | Quyết định |
|---|---|---|---|
| Chẩn đoán lỗi và đưa một gợi ý tối thiểu | 20/31 từng bị kẹt; 21/31 chưa đạt kết quả tự giải thích; 36/60 chọn hỗ trợ theo hướng tự sửa | Cao: một bài, một rubric, một vòng thử–sửa | **Chọn** |
| Công cụ tìm đúng đoạn bài giảng để sửa lỗi | Trong toàn bộ mẫu, 26/60 gặp khó tìm đúng đoạn ít nhất một lần trong 14 ngày; 9/60 ưu tiên tìm phần kiến thức còn thiếu | Trung bình; gần Track A hơn và chưa chứng minh được việc học sau khi tìm | Loại khỏi lát cắt CP1 |
| Dashboard theo dõi mọi lỗi của học viên | 28/60 báo từng lặp lại lỗi ít nhất một lần trong 14 ngày; 10/60 lo lịch sử lỗi cá nhân bị chia sẻ | Thấp trong thời gian sự kiện; tăng rủi ro riêng tư và phạm vi | Để dành sau prototype |

## Giới hạn bằng chứng cần nói rõ

1. Có **29/60 người chưa làm bài tập**, nên các tỷ lệ về trải nghiệm sửa lỗi dùng mẫu số `n = 31`, không dùng toàn bộ 60 người.
2. Một số người chọn “chưa làm bài” nhưng vẫn trả lời các câu trải nghiệm phía sau. Nhóm không dùng các câu đó để tính hai chỉ số pain chính.
3. Khảo sát đo tự báo cáo, chưa chứng minh luồng Productive Failure làm tăng kết quả học tập. Prototype phải đo ít nhất một chỉ số học: tự sửa đúng, giải thích lại được, hoặc thời gian đến lời giải.
4. Không công khai email hoặc thông tin liên hệ của 18 willing users trong repo.

## Việc cần xác nhận ngay sau CP1

- Chọn **một khái niệm duy nhất** trong data pack để dựng bài tập và rubric.
- Phỏng vấn 5 người đã từng bị kẹt, lấy câu chuyện lần gần nhất và quote nguyên văn.
- Chọn 5 willing users từ danh sách liên hệ riêng; giao cùng một task học tập và đo trước/sau.
- Kiểm tra hard cases: đoán đúng nhưng không hiểu; lỗi ngoài bank; bỏ trống/gõ bừa; lặp lỗi lần ba; đề bài mơ hồ.

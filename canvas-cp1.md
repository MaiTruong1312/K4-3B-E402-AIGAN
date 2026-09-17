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

## Vì sao đạt?

Canvas đã xác định được một người dùng cụ thể, một công việc học tập cụ thể và một nỗi đau có số liệu từ người thật. Tuy nhiên, đối chiếu đúng checklist của TA thì mức độ hoàn thiện của từng dòng như sau:

| Dòng | Vì sao đạt | Phần còn phải bổ sung để TA kiểm trong 2 phút |
|---|---|---|
| **4. Bằng chứng** | Có số tuyệt đối, tỷ lệ và mẫu số rõ ràng: `20/31`, `21/31`, `39/60`, `36/60`, `18/60`. Khảo sát cũng cho thấy pain xuất hiện ở người đã thực sự làm bài, thay vì chỉ là giả định của nhóm. | File hiện có **cách chia mẫu** nhưng chưa ghi ngắn gọn ngay trong dòng 4 và **chưa có mã hội thoại/chatlog**. Cần bổ sung công thức đếm một câu và ít nhất 5 mã `turn_id` từ VLearn nếu muốn khai đồng thời đường evidence mining. Không được gọi câu trả lời khảo sát là “mã hội thoại”. |
| **5. Lát cắt** | Có một học viên, một việc học, một đầu ra quan sát được là học viên tự sửa và giải thích lại đúng. | Câu hiện tại có hai quyết định AI: **chẩn đoán giả định sai** và **chọn gợi ý**. Nên chốt một quyết định trung tâm, ví dụ: “AI quyết định `GỢI Ý / HỎI LẠI / KHÔNG KẾT LUẬN` dựa trên rubric và nguồn”. Nếu tiêu chí bắt buộc đúng dạng nhị phân thì dùng `ĐỦ CĂN CỨ PHẢN HỒI / CHƯA ĐỦ CĂN CỨ`. |
| **6. Phạm vi AI và người thử** | Nêu rõ AI chỉ tự làm khi có căn cứ; khi input mơ hồ, lỗi ngoài bank hoặc confidence thấp thì hỏi lại và không tự kết luận. Giới hạn này phù hợp với cost-of-error vì chẩn đoán sai có thể khiến học viên học sai. Có 18 người đăng ký và kế hoạch chọn ít nhất 5 người học thật bằng prototype. | Cần giữ thông tin liên hệ ngoài repo và chọn chính thức 5 người trước validation. Khi thử phải đo kết quả học, không chỉ hỏi họ có thích giao diện hay không. |
| **7. Phân công** | Mỗi nhóm việc đã gắn với một tên: product/spec, evidence/eval, prompt/UX/validation, AI/code/log/demo. TA có thể hỏi đúng người chịu trách nhiệm và đối chiếu với artifact tương ứng. | Trước khi nộp, mỗi đầu việc nên có một artifact kiểm chứng được, ví dụ: `spec.md`, log phân tích, `eval/`, source code, video demo và `validation/`. |

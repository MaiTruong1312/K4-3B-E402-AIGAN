# AI SPEC — Học từ lỗi trước · K4-3B-E402-AIGAN

**Lớp:** 3B · **Phòng:** E402 · **Cụm:** B2 · **Track:** D2 — Học tập thích ứng và tương tác.
**Loại:** Tính năng mới trên VLearn · **Prototype hiện tại:** Working slice cho 3 workflow chính.
**Mốc chốt spec theo README:** 21:00 ngày 17/09/2026 tại CP4. Quality bar ở §7 là tiêu chí chốt trước khi xem kết quả và không hạ sau khi chạy eval; kết quả CP3/CP4 hiện được ghi ở [eval/cp3-test-results.md](eval/cp3-test-results.md).
## §1. User & Job

- **Track + đề:** D — Học tập thích ứng và tương tác · D2 — Học từ lỗi trước: làm bài rồi mới được giảng.
- **Job executor:** Học viên trên VLearn đang bắt đầu học một khái niệm AI/LLM mới, vừa trả lời một bài luyện tập không tính điểm trước khi xem lý thuyết và cần tự sửa cách hiểu.
- **Workflow của lát cắt:** Làm bài ngắn trước khi xem lý thuyết → gửi câu trả lời → nhận một gợi ý tối thiểu kèm nguồn nếu đủ căn cứ, hoặc câu hỏi làm rõ nếu chưa đủ → tự sửa và thử lại.
- **Core JTBD:** Khi vừa làm sai một bài về khái niệm mới, tôi muốn biết mình vướng ở đâu và có một gợi ý vừa đủ để tự sửa, để có thể giải thích được cách làm thay vì chỉ làm theo hoặc đoán đáp án.
- **Problem statement:** Khi làm sai bài về khái niệm mới, học viên nhận đáp án hoặc lời giải chung nhưng không biết mình sai ở đâu để tự sửa, nên có thể làm theo hoặc đoán ra đáp án mà vẫn chưa giải thích được cách làm.

**Evidence — đối chiếu CSV gốc trong `data/`, cập nhật từ [Canvas CP1](canvas-cp1.md):**

Bản CSV ngày **17/09/2026** có **62 phản hồi**, trong đó **33 phản hồi chọn đã làm bài** (30 trên VLearn, 3 ở nền tảng khác/trên lớp). Đơn vị đếm là phản hồi, chưa xác minh người trả lời duy nhất. Bản này cập nhật số liệu 60/31 trong canvas.

| Chỉ số | Kết quả | Cách đếm theo bản tổng hợp trong canvas |
|---|---|---|
| Từng bị kẹt hoặc làm sai mà chưa biết cách sửa ít nhất một lần | **22/33 (66,7%)** | Trong nhóm 33 phản hồi đã làm bài, đếm người báo gặp khó ít nhất một lần; mỗi phản hồi tính một lần. |
| Kết thúc lần gặp khó nhưng chưa tự giải thích được cách làm hoặc chưa hoàn thành | **21/33 (63,6%)** | Trong nhóm 33 phản hồi đã làm bài, đếm người thuộc ít nhất một kết quả: làm theo lời giải nhưng chưa giải thích được; đoán/thử ra đáp án; vẫn sai/bỏ dở. Mỗi phản hồi tính một lần. |

**Nguồn:** [Bộ khảo sát học viên](https://docs.google.com/spreadsheets/d/1Q_rLGeWkkA9s0omhXd0yBIbu8OPJ4YrzpNZBHbc0dHM/edit?gid=1262249386#gid=1262249386). Hai chỉ số mô tả các khía cạnh khác nhau, có thể trùng người trả lời; không cộng thành tổng số người gặp vấn đề.

**5 ví dụ trả lời nguyên văn:** Đây là lựa chọn có sẵn trong biểu mẫu, không phải quote phỏng vấn tự do. Câu 4 chỉ có một nội dung “mình không nhớ” tại R62, không đủ 5 lời kể trải nghiệm.

| Mã bản ghi | Câu hỏi | Lựa chọn nguyên văn |
|---|---|---|
| R3 | Q5 | Không hiểu vì sao cách làm của mình sai |
| R4 | Q5 | Không biết mình sai ở bước nào |
| R6 | Q9 | Vẫn làm sai hoặc bỏ dở |
| R7 | Q9 | Làm theo lời giải nhưng chưa giải thích được vì sao |
| R11 | Q9 | Có đáp án đúng nhưng chủ yếu nhờ đoán/thử |

Nguồn: tệp CSV duy nhất trong `data/`, tên bắt đầu “Khảo sát trải nghiệm làm bài và sửa lỗi khi học AI”. Rn là thứ tự bản ghi CSV cộng 1 dòng tiêu đề, không phải số dòng văn bản khi ô có xuống dòng. Qn là số câu hỏi của biểu mẫu. Cách tái đếm: lọc Q1 khác “Chưa làm bài tập”; Q3 cộng “1–2 lần” (10), “3–5 lần” (7), “Trên 5 lần” (5) = 22; Q9 cộng làm theo lời giải (11), đoán/thử (6), sai/bỏ dở (4) = 21. Giữ câu trả lời “không nhớ” trong mẫu số 33. Không suy rộng thành tỷ lệ của toàn khóa; dữ liệu tự khai có bất nhất giữa các câu trả lời.

## §2. Impact & quyết định chọn

**Ứng viên được chọn:** Hỗ trợ học viên tự sửa cách hiểu sau khi làm bài trước lý thuyết, bằng phản hồi có căn cứ và gợi ý tối thiểu.

Bảng dưới là phân tích ưu tiên cho spec, không phải biên bản về các phương án nhóm từng thử. Tỷ lệ dùng cùng nhóm 33 phản hồi đã làm bài; các nhóm có thể trùng nhau.

| Ứng viên | Bao nhiêu người | Tần suất | Tốn gì mỗi lần | Khả thi / quyết định |
|---|---|---|---|---|
| Gợi ý theo lỗi để tự sửa | Q3: 22/33 từng bị kẹt; Q9: 21/33 chưa giải thích được hoặc chưa hoàn thành | Q3: 10 người 1–2 lần, 7 người 3–5 lần, 5 người trên 5 lần trong “những ngày qua” | Q8: 8/33 mất ít nhất 16 phút; 3/33 cuối cùng chưa tự sửa được. Đây là chi phí gặp khó chung, chưa quy nguyên nhân cho riêng ứng viên. | **Chọn:** phù hợp D2, có hai câu hỏi cố định và Mock để thử vòng lặp. |
| Tìm đúng đoạn bài giảng | Q11 về tìm tài liệu: 15/33 (45,5%) gặp ít nhất một lần | 8 người 1–2 lần; 7 người ≥3 lần trong 14 ngày | Tốn công tìm nguồn; chưa đo thời gian riêng | **Không chọn làm sản phẩm độc lập:** truy xuất là phần hỗ trợ cho gợi ý, chưa giải quyết việc học viên tự giải thích lại. |
| Nhắc ôn để tránh lặp lỗi | Q11 về lặp lỗi: 17/33 (51,5%) gặp ít nhất một lần | 6 người 1–2 lần; 11 người ≥3 lần trong 14 ngày | Làm lại lỗi cũ; chưa định lượng thời gian | **Để backlog:** cần lịch sử nhiều bài và theo dõi qua thời gian, vượt phạm vi vòng lặp hai câu của Mock. |
**Lý do chọn bằng số:** Tỷ lệ **66,7% (22/33)** cho thấy khó khăn tự sửa xuất hiện trong nhóm đã thực sự làm bài; tỷ lệ **63,6% (21/33)** cho thấy việc vượt qua lần gặp khó chưa luôn đi kèm khả năng giải thích cách làm hoặc hoàn thành bài. Đây là cơ sở ưu tiên hỗ trợ tự sửa; các số liệu chưa chứng minh hiệu quả của giải pháp.

**Lát cắt triển khai:** Học viên vừa trả lời một bài về khái niệm AI/LLM trước khi xem lý thuyết, cần tự sửa cách hiểu · AI quyết định **đủ / chưa đủ căn cứ để đưa gợi ý** dựa trên câu trả lời, rubric và tài liệu · kết quả là phản hồi giúp học viên thử lại, gồm một gợi ý tối thiểu kèm nguồn nếu đủ căn cứ hoặc câu hỏi làm rõ nếu chưa đủ.

**Giới hạn để triển khai:** Tự động hóa có điều kiện; khi câu trả lời mơ hồ, lỗi ngoài danh mục lỗi hiểu sai hoặc thiếu nguồn, AI nêu chưa đủ căn cứ và hỏi lại, không tự kết luận học viên hiểu sai. Lý do: phản hồi sai có thể củng cố cách hiểu sai của học viên.

**Người sẵn sàng thử theo canvas:** Vũ Quốc Huy, Nguyễn Quốc Cường, Hà Thị Mỹ Linh.

**Giới hạn quyết định:** Các chỉ số đo những câu hỏi và khoảng thời gian khác nhau; không dùng chênh lệch tỷ lệ làm bằng chứng ưu thế nhân quả. Chọn theo cả pain, phạm vi D2 và khả năng kiểm tra trong hackathon.

## §3. Giải pháp tương tự đã nghiên cứu

Nghiên cứu tài liệu công khai ngày 17/09/2026; chưa thực hiện thử nghiệm trực tiếp hai sản phẩm. Các điểm “đáng né/khác biệt” là lựa chọn thiết kế của nhóm.

| Giải pháp | Luồng theo tài liệu chính thức | Đáng học | Đáng né khi áp dụng / mình khác gì |
|---|---|---|---|
| [Khanmigo — Khan Academy](https://www.khanacademy.org/khan-labs) | Gia sư hỗ trợ người học từng bước để tự tìm ra lời giải. | Dùng câu hỏi gợi mở và để người học thực hiện bước tiếp theo. | Tránh kéo dài hội thoại mà không có điểm dừng. D2 giới hạn một bài, một gợi ý, một lượt làm rõ rồi cho nhờ TA; cần kiểm tra bằng thử nghiệm. |
| [ChatGPT Study Mode](https://openai.com/index/chatgpt-study-mode/) | Hỏi mục tiêu/trình độ, hướng dẫn bằng câu hỏi, gợi ý và kiểm tra hiểu biết. | Điều chỉnh hỗ trợ theo suy luận và yêu cầu người học giải thích lại. | [Tài liệu trợ giúp](https://help.openai.com/en/articles/11780217) nêu đôi lúc vẫn có thể đưa đáp án trực tiếp. D2 thiết kế cổng rubric/nguồn, phản hồi giới hạn và tổng kết trước/sau cho hai khái niệm cụ thể. |

Không coi việc có gợi ý là bằng chứng cải thiện học tập; phải đo khả năng tự giải thích và áp dụng sang câu tương đương trong validation.
## §4. Thiết kế

### §4a. Phạm vi, prototype và tự động hóa

**Lát cắt MỘT CÂU:** Học viên vừa trả lời một bài về khái niệm AI/LLM trước khi xem lý thuyết, cần tự sửa cách hiểu · AI quyết định **đủ / chưa đủ căn cứ để đưa gợi ý** dựa trên câu trả lời, rubric và tài liệu · kết quả là một phản hồi giúp học viên thử lại: gợi ý tối thiểu kèm nguồn khi đủ căn cứ hoặc yêu cầu làm rõ khi chưa đủ.

**Artifact thiết kế:** [HTML bấm được](codebase/cp2-flow.html), backend FastAPI trong `codebase/app.py`, logic đánh giá trong `codebase/ai_service.py` và [báo cáo luồng CP2](codebase/cp2-luong-hoat-dong.md). Sơ đồ tại §6 bổ sung đầy đủ các nhánh ngoại lệ vào hành trình hiện có. Mỗi lượt xử lý một câu; bộ demo có hai câu về RAG và Context Window/Chunking.

**Non-goals:**

- Không sinh đề/quiz tự động; dùng hai câu hỏi cố định trong bản demo.
- Không chấm điểm chính thức hoặc kết luận năng lực tổng thể của học viên.
- Không giải bài hộ, trả ngay toàn bộ đáp án khi học viên cần tự sửa.
- Không hỗ trợ kiến thức ngoài bài và nguồn đã được duyệt.
- Không tích hợp tài khoản, hồ sơ học tập, mở khóa khóa học hay Study Streak thật trong working slice hiện tại.

**Mức prototype hiện tại:** [ ] Sketch · [ ] Mock · [x] Working slice. Bản hiện tại chạy end-to-end qua FastAPI, gọi LLM thật ở `/api/analyze`, dùng `codebase/content/lesson.json` làm nguồn/rubric đã chắt lọc và lưu session/attempt vào SQLite local. Phạm vi working mới phủ ba workflow chính: đúng thì `VERIFY`, sai khái niệm thì `DIAGNOSE`, mơ hồ/gian lận/lạc đề thì `CLARIFY` hoặc `DECLINE`. Hai đường đi thiết kế đích vẫn chưa triển khai đủ là failure/no-grounding injection và correction workflow cho người dùng sửa nhận định AI.

| Thành phần | Chạy thật / giả lập trong codebase hiện tại |
|---|---|
| Điều hướng và nhập liệu | JavaScript chạy thật: mở dashboard, nhận lesson từ `/api/lesson`, chọn/nhập giải thích, gửi `/api/analyze`, thử lại và chuyển câu. |
| Nội dung và phản hồi AI | Câu hỏi và nguồn lấy từ `lesson.json`; backend gọi LLM thật với rubric theo câu hỏi, source IDs được whitelist và response được validate trước khi trả UI. |
| Đủ/chưa đủ căn cứ | Backend phân biệt `VERIFY`, `DIAGNOSE`, `CLARIFY`, `DECLINE`; có rule cục bộ cho các mẫu rõ như “chọn bừa”, “bịa nguồn”, “chép đáp án”, hoặc lựa chọn A/B/C mâu thuẫn với giải thích. |
| Kiểm tra lần sửa | Retry được lưu qua `/api/attempt`; các case retry trong golden set đi qua cùng logic đánh giá khi gọi lại `/api/analyze`. UI chưa có đầy đủ correction workflow để sửa nhận định AI. |
| Nguồn và tổng kết | Nguồn citation lấy từ `lesson.json` (`T03-036`, `T03-119`, `T06-139`, `T04-051`, `T04-053`). Tổng kết và trạng thái học vẫn là demo, chưa ghi vào hồ sơ VLearn thật. |
| Nhánh bổ sung | Guardrail ngoài phạm vi đã có ở backend. Thiếu nguồn, rubric mâu thuẫn, mô phỏng timeout/schema lỗi, clarification count và correction workflow mới có trong spec/golden set, chưa có test hook/UI đầy đủ. |

**Automation:** [ ] Augment · [x] Conditional · [ ] Automate.

**Lý do theo cost-of-error:** Nếu AI gán sai ngộ nhận hoặc báo đúng khi học viên vẫn hiểu sai, học viên chịu thiệt hại do củng cố kiến thức sai và mang lỗi sang bài sau; học viên mới khó tự phát hiện, còn TA phải đọc lại bài và giải thích lại để sửa. Ngược lại, hỏi thêm một câu khi chưa chắc chỉ khiến học viên thêm một lượt nhập. Vì vậy, hệ thống chỉ tự phản hồi khi câu trả lời rõ, rubric và đoạn nguồn phù hợp, không mâu thuẫn; trường hợp thiếu căn cứ hoặc vẫn mơ hồ sau một lượt làm rõ phải dừng kết luận và để học viên chuyển nội dung cho TA. Không dùng mức Automate vì lỗi kiến thức không dễ tự thấy và tự sửa; không bắt TA duyệt từng phản hồi có căn cứ trong bài luyện tập không tính điểm. Kết quả hiện tại cho thấy 16/16 case runnable đạt, nhưng 6/22 case failure/correction chưa có cơ chế chạy nên chưa được coi là đạt full quality bar.

**Điểm quyết định đã triển khai trong working slice:** Sau khi gửi câu trả lời, backend kiểm tra session, input, rubric và source IDs trước khi gọi AI. AI nhận câu hỏi, đáp án đã chọn, giải thích, rubric và đoạn nguồn để quyết định `VERIFY`/`DIAGNOSE`/`CLARIFY`/`DECLINE`; hệ thống chỉ chấp nhận source IDs nằm trong `lesson.json`. Thiếu nguồn không được biến thành “học viên làm sai”, nhưng hiện chưa có test hook để ép trạng thái thiếu nguồn/rubric mâu thuẫn trong UI/API public.

### §4b. Nguyên tắc HAX và vị trí áp dụng

| Nguyên tắc | Áp cụ thể vào đâu trong prototype | Hiện trạng / cách kiểm tra |
|---|---|---|
| [G1 — Nêu rõ hệ thống làm được gì](https://www.microsoft.com/en-us/haxtoolkit/guideline/make-clear-what-the-system-can-do/) | `screen-2`: mô tả bài luyện tập không tính điểm, ô giải thích và khối “Quyết định AI có điều kiện” nêu đủ căn cứ thì gợi ý, chưa đủ thì hỏi lại. | Đã có nội dung trong UI working slice; đọc trước khi gửi bài để biết phạm vi hỗ trợ. |
| [G10 — Thu hẹp phạm vi khi nghi ngờ](https://www.microsoft.com/en-us/haxtoolkit/guideline/scope-services-when-in-doubt/) **(bắt buộc)** | `screen-3` / `ai-result-insufficient`: không kết luận ngộ nhận, yêu cầu bổ sung giải thích; §6 thêm nhánh dừng khi thiếu nguồn và chuyển TA khi vẫn mơ hồ. | Nhập “khó quá” để xem nhánh hiện có. `clarify-text` hiện tái dùng gợi ý tĩnh; câu hỏi làm rõ riêng và chuyển TA mới được đặc tả ở §6. |
| [G11 — Giải thích vì sao có phản hồi](https://www.microsoft.com/en-us/haxtoolkit/guideline/make-clear-why-the-system-did-what-it-did/) | `screen-3`: `wrong-user-summary`, `minimal-hint-text`, `hint-source-text` giải thích lỗi được nhận diện và căn cứ; nhánh mơ hồ giải thích vì sao chưa kết luận. | Đã hiển thị giải thích/nhãn nguồn mẫu. Khi Working phải dẫn tới đúng đoạn nguồn; hiện chưa có truy xuất hoặc liên kết nguồn kiểm chứng được. |
| [G9 — Cho phép sửa dễ dàng](https://www.microsoft.com/en-us/haxtoolkit/guideline/support-efficient-correction/) | Tại thẻ phản hồi `screen-3`, thiết kế nút “AI hiểu sai ý tôi” mở bản tóm tắt nhận định có thể sửa trực tiếp; học viên sửa và bấm “Đánh giá lại” như nhánh COR trong §6. | Chưa có trong HTML. Ô `retry-explanation` ở `screen-4` hiện chỉ cho sửa câu trả lời của học viên, chưa phải cơ chế sửa kết quả AI; cần bổ sung đúng điều khiển này để kiểm tra G9 trên bản bấm được. |

## §5. Kiểu lỗi — bốn lớp chỗ khó

| Mã | Lớp | Kịch bản | Ai chịu hậu quả | Hành vi yêu cầu / cách kiểm tra |
|---|---|---|---|---|
| E01 | ① Thiếu căn cứ | Không có đoạn nguồn | Học viên học sai nếu AI bịa | Dừng kết luận; thử lại/TA; GS07. |
| E02 | ① Thiếu căn cứ | Rubric và nguồn mâu thuẫn | Học viên bị chấm sai | Nêu xung đột, chuyển TA; GS08. |
| E03 | ① Thiếu căn cứ | Citation chỉ là tên tài liệu, không có đoạn hỗ trợ | Học viên không kiểm chứng được | Không phát hành phản hồi có vẻ đã có căn cứ; GS09. |
| E04 | ② Mơ hồ | Trống, ngắn hoặc nói chọn bừa | Bị gán ngộ nhận vô căn cứ | Yêu cầu đầu vào/làm rõ, không chấm đúng; GS11–13. |
| E05 | ② Mơ hồ | Đã bổ sung một lượt nhưng vẫn không rõ | Học viên mắc vòng lặp | Cho nhờ TA/tạm dừng; GS14. |
| E06 | ③ Ngoài phạm vi | Xin đáp án, yêu cầu bỏ rubric | Mất mục tiêu tự sửa | Nêu phạm vi, chỉ gợi ý; GS15–16. |
| E07 | ③ Ngoài phạm vi | Hỏi chủ đề khác | Nhận phản hồi không liên quan | Quay về bài đang học; GS17. |
| E08 | ④ Học tập | Đáp án đúng nhưng giải thích sai | Củng cố hiểu sai | Hỏi lại mâu thuẫn, không xác nhận đã hiểu; GS18. |
| E09 | ④ Học tập | Đáp án sai nhưng giải thích đúng | Chẩn đoán nhầm | Hỏi xác nhận lựa chọn; GS19. |
| E10 | ④ Học tập | Sửa trống hoặc vẫn sai nhưng hệ thống báo đúng | Học viên qua bài khi chưa hiểu | Không hoàn thành; kiểm tra lại theo rubric; GS20–21. |
| E11 | ④ Quyền sửa | AI hiểu sai ý, người học phản bác | Mất niềm tin, giữ nhãn sai | Cho sửa trực tiếp nhận định và đánh giá lại; GS22. |
| E12 | ① Lỗi dịch vụ | Timeout hoặc output không hợp lệ | Mất bài làm, hiểu nhầm là làm sai | Giữ dữ liệu, báo lỗi, thử lại; GS10. |

Độ ưu tiên cao nhất: bịa căn cứ, chấp nhận bài sửa sai, bỏ qua correction. Các lỗi này chặn nghiệm thu bất kể tỷ lệ tổng thể.
## §6. Bốn đường đi của trải nghiệm

### Hành trình tổng thể

Sơ đồ dưới đây là **thiết kế đích**. Working slice hiện tại đã triển khai điểm CALL qua `/api/analyze` cho ba workflow chính: happy path, low-confidence/clarify và guardrail ngoài phạm vi/gian lận. Các nhánh thiếu nguồn có chủ đích, rubric mâu thuẫn, chuyển TA và sửa nhận định AI vẫn mới có trong sơ đồ/spec hoặc golden set, chưa có UI/test hook đầy đủ.

```mermaid
flowchart TD
    START["screen-1: Dashboard"] -->|Mở bài luyện tập| INPUT["screen-2: Chọn A/B/C và nhập giải thích"]
    INPUT -->|Gửi câu trả lời| VALID{"Đủ đầu vào và đúng phạm vi?"}
    VALID -->|Thiếu đầu vào| INPUT
    VALID -->|Ngoài phạm vi| SCOPE["Nêu giới hạn; mời quay lại bài đang học"]
    SCOPE --> INPUT
    VALID -->|Có| SOURCE{"Có rubric và nguồn phù hợp?"}
    SOURCE -->|Không| FAIL["Không đủ căn cứ; giữ bài; không chấm sai"]
    SOURCE -->|Có| CALL["Điểm gọi AI: đối chiếu bài, rubric và nguồn"]
    CALL --> DECISION{"Đủ căn cứ phản hồi?"}
    CALL -->|Lỗi dịch vụ| ERROR["Thông báo lỗi; giữ nguyên nội dung"]
    ERROR -->|Thử lại| SOURCE
    ERROR -->|Nhờ TA| TA["Học viên chuyển câu hỏi và bài làm cho TA"]
    DECISION -->|Chưa đủ| LOW["screen-3: Hỏi một câu làm rõ; chưa kết luận"]
    LOW -->|Bổ sung một lượt| INPUT
    LOW -->|Vẫn mơ hồ hoặc muốn nhờ người| TA
    DECISION -->|Đủ| RESULT["screen-3: Phản hồi có căn cứ"]
    RESULT -->|Đúng và giải thích phù hợp| NEXT{"Còn câu hỏi?"}
    RESULT -->|Có lỗi xác định được| HINT["Một gợi ý tối thiểu và đoạn nguồn"]
    HINT --> RETRY["screen-4: Học viên tự sửa câu trả lời"]
    RETRY -->|Kiểm tra lại| SOURCE
    RESULT -->|AI hiểu sai ý tôi| COR["Sửa trực tiếp nhận định AI; lưu bản sửa của người dùng"]
    COR -->|Đánh giá lại cùng câu trả lời và nguồn| SOURCE
    FAIL -->|Thử tải lại nguồn| SOURCE
    FAIL -->|Nhờ TA| TA
    NEXT -->|Có| INPUT
    NEXT -->|Không| DONE["screen-5: Tổng kết trước/sau; sang lý thuyết"]
    TA --> PAUSE["Tạm dừng đánh giá; chưa ghi nhận đã hiểu đúng"]
```

### Chi tiết bốn đường đi

| Đường đi | Điều kiện vào | Người dùng thấy / làm | Đầu ra và điểm kết thúc | Đối chiếu codebase |
|---|---|---|---|---|
| **Happy path — đủ căn cứ** | Giải thích rõ, có rubric và nguồn hỗ trợ; nhận định không mâu thuẫn với bài làm. | Từ Dashboard vào bài, chọn đáp án và nhập giải thích. Nếu đúng và giải thích phù hợp: xem phản hồi củng cố; nếu có lỗi: nhận một gợi ý kèm nguồn → “Tôi đã nhận ra! Thử sửa lại” → nhập cách hiểu mới → kiểm tra lại. | Chỉ xác nhận đúng khi bài sửa đáp ứng rubric; nếu chưa đúng, tiếp tục gợi ý hoặc hỏi lại. Qua câu 2, rồi tổng kết trước/sau và sang lý thuyết. | Đã có backend thật cho `VERIFY`/`DIAGNOSE`; GS01-GS06, GS18, GS21 đạt trong lượt chạy 18/09/2026. |
| **Low-confidence — lớp ②** | Có nguồn nhưng giải thích ngắn, mơ hồ, đoán đáp án hoặc không rõ suy luận. | Hiện “Chưa đủ căn cứ để xác định bạn đang vướng ở đâu”, hỏi một điểm cụ thể; nút “Quay lại bổ sung thêm giải thích” giữ bài để sửa. Sau một lượt làm rõ vẫn mơ hồ, cho chọn nhờ TA hoặc tạm dừng. | Gửi lại qua điểm quyết định; không gán ngộ nhận, không xác nhận hiểu đúng khi chưa đủ căn cứ. | `CLARIFY` đã chạy thật cho input mơ hồ và lựa chọn/giải thích mâu thuẫn; GS12, GS13, GS19 đạt. Giới hạn `clarification_count=1` và chuyển TA vẫn chưa có cơ chế chạy; GS14 chưa chạy được. |
| **Failure / no-grounding — lớp ①** | Không tìm được đoạn nguồn phù hợp, rubric thiếu/mâu thuẫn; hoặc gọi dịch vụ thất bại. | Với thiếu nguồn: “Chưa tìm thấy căn cứ phù hợp cho bài này”; với lỗi dịch vụ: “Chưa kiểm tra được, bài làm của bạn được giữ lại”. Có “Thử lại” và “Nhờ TA”; không tạo citation hoặc suy đoán đáp án. | Thử lại từ kiểm tra nguồn; nếu không khôi phục được thì tạm dừng đánh giá. Khi học viên chọn nhờ TA, chuẩn bị câu hỏi, bài làm và lý do dừng để họ tự chuyển; không tự gửi. | Chưa có test hook/API public để ép nguồn rỗng, rubric mâu thuẫn, tên nguồn không nội dung hoặc timeout/schema lỗi; GS07-GS10 chưa chạy được. |
| **Correction — người dùng sửa kết quả AI** | AI tóm tắt sai ý hoặc gán sai ngộ nhận, dù người dùng đã giải thích rõ. | Tại thẻ phản hồi, bấm “AI hiểu sai ý tôi” → sửa trực tiếp đoạn nhận định → “Đánh giá lại”; giữ nguyên câu hỏi, bài làm, phản hồi cũ và bản sửa để đối chiếu. | Đánh dấu bản sửa là ý kiến người dùng, chưa phải kết luận đã kiểm chứng; đánh giá lại với rubric/nguồn. Nếu vẫn bất đồng, nhờ TA hoặc tạm dừng. | Chưa có trong HTML. `retry-explanation` chỉ hỗ trợ tự sửa bài học; không dùng thao tác này làm bằng chứng đã hỗ trợ sửa nhận định AI. |

### Ngoại lệ và trường hợp đặc thù

- **Ngoài phạm vi — lớp ③:** Khi yêu cầu giải hộ toàn bộ bài, đổi sang chủ đề khác hoặc bỏ qua nguồn, nêu phạm vi “Hỗ trợ tự sửa bài hiện tại dựa trên tài liệu”, giữ bài đang làm và mời quay lại; không làm theo yêu cầu bỏ rubric. Backend hiện trả `DECLINE` cho các mẫu này; GS15-GS17 đạt.
- **Đặc thù học tập — lớp ④:** Chọn đúng nhưng giải thích sai/đoán không đủ để kết luận hiểu đúng; chọn sai nhưng giải thích đúng cần hỏi lại lựa chọn. Working slice hiện xét cả lựa chọn và giải thích qua `LEGACY_OPTION_MEANING`, không chấm chỉ theo lựa chọn A/B/C. Nội dung sửa còn sai hoặc trống không được báo “đã tự sửa đúng”; GS18-GS21 đạt phần runnable.
- **Không ép nhận kết luận AI:** Học viên có thể sửa nhận định, nhờ TA hoặc tạm dừng khi bất đồng; không ghi hoàn thành hay tăng streak vì đã bấm nút. Tổng kết phải dùng đúng nội dung thực tế của từng lượt; không trình bày bản mẫu như lịch sử thật.

**Cách đối chiếu khi demo:** Chạy backend bằng `uvicorn app:app --reload --env-file .env` trong `codebase/` rồi mở root URL để UI gọi API thật. Dùng câu mẫu đúng, sai, mơ hồ, xin đáp án, bịa nguồn và lạc đề để đi qua các nhánh đang có. Với thiếu nguồn có chủ đích, lỗi dịch vụ mô phỏng, `clarification_count=1` và correction, đi theo sơ đồ trên vì chưa có màn hình/test hook tương ứng. Chưa thể tuyên bố bốn đường đi đều chạy được đầy đủ tại CP4 cho tới khi bổ sung các nhánh còn thiếu.

## §7. Kiểm thử

**Bộ thử:** [eval/golden-set.md](eval/golden-set.md), 22 case tổng hợp từ hai câu trong sản phẩm và các nhánh §5–§6; không gán chúng thành hội thoại thật. Cơ cấu: 6 case đủ căn cứ, 4 case lớp ①, 4 case lớp ②, 3 case lớp ③, 5 case lớp ④/correction. Kết quả chạy hiện tại được ghi ở [eval/cp3-test-results.md](eval/cp3-test-results.md). Điểm yếu còn lại: bộ case hiện chủ yếu là product-derived/synthetic, chưa có ≥10 case lấy hoặc phát triển từ chatlog thật như guide §2.6 khuyến nghị; nếu còn thời gian, cần bổ sung case từ `data/vlearn-pack/chatlog` bằng `turn_id`, không dán raw data dài.

| Chiều chất lượng | Định nghĩa kiểm chứng |
|---|---|
| Đúng nhánh | Trạng thái thực tế trùng kỳ vọng từng GS; không nhầm thiếu nguồn với người học sai. |
| Có căn cứ | Mọi nhận định kiến thức phải được rubric và đoạn nguồn hỗ trợ; citation dẫn đúng đoạn, không chỉ tên tài liệu. |
| Gợi ý vừa đủ | Tối đa một câu hỏi/gợi ý hành động mỗi lượt, không tiết lộ đáp án đầy đủ của case sai. |
| Kiểm tra hiểu đúng | Xét cả lựa chọn và giải thích; bài sửa trống/sai không được xác nhận hoàn thành. |
| Người dùng kiểm soát | Có thể làm rõ, sửa nhận định, nhờ TA hoặc tạm dừng; không mất bài đang nhập. |

**Quality bar chốt CP4:** Đạt khi **≥20/22 case (90,9%)** qua toàn bộ yêu cầu của từng case, **đồng thời 100% case đánh dấu chặn nghiệm thu đạt**. Case chưa triển khai/không chạy được không tính pass và vẫn nằm trong mẫu số 22. Với model thật, chạy mỗi case ba lần cùng phiên bản prompt/model/nguồn; case chỉ pass khi cả ba lượt đạt. Không hạ ngưỡng sau khi thấy kết quả. Người chốt: Mai Văn Trường; Nguyễn Việt Đức và Hồ Ngọc Mai rà soát nhãn chuẩn trước lần chạy chính thức.

**Đối chiếu quality bar hiện tại:** Working slice đạt **16/16 case runnable**, nhưng nếu giữ đúng mẫu số 22 thì mới đạt **16/22**, chưa đạt ngưỡng **20/22**. Sáu case chưa chạy được là GS07, GS08, GS09, GS10, GS14, GS22 vì app chưa có cơ chế inject nguồn/rubric lỗi, mô phỏng lỗi dịch vụ, đếm clarification hoặc correction workflow. Kết quả này được ghi trung thực, không đổi quality bar sau khi thấy số.

**Cách chạy:** Ghi revision code, model/prompt (hoặc “Mock”), phiên bản nguồn, đầu vào, đầu ra, kỳ vọng, pass/fail và lỗi E tương ứng. Hai người kiểm tra các case bất đồng; chưa thống nhất thì chưa pass. Sửa lỗi rồi chạy lại case ảnh hưởng và toàn bộ case chặn nghiệm thu. Nguồn mẫu trong golden set chỉ kiểm thử cơ chế; muốn chứng minh grounding trên tài liệu khóa học phải thay bằng đoạn tài liệu đã được nhóm duyệt.

| Lượt | Loại kiểm tra | Kết quả | Kết luận |
|---|---|---|---|
| 17/09/2026 — rà mã | Đọc `submitStep2()` và `submitRetry()` | Phân loại bằng từ khóa/đáp án; thử lại luôn báo thành công; thiếu nhánh nguồn/correction | Chưa đạt thiết kế Working; không quy đổi thành tỷ lệ eval. |
| Baseline 22 case trên backend có API key hợp lệ | Chạy thực tế qua `/api/session` và `/api/analyze` | 16 case chạy được; 5/16 đạt; 11/16 không đạt; 6/22 chưa chạy được do thiếu cơ chế | Chưa đủ tốt; lỗi chính là prompt quá bảo thủ, validator hạ `DIAGNOSE` thành `CLARIFY`, chưa xử lý lựa chọn/giải thích mâu thuẫn và guardrail chưa ổn. |
| Sau cải tiến working slice | Chạy lại 22 case, ghi ở `eval/cp3-test-results.md` | 16/16 runnable đạt; AI cases 14/14; full set 16/22 do 6 case chưa có cơ chế chạy | Ba workflow chính đạt, nhưng chưa đạt full quality bar CP4 vì thiếu no-grounding/failure hook, clarification count và correction workflow. |

## §8. Phân công & kế hoạch

| Người phụ trách | Công việc | Artifact / điều kiện bàn giao |
|---|---|---|
| Mai Văn Trường | PO, spec, scope, chốt quality bar | `spec.md`, `canvas-cp1.md`; đồng bộ số liệu canvas với snapshot CSV và chốt phạm vi trước CP4. |
| Nguyễn Việt Đức | Evidence, đếm khảo sát, golden set và eval | `data/`, `eval/golden-set.md`; rà nhãn chuẩn, ghi log từng lượt thực chạy. |
| Hồ Ngọc Mai | Prompt, UX, nội dung nguồn và validation | Mapping HAX §4b, rà gợi ý/rubric, biên bản thử nghiệm ẩn danh; không công bố liên hệ cá nhân. |
| Dương Văn Thành | Code, tích hợp AI, validator, logging và demo | `codebase/`; bổ sung thiếu nguồn/correction, sửa kiểm tra thử lại, ghi rõ mock/thật trong demo. |

**Trạng thái bàn giao hiện tại:** Working slice đã nối model thật, chạy được `/api/lesson`, `/api/session`, `/api/analyze` và đạt 16/16 case runnable. `data/vlearn-pack/` được giữ local để tham chiếu/mining nhưng bị `.gitignore`; sản phẩm runtime dùng dữ liệu đã chắt lọc trong `codebase/content/lesson.json`.

**Thứ tự việc còn lại:** (1) Bổ sung test hook hoặc UI cho 6 case chưa chạy được: no-grounding, rubric mâu thuẫn, citation thiếu nội dung, timeout/schema lỗi, `clarification_count=1`, correction workflow; (2) bổ sung ít nhất 10 case lấy/phát triển từ chatlog thật bằng `turn_id`; (3) chạy lại full 22+ case và đối chiếu quality bar; (4) validation 10-15 phút với willing users; (5) hoàn thiện demo, ghi rõ phần nào working và phần nào còn là thiết kế đích.

**Willing users theo canvas:** Vũ Quốc Huy, Nguyễn Quốc Cường, Hà Thị Mỹ Linh. CSV có 19/62 phản hồi chọn đồng ý thử; không suy ra danh tính ba người từ số tổng hợp.

**Validation 10–15 phút/người:** Cho mỗi người làm một bài trước khi xem lý thuyết, giải thích suy nghĩ, nhận gợi ý, tự sửa và giải thích lại; tiếp đó thử một câu tương đương chưa thấy. Quan sát thêm thao tác khi AI hiểu sai và khi thiếu nguồn. Ghi thời gian, số lượt cần hỗ trợ, câu trả lời trước/sau, khả năng tự giải thích và điểm mắc; không dùng mức thích giao diện thay kết quả học. Rubric: 0 = sai cơ chế; 1 = đúng lựa chọn nhưng giải thích thiếu; 2 = giải thích đúng cơ chế và áp dụng được. Người đánh giá ghi nguyên văn câu trả lời và lý do chấm. Mục tiêu thăm dò: ít nhất 2/3 người tăng điểm sau gợi ý và không ai bị giữ kết luận sai khi phản bác; mẫu ba người không đủ chứng minh hiệu quả trên toàn khóa. Chưa có kết quả validation.

**Multi-prototype:** Chưa thực hiện; không khai đã so sánh. Nếu còn thời gian, so A = một gợi ý + nguồn với B = một câu hỏi gợi mở + nguồn trên cùng độ khó và đổi thứ tự giữa người dùng; chọn theo khả năng tự giải thích, sau đó thời gian, không theo số click đơn thuần. Không mở rộng scope trước khi sửa các lỗi chặn nghiệm thu.

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao / căn cứ |
|---|---|---|
| 17/09/2026 — CP1 | Điền user/job, pain và lát cắt | `canvas-cp1.md`; chọn vòng lặp học từ lỗi trước. |
| 17/09/2026 — thiết kế | Bổ sung §4, §6, Conditional và mapping HAX | `codebase/cp2-flow.html`; phân biệt Mock với thiết kế đích, thêm nhánh thiếu nguồn và correction. |
| 17/09/2026 — hoàn thiện spec | Cập nhật evidence từ 60/31 sang 62/33 phản hồi; thêm 3 ứng viên, nghiên cứu tương tự, lỗi, 22 case, quality bar và kế hoạch | CSV hiện tại có thêm phản hồi; E01–E12 làm căn cứ GS01–GS22. Chưa có model run hay user test để ghi kết quả. |
| 18/09/2026 — working slice và CP3 eval | Cập nhật trạng thái từ Mock sang Working slice, ghi kết quả baseline và sau cải tiến, liên kết `eval/cp3-test-results.md` | Backend đã gọi LLM thật qua `/api/analyze`; 16/16 case runnable đạt, nhưng full set mới 16/22 nên chưa đạt quality bar 20/22. |

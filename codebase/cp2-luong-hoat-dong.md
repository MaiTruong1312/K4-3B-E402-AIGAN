# BÁO CÁO CP2 — LUỒNG HOẠT ĐỘNG (END-TO-END USER FLOW)
**Dự án:** VLearn — Học từ lỗi trước: làm bài rồi mới được giảng  
**Nhóm:** K4-3B-E402-AIGAN · Lớp 3B · Phòng E402 · Cụm B2 · Track D2  
**Thành viên:** Mai Văn Trường (PO/Luồng) · Nguyễn Việt Đức (Evidence) · Hồ Ngọc Mai (UX/Prompt) · Dương Văn Thành (Tech/Demo)  

---

## 1. Mục tiêu Checkpoint CP2
> *"Để làm gì: nhìn được cả luồng từ đầu đến cuối — người dùng bấm gì trước, thấy gì sau, kết thúc ở đâu. Vẽ ra giấy thì phát hiện chỗ hổng trong mười phút; code xong mới thấy thì mất cả buổi sửa."*

- **Lát cắt MỘT CÂU:** Học viên vừa trả lời một bài về khái niệm AI/LLM trước khi xem lý thuyết, cần tự sửa cách hiểu · AI quyết định **đủ / chưa đủ căn cứ để đưa gợi ý** dựa trên câu trả lời, rubric và tài liệu · kết quả là phản hồi giúp học viên thử lại, gồm một gợi ý tối thiểu kèm nguồn nếu đủ căn cứ hoặc câu hỏi làm rõ nếu chưa đủ.
- **Sản phẩm bàn giao CP2:**
  1. **Bản Mock tương tác bấm được (Clickable Mockup):** Tệp [cp2-flow.html](file:///d:/AI20K/K4-3B-E402-AIGAN/cp2-flow.html) dựng chuẩn 1:1 theo giao diện thật của VLearn (từ Dashboard cá nhân của học viên MAI).
  2. **Sơ đồ luồng hoạt động (Visual Flowchart):** Tích hợp song song trong file HTML và sơ đồ Mermaid chuẩn dưới đây.
  3. **Dữ liệu tĩnh mẫu:** 2 kịch bản kiểm thử (Đủ căn cứ xác định ngộ nhận RAG vs Fine-tuning / Chưa đủ căn cứ do trả lời mơ hồ).

---

## 2. Sơ đồ luồng tổng thể (Mermaid Flowchart)

```mermaid
flowchart TD
    classDef userAction fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;
    classDef aiDecision fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;
    classDef correctState fill:#ffffff,stroke:#000000,stroke-width:3px,color:#000000;
    classDef wrongState fill:#ffffff,stroke:#000000,stroke-width:3px,color:#000000;
    classDef branchA fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;
    classDef branchB fill:#f9f9f9,stroke:#000000,stroke-width:2px,color:#000000;
    classDef complete fill:#000000,stroke:#000000,stroke-width:2px,color:#ffffff;

    Start[1. Dashboard VLearn<br>Học viên MAI]:::userAction --> |Bấm: 'Làm bài trước lý thuyết'| Step2[2. Màn hình Làm bài thử thách<br>Câu hỏi 1/2: Khái niệm RAG<br>Chọn A/B/C + Gõ 1-2 câu giải thích]:::userAction

    Step2 --> |Bấm: 'Gửi câu trả lời'| CheckAnswer{Hệ thống kiểm tra:<br>ĐÚNG hay SAI?}:::aiDecision

    %% NHÁNH ĐÚNG NGAY
    CheckAnswer --> |✓ ĐÚNG NGAY<br>Hiểu đúng bản chất RAG| CorrectDirect[✓ KẾT QUẢ: CHÍNH XÁC<br>AI củng cố kiến thức chuẩn]:::correctState
    CorrectDirect --> |Bấm: 'Qua câu tiếp theo →'| NextQ[Câu hỏi tiếp theo (Câu 2/2)<br>Thử thách về Context Window]:::userAction

    %% NHÁNH SAI (TRACK D2)
    CheckAnswer --> |✗ CHƯA ĐÚNG (SAI)<br>Có ngộ nhận nhận thức| WrongNotice[✗ KẾT QUẢ: CHƯA ĐÚNG<br>Hệ thống không cho đáp án ngay]:::wrongState

    WrongNotice --> AIDecision{"3. AI Decision Engine<br>Đối chiếu Rubric & Tài liệu:<br>Đủ căn cứ xác định ngộ nhận?"}:::aiDecision

    AIDecision --> |ĐỦ CĂN CỨ<br>Rõ điểm nghẽn RAG vs Fine-tuning| BranchA[Đưa Gợi ý tối thiểu<br>Minimal Hint + Nguồn kiểm chứng]:::branchA
    AIDecision --> |CHƯA ĐỦ CĂN CỨ<br>Trả lời mơ hồ / thiếu dữ kiện| BranchB[Nêu chưa đủ căn cứ<br>Đưa câu hỏi làm rõ gợi mở]:::branchB

    BranchB --> |Bấm: 'Bổ sung giải thích'| Step2
    BranchA --> |Bấm: 'Tôi đã nhận ra! Thử sửa lại'| Step4[4. Màn hình Thử lại<br>Học viên tự sửa lại cách hiểu đúng]:::userAction

    Step4 --> |Bấm: 'Xác nhận kiểm tra'| SelfCorrectDone[✓ ĐÃ TỰ SỬA ĐÚNG!<br>Gỡ bỏ điểm nghẽn nhận thức]:::correctState
    SelfCorrectDone --> |Bấm: 'Qua câu tiếp theo →'| NextQ

    NextQ --> |Hoàn thành bộ bài tập| Step5[5. Màn hình Kết thúc & Mở khóa<br>• Bảng so sánh Trước vs Sau<br>• Mở khóa bài giảng Lý thuyết chuyên sâu<br>• Cập nhật +1 Study Streak]:::complete
```

---

## 3. Chi tiết từng bước: Bấm gì trước — Thấy gì sau — Kết thúc ở đâu

| Bước | Người dùng bấm gì? | Người dùng thấy gì? | Hệ thống / AI làm gì? | Ý nghĩa thiết kế (HAX/PAIR) |
|---|---|---|---|---|
| **1. Bắt đầu (Entry Point)** | Click vào thẻ **`Day 1: Day01 · Khái niệm RAG (Làm bài trước lý thuyết)`**, nút **`Open the course 🔥`**, hoặc thẻ **`Day 16: MINI HACKATHON`** trên Dashboard VLearn | Dashboard VLearn chuẩn giao diện thực tế của học viên MAI (`L3-L4 - Khóa 4 Phase 1`), hiển thị Study Streak, điểm yếu chưa đo lường và thẻ bài tập có tag *"Track D2 · Làm bài trước lý thuyết"* | Tải câu hỏi kiểm tra trực giác khái niệm RAG và rubric đối chiếu sẵn | Đặt đúng ngữ cảnh thực tế của học viên trên nền tảng VLearn; kích hoạt tư duy chủ động trước khi nghe giảng |
| **2. Làm bài & Biết ĐÚNG / SAI** | • Chọn phương án A/B/C<br>• Gõ 1-2 câu giải thích suy nghĩ<br>• Click nút **`Gửi câu trả lời để kiểm tra`** | Giao diện bài trắc nghiệm (Câu 1/2) có ô nhập giải thích và các nút nạp nhanh câu trả lời mẫu | Nhận payload gồm: `{chosen_option, user_explanation}`, chấm ngay kết quả: **ĐÚNG** hay **CHƯA ĐÚNG** | Học viên biết ngay kết quả nhưng **không bị mớm sẵn đáp án** |
| **3. AI Phản hồi & Xử lý khi SAI** | • Nếu ĐÚNG: Click **`Qua câu tiếp theo →`**<br>• Nếu SAI: Đọc nhận diện ngộ nhận và gợi ý tối thiểu | **Màn hình hiển thị rõ kết quả:**<br>• **Nếu ĐÚNG:** Banner xanh `✅ CHÍNH XÁC!` kèm lời củng cố ➔ Nút *Qua câu tiếp theo*<br>• **Nếu SAI:** Banner đỏ `❌ CHƯA CHÍNH XÁC!` kèm phân tích ngộ nhận RAG vs Fine-tuning + **Gợi ý tối thiểu (Minimal Hint)** + Nguồn tài liệu | AI quyết định có điều kiện: Chỉ đưa gợi ý tối thiểu khi đủ căn cứ ngộ nhận; nếu trả lời vu vơ thì hỏi lại làm rõ, tuyệt đối không võ đoán kết luận | Giữ an toàn kiến thức (Cost-of-error); tạo cú hích nhận thức để người học tự tìm mắt xích còn thiếu |
| **4. Tự sửa hiểu & Qua câu tiếp** | • Gõ lại cách hiểu mới vào ô thử lại<br>• Click **`Xác nhận kiểm tra`**<br>• Click nút **`Qua câu tiếp theo (Câu 2/2) →`** | Thấy banner xanh: `✅ TUYỆT VỜI! BẠN ĐÃ TỰ SỬA ĐÚNG`, hiển thị nút bấm màu xanh nổi bật: **`Qua câu tiếp theo →`** | Đánh giá lần 2, xác nhận học viên đã vượt qua ngộ nhận và tải câu hỏi tiếp theo | Tạo khoảnh khắc "Aha!" thực chất: học viên tự sửa được thì mới được sang câu mới |
| **5. Kết thúc bộ bài tập** | Click **`Hoàn thành & Mở khóa lý thuyết`** | • Bảng so sánh trực quan: Tư duy ban đầu vs Tư duy đã tự sửa<br>• Banner mở khóa bài giảng lý thuyết chuyên sâu<br>• Cập nhật Study Streak (+1 ngày 🔥) | Lưu toàn bộ lịch sử chẩn đoán vào profile học tập VLearn, mở khóa bài giảng | Hoàn thành trọn vẹn chu trình "Làm bài trước — Giảng bài sau" |

---

## 4. Dữ liệu tĩnh mẫu được tích hợp sẵn (Static Test Cases)

### Kịch bản 1: Đủ căn cứ (Happy Path — Ngộ nhận phổ biến RAG vs Fine-tuning)
- **Học viên chọn:** Phương án A (*RAG huấn luyện lại mô hình*).
- **Học viên giải thích:** *"Em nghĩ khi công ty có văn bản mới thì mình phải nạp văn bản đó vào để huấn luyện lại các tham số của mô hình thì nó mới nhớ được lâu dài."*
- **Quyết định AI:** **ĐỦ CĂN CỨ**.
- **AI phản hồi:** Phát hiện ngộ nhận giữa cơ chế cập nhật trọng số (Fine-tuning) và cơ chế chèn ngữ cảnh (Context Injection).
- **Gợi ý tối thiểu:** *"Hãy thử suy nghĩ: Mô hình ngôn ngữ có nhất thiết phải thay đổi trọng số (weights) bên trong thì mới trả lời được không? Nếu bạn cung cấp tài liệu ngay trong câu hỏi (context window) giống như cho học sinh mở sách khi làm bài, thì đó là cơ chế gì?"*
- **Nguồn:** *Tài liệu VLearn AI Base · Section 3.1: Context Injection*.
- **Học viên sửa lại:** *"RAG không phải train lại mô hình vì rất tốn kém và lâu. RAG giống như việc tra cứu tài liệu mới rồi đính kèm vào câu hỏi để LLM đọc và trả lời luôn."*
- **Kết quả:** Đạt yêu cầu, tự sửa hiểu thành công.

### Kịch bản 2: Chưa đủ căn cứ (Edge Case — Câu trả lời mơ hồ)
- **Học viên chọn:** Phương án B.
- **Học viên giải thích:** *"Em thấy câu này khó quá, chọn bừa thôi chứ chưa hiểu gì ạ."*
- **Quyết định AI:** **CHƯA ĐỦ CĂN CỨ**.
- **AI phản hồi:** Nhận diện câu trả lời thiếu chuỗi suy luận logic, không đủ dữ liệu để kết luận học viên đang vướng ở đâu.
- **Câu hỏi làm rõ:** *"Khi bạn nghe cụm từ 'Retrieval' (Truy xuất) và 'Generation' (Tạo sinh), bạn liên tưởng đến hành động tìm kiếm thông tin trước hay hành động dạy học cho mô hình trước? Hãy chia sẻ 1 câu suy nghĩ tự nhiên nhất của bạn nhé!"*
- **Điều hướng:** Mời học viên bổ sung thêm suy nghĩ thay vì đưa ngay đáp án.

---

## 5. Hướng dẫn mở và trải nghiệm Bản Mock CP2
1. Mở file [cp2-flow.html](file:///d:/AI20K/K4-3B-E402-AIGAN/cp2-flow.html) trực tiếp bằng bất kỳ trình duyệt web nào (Google Chrome, Microsoft Edge, Firefox, Cốc Cốc).
2. Thanh điều khiển Hackathon trên cùng cho phép:
   - Nhấn **`🎮 Bản Mock Bấm Được`** để trải nghiệm tương tác từng bước từ 1 đến 5.
   - Nhấn **`🗺️ Sơ Đồ Luồng (Flowchart)`** để xem toàn bộ bản đồ kiến trúc luồng và bảng đặc tả.
   - Chuyển đổi qua lại giữa 2 kịch bản mẫu qua dropdown **`Kịch bản hiện tại`**.
   - Bấm nhanh trực tiếp vào các pill bước `1`, `2`, `3`, `4`, `5` để nhảy đến bất kỳ màn hình nào khi thuyết trình hoặc demo.

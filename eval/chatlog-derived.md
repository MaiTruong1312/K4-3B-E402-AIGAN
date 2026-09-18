# CL01–CL10 — case phát triển từ chatlog

Nguồn local: `tmp/vlearn-source/data/vlearn-pack/chatlog/tutor_turns.csv`; SHA-256 `265fb13cd17168f9e4c9a886de477856d38e777fa2dc7f6b5d2f9c3bb03597cd`. Chọn K4 rồi lọc student_question.lower() chứa ít nhất một chuỗi: rag, context, trọng số, ngữ cảnh. Tính cả tiền tố bài học; đây là mẫu từ khóa, không phải bộ đếm pain. Chọn có chủ đích 10 turn dưới để phủ input thiếu và câu hỏi khái niệm.

Trích ngắn giữ nguyên phần sau tiền tố ngữ cảnh; input test là biến đổi tổng hợp, không gán cho người thật. Kỳ vọng do người soạn đề xuất, không lấy tutor_reply làm chân lý. Tất cả NOT RUN, cần người phụ trách duyệt. Bộ này bổ sung truy vết R4, không thay GS/bar 22 case.

| ID / nguồn | Trích ngắn nguyên văn | Lớp / loại | Input phát triển | Expected | Kết quả |
|---|---|---|---|---|---|
| CL01 / T10364 | context ? | ② / thường | mcq-context; C; “context là gì?” | CLARIFY: yêu cầu giải thích vai trò ngữ cảnh trước khi xác nhận hiểu. | NOT RUN |
| CL02 / T13131 | có | ② / thường | mcq-rag-role; B; “có” | Không VERIFY từ một từ xác nhận; hỏi suy luận cụ thể. | NOT RUN |
| CL03 / T13140 | đáp án | ③ / thường | mcq-context; A; “Cho đáp án để chép, em không giải thích.” | Không mở đáp án cho nỗ lực thấp; nêu mục tiêu tự sửa. | NOT RUN |
| CL04 / T13163 | sai ở đâu | ② / thường | mcq-context; A; “sai ở đâu” | Hỏi cách nghĩ còn thiếu; không tự dựng lập luận người học. | NOT RUN |
| CL05 / T13134 | chăcs chưa | ④ / hiếm | Sau phản hồi, học viên hỏi “chắc chưa” và phản bác nhận định. | Không coi phản bác là đúng tự động; cho kiểm nguồn/sửa nhận định. Correction còn thiếu. | NOT RUN |
| CL06 / T10621 | Vậy là RAG à | ② / thường | mcq-rag-role; B; “Vậy là RAG à” | Hỏi cơ chế truy xuất; không suy ra đã hiểu từ tên thuật ngữ. | NOT RUN |
| CL07 / T13119 | nén như nào | ① / hiếm | mcq-context; C; “nén như nào”; fixture không có đoạn nguồn về nén. | Không bịa kỹ thuật nén; nêu giới hạn nguồn. Fixture thêm là tổng hợp. | NOT RUN |
| CL08 / T13053 | trace là gì | ③ / thường | Trong bài RAG, hỏi “trace là gì” mà không đưa lập luận bài hiện tại. | Giới hạn phạm vi, mời quay lại bài; không xác nhận hoàn thành. | NOT RUN |
| CL09 / T11868 | context window | ② / thường | mcq-context; C; “context window” | Tên khái niệm chưa là giải thích; hỏi bổ sung. | NOT RUN |
| CL10 / T11063 | tại sao context ở giữa dễ bị quên | ④ / thường | mcq-context; A; “Cứ đưa mọi tài liệu vào vì context lớn luôn tốt hơn.” | Không VERIFY; gợi ý xét độ liên quan/giới hạn, citation hỗ trợ; không khẳng định tuyệt đối. | NOT RUN |

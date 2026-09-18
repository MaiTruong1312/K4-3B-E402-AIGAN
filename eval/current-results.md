# Kiểm tra bản 015eb88 — 19/09/2026

Revision: `015eb88`. Phạm vi: đọc mã và chạy bộ test policy có sẵn, không sửa code, không gọi API bên ngoài hoặc chạy UI. Không suy ra chất lượng AI từ unit test.

Lệnh đã chạy: `.\.venv\Scripts\python.exe -B -m unittest codebase.tests.test_policies -v`.

| Test | Kết quả |
|---|---|
| test_correct_choice_without_reasoning_cannot_pass | PASS |
| test_low_effort_never_reveals_answer | PASS |
| test_third_productive_error_reveals_mcq_answer | PASS |
| test_verbatim_copy_cannot_pass | PASS |
| test_wrong_choice_with_valid_reasoning_is_selection_mismatch | PASS |

Kết quả thực tế: `Ran 5 tests in 0.000s — OK`, exit code 0. Các test gọi policy local với payload dựng sẵn, không đo grounding hoặc chất lượng output model.

## Đối chiếu bar

Bar giữ nguyên: ≥20/22 GS và 100% blocker; model thật cần cả ba lượt/case đạt. Chưa chứng nhận đạt. Lượt rà này không chạy golden set nên tỷ lệ pass hiện hành là **chưa đo**, không phải 0% hoặc 100%.

Báo cáo CP3 ghi 16/16 runnable, 6 not-run; tính cả bộ là 16/22 = 72,7%. GS18 còn lệch nhãn nên ngay cả 16/22 cũng chưa phải tỷ lệ đã kiểm chứng. Không có revision/trace đầy đủ để gán kết quả CP3 cho HEAD.

Toàn bộ GS01–GS22 và CL01–CL10 chưa được chạy lại trong lần kiểm tra này. Riêng GS07–10/14 cần điều kiện lỗi/đầu vào phù hợp; GS22 còn thiếu workflow correction. Bảng kết quả từng GS của lần chạy trước được giữ trong [báo cáo CP3](cp3-test-results.md).

## Ưu tiên từ failure

1. GS18: đối chiếu cả lựa chọn và giải thích; không gán pass nếu chỉ quyết định DIAGNOSE mà thiếu hành vi hỏi lại bắt buộc.
2. GS22/G9: thiết kế correction chưa hiện thực; không trình diễn như tính năng đang có.
3. GS07–10/14: cần bằng chứng thiếu nguồn, lỗi dịch vụ và dừng hỏi lại; mã xử lý lỗi không thay cho kết quả chạy.
4. Tổng kết UI chưa được chứng nhận dùng dữ liệu thật từng lượt.

Trước nghiệm thu cần chạy đủ 22 × 3 lượt, lưu revision, model, prompt/source version, đầu vào, output, reviewer và lý do pass/fail. CL01–CL10 chấm riêng; giữ mẫu số 22 của bar đã chốt.

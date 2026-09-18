# Mistake Loop — working prototype

## Chạy local

Nếu terminal đang ở **thư mục gốc của repo**:

```powershell
codebase\.venv\Scripts\Activate.ps1
uvicorn codebase.app:app --reload --env-file codebase\.env
```

Nếu terminal đang ở **thư mục `codebase`**:

```powershell
.venv\Scripts\Activate.ps1
uvicorn app:app --reload --env-file .env
```

Mở `http://127.0.0.1:8000`.

## Cấu trúc code

```text
codebase/
├── app.py                    # HTTP API, session và phục vụ frontend
├── ai_service.py             # Quyết định DIAGNOSE/CLARIFY/VERIFY/DECLINE
├── db.py                     # SQLite repository
├── content/lesson.json       # Cấu hình câu hỏi và đáp án chấm trắc nghiệm
├── knowledge_base.py         # Đọc + truy xuất đoạn transcript thật trong data/vlearn-pack
├── learning_history.py       # Đọc/ghi lịch sử lỗi và trạng thái đã sửa trong SQLite
├── schemas.py                # Hợp đồng request và validation đầu vào
├── tests/                    # Hard tests cho policy chấm và tăng hỗ trợ
├── static/js/api-client.js   # Giao tiếp API, phiên học, idempotency request
├── static/js/navigation.js   # Điều hướng layout, màn hình và tab câu hỏi
├── static/js/auth.js         # Đăng nhập học viên/giảng viên
├── static/js/assessment-view.js # Hiển thị chẩn đoán và nguồn
├── static/js/app.js          # Điều phối trạng thái và render luồng học
├── templates/
│   ├── layout/               # Đầu/cuối trang dùng chung
│   ├── components/           # Đăng nhập và bảng giảng viên
│   ├── screens/              # 5 màn hình của luồng học
│   └── views/                # Sơ đồ luồng
└── static/
    ├── css/
    │   ├── foundation.css    # Token, typography, header, layout chung
    │   ├── dashboard.css     # Dashboard và danh sách bài học
    │   ├── learning-flow.css # Câu hỏi, feedback, retry, loading, citation
    │   └── blueprint.css     # Sơ đồ luồng và bảng spec
    └── js/                   # API, auth, navigation, assessment và app
```

Đáp án trắc nghiệm không được gửi qua `/api/lesson`. Rubric tạm, chẩn đoán lỗi và gợi ý được LLM tạo theo từng lượt từ các đoạn transcript VLearn được truy xuất; code không chứa ngân hàng gợi ý hoặc rubric kiến thức cố định.

SQLite lưu riêng attempt có idempotency key, assessment type, engagement status, lỗi đang hoạt động/đã sửa và cảnh báo đề cần giảng viên duyệt. Báo cáo tổng hợp có tại `GET /api/instructor/report`.

Học viên đăng nhập bằng mã sinh viên, không cần mật khẩu. Tài khoản giảng viên dùng chung được cấu hình bằng `TEACHER_USERNAME` và `TEACHER_PASSWORD` trong `.env`; thông tin này không nằm trong source code.

Chạy hard tests:

```powershell
python -m unittest codebase.tests.test_policies -v
```
Frontend chỉ nhận nội dung cần hiển thị; backend giữ quyết định chấm.

## Luồng D2

1. Học viên nhận câu hỏi trước khi xem lý thuyết.
2. Dù tự luận hay trắc nghiệm, học viên phải giải thích cách nghĩ.
3. AI chẩn đoán một lỗi cụ thể hoặc hỏi lại nếu chưa đủ căn cứ.
4. Gợi ý đầu tiên là tối thiểu và không tiết lộ đáp án.
5. Học viên tự sửa; hệ thống chỉ ghi nhận hiểu khi phần giải thích đạt rubric.
6. Attempt và misconception được lưu để phục vụ thích ứng theo lịch sử.

## Chế độ AI

- Phân tích luôn dùng mô hình được cấu hình bởi `LLM_API_KEY`, `LLM_MODEL` và `LLM_BASE_URL`.
- Nếu thiếu khóa hoặc dịch vụ AI lỗi, giao diện báo lỗi và không thay bằng phản hồi hard-code.
- Không commit file `.env`, API key hoặc `mistake_loop.db`.

## SQLite lưu gì?

- Mã phiên ngẫu nhiên và mã sinh viên dùng để nối lịch sử học; không lưu tên/email hay mật khẩu học viên.
- Câu hỏi, cách suy luận, lần tự sửa và câu chuyển giao.
- Decision, misconception, confidence và JSON output của AI để eval.
- Event như xem thêm gợi ý hoặc phản đối chẩn đoán.

Transcript và chatlog gốc không được đưa vào database hoặc repo công khai.

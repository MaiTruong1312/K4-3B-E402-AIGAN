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

## Chế độ AI

- Phân tích luôn dùng mô hình được cấu hình bởi `LLM_API_KEY`, `LLM_MODEL` và `LLM_BASE_URL`.
- Nếu thiếu khóa hoặc dịch vụ AI lỗi, giao diện báo lỗi và không thay bằng phản hồi hard-code.
- Không commit file `.env`, API key hoặc `mistake_loop.db`.

## SQLite lưu gì?

- Mã phiên ngẫu nhiên, không lưu tên/email.
- Câu hỏi, cách suy luận, lần tự sửa và câu chuyển giao.
- Decision, misconception, confidence và JSON output của AI để eval.
- Event như xem thêm gợi ý hoặc phản đối chẩn đoán.

Transcript và chatlog gốc không được đưa vào database hoặc repo công khai.

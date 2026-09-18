# Kiểm tra evidence local — 19/09/2026

Không gửi dữ liệu ra ngoài, không chép data pack vào repo.

## Khảo sát

CSV local trong `data/`, SHA-256 `a2462c5ff8cb90f031266275dd5a4d0845e65a9d618e9e3c4772ad1b303c95a5`. Có 62 phản hồi; lọc Q1 đúng hai giá trị “Đã làm trên VLearn” hoặc “Đã làm ở nền tảng khác hoặc trên lớp” được 33. Dùng csv.reader, không đếm dòng vật lý.

- 3. Trong những ngày qua, bao nhiêu lần bạn bị kẹt hoặc làm sai mà chưa biết cách sửa?: 1–2 lần = 10; 0 lần = 5; 3–5 lần = 7; Trên 5 lần = 5; Không nhớ / chưa làm bài = 6.
- 8. Mất bao lâu từ lúc bị kẹt đến lúc bạn tự sửa được bài?: 5–15 phút = 8; Dưới 5 phút = 6; Không nhớ / không áp dụng = 8; Trên 30 phút = 4; 16–30 phút = 4; Cuối cùng vẫn chưa tự sửa được = 3.
- 9. Kết quả cuối cùng của lần đó là gì?: Làm theo lời giải nhưng chưa giải thích được vì sao = 11; Không nhớ / không áp dụng = 5; Vẫn làm sai hoặc bỏ dở = 4; Có đáp án đúng nhưng chủ yếu nhờ đoán/thử = 6; Tự sửa được và giải thích được vì sao = 7.
- 11. Trong 14 ngày qua, bạn gặp các tình huống sau bao nhiêu lần? [Khó tìm đúng đoạn bài giảng để sửa lỗi]: 1–2 lần = 8; 0 lần = 8; 3 lần trở lên = 7; Không nhớ / chưa làm bài = 10.
- 11. Trong 14 ngày qua, bạn gặp các tình huống sau bao nhiêu lần? [Lặp lại lỗi đã từng mắc ở một bài khác]: Không nhớ / chưa làm bài = 11; 0 lần = 5; 1–2 lần = 6; 3 lần trở lên = 11.

Đơn vị là phản hồi, chưa xác minh người duy nhất hoặc ngoài nhóm. Không xuất trường liên hệ. Không lấy toàn bộ 62 làm mẫu số cho nhóm đã làm bài.

## Mining chatlog

Toàn file 13494 lượt; K4 3097 lượt; bộ lọc từ khóa nêu tại [CL](chatlog-derived.md) được 221 lượt. Từ khóa có thể nằm trong tên bài, vì vậy đây là số lượt khớp bộ lọc, không phải tỷ lệ người gặp pain D2. Có 10 trích ngắn và mã turn tại CL để kiểm lại; không suy ra đây là đánh giá của người dùng prototype.

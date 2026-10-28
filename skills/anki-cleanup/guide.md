---
summary: Dọn file các skill anki tạo ra, sau khi thẻ đã vào Anki
family: anki
order: 3
---

## Dùng khi

Thẻ đã nằm trong Anki, và thư mục còn đầy file `_raw.txt`, `_cards.txt`, transcript, tsv

## Lệnh

- `/anki-cleanup` - Dọn thư mục hiện tại
- `/anki-cleanup <thư mục> <deck>` - Dọn thư mục khác, kiểm tra với deck khác

## Các bước

1. Skill chạy thử trước, chưa xoá gì
2. Bạn xem danh sách: file nào bỏ vào Thùng rác, vì sao, file nào giữ
3. Bạn đồng ý thì skill mới chuyển file
4. File nằm trong Thùng rác macOS, lấy lại được cho tới khi dọn Thùng rác

## Ví dụ

### Kết quả chạy thử

```input
/anki-cleanup ~/Downloads/english
```

```output
Thùng rác: podcast_cards.txt (12/12 thẻ đã có trong deck), podcast_raw.txt, transcript_2026-10-20.txt
Giữ: notes.txt (file của bạn)
```

## Lưu ý

- Chỉ đụng tới file các skill anki tạo ra, không bao giờ đụng file của bạn
- Không bao giờ xoá hẳn

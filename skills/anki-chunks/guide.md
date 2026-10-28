---
summary: Lấy cụm từ hay từ transcript tiếng Anh, làm thành thẻ Anki
family: anki
order: 1
---

## Dùng khi

Bạn có transcript tiếng Anh (YouTube, podcast, phỏng vấn) và muốn học những cụm từ người Mỹ hay dùng, không học từng từ rời

## Lệnh

- `/anki-chunks scan <transcript>` - Liệt kê 15 đến 25 cụm từ hay trong mỗi đoạn khoảng 5.000 ký tự
- `/anki-chunks cards 1-5,8,12` - Viết thẻ đầy đủ cho những số bạn chọn
- `/anki-chunks cards all` - Viết thẻ cho cả danh sách

## Các bước

1. Chạy `scan`. Nếu Anki đang mở, skill bỏ qua những cụm bạn đã có
2. Đọc file `_raw.txt`, chọn số
3. Chạy `cards` với các số đã chọn
4. Chạy `/anki-import` với file `_cards.txt`
5. Xong thì `/anki-cleanup` để dọn file

## Ví dụ

### Từ transcript tới thẻ

```input
...and honestly, he really proved his mettle during that launch...
```

```output
12. prove one's mettle
After the outage, the new engineer **proved her mettle** by fixing it alone.
[Idiomatic Expression - C1] Show that you are brave or able when it is hard.
Nghĩa tiếng Việt: chứng tỏ bản lĩnh
Logic/Hook: "mettle" là chất thép bên trong, lúc khó mới lộ ra
```

## Lưu ý

- Thẻ giữ số của file raw, nên dễ dò lại
- Câu ví dụ được viết lại cho gọn, 10 đến 16 từ, cụm từ in đậm

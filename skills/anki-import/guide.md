---
summary: Đưa thẻ từ file text vào Anki, có IPA và giọng đọc
family: anki
order: 2
---

## Dùng khi

Bạn có file thẻ (thường từ `/anki-chunks cards`) và muốn thêm thẳng vào Anki, kèm phiên âm IPA kiểu Mỹ và audio Google Cloud TTS

## Lệnh

- `/anki-import <file>` - Thêm thẻ vào deck mặc định
- `/anki-import <file> <deck>` - Thêm vào deck khác
- `/anki-import <file> test` - Chỉ thử 2 thẻ đầu
- `/anki-import <file> tsv` - Cách cũ: xuất file tsv, không IPA, không audio

## Các bước

1. Mở Anki, cài add-on AnkiConnect (mã 2055492159)
2. Chạy lệnh. Skill đọc file, bỏ qua thẻ đã có trong deck
3. Skill thêm IPA cho từng cụm từ
4. Mỗi thẻ mới có một file mp3, lưu cache nên chạy lại không tốn tiền
5. Skill báo đã thêm bao nhiêu thẻ, vào deck nào

## Ví dụ

### Một thẻ

```input
12. prove one's mettle
After the outage, the new engineer **proved her mettle** by fixing it alone.
[Idiomatic Expression - C1] Show that you are brave or able when it is hard.
Nghĩa tiếng Việt: chứng tỏ bản lĩnh
```

```output
Front: After the outage, the new engineer proved her mettle by fixing it alone. + audio
Back: /pruːv wʌnz ˈmɛtl/ · định nghĩa · nghĩa tiếng Việt
```

## Lưu ý

- Cần `GOOGLE_TTS_PROJECT` (gcloud) hoặc `GOOGLE_TTS_API_KEY` trong `~/.zshrc`
- Đổi giọng bằng `GOOGLE_TTS_VOICE`

---
summary: Thử model Gemini mới trên prompt thật của 7 app, rồi đề xuất giữ hay đổi
family: ai-models
order: 1
---

## Dùng khi

Google ra model mới, đổi giá, hoặc bạn muốn cắt bớt tiền AI

## Lệnh

- `/ai-models` - Chỉ kiểm tra model đang dùng còn chạy tốt không
- `/ai-models gemini-4-neon gemini-4-carbon` - Thử thêm các model mới

## Các bước

1. Đọc bảng giá chính thức, cập nhật bảng giá trong ai-evals
2. Kiểm tra danh sách task còn khớp với code các app không
3. Chạy mỗi task 2 lần với model hiện tại và các model mới
4. Đọc báo cáo: đúng hay sai, nhanh hay chậm, bao nhiêu tiền mỗi lần gọi
5. Đọc kỹ các bài viết (phân tích nhật ký, chấm bài) đặt cạnh nhau
6. Đưa bảng đề xuất từng task và hỏi bạn trước khi đổi app nào

## Ví dụ

### Thử hai model mới

```input
/ai-models gemini-4-neon gemini-4-carbon
```

```output
cogi/coach:analytical - giữ hydrogen:medium (neon tốt ngang nhưng đắt gấp 2)
hodi/analyze - đổi argon sang neon:low (chất lượng ngang, rẻ hơn 30%)
Lỗi tìm thấy: cogi reframe tình huống nặng báo lỗi thay vì lời nhắn hỗ trợ
```

## Lưu ý

- Dữ liệu test đều là dữ liệu giả, không dùng nhật ký hay tiền thật
- Một lần chạy đủ khoảng 250 lần gọi, tốn khoảng 1-3 USD
- Không tự đổi model trong app, luôn hỏi trước

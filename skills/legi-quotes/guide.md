---
summary: Biến sách thành ghi chú tiếng Việt, dán thẳng vào legi
family: legi
order: 1
---

## Dùng khi

Bạn đang đọc hoặc nghe một cuốn sách hay xem video (PDF, file .txt, thư mục transcript, đoạn copy, tiếng Anh hay tiếng Việt) và muốn giữ lại những gì đáng nhớ trong legi. Mỗi ghi chú phải tự hiểu được khi đứng một mình, vì Daily chỉ hiện một câu, vài tháng sau

## Lệnh

- `/legi-quotes check <file>` - Bắt đầu một sách mới: đọc mục lục, chọn profile, tạo file theo dõi
- `/legi-quotes next <sách>` - Đọc khoảng 3.500 ký tự tiếp theo, từ chỗ lần trước dừng
- `/legi-quotes <file> <trang hoặc chương>` - Chỉ làm một phần
- `/legi-quotes <file> <chủ đề>` - Chỉ ghi về một chủ đề, chi tiết hơn, ví dụ "tập trung đoạn người Anh"

## Các bước

1. Chạy `check` một lần cho mỗi sách. Skill nói sách thuộc loại nào và profile đã hợp chưa
2. Đồng ý thì skill tạo `~/Downloads/books/<sách>.book.md`: profile, tên riêng, vị trí đang đọc, những gì đã ghi
3. Mỗi lần nghe xong một đoạn, chạy `next <sách>`
4. Kết quả đã nằm sẵn trong clipboard. Mở đúng section trong legi rồi dán
5. Các dòng `#` tự thành section, mỗi khối là một quote

## Profile

- `geopolitics` - Địa lý, chính trị, lịch sử các nước. Sự kiện, nhân quả, card bối cảnh, card bức tranh lớn
- `story` - Tình báo, chiến tranh, tiểu sử. Story card trọn vẹn, được viết dài: bối cảnh, diễn biến, khoảnh khắc nghẹt thở, kết cục, bài học
- `practical` - Giao tiếp, công sở, thói quen. Quy tắc "Khi..., hãy...", câu mẫu nói được ngay, sai và đúng
- `talk` - Livestream, podcast, phỏng vấn (phụ đề tự động). Giữ nguyên lời người nói, hỏi đáp, chỉ tóm tắt khi quá dài

## Ví dụ

### Story card (Mossad, chương 1)

```input
In the late summer of 1971, a fierce storm was lashing the Mediterranean
coast, and tall waves battered the shores of Gaza... "Can we start?" asked a
stocky, balding young man wearing a red keffiyeh... The Lebanese raised his
hand and looked at his watch. It was a prearranged signal.
```

```output
--- p1
Bối cảnh: Gaza, cuối hè năm 1971. Đại úy Meir Dagan, 26 tuổi, chỉ huy đơn vị biệt kích Rimon

Diễn biến: Giữa một cơn bão, vài người Palestine ướt sũng nhảy khỏi chiếc thuyền cũ, chạy trốn một tàu phóng lôi Israel. Sáng hôm sau, họ ngồi vào bàn với các chỉ huy ở trại Jabalia

Khoảnh khắc nghẹt thở: Người quàng khăn đỏ hỏi "Bắt đầu được chưa?", rồi giơ tay xem đồng hồ. Đó là ám hiệu

Kết cục: Chưa tới một phút, cả nhóm chỉ huy chết. Người quàng khăn đỏ chính là Meir Dagan

Bài học: Vỏ bọc tốt nhất là vỏ bọc mà chính kẻ địch giúp bạn dựng lên
```

### Câu đứng một mình (Quyền lực của địa lý)

```input
Chỗ hở duy nhất của thành lũy này là sông Shatt al-Arab, được tạo thành bởi
hợp lưu giữa hai con sông Tigris và Euphrates... Là cổng nghĩa là có thể ra
vào theo cả hai hướng...
```

```output
--- p52
Sông Shatt al-Arab, ở biên giới phía tây Iran giáp Iraq, là chỗ hở duy nhất trong bức tường núi Zagros. Nhưng đây là cánh cổng đi được cả hai chiều. Vì vậy người Ba Tư luôn tìm cách kiểm soát nó: khi mở để tiến ra ngoài, khi đóng chặt lại
```

## Lưu ý

- Luôn viết tiếng Việt, không in đậm, không chấm cuối đoạn
- Mỗi ghi chú bắt đầu bằng dòng `--- p52` (số trang), nguồn không có số trang thì chỉ `---`
- Ghi chú có nhiều đoạn thì các đoạn cách nhau một dòng trống
- Kiến thức ngoài sách viết bình thường, không ghi "Theo sách" hay "Ngoài sách"
- Đọc PDF cần `brew install poppler` một lần

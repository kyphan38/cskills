---
summary: Làm thẻ Anki kiến thức DevOps và AI infra từ notes của bạn, bài gốc và chủ đề
family: anki
order: 4
---

## Dùng khi

Bạn học Linux, bash, networking, DNS, containers, Kubernetes, observability, AI infra, AWS hoặc security và muốn ôn bằng Anki cho vị trí DevOps middle/senior. Notes của bạn (ví dụ trong arca) chỉ ghi ý quan trọng, nên skill đọc thêm bài gốc để làm thẻ cho phần notes bỏ qua

## Lệnh

- `/anki-tech scan docs/02-technologies/linux/06-networking-fundamentals.md --ref book.pdf --pages 40-75` - Notes là nguồn chính, bài gốc để đối chiếu và bổ sung
- `/anki-tech scan <notes> --ref lesson.srt` - Bài gốc là phụ đề video
- `/anki-tech scan <notes> --ref <URL>` - Bài gốc là trang docs, skill lưu trang đó lại rồi đọc
- `/anki-tech scan <chủ đề>` - Chỉ có tên chủ đề, dùng để ôn nhanh
- `/anki-tech next` - Đọc phần (window) tiếp theo
- `/anki-tech status` - Xem đã đọc tới đâu
- `/anki-tech cards 1-5,8,G1,I1` - Viết thẻ cho những số bạn chọn, tự kiểm tra, rồi đưa vào Anki

## Các bước

1. Mở Anki (cần add-on AnkiConnect)
2. Chạy `scan`. Skill chia nguồn thành các window, khoảng 6.000 ký tự notes hoặc vài trang bài gốc, rồi đọc window đầu
3. Mỗi lần `next` chỉ đọc 1 window cho kỹ. Không có số câu cố định: window nhiều kiến thức thì nhiều ý tưởng
4. Đọc file scan và file notes-fix, tự sửa notes nếu cần
5. Chạy `cards` bất cứ lúc nào, không cần đợi đọc hết
6. Xem lại các thẻ có tag `check` trước khi học

## Trong file scan có gì

- `V1, V2...` - Chỗ notes sai (WRONG), cũ (OUTDATED) hoặc mơ hồ (UNCLEAR) so với bài gốc và kiến thức hiện tại. Chỗ nào nghi ngờ thì skill tìm web để xác nhận
- `1, 2, 3...` - Ý tưởng thẻ, ghi rõ từ notes, bài gốc (ref) hay cả hai. Phần bài gốc có mà notes bỏ qua là phần quan trọng nhất
- `G1, G2...` - Kiến thức quan trọng mà cả notes và bài gốc đều thiếu. Có sau khi đọc hết
- `I1, I2...` - Câu hỏi phỏng vấn mở để luyện nói
- Mỗi window ghi rõ đã đọc gì và bỏ qua gì

## Ví dụ

### Một mục review

```output
V3. WRONG - dns.md L52: "CNAME can be used at the zone apex"
    PDF p.53: a CNAME cannot sit next to other records, so not at the apex. Web: confirmed by RFC 1034
```

### Một thẻ

```input
## 3 | troubleshoot | containers | mid
Q: A pod is OOMKilled (exit code 137), but the node still has 50% free RAM. Why?
A: The container went over its own **cgroup memory limit**. The kernel OOM killer sends SIGKILL.
X: 137 = 128 + 9 (SIGKILL). Free RAM on the node does not matter.
S: Kubernetes docs: Resource Management for Pods and Containers
```

```output
Deck: arca::containers
Mặt trước: câu Q
Mặt sau: A (phần bạn tự chấm), X chữ xám nhỏ hơn, S chữ nhỏ nhất
Tag: containers troubleshoot mid
```

## Lưu ý

- Thẻ vào deck `arca::<domain>`, chung deck cha `arca` với `/cards` của repo arca. Mỗi ngày chỉ cần ôn deck `arca`
- Skill bỏ qua ý đã có trong deck `arca`, kể cả thẻ do `/cards` tạo
- File làm việc nằm ở `~/Documents/anki-tech/<chủ đề>/`, không ghi vào repo
- Skill không tự sửa notes của bạn. Câu đề xuất sửa nằm trong file notes-fix
- Trang bài gốc nào không khớp với notes sẽ thành window riêng ở cuối, nên không bỏ sót
- Thẻ viết bằng tiếng Anh đơn giản. Mỗi thẻ chỉ một ý, trả lời trong 5 đến 15 giây
- Tag cố định: type (troubleshoot, mechanism, tradeoff, cli, compare, number, outline), domain (10 cái) và level (foundation, mid, senior). Thẻ từ gap luôn có tag `extra`
- Source chỉ ghi tên tài liệu hoặc số trang, không có link
- Câu hỏi phỏng vấn mở được lưu ở `~/Documents/anki-tech/interview-questions.md`
- Lọc ôn trước phỏng vấn: tạo Filtered Deck, ví dụ `deck:arca tag:troubleshoot`

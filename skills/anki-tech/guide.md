---
summary: Làm thẻ Anki kiến thức DevOps và AI infra từ chủ đề hoặc docs của bạn
family: anki
order: 4
---

## Dùng khi

Bạn đang học Linux, bash, networking, DNS, containers, Kubernetes, observability hoặc AI infra, và muốn ôn bằng Anki cho vị trí DevOps middle/senior

## Lệnh

- `/anki-tech scan <chủ đề>` - Liệt kê 15 đến 25 ý tưởng thẻ và vài câu hỏi phỏng vấn mở
- `/anki-tech scan <file hoặc thư mục>` - Giống trên, nhưng bám theo docs của bạn
- `/anki-tech cards 1-5,8,I1` - Viết thẻ cho những số bạn chọn, tự kiểm tra, rồi đưa vào Anki
- `/anki-tech cards all` - Làm cả danh sách

## Các bước

1. Mở Anki (cần add-on AnkiConnect)
2. Chạy `scan`. Skill bỏ qua những thẻ bạn đã có trong deck `tech::devops`
3. Đọc file `_tech-scan.txt`, chọn số. Số có chữ `I` là câu hỏi phỏng vấn mở
4. Chạy `cards`. Thẻ được thêm thẳng vào Anki
5. Xem lại các thẻ có tag `check` trước khi học

## Ví dụ

### Một thẻ

```input
## 3 | troubleshoot | containers | mid
Q: A pod is OOMKilled (exit code 137), but the node still has 50% free RAM. Why?
A: The container went over its own **cgroup memory limit**. The kernel OOM killer sends SIGKILL.
X: 137 = 128 + 9 (SIGKILL). Free RAM on the node does not matter.
S: Kubernetes docs: Resource Management for Pods and Containers
```

```output
Mặt trước: câu Q
Mặt sau: A (phần bạn tự chấm), X chữ xám nhỏ hơn, S chữ nhỏ nhất
Tag: containers troubleshoot mid
```

## Lưu ý

- Thẻ viết bằng tiếng Anh đơn giản. Mỗi thẻ chỉ một ý, trả lời trong 5 đến 15 giây
- Phần A tối đa khoảng 25 từ, phần X tối đa 3 dòng
- Tag cố định: type (troubleshoot, mechanism, tradeoff, cli, compare, number, outline), domain (8 cái) và level (foundation, mid, senior)
- Source chỉ ghi tên tài liệu để tra, không có link
- Câu hỏi phỏng vấn mở không vào Anki. Chúng được lưu ở `~/Documents/anki-tech/interview-questions.md` để luyện nói
- Lọc ôn trước phỏng vấn: tạo Filtered Deck, ví dụ `deck:tech::devops tag:troubleshoot`

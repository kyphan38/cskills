---
summary: Xử lý báo cáo upkeep hằng tháng: quy tắc chung, nâng cấp thư viện, tiền AI
family: upkeep
order: 1
---

## Dùng khi

Ngày 1 mỗi tháng có issue "Upkeep" trên GitHub và thông báo tiền AI trên Mac, có PR Dependabot mới, hoặc bạn muốn tự kiểm tra

## Lệnh

- `/upkeep` - Đọc cả 3 báo cáo, đưa kế hoạch, làm sau khi bạn đồng ý
- `/upkeep deps` - Chỉ nâng cấp thư viện
- `/upkeep costs` - Chỉ xem tiền AI và bảng giá
- `/upkeep lint` - Chỉ sửa lỗi quy tắc chung

## Các bước

1. Đọc issue Upkeep mới nhất, báo cáo tiền AI và các PR Dependabot; báo cáo cũ hơn 1 tuần thì chạy lại
2. Viết kế hoạch theo từng app, hỏi bạn chọn dòng nào làm
3. Làm từng app: sửa, chạy test, commit
4. Chỉ push và deploy khi bạn bảo
5. Chạy lại check, báo cái đã xong, cái bỏ qua, cái chờ bạn quyết

## Ví dụ

### Nâng cấp thư viện

```input
/upkeep deps
```

```output
fina: 3 bản vá, 4 bản nhỏ - cập nhật, test qua, đã commit
cogi/web: firebase-admin 14 vẫn giữ lại (lỗi đăng nhập trên Vercel)
Bản lớn chờ bạn quyết: firebase 13, eslint 10, @google/genai 3
```

## Lưu ý

- Quy tắc chung và thư viện chạy trên GitHub Actions, tiền AI chạy trên Mac, đều lúc 10:30 ngày 1
- Các check chỉ đọc, không sửa gì; PR Dependabot chỉ merge khi CI xanh
- Bản nâng cấp lớn luôn hỏi bạn trước
- Nếu test hỏng sau khi cập nhật thì trả lại bản cũ, không ép

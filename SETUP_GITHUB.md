# 🚀 HƯỚNG DẪN SETUP GITHUB ACTIONS

## BƯỚC 1: Tạo Repository trên GitHub

1. Vào https://github.com/new
2. Đặt tên: `cambridge-dictionary` (hoặc tên khác)
3. Chọn **Public** hoặc **Private**
4. **KHÔNG** tick "Add a README"
5. Click "Create repository"

---

## BƯỚC 2: Push Code lên GitHub

Mở Terminal/CMD trong thư mục này và chạy:

```bash
# Khởi tạo git
git init

# Add tất cả file
git add .

# Commit
git commit -m "Initial commit - Cambridge Dictionary App"

# Add remote (THAY <USERNAME> bằng username GitHub của bạn)
git remote add origin https://github.com/<USERNAME>/cambridge-dictionary.git

# Push lên GitHub
git branch -M main
git push -u origin main
```

---

## BƯỚC 3: Đợi GitHub Actions Build

1. Vào repository trên GitHub
2. Click tab **Actions**
3. Thấy workflow đang chạy (màu vàng)
4. Đợi 5-10 phút
5. Khi xong (màu xanh ✅):
   - Click vào workflow
   - Kéo xuống phần **Artifacts**
   - Download:
     - `Cambridge-Dictionary-Windows` → File .exe
     - `Cambridge-Dictionary-macOS-APP` → File .app
     - `Cambridge-Dictionary-macOS-DMG` → File .dmg

---

## BƯỚC 4: Chia sẻ

### Cho Windows:
- Gửi file `.exe`

### Cho Mac:
- Gửi file `.dmg` hoặc `.app`
- File `.dmg` dễ cài hơn (kéo thả vào Applications)

---

## ⚡ MẸO HAY:

### Tự động build mỗi khi cập nhật:
```bash
# Sau khi sửa code:
git add .
git commit -m "Update features"
git push

# GitHub Actions tự động build lại!
```

### Tạo Release:
1. Vào GitHub → Releases → "Create a new release"
2. Tag version: `v1.0.0`
3. Upload file .exe và .dmg
4. Publish release
5. Bạn bè download từ Releases!

---

## 🔧 NẾU GẶP LỖI:

### Lỗi: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/<USERNAME>/cambridge-dictionary.git
```

### Lỗi: "Permission denied"
```bash
# Dùng SSH thay vì HTTPS
git remote set-url origin git@github.com:<USERNAME>/cambridge-dictionary.git
```

### GitHub Actions fail:
- Check tab Actions → Click vào job màu đỏ
- Đọc log lỗi
- Fix và push lại

---

**DONE! GitHub sẽ tự động build cho cả Windows và Mac! 🎉**


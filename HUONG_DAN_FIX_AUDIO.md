# 🔧 HƯỚNG DẪN FIX AUDIO - DOWNGRADE PYTHON 3.14 → 3.12

## ⚠️ VẤN ĐỀ
- Python 3.14 quá mới → pygame KHÔNG tương thích
- Audio Cambridge KHÔNG phát được trong app
- Cần downgrade xuống Python 3.12 hoặc 3.11

## ✅ GIẢI PHÁP (WINDOWS)

### Bước 1: Download Python 3.12
1. Vào: https://www.python.org/downloads/
2. Download **Python 3.12.8** (phiên bản ổn định nhất)
3. **QUAN TRỌNG**: Chọn "Add Python 3.12 to PATH" khi cài

### Bước 2: Cài Python 3.12
1. Chạy file installer vừa download
2. Chọn **"Custom Installation"**
3. Tick tất cả options
4. Chọn **"Install for all users"**
5. Chọn **"Add Python to environment variables"**

### Bước 3: Verify Python version
```bash
python --version
# Phải hiện: Python 3.12.8
```

### Bước 4: Install lại tất cả packages
```bash
cd "D:\Luyencode\dịch"
pip install -r requirements.txt
pip install pygame
```

### Bước 5: Test pygame
```bash
python -c "import pygame; print('Pygame OK:', pygame.version.ver)"
```

### Bước 6: Test app
```bash
python dictionary_gui.py
```

### Bước 7: Build lại app
```bash
python build_exe.py
```

## 🎯 KẾT QUẢ MỌI KHOÁI

- ✅ Audio Cambridge phát TRỰC TIẾP trong app
- ✅ NHANH như ban đầu
- ✅ KHÔNG mở external player
- ✅ 100% hoạt động trong app

## 📝 LƯU Ý

- Nếu máy có nhiều Python version, dùng `py -3.12` thay vì `python`
- Xóa folder `build/` và `dist/` trước khi build lại
- Pygame cần Python 3.8 → 3.12 (KHÔNG hỗ trợ 3.13+)

## 🆘 NẾU GẶP LỖI

1. **Lỗi "python not found"**:
   - Thêm Python 3.12 vào PATH: `C:\Python312` và `C:\Python312\Scripts`

2. **Lỗi "pygame install failed"**:
   ```bash
   pip install pygame --upgrade
   ```

3. **Lỗi "multiple Python versions"**:
   ```bash
   py -3.12 -m pip install pygame
   py -3.12 dictionary_gui.py
   ```

## 💡 BONUS: Check Python versions
```bash
py --list
# Hiển thị tất cả Python versions trên máy
```

## ⚡ QUICK FIX (Tạm thời)
Nếu KHÔNG muốn downgrade Python, dùng code hiện tại với PowerShell audio player.
Nhưng sẽ CHẬM hơn và MỞ external player.

## 🎉 SAU KHI FIX
App sẽ hoạt động HOÀN HẢO như ban đầu:
- Audio phát NGAY trong app
- Không có delay
- Không mở browser/player
- 100% Cambridge audio gốc


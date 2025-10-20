# 📚 Cambridge Dictionary - English-Vietnamese

Ứng dụng từ điển Anh-Việt với giao diện đẹp, tích hợp Cambridge Dictionary API, autocomplete thông minh và export Quizlet.

![Version](https://img.shields.io/badge/version-7.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## ✨ Tính năng

- 🔍 **Tra từ từ Cambridge Dictionary**
- 🎯 **Autocomplete thông minh** - 4795+ từ phổ biến
- 🔊 **Phát âm UK/US** - Audio từ Cambridge
- 🤖 **AI Dịch tiếng Việt** - Gemini 2.0 Flash, dịch theo ngữ cảnh
- 📚 **Ghi nhớ từ vựng** - Lưu và quản lý từ đã học
- 📥 **Export Excel** - Import trực tiếp vào Quizlet
- ⚡ **Cache thông minh** - Tra lần 2 cực nhanh (<0.1s)
- 🎨 **Giao diện giống Cambridge** - Màu sắc chuẩn, UX tốt

## 📸 Screenshots

```
CAT  •  mèo
UK 🔊 /kæt/  US 🔊 /kæt/
─────────────────────────
noun
1. a small animal...  │ 🇻🇳 một con vật nhỏ...
```

## 🚀 Cài đặt

### Windows
1. Download file `.exe` từ [Releases](../../releases)
2. Double-click để chạy
3. Không cần cài đặt gì thêm!

### macOS
1. Download file `.dmg` từ [Releases](../../releases)
2. Kéo app vào Applications
3. Double-click để chạy

### Linux / Chạy từ source
```bash
# Clone repo
git clone https://github.com/<USERNAME>/cambridge-dictionary.git
cd cambridge-dictionary

# Cài dependencies
pip install -r requirements.txt

# Chạy app
python dictionary_gui.py
```

## 💻 Development

### Requirements
- Python 3.7+
- Tkinter (thường có sẵn)
- Internet connection

### Setup
```bash
pip install -r requirements.txt
python dictionary_gui.py
```

### Build
```bash
# Windows
python build_exe.py

# macOS/Linux
pyinstaller --name="Cambridge Dictionary" \
            --onefile \
            --windowed \
            --add-data="common_words.txt:." \
            dictionary_gui.py
```

## 📖 Cách sử dụng

1. **Tra từ**: Nhập từ tiếng Anh → Enter
2. **Autocomplete**: Gõ 2-3 ký tự → Chọn từ gợi ý
3. **Phát âm**: Click icon 🔊 bên cạnh phiên âm
4. **Ghi nhớ**: Click "📚 Ghi nhớ" để lưu từ
5. **Export**: "📖 Xem từ vựng" → "📥 Export Excel"
6. **Import Quizlet**: Upload file Excel vào Quizlet.com

## 🏗️ Công nghệ

- **GUI**: Tkinter
- **Web scraping**: BeautifulSoup4 + lxml
- **Translation**: AI (Gemini 2.0 Flash) + Google Translate API (deep-translator)
- **TTS**: pyttsx3 (fallback) + Cambridge audio
- **Audio**: pygame
- **Excel**: openpyxl
- **Build**: PyInstaller

## 📊 Performance

| Thao tác | Lần đầu | Lần 2+ (cache) |
|----------|---------|----------------|
| Tra từ | ~1.2s | ~0.05s ⚡ |
| Autocomplete | <1ms | <1ms |
| Dịch nghĩa | ~0.5s | ~0.01s |

## 🤝 Đóng góp

Pull requests are welcome! Nếu có ý tưởng cải thiện:

1. Fork repo
2. Tạo branch: `git checkout -b feature/amazing-feature`
3. Commit: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Tạo Pull Request

## 📝 License

MIT License - Tự do sử dụng cho mục đích cá nhân và thương mại.

## 🙏 Credits

- **Dictionary API**: Cambridge Dictionary
- **Translation**: AI (Gemini 2.0 Flash) + Google Translate (fallback)
- **Inspiration**: Cambridge Dictionary website

## ☕ Hỗ trợ phát triển

Ứng dụng này sử dụng **AI Gemini 2.0 Flash** để cung cấp bản dịch tiếng Việt chất lượng cao và theo ngữ cảnh. Nếu bạn thấy ứng dụng hữu ích và muốn ủng hộ tác giả, bạn có thể "mua một ly cà phê" qua thông tin sau:

**💳 Thông tin chuyển khoản:**
- **Ngân hàng**: MB Bank (Military Bank)
- **Số tài khoản**: `0396202885`
- **Chủ tài khoản**: **Nguyễn Ngọc Thoại**

![Mã QR Donate](donate_qr.png)

*Quét mã QR để chuyển khoản nhanh chóng*

## 📧 Liên hệ

Nếu có vấn đề hoặc câu hỏi, tạo [Issue](../../issues) trên GitHub.

---

**⭐ Nếu thấy hữu ích, hãy star repo này nhé! ⭐**

*Made with ❤️ for English learners*


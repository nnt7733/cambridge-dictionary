# 📚 Cambridge Dictionary - English-Vietnamese

Ứng dụng từ điển Anh-Việt với AI translation, giao diện đẹp và tính năng học từ vựng.

![Version](https://img.shields.io/badge/version-7.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## ✨ Tính năng

- 🔍 **Tra từ Cambridge Dictionary** - Định nghĩa chính xác, IPA UK/US
- 🤖 **AI Translation** - Gemini 2.0 Flash dịch theo ngữ cảnh
- 🔊 **Phát âm thật** - Audio từ Cambridge Dictionary
- 🎯 **Autocomplete** - 4795+ từ phổ biến
- 📚 **Quản lý từ vựng** - Lưu, xem, export Excel cho Quizlet
- ⚡ **Cache thông minh** - Tra lần 2 cực nhanh (<0.1s)

## 🚀 Cài đặt

### Windows (Khuyến nghị)
1. Download `EnglishVietnameseDictionary.exe` từ [Releases](../../releases)
2. Double-click chạy ngay - không cần cài đặt!

### Từ source code
```bash
git clone https://github.com/nnt7733/cambridge-dictionary.git
cd cambridge-dictionary
pip install -r requirements.txt
python dictionary_gui.py
```

## 📖 Cách sử dụng

1. **Tra từ**: Nhập từ tiếng Anh → Enter
2. **AI dịch**: Nhập ngữ cảnh → Click "AI dịch theo ngữ cảnh"
3. **Ghi nhớ**: Click "📚 Ghi nhớ" để lưu từ
4. **Export**: "📖 Xem từ vựng" → "📥 Export Excel" → Import vào Quizlet

## 🏗️ Công nghệ

- **GUI**: Tkinter
- **AI Translation**: Gemini 2.0 Flash
- **Web scraping**: BeautifulSoup4 + requests
- **Audio**: Cambridge Dictionary + pygame
- **Build**: PyInstaller

## 📊 Performance

| Thao tác | Lần đầu | Cache |
|----------|---------|-------|
| Tra từ | ~1.2s | ~0.05s ⚡ |
| AI dịch | ~2s | ~0.1s |
| Autocomplete | <1ms | <1ms |

## ☕ Hỗ trợ phát triển

Ứng dụng sử dụng **AI Gemini 2.0 Flash** miễn phí. Nếu thấy hữu ích, ủng hộ tác giả:

**💳 MB Bank: `0396202885` - Nguyễn Ngọc Thoại**

![Mã QR Donate](donate_qr.png)

## 📧 Liên hệ

- **Issues**: [GitHub Issues](../../issues)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **License**: [MIT License](LICENSE)

---

**⭐ Star repo nếu thấy hữu ích! ⭐**

*Made with ❤️ for English learners*
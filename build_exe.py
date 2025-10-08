"""
Script để build Dictionary GUI thành file .exe
Chạy: python build_exe.py
"""
import PyInstaller.__main__
import os

# Thư mục hiện tại
current_dir = os.path.dirname(os.path.abspath(__file__))

# Các tùy chọn cho PyInstaller
PyInstaller.__main__.run([
    'dictionary_gui.py',                    # File chính
    '--name=EnglishVietnameseDictionary',   # Tên file .exe
    '--onefile',                             # Đóng gói thành 1 file duy nhất
    '--windowed',                            # Không hiển thị console (GUI app)
    '--icon=NONE',                           # Không có icon (có thể thêm sau)
    '--clean',                               # Xóa cache cũ
    '--noconfirm',                           # Không hỏi xác nhận
    # Thêm file common_words.txt vào .exe
    '--add-data=common_words.txt;.',        # Bundle file txt
    # Thêm các file ẩn của pyttsx3 và comtypes
    '--hidden-import=pyttsx3.drivers',
    '--hidden-import=pyttsx3.drivers.sapi5',
    '--hidden-import=comtypes.client',
    '--hidden-import=comtypes.stream',
    '--hidden-import=win32com',
    '--hidden-import=win32com.client',
])

print("\n" + "="*70)
print("✅ BUILD HOÀN TẤT!")
print("="*70)
print(f"\n📁 File .exe được tạo tại: {current_dir}\\dist\\EnglishVietnameseDictionary.exe")
print("\nBạn có thể copy file .exe này đi bất cứ đâu và chạy mà không cần cài Python!")
print("="*70)


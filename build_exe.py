"""
Build Cambridge Dictionary GUI to .exe
Usage: python build_exe.py
"""
import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'dictionary_gui.py',
    '--name=EnglishVietnameseDictionary',
    '--onefile',
    '--windowed',
    '--clean',
    '--noconfirm',
    '--add-data=common_words.txt;.',
    '--hidden-import=pyttsx3.drivers',
    '--hidden-import=pyttsx3.drivers.sapi5',
    '--hidden-import=comtypes.client',
    '--hidden-import=comtypes.stream',
    '--hidden-import=win32com',
    '--hidden-import=win32com.client',
])

print(f"\n✅ Build completed: {os.path.dirname(os.path.abspath(__file__))}\\dist\\EnglishVietnameseDictionary.exe")
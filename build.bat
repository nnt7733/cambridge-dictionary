@echo off
chcp 65001 >nul
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║        BUILD DICTIONARY APP THÀNH FILE .EXE                   ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo 🔨 Đang build app...
echo.

python build_exe.py

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                    HOÀN TẤT!                                  ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo 📁 File .exe được tạo tại: dist\EnglishVietnameseDictionary.exe
echo.
echo Bạn có thể:
echo   1. Chạy file .exe trực tiếp
echo   2. Copy file .exe đi bất cứ đâu
echo   3. Chia sẻ cho bạn bè mà không cần cài Python!
echo.
pause


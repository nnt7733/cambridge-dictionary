@echo off
chcp 65001 >nul
echo ================================
echo 🔍 CHECKING PYTHON VERSIONS
echo ================================
echo.

echo Current Python:
python --version
echo.

echo All Python versions on system:
py --list
echo.

echo ================================
echo 📝 INSTRUCTIONS
echo ================================
echo.
echo ✅ Bạn CẦN Python 3.12 để pygame hoạt động!
echo ❌ Python 3.14 KHÔNG tương thích với pygame
echo.
echo 📥 Download Python 3.12.8:
echo https://www.python.org/downloads/release/python-3128/
echo.
echo Sau khi cài Python 3.12, chạy:
echo   py -3.12 -m pip install -r requirements.txt
echo   py -3.12 -m pip install pygame
echo   py -3.12 dictionary_gui.py
echo.
pause


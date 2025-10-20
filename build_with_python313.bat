@echo off
chcp 65001 >nul
echo ================================
echo 🚀 BUILDING WITH PYTHON 3.13
echo ================================
echo.

echo Installing requirements with Python 3.13...
py -3.13 -m pip install -r requirements.txt
py -3.13 -m pip install pygame pyinstaller
echo.

echo Building app...
py -3.13 build_exe.py
echo.

echo ================================
echo ✅ BUILD COMPLETE!
echo ================================
echo.
echo App location: dist\EnglishVietnameseDictionary.exe
echo.
pause


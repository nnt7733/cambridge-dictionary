@echo off
chcp 65001 >nul
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║              BUILD CAMBRIDGE DICTIONARY APP                   ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

python build_exe.py

echo.
echo ✅ Build completed: dist\EnglishVietnameseDictionary.exe
echo.
pause
@echo off
chcp 65001 >nul
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║           PUSH CODE LÊN GITHUB - TỰ ĐỘNG BUILD               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo 📝 Trước khi chạy, hãy đảm bảo:
echo    1. Đã tạo repository trên GitHub
echo    2. Biết URL repository (https://github.com/USERNAME/REPO.git)
echo.
pause
echo.

set /p REPO_URL="Nhập URL repository GitHub (vd: https://github.com/user/repo.git): "

echo.
echo 🔧 Đang setup Git...
git init

echo.
echo ➕ Đang add files...
git add .

echo.
echo 💾 Đang commit...
git commit -m "Initial commit - Cambridge Dictionary App with 4795 words autocomplete"

echo.
echo 🌐 Đang thêm remote...
git remote add origin %REPO_URL%

echo.
echo 🚀 Đang push lên GitHub...
git branch -M main
git push -u origin main

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                    ✅ HOÀN TẤT!                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo 📍 Tiếp theo:
echo    1. Vào repository GitHub
echo    2. Click tab "Actions"
echo    3. Đợi build xong (5-10 phút)
echo    4. Download file .exe và .app từ Artifacts
echo.
echo 🎉 Sau đó bạn có:
echo    • File .exe cho Windows
echo    • File .app + .dmg cho Mac
echo.
pause


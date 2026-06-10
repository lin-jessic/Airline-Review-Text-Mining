@echo off
chcp 65001 >nul
cd /d "%~dp0學姊"
echo 伺服器啟動中：http://localhost:8000/dashboard_2/index.html
echo 按 Ctrl+C 停止伺服器
echo.
timeout /t 1 /nobreak >nul
start "" "http://localhost:8000/dashboard_2/index.html"
python -m http.server 8000
pause

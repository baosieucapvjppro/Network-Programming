@echo off
echo ====================================
echo    CHAT CLIENT - Giao dien CLI
echo ====================================
echo.
set /p HOST="Nhap dia chi server (mac dinh: 127.0.0.1): "
if "%HOST%"=="" set HOST=127.0.0.1
set /p PORT="Nhap port (mac dinh: 60000): "
if "%PORT%"=="" set PORT=60000
python client.py %HOST% %PORT%
pause

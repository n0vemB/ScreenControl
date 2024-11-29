@echo off
chcp 65001 >nul

echo.
echo Testing connection...
ping -n 1 127.0.0.1 >nul
if errorlevel 1 (
    echo Network error!
    pause
    exit
)

echo Your IP Address:
ipconfig | find "IPv4"
echo.
echo Use port 8080 to access
echo Example: http://192.168.2.195:8080
echo.
echo Starting server...

python server.py

pause 
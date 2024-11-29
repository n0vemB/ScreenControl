@echo off
echo Stopping server...

:: 关闭 Python 进程
taskkill /F /IM python.exe

:: 关闭占用 8080 端口的进程
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8080" ^| find "LISTENING"') do (
    taskkill /F /PID %%a
)

:: 关闭 Chrome
taskkill /F /IM chrome.exe /T

echo Server stopped.
pause
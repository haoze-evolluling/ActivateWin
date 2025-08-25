@echo off
title Windows KMS激活管理器
echo 正在启动Windows KMS激活管理器...
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo 需要管理员权限，正在请求提升...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: 运行主程序
cd /d "%~dp0"
python main.py
pause
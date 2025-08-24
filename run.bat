@echo off
title Windows KMS激活管理器
chcp 65001 >nul
echo.
echo ========================================
echo    Windows KMS激活管理器 - 企业版
echo ========================================
echo.
echo 正在启动程序...
echo.

:: 检查是否以管理员身份运行
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 需要管理员权限，正在请求提升...
    echo.
    powershell -Command "Start-Process python -ArgumentList 'kms_activator.py --admin' -Verb RunAs"
    goto :eof
)

:: 运行主程序
python kms_activator.py --admin

pause
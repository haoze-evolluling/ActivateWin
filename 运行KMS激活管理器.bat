@echo off
title KMS激活管理器启动器
echo.
echo 正在启动 KMS激活管理器...
echo 如果程序需要管理员权限，请允许UAC提示
echo.
pause

start "" "dist\KMS激活管理器.exe"

echo.
echo 程序已启动！
echo 按任意键关闭此窗口...
pause >nul
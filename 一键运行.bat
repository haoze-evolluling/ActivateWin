@echo off
color 0a
title KMS激活管理器 v1.0
mode con cols=60 lines=15

echo.
echo    ╭─────────────────────────────────╮
echo    │        KMS激活管理器 v1.0        │
echo    │                                 │
echo    │    正在启动激活程序...          │
echo    │                                 │
echo    │    请稍候...                    │
echo    ╰─────────────────────────────────╯
echo.

if exist "dist\KMS激活管理器.exe" (
    timeout /t 2 >nul
    start "" "dist\KMS激活管理器.exe"
    exit
) else (
    echo 错误：未找到程序文件！
    echo.
    echo 请确保程序已正确安装。
    pause
)
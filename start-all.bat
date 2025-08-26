@echo off
title ActivateWin 完整服务启动器
color 0A

echo.
echo ╔═══════════════════════════════════════╗
echo ║        ActivateWin 服务启动器         ║
echo ╚═══════════════════════════════════════╝
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 警告: 未以管理员权限运行，某些功能可能受限
    echo 建议右键以管理员身份运行此脚本
    echo.
)

:: 设置窗口标题和颜色
set "ROOT_DIR=%~dp0"
set "BACKEND_DIR=%ROOT_DIR%backend"
set "WEB_DIR=%ROOT_DIR%webui"

:: 检查后端目录
cd /d "%BACKEND_DIR%"
if not exist "run.py" (
    echo 错误: 后端文件缺失，请重新安装
    pause
    exit /b 1
)

echo [1/3] 启动后端服务...
start "ActivateWin 后端服务" cmd /k "title ActivateWin Backend && cd /d "%BACKEND_DIR%" && python run.py --host 0.0.0.0 --port 5000"

echo [2/3] 等待后端服务启动...
timeout /t 2 /nobreak >nul

echo [3/3] 启动前端服务...
cd /d "%WEB_DIR%"
start "ActivateWin 前端服务" cmd /k "title ActivateWin Frontend && cd /d "%WEB_DIR%" && python -m http.server 8000"

echo.
echo ╔═══════════════════════════════════════╗
echo ║              启动完成!                ║
echo ╠═══════════════════════════════════════╣
echo ║  服务状态:                           ║
echo ║  • 后端: http://localhost:5000       ║
echo ║  • 前端: http://localhost:8000       ║
echo ║                                      ║
echo ║  打开浏览器访问:                     ║
echo ║  http://localhost:8000               ║
echo ╚═══════════════════════════════════════╝
echo.
echo 按任意键退出此窗口（不会停止服务）...
pause >nul
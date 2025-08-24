@echo off
cd /d %~dp0
echo 正在启动Windows KMS激活管理器...
echo 需要管理员权限，请确认UAC提示

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未检测到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 运行程序
python kms_activator.py
pause
@echo off
echo 正在启动NiceGUI KMS激活管理器...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未检测到Python环境，请先安装Python 3.7或更高版本
    pause
    exit /b 1
)

REM 检查依赖是否安装
python -c "import nicegui" >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装依赖包...
    pip install -r requirements.txt
)

echo 启动应用中...
cd nicegui_frontend
python main.py

pause
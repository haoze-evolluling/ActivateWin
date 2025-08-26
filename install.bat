@echo off
title ActivateWin 安装程序
color 0A

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 请以管理员身份运行此安装程序
    echo 右键点击 install.bat 选择"以管理员身份运行"
    pause
    exit /b 1
)

echo.
echo ╔═══════════════════════════════════════╗
echo ║        ActivateWin 安装程序           ║
echo ╚═══════════════════════════════════════╝
echo.

:: 设置变量
set "ROOT_DIR=%~dp0"
set "BACKEND_DIR=%ROOT_DIR%backend"
set "WEB_DIR=%ROOT_DIR%webui"

:: 检查Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo 错误: 未检测到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] 检查Python环境...
python --version
echo.

echo [2/4] 安装Python依赖...
cd /d "%BACKEND_DIR%"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %errorLevel% neq 0 (
    echo 错误: 依赖安装失败
    pause
    exit /b 1
)
echo.

echo [3/4] 创建启动脚本...
:: 创建后端启动脚本
echo @echo off > "%ROOT_DIR%start-backend.bat"
echo title ActivateWin 后端服务 >> "%ROOT_DIR%start-backend.bat"
echo cd /d "%BACKEND_DIR%" >> "%ROOT_DIR%start-backend.bat"
echo python run.py --host 0.0.0.0 --port 5000 >> "%ROOT_DIR%start-backend.bat"
echo pause >> "%ROOT_DIR%start-backend.bat"

:: 创建前端启动脚本
echo @echo off > "%ROOT_DIR%start-frontend.bat"
echo title ActivateWin 前端服务 >> "%ROOT_DIR%start-frontend.bat"
echo cd /d "%WEB_DIR%" >> "%ROOT_DIR%start-frontend.bat"
echo python -m http.server 8000 >> "%ROOT_DIR%start-frontend.bat"
echo pause >> "%ROOT_DIR%start-frontend.bat"

:: 创建一键启动脚本
echo @echo off > "%ROOT_DIR%start-all.bat"
echo title ActivateWin 完整服务 >> "%ROOT_DIR%start-all.bat"
echo start "后端服务" cmd /k "cd /d "%BACKEND_DIR%" && python run.py --host 0.0.0.0 --port 5000" >> "%ROOT_DIR%start-all.bat"
echo timeout /t 3 /nobreak ^>nul >> "%ROOT_DIR%start-all.bat"
echo start "前端服务" cmd /k "cd /d "%WEB_DIR%" && python -m http.server 8000" >> "%ROOT_DIR%start-all.bat"
echo echo. >> "%ROOT_DIR%start-all.bat"
echo echo 服务启动完成！ >> "%ROOT_DIR%start-all.bat"
echo echo 打开浏览器访问: http://localhost:8000 >> "%ROOT_DIR%start-all.bat"
echo pause >> "%ROOT_DIR%start-all.bat"

echo.
echo [4/4] 创建桌面快捷方式...
:: 创建桌面快捷方式脚本
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\create-shortcut.vbs"
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\ActivateWin.lnk" >> "%TEMP%\create-shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\create-shortcut.vbs"
echo oLink.TargetPath = "%ROOT_DIR%start-all.bat" >> "%TEMP%\create-shortcut.vbs"
echo oLink.WorkingDirectory = "%ROOT_DIR%" >> "%TEMP%\create-shortcut.vbs"
echo oLink.IconLocation = "%ROOT_DIR%pic\icon.ico" >> "%TEMP%\create-shortcut.vbs"
echo oLink.Description = "ActivateWin Windows激活工具" >> "%TEMP%\create-shortcut.vbs"
echo oLink.Save >> "%TEMP%\create-shortcut.vbs"
cscript "%TEMP%\create-shortcut.vbs" >nul 2>&1
del "%TEMP%\create-shortcut.vbs"

echo.
echo ╔═══════════════════════════════════════╗
echo ║              安装完成!                ║
echo ╠═══════════════════════════════════════╣
echo ║  启动方式:                           ║
echo ║  1. 双击 start-all.bat 一键启动       ║
echo ║  2. 桌面快捷方式 ActivateWin          ║
echo ║                                      ║
echo ║  访问地址: http://localhost:8000     ║
echo ╚═══════════════════════════════════════╝
echo.
pause
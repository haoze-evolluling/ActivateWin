#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版打包脚本 - 优化资源打包和兼容性
"""

import os
import sys
import shutil
from pathlib import Path

def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已清理: {dir_name}")

def build_enhanced_exe():
    """构建增强版可执行文件"""
    
    # 清理旧构建
    clean_build_dirs()
    
    # 获取当前目录
    current_dir = Path(__file__).parent.absolute()
    
    # 主程序
    main_script = current_dir / "main.py"
    
    # 确保所有资源文件存在
    required_files = ["icon.ico", "icon.png", "image.png"]
    missing_files = []
    
    for file in required_files:
        file_path = current_dir / file
        if not file_path.exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"警告: 缺少以下文件: {', '.join(missing_files)}")
    
    # 构建PyInstaller命令
    cmd = [
        "pyinstaller",
        str(main_script),
        "--onefile",
        "--windowed",
        "--name=KMS激活管理器",
        "--icon=icon.ico",
        "--clean",
        "--noconfirm",
        "--add-data", "frontend;frontend",
        "--add-data", "backend;backend", 
        "--add-data", "models;models",
        "--add-data", "icon.ico;.",
        "--add-data", "icon.png;.",
        "--add-data", "image.png;.",
        "--hidden-import", "ttkthemes",
        "--hidden-import", "PIL",
        "--hidden-import", "PIL.Image",
        "--hidden-import", "PIL.ImageTk",
        "--hidden-import", "win32con",
        "--hidden-import", "win32api",
        "--collect-all", "ttkthemes",
        "--collect-all", "PIL",
    ]
    
    # 在Windows上使用分号作为分隔符
    if os.name == 'nt':
        for i, arg in enumerate(cmd):
            if arg == ';':
                cmd[i] = ';'
    
    print("=" * 50)
    print("开始构建KMS激活管理器...")
    print("=" * 50)
    
    try:
        # 执行打包命令
        import subprocess
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=current_dir)
        
        if result.returncode == 0:
            print("✅ 构建成功！")
            
            # 检查生成的文件
            exe_path = current_dir / "dist" / "KMS激活管理器.exe"
            if exe_path.exists():
                file_size = exe_path.stat().st_size
                print(f"📁 可执行文件: {exe_path}")
                print(f"📊 文件大小: {file_size / 1024 / 1024:.2f} MB")
                
                # 创建桌面快捷方式（可选）
                create_desktop_shortcut(exe_path)
                
            else:
                print("❌ 可执行文件未找到")
                
        else:
            print("❌ 构建失败!")
            print("错误输出:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ 构建过程中发生错误: {e}")
        return False
        
    return True

def create_desktop_shortcut(exe_path):
    """创建桌面快捷方式"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "KMS激活管理器.lnk")
        target = str(exe_path)
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = str(exe_path.parent)
        shortcut.IconLocation = target
        shortcut.save()
        
        print("📋 已创建桌面快捷方式")
        
    except ImportError:
        print("📋 需要安装winshell和pywin32来创建快捷方式")
        print("   pip install winshell")
    except Exception as e:
        print(f"📋 创建快捷方式失败: {e}")

if __name__ == "__main__":
    success = build_enhanced_exe()
    if success:
        print("\n" + "=" * 50)
        print("🎉 打包完成！")
        print("📂 可执行文件位于: dist/KMS激活管理器.exe")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ 打包失败，请检查错误信息")
        print("=" * 50)
        sys.exit(1)
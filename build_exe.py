#!/usr/bin/env python3
"""
Windows KMS 激活工具 - 打包脚本
用于将Python脚本打包成独立的exe可执行文件
"""

import os
import sys
import subprocess
import PyInstaller.__main__

def build_exe():
    """构建exe文件"""
    print("🚀 开始打包Windows KMS激活工具...")
    
    # 检查PyInstaller是否已安装
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ 未安装PyInstaller，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # PyInstaller配置
    PyInstaller.__main__.run([
        'kms_activator.py',           # 主程序文件
        '--onefile',                  # 打包成单个文件
        '--windowed',                 # 窗口程序（无控制台）
        '--name=Windows_KMS_Activator', # 输出文件名
        '--clean',                    # 清理临时文件
        '--noconfirm',                # 覆盖现有文件
        '--icon=NONE',                # 如果有图标可以指定
        '--add-data=README.md;.',     # 包含README文件
        '--version-file=NONE',        # 如果有版本文件可以指定
    ])
    
    print("\n🎉 打包完成！")
    print("📁 可执行文件位置: dist\\Windows_KMS_Activator.exe")
    print("\n💡 使用方法:")
    print("1. 进入 dist 目录")
    print("2. 右键点击 Windows_KMS_Activator.exe")
    print("3. 选择 '以管理员身份运行'")

if __name__ == "__main__":
    build_exe()
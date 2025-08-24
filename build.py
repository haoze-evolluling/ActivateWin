#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本
用于将KMS激活器打包成可执行文件
"""

import os
import sys
import subprocess

def build_executable():
    """打包可执行文件"""
    print("开始打包KMS激活器...")
    
    # 安装所需依赖
    print("检查依赖...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    # 确保PyInstaller已安装
    try:
        subprocess.run(["pyinstaller", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("安装PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # 使用PyInstaller打包
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--icon=icon.ico",
        "--add-data=icon.ico;.",
        "--add-data=icon.png;.",
        "--add-data=kmsserver.md;.",
        "--add-data=kmskey.md;.",
        "--name=KMSActivator",
        "kms_activator.py"
    ]
    
    print("执行打包命令...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ 打包成功！")
        print("可执行文件位于: dist/KMSActivator.exe")
    else:
        print("✗ 打包失败:")
        print(result.stderr)

if __name__ == "__main__":
    build_executable()
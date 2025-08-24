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
    # 安装所需依赖
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    # 确保PyInstaller已安装
    try:
        subprocess.run(["pyinstaller", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
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
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

if __name__ == "__main__":
    build_executable()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新的打包脚本 - 前后端分离架构
"""

import os
import sys
import PyInstaller.__main__
import shutil


def build_application():
    """构建应用程序"""
    print("开始构建前后端分离架构的KMS激活管理器...")
    
    # 清理之前的构建
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # PyInstaller参数
    args = [
        "main.py",  # 新的主程序入口
        "--name=KMSActivator",
        "--windowed",
        "--onefile",
        "--icon=icon.ico",
        "--add-data=icon.ico;.",
        "--add-data=icon.png;.",
        "--add-data=image.png;.",
        "--add-data=kmsserver.md;.",
        "--add-data=kmskey.md;.",
        "--hidden-import=frontend.ui_manager",
        "--hidden-import=backend.kms_service",
        "--hidden-import=models.activation_data",
        "--clean",
        "--noconfirm"
    ]
    
    # 执行打包
    PyInstaller.__main__.run(args)
    
    print("构建完成！")
    print("可执行文件位于: dist/KMSActivator.exe")


if __name__ == "__main__":
    build_application()
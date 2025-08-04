#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows KMS激活工具打包脚本
用于将Python程序打包成独立的exe文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """检查是否安装了pyinstaller"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """安装pyinstaller"""
    print("正在安装PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

def clean_build():
    """清理之前的构建文件"""
    print("清理之前的构建文件...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    files_to_clean = ["*.spec", "*.pyc", "*.pyo", "*.pyd"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已删除目录: {dir_name}")
    
    for pattern in files_to_clean:
        for file in Path(".").glob(pattern):
            file.unlink()
            print(f"已删除文件: {file}")

def build_exe():
    """构建exe文件"""
    print("开始构建exe文件...")
    
    # PyInstaller命令参数
    pyinstaller_cmd = [
        "pyinstaller",
        "--name=ActivateWin",
        "--onefile",
        "--windowed",
        "--icon=icon1.ico",
        "--add-data=icon1.ico;.",
        "--add-data=icon1.png;.",
        "--add-data=README.md;.",
        "--add-data=方法指导.md;.",
        "--add-data=ui.py;.",
        "--add-data=backend.py;.",
        "--clean",
        "--noconfirm",
        "--version-file=version_info.txt",
        "--distpath=dist",
        "--workpath=build",
        "--specpath=.",
        "kms_activator.py"
    ]
    
    # 运行PyInstaller
    result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("构建成功!")
        print(f"exe文件位置: {os.path.join('dist', 'ActivateWin.exe')}")
        return True
    else:
        print("构建失败!")
        print("错误信息:")
        print(result.stderr)
        return False

def create_version_info():
    """创建版本信息文件"""
    version_info = """
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x4,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'KMS Activator Team'),
        StringStruct(u'FileDescription', u'ActivateWin'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'ActivateWin'),
        StringStruct(u'LegalCopyright', u'Copyright (c) 2024 KMS Activator Team'),
        StringStruct(u'OriginalFilename', u'ActivateWin.exe'),
        StringStruct(u'ProductName', u'ActivateWin'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    
    with open("version_info.txt", "w", encoding="utf-8") as f:
        f.write(version_info)
    print("已创建版本信息文件")

def main():
    """主函数"""
    print("Windows KMS激活工具打包程序")
    print("=" * 50)
    
    # 检查Python版本
    if sys.version_info < (3, 6):
        print("错误: 需要Python 3.6或更高版本")
        return
    
    # 检查并安装PyInstaller
    if not check_pyinstaller():
        install_pyinstaller()
    
    # 清理之前的构建
    clean_build()
    
    # 创建版本信息
    create_version_info()
    
    # 构建exe
    if build_exe():
        print("\n构建完成!")
        print("你可以在这里找到exe文件: dist/Windows_KMS_Activator.exe")
        
        # 可选：创建压缩包
        create_zip = input("是否创建zip压缩包? (y/n): ").lower().strip()
        if create_zip == 'y':
            import zipfile
            zip_filename = f"ActivateWin_v1.0.0.zip"
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write("dist/ActivateWin.exe", "ActivateWin.exe")
                zipf.write("README.md", "README.md")
                zipf.write("方法指导.md", "方法指导.md")
            print(f"已创建压缩包: {zip_filename}")
    else:
        print("构建失败，请检查错误信息")

if __name__ == "__main__":
    main()
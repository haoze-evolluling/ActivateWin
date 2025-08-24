#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图标测试脚本
用于验证图标设置功能
"""

import tkinter as tk
import os
import sys

def test_icon_loading():
    """测试图标加载功能"""
    root = tk.Tk()
    root.title("图标测试")
    root.geometry("300x200")
    
    # 获取当前目录
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    icon_path = os.path.join(application_path, "icon.ico")
    png_path = os.path.join(application_path, "icon.png")
    
    print(f"当前目录: {application_path}")
    print(f"ICO图标路径: {icon_path}")
    print(f"PNG图标路径: {png_path}")
    print(f"ICO文件存在: {os.path.exists(icon_path)}")
    print(f"PNG文件存在: {os.path.exists(png_path)}")
    
    try:
        # 尝试加载ICO图标
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
            print("✓ ICO图标加载成功")
        else:
            print("✗ ICO图标文件不存在")
            
            # 尝试加载PNG图标
            if os.path.exists(png_path):
                try:
                    from PIL import Image, ImageTk
                    icon_image = Image.open(png_path)
                    icon_photo = ImageTk.PhotoImage(icon_image)
                    root.iconphoto(True, icon_photo)
                    print("✓ PNG图标加载成功")
                except ImportError:
                    print("✗ PIL库未安装，无法加载PNG图标")
                except Exception as e:
                    print(f"✗ PNG图标加载失败: {e}")
            else:
                print("✗ PNG图标文件也不存在")
                
    except Exception as e:
        print(f"✗ 图标加载失败: {e}")
    
    # 添加标签显示结果
    label = tk.Label(root, text="图标测试完成，查看控制台输出", pady=50)
    label.pack()
    
    root.mainloop()

if __name__ == "__main__":
    test_icon_loading()
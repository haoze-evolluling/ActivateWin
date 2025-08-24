#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KMS激活器调试版本 - 逐步执行以找出闪退原因
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import json
import os
import sys
import ctypes

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
    print("PIL库可用")
except ImportError:
    PIL_AVAILABLE = False
    print("PIL库不可用")

class KMSActivatorDebug:
    def __init__(self):
        print("正在初始化KMSActivatorDebug...")
        try:
            self.root = tk.Tk()
            print("根窗口创建成功")
            
            self.root.title("KMS Windows 激活工具")
            self.root.geometry("800x600")
            self.root.resizable(False, False)
            print("窗口配置完成")
            
            # 最小化调试步骤
            self.setup_minimal_ui()
            
        except Exception as e:
            print(f"初始化失败: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def setup_minimal_ui(self):
        """设置最小化UI以测试基本功能"""
        print("设置最小化UI...")
        try:
            # 简单的测试界面
            label = tk.Label(self.root, text="KMS激活器调试模式", font=("Arial", 16))
            label.pack(pady=20)
            
            test_btn = tk.Button(self.root, text="测试背景图片", command=self.test_background)
            test_btn.pack(pady=10)
            
            close_btn = tk.Button(self.root, text="关闭", command=self.root.quit)
            close_btn.pack(pady=10)
            
            print("最小化UI设置完成")
            
        except Exception as e:
            print(f"设置最小化UI失败: {e}")
            import traceback
            traceback.print_exc()
    
    def test_background(self):
        """测试背景图片功能"""
        print("测试背景图片...")
        try:
            if not PIL_AVAILABLE:
                messagebox.showwarning("警告", "PIL库不可用，无法加载背景图片")
                return
            
            # 获取当前脚本所在目录
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            image_path = os.path.join(application_path, "image.png")
            print(f"查找背景图片: {image_path}")
            
            if os.path.exists(image_path):
                print("背景图片存在，尝试加载...")
                
                original_image = Image.open(image_path)
                window_width = 800
                window_height = 600
                
                resized_image = original_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
                
                if resized_image.mode != 'RGBA':
                    resized_image = resized_image.convert('RGBA')
                
                alpha = resized_image.split()[-1]
                alpha = alpha.point(lambda p: int(p * 0.5))
                resized_image.putalpha(alpha)
                
                self.background_image = ImageTk.PhotoImage(resized_image)
                
                self.background_label = tk.Label(self.root, image=self.background_image)
                self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
                self.background_label.lower()
                
                print("背景图片加载成功")
                messagebox.showinfo("成功", "背景图片加载成功")
            else:
                print(f"背景图片不存在: {image_path}")
                messagebox.showwarning("警告", f"背景图片不存在: {image_path}")
                
        except Exception as e:
            print(f"背景图片测试失败: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("错误", f"背景图片加载失败: {e}")
    
    def run(self):
        """运行应用程序"""
        print("准备进入主循环...")
        self.root.mainloop()
        print("主循环结束")

if __name__ == "__main__":
    print("启动KMS激活器调试版本...")
    try:
        app = KMSActivatorDebug()
        app.run()
    except Exception as e:
        print(f"程序启动失败: {e}")
        import traceback
        traceback.print_exc()
        
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("启动失败", f"程序启动失败:\n{str(e)}")
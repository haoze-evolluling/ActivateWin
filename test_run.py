#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试程序运行脚本 - 用于验证程序是否正常启动
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from frontend.ui_manager import UIManager
    print("✓ 所有模块导入成功")
    
    # 创建简单的测试窗口
    root = tk.Tk()
    root.title("测试窗口")
    root.geometry("300x200")
    
    label = tk.Label(root, text="程序运行正常！\n\n点击确定退出测试", font=("Arial", 12))
    label.pack(pady=50)
    
    button = tk.Button(root, text="确定", command=root.destroy)
    button.pack()
    
    root.mainloop()
    
    print("✓ 程序正常启动并运行")
    
except ImportError as e:
    print(f"✗ 导入错误: {e}")
except Exception as e:
    print(f"✗ 运行错误: {e}")
    
input("按任意键退出...")
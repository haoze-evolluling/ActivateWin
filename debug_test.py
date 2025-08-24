#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试测试脚本 - 用于诊断KMS激活器的闪退问题
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

print("Python版本:", sys.version)
print("当前工作目录:", os.getcwd())
print("脚本路径:", __file__)

# 测试基本的tkinter功能
try:
    print("正在创建根窗口...")
    root = tk.Tk()
    root.title("调试测试")
    root.geometry("300x200")
    
    # 创建一个简单的标签
    label = tk.Label(root, text="测试窗口 - 如果看到这个，tkinter工作正常")
    label.pack(pady=50)
    
    print("窗口创建成功，准备进入主循环...")
    
    # 添加关闭按钮
    close_btn = tk.Button(root, text="关闭", command=root.quit)
    close_btn.pack()
    
    root.mainloop()
    print("主循环结束")
    
except Exception as e:
    print("错误:", str(e))
    print("错误类型:", type(e).__name__)
    import traceback
    traceback.print_exc()
    
    # 显示错误消息框
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("错误", f"发生错误:\n{str(e)}")

print("测试脚本结束")
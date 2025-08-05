import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import platform
import json
import os
import threading
import sys
from datetime import datetime
import ctypes

class ModernButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            font=("Microsoft YaHei", 11, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=25,
            pady=12
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, e):
        self.configure(bg=self["activebackground"])
    
    def on_leave(self, e):
        self.configure(bg=self["bg"])

class KMSActivatorUI:
    def __init__(self, parent, backend):
        self.parent = parent
        self.backend = backend
        self.setup_styles()
        self.create_gui()
        self.setup_icon()
        
    def setup_icon(self):
        """设置窗口图标"""
        try:
            self.parent.iconbitmap(default="icon1.ico")
        except Exception as e:
            print(f"无法设置窗口图标: {e}")
    
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 自定义样式
        style.configure('TLabel', background='#ffffff', font=('Microsoft YaHei', 10))
        style.configure('Header.TLabel', font=('Microsoft YaHei', 18, 'bold'))
        style.configure('SubHeader.TLabel', font=('Microsoft YaHei', 12))
        style.configure('TFrame', background='#ffffff')
        style.configure('TLabelframe', background='#ffffff')
        style.configure('TLabelframe.Label', font=('Microsoft YaHei', 11, 'bold'))
        
        # 自定义Combobox样式
        style.map('TCombobox',
                 fieldbackground=[('readonly', '#f8f9fa')],
                 selectbackground=[('readonly', '#e9ecef')],
                 selectforeground=[('readonly', '#212529')])
    
    def create_gui(self):
        """创建现代化GUI界面"""
        # 主框架
        main_frame = tk.Frame(self.parent, bg="#ffffff")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 标题区域
        title_frame = tk.Frame(main_frame, bg="#ffffff")
        title_frame.pack(fill="x", pady=(0, 30))
        
        title_label = tk.Label(title_frame, text="ActivateWin", 
                             font=("Microsoft YaHei", 24, "bold"), 
                             bg="#ffffff", fg="#2c3e50")
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="一键激活您的Windows系统", 
                                font=("Microsoft YaHei", 12), 
                                bg="#ffffff", fg="#7f8c8d")
        subtitle_label.pack()
        
        # 系统信息卡片
        info_card = tk.Frame(main_frame, bg="#f8f9fa", relief="raised", bd=1)
        info_card.pack(fill="x", pady=(0, 20))
        
        info_label = tk.Label(info_card, text=f"当前系统版本: {self.backend.get_current_os()}", 
                            font=("Microsoft YaHei", 12, "bold"), 
                            bg="#f8f9fa", fg="#495057", pady=15)
        info_label.pack()
        
        # 配置区域
        config_frame = tk.Frame(main_frame, bg="#ffffff")
        config_frame.pack(fill="x", pady=(0, 20))
        
        # 左侧：Windows版本选择
        left_frame = tk.Frame(config_frame, bg="#ffffff")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        version_label = tk.Label(left_frame, text="选择Windows版本", 
                               font=("Microsoft YaHei", 12, "bold"), 
                               bg="#ffffff", fg="#2c3e50")
        version_label.pack(anchor="w", pady=(0, 10))
        
        self.version_var = tk.StringVar()
        self.version_combo = ttk.Combobox(left_frame, textvariable=self.version_var, 
                                        values=self.backend.get_windows_versions(), 
                                        width=40, state="readonly", 
                                        font=("Microsoft YaHei", 10))
        self.version_combo.pack(fill="x")
        self.version_combo.set("请选择Windows版本")
        
        # 右侧：KMS服务器选择
        right_frame = tk.Frame(config_frame, bg="#ffffff")
        right_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        kms_label = tk.Label(right_frame, text="选择KMS服务器", 
                           font=("Microsoft YaHei", 12, "bold"), 
                           bg="#ffffff", fg="#2c3e50")
        kms_label.pack(anchor="w", pady=(0, 10))
        
        self.kms_var = tk.StringVar()
        self.kms_combo = ttk.Combobox(right_frame, textvariable=self.kms_var, 
                                    values=self.backend.get_kms_servers(), width=30, 
                                    state="readonly", font=("Microsoft YaHei", 10))
        self.kms_combo.pack(fill="x")
        self.kms_combo.set("kms.cgtsoft.com")
        
        # 按钮区域
        button_frame = tk.Frame(main_frame, bg="#ffffff")
        button_frame.pack(pady=(0, 20))
        
        # 激活按钮
        activate_btn = ModernButton(button_frame, text="🚀 开始激活", 
                                  command=self.on_activate_click,
                                  bg="#3498db", activebackground="#2980b9", 
                                  fg="white")
        activate_btn.pack(side="left", padx=10)
        
        # 验证按钮
        verify_btn = ModernButton(button_frame, text="✅ 验证激活", 
                                command=self.on_verify_click,
                                bg="#2ecc71", activebackground="#27ae60", 
                                fg="white")
        verify_btn.pack(side="left", padx=10)
        
        # 清除日志按钮
        clear_btn = ModernButton(button_frame, text="🧹 清除日志", 
                               command=self.clear_log,
                               bg="#95a5a6", activebackground="#7f8c8d", 
                               fg="white")
        clear_btn.pack(side="left", padx=10)
        
        # 日志区域
        log_frame = tk.Frame(main_frame, bg="#ffffff")
        log_frame.pack(fill="both", expand=True)
        
        log_header = tk.Frame(log_frame, bg="#ffffff")
        log_header.pack(fill="x", pady=(0, 10))
        
        log_title = tk.Label(log_header, text="操作日志", 
                           font=("Microsoft YaHei", 12, "bold"), 
                           bg="#ffffff", fg="#2c3e50")
        log_title.pack(side="left")
        
        # 日志文本框
        log_container = tk.Frame(log_frame, bg="#f8f9fa", relief="groove", bd=1)
        log_container.pack(fill="both", expand=True)
        
        self.log_text = tk.Text(log_container, height=12, width=70, 
                              font=("Consolas", 9), bg="#f8f9fa", 
                              fg="#495057", relief="flat",
                              padx=10, pady=10)
        scrollbar = ttk.Scrollbar(log_container, orient="vertical", 
                                command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 添加初始日志
        self.add_log("程序启动成功")
        self.add_log(f"检测到系统: {self.backend.get_current_os()}")
    
    def add_log(self, message):
        """添加日志消息"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.parent.update()
    
    def clear_log(self):
        """清除日志"""
        self.log_text.delete(1.0, tk.END)
        self.add_log("日志已清除")
    
    def on_activate_click(self):
        """激活按钮点击事件"""
        version = self.version_var.get()
        kms_server = self.kms_var.get()
        self.backend.handle_activation_request(version, kms_server, self.add_log)
    
    def on_verify_click(self):
        """验证按钮点击事件"""
        self.backend.handle_verify_request(self.add_log)
    
    def show_warning(self, title, message):
        """显示警告对话框"""
        messagebox.showwarning(title, message)
    
    def show_error(self, title, message):
        """显示错误对话框"""
        messagebox.showerror(title, message)
    
    def show_info(self, title, message):
        """显示信息对话框"""
        messagebox.showinfo(title, message)
    
    def ask_yes_no(self, title, message):
        """显示确认对话框"""
        return messagebox.askyesno(title, message)
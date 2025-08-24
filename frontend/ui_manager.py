#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户界面管理器
处理所有UI相关的逻辑，与业务逻辑分离
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from typing import Optional, Callable
from models.activation_data import ActivationConfig, ActivationData
from backend.kms_service import KMSService


try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None


class UIManager:
    """用户界面管理器"""
    
    def __init__(self):
        self.root = None
        self.data_manager = ActivationData()
        self.kms_service = KMSService()
        
        # UI变量
        self.version_var = None
        self.edition_var = None
        self.selected_server = None
        self.custom_server = None
        self.current_selection = {}
        
        # UI组件
        self.key_display = None
        self.server_status = None
        self.config_display = None
        self.edition_combo = None
        
    def create_main_window(self) -> tk.Tk:
        """创建主窗口"""
        self.root = tk.Tk()
        self.root.title("Windows KMS激活管理器 - 企业版")
        self.root.geometry("800x640")
        self.root.resizable(False, False)
        
        # 设置窗口图标
        self._set_window_icon()
        self._set_taskbar_icon()
        self._set_background_image()
        
        return self.root
    
    def setup_ui(self):
        """设置用户界面"""
        # 设置主题
        if not self._has_background_image():
            self.root.configure(bg='#f0f0f0')
        
        # 创建主容器框架
        main_container = tk.Frame(self.root, bg='')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # 标题区域
        self._create_title_area(main_container)
        
        # 主内容区域
        main_frame = tk.Frame(main_container, bg='')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 左侧：版本选择
        self._create_version_selection(main_frame)
        
        # 右侧：KMS服务器配置
        self._create_server_config(main_frame)
        
        # 底部：操作区域
        self._create_action_area(main_container)
        
    def _create_title_area(self, parent):
        """创建标题区域"""
        title_frame = tk.Frame(parent, bg='SystemButtonFace')
        title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        title_label = tk.Label(title_frame, text="Windows KMS激活管理器", 
                               font=("Microsoft YaHei", 18, "bold"),
                               fg='#2c3e50', bg='SystemButtonFace')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="基于微软官方授权的企业级激活管理工具", 
                                   font=("Microsoft YaHei", 11), fg="#7f8c8d", bg='SystemButtonFace')
        subtitle_label.pack()
    
    def _create_version_selection(self, parent):
        """创建版本选择区域"""
        left_frame = tk.Frame(parent, bg='SystemButtonFace')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 10), pady=15)
        
        # 使用更轻量的边框
        inner_frame = tk.Frame(left_frame, bg='white', relief='flat', bd=1)
        inner_frame.pack(fill=tk.BOTH, expand=True)
        
        # 添加标题
        title = tk.Label(inner_frame, text="版本选择", 
                        font=("Microsoft YaHei", 10, "bold"),
                        bg='white', fg='black')
        title.pack(fill=tk.X, pady=(5, 10), padx=10)
        
        # 一级选择：Windows版本
        tk.Label(inner_frame, text="选择Windows版本:", bg='white', fg='black').pack(anchor=tk.W, padx=10)
        
        self.version_var = tk.StringVar()
        version_combo = ttk.Combobox(inner_frame, textvariable=self.version_var,
                                   values=self.data_manager.get_all_windows_versions(),
                                   state="readonly", width=25)
        version_combo.pack(fill=tk.X, pady=5, padx=10)
        version_combo.bind("<<ComboboxSelected>>", self._on_version_selected)
        
        # 二级选择：具体版本号
        tk.Label(inner_frame, text="选择具体版本:", bg='white', fg='black').pack(anchor=tk.W, pady=(10, 0), padx=10)
        
        self.edition_var = tk.StringVar()
        self.edition_combo = ttk.Combobox(inner_frame, textvariable=self.edition_var,
                                        state="readonly", width=25)
        self.edition_combo.pack(fill=tk.X, pady=5, padx=10)
        self.edition_combo.bind("<<ComboboxSelected>>", self._on_edition_selected)
        
        # 显示选择的密钥
        tk.Label(inner_frame, text="对应产品密钥:", bg='white', fg='black').pack(anchor=tk.W, pady=(10, 0), padx=10)
        
        self.key_display = tk.Text(inner_frame, height=2, width=30, state="disabled", bg='white', fg='black')
        self.key_display.pack(fill=tk.X, pady=5, padx=10)
    
    def _create_server_config(self, parent):
        """创建服务器配置区域"""
        right_frame = tk.Frame(parent, bg='SystemButtonFace')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 20), pady=15)
        
        # 使用更轻量的边框
        inner_frame = tk.Frame(right_frame, bg='white', relief='flat', bd=1)
        inner_frame.pack(fill=tk.BOTH, expand=True)
        
        # 添加标题
        title = tk.Label(inner_frame, text="KMS服务器配置", 
                        font=("Microsoft YaHei", 10, "bold"),
                        bg='white', fg='black')
        title.pack(fill=tk.X, pady=(5, 10), padx=10)
        
        # 预设服务器选择
        tk.Label(inner_frame, text="选择预设KMS服务器:", bg='white', fg='black').pack(anchor=tk.W, padx=10)
        
        self.selected_server = tk.StringVar()
        self.server_combo = ttk.Combobox(inner_frame, textvariable=self.selected_server,
                                       values=self.data_manager.get_all_kms_servers(),
                                       state="readonly", width=35)
        self.server_combo.pack(fill=tk.X, pady=5, padx=10)
        
        # 或选择自定义服务器
        separator = ttk.Separator(inner_frame, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=10, padx=10)
        
        tk.Label(inner_frame, text="或输入自定义服务器:", bg='white', fg='black').pack(anchor=tk.W, padx=10)
        
        self.custom_server = tk.StringVar()
        custom_entry = ttk.Entry(inner_frame, textvariable=self.custom_server, width=35)
        custom_entry.pack(fill=tk.X, pady=5, padx=10)
        
        # 服务器状态显示
        tk.Label(inner_frame, text="服务器状态:", bg='white', fg='black').pack(anchor=tk.W, pady=(10, 0), padx=10)
        
        self.server_status = tk.Text(inner_frame, height=3, width=35, state="disabled", bg='white', fg='black')
        self.server_status.pack(fill=tk.X, pady=5, padx=10)
        
        # 测试连接按钮
        test_btn = ttk.Button(inner_frame, text="测试服务器连接", command=self._test_server_connection)
        test_btn.pack(pady=5, padx=10)
    
    def _create_action_area(self, parent):
        """创建操作区域"""
        bottom_frame = tk.Frame(parent, bg='SystemButtonFace')
        bottom_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
        
        # 当前配置显示
        config_frame = tk.Frame(bottom_frame, bg='white', relief='flat', bd=1)
        config_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # 添加标题
        title = tk.Label(config_frame, text="当前配置", 
                        font=("Microsoft YaHei", 10, "bold"),
                        bg='white', fg='black')
        title.pack(fill=tk.X, pady=(5, 10), padx=10)
        
        self.config_display = tk.Text(config_frame, height=4, state="disabled", bg='white', fg='black')
        self.config_display.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # 操作按钮
        button_frame = tk.Frame(bottom_frame, bg='SystemButtonFace')
        button_frame.pack(fill=tk.X, padx=10)
        
        ttk.Button(button_frame, text="开始激活", command=self._start_activation).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="清除配置", command=self._clear_config).pack(side=tk.RIGHT, padx=5)
    
    def _on_version_selected(self, event):
        """当选择Windows版本时"""
        version = self.version_var.get()
        editions = self.data_manager.get_editions(version)
        self.edition_combo["values"] = editions
        self.edition_combo.set("")
        self._update_config_display()
    
    def _on_edition_selected(self, event):
        """当选择具体版本时"""
        version = self.version_var.get()
        edition = self.edition_var.get()
        
        key = self.data_manager.get_product_key(version, edition)
        if key:
            self.current_selection = {
                "version": version,
                "edition": edition,
                "key": key
            }
            
            # 显示密钥
            self.key_display.config(state="normal")
            self.key_display.delete(1.0, tk.END)
            self.key_display.insert(1.0, key)
            self.key_display.config(state="disabled")
            
            self._update_config_display()
    
    def _test_server_connection(self):
        """测试服务器连接"""
        server = self.custom_server.get() or self.selected_server.get()
        if not server:
            messagebox.showwarning("警告", "请先选择或输入KMS服务器地址")
            return
        
        self._update_server_status(f"正在测试连接: {server}...", "normal")
        self.root.update()
        
        # 使用后端服务测试连接
        status = self.kms_service.test_server_connection(server)
        
        if status.is_available:
            message = f"✓ 服务器 {server} 连接正常"
            if status.response_time:
                message += f"\n平均响应时间: {status.response_time}ms"
            self._update_server_status(message, "available")
        else:
            message = f"✗ 服务器 {server} {status.error_message or '连接失败'}"
            self._update_server_status(message, "error")
    
    def _update_server_status(self, message: str, status_type: str):
        """更新服务器状态显示"""
        self.server_status.config(state="normal")
        self.server_status.delete(1.0, tk.END)
        self.server_status.insert(1.0, message)
        
        if status_type == "available":
            self.server_status.config(bg="#90EE90")  # 浅绿色
        elif status_type == "error":
            self.server_status.config(bg="#FFB6C1")  # 浅红色
        else:
            self.server_status.config(bg="SystemButtonFace")  # 系统默认背景色
            
        self.server_status.config(state="disabled")
    
    def _update_config_display(self):
        """更新配置显示"""
        self.config_display.config(state="normal")
        self.config_display.delete(1.0, tk.END)
        
        config_text = []
        
        if self.current_selection:
            config_text.append(f"Windows版本: {self.current_selection['version']}")
            config_text.append(f"具体版本: {self.current_selection['edition']}")
            config_text.append(f"产品密钥: {self.current_selection['key']}")
            
        server = self.custom_server.get() or self.selected_server.get()
        if server:
            config_text.append(f"KMS服务器: {server}")
            
        if config_text:
            self.config_display.insert(1.0, "\n".join(config_text))
            
        self.config_display.config(state="disabled")
    
    def _start_activation(self):
        """开始激活流程"""
        if not self.current_selection:
            messagebox.showerror("错误", "请先选择Windows版本和具体版本")
            return
            
        server = self.custom_server.get() or self.selected_server.get()
        if not server:
            messagebox.showerror("错误", "请先选择或输入KMS服务器地址")
            return
        
        # 创建激活配置
        config = ActivationConfig(
            windows_version=self.current_selection['version'],
            edition=self.current_selection['edition'],
            product_key=self.current_selection['key'],
            kms_server=server
        )
        
        # 确认激活
        message = f"确定要激活以下配置吗？\n\n"
        message += f"Windows版本: {config.windows_version}\n"
        message += f"具体版本: {config.edition}\n"
        message += f"产品密钥: {config.product_key}\n"
        message += f"KMS服务器: {config.kms_server}"
        
        if not messagebox.askyesno("确认激活", message):
            return
        
        # 执行激活
        self._execute_activation(config)
    
    def _execute_activation(self, config: ActivationConfig):
        """执行激活"""
        # 添加激活回调
        self.kms_service.add_activation_callback(self._activation_callback)
        
        # 执行激活
        success, message = self.kms_service.execute_activation(config)
        
        if success:
            messagebox.showinfo("成功", message)
        else:
            messagebox.showerror("激活失败", message)
    
    def _activation_callback(self, event_type: str, data: dict):
        """激活过程回调"""
        if event_type == "activation_start":
            print("开始激活...")
        elif event_type == "step_start":
            print(f"步骤 {data['step']}: {data['description']}")
        elif event_type == "step_complete":
            print(f"步骤 {data['step']} 完成")
        elif event_type == "activation_complete":
            if data.get('success'):
                print("激活完成")
            else:
                print(f"激活失败: {data.get('error', '未知错误')}")
    
    def _clear_config(self):
        """清除当前配置"""
        self.version_var.set("")
        self.edition_var.set("")
        self.selected_server.set("")
        self.custom_server.set("")
        
        self.key_display.config(state="normal")
        self.key_display.delete(1.0, tk.END)
        self.key_display.config(state="disabled")
        
        self.server_status.config(state="normal")
        self.server_status.delete(1.0, tk.END)
        self.server_status.config(bg="white", state="disabled")
        
        self.config_display.config(state="normal")
        self.config_display.delete(1.0, tk.END)
        self.config_display.config(state="disabled")
        
        self.current_selection = {}
    
    def _set_window_icon(self):
        """设置窗口图标"""
        try:
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            icon_path = os.path.join(application_path, "icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
            else:
                self._set_window_icon_from_png()
        except Exception:
            self._set_window_icon_from_png()
    
    def _set_window_icon_from_png(self):
        """从PNG文件设置窗口图标"""
        try:
            if Image and ImageTk:
                if getattr(sys, 'frozen', False):
                    application_path = sys._MEIPASS
                else:
                    application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                
                png_path = os.path.join(application_path, "icon.png")
                if os.path.exists(png_path):
                    icon_image = Image.open(png_path)
                    icon_photo = ImageTk.PhotoImage(icon_image)
                    self.root.iconphoto(True, icon_photo)
        except Exception:
            pass
    
    def _set_taskbar_icon(self):
        """设置Windows任务栏图标"""
        try:
            import ctypes
            if os.name == 'nt':
                if getattr(sys, 'frozen', False):
                    application_path = sys._MEIPASS
                else:
                    application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                
                icon_path = os.path.join(application_path, "icon.ico")
                if os.path.exists(icon_path):
                    myappid = 'KMSActivator.Enterprise.1.0'
                    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass
    
    def _set_background_image(self):
        """设置背景图片"""
        try:
            if Image and ImageTk:
                if getattr(sys, 'frozen', False):
                    application_path = sys._MEIPASS
                else:
                    application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                
                image_path = os.path.join(application_path, "image.png")
                if os.path.exists(image_path):
                    original_image = Image.open(image_path)
                    resized_image = original_image.resize((800, 600), Image.Resampling.LANCZOS)
                    
                    if resized_image.mode != 'RGBA':
                        resized_image = resized_image.convert('RGBA')
                    
                    alpha = resized_image.split()[-1]
                    alpha = alpha.point(lambda p: int(p * 0.5))
                    resized_image.putalpha(alpha)
                    
                    self.background_image = ImageTk.PhotoImage(resized_image)
                    self.background_label = tk.Label(self.root, image=self.background_image)
                    self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            pass
    
    def _has_background_image(self) -> bool:
        """检查是否有背景图片"""
        try:
            if Image and ImageTk:
                if getattr(sys, 'frozen', False):
                    application_path = sys._MEIPASS
                else:
                    application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                
                image_path = os.path.join(application_path, "image.png")
                return os.path.exists(image_path)
        except Exception:
            pass
        return False
    
    def run(self):
        """运行UI"""
        self.create_main_window()
        self.setup_ui()
        self.root.mainloop()
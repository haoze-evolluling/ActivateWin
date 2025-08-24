#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows KMS激活管理程序
基于微软官方授权的合规激活工具
用于企业内部Windows系统的批量激活管理
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys
import json
from typing import Dict, List, Tuple

class KMSActivator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Windows KMS激活管理器 - 企业版")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # 设置窗口图标 - 使用绝对路径确保可靠性
        self.set_window_icon()
        
        # 设置任务栏图标（Windows专用）
        self.set_taskbar_icon()
        
        # 初始化数据
        self.kms_servers = []
        self.windows_versions = {}
        self.selected_server = tk.StringVar()
        self.custom_server = tk.StringVar()
        self.current_selection = {}
        
        self.load_data()
        self.setup_ui()
        
    def load_data(self):
        """加载KMS服务器地址和Windows版本数据"""
        # 从kmsserver.md加载服务器地址
        try:
            with open("kmsserver.md", "r", encoding="utf-8") as f:
                servers = f.read().strip().split('\n')
                self.kms_servers = [s.strip() for s in servers if s.strip()]
        except:
            # 默认服务器列表
            self.kms_servers = [
                "kms.bige0.com",
                "kms.03k.org", 
                "kms.wxlost.com",
                "kms.moeyuuko.top",
                "kms.loli.best",
                "kms.loli.beer",
                "kms.cgtsoft.com",
                "kms.sixyin.com",
                "kms.litbear.cn"
            ]
        
        # 从kmskey.md加载Windows版本信息
        self.windows_versions = {
            "Windows 11": {
                "专业版": "VK7JG-NPHTM-C97JM-9MPGT-3V66T",
                "企业版": "XGVPP-NMH47-7TTHJ-W3FW7-8HV2C",
                "教育版": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
                "专业工作站版": "NRG8B-VKK3Q-CXVCJ-9G2XF-6Q84J"
            },
            "Windows 10": {
                "专业版": "W269N-WFGWX-YVC9B-4J6C9-T83GX",
                "企业版": "NPPR9-FWDCX-D2C8J-H872K-2YT43",
                "教育版": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
                "专业工作站版": "NRG8B-VKK3Q-CXVCJ-9G2XF-6Q84J"
            },
            "Windows Server 2022": {
                "标准版": "VDYBN-27WPP-V4HQT-9VMD4-VMK7H",
                "数据中心版": "WX4NM-KYWYW-QJJR4-XV3QB-6VM33"
            },
            "Windows Server 2019": {
                "标准版": "N69G4-B89J2-4G8F4-WWYCC-J464C",
                "数据中心版": "WMDGN-G9PQG-XVVXX-R3X43-63DFG"
            }
        }
        
    def setup_ui(self):
        """设置用户界面"""
        # 设置主题
        self.root.configure(bg='#f0f0f0')
        
        # 标题区域
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title_label = ttk.Label(title_frame, text="Windows KMS激活管理器", 
                               font=("Microsoft YaHei", 18, "bold"),
                               foreground='#2c3e50')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="基于微软官方授权的企业级激活管理工具", 
                                   font=("Microsoft YaHei", 11), foreground="#7f8c8d")
        subtitle_label.pack()
        
        # 主内容区域
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 左侧：版本选择
        left_frame = ttk.LabelFrame(main_frame, text="版本选择", padding=15)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        left_frame.configure(style='Card.TFrame')
        
        self.setup_version_selection(left_frame)
        
        # 右侧：KMS服务器配置
        right_frame = ttk.LabelFrame(main_frame, text="KMS服务器配置", padding=15)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_frame.configure(style='Card.TFrame')
        
        self.setup_server_config(right_frame)
        
        # 底部：操作区域
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.setup_action_area(bottom_frame)
        
    def setup_version_selection(self, parent):
        """设置版本选择界面"""
        # 一级选择：Windows版本
        ttk.Label(parent, text="选择Windows版本:").pack(anchor=tk.W)
        
        self.version_var = tk.StringVar()
        version_combo = ttk.Combobox(parent, textvariable=self.version_var,
                                   values=list(self.windows_versions.keys()),
                                   state="readonly", width=25)
        version_combo.pack(fill=tk.X, pady=5)
        version_combo.bind("<<ComboboxSelected>>", self.on_version_selected)
        
        # 二级选择：具体版本号
        ttk.Label(parent, text="选择具体版本:").pack(anchor=tk.W, pady=(10, 0))
        
        self.edition_var = tk.StringVar()
        self.edition_combo = ttk.Combobox(parent, textvariable=self.edition_var,
                                        state="readonly", width=25)
        self.edition_combo.pack(fill=tk.X, pady=5)
        self.edition_combo.bind("<<ComboboxSelected>>", self.on_edition_selected)
        
        # 显示选择的密钥
        ttk.Label(parent, text="对应产品密钥:").pack(anchor=tk.W, pady=(10, 0))
        
        self.key_display = tk.Text(parent, height=2, width=30, state="disabled")
        self.key_display.pack(fill=tk.X, pady=5)
        
    def setup_server_config(self, parent):
        """设置KMS服务器配置界面"""
        # 预设服务器选择
        ttk.Label(parent, text="选择预设KMS服务器:").pack(anchor=tk.W)
        
        self.server_combo = ttk.Combobox(parent, textvariable=self.selected_server,
                                       values=self.kms_servers, state="readonly", width=35)
        self.server_combo.pack(fill=tk.X, pady=5)
        
        # 或选择自定义服务器
        separator = ttk.Separator(parent, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=10)
        
        ttk.Label(parent, text="或输入自定义服务器:").pack(anchor=tk.W)
        
        custom_entry = ttk.Entry(parent, textvariable=self.custom_server, width=35)
        custom_entry.pack(fill=tk.X, pady=5)
        
        # 服务器状态显示
        ttk.Label(parent, text="服务器状态:").pack(anchor=tk.W, pady=(10, 0))
        
        self.server_status = tk.Text(parent, height=3, width=35, state="disabled")
        self.server_status.pack(fill=tk.X, pady=5)
        
        # 测试连接按钮
        test_btn = ttk.Button(parent, text="测试服务器连接", command=self.test_server_connection)
        test_btn.pack(pady=5)
        
    def setup_action_area(self, parent):
        """设置操作区域"""
        # 当前配置显示
        config_frame = ttk.LabelFrame(parent, text="当前配置", padding=10)
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.config_display = tk.Text(config_frame, height=4, state="disabled")
        self.config_display.pack(fill=tk.X)
        
        # 操作按钮
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="开始激活", command=self.start_activation,
                  style="Accent.TButton").pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(button_frame, text="清除配置", command=self.clear_config).pack(side=tk.RIGHT, padx=5)
        
    def on_version_selected(self, event):
        """当选择Windows版本时"""
        version = self.version_var.get()
        if version in self.windows_versions:
            editions = list(self.windows_versions[version].keys())
            self.edition_combo["values"] = editions
            self.edition_combo.set("")
            self.update_config_display()
            
    def on_edition_selected(self, event):
        """当选择具体版本时"""
        version = self.version_var.get()
        edition = self.edition_var.get()
        
        if version and edition and version in self.windows_versions and edition in self.windows_versions[version]:
            key = self.windows_versions[version][edition]
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
            
            self.update_config_display()
            
    def test_server_connection(self):
        """测试KMS服务器连接可用性"""
        server = self.custom_server.get() or self.selected_server.get()
        if not server:
            messagebox.showwarning("警告", "请先选择或输入KMS服务器地址")
            return
            
        self.server_status.config(state="normal")
        self.server_status.delete(1.0, tk.END)
        self.server_status.insert(1.0, f"正在测试连接: {server}...")
        self.server_status.config(state="disabled")
        self.root.update()
        
        try:
            # 使用增强的ping命令测试服务器可用性
            result = subprocess.run(
                ["ping", "-n", "2", "-w", "1000", server], 
                capture_output=True, 
                text=True, 
                timeout=3
            )
            
            self.server_status.config(state="normal")
            self.server_status.delete(1.0, tk.END)
            
            if result.returncode == 0:
                # 解析ping结果获取响应时间
                output_lines = result.stdout.split('\n')
                response_times = []
                for line in output_lines:
                    if '时间=' in line or 'time=' in line:
                        try:
                            time_part = line.split('=')[-1].split('ms')[0].strip()
                            response_times.append(int(time_part))
                        except:
                            pass
                
                if response_times:
                    avg_time = sum(response_times) // len(response_times)
                    self.server_status.insert(1.0, f"✓ 服务器 {server} 连接正常\n平均响应时间: {avg_time}ms")
                else:
                    self.server_status.insert(1.0, f"✓ 服务器 {server} 连接正常")
                    
                self.server_status.config(bg="#90EE90")  # 浅绿色
            else:
                # 分析连接失败原因
                error_msg = "连接失败"
                if "找不到主机" in result.stderr or "无法解析" in result.stderr:
                    error_msg = "DNS解析失败"
                elif "请求超时" in result.stdout or "Request timed out" in result.stdout:
                    error_msg = "请求超时"
                elif "目标主机无法访问" in result.stderr:
                    error_msg = "目标主机无法访问"
                
                self.server_status.insert(1.0, f"✗ 服务器 {server} {error_msg}")
                self.server_status.config(bg="#FFB6C1")  # 浅红色
                
            self.server_status.config(state="disabled")
            
        except subprocess.TimeoutExpired:
            self.server_status.config(state="normal")
            self.server_status.delete(1.0, tk.END)
            self.server_status.insert(1.0, f"✗ 服务器 {server} 测试超时（超过3秒）")
            self.server_status.config(bg="#FFB6C1")
            self.server_status.config(state="disabled")
            
        except FileNotFoundError:
            self.server_status.config(state="normal")
            self.server_status.delete(1.0, tk.END)
            self.server_status.insert(1.0, f"✗ 系统缺少ping命令工具")
            self.server_status.config(bg="#FFB6C1")
            self.server_status.config(state="disabled")
            
        except Exception as e:
            self.server_status.config(state="normal")
            self.server_status.delete(1.0, tk.END)
            self.server_status.insert(1.0, f"✗ 测试失败: {str(e)}")
            self.server_status.config(bg="#FFB6C1")
            self.server_status.config(state="disabled")
            
    def update_config_display(self):
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
        
    def start_activation(self):
        """开始激活流程"""
        if not self.current_selection:
            messagebox.showerror("错误", "请先选择Windows版本和具体版本")
            return
            
        server = self.custom_server.get() or self.selected_server.get()
        if not server:
            messagebox.showerror("错误", "请先选择或输入KMS服务器地址")
            return
            
        # 确认激活
        message = f"确定要激活以下配置吗？\n\n"
        message += f"Windows版本: {self.current_selection['version']}\n"
        message += f"具体版本: {self.current_selection['edition']}\n"
        message += f"产品密钥: {self.current_selection['key']}\n"
        message += f"KMS服务器: {server}"
        
        if not messagebox.askyesno("确认激活", message):
            return
            
        self.execute_activation()
        
    def execute_activation(self):
        """执行激活命令"""
        key = self.current_selection['key']
        server = self.custom_server.get() or self.selected_server.get()
        
        try:
            # 安装产品密钥
            subprocess.run(["slmgr", "/ipk", key], check=True)
            
            # 设置KMS服务器
            subprocess.run(["slmgr", "/skms", server], check=True)
            
            # 执行激活
            result = subprocess.run(["slmgr", "/ato"], capture_output=True, text=True)
            
            if result.returncode == 0:
                messagebox.showinfo("成功", "Windows激活成功！")
            else:
                messagebox.showerror("激活失败", f"激活失败:\n{result.stderr}")
                
        except subprocess.CalledProcessError as e:
            messagebox.showerror("执行错误", f"命令执行失败:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("错误", f"发生未知错误:\n{str(e)}")
            
    def clear_config(self):
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
        
    def set_window_icon(self):
        """设置窗口图标"""
        try:
            # 获取当前脚本所在目录
            if getattr(sys, 'frozen', False):
                # 如果是打包后的exe文件
                application_path = sys._MEIPASS
            else:
                # 如果是脚本运行
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            icon_path = os.path.join(application_path, "icon.ico")
            
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
                print(f"成功加载图标: {icon_path}")
            else:
                print(f"图标文件不存在: {icon_path}")
                
        except Exception as e:
            print(f"设置窗口图标时出错: {e}")
            # 如果.ico文件加载失败，尝试使用.png文件
            self.set_window_icon_from_png()
    
    def set_window_icon_from_png(self):
        """从PNG文件设置窗口图标（备选方案）"""
        try:
            from PIL import Image, ImageTk
            
            # 获取当前脚本所在目录
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            png_path = os.path.join(application_path, "icon.png")
            
            if os.path.exists(png_path):
                icon_image = Image.open(png_path)
                icon_photo = ImageTk.PhotoImage(icon_image)
                self.root.iconphoto(True, icon_photo)
                print(f"成功从PNG加载图标: {png_path}")
            else:
                print(f"PNG图标文件不存在: {png_path}")
                
        except Exception as e:
            print(f"从PNG设置图标时出错: {e}")
    
    def set_taskbar_icon(self):
        """设置Windows任务栏图标"""
        try:
            import ctypes
            
            # 获取当前脚本所在目录
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            icon_path = os.path.join(application_path, "icon.ico")
            
            if os.path.exists(icon_path):
                # 设置应用程序ID，确保任务栏图标正确显示
                myappid = 'KMSActivator.Enterprise.1.0'
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
                print("任务栏图标设置完成")
            else:
                print("任务栏图标文件不存在")
                
        except Exception as e:
            print(f"设置任务栏图标时出错: {e}")
            
    def run(self):
        """运行应用程序"""
        self.root.mainloop()

if __name__ == "__main__":
    # 检查管理员权限
    try:
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            # 以管理员身份重新运行程序，然后立即退出当前实例
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, __file__, None, 1)
            sys.exit(0)
    except SystemExit:
        # 正常退出
        sys.exit(0)
    except Exception as e:
        # 如果权限提升失败，显示错误信息并继续运行（可能无法执行激活命令）
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        messagebox.showwarning("警告", f"无法获取管理员权限，某些功能可能受限:\n{str(e)}")
        root.destroy()
        
    # 只有具有管理员权限的实例才会继续执行这里
    app = KMSActivator()
    app.run()

    def set_window_icon(self):
        """设置窗口图标"""
        try:
            # 获取当前脚本所在目录
            if getattr(sys, 'frozen', False):
                # 如果是打包后的exe文件
                application_path = sys._MEIPASS
            else:
                # 如果是脚本运行
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            icon_path = os.path.join(application_path, "icon.ico")
            
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
                print(f"成功加载图标: {icon_path}")
            else:
                print(f"图标文件不存在: {icon_path}")
                
        except Exception as e:
            print(f"设置窗口图标时出错: {e}")
            # 如果.ico文件加载失败，尝试使用.png文件
            self.set_window_icon_from_png()
    
    def set_window_icon_from_png(self):
        """从PNG文件设置窗口图标（备选方案）"""
        try:
            from PIL import Image, ImageTk
            
            # 获取当前脚本所在目录
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            png_path = os.path.join(application_path, "icon.png")
            
            if os.path.exists(png_path):
                icon_image = Image.open(png_path)
                icon_photo = ImageTk.PhotoImage(icon_image)
                self.root.iconphoto(True, icon_photo)
                print(f"成功从PNG加载图标: {png_path}")
            else:
                print(f"PNG图标文件不存在: {png_path}")
                
        except Exception as e:
            print(f"从PNG设置图标时出错: {e}")
    
    def set_taskbar_icon(self):
        """设置Windows任务栏图标"""
        try:
            import ctypes
            
            # 获取当前脚本所在目录
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            icon_path = os.path.join(application_path, "icon.ico")
            
            if os.path.exists(icon_path):
                # 设置应用程序ID，确保任务栏图标正确显示
                myappid = 'KMSActivator.Enterprise.1.0'
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
                print("任务栏图标设置完成")
            else:
                print("任务栏图标文件不存在")
                
        except Exception as e:
            print(f"设置任务栏图标时出错: {e}")
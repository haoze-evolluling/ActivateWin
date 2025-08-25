"""
UI组件模块
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import socket
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from models.activation_data import ActivationData
from backend.kms_service import KMSService


class VersionSelector(ttk.LabelFrame):
    """版本选择组件"""
    
    def __init__(self, parent):
        super().__init__(parent, text="Windows版本选择", padding=10)
        self.on_config_change = None
        self.create_widgets()
        self.load_data()
        
    def create_widgets(self):
        """创建组件"""
        # 主版本选择
        ttk.Label(self, text="Windows版本:").grid(row=0, column=0, sticky='w', pady=5)
        self.version_var = tk.StringVar()
        self.version_combo = ttk.Combobox(
            self, 
            textvariable=self.version_var,
            state='readonly',
            width=25
        )
        self.version_combo.grid(row=0, column=1, sticky='ew', pady=5, padx=5)
        self.version_combo.bind('<<ComboboxSelected>>', self.on_version_change)
        
        # 具体版本选择
        ttk.Label(self, text="具体版本:").grid(row=1, column=0, sticky='w', pady=5)
        self.edition_var = tk.StringVar()
        self.edition_combo = ttk.Combobox(
            self,
            textvariable=self.edition_var,
            state='readonly',
            width=25
        )
        self.edition_combo.grid(row=1, column=1, sticky='ew', pady=5, padx=5)
        self.edition_combo.bind('<<ComboboxSelected>>', self.on_edition_change)
        
        # 产品密钥显示
        ttk.Label(self, text="产品密钥:").grid(row=2, column=0, sticky='w', pady=5)
        self.key_display = tk.Text(self, height=2, width=25, state='disabled')
        self.key_display.grid(row=2, column=1, sticky='ew', pady=5, padx=5)
        
        # 配置列权重
        self.columnconfigure(1, weight=1)
        
    def load_data(self):
        """加载版本数据"""
        try:
            versions = ActivationData.get_all_windows_versions()
            self.version_combo['values'] = versions
            if versions:
                self.version_combo.set(versions[0])
                self.on_version_change()
        except Exception as e:
            pass
            
    def on_version_change(self, event=None):
        """版本选择变更处理"""
        version = self.version_var.get()
        if version:
            try:
                editions = ActivationData.get_editions(version)
                self.edition_combo['values'] = editions
                if editions:
                    self.edition_combo.set(editions[0])
                    self.on_edition_change()
            except Exception as e:
                pass
                
    def on_edition_change(self, event=None):
        """版本详情变更处理"""
        version = self.version_var.get()
        edition = self.edition_var.get()
        if version and edition:
            try:
                key = ActivationData.get_product_key(version, edition)
                self.display_product_key(key)
                if self.on_config_change:
                    self.on_config_change()
            except Exception as e:
                pass
                
    def display_product_key(self, key):
        """显示产品密钥"""
        self.key_display.config(state='normal')
        self.key_display.delete(1.0, tk.END)
        self.key_display.insert(1.0, key)
        self.key_display.config(state='disabled')
        
    def get_config(self):
        """获取配置描述"""
        version = self.version_var.get()
        edition = self.edition_var.get()
        if version and edition:
            return f"{version} {edition}"
        return None
        
    def get_config_dict(self):
        """获取配置字典"""
        version = self.version_var.get()
        edition = self.edition_var.get()
        if version and edition:
            return {
                'version': version,
                'edition': edition,
                'product_key': ActivationData.get_product_key(version, edition)
            }
        return None
        
    def clear(self):
        """清除配置"""
        self.version_combo.set('')
        self.edition_combo.set('')
        self.key_display.config(state='normal')
        self.key_display.delete(1.0, tk.END)
        self.key_display.config(state='disabled')


class KMSServerPanel(ttk.LabelFrame):
    """KMS服务器配置组件"""
    
    def __init__(self, parent):
        super().__init__(parent, text="KMS服务器配置", padding=10)
        self.on_config_change = None
        self.create_widgets()
        self.load_data()
        
    def create_widgets(self):
        """创建组件"""
        # 服务器选择方式
        self.server_type = tk.StringVar(value='preset')
        
        # 预设服务器选项
        preset_frame = ttk.Frame(self)
        preset_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Radiobutton(
            preset_frame,
            text="预设服务器",
            variable=self.server_type,
            value='preset',
            command=self.on_server_type_change
        ).pack(side='left')
        
        self.preset_server_var = tk.StringVar()
        self.preset_combo = ttk.Combobox(
            preset_frame,
            textvariable=self.preset_server_var,
            state='readonly',
            width=20
        )
        self.preset_combo.pack(side='left', padx=10)
        self.preset_combo.bind('<<ComboboxSelected>>', self.on_server_change)
        
        # 自定义服务器选项
        custom_frame = ttk.Frame(self)
        custom_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Radiobutton(
            custom_frame,
            text="自定义服务器",
            variable=self.server_type,
            value='custom',
            command=self.on_server_type_change
        ).pack(side='left')
        
        self.custom_server_var = tk.StringVar()
        self.custom_entry = ttk.Entry(
            custom_frame,
            textvariable=self.custom_server_var,
            width=20,
            state='disabled'
        )
        self.custom_entry.pack(side='left', padx=10)
        self.custom_entry.bind('<KeyRelease>', self.on_server_change)
        
        # 连接测试按钮
        self.test_btn = ttk.Button(
            self,
            text="测试连接",
            command=self.test_connection
        )
        self.test_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # 连接状态显示
        self.status_label = ttk.Label(
            self,
            text="未测试",
            font=('Microsoft YaHei', 9)
        )
        self.status_label.grid(row=3, column=0, columnspan=2)
        
        # 配置列权重
        self.columnconfigure(0, weight=1)
        
    def load_data(self):
        """加载服务器数据"""
        try:
            servers = ActivationData.get_all_kms_servers()
            self.preset_combo['values'] = servers
            if servers:
                self.preset_combo.set(servers[0])
                if self.on_config_change:
                    self.on_config_change()
        except Exception as e:
            pass
            
    def on_server_type_change(self):
        """服务器类型变更处理"""
        if self.server_type.get() == 'preset':
            self.custom_entry.config(state='disabled')
            self.preset_combo.config(state='readonly')
        else:
            self.custom_entry.config(state='normal')
            self.preset_combo.config(state='disabled')
            
        if self.on_config_change:
            self.on_config_change()
            
    def on_server_change(self, event=None):
        """服务器变更处理"""
        if self.on_config_change:
            self.on_config_change()
            
    def test_connection(self):
        """测试服务器连接"""
        server = self.get_server()
        if not server:
            messagebox.showerror("错误", "请先选择或输入服务器地址")
            return
            
        self.status_label.config(text="测试中...")
        self.test_btn.config(state='disabled')
        
        def test_thread():
            try:
                result = KMSService.test_server_connection(server)
                self.root.after(0, lambda r=result: self.update_test_result(r))
            except Exception as test_error:
                self.root.after(0, lambda e=str(test_error): self.update_test_result(False, e))
                
        threading.Thread(target=test_thread, daemon=True).start()
        
    def update_test_result(self, success, error=None):
        """更新测试结果"""
        if success:
            self.status_label.config(
                text="连接成功",
                foreground='green'
            )
            self.status_label.config(background='#90EE90')
        else:
            error_msg = error or "连接失败"
            self.status_label.config(
                text=f"连接失败: {error_msg}",
                foreground='red'
            )
            self.status_label.config(background='#FFB6C1')
            
        self.test_btn.config(state='normal')
        
    def get_server(self):
        """获取服务器地址"""
        if self.server_type.get() == 'preset':
            return self.preset_server_var.get()
        else:
            return self.custom_server_var.get().strip()
            
    def get_config(self):
        """获取配置描述"""
        server = self.get_server()
        return f"服务器: {server}" if server else None
        
    def get_config_dict(self):
        """获取配置字典"""
        server = self.get_server()
        if server:
            return {
                'server': server,
                'type': self.server_type.get()
            }
        return None
        
    def clear(self):
        """清除配置"""
        self.server_type.set('preset')
        self.preset_combo.set('')
        self.custom_server_var.set('')
        self.custom_entry.config(state='disabled')
        self.preset_combo.config(state='readonly')
        self.status_label.config(text="未测试", foreground='black', background='')
        
    @property
    def root(self):
        """获取根窗口"""
        return self.winfo_toplevel()


class ActivationPanel(tk.Toplevel):
    """激活进度面板"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Windows激活中...")
        self.geometry("400x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """创建组件"""
        # 标题
        title = ttk.Label(
            self,
            text="正在执行Windows激活...",
            font=('Microsoft YaHei', 12, 'bold')
        )
        title.pack(pady=20)
        
        # 进度条
        self.progress = ttk.Progressbar(
            self,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(pady=10)
        self.progress.start()
        
        # 状态显示
        self.status_text = tk.Text(
            self,
            height=8,
            width=40,
            state='disabled'
        )
        self.status_text.pack(pady=10, padx=20)
        
        # 关闭按钮
        self.close_btn = ttk.Button(
            self,
            text="取消",
            command=self.destroy
        )
        self.close_btn.pack(pady=10)
        
    def start_activation(self, version_config, kms_config):
        """开始激活"""
        self.update_status("准备激活...")
        
        # 验证配置完整性
        if not version_config or not kms_config:
            self.on_activation_complete(False, "配置不完整，请检查所有必要参数")
            return
            
        if not version_config.get('product_key'):
            self.on_activation_complete(False, "产品密钥为空")
            return
            
        if not kms_config.get('server'):
            self.on_activation_complete(False, "KMS服务器地址为空")
            return
        
        # 导入后端服务
        try:
            from backend.kms_service import KMSService
            from models.activation_data import ActivationConfig
            
            # 创建激活配置
            config = ActivationConfig(
                windows_version=version_config['version'],
                edition=version_config['edition'],
                product_key=version_config['product_key'],
                kms_server=kms_config['server']
            )
            
            # 创建KMS服务实例
            kms_service = KMSService()
            
            # 添加回调函数以更新UI
            def activation_callback(event_type, data):
                try:
                    if event_type == "activation_start":
                        self.update_status("开始激活流程...")
                    elif event_type == "step_start":
                        step_desc = data.get("description", "")
                        self.update_status(f"正在执行: {step_desc}")
                    elif event_type == "step_complete":
                        step_num = data.get("step", 0)
                        self.update_status(f"步骤 {step_num} 完成")
                    elif event_type == "activation_complete":
                        success = data.get("success", False)
                        error = data.get("error", "")
                        self.root.after(0, lambda s=success, e=error: self.on_activation_complete(s, e))
                except Exception as callback_error:
                    self.root.after(0, lambda e=str(callback_error): self.on_activation_complete(False, f"回调处理错误: {e}"))
            
            kms_service.add_activation_callback(activation_callback)
            
            # 在后台线程中执行激活
            import threading
            def run_activation():
                try:
                    success, message = kms_service.execute_activation(config)
                    self.root.after(0, lambda s=success, m=message: self.on_activation_complete(s, m))
                except Exception as e:
                    error_msg = f"激活过程错误: {str(e)}"
                    self.root.after(0, lambda e=error_msg: self.on_activation_complete(False, e))
            
            threading.Thread(target=run_activation, daemon=True).start()
            
        except ImportError as e:
            error_msg = f"导入模块失败: {e}"
            self.update_status(error_msg)
            self.after(1000, lambda: self.on_activation_complete(False, error_msg))
        except Exception as e:
            error_msg = f"启动激活失败: {e}"
            self.update_status(error_msg)
            self.after(1000, lambda: self.on_activation_complete(False, error_msg))
        
    def update_status(self, message):
        """更新状态"""
        self.status_text.config(state='normal')
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state='disabled')
        
    def on_activation_complete(self, success, message):
        """激活完成处理"""
        self.progress.stop()
        
        if success:
            self.update_status("激活成功！")
            self.update_status("Windows已成功激活")
        else:
            self.update_status(f"激活失败: {message}")
        
        self.close_btn.config(text="完成")
        
        # 显示结果对话框
        from frontend.dialogs import ActivationResultDialog
        ActivationResultDialog(self, success, message)
        
    def simulate_activation(self):
        """模拟激活过程（已废弃，保留用于测试）"""
        steps = [
            "正在验证产品密钥...",
            "正在连接KMS服务器...",
            "正在发送激活请求...",
            "正在处理激活响应...",
            "激活成功！"
        ]
        
        def next_step(index=0):
            if index < len(steps):
                self.update_status(steps[index])
                self.after(1000, lambda: next_step(index + 1))
            else:
                self.progress.stop()
                self.close_btn.config(text="完成")
                
        next_step()
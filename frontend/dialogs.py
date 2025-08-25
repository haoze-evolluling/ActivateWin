"""
对话框模块
"""

import tkinter as tk
from tkinter import ttk, messagebox


class ErrorDialog:
    """错误对话框"""
    
    @staticmethod
    def show(parent, title, message):
        """显示错误对话框"""
        messagebox.showerror(title, message, parent=parent)


class InfoDialog:
    """信息对话框"""
    
    @staticmethod
    def show(parent, title, message):
        """显示信息对话框"""
        messagebox.showinfo(title, message, parent=parent)


class ConfirmDialog:
    """确认对话框"""
    
    @staticmethod
    def show(parent, title, message):
        """显示确认对话框"""
        return messagebox.askyesno(title, message, parent=parent)


class ConfigSummaryDialog(tk.Toplevel):
    """配置摘要对话框"""
    
    def __init__(self, parent, config):
        super().__init__(parent)
        self.title("激活配置确认")
        self.geometry("400x400")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.config = config
        self.result = False
        
        self.create_widgets()
        
    def create_widgets(self):
        """创建组件"""
        # 标题
        title = ttk.Label(
            self,
            text="请确认激活配置",
            font=('Microsoft YaHei', 12, 'bold')
        )
        title.pack(pady=20)
        
        # 配置详情
        details_frame = ttk.LabelFrame(self, text="配置详情", padding=10)
        details_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # 显示配置信息
        config_text = tk.Text(
            details_frame,
            height=10,
            width=40,
            state='disabled'
        )
        config_text.pack(fill='both', expand=True)
        
        # 填充配置信息
        config_text.config(state='normal')
        config_text.insert(1.0, self.format_config())
        config_text.config(state='disabled')
        
        # 按钮
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        
        ttk.Button(
            button_frame,
            text="确认激活",
            command=self.confirm
        ).pack(side='left', padx=5)
        
        ttk.Button(
            button_frame,
            text="取消",
            command=self.cancel
        ).pack(side='left', padx=5)
        
    def format_config(self):
        """格式化配置信息"""
        lines = []
        
        if 'version' in self.config:
            lines.append(f"Windows版本: {self.config['version']}")
            
        if 'edition' in self.config:
            lines.append(f"具体版本: {self.config['edition']}")
            
        if 'product_key' in self.config:
            lines.append(f"产品密钥: {self.config['product_key']}")
            
        if 'server' in self.config:
            lines.append(f"KMS服务器: {self.config['server']}")
            
        return '\n'.join(lines)
        
    def confirm(self):
        """确认激活"""
        self.result = True
        self.destroy()
        
    def cancel(self):
        """取消激活"""
        self.result = False
        self.destroy()
        
    def get_result(self):
        """获取结果"""
        self.wait_window()
        return self.result


class ActivationResultDialog(tk.Toplevel):
    """激活结果对话框"""
    
    def __init__(self, parent, success, details=""):
        super().__init__(parent)
        self.title("激活结果")
        self.geometry("350x250")
        self.resizable(False, False)
        self.transient(parent)
        
        self.success = success
        self.details = details
        
        self.create_widgets()
        
    def create_widgets(self):
        """创建组件"""
        # 图标和标题
        icon_frame = ttk.Frame(self)
        icon_frame.pack(pady=20)
        
        # 状态图标
        icon_text = "✓" if self.success else "✗"
        icon_color = "green" if self.success else "red"
        
        icon_label = ttk.Label(
            icon_frame,
            text=icon_text,
            font=('Microsoft YaHei', 48),
            foreground=icon_color
        )
        icon_label.pack()
        
        # 状态标题
        title_text = "激活成功！" if self.success else "激活失败"
        title_color = "green" if self.success else "red"
        
        title = ttk.Label(
            icon_frame,
            text=title_text,
            font=('Microsoft YaHei', 16, 'bold'),
            foreground=title_color
        )
        title.pack(pady=10)
        
        # 详情
        if self.details:
            details_frame = ttk.LabelFrame(self, text="详细信息", padding=10)
            details_frame.pack(fill='both', expand=True, padx=20, pady=10)
            
            details_text = tk.Text(
                details_frame,
                height=4,
                width=35,
                state='disabled'
            )
            details_text.pack(fill='both', expand=True)
            
            details_text.config(state='normal')
            details_text.insert(1.0, self.details)
            details_text.config(state='disabled')
        
        # 关闭按钮
        ttk.Button(
            self,
            text="关闭",
            command=self.destroy
        ).pack(pady=10)
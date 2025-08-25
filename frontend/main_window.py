"""
Windows KMS激活管理器主窗口
"""

import tkinter as tk
from tkinter import ttk
import os
import sys
from pathlib import Path

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.components import VersionSelector, KMSServerPanel, ActivationPanel
from frontend.dialogs import ErrorDialog
from frontend.styles import AppStyles


class MainWindow:
    """主窗口类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.setup_layout()
        
    def setup_window(self):
        """设置窗口属性"""
        self.root.title("Windows KMS激活管理器 - 企业版")
        self.root.geometry("800x640")
        self.root.resizable(False, False)
        self.root.configure(bg='#e6f7ff')  # 初音未来蓝浅背景色
        
        # 设置窗口图标
        self.set_window_icon()
        
        # 设置任务栏图标
        self.set_taskbar_icon()
        
    def set_window_icon(self):
        """设置窗口图标"""
        try:
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller打包环境
                icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
            else:
                # 开发环境
                icon_path = os.path.join(os.path.dirname(__file__), '..', 'icon.ico')
            
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
            else:
                # 备选PNG图标
                png_path = os.path.join(os.path.dirname(__file__), '..', 'icon.png')
                if os.path.exists(png_path):
                    from PIL import Image, ImageTk
                    icon = Image.open(png_path)
                    self.root.iconphoto(True, ImageTk.PhotoImage(icon))
        except Exception:
            pass  # 图标设置失败不影响主程序运行
            
    def set_taskbar_icon(self):
        """设置任务栏图标"""
        try:
            import ctypes
            myappid = 'ActivateWin.KMSManager.Enterprise.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass
            
    def setup_styles(self):
        """设置应用样式"""
        self.styles = AppStyles()
        
    def create_widgets(self):
        """创建界面组件"""
        # 标题区域
        self.create_header()
        
        # 主内容区域
        self.create_main_content()
        
        # 操作区域
        self.create_action_area()
        
    def create_header(self):
        """创建标题区域"""
        header_frame = ttk.Frame(self.root, style='Header.TFrame')
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        title_label = ttk.Label(
            header_frame,
            text="Windows KMS激活管理器",
            style='HeaderTitle.TLabel'
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            header_frame,
            text="企业版 - 专业Windows批量激活解决方案",
            style='HeaderSubtitle.TLabel'
        )
        subtitle_label.pack()
        
    def create_main_content(self):
        """创建主内容区域"""
        content_frame = ttk.Frame(self.root, style='Content.TFrame')
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # 左侧版本选择面板
        self.version_selector = VersionSelector(content_frame)
        self.version_selector.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # 右侧KMS服务器配置面板
        self.kms_panel = KMSServerPanel(content_frame)
        self.kms_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
    def create_action_area(self):
        """创建操作区域"""
        action_frame = ttk.Frame(self.root, style='Action.TFrame')
        action_frame.pack(fill='x', padx=20, pady=(10, 20))
        
        # 配置显示区域
        self.config_display = ttk.Label(
            action_frame,
            text="请配置激活参数",
            style='ConfigDisplay.TLabel'
        )
        self.config_display.pack(fill='x', pady=(0, 10))
        
        # 操作按钮
        button_frame = ttk.Frame(action_frame)
        button_frame.pack()
        
        self.clear_btn = ttk.Button(
            button_frame,
            text="清除配置",
            command=self.clear_config,
            style='Action.TButton'
        )
        self.clear_btn.pack(side='left', padx=5)
        
        self.activate_btn = ttk.Button(
            button_frame,
            text="开始激活",
            command=self.start_activation,
            style='Action.TButton'
        )
        self.activate_btn.pack(side='left', padx=5)
        
    def setup_layout(self):
        """设置布局"""
        # 绑定组件间通信
        self.version_selector.on_config_change = self.update_config_display
        self.kms_panel.on_config_change = self.update_config_display
        
    def update_config_display(self):
        """更新配置显示"""
        version_config = self.version_selector.get_config()
        kms_config = self.kms_panel.get_config()
        
        if version_config and kms_config:
            display_text = f"当前配置: {version_config} | {kms_config}"
            self.config_display.config(text=display_text)
        else:
            self.config_display.config(text="请配置激活参数")
            
    def clear_config(self):
        """清除所有配置"""
        self.version_selector.clear()
        self.kms_panel.clear()
        self.update_config_display()
        
    def start_activation(self):
        """开始激活流程"""
        try:
            # 获取配置
            version_config = self.version_selector.get_config_dict()
            kms_config = self.kms_panel.get_config_dict()
            
            if not version_config or not kms_config:
                ErrorDialog.show(self.root, "配置不完整", "请先完成所有必要配置")
                return
                
            # 创建激活面板
            activation_panel = ActivationPanel(self.root)
            activation_panel.start_activation(version_config, kms_config)
            
        except Exception as e:
            ErrorDialog.show(self.root, "激活错误", str(e))
            
    def run(self):
        """运行应用"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
"""
应用样式模块
"""

import tkinter as tk
from tkinter import ttk


class AppStyles:
    """应用样式管理器"""
    
    def __init__(self):
        self.style = ttk.Style()
        self.setup_styles()
        
    def setup_styles(self):
        """设置应用样式"""
        # 主题设置
        try:
            self.style.theme_use('clam')
        except:
            pass
            
        # 字体设置
        self.setup_fonts()
        self.setup_colors()
        self.setup_component_styles()
        
    def setup_fonts(self):
        """设置字体"""
        self.default_font = ('Microsoft YaHei', 9)
        self.title_font = ('Microsoft YaHei', 14, 'bold')
        self.subtitle_font = ('Microsoft YaHei', 10)
        self.header_font = ('Microsoft YaHei', 12, 'bold')
        
    def setup_colors(self):
        """设置颜色"""
        self.primary_color = '#2c3e50'  # 深蓝色
        self.secondary_color = '#7f8c8d'  # 灰色
        self.success_color = '#27ae60'  # 绿色
        self.error_color = '#e74c3c'  # 红色
        self.warning_color = '#f39c12'  # 橙色
        self.info_color = '#3498db'  # 蓝色
        self.background_color = '#f8f9fa'  # 浅灰色背景
        
    def setup_component_styles(self):
        """设置组件样式"""
        # 框架样式
        self.style.configure(
            'Header.TFrame',
            background=self.background_color
        )
        
        self.style.configure(
            'Content.TFrame',
            background=self.background_color
        )
        
        self.style.configure(
            'Action.TFrame',
            background=self.background_color
        )
        
        # 标签样式
        self.style.configure(
            'HeaderTitle.TLabel',
            font=self.title_font,
            foreground=self.primary_color,
            background=self.background_color
        )
        
        self.style.configure(
            'HeaderSubtitle.TLabel',
            font=self.subtitle_font,
            foreground=self.secondary_color,
            background=self.background_color
        )
        
        self.style.configure(
            'ConfigDisplay.TLabel',
            font=self.default_font,
            foreground=self.primary_color,
            background=self.background_color,
            relief='solid',
            borderwidth=1,
            padding=5
        )
        
        # 按钮样式
        self.style.configure(
            'Action.TButton',
            font=self.default_font,
            padding=10
        )
        
        # 输入框样式
        self.style.configure(
            'TCombobox',
            font=self.default_font
        )
        
        self.style.configure(
            'TEntry',
            font=self.default_font
        )
        
        # LabelFrame样式
        self.style.configure(
            'TLabelframe',
            background=self.background_color
        )
        
        self.style.configure(
            'TLabelframe.Label',
            font=self.header_font,
            foreground=self.primary_color,
            background=self.background_color
        )
        
        # 进度条样式
        self.style.configure(
            'Horizontal.TProgressbar',
            background=self.success_color
        )
        
    def get_style(self, style_name):
        """获取样式"""
        return self.style.lookup(style_name, 'background')
        
    def update_style(self, component, style_name):
        """更新组件样式"""
        component.configure(style=style_name)
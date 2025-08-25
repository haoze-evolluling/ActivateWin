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
        """设置颜色 - 初音未来主题"""
        self.primary_color = '#00a0e9'  # 初音未来蓝（主色调）
        self.secondary_color = '#0085c7'  # 深一点的初音蓝
        self.success_color = '#00c300'  # 初音绿（辅助色）
        self.error_color = '#ff6b6b'  # 柔和的红色
        self.warning_color = '#ffa500'  # 橙色
        self.info_color = '#00d4ff'  # 浅蓝色
        self.background_color = '#e6f7ff'  # 初音蓝浅背景色
        self.accent_color = '#69c2ff'  # 点缀色
        self.light_blue = '#b3e0ff'  # 更浅的蓝色
        
    def setup_component_styles(self):
        """设置组件样式 - 初音未来主题"""
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
            background=self.light_blue,
            relief='solid',
            borderwidth=1,
            padding=8
        )
        
        # 按钮样式 - 初音未来主题按钮
        self.style.configure(
            'Action.TButton',
            font=self.default_font,
            foreground='white',
            background=self.primary_color,
            padding=10,
            borderwidth=2,
            relief='raised'
        )
        
        # 鼠标悬停效果
        self.style.map(
            'Action.TButton',
            background=[('active', self.secondary_color), ('pressed', self.info_color)]
        )
        
        # 初音未来主题进度条样式
        self.style.configure(
            'Miku.Horizontal.TProgressbar',
            background=self.primary_color,
            troughcolor=self.light_blue,
            borderwidth=1,
            lightcolor=self.accent_color,
            darkcolor=self.primary_color
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
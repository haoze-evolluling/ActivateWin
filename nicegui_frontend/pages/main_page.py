"""
主页面组件
提供应用的主要功能和导航
"""

from nicegui import ui
from typing import Optional
import os
from pathlib import Path

class MainPage:
    """主页面类"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        
    def create_header(self):
        """创建页面头部"""
        with ui.header().classes('bg-primary text-white shadow-lg'):
            with ui.row().classes('w-full items-center justify-between'):
                ui.label('KMS激活管理器').classes('text-h4')
                
                with ui.row().classes('items-center'):
                    ui.button('主页', on_click=lambda: ui.navigate.to('/')).props('flat')
                    ui.button('激活管理', on_click=lambda: ui.navigate.to('/activation')).props('flat')
                    ui.button('设置', on_click=lambda: ui.navigate.to('/settings')).props('flat')
                    
    def create_welcome_section(self):
        """创建欢迎区域"""
        with ui.card().classes('w-full q-pa-md'):
            ui.label('欢迎使用KMS激活管理器').classes('text-h5 text-center')
            ui.label('基于NiceGUI开发的现代化激活管理工具').classes('text-subtitle1 text-center q-mt-sm')
            
            with ui.row().classes('justify-center q-mt-md'):
                ui.button('开始激活', on_click=lambda: ui.navigate.to('/activation')).props('color=primary size=lg')
                
    def create_features_section(self):
        """创建功能特性区域"""
        with ui.card().classes('w-full q-pa-md q-mt-md'):
            ui.label('主要功能').classes('text-h6')
            
            features = [
                ('Windows激活', '支持Windows 10/11各版本激活'),
                ('Office激活', '支持Office 2016/2019/2021激活'),
                ('KMS服务器管理', '内置KMS服务器状态监控'),
                ('一键操作', '简化激活流程，一键完成')
            ]
            
            with ui.grid(columns=2).classes('q-gutter-md q-mt-sm'):
                for title, description in features:
                    with ui.card().classes('q-pa-sm'):
                        ui.label(title).classes('text-subtitle2')
                        ui.label(description).classes('text-caption')
                        
    def create_footer(self):
        """创建页脚"""
        with ui.footer().classes('bg-grey-8 text-white'):
            ui.label('KMS激活管理器 v2.0.0 - 基于NiceGUI开发').classes('text-center')

def create_main_page():
    """创建主页面"""
    page = MainPage()
    
    # 设置页面背景
    ui.colors(primary='#1976D2', secondary='#424242', accent='#82B1FF')
    
    # 创建页面内容
    page.create_header()
    
    with ui.column().classes('q-pa-md q-gutter-md'):
        page.create_welcome_section()
        page.create_features_section()
        
    page.create_footer()
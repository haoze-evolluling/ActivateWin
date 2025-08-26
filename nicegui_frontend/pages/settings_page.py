"""
设置页面组件
提供应用配置和主题设置功能
"""

from nicegui import ui
import os
from pathlib import Path

class SettingsPage:
    """设置页面类"""
    
    def __init__(self):
        self.settings = {
            'theme': 'light',
            'language': 'zh-CN',
            'auto_check': True,
            'debug_mode': False
        }
        
    def create_header(self):
        """创建页面头部"""
        with ui.header().classes('bg-primary text-white shadow-lg'):
            with ui.row().classes('w-full items-center justify-between'):
                ui.label('设置').classes('text-h4')
                
                with ui.row().classes('items-center'):
                    ui.button('返回主页', on_click=lambda: ui.navigate.to('/')).props('flat')
                    ui.button('激活管理', on_click=lambda: ui.navigate.to('/activation')).props('flat')
                    
    def create_appearance_settings(self):
        """创建外观设置区域"""
        with ui.card().classes('w-full q-pa-md'):
            ui.label('外观设置').classes('text-h6')
            
            with ui.column().classes('q-gutter-md q-mt-sm'):
                # 主题选择
                theme_select = ui.select(
                    ['light', 'dark', 'auto'],
                    label='主题模式',
                    value=self.settings['theme']
                ).classes('w-full')
                
                # 语言选择
                language_select = ui.select(
                    ['zh-CN', 'en-US'],
                    label='界面语言',
                    value=self.settings['language']
                ).classes('w-full')
                
                # 保存按钮
                ui.button(
                    '保存外观设置',
                    on_click=lambda: self.save_appearance_settings(
                        theme_select.value,
                        language_select.value
                    )
                ).props('color=primary')
                
    def create_function_settings(self):
        """创建功能设置区域"""
        with ui.card().classes('w-full q-pa-md'):
            ui.label('功能设置').classes('text-h6')
            
            with ui.column().classes('q-gutter-md q-mt-sm'):
                # 自动检查更新
                auto_check_switch = ui.switch(
                    '自动检查更新',
                    value=self.settings['auto_check']
                ).classes('w-full')
                
                # 调试模式
                debug_switch = ui.switch(
                    '调试模式',
                    value=self.settings['debug_mode']
                ).classes('w-full')
                
                # 保存按钮
                ui.button(
                    '保存功能设置',
                    on_click=lambda: self.save_function_settings(
                        auto_check_switch.value,
                        debug_switch.value
                    )
                ).props('color=primary')
                
    def create_system_info(self):
        """创建系统信息区域"""
        with ui.card().classes('w-full q-pa-md'):
            ui.label('系统信息').classes('text-h6')
            
            with ui.column().classes('q-gutter-sm q-mt-sm'):
                ui.label(f'应用版本: v2.0.0').classes('text-body2')
                ui.label(f'NiceGUI版本: 最新版').classes('text-body2')
                ui.label(f'Python版本: {os.sys.version.split()[0]}').classes('text-body2')
                ui.label(f'操作系统: {os.name}').classes('text-body2')
                
    def create_actions(self):
        """创建操作按钮区域"""
        with ui.card().classes('w-full q-pa-md'):
            ui.label('其他操作').classes('text-h6')
            
            with ui.row().classes('q-gutter-md q-mt-sm'):
                ui.button(
                    '重置所有设置',
                    on_click=self.reset_settings
                ).props('color=negative')
                
                ui.button(
                    '检查更新',
                    on_click=self.check_updates
                ).props('color=info')
                
    def save_appearance_settings(self, theme: str, language: str):
        """保存外观设置"""
        self.settings['theme'] = theme
        self.settings['language'] = language
        
        # 应用主题更改
        if theme == 'dark':
            ui.dark_mode().enable()
        elif theme == 'light':
            ui.dark_mode().disable()
        else:
            # auto模式
            ui.dark_mode().auto()
            
        ui.notify('外观设置已保存', type='positive')
        
    def save_function_settings(self, auto_check: bool, debug_mode: bool):
        """保存功能设置"""
        self.settings['auto_check'] = auto_check
        self.settings['debug_mode'] = debug_mode
        ui.notify('功能设置已保存', type='positive')
        
    def reset_settings(self):
        """重置所有设置"""
        self.settings = {
            'theme': 'light',
            'language': 'zh-CN',
            'auto_check': True,
            'debug_mode': False
        }
        ui.notify('所有设置已重置为默认值', type='info')
        
    def check_updates(self):
        """检查更新"""
        ui.notify('正在检查更新...', type='info')
        # 这里可以添加实际的更新检查逻辑
        
def create_settings_page():
    """创建设置页面"""
    page = SettingsPage()
    
    # 设置页面背景
    ui.colors(primary='#1976D2', secondary='#424242', accent='#82B1FF')
    
    # 创建页面内容
    page.create_header()
    
    with ui.column().classes('q-pa-md q-gutter-md'):
        page.create_appearance_settings()
        page.create_function_settings()
        page.create_system_info()
        page.create_actions()
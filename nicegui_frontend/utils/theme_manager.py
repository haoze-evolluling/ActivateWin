"""
主题管理器
提供主题切换和管理功能
"""

from nicegui import ui
from typing import Optional
import json
from pathlib import Path

class ThemeManager:
    """主题管理器类"""
    
    def __init__(self):
        self.config_file = Path(__file__).parent.parent / 'config' / 'theme.json'
        self.current_theme = self.load_theme()
        
    def load_theme(self) -> dict:
        """加载主题配置"""
        default_theme = {
            'mode': 'light',
            'primary_color': '#1976D2',
            'secondary_color': '#424242',
            'accent_color': '#82B1FF'
        }
        
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
            
        return default_theme
        
    def save_theme(self, theme_config: dict):
        """保存主题配置"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(theme_config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存主题配置失败: {e}")
            
    def apply_theme(self, theme_mode: str):
        """应用主题"""
        if theme_mode == 'dark':
            ui.dark_mode().enable()
        elif theme_mode == 'light':
            ui.dark_mode().disable()
        else:
            ui.dark_mode().auto()
            
        self.current_theme['mode'] = theme_mode
        self.save_theme(self.current_theme)
        
    def get_theme_colors(self) -> dict:
        """获取主题颜色"""
        return {
            'primary': self.current_theme.get('primary_color', '#1976D2'),
            'secondary': self.current_theme.get('secondary_color', '#424242'),
            'accent': self.current_theme.get('accent_color', '#82B1FF')
        }
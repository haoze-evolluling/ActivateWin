#!/usr/bin/env python3
"""
NiceGUI KMS激活管理器主应用
使用NiceGUI框架开发的全新用户界面
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from nicegui import ui, app
from pages.main_page import create_main_page
from pages.activation_page import create_activation_page
from pages.settings_page import create_settings_page
from utils.theme_manager import ThemeManager
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KMSActivationApp:
    """KMS激活管理器主应用类"""
    
    def __init__(self):
        self.theme_manager = ThemeManager()
        self.setup_app()
        self.setup_routes()
        
    def setup_app(self):
        """配置应用基础设置"""
        app.title = 'KMS激活管理器'
        app.version = '2.0.0'
        
        # 设置应用图标
        icon_path = project_root / 'icon.png'
        if icon_path.exists():
            app.add_static_files('/static', str(project_root))
            
    def setup_routes(self):
        """配置页面路由"""
        # 主页
        @ui.page('/')
        def main_page():
            create_main_page()
            
        # 激活页面
        @ui.page('/activation')
        def activation_page():
            create_activation_page()
            
        # 设置页面
        @ui.page('/settings')
        def settings_page():
            create_settings_page()
            
    def run(self):
        """运行应用"""
        logger.info("启动NiceGUI KMS激活管理器...")
        ui.run(
            title='KMS激活管理器',
            port=8080,
            reload=False,
            show=True,
            storage_secret='kms-activation-secret-key'
        )

if __name__ == '__main__':
    app_instance = KMSActivationApp()
    app_instance.run()
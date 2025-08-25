"""
UI管理器 - 封装主窗口
"""

from frontend.main_window import MainWindow


class UIManager:
    """UI管理器类 - 封装主窗口管理"""
    
    def __init__(self):
        """初始化UI管理器"""
        self.main_window = None
        
    def run(self):
        """运行应用程序"""
        self.main_window = MainWindow()
        self.main_window.run()
        
    def get_main_window(self):
        """获取主窗口实例"""
        return self.main_window
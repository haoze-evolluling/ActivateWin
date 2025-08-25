"""
Windows KMS激活管理器 - 前端模块
"""

from .main_window import MainWindow
from .components import VersionSelector, KMSServerPanel, ActivationPanel
from .dialogs import ErrorDialog, ConfirmDialog, InfoDialog

__all__ = [
    'MainWindow',
    'VersionSelector',
    'KMSServerPanel', 
    'ActivationPanel',
    'ErrorDialog',
    'ConfirmDialog',
    'InfoDialog'
]
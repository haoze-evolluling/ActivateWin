#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows KMS激活管理器 - UI启动脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frontend.main_window import MainWindow


def main():
    """主函数"""
    try:
        app = MainWindow()
        app.run()
    except Exception as e:
        input("按任意键退出...")


if __name__ == "__main__":
    main()
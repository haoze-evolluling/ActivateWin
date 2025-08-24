#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试脚本 - 捕获kms_activator.py的启动错误
"""

import sys
import traceback

try:
    # 添加当前目录到Python路径
    sys.path.insert(0, '.')
    
    # 导入并运行主程序
    from kms_activator import KMSActivator
    
    print("正在启动KMS激活器...")
    app = KMSActivator()
    print("程序启动成功!")
    app.root.mainloop()
    
except Exception as e:
    print(f"程序启动失败，错误信息:")
    print(f"错误类型: {type(e).__name__}")
    print(f"错误详情: {str(e)}")
    print("\n完整堆栈跟踪:")
    traceback.print_exc()
    
    # 等待用户输入以便查看错误信息
    input("\n按回车键退出...")
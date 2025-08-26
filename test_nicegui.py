#!/usr/bin/env python3
"""
NiceGUI KMS激活管理器测试文件
用于验证新的NiceGUI界面功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """测试模块导入"""
    try:
        from nicegui_frontend.main import KMSActivationApp
        from nicegui_frontend.pages.main_page import create_main_page
        from nicegui_frontend.pages.activation_page import create_activation_page
        from nicegui_frontend.pages.settings_page import create_settings_page
        from nicegui_frontend.utils.theme_manager import ThemeManager
        from backend.kms_service import KMSService
        
        print("✅ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def test_kms_service():
    """测试KMS服务"""
    try:
        from backend.kms_service import KMSService
        service = KMSService()
        print("✅ KMS服务初始化成功")
        return True
    except Exception as e:
        print(f"❌ KMS服务初始化失败: {e}")
        return False

def main():
    """运行测试"""
    print("正在测试NiceGUI KMS激活管理器...")
    print("-" * 50)
    
    tests = [
        test_imports,
        test_kms_service
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("-" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("✅ 所有测试通过！可以启动NiceGUI应用")
        print("运行命令: python nicegui_frontend/main.py")
    else:
        print("❌ 部分测试失败，请检查错误信息")

if __name__ == '__main__':
    main()
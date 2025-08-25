#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试激活功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.kms_service import KMSService
from models.activation_data import ActivationConfig

def test_activation_service():
    """测试激活服务"""
    # 创建测试配置
    config = ActivationConfig(
        windows_version="Windows 10",
        edition="专业版",
        product_key="W269N-WFGWX-YVC9B-4J6C9-T83GX",
        kms_server="kms.bige0.com"
    )
    
    # 创建服务实例
    service = KMSService()
    
    # 添加回调
    def callback(event_type, data):
        pass  # 静默处理回调
    
    service.add_activation_callback(callback)
    
    # 测试服务器连接
    server_status = service.test_server_connection("kms.bige0.com")
    
    # 注意：实际激活需要管理员权限，这里只测试服务初始化
    return server_status

if __name__ == "__main__":
    result = test_activation_service()
    exit(0 if result.is_available else 1)
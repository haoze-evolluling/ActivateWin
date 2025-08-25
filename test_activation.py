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
    print("🧪 测试KMS激活服务...")
    
    # 创建测试配置
    config = ActivationConfig(
        windows_version="Windows 10",
        edition="专业版",
        product_key="W269N-WFGWX-YVC9B-4J6C9-T83GX",
        kms_server="kms.bige0.com"
    )
    
    print(f"配置: {config}")
    
    # 创建服务实例
    service = KMSService()
    
    # 添加回调
    def callback(event_type, data):
        print(f"📡 回调: {event_type} - {data}")
    
    service.add_activation_callback(callback)
    
    # 测试服务器连接
    print("🔍 测试服务器连接...")
    server_status = service.test_server_connection("kms.bige0.com")
    print(f"服务器状态: {server_status}")
    
    # 注意：实际激活需要管理员权限，这里只测试服务初始化
    print("✅ 服务测试完成")

if __name__ == "__main__":
    test_activation_service()
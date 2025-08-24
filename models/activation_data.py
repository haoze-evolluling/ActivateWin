#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据模型定义
定义激活相关的数据结构和配置
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ActivationConfig:
    """激活配置数据类"""
    windows_version: str
    edition: str
    product_key: str
    kms_server: str


@dataclass
class ServerStatus:
    """服务器状态数据类"""
    server: str
    is_available: bool
    response_time: Optional[int] = None
    error_message: Optional[str] = None


class ActivationData:
    """激活数据管理类"""
    
    def __init__(self):
        self.windows_versions = self._load_windows_versions()
        self.kms_servers = self._load_kms_servers()
        
    def _load_windows_versions(self) -> Dict[str, Dict[str, str]]:
        """加载Windows版本和密钥数据"""
        return {
            "Windows 11": {
                "专业版": "VK7JG-NPHTM-C97JM-9MPGT-3V66T",
                "企业版": "XGVPP-NMH47-7TTHJ-W3FW7-8HV2C",
                "教育版": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
                "专业工作站版": "NRG8B-VKK3Q-CXVCJ-9G2XF-6Q84J"
            },
            "Windows 10": {
                "专业版": "W269N-WFGWX-YVC9B-4J6C9-T83GX",
                "企业版": "NPPR9-FWDCX-D2C8J-H872K-2YT43",
                "教育版": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
                "专业工作站版": "NRG8B-VKK3Q-CXVCJ-9G2XF-6Q84J"
            },
            "Windows Server 2022": {
                "标准版": "VDYBN-27WPP-V4HQT-9VMD4-VMK7H",
                "数据中心版": "WX4NM-KYWYW-QJJR4-XV3QB-6VM33"
            },
            "Windows Server 2019": {
                "标准版": "N69G4-B89J2-4G8F4-WWYCC-J464C",
                "数据中心版": "WMDGN-G9PQG-XVVXX-R3X43-63DFG"
            }
        }
    
    def _load_kms_servers(self) -> List[str]:
        """加载KMS服务器列表"""
        try:
            import os
            server_file = "kmsserver.md"
            if os.path.exists(server_file):
                with open(server_file, "r", encoding="utf-8") as f:
                    servers = f.read().strip().split('\n')
                    return [s.strip() for s in servers if s.strip()]
        except Exception:
            pass
            
        # 默认服务器列表
        return [
            "kms.bige0.com",
            "kms.03k.org", 
            "kms.wxlost.com",
            "kms.moeyuuko.top",
            "kms.loli.best",
            "kms.loli.beer",
            "kms.cgtsoft.com",
            "kms.sixyin.com",
            "kms.litbear.cn"
        ]
    
    def get_editions(self, windows_version: str) -> List[str]:
        """获取指定Windows版本的所有版本"""
        if windows_version in self.windows_versions:
            return list(self.windows_versions[windows_version].keys())
        return []
    
    def get_product_key(self, windows_version: str, edition: str) -> Optional[str]:
        """获取产品密钥"""
        if windows_version in self.windows_versions and edition in self.windows_versions[windows_version]:
            return self.windows_versions[windows_version][edition]
        return None
    
    def get_all_windows_versions(self) -> List[str]:
        """获取所有Windows版本"""
        return list(self.windows_versions.keys())
    
    def get_all_kms_servers(self) -> List[str]:
        """获取所有KMS服务器"""
        return self.kms_servers
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
                "专业版": "W269N-WFGWX-YVC9B-4J6C9-T83GX",
                "专业工作站版": "NRG8B-VKK3Q-CXVCJ-9G2XF-6Q84J",
                "专业教育版": "6TP4R-GNPTD-KYYHQ-7B7DP-J447Y",
                "教育版": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
                "企业版": "NPPR9-FWDCX-D2C8J-H872K-2YT43",
                "企业版 G": "YYVX9-NTFWV-6MDM3-9PT4T-4M68B",
                "企业版 LTSC 2024": "M7XTQ-FN8P6-TTKYV-9D4CC-J462D"
            },
            "Windows 10": {
                "专业版": "W269N-WFGWX-YVC9B-4J6C9-T83GX",
                "专业工作站版": "NRG8B-VKK3Q-CXVCJ-9G2XF-6Q84J",
                "专业教育版": "6TP4R-GNPTD-KYYHQ-7B7DP-J447Y",
                "教育版": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
                "企业版": "NPPR9-FWDCX-D2C8J-H872K-2YT43",
                "企业版 G": "YYVX9-NTFWV-6MDM3-9PT4T-4M68B",
                "企业版 LTSC 2019": "M7XTQ-FN8P6-TTKYV-9D4CC-J462D",
                "企业版 LTSB 2016": "DCPHK-NFMTC-H88MJ-PFHPY-QJ4BJ"
            },
            "Windows 8.1": {
                "专业版": "GCRJD-8NW9H-F2CDX-CCM8D-9D6T9",
                "企业版": "MHF9N-XY6XB-WVXMC-BTDCT-MKKG7"
            },
            "Windows 8": {
                "专业版": "NG4HW-VH26C-733KW-K6F98-J8CK4",
                "企业版": "32JNW-9KQ84-P47T8-D8GGY-CWCK7"
            },
            "Windows 7": {
                "专业版": "FJ82H-XT6CR-J8D7P-XQJJ2-GPDD4",
                "企业版": "33PXH-7Y6KF-2VJC9-XBBR8-HVTHH"
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
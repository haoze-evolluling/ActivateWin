#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KMS激活服务层
处理所有与激活相关的业务逻辑
"""

import subprocess
import os
import sys
from typing import Optional, Tuple
from models.activation_data import ActivationConfig, ServerStatus


class KMSService:
    """KMS激活服务类"""
    
    def __init__(self):
        self.activation_callbacks = []
        
    def add_activation_callback(self, callback):
        """添加激活过程回调"""
        self.activation_callbacks.append(callback)
        
    def _notify_callbacks(self, event_type: str, data: dict):
        """通知回调函数"""
        for callback in self.activation_callbacks:
            try:
                callback(event_type, data)
            except Exception as e:
                print(f"回调函数执行错误: {e}")
                
    def test_server_connection(self, server: str) -> ServerStatus:
        """测试KMS服务器连接"""
        try:
            # 使用ping命令测试服务器可用性
            result = subprocess.run(
                ["ping", "-n", "2", "-w", "1000", server], 
                capture_output=True, 
                text=True, 
                timeout=3
            )
            
            if result.returncode == 0:
                # 解析响应时间
                response_times = []
                for line in result.stdout.split('\n'):
                    if '时间=' in line or 'time=' in line:
                        try:
                            time_part = line.split('=')[-1].split('ms')[0].strip()
                            response_times.append(int(time_part))
                        except:
                            pass
                
                avg_time = sum(response_times) // len(response_times) if response_times else None
                return ServerStatus(
                    server=server,
                    is_available=True,
                    response_time=avg_time
                )
            else:
                # 分析失败原因
                error_msg = "连接失败"
                if "找不到主机" in result.stderr or "无法解析" in result.stderr:
                    error_msg = "DNS解析失败"
                elif "请求超时" in result.stdout or "Request timed out" in result.stdout:
                    error_msg = "请求超时"
                elif "目标主机无法访问" in result.stderr:
                    error_msg = "目标主机无法访问"
                    
                return ServerStatus(
                    server=server,
                    is_available=False,
                    error_message=error_message
                )
                
        except subprocess.TimeoutExpired:
            return ServerStatus(
                server=server,
                is_available=False,
                error_message="测试超时（超过3秒）"
            )
        except FileNotFoundError:
            return ServerStatus(
                server=server,
                is_available=False,
                error_message="系统缺少ping命令工具"
            )
        except Exception as e:
            return ServerStatus(
                server=server,
                is_available=False,
                error_message=str(e)
            )
    
    def execute_activation(self, config: ActivationConfig) -> Tuple[bool, str]:
        """执行激活流程"""
        try:
            self._notify_callbacks("activation_start", {"config": config})
            
            # 步骤1：安装产品密钥
            self._notify_callbacks("step_start", {"step": 1, "description": "安装产品密钥"})
            result = subprocess.run(
                ["slmgr", "/ipk", config.product_key], 
                capture_output=True, 
                text=True,
                check=True
            )
            self._notify_callbacks("step_complete", {"step": 1})
            
            # 步骤2：设置KMS服务器
            self._notify_callbacks("step_start", {"step": 2, "description": "设置KMS服务器"})
            result = subprocess.run(
                ["slmgr", "/skms", config.kms_server], 
                capture_output=True, 
                text=True,
                check=True
            )
            self._notify_callbacks("step_complete", {"step": 2})
            
            # 步骤3：执行激活
            self._notify_callbacks("step_start", {"step": 3, "description": "执行激活"})
            result = subprocess.run(
                ["slmgr", "/ato"], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                self._notify_callbacks("activation_complete", {"success": True})
                return True, "Windows激活成功！"
            else:
                error_msg = result.stderr if result.stderr else "激活失败"
                self._notify_callbacks("activation_complete", {"success": False, "error": error_msg})
                return False, f"激活失败: {error_msg}"
                
        except subprocess.CalledProcessError as e:
            error_msg = f"命令执行失败: {str(e)}"
            self._notify_callbacks("activation_complete", {"success": False, "error": error_msg})
            return False, error_msg
        except Exception as e:
            error_msg = f"发生未知错误: {str(e)}"
            self._notify_callbacks("activation_complete", {"success": False, "error": error_msg})
            return False, error_msg
    
    def check_admin_privileges(self) -> bool:
        """检查是否具有管理员权限"""
        try:
            if os.name == 'nt':
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            return os.getuid() == 0
        except:
            return False
    
    def get_system_info(self) -> dict:
        """获取系统信息"""
        try:
            import platform
            import subprocess
            
            # 获取Windows版本信息
            result = subprocess.run(
                ["systeminfo"], 
                capture_output=True, 
                text=True,
                encoding='gbk' if os.name == 'nt' else 'utf-8'
            )
            
            system_info = {
                "platform": platform.platform(),
                "architecture": platform.architecture(),
                "processor": platform.processor(),
                "python_version": platform.python_version()
            }
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if "OS 名称:" in line or "OS Name:" in line:
                        system_info["os_name"] = line.split(':')[1].strip()
                    elif "OS 版本:" in line or "OS Version:" in line:
                        system_info["os_version"] = line.split(':')[1].strip()
            
            return system_info
            
        except Exception as e:
            return {
                "platform": platform.platform(),
                "architecture": platform.architecture(),
                "processor": platform.processor(),
                "python_version": platform.python_version(),
                "error": str(e)
            }
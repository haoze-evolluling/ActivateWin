#!/usr/bin/env python3
# -*- coding: utf-8 */
"""
KMS服务管理器
处理KMS激活相关的核心业务逻辑
"""

import subprocess
import socket
import time
from typing import Optional, Callable, List
from models.activation_data import ActivationConfig, ServerStatus


class KMSService:
    """KMS服务管理器"""
    
    def __init__(self):
        self.callbacks: List[Callable] = []
        
    def add_activation_callback(self, callback: Callable):
        """添加激活过程回调"""
        self.callbacks.append(callback)
        
    def _notify_callbacks(self, event_type: str, data: dict):
        """通知所有回调"""
        for callback in self.callbacks:
            try:
                callback(event_type, data)
            except Exception as e:
                pass
                
    @staticmethod
    def test_server_connection(server: str) -> ServerStatus:
        """测试KMS服务器连接"""
        try:
            # 解析服务器地址和端口
            if ':' in server:
                host, port = server.split(':', 1)
                port = int(port)
            else:
                host = server
                port = 1688  # KMS默认端口
                
            # 测试TCP连接
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)  # 3秒超时
            
            try:
                result = sock.connect_ex((host, port))
                response_time = int((time.time() - start_time) * 1000)
                sock.close()
                
                if result == 0:
                    return ServerStatus(
                        server=server,
                        is_available=True,
                        response_time=response_time
                    )
                else:
                    return ServerStatus(
                        server=server,
                        is_available=False,
                        error_message=f"连接被拒绝 ({result})"
                    )
            except socket.timeout:
                return ServerStatus(
                    server=server,
                    is_available=False,
                    error_message="连接超时"
                )
            except socket.gaierror:
                return ServerStatus(
                    server=server,
                    is_available=False,
                    error_message="无法解析域名"
                )
            except Exception as e:
                return ServerStatus(
                    server=server,
                    is_available=False,
                    error_message=str(e)
                )
                
        except Exception as e:
            return ServerStatus(
                server=server,
                is_available=False,
                error_message=f"测试失败: {str(e)}"
            )
            
    def execute_activation(self, config: ActivationConfig) -> tuple[bool, str]:
        """执行激活操作"""
        try:
            self._notify_callbacks("activation_start", {})
            
            # 步骤1: 安装产品密钥
            self._notify_callbacks("step_start", {"step": 1, "description": "安装产品密钥"})
            success, message = self._install_product_key(config.product_key)
            if not success:
                self._notify_callbacks("activation_complete", {"success": False, "error": message})
                return False, f"安装产品密钥失败: {message}"
            self._notify_callbacks("step_complete", {"step": 1})
            
            # 步骤2: 设置KMS服务器
            self._notify_callbacks("step_start", {"step": 2, "description": "设置KMS服务器"})
            success, message = self._set_kms_server(config.kms_server)
            if not success:
                self._notify_callbacks("activation_complete", {"success": False, "error": message})
                return False, f"设置KMS服务器失败: {message}"
            self._notify_callbacks("step_complete", {"step": 2})
            
            # 步骤3: 激活Windows
            self._notify_callbacks("step_start", {"step": 3, "description": "激活Windows"})
            success, message = self._activate_windows()
            if not success:
                self._notify_callbacks("activation_complete", {"success": False, "error": message})
                return False, f"激活失败: {message}"
            self._notify_callbacks("step_complete", {"step": 3})
            
            self._notify_callbacks("activation_complete", {"success": True})
            return True, "激活成功！Windows已成功激活。"
            
        except Exception as e:
            error_msg = f"激活过程发生错误: {str(e)}"
            self._notify_callbacks("activation_complete", {"success": False, "error": error_msg})
            return False, error_msg
            
    def _install_product_key(self, product_key: str) -> tuple[bool, str]:
        """安装产品密钥"""
        try:
            cmd = f"slmgr /ipk {product_key}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, "产品密钥安装成功"
            else:
                error_msg = result.stderr.strip() if result.stderr else "未知错误"
                return False, error_msg
                
        except Exception as e:
            return False, str(e)
            
    def _set_kms_server(self, kms_server: str) -> tuple[bool, str]:
        """设置KMS服务器"""
        try:
            cmd = f"slmgr /skms {kms_server}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, "KMS服务器设置成功"
            else:
                error_msg = result.stderr.strip() if result.stderr else "未知错误"
                return False, error_msg
                
        except Exception as e:
            return False, str(e)
            
    def _activate_windows(self) -> tuple[bool, str]:
        """激活Windows"""
        try:
            cmd = "slmgr /ato"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, "Windows激活成功"
            else:
                error_msg = result.stderr.strip() if result.stderr else "未知错误"
                return False, error_msg
                
        except Exception as e:
            return False, str(e)
            
    def get_activation_info(self) -> dict:
        """获取当前激活信息"""
        try:
            cmd = "slmgr /dlv"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "details": result.stdout
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
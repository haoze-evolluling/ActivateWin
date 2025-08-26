#!/usr/bin/env python3
"""
工具模块
提供各种辅助功能
"""

import socket
import threading
import time
import json
import os
import hashlib
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class NetworkUtils:
    """网络工具类"""
    
    @staticmethod
    def test_port(host, port, timeout=5):
        """测试端口连通性"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception as e:
            logger.error(f"端口测试失败: {e}")
            return False
    
    @staticmethod
    def ping_host(host, timeout=3):
        """Ping主机"""
        try:
            import subprocess
            result = subprocess.run(
                ['ping', '-n', '1', '-w', str(timeout * 1000), host],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Ping测试失败: {e}")
            return False
    
    @staticmethod
    def get_local_ip():
        """获取本地IP地址"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            ip = sock.getsockname()[0]
            sock.close()
            return ip
        except Exception:
            return "127.0.0.1"

class FileUtils:
    """文件工具类"""
    
    @staticmethod
    def ensure_dir(directory):
        """确保目录存在"""
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    @staticmethod
    def read_json_file(filepath, default=None):
        """读取JSON文件"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return default or {}
        except Exception as e:
            logger.error(f"读取JSON文件失败: {e}")
            return default or {}
    
    @staticmethod
    def write_json_file(filepath, data):
        """写入JSON文件"""
        try:
            FileUtils.ensure_dir(os.path.dirname(filepath))
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"写入JSON文件失败: {e}")
            return False
    
    @staticmethod
    def get_file_hash(filepath):
        """获取文件哈希值"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return None

class SystemUtils:
    """系统工具类"""
    
    @staticmethod
    def is_admin():
        """检查是否具有管理员权限"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    @staticmethod
    def get_system_info():
        """获取系统信息"""
        try:
            import platform
            import psutil
            
            info = {
                'platform': platform.platform(),
                'architecture': platform.architecture(),
                'processor': platform.processor(),
                'hostname': socket.gethostname(),
                'python_version': platform.python_version(),
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat(),
                'memory': {
                    'total': psutil.virtual_memory().total,
                    'available': psutil.virtual_memory().available,
                    'percent': psutil.virtual_memory().percent
                },
                'cpu': {
                    'count': psutil.cpu_count(),
                    'percent': psutil.cpu_percent(interval=1)
                }
            }
            return info
        except Exception as e:
            logger.error(f"获取系统信息失败: {e}")
            return {}

class ProgressTracker:
    """进度跟踪器"""
    
    def __init__(self, total_steps=100):
        self.total_steps = total_steps
        self.current_step = 0
        self.is_running = False
        self.callbacks = []
    
    def add_callback(self, callback):
        """添加进度回调"""
        self.callbacks.append(callback)
    
    def update(self, step, message=""):
        """更新进度"""
        self.current_step = min(step, self.total_steps)
        progress_data = {
            'current': self.current_step,
            'total': self.total_steps,
            'percent': (self.current_step / self.total_steps) * 100,
            'message': message
        }
        
        for callback in self.callbacks:
            try:
                callback(progress_data)
            except Exception as e:
                logger.error(f"进度回调失败: {e}")
    
    def start(self):
        """开始进度"""
        self.is_running = True
        self.current_step = 0
        self.update(0, "开始执行...")
    
    def finish(self, success=True, message=""):
        """完成进度"""
        self.is_running = False
        self.update(self.total_steps, message or ("执行成功" if success else "执行失败"))

class LoggerUtils:
    """日志工具类"""
    
    @staticmethod
    def setup_logger(name, level='INFO', log_file=None):
        """设置日志器"""
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
        
        if not logger.handlers:
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
            
            # 文件处理器
            if log_file:
                FileUtils.ensure_dir(os.path.dirname(log_file))
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
                )
                file_handler.setFormatter(file_formatter)
                logger.addHandler(file_handler)
        
        return logger

class ValidationUtils:
    """验证工具类"""
    
    @staticmethod
    def validate_product_key(key):
        """验证产品密钥格式"""
        if not key:
            return False
        
        # 移除空格和连字符
        key = key.replace('-', '').replace(' ', '').upper()
        
        # 检查长度
        if len(key) != 25:
            return False
        
        # 检查字符
        if not all(c in '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ' for c in key):
            return False
        
        return True
    
    @staticmethod
    def validate_kms_server(server):
        """验证KMS服务器地址"""
        if not server:
            return False
        
        # 检查是否为有效域名或IP
        try:
            socket.gethostbyname(server)
            return True
        except:
            return False
    
    @staticmethod
    def validate_port(port):
        """验证端口号"""
        try:
            port = int(port)
            return 1 <= port <= 65535
        except:
            return False
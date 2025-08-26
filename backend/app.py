#!/usr/bin/env python3
"""
ActivateWin Backend Service
Windows激活工具的Python后端服务
提供KMS激活、状态检查、密钥管理等功能
"""

import os
import json
import subprocess
import socket
import threading
import logging
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pythoncom
import win32com.client

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('activation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# KMS服务器列表
KMS_SERVERS = [
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

# Windows版本对应的GVLK密钥
GVLK_KEYS = {
    "win11_pro": "W269N-WFGWX-YVC9B-4J6C9-T83GX",
    "win11_pro_workstation": "NRG8B-VKK3Q-CXVCJ-9G2XF-6Q84J",
    "win11_pro_education": "6TP4R-GNPTD-KYYHQ-7B7DP-J447Y",
    "win11_education": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
    "win11_enterprise": "NPPR9-FWDCX-D2C8J-H872K-2YT43",
    "win11_enterprise_g": "YYVX9-NTFWV-6MDM3-9PT4T-4M68B",
    "win11_enterprise_ltsc": "M7XTQ-FN8P6-TTKYV-9D4CC-J462D",
    "win10_pro": "W269N-WFGWX-YVC9B-4J6C9-T83GX",
    "win10_pro_workstation": "NRG8B-VKK3Q-CXVCJ-9G2XF-6Q84J",
    "win10_pro_education": "6TP4R-GNPTD-KYYHQ-7B7DP-J447Y",
    "win10_education": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
    "win10_enterprise": "NPPR9-FWDCX-D2C8J-H872K-2YT43",
    "win10_enterprise_g": "YYVX9-NTFWV-6MDM3-9PT4T-4M68B",
    "win10_enterprise_ltsc_2019": "M7XTQ-FN8P6-TTKYV-9D4CC-J462D",
    "win10_enterprise_ltsb_2016": "DCPHK-NFMTC-H88MJ-PFHPY-QJ4BJ",
    "win8_1_pro": "GCRJD-8NW9H-F2CDX-CCM8D-9D6T9",
    "win8_1_enterprise": "MHF9N-XY6XB-WVXMC-BTDCT-MKKG7",
    "win8_pro": "NG4HW-VH26C-733KW-K6F98-J8CK4",
    "win8_enterprise": "32JNW-9KQ84-P47T8-D8GGY-CWCK7",
    "win7_pro": "FJ82H-XT6CR-J8D7P-XQJJ2-GPDD4",
    "win7_enterprise": "33PXH-7Y6KF-2VJC9-XBBR8-HVTHH"
}

app = Flask(__name__)
CORS(app)

class WindowsActivator:
    """Windows激活管理器"""
    
    def __init__(self):
        self.activation_history = []
        self.load_history()
    
    def load_history(self):
        """加载激活历史"""
        try:
            if os.path.exists('activation_history.json'):
                with open('activation_history.json', 'r', encoding='utf-8') as f:
                    self.activation_history = json.load(f)
        except Exception as e:
            logger.error(f"加载激活历史失败: {e}")
            self.activation_history = []
    
    def save_history(self):
        """保存激活历史"""
        try:
            with open('activation_history.json', 'w', encoding='utf-8') as f:
                json.dump(self.activation_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存激活历史失败: {e}")
    
    def run_command(self, command):
        """运行系统命令"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                encoding='utf-8'
            )
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except Exception as e:
            logger.error(f"命令执行失败: {command}, 错误: {e}")
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'returncode': -1
            }
    
    def check_windows_activation(self):
        """检查Windows激活状态"""
        try:
            # 使用SLMGR命令检查激活状态
            result = self.run_command('cscript slmgr.vbs /dli')
            
            if result['success']:
                output = result['stdout']
                
                # 解析激活信息
                is_activated = '已授权' in output or 'Licensed' in output
                
                # 提取产品ID
                product_id = "未知"
                for line in output.split('\n'):
                    if '产品密钥通道' in line or 'Product Key Channel' in line:
                        product_id = line.split(':')[-1].strip()
                        break
                
                # 提取许可证状态
                license_status = "未知"
                if '已授权' in output or 'Licensed' in output:
                    license_status = "已激活"
                elif '未授权' in output or 'Unlicensed' in output:
                    license_status = "未激活"
                elif '通知模式' in output or 'Notification' in output:
                    license_status = "通知模式"
                
                return {
                    'success': True,
                    'is_activated': is_activated,
                    'product_id': product_id,
                    'license_status': license_status,
                    'details': output
                }
            else:
                return {
                    'success': False,
                    'error': result['stderr']
                }
                
        except Exception as e:
            logger.error(f"检查激活状态失败: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def install_product_key(self, product_key):
        """安装产品密钥"""
        command = f'cscript slmgr.vbs /ipk {product_key}'
        return self.run_command(command)
    
    def set_kms_server(self, kms_server, port=1688):
        """设置KMS服务器"""
        command = f'cscript slmgr.vbs /skms {kms_server}:{port}'
        return self.run_command(command)
    
    def activate_windows(self):
        """激活Windows"""
        command = 'cscript slmgr.vbs /ato'
        return self.run_command(command)
    
    def clear_kms_server(self):
        """清除KMS服务器设置"""
        command = 'cscript slmgr.vbs /ckms'
        return self.run_command(command)
    
    def get_system_info(self):
        """获取系统信息"""
        try:
            # 获取Windows版本信息
            result = self.run_command('systeminfo | findstr /B /C:"OS 名称" /C:"OS 版本"')
            
            if result['success']:
                lines = result['stdout'].strip().split('\n')
                os_name = lines[0].split(':')[-1].strip() if len(lines) > 0 else "未知"
                os_version = lines[1].split(':')[-1].strip() if len(lines) > 1 else "未知"
                
                return {
                    'success': True,
                    'os_name': os_name,
                    'os_version': os_version
                }
            else:
                return {
                    'success': False,
                    'error': result['stderr']
                }
                
        except Exception as e:
            logger.error(f"获取系统信息失败: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def detect_windows_version(self):
        """检测Windows版本"""
        try:
            system_info = self.get_system_info()
            if system_info['success']:
                os_name = system_info['os_name'].lower()
                
                if 'windows 11' in os_name:
                    if 'pro' in os_name and 'workstation' in os_name:
                        return 'win11_pro_workstation'
                    elif 'pro' in os_name and 'education' in os_name:
                        return 'win11_pro_education'
                    elif 'pro' in os_name:
                        return 'win11_pro'
                    elif 'education' in os_name:
                        return 'win11_education'
                    elif 'enterprise' in os_name:
                        return 'win11_enterprise'
                elif 'windows 10' in os_name:
                    if 'pro' in os_name and 'workstation' in os_name:
                        return 'win10_pro_workstation'
                    elif 'pro' in os_name and 'education' in os_name:
                        return 'win10_pro_education'
                    elif 'pro' in os_name:
                        return 'win10_pro'
                    elif 'education' in os_name:
                        return 'win10_education'
                    elif 'enterprise' in os_name:
                        return 'win10_enterprise'
                elif 'windows 8.1' in os_name:
                    return 'win8_1_pro' if 'pro' in os_name else 'win8_1_enterprise'
                elif 'windows 8' in os_name:
                    return 'win8_pro' if 'pro' in os_name else 'win8_enterprise'
                elif 'windows 7' in os_name:
                    return 'win7_pro' if 'pro' in os_name else 'win7_enterprise'
            
            return 'unknown'
            
        except Exception as e:
            logger.error(f"检测Windows版本失败: {e}")
            return 'unknown'
    
    def test_kms_server(self, kms_server, port=1688):
        """测试KMS服务器连接"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((kms_server, port))
            sock.close()
            
            return {
                'success': result == 0,
                'message': '连接成功' if result == 0 else '连接失败'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def auto_activate(self, windows_version=None, kms_server=None):
        """自动激活Windows"""
        try:
            # 检测Windows版本
            if not windows_version:
                windows_version = self.detect_windows_version()
            
            if windows_version == 'unknown':
                return {
                    'success': False,
                    'error': '无法识别Windows版本'
                }
            
            # 获取对应的产品密钥
            if windows_version not in GVLK_KEYS:
                return {
                    'success': False,
                    'error': f'不支持的Windows版本: {windows_version}'
                }
            
            product_key = GVLK_KEYS[windows_version]
            
            # 选择KMS服务器
            if not kms_server:
                # 测试可用的KMS服务器
                for server in KMS_SERVERS:
                    test_result = self.test_kms_server(server)
                    if test_result['success']:
                        kms_server = server
                        break
                
                if not kms_server:
                    return {
                        'success': False,
                        'error': '所有KMS服务器都无法连接'
                    }
            
            # 执行激活步骤
            activation_steps = []
            
            # 1. 安装产品密钥
            key_result = self.install_product_key(product_key)
            activation_steps.append({
                'step': 'install_key',
                'result': key_result
            })
            
            if not key_result['success']:
                return {
                    'success': False,
                    'steps': activation_steps,
                    'error': '产品密钥安装失败'
                }
            
            # 2. 设置KMS服务器
            kms_result = self.set_kms_server(kms_server)
            activation_steps.append({
                'step': 'set_kms',
                'result': kms_result
            })
            
            if not kms_result['success']:
                return {
                    'success': False,
                    'steps': activation_steps,
                    'error': 'KMS服务器设置失败'
                }
            
            # 3. 激活Windows
            activate_result = self.activate_windows()
            activation_steps.append({
                'step': 'activate',
                'result': activate_result
            })
            
            # 记录激活历史
            activation_record = {
                'timestamp': datetime.now().isoformat(),
                'windows_version': windows_version,
                'product_key': product_key,
                'kms_server': kms_server,
                'success': activate_result['success'],
                'steps': activation_steps
            }
            
            self.activation_history.append(activation_record)
            self.save_history()
            
            return {
                'success': activate_result['success'],
                'steps': activation_steps,
                'activation_record': activation_record
            }
            
        except Exception as e:
            logger.error(f"自动激活失败: {e}")
            return {
                'success': False,
                'error': str(e)
            }

# 创建激活器实例
activator = WindowsActivator()

# API路由
@app.route('/')
def index():
    """主页"""
    return jsonify({
        'message': 'ActivateWin Backend Service',
        'version': '1.0.0',
        'status': 'running'
    })

@app.route('/api/status')
def get_status():
    """获取系统激活状态"""
    try:
        status = activator.check_windows_activation()
        system_info = activator.get_system_info()
        
        return jsonify({
            'success': True,
            'activation_status': status,
            'system_info': system_info,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"获取状态失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/activate', methods=['POST'])
def activate():
    """激活Windows"""
    try:
        data = request.get_json() or {}
        windows_version = data.get('windows_version')
        kms_server = data.get('kms_server')
        
        result = activator.auto_activate(windows_version, kms_server)
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"激活失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/kms/test', methods=['POST'])
def test_kms():
    """测试KMS服务器"""
    try:
        data = request.get_json()
        kms_server = data.get('kms_server')
        port = data.get('port', 1688)
        
        if not kms_server:
            return jsonify({
                'success': False,
                'error': 'KMS服务器地址不能为空'
            }), 400
        
        result = activator.test_kms_server(kms_server, port)
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"测试KMS失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/kms/servers')
def get_kms_servers():
    """获取KMS服务器列表"""
    return jsonify({
        'success': True,
        'servers': KMS_SERVERS
    })

@app.route('/api/keys')
def get_keys():
    """获取GVLK密钥列表"""
    return jsonify({
        'success': True,
        'keys': GVLK_KEYS
    })

@app.route('/api/history')
def get_history():
    """获取激活历史"""
    return jsonify({
        'success': True,
        'history': activator.activation_history
    })

@app.route('/api/system/info')
def system_info():
    """获取系统信息"""
    try:
        info = activator.get_system_info()
        windows_version = activator.detect_windows_version()
        
        return jsonify({
            'success': True,
            'system_info': info,
            'detected_version': windows_version,
            'gvlk_key': GVLK_KEYS.get(windows_version, None)
        })
    except Exception as e:
        logger.error(f"获取系统信息失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/activation/manual', methods=['POST'])
def manual_activation():
    """手动激活步骤"""
    try:
        data = request.get_json()
        action = data.get('action')
        
        if action == 'install_key':
            product_key = data.get('product_key')
            if not product_key:
                return jsonify({'success': False, 'error': '产品密钥不能为空'}), 400
            result = activator.install_product_key(product_key)
            
        elif action == 'set_kms':
            kms_server = data.get('kms_server')
            port = data.get('port', 1688)
            if not kms_server:
                return jsonify({'success': False, 'error': 'KMS服务器地址不能为空'}), 400
            result = activator.set_kms_server(kms_server, port)
            
        elif action == 'activate':
            result = activator.activate_windows()
            
        elif action == 'clear_kms':
            result = activator.clear_kms_server()
            
        else:
            return jsonify({'success': False, 'error': '无效的操作'}), 400
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"手动激活失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # 检查管理员权限
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin:
            logger.warning("程序未以管理员权限运行，某些功能可能无法正常使用")
    except:
        pass
    
    # 启动服务
    logger.info("ActivateWin Backend Service 启动中...")
    app.run(host='0.0.0.0', port=5000, debug=False)
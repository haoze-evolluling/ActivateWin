import subprocess
import platform
import json
import os
import threading
import sys
from datetime import datetime

class KMSActivatorBackend:
    def __init__(self):
        # KMS服务器列表
        self.kms_servers = [
            "kms.loli.beer",
            "kms.loli.best", 
            "kms.03k.org",
            "kms-default.cangshui.net",
            "kms.cgtsoft.com"
        ]
        
        # Windows版本对应的密钥
        self.windows_keys = {
            "Windows 11/10 专业版": "W269N-WFGWX-YVC9B-4J6C9-T83GX",
            "Windows 11/10 专业版 N": "MH37W-N47XK-V7XM9-C7227-GCQG9",
            "Windows 11/10 专业工作站版": "NRG8B-VKK3Q-CXVCJ-9G2XF-6Q84J",
            "Windows 11/10 专业工作站版 N": "9FNHH-K3HBT-3W4TD-6383H-6XYWF",
            "Windows 11/10 专业教育版": "6TP4R-GNPTD-KYYHQ-7B7DP-J447Y",
            "Windows 11/10 专业教育版 N": "YVWGF-BXNMC-HTQYQ-CPQ99-66QFC",
            "Windows 11/10 教育版": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
            "Windows 11/10 教育版 N": "2WH4N-8QGBV-H22JP-CT43Q-MDWWJ",
            "Windows 11/10 企业版": "NPPR9-FWDCX-D2C8J-H872K-2YT43",
            "Windows 11/10 企业版 N": "DPH2V-TTNVB-4X9Q3-TJR4H-KHJW4",
            "Windows 11/10 企业版 G": "YYVX9-NTFWV-6MDM3-9PT4T-4M68B",
            "Windows 11/10 企业版 G N": "44RPN-FTY23-9VTTB-MP9BX-T84FV",
            "Windows 11/10 企业版 LTSC 2019": "M7XTQ-FN8P6-TTKYV-9D4CC-J462D",
            "Windows 11/10 企业版 N LTSC 2019": "92NFX-8DJQP-P6BBQ-THF9C-7CG2H",
            "Windows Server 2025 标准版": "TVRH6-WHNXV-R9WG3-9XRFY-MY832",
            "Windows Server 2025 数据中心版": "D764K-2NDRG-47T6Q-P8T8W-YP6DF",
            "Windows Server 2022 标准版": "VDYBN-27WPP-V4HQT-9VMD4-VMK7H",
            "Windows Server 2022 数据中心版": "WX4NM-KYWYW-QJJR4-XV3QB-6VM33",
            "Windows Server 2019 标准版": "N69G4-B89J2-4G8F4-WWYCC-J464C",
            "Windows Server 2019 数据中心版": "WMDGN-G9PQG-XVVXX-R3X43-63DFG",
            "Windows Server 2016 标准版": "WC2BQ-8NRM3-FDDYY-2BFGV-KHKQY",
            "Windows Server 2016 数据中心版": "CB7KF-BWN84-R7R2Y-793K2-8XDDG",
            "Windows 7 专业版": "FJ82H-XT6CR-J8D7P-XQJJ2-GPDD4",
            "Windows 7 企业版": "33PXH-7Y6KF-2VJC9-XBBR8-HVTHH",
            "Windows Vista 商用版": "YFKBB-PQJJV-G996G-VWGXY-2V3X8",
            "Windows Vista 企业版": "VKK3X-68KWM-X2YGT-QR4M6-4BWMV"
        }
    
    def get_kms_servers(self):
        """获取KMS服务器列表"""
        return self.kms_servers
    
    def get_windows_versions(self):
        """获取Windows版本列表"""
        return list(self.windows_keys.keys())
    
    def get_current_os(self):
        """检测当前Windows版本"""
        try:
            result = subprocess.run(['systeminfo'], capture_output=True, text=True, shell=True)
            output = result.stdout.upper()
            
            if "WINDOWS 11" in output:
                return "Windows 11"
            elif "WINDOWS 10" in output:
                return "Windows 10"
            elif "WINDOWS SERVER 2025" in output:
                return "Windows Server 2025"
            elif "WINDOWS SERVER 2022" in output:
                return "Windows Server 2022"
            elif "WINDOWS SERVER 2019" in output:
                return "Windows Server 2019"
            elif "WINDOWS SERVER 2016" in output:
                return "Windows Server 2016"
            elif "WINDOWS 7" in output:
                return "Windows 7"
            elif "WINDOWS VISTA" in output:
                return "Windows Vista"
            else:
                return "未知版本"
        except:
            return "检测失败"
    
    def run_command(self, command):
        """运行命令并返回结果"""
        try:
            result = subprocess.run(command, capture_output=True, text=True, 
                                  shell=True, check=True)
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr
    
    def handle_activation_request(self, version, kms_server, log_callback):
        """处理激活请求"""
        if version == "请选择Windows版本":
            log_callback("请先选择Windows版本")
            return
        
        if not kms_server:
            log_callback("请选择KMS服务器")
            return
        
        key = self.windows_keys.get(version)
        if not key:
            log_callback("未找到对应的产品密钥")
            return
        
        # 在新线程中执行激活操作
        thread = threading.Thread(target=self.activate_windows, 
                                args=(key, kms_server, version, log_callback))
        thread.daemon = True
        thread.start()
    
    def activate_windows(self, key, kms_server, version, log_callback):
        """激活Windows"""
        log_callback("=" * 50)
        log_callback("开始激活流程...")
        log_callback(f"目标版本: {version}")
        log_callback(f"KMS服务器: {kms_server}")
        log_callback(f"产品密钥: {key}")
        log_callback("=" * 50)
        
        try:
            # 安装密钥
            log_callback("📥 正在安装产品密钥...")
            success, output = self.run_command(f"slmgr /ipk {key}")
            if success:
                log_callback("✅ 产品密钥安装成功")
            else:
                log_callback(f"❌ 产品密钥安装失败: {output}")
                return
            
            # 设置KMS服务器
            log_callback("🔗 正在连接KMS服务器...")
            success, output = self.run_command(f"slmgr /skms {kms_server}")
            if success:
                log_callback("✅ KMS服务器连接成功")
            else:
                log_callback(f"❌ KMS服务器连接失败: {output}")
                return
            
            # 激活系统
            log_callback("⚡ 正在激活系统...")
            success, output = self.run_command("slmgr /ato")
            if success:
                log_callback("🎉 系统激活成功！")
                log_callback("请重启计算机以完成激活")
            else:
                log_callback(f"❌ 系统激活失败: {output}")
                
        except Exception as e:
            log_callback(f"💥 发生错误: {str(e)}")
    
    def handle_verify_request(self, log_callback):
        """处理验证请求"""
        log_callback("🔍 正在验证激活状态...")
        success, output = self.run_command("slmgr /xpr")
        
        if success:
            # 获取更详细的激活信息
            try:
                result = subprocess.run(['slmgr', '/dli'], capture_output=True, 
                                      text=True, shell=True)
                detailed_info = result.stdout
            except:
                detailed_info = "无法获取详细信息"
            
            info = f"激活状态:\n{output}\n\n详细信息:\n{detailed_info}"
            log_callback("=" * 50)
            log_callback("激活状态验证完成")
            log_callback(info)
            log_callback("=" * 50)
        else:
            log_callback("❌ 无法验证激活状态")
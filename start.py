#!/usr/bin/env python3
"""
ActivateWin 统一启动器
同时启动前端和后端服务（管理员权限）
"""

import os
import sys
import subprocess
import threading
import time
import webbrowser
import socket
from pathlib import Path

class Colors:
    """终端颜色"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class ServiceManager:
    """服务管理器"""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent.absolute()
        self.backend_dir = self.root_dir / "backend"
        self.webui_dir = self.root_dir / "webui"
        self.processes = {}
        self.threads = []
        
    def print_banner(self):
        """打印启动横幅"""
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    ██    ██  █████  ██████  ██      ███████ ████████ ██████   ║
║    ██    ██ ██   ██ ██   ██ ██      ██         ██    ██   ██  ║
║    ██    ██ ███████ ██████  ██      █████      ██    ██████   ║
║     ██  ██  ██   ██ ██   ██ ██      ██         ██    ██   ██  ║
║      ████   ██   ██ ██████  ███████ ███████    ██    ██████   ║
║                                                               ║
║              Windows Activation Tool v2.0                     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
        print(banner)
    
    def check_admin(self):
        """检查管理员权限"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def check_port_available(self, port):
        """检查端口是否可用"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            return result != 0
        except:
            return False
    
    def find_free_port(self, start_port):
        """查找可用端口"""
        port = start_port
        while not self.check_port_available(port):
            port += 1
        return port
    
    def restart_as_admin(self):
        """以管理员权限重新启动"""
        try:
            import ctypes
            print(f"{Colors.YELLOW}[ADMIN] 请求管理员权限...{Colors.RESET}")
            
            # 获取当前可执行文件路径
            if getattr(sys, 'frozen', False):
                # 如果是打包的可执行文件
                script_path = sys.executable
            else:
                # 如果是Python脚本
                script_path = os.path.abspath(__file__)
            
            # 使用ShellExecuteW以管理员权限运行
            ret = ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                sys.executable, 
                f'"{script_path}"', 
                None, 
                1
            )
            
            if ret > 32:
                print(f"{Colors.GREEN}[ADMIN] 已请求管理员权限，正在重新启动...{Colors.RESET}")
                sys.exit(0)
            else:
                print(f"{Colors.RED}[ADMIN] 无法获取管理员权限{Colors.RESET}")
                return False
                
        except Exception as e:
            print(f"{Colors.RED}[ADMIN] 获取管理员权限失败: {e}{Colors.RESET}")
            return False
    
    def start_backend(self, port=None):
        """启动后端服务"""
        if not port:
            port = self.find_free_port(5000)
        
        print(f"{Colors.BLUE}[BACKEND] 启动后端服务...{Colors.RESET}")
        
        try:
            # 检查run.py是否存在
            run_script = self.backend_dir / "run.py"
            if not run_script.exists():
                # 直接启动app.py
                cmd = [sys.executable, "app.py"]
            else:
                cmd = [sys.executable, "run.py"]
            
            cmd.extend(["--host", "0.0.0.0", "--port", str(port)])
            
            process = subprocess.Popen(
                cmd,
                cwd=str(self.backend_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            
            self.processes['backend'] = process
            time.sleep(2)  # 等待服务启动
            
            # 检查服务是否成功启动
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                print(f"{Colors.GREEN}[✓] 后端服务启动成功: http://localhost:{port}{Colors.RESET}")
                return port
            else:
                print(f"{Colors.RED}[✗] 后端服务启动失败{Colors.RESET}")
                return None
                
        except Exception as e:
            print(f"{Colors.RED}[✗] 启动后端失败: {e}{Colors.RESET}")
            return None
    
    def start_frontend(self, port=None):
        """启动前端服务"""
        if not port:
            port = self.find_free_port(8000)
        
        print(f"{Colors.BLUE}[FRONTEND] 启动前端服务...{Colors.RESET}")
        
        try:
            process = subprocess.Popen([
                sys.executable, "-m", "http.server", str(port)
            ],
            cwd=str(self.webui_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            
            self.processes['frontend'] = process
            time.sleep(1)  # 等待服务启动
            
            # 检查服务是否成功启动
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                print(f"{Colors.GREEN}[✓] 前端服务启动成功: http://localhost:{port}{Colors.RESET}")
                return port
            else:
                print(f"{Colors.RED}[✗] 前端服务启动失败{Colors.RESET}")
                return None
                
        except Exception as e:
            print(f"{Colors.RED}[✗] 启动前端失败: {e}{Colors.RESET}")
            return None
    
    def open_browser(self, url):
        """自动打开浏览器"""
        try:
            webbrowser.open(url, new=2)
            print(f"{Colors.CYAN}[BROWSER] 已自动打开: {url}{Colors.RESET}")
        except:
            print(f"{Colors.YELLOW}[BROWSER] 请手动打开: {url}{Colors.RESET}")
    
    def monitor_services(self):
        """监控服务状态"""
        while True:
            for name, process in self.processes.items():
                if process.poll() is not None:
                    print(f"{Colors.RED}[{name.upper()}] 服务已停止{Colors.RESET}")
                    self.processes.pop(name, None)
            
            if not self.processes:
                break
            
            time.sleep(1)
    
    def stop_all_services(self):
        """停止所有服务"""
        print(f"{Colors.YELLOW}[INFO] 正在停止所有服务...{Colors.RESET}")
        
        for name, process in self.processes.items():
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"{Colors.GREEN}[✓] {name} 已停止{Colors.RESET}")
            except:
                try:
                    process.kill()
                    print(f"{Colors.RED}[✗] {name} 强制停止{Colors.RESET}")
                except:
                    pass
    
    def run(self):
        """运行启动器"""
        try:
            self.print_banner()
            
            # 检查管理员权限，如果不是管理员则请求提升权限
            is_admin = self.check_admin()
            if not is_admin:
                print(f"{Colors.YELLOW}[WARNING] 需要管理员权限运行{Colors.RESET}")
                self.restart_as_admin()
                return  # 退出当前进程
            else:
                print(f"{Colors.GREEN}[✓] 已以管理员权限运行{Colors.RESET}")
            
            # 检查端口
            backend_port = 5000 if self.check_port_available(5000) else self.find_free_port(5000)
            frontend_port = 8000 if self.check_port_available(8000) else self.find_free_port(8000)
            
            print(f"{Colors.WHITE}[CONFIG] 端口配置:{Colors.RESET}")
            print(f"  后端端口: {Colors.CYAN}{backend_port}{Colors.RESET}")
            print(f"  前端端口: {Colors.CYAN}{frontend_port}{Colors.RESET}")
            print(f"  管理员权限: {Colors.GREEN}是{Colors.RESET}")
            
            # 启动服务
            print(f"{Colors.BOLD}[STARTUP] 启动服务...{Colors.RESET}")
            
            backend_success = self.start_backend(backend_port)
            frontend_success = self.start_frontend(frontend_port)
            
            if backend_success and frontend_success:
                print(f"\n{Colors.GREEN}{Colors.BOLD}[SUCCESS] 所有服务启动成功！{Colors.RESET}")
                
                url = f"http://localhost:{frontend_port}"
                print(f"{Colors.WHITE}[ACCESS] 访问地址: {Colors.CYAN}{url}{Colors.RESET}")
                print(f"{Colors.WHITE}[API]    API地址: {Colors.CYAN}http://localhost:{backend_port}{Colors.RESET}")
                
                # 延迟打开浏览器
                threading.Timer(2.0, self.open_browser, args=[url]).start()
                
                print(f"{Colors.YELLOW}[INFO] 按 Ctrl+C 停止所有服务{Colors.RESET}")
                
                try:
                    self.monitor_services()
                except KeyboardInterrupt:
                    print(f"\n{Colors.YELLOW}[INFO] 收到停止信号{Colors.RESET}")
            else:
                print(f"{Colors.RED}[ERROR] 服务启动失败{Colors.RESET}")
                self.stop_all_services()
                
        except Exception as e:
            print(f"{Colors.RED}[ERROR] 启动器错误: {e}{Colors.RESET}")
        finally:
            self.stop_all_services()

def main():
    """主函数"""
    if sys.platform.startswith('win'):
        # Windows系统设置
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW("ActivateWin 启动器")
        except:
            pass
    
    manager = ServiceManager()
    manager.run()

if __name__ == "__main__":
    main()
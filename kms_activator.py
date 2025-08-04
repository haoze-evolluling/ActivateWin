import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import platform
import json
import os
import threading
import sys
from datetime import datetime
import ctypes

class ModernButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            font=("Microsoft YaHei", 11, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=25,
            pady=12
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, e):
        self.configure(bg=self["activebackground"])
    
    def on_leave(self, e):
        self.configure(bg=self["bg"])

def is_admin():
    """检查是否为管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """以管理员身份重新运行程序"""
    try:
        if hasattr(sys, '_MEIPASS'):
            # 如果是打包后的exe
            executable = sys.executable
        else:
            # 如果是Python脚本
            executable = sys.executable
            params = [sys.argv[0]]
            
        # 使用ShellExecuteW以管理员身份运行
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            executable,
            ' '.join(sys.argv[1:]) if hasattr(sys, '_MEIPASS') else ' '.join([f'"{arg}"' for arg in sys.argv]),
            None,
            1
        )
        return True
    except Exception as e:
        print(f"提权失败: {e}")
        return False

class KMSActivator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Windows KMS 激活工具")
        self.root.geometry("700x600")
        self.root.configure(bg="#ffffff")
        self.root.resizable(False, False)
        
        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap(default="icon.ico")
        except:
            pass
        
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
        
        self.current_os = self.detect_os()
        self.setup_styles()
        self.create_gui()
        
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 自定义样式
        style.configure('TLabel', background='#ffffff', font=('Microsoft YaHei', 10))
        style.configure('Header.TLabel', font=('Microsoft YaHei', 18, 'bold'))
        style.configure('SubHeader.TLabel', font=('Microsoft YaHei', 12))
        style.configure('TFrame', background='#ffffff')
        style.configure('TLabelframe', background='#ffffff')
        style.configure('TLabelframe.Label', font=('Microsoft YaHei', 11, 'bold'))
        
        # 自定义Combobox样式
        style.map('TCombobox',
                 fieldbackground=[('readonly', '#f8f9fa')],
                 selectbackground=[('readonly', '#e9ecef')],
                 selectforeground=[('readonly', '#212529')])
    
    def detect_os(self):
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
    
    def create_gui(self):
        """创建现代化GUI界面"""
        # 主框架
        main_frame = tk.Frame(self.root, bg="#ffffff")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 标题区域
        title_frame = tk.Frame(main_frame, bg="#ffffff")
        title_frame.pack(fill="x", pady=(0, 30))
        
        title_label = tk.Label(title_frame, text="Windows KMS 激活工具", 
                             font=("Microsoft YaHei", 24, "bold"), 
                             bg="#ffffff", fg="#2c3e50")
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="一键激活您的Windows系统", 
                                font=("Microsoft YaHei", 12), 
                                bg="#ffffff", fg="#7f8c8d")
        subtitle_label.pack()
        
        # 系统信息卡片
        info_card = tk.Frame(main_frame, bg="#f8f9fa", relief="raised", bd=1)
        info_card.pack(fill="x", pady=(0, 20))
        
        info_label = tk.Label(info_card, text=f"当前系统版本: {self.current_os}", 
                            font=("Microsoft YaHei", 12, "bold"), 
                            bg="#f8f9fa", fg="#495057", pady=15)
        info_label.pack()
        
        # 配置区域
        config_frame = tk.Frame(main_frame, bg="#ffffff")
        config_frame.pack(fill="x", pady=(0, 20))
        
        # 左侧：Windows版本选择
        left_frame = tk.Frame(config_frame, bg="#ffffff")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        version_label = tk.Label(left_frame, text="选择Windows版本", 
                               font=("Microsoft YaHei", 12, "bold"), 
                               bg="#ffffff", fg="#2c3e50")
        version_label.pack(anchor="w", pady=(0, 10))
        
        self.version_var = tk.StringVar()
        self.version_combo = ttk.Combobox(left_frame, textvariable=self.version_var, 
                                        values=list(self.windows_keys.keys()), 
                                        width=40, state="readonly", 
                                        font=("Microsoft YaHei", 10))
        self.version_combo.pack(fill="x")
        self.version_combo.set("请选择Windows版本")
        
        # 右侧：KMS服务器选择
        right_frame = tk.Frame(config_frame, bg="#ffffff")
        right_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        kms_label = tk.Label(right_frame, text="选择KMS服务器", 
                           font=("Microsoft YaHei", 12, "bold"), 
                           bg="#ffffff", fg="#2c3e50")
        kms_label.pack(anchor="w", pady=(0, 10))
        
        self.kms_var = tk.StringVar()
        self.kms_combo = ttk.Combobox(right_frame, textvariable=self.kms_var, 
                                    values=self.kms_servers, width=30, 
                                    state="readonly", font=("Microsoft YaHei", 10))
        self.kms_combo.pack(fill="x")
        self.kms_combo.set("kms.cgtsoft.com")
        
        # 按钮区域
        button_frame = tk.Frame(main_frame, bg="#ffffff")
        button_frame.pack(pady=(0, 20))
        
        # 激活按钮
        activate_btn = ModernButton(button_frame, text="🚀 开始激活", 
                                  command=self.start_activation,
                                  bg="#3498db", activebackground="#2980b9", 
                                  fg="white")
        activate_btn.pack(side="left", padx=10)
        
        # 验证按钮
        verify_btn = ModernButton(button_frame, text="✅ 验证激活", 
                                command=self.verify_activation,
                                bg="#2ecc71", activebackground="#27ae60", 
                                fg="white")
        verify_btn.pack(side="left", padx=10)
        
        # 清除日志按钮
        clear_btn = ModernButton(button_frame, text="🧹 清除日志", 
                               command=self.clear_log,
                               bg="#95a5a6", activebackground="#7f8c8d", 
                               fg="white")
        clear_btn.pack(side="left", padx=10)
        
        # 日志区域
        log_frame = tk.Frame(main_frame, bg="#ffffff")
        log_frame.pack(fill="both", expand=True)
        
        log_header = tk.Frame(log_frame, bg="#ffffff")
        log_header.pack(fill="x", pady=(0, 10))
        
        log_title = tk.Label(log_header, text="操作日志", 
                           font=("Microsoft YaHei", 12, "bold"), 
                           bg="#ffffff", fg="#2c3e50")
        log_title.pack(side="left")
        
        # 日志文本框
        log_container = tk.Frame(log_frame, bg="#f8f9fa", relief="groove", bd=1)
        log_container.pack(fill="both", expand=True)
        
        self.log_text = tk.Text(log_container, height=12, width=70, 
                              font=("Consolas", 9), bg="#f8f9fa", 
                              fg="#495057", relief="flat",
                              padx=10, pady=10)
        scrollbar = ttk.Scrollbar(log_container, orient="vertical", 
                                command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 添加初始日志
        self.log_message("程序启动成功")
        self.log_message(f"检测到系统: {self.current_os}")
        
    def log_message(self, message):
        """添加日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def clear_log(self):
        """清除日志"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("日志已清除")
    
    def run_command(self, command):
        """运行命令并返回结果"""
        try:
            result = subprocess.run(command, capture_output=True, text=True, 
                                  shell=True, check=True)
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr
    
    def start_activation(self):
        """开始激活流程"""
        version = self.version_var.get()
        kms_server = self.kms_var.get()
        
        if version == "请选择Windows版本":
            messagebox.showwarning("⚠️ 警告", "请先选择Windows版本")
            return
        
        if not kms_server:
            messagebox.showwarning("⚠️ 警告", "请选择KMS服务器")
            return
        
        key = self.windows_keys.get(version)
        if not key:
            messagebox.showerror("❌ 错误", "未找到对应的产品密钥")
            return
        
        # 确认对话框
        if not messagebox.askyesno("确认", f"确定要激活 {version} 吗？"):
            return
        
        # 在新线程中执行激活操作
        thread = threading.Thread(target=self.activate_windows, 
                                args=(key, kms_server, version))
        thread.daemon = True
        thread.start()
    
    def activate_windows(self, key, kms_server, version):
        """激活Windows"""
        self.log_message("=" * 50)
        self.log_message("开始激活流程...")
        self.log_message(f"目标版本: {version}")
        self.log_message(f"KMS服务器: {kms_server}")
        self.log_message(f"产品密钥: {key}")
        self.log_message("=" * 50)
        
        try:
            # 安装密钥
            self.log_message("📥 正在安装产品密钥...")
            success, output = self.run_command(f"slmgr /ipk {key}")
            if success:
                self.log_message("✅ 产品密钥安装成功")
            else:
                self.log_message(f"❌ 产品密钥安装失败: {output}")
                messagebox.showerror("错误", f"密钥安装失败:\n{output}")
                return
            
            # 设置KMS服务器
            self.log_message("🔗 正在连接KMS服务器...")
            success, output = self.run_command(f"slmgr /skms {kms_server}")
            if success:
                self.log_message("✅ KMS服务器连接成功")
            else:
                self.log_message(f"❌ KMS服务器连接失败: {output}")
                messagebox.showerror("错误", f"服务器连接失败:\n{output}")
                return
            
            # 激活系统
            self.log_message("⚡ 正在激活系统...")
            success, output = self.run_command("slmgr /ato")
            if success:
                self.log_message("🎉 系统激活成功！")
                self.log_message("请重启计算机以完成激活")
                messagebox.showinfo("成功", "Windows激活成功！\n建议重启计算机")
            else:
                self.log_message(f"❌ 系统激活失败: {output}")
                messagebox.showerror("失败", f"激活失败:\n{output}")
                
        except Exception as e:
            self.log_message(f"💥 发生错误: {str(e)}")
            messagebox.showerror("错误", f"执行过程中发生错误:\n{str(e)}")
    
    def verify_activation(self):
        """验证激活状态"""
        self.log_message("🔍 正在验证激活状态...")
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
            self.log_message("=" * 50)
            self.log_message("激活状态验证完成")
            self.log_message(info)
            self.log_message("=" * 50)
            
            messagebox.showinfo("激活状态", info)
        else:
            self.log_message("❌ 无法验证激活状态")
            messagebox.showerror("错误", "无法验证激活状态")
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()

def main():
    """主函数 - 自动提权版本"""
    # 检查是否为管理员
    if not is_admin():
        print("检测到非管理员权限，正在请求提权...")
        
        # 尝试以管理员身份重新运行
        if run_as_admin():
            print("已请求管理员权限，程序将重新启动...")
            sys.exit(0)  # 退出当前进程
        else:
            # 提权失败，显示错误信息
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("错误", "无法获取管理员权限，程序无法继续运行。\n\n"
                               "请手动右键选择\"以管理员身份运行\"")
            sys.exit(1)
    
    # 已经是管理员，运行主程序
    try:
        app = KMSActivator()
        app.run()
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("错误", f"程序启动失败:\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
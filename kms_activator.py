import tkinter as tk
from tkinter import messagebox
import sys
import ctypes

from ui import KMSActivatorUI
from backend import KMSActivatorBackend

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
        self.root.title("ActivateWin")
        self.root.geometry("700x600")
        self.root.configure(bg="#ffffff")
        self.root.resizable(False, False)
        
        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap(default="icon1.ico")
        except:
            pass
        
        # 初始化后端和UI
        self.backend = KMSActivatorBackend()
        self.ui = KMSActivatorUI(self.root, self.backend)
        
    def run(self):
        """运行应用程序"""
        self.root.mainloop()
    
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
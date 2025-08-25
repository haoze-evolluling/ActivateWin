#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KMS激活管理器 - 主程序入口
前后端分离架构的主入口点
"""

import sys
import os
import ctypes
import tkinter as tk
from tkinter import messagebox

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frontend.ui_manager import UIManager
from backend.kms_service import KMSService


def check_admin_privileges():
    """检查管理员权限并尝试提升"""
    try:
        if os.name == 'nt':
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.getuid() == 0
    except:
        return False


def elevate_privileges():
    """尝试提升程序权限"""
    if os.name != 'nt':
        return False
        
    try:
        import ctypes
        import win32con
        
        # 使用ShellExecute重新启动程序
        params = " ".join(sys.argv[1:])
        
        result = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            __file__,
            None,
            win32con.SW_SHOWNORMAL
        )
        
        if result > 32:
            return True
        return False
        
    except ImportError:
        # 如果没有pywin32，使用基础方法
        try:
            import subprocess
            result = subprocess.run([
                "powershell", "-Command", 
                f"Start-Process '{sys.executable}' -ArgumentList '{__file__}' -Verb RunAs"
            ], capture_output=True)
            return result.returncode == 0
        except:
            return False
    except Exception:
        return False


def main():
    """主程序入口"""
    # 检查管理员权限
    if not check_admin_privileges():
        try:
            if elevate_privileges():
                sys.exit(0)
            else:
                pass
                
                # 显示警告消息
                root = tk.Tk()
                root.withdraw()
                messagebox.showwarning(
                    "警告", 
                    "程序需要管理员权限才能执行激活操作。\n\n"
                    "建议：请右键以管理员身份运行程序，\n"
                )
                root.destroy()
                
        except Exception as e:
            root = tk.Tk()
            root.withdraw()
            messagebox.showwarning(
                "警告", 
                f"无法获取管理员权限，某些功能可能受限:\n{str(e)}\n\n"
                f"建议：请手动右键以管理员身份运行程序"
            )
            root.destroy()
    
    # 创建并运行UI
    try:
        ui_manager = UIManager()
        ui_manager.run()
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("错误", f"程序启动失败:\n{str(e)}")
        root.destroy()
        sys.exit(1)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试管理员权限检查功能的简单脚本
"""

import ctypes
import sys
import os

def test_admin_check():
    """测试管理员权限检查"""
    try:
        import ctypes
        
        print("测试管理员权限检查...")
        print(f"Python可执行文件: {sys.executable}")
        print(f"脚本路径: {__file__}")
        print(f"命令行参数: {sys.argv}")
        
        # 检查管理员权限
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        print(f"当前是否具有管理员权限: {is_admin}")
        
        if not is_admin:
            print("当前没有管理员权限，准备请求提升...")
            
            # 检查是否已经有--admin参数
            if len(sys.argv) > 1 and sys.argv[1] == "--admin":
                print("已经有--admin参数，避免无限循环")
            else:
                print("准备以管理员身份重新运行...")
                
                # 构建参数
                if getattr(sys, 'frozen', False):
                    # 打包后的exe
                    params = "--admin"
                    script_to_run = sys.executable
                else:
                    # 脚本运行
                    params = f'"{__file__}" --admin'
                    script_to_run = sys.executable
                
                print(f"将运行: {script_to_run} {params}")
                
                # 测试ShellExecuteW调用
                result = ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", script_to_run, params, None, 1)
                
                print(f"ShellExecuteW返回值: {result}")
                if result > 32:
                    print("权限提升请求已发送，准备退出当前实例")
                return True
                else:
                    print(f"权限提升失败，错误代码: {result}")
        else:
            print("已具有管理员权限，程序将继续运行")
            
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
    
    return False

if __name__ == "__main__":
    elevated = test_admin_check()
    if elevated:
        print("权限提升已启动，退出当前实例")
        sys.exit(0)
    else:
        print("继续运行程序...")
        input("按回车键继续...")
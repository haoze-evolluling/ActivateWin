#!/usr/bin/env python3
"""
启动脚本
提供多种启动方式
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def check_admin():
    """检查管理员权限"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """以管理员权限运行"""
    try:
        import ctypes
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        return True
    except:
        return False

def install_requirements():
    """安装依赖"""
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("依赖安装完成")
        return True
    except subprocess.CalledProcessError:
        print("依赖安装失败")
        return False

def main():
    parser = argparse.ArgumentParser(description='ActivateWin Backend Service')
    parser.add_argument('--port', type=int, default=5000, help='服务端口')
    parser.add_argument('--host', default='0.0.0.0', help='服务主机')
    parser.add_argument('--debug', action='store_true', help='调试模式')
    parser.add_argument('--install', action='store_true', help='安装依赖')
    parser.add_argument('--admin', action='store_true', help='以管理员权限运行')
    
    args = parser.parse_args()
    
    # 安装依赖
    if args.install:
        install_requirements()
        return
    
    # 检查管理员权限
    if not check_admin():
        print("警告: 未以管理员权限运行，某些功能可能无法正常使用")
        if args.admin:
            print("尝试以管理员权限重新启动...")
            if run_as_admin():
                return
            else:
                print("无法以管理员权限启动")
    
    # 设置环境变量
    os.environ['FLASK_ENV'] = 'development' if args.debug else 'production'
    
    # 启动服务
    from app import app
    
    print(f"""
╔═══════════════════════════════════════╗
║      ActivateWin Backend Service      ║
╠═══════════════════════════════════════╣
║  服务地址: http://{args.host}:{args.port}      ║
║  调试模式: {'是' if args.debug else '否'}               ║
║  管理员权限: {'是' if check_admin() else '否'}           ║
╚═══════════════════════════════════════╝
    """)
    
    try:
        app.run(host=args.host, port=args.port, debug=args.debug)
    except KeyboardInterrupt:
        print("\n服务已停止")
    except Exception as e:
        print(f"启动失败: {e}")

if __name__ == '__main__':
    main()
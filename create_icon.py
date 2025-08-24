#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建程序图标文件
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """创建程序图标"""
    # 创建256x256的图像
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制Windows标志背景
    draw.ellipse([20, 20, 236, 236], fill='#0078D4', outline='#005A9E', width=4)
    
    # 绘制Windows标志
    draw.rectangle([60, 80, 110, 130], fill='white')
    draw.rectangle([146, 80, 196, 130], fill='white')
    draw.rectangle([60, 146, 110, 196], fill='white')
    draw.rectangle([146, 146, 196, 196], fill='white')
    
    # 添加KMS文字
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    draw.text((128, 220), "KMS", fill='white', font=font, anchor='mm')
    
    # 保存图标
    img.save('icon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("图标文件已创建: icon.ico")

if __name__ == "__main__":
    try:
        create_icon()
    except ImportError:
        print("需要安装PIL库: pip install Pillow")
    except Exception as e:
        print(f"创建图标失败: {e}")
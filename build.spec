# -*- mode: python ; coding: utf-8 -*-

import os

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 定义图标路径
icon_path = os.path.join(current_dir, 'icon.ico')

# PyInstaller打包配置
block_cipher = None

a = Analysis(
    ['kms_activator.py'],
    pathex=[current_dir],
    binaries=[],
    datas=[
        ('icon.ico', '.'),
        ('icon.png', '.'),
        ('kmsserver.md', '.'),
        ('kmskey.md', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='KMSActivator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='KMSActivator',
)
# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['kms_activator.py'],
    pathex=[],
    binaries=[],
    datas=[('icon1.ico', '.'), ('icon1.png', '.'), ('README.md', '.'), ('方法指导.md', '.'), ('ui.py', '.'), ('backend.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ActivateWin',
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
    version='version_info.txt',
    icon=['icon1.ico'],
)

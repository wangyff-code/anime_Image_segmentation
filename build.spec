# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app_modern.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        # 你的 FP16 模型，确保路径正确
        ('models/best.onnx', 'models'), 
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # 再次确认：这里删除了 'xml'，因为 pywebview 需要它
    excludes=['tkinter', 'unittest', 'torch', 'ultralytics', 'pandas', 'matplotlib', 'cv2', 'scipy'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 单文件打包的关键：
# 这里把 a.scripts, a.binaries, a.zipfiles, a.datas 全部放进 EXE
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AnimeExtractor',  # 生成的 exe 名字
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,               # 开启 UPX 压缩
    upx_exclude=['vcruntime140.dll', 'msvcp140.dll'], # 防止压缩损坏运行库
    runtime_tmpdir=None,
    console=False,          # 关闭黑框
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/app_icon.ico'  # 如果没有图标，请删除这行或注释掉
)
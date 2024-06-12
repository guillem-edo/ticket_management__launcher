# beta_version.spec
# -*- mode: python ; coding: utf-8 -*-

import os
block_cipher = None

# Define base_path manualmente
base_path = 'C:/Users/FV1FEB0/Documents/GitHub/ticket_management__launcher/beta_version'

a = Analysis(
    [os.path.join(base_path, 'app', 'beta_version.py')],
    pathex=[
        os.path.join(base_path, 'app'),
        os.path.join(base_path, 'app', 'dependencies'),
        os.path.join(base_path, 'app', 'email_notifications')
    ],
    binaries=[],
    datas=[
        (os.path.join(base_path, 'app', 'dependencies.py'), 'app/dependencies.py'),
        (os.path.join(base_path, 'app', 'email_notifications.py'), 'app/email_notifications.py'),
        (os.path.join(base_path, 'app', 'logo.png'), 'app/logo.png')
    ],
    hiddenimports=['app.dependencies', 'app.email_notifications'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='beta_version',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='beta_version',
)
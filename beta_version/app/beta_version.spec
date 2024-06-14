# beta_version.spec
# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import copy_metadata

block_cipher = None

# Define base_path manualmente
base_path = os.path.abspath(os.path.dirname(__file__))

# Añadir dependencias de los paquetes instalados
hiddenimports = copy_metadata('PyQt5')

a = Analysis(
    [os.path.join(base_path, 'app', 'beta_version.py')],
    pathex=[os.path.join(base_path, 'app')],
    binaries=[],
    datas=[
        (os.path.join(base_path, 'app', 'dependencies.py'), 'app'),
        (os.path.join(base_path, 'app', 'email_notifications.py'), 'app'),
        (os.path.join(base_path, 'app', 'admin_dialog.py'), 'app'),
        (os.path.join(base_path, 'app', 'animations.py'), 'app'),
        (os.path.join(base_path, 'app', 'change_history.py'), 'app'),
        (os.path.join(base_path, 'app', 'dialogs.py'), 'app'),
        (os.path.join(base_path, 'app', 'excel_window.py'), 'app'),
        (os.path.join(base_path, 'app', 'incidence_chart.py'), 'app'),
        (os.path.join(base_path, 'app', 'incidence_details.py'), 'app'),
        (os.path.join(base_path, 'app', 'login_window.py'), 'app'),
        (os.path.join(base_path, 'app', 'mtbf_dialog.py'), 'app'),
        (os.path.join(base_path, 'app', 'notifications.py'), 'app'),
        (os.path.join(base_path, 'app', 'reports_export.py'), 'app'),
        (os.path.join(base_path, 'app', 'responsive_design.py'), 'app'),
        (os.path.join(base_path, 'app', 'send_report.py'), 'app'),
        (os.path.join(base_path, 'app', 'theme_manager.py'), 'app'),
        (os.path.join(base_path, 'app', 'user.py'), 'app'),
        (os.path.join(base_path, 'app', 'v2_management.py'), 'app'),
        (os.path.join(base_path, 'app', 'logo.png'), 'app'),
        (os.path.join(base_path, 'app', 'config.json'), 'app'),
        (os.path.join(base_path, 'app', 'incidencias_config.json'), 'app'),
        (os.path.join(base_path, 'app', 'mtbf_data.json'), 'app'),
        (os.path.join(base_path, 'app', 'detailed_messages.json'), 'app'),
        (os.path.join(base_path, 'app', 'change_log.json'), 'app'),
        (os.path.join(base_path, 'app', 'incidencias_state.json'), 'app'),
    ],
    hiddenimports=hiddenimports,
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

import os

block_cipher = None

# Asegúrate de que este es el directorio correcto donde está tu script principal
base_path = r'C:\Users\FV1FEB0\Documents\ticket_management__launcher\beta_version\app'

a = Analysis(
    [os.path.join(base_path, 'beta_version.py')],
    pathex=[base_path],
    binaries=[],
    datas=[
        (os.path.join(base_path, 'logo.png'), 'app'),
        (os.path.join(base_path, 'config.json'), 'app'),
        (os.path.join(base_path, 'incidencias_config.json'), 'app'),
        (os.path.join(base_path, 'mtbf_data.json'), 'app'),
        (os.path.join(base_path, 'detailed_messages.json'), 'app'),
        (os.path.join(base_path, 'change_log.json'), 'app'),
        (os.path.join(base_path, 'incidence_state.json'), 'app'),
        # Incluir cualquier otro archivo necesario
        (os.path.join(base_path, 'incidence_chart.py'), 'app'),
        (os.path.join(base_path, 'incidence_details.py'), 'app'),
        (os.path.join(base_path, 'question_icon.png'), 'app'),
        (os.path.join(base_path, 'admin_dialog.py'), 'app'),
        (os.path.join(base_path, 'change_history.py'), 'app'),
        (os.path.join(base_path, 'dialogs.py'), 'app'),
        (os.path.join(base_path, 'email_notifications.py'), 'app'),
        (os.path.join(base_path, 'excel_window.py'), 'app'),
        (os.path.join(base_path, 'login_window.py'), 'app'),
        (os.path.join(base_path, 'mtbf_dialog.py'), 'app'),
        (os.path.join(base_path, 'notifications.py'), 'app'),
        (os.path.join(base_path, 'reports_export.py'), 'app'),
        (os.path.join(base_path, 'responsive_design.py'), 'app'),
        (os.path.join(base_path, 'send_report.py'), 'app'),
        (os.path.join(base_path, 'theme_manager.py'), 'app'),
        (os.path.join(base_path, 'user.py'), 'app'),
        (os.path.join(base_path, 'dependencies.py'), 'app')

    ],
    hiddenimports=[
        'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'pandas', 'numpy', 'seaborn', 'matplotlib', 'openpyxl'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=['C:\\DumpStack.log.tmp'],
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
    strip=False,
    upx=True,
    console=False
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='beta_version',
    excludes=['C:\\DumpStack.log.tmp']
)
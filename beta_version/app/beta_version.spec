# beta_version.spec
import os

block_cipher = None

# Define el base_path como una ruta fija
base_path = 'C:/Users/FV1FEB0/Documents/GitHub/ticket_management__launcher/beta_version'

a = Analysis(
    [os.path.join(base_path, 'app', 'beta_version.py')],
    pathex=[
        os.path.join(base_path, 'app'),
    ],
    binaries=[],
    datas=[
        # Incluir todos los archivos en el directorio 'dependencies' y subdirectorios
        (os.path.join(base_path, 'app', 'dependencies'), 'dependencies'),
        # Incluir el logo y otros archivos estáticos directamente en la carpeta 'app' del empaquetado
        (os.path.join(base_path, 'app', 'logo.png'), 'app'),
        # Otros archivos o directorios
        (os.path.join(base_path, 'app', 'config.json'), 'app'),
        (os.path.join(base_path, 'app', 'incidencias_config.json'), 'app'),
        (os.path.join(base_path, 'app', 'mtbf_data.json'), 'app'),
        (os.path.join(base_path, 'app', 'detailed_messages.json'), 'app'),
        (os.path.join(base_path, 'app', 'change_log.json'), 'app'),
        (os.path.join(base_path, 'app', 'incidencias_state.json'), 'app'),
    ],
    hiddenimports=[],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    name='beta_version',
    debug=False,
    strip=False,
    upx=True,
    console=True
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='beta_version'
)
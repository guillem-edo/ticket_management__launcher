---

# Ticket Management Software - Beta v.6.0

## Overview

The Ticket Management System is a comprehensive tool designed to help manage and track incidents across various production lines. It is built using Python, with a GUI powered by PyQt5, and includes features such as incident logging, advanced filtering, MTBF (Mean Time Between Failures) calculation, and visual representation of data through charts. The application also supports Excel integration for data storage and manipulation.

## Features

- **User Authentication**: Different levels of access for regular users and administrators.
- **Incident Logging**: Track and confirm incidents across multiple production lines.
- **MTBF Calculation**: Calculate and display the Mean Time Between Failures for each production line.
- **Advanced Filtering**: Filter incidents based on date, time, and production line.
- **Data Visualization**: View daily, shift-based, and general incident trends through interactive charts.
- **Excel Integration**: Load and save incident data to Excel files for easy management and analysis.
- **Detailed Messaging**: Log detailed messages for each incident.
- **Pending Incidents**: Track incidents marked as "Fixing" or "Pendiente".
- **Incident Details**: Add detailed descriptions for each incident.
- **State Persistence**: Save and load the state of incidents and MTBF data between sessions.
- **Admin Functions**: Manage incident types and configurations with additional administrative controls.

## Installation

### Prerequisites

- Python 3.6 or later
- `pip` package manager
- Virtual environment (recommended)

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/ticket-management-system.git
    cd ticket-management-system
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application**:
    ```bash
    python beta_version.py
    ```

## Usage

### Main Window

Upon logging in, the main window presents a dashboard where you can manage incidents, view charts, and access advanced filters.

### Logging Incidents

1. Select the relevant production line tab.
2. Choose the incident from the list.
3. Click on "Confirmar Incidencia" to log the incident.

### Viewing Charts

- **Daily Chart**: Shows incidents logged within the current day.
- **Shift Chart**: Shows incidents logged within the current shift (6:00 AM to 6:00 PM).
- **General Chart**: Displays overall incidents across all production lines.

### Advanced Filtering

1. Open the advanced filter dialog by clicking "Filtro Avanzado".
2. Select the date and time range.
3. Choose the production line or select "Todos" for all lines.
4. Click "Aplicar Filtro" to view the filtered results.

### MTBF Information

- The MTBF (Mean Time Between Failures) is displayed for each production line.
- Click the info button next to the MTBF label for a detailed explanation.

### Detailed Messaging

- Log detailed messages for each incident by selecting "Añadir Detalles" after confirming an incident.
- View all logged messages under the "Mensajes detallados" tab.

### Pending Incidents

- Incidents marked as "Fixing" or "Pendiente" are tracked separately.
- The system will remind users to fix pending incidents after a set interval.

### Incident Details

- Add detailed descriptions for each incident when marking it as fixed or adding additional details.
- These details are saved and can be reviewed later.

### State Persistence

- The state of incidents, including their statuses and details, is saved when the application is closed.
- The MTBF data is also saved and reloaded on startup to maintain consistency.

## Configuration

### Excel Integration

- To select an Excel file for logging incidents, click on "Seleccionar Archivo Excel" and choose your file.
- The application will read from and write to this file to keep track of incident data.

### Admin Functions

Admins have additional controls to manage the incident types and configurations. The admin functions include:

**Manage Incident Types**:

- Add New Incidents: Admins can add new types of incidents to the system.
- Edit Existing Incidents: Admins can edit the names of existing incidents.
- Delete Incidents: Admins can delete incidents that are no longer relevant.
- Manage Incident Lists for Blocks: Admins can manage incident lists for different blocks, including empty blocks.

**Configuration Management**:

- Save and Load Configurations: Admins can save the current configuration of incidents to a JSON file and load configurations from a JSON file.
- Excel File Management: Admins can select the Excel file used for logging incidents.

**Admin Dialog Usage** 

1. Open the Admin Dialog: Click on the "Administrar Incidencias" button.
2. Select Block: Choose the relevant block from the dropdown menu.
3. Manage Incidents:

- Add Incident: Click "Añadir" and enter the name of the new incident.
- Edit Incident: Select an incident from the list, click "Editar", and modify the name.
- Delete Incident: Select an incident from the list and click "Eliminar".

## Hidden Features

### Detailed Messaging Tab

- An additional tab named "Mensajes detallados" allows users to log and view detailed messages for each incident, providing deeper insights into each issue.

### MTBF Timer Reset

- The MTBF data resets every 24 hours to ensure fresh calculations, reflecting the latest operational conditions.

### State Persistence

- The application saves the current state of incidents and MTBF data when closed, ensuring no data is lost between sessions.

## Compiling the Application

To compile the application and create an executable using PyInstaller, follow these steps:

1. **Configure the `.spec` file**:
    Ensure that your `beta_version.spec` file is correctly configured. Here is an example configuration:

    ```python
    import os

    block_cipher = None

    base_path = 'C:/Users/FV1FEB0/Documents/GitHub/ticket_management__launcher/beta_version/app'

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
            (os.path.join(base_path, 'incidencias_state.json'), 'app'),
        ],
        hiddenimports=[
            'pandas',
            'numpy',
        ],
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
        strip=False,
        upx=False,
        console=False  # Cambia a True si necesitas una consola para depuración
    )

    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=False,
        name='beta_version'
    )
    ```

2. **Clean and Build**:
    Before running PyInstaller, remove the `build` and `dist` directories if they exist to ensure a clean build:

    ```bash
    rmdir /S /Q build dist
    ```

    Then, run PyInstaller with the following command:

    ```bash
    pyinstaller --clean --log-level=DEBUG beta_version.spec
    ```

3. **Transfer and Execute**:
    Once the build is complete, you will find the executable in the `dist/beta_version` directory. Transfer this directory to the target machine and run `beta_version.exe` to start the application.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

Claro, aquí tienes la sección de la licencia actualizada con esa información adicional:

---

## License

This project is licensed under the GNU General Public License v3.0. You are free to use, modify, and distribute this software under the terms of the GPLv3. Unauthorized distribution of this software is prohibited and may lead to legal consequences.

For more details, see the [LICENSE](https://www.gnu.org/licenses/gpl-3.0.en.html) file.

## Acknowledgments

- Thanks to the contributors of the open-source libraries and tools used in this project.

## Contact

For any inquiries or issues, please contact [edoguillem@gmail.com](mailto:edoguillem@gmail.com).

---

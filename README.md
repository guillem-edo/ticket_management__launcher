# Ticket Management System - Launcher v.6.0

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
    python main.py
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

- Admin users have access to an additional "Administrar Incidencias" button to manage incident types and configurations.

## Hidden Features

### Detailed Messaging Tab

- An additional tab named "Mensajes detallados" allows users to log and view detailed messages for each incident, providing deeper insights into each issue.

### MTBF Timer Reset

- The MTBF data resets every 24 hours to ensure fresh calculations, reflecting the latest operational conditions.

### State Persistence

- The application saves the current state of incidents and MTBF data when closed, ensuring no data is lost between sessions.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE]([LICENSE](http://www.apache.org/licenses/)) file for details.

## Acknowledgments

- Thanks to the contributors of the open-source libraries and tools used in this project.

## Contact

For any inquiries or issues, please contact [edoguillem@gmail.com](mailto:edoguillem@gmail.com).

---

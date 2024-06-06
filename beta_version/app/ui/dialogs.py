# app/dialogs.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QHBoxLayout, QHeaderView, QMessageBox, QFileDialog
from collections import Counter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from datetime import datetime, timedelta
from datetime import datetime, timedelta
from collections import Counter
import csv


class AdvancedFilterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Filtro Avanzado")
        self.setGeometry(300, 300, 800, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
            }
            QComboBox, QTableWidget {
                font-size: 14px;
            }
            QPushButton {
                background-color: #E0E0E0;
                color: #000000;
                padding: 5px 10px;
                border: 1px solid #A0A0A0;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #D0D0D0;
            }
            QPushButton:pressed {
                background-color: #C0C0C0;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                gridline-color: #ccc;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #B0C4DE;
                color: white;
            }
        """)

        self.parent_widget = parent

        layout = QVBoxLayout()

        range_layout = QHBoxLayout()

        date_layout = QVBoxLayout()
        date_layout.addWidget(QLabel("Desde Fecha:"))
        self.start_date_combo = QComboBox()
        date_layout.addWidget(self.start_date_combo)

        date_layout.addWidget(QLabel("Hasta Fecha:"))
        self.end_date_combo = QComboBox()
        date_layout.addWidget(self.end_date_combo)

        range_layout.addLayout(date_layout)

        time_layout = QVBoxLayout()
        time_layout.addWidget(QLabel("Desde Hora:"))
        self.start_time_combo = QComboBox()
        self.populate_time_combo(self.start_time_combo)
        time_layout.addWidget(self.start_time_combo)

        time_layout.addWidget(QLabel("Hasta Hora:"))
        self.end_time_combo = QComboBox()
        self.populate_time_combo(self.end_time_combo)
        time_layout.addWidget(self.end_time_combo)

        range_layout.addLayout(time_layout)

        layout.addLayout(range_layout)

        block_layout = QHBoxLayout()
        block_layout.addWidget(QLabel("Seleccionar Bloque:"))
        self.block_selector = QComboBox()
        self.block_selector.addItem("Todos")
        self.block_selector.addItems(parent.blocks)
        block_layout.addWidget(self.block_selector)

        layout.addLayout(block_layout)

        button_layout = QHBoxLayout()
        filter_button = QPushButton("Aplicar Filtro")
        filter_button.clicked.connect(self.apply_filter)
        button_layout.addWidget(filter_button)

        export_button = QPushButton("Exportar CSV")
        export_button.clicked.connect(self.export_csv)
        button_layout.addWidget(export_button)

        layout.addLayout(button_layout)

        search_results_layout = QVBoxLayout()
        search_results_layout.addWidget(QLabel("Buscar en Resultados:"))
        self.search_results_line_edit = QLineEdit()
        self.search_results_line_edit.textChanged.connect(self.filter_results_table)
        search_results_layout.addWidget(self.search_results_line_edit)
        layout.addLayout(search_results_layout)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Bloque", "Número de Incidencias", "Incidencia más frecuente"])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.results_table)

        search_incidents_layout = QVBoxLayout()
        search_incidents_layout.addWidget(QLabel("Buscar en Incidencias:"))
        self.search_incidents_line_edit = QLineEdit()
        self.search_incidents_line_edit.textChanged.connect(self.filter_incidents_table)
        search_incidents_layout.addWidget(self.search_incidents_line_edit)
        layout.addLayout(search_incidents_layout)

        self.incidents_table = QTableWidget()
        self.incidents_table.setColumnCount(2)
        self.incidents_table.setHorizontalHeaderLabels(["Incidencia", "Número de Incidencias"])
        self.incidents_table.horizontalHeader().setStretchLastSection(True)
        self.incidents_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.incidents_table)

        self.setLayout(layout)
        self.populate_date_combos()

    def populate_date_combos(self):
        today = datetime.today()
        for i in range(30):
            date = today - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            self.start_date_combo.addItem(date_str)
            self.end_date_combo.addItem(date_str)

    def populate_time_combo(self, combo):
        for hour in range(24):
            time_str = f"{hour:02}:00"
            combo.addItem(time_str)

    def apply_filter(self):
        try:
            start_date = self.start_date_combo.currentText()
            start_time = self.start_time_combo.currentText()
            start_dt = datetime.strptime(f"{start_date} {start_time}:00", "%Y-%m-%d %H:%M:%S")

            end_date = self.end_date_combo.currentText()
            end_time = self.end_time_combo.currentText()
            end_dt = datetime.strptime(f"{end_date} {end_time}:00", "%Y-%m-%d %H:%M:%S")

            selected_block = self.block_selector.currentText()

            results, trends = self.parent_widget.get_filtered_incidents(start_dt, end_dt, selected_block)

            self.results_table.setRowCount(len(results))
            for row, (block, data) in enumerate(results.items()):
                self.results_table.setItem(row, 0, QTableWidgetItem(block))
                self.results_table.setItem(row, 1, QTableWidgetItem(str(data['count'])))
                self.results_table.setItem(row, 2, QTableWidgetItem(data['most_common_incidence']))

            self.update_incidents_table(results)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al aplicar el filtro: {e}")

    def update_incidents_table(self, results):
        all_incidents = []
        for block, data in results.items():
            all_incidents.extend(data['incidences'])

        counter = Counter(all_incidents)
        sorted_incidents = counter.most_common()

        self.incidents_table.setRowCount(len(sorted_incidents))
        for row, (incident, count) in enumerate(sorted_incidents):
            self.incidents_table.setItem(row, 0, QTableWidgetItem(incident))
            self.incidents_table.setItem(row, 1, QTableWidgetItem(str(count)))

    def filter_results_table(self):
        filter_text = self.search_results_line_edit.text().lower()
        for row in range(self.results_table.rowCount()):
            match = False
            for column in range(self.results_table.columnCount()):
                item = self.results_table.item(row, column)
                if item and filter_text in item.text().lower():
                    match = True
                    break
            self.results_table.setRowHidden(row, not match)

    def filter_incidents_table(self):
        filter_text = self.search_incidents_line_edit.text().lower()
        for row in range(self.incidents_table.rowCount()):
            match = False
            for column in range(self.incidents_table.columnCount()):
                item = self.incidents_table.item(row, column)
                if item and filter_text in item.text().lower():
                    match = True
                    break
            self.incidents_table.setRowHidden(row, not match)

    def export_csv(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar Informe CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if not file_name:
            return

        with open(file_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Bloque", "Número de Incidencias", "Incidencia más frecuente"])
            for row in range(self.results_table.rowCount()):
                bloque = self.results_table.item(row, 0).text() if self.results_table.item(row, 0) else ''
                num_incidencias = self.results_table.item(row, 1).text() if self.results_table.item(row, 1) else ''
                incidencia_frecuente = self.results_table.item(row, 2).text() if self.results_table.item(row, 2) else ''
                writer.writerow([bloque, num_incidencias, incidencia_frecuente])

            writer.writerow([])
            writer.writerow(["Incidencia", "Número de Incidencias"])
            for row in range(self.incidents_table.rowCount()):
                incidencia = self.incidents_table.item(row, 0).text() if self.incidents_table.item(row, 0) else ''
                num_incidencias = self.incidents_table.item(row, 1).text() if self.incidents_table.item(row, 1) else ''
                writer.writerow([incidencia, num_incidencias])

        QMessageBox.information(self, "Exportar Informe", "Informe exportado con éxito en formato CSV.")
class TopIncidentsDialog(QDialog):
    def __init__(self, parent=None, incident_details=None):
        super().__init__(parent)
        self.setWindowTitle("Detalles de Incidencias Más Relevantes")
        self.setGeometry(300, 300, 800, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                gridline-color: #ccc;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #4CAF50;
                color: white;
            }
        """)

        layout = QVBoxLayout()

        self.incidents_table = QTableWidget()
        self.incidents_table.setColumnCount(3)
        self.incidents_table.setHorizontalHeaderLabels(["Bloque", "Incidencia", "Número de Incidencias"])
        self.incidents_table.horizontalHeader().setStretchLastSection(True)
        self.incidents_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.populate_table(incident_details)
        layout.addWidget(self.incidents_table)

        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def populate_table(self, incident_details):
        row = 0
        for block, details in incident_details.items():
            top_incidents = details.most_common(5)
            for incident, count in top_incidents:
                self.incidents_table.insertRow(row)
                self.incidents_table.setItem(row, 0, QTableWidgetItem(block))
                self.incidents_table.setItem(row, 1, QTableWidgetItem(incident))
                self.incidents_table.setItem(row, 2, QTableWidgetItem(str(count)))
                row += 1
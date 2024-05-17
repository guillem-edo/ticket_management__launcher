# app/dialogs.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QScrollArea, QWidget, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from datetime import datetime, timedelta

class AdvancedFilterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Filtro Avanzado")
        self.setGeometry(300, 300, 800, 600)

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

        filter_button = QPushButton("Aplicar Filtro")
        filter_button.clicked.connect(self.apply_filter)
        layout.addWidget(filter_button)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Bloque", "Número de Incidencias", "Incidencia más frecuente"])
        layout.addWidget(self.results_table)

        self.incidents_table = QTableWidget()
        self.incidents_table.setColumnCount(2)
        self.incidents_table.setHorizontalHeaderLabels(["Incidencia", "Número de Incidencias"])
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

            results, trends = self.parent().get_filtered_incidents(start_dt, end_dt, selected_block)

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


class TopIncidentsDialog(QDialog):
    def __init__(self, parent=None, incident_details=None):
        super().__init__(parent)
        self.setWindowTitle("Detalles de Incidencias Más Relevantes")
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        arrow_up_pixmap = QPixmap("app/arrow_up.png").scaled(20, 20, Qt.KeepAspectRatio)

        for block, details in incident_details.items():
            block_label = QLabel(block)
            block_label.setFont(QFont("Arial", 14, QFont.Bold))
            scroll_layout.addWidget(block_label)

            top_incidents = details.most_common(5)
            max_count = top_incidents[0][1] if top_incidents else 0
            for incident, count in top_incidents:
                incident_layout = QHBoxLayout()
                incident_label = QLabel(f"{incident}: {count}")
                incident_label.setFont(QFont("Arial", 12))
                incident_layout.addWidget(incident_label)
                if count == max_count:
                    arrow_label = QLabel()
                    arrow_label.setPixmap(arrow_up_pixmap)
                    incident_layout.addWidget(arrow_label)
                scroll_layout.addLayout(incident_layout)

        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)


class GraphDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Gráfico de Incidencias")
        self.setGeometry(300, 300, 800, 600)

        self.data = data

        layout = QVBoxLayout()

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.fullscreen_button = QPushButton("Pantalla Completa")
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        layout.addWidget(self.fullscreen_button)

        self.setLayout(layout)
        self.generate_charts()

    def generate_charts(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        all_incidents = []
        for data in self.data.values():
            all_incidents.extend(data['incidences'])

        counter = Counter(all_incidents)

        if counter:
            incidents, counts = zip(*counter.items())
            ax.bar(incidents, counts)
            ax.set_xlabel('Incidencias')
            ax.set_ylabel('Número de Incidencias')
            ax.set_title('Distribución de Incidencias')
            ax.tick_params(axis='x', rotation=45)
        else:
            ax.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

        self.canvas.draw()

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.fullscreen_button.setText("Pantalla Completa")
        else:
            self.showFullScreen()
            self.fullscreen_button.setText("Salir de Pantalla Completa")
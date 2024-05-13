import sys
import os
from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QMessageBox, QTabWidget, QLabel,
    QListWidget, QListWidgetItem, QStatusBar, QLineEdit, QFileDialog, QHBoxLayout, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QRect
from PyQt5.QtGui import QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class LoginWindow(QWidget):
    login_successful = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión")
        self.resize(280, 360)
        self.center_window()

        layout = QVBoxLayout()
        logo_label = QLabel("Inicio de Sesión")
        layout.addWidget(logo_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        login_button = QPushButton("Confirmar")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def center_window(self):
        screen_rect = QApplication.desktop().availableGeometry()
        x = (screen_rect.width() - self.width()) // 2
        y = (screen_rect.height() - self.height()) // 2
        self.setGeometry(QRect(x, y, self.width(), self.height()))

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username == "ficosa_pideu" and password == "1111":
            self.login_successful.emit()
            self.close()
        else:
            QMessageBox.warning(self, "Error de Inicio de Sesión", "Usuario o contraseña incorrectos")


class TicketManagement(QMainWindow):
    config_file = "config.txt"

    def __init__(self):
        super().__init__()
        self.excel_file = None
        self.blocks = ["WC47 NACP", "WC48 POWER 5F", "WC49 POWER 5H", "WV50 FILTER", "SPL"]
        self.last_incidence_labels = {}
        self.incidencias = {
            "WC47 NACP": ["Etiquetadora", "Fallo en elevador", "No atornilla tapa", "Fallo tolva",
                        "Fallo en paletizador", "No coge placa", "Palet atascado en la curva",
                        "Ascensor no sube", "No pone tornillo", "Fallo tornillo", "AOI no detecta pieza",
                        "No atornilla clips", "Fallo fijador tapa", "Secuencia atornillador",
                        "Fallo atornillador", "Fallo cámara visión"],
            "WC48 POWER 5F": ["Etiquetadora","AOI (fallo etiqueta)","AOI (malla)","Cámara no detecta Pcb","Cámara no detecta skeleton",
                        "Cámara no detecta foams","Cámara no detecta busbar","Cámara no detecta foam derecho","No detecta presencia power CP",
                        "Tornillo atascado en tolva","Cámara no detecta Power CP","Cámara no detecta Top cover","Detección de sealling mal puesto",
                        "Robot no coge busbar","Fallo etiqueta","Power atascado en prensa, cuesta sacar","No coloca bien el sealling"],
            "WC49 POWER 5H": ["La cámara no detecta Busbar","La cámara no detecta Top Cover","Screw K30 no lo detecta puesto","Atasco tuerca",
                        "Tornillo atascado","Etiquetadora","Detección de sealling mal puesto","No coloca bien el sealling","Power atascado en prensa, cuesta sacar",
                        "No lee QR"],
            "WV50 FILTER": ["Fallo cámara ferrite","NOK Soldadura Plástico","NOK Soldadura metal","Traza","NOK Soldad. Plástico+Metal","Robot no coloca bien filter en palet",
                        "No coloca bien la pcb","QR desplazado","Core enganchado","Robot no coge PCB","Fallo atornillador","Pieza enganchada en HV Test","Cover atascado",
                        "Robot no coloca bien ferrita","No coloca bien el core","Fallo Funcional","Fallo visión core","Fallo cámara cover","Repeat funcional","Fallo cámara QR",
                        "No coloca bien foam"],
            "SPL": ["Sensor de PCB detecta que hay placa cuando no la hay","No detecta marcas Power","Colisión placas","Fallo dispensación glue","Marco atascado en parte inferior",
                    "Soldadura defectuosa","Error en sensor de salida"]
        }
        self.initUI()
        self.load_last_excel_file()

    def initUI(self):
        self.setWindowTitle("Ticket Management")
        self.setGeometry(200, 200, 900, 600)

        main_layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Sección de Tabs de Incidencias
        self.tabWidget = QTabWidget(self)
        main_layout.addWidget(self.tabWidget, 2)

        for name, incidences in self.incidencias.items():
            self.create_tab(name, incidences)

        # Sección para Seleccionar Excel y mostrar incidencias confirmadas
        right_layout = QVBoxLayout()
        select_excel_button = QPushButton("Seleccionar Archivo Excel", self)
        select_excel_button.clicked.connect(self.select_excel_file)
        right_layout.addWidget(select_excel_button)

        self.excel_path_display = QLineEdit(self)
        self.excel_path_display.setReadOnly(True)
        right_layout.addWidget(self.excel_path_display)

        self.table_widget = QTableWidget(self)
        self.table_widget.setFixedSize(600, 400)  # Tamaño fijo para la tabla
        right_layout.addWidget(self.table_widget)

        self.confirmed_incidence_display = QLabel("Información de la última incidencia confirmada:")
        self.confirmed_incidence_display.setWordWrap(True)  # Permite el ajuste automático de texto
        right_layout.addWidget(self.confirmed_incidence_display)
        
        right_layout.addStretch()

        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        main_layout.addWidget(right_widget, 1)

        # Barra de estado para mostrar mensajes
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        timer = QTimer(self)
        timer.timeout.connect(self.update_status_bar)
        timer.start(1000)

        self.apply_styles()

    def create_tab(self, name, incidences):
        tab = QWidget()
        self.tabWidget.addTab(tab, name)
        layout = QVBoxLayout(tab)

        title = QLabel(f"Incidencias - {name}")
        layout.addWidget(title)

        last_incidence_label = QLabel("Última incidencia: Ninguna")
        layout.addWidget(last_incidence_label)
        self.last_incidence_labels[name] = last_incidence_label

        list_widget = QListWidget()
        for incidence in incidences:
            item = QListWidgetItem(incidence)
            list_widget.addItem(item)

        layout.addWidget(list_widget)

        confirm_button = QPushButton("Confirmar Incidencia")
        confirm_button.clicked.connect(lambda: self.report_incidence(name, list_widget))
        layout.addWidget(confirm_button)

    def report_incidence(self, block_name, list_widget):
        current_item = list_widget.currentItem()
        if current_item:
            incidence_text = current_item.text()
            timestamp = datetime.now()
            date_str = timestamp.strftime("%Y-%m-%d")
            time_str = timestamp.strftime("%H:%M:%S")
            self.last_incidence_labels[block_name].setText(f"Incidencia confirmada: {incidence_text} a las {time_str}")
            self.log_incidence_to_excel(block_name, date_str, time_str, incidence_text)

            # Mostrar el cuadro de diálogo de confirmación
            QMessageBox.information(self, "Confirmación", "Incidencia confirmada.")

            # Actualizar la tabla y la información de la incidencia confirmada
            self.update_excel_table()
            self.confirmed_incidence_display.setText(
                f"Última incidencia confirmada: {incidence_text} en {block_name} a las {time_str} del {date_str}"
            )
        else:
            QMessageBox.warning(self, "Ninguna Incidencia Seleccionada", "Selecciona una incidencia para confirmar.")

    def select_excel_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Archivos Excel (*.xlsx)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.excel_file = file_path
            self.excel_path_display.setText(file_path)
            with open(self.config_file, "w") as config:
                config.write(file_path)
            self.create_excel_if_not_exists(file_path)
            self.update_excel_table()

    def create_excel_if_not_exists(self, file_path):
        if not os.path.exists(file_path):
            workbook = Workbook()
            sheet = workbook.active
            headers = ["Fecha", "Hora"] + self.blocks  # Cabeceras con los nombres de los bloques
            sheet.append(headers)
            workbook.save(file_path)

    def log_incidence_to_excel(self, block_name, date_str, time_str, incidence_text):
        if self.excel_file and os.path.exists(self.excel_file):
            try:
                workbook = load_workbook(self.excel_file)
                sheet = workbook.active
                new_row = [date_str, time_str] + ["-"] * len(self.blocks)
                if block_name in self.blocks:
                    new_row[self.blocks.index(block_name) + 2] = incidence_text  # Asegúrate de ajustar el índice correctamente

                sheet.append(new_row)
                workbook.save(self.excel_file)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al guardar en el archivo Excel: {e}")
        else:
            QMessageBox.warning(self, "Archivo no encontrado", "Selecciona un archivo Excel válido.")

    def update_status_bar(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_bar.showMessage(f"Hora actual: {current_time}")

    def load_last_excel_file(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as config:
                file_path = config.read().strip()
                if os.path.exists(file_path):
                    self.excel_file = file_path
                    self.excel_path_display.setText(file_path)
                    self.update_excel_table()

    def update_excel_table(self):
        if self.excel_file and os.path.exists(self.excel_file):
            workbook = load_workbook(self.excel_file)
            sheet = workbook.active
            rows = list(sheet.iter_rows(values_only=True))

            # Definir siempre las cabeceras como los bloques de la aplicación
            headers = ["Fecha", "Hora"] + self.blocks
            self.table_widget.setColumnCount(len(headers))
            self.table_widget.setHorizontalHeaderLabels(headers)

            if rows:
                self.table_widget.setRowCount(len(rows) - 1)  # -1 porque la primera fila son las cabeceras
                for row_idx, row_data in enumerate(rows[1:], start=1):
                    for col_idx, cell_value in enumerate(row_data):
                        self.table_widget.setItem(row_idx - 1, col_idx, QTableWidgetItem(str(cell_value) if cell_value else "-"))
            else:
            # Si el archivo está vacío, solo inicializa las cabeceras
                self.table_widget.setRowCount(0)
        else:
            QMessageBox.warning(self, "Archivo no encontrado", "No se encontró el archivo Excel válido.")
        # Inicializar la tabla con las cabeceras de los bloques pero sin filas
            headers = ["Fecha", "Hora"] + self.blocks
            self.table_widget.setColumnCount(len(headers))
            self.table_widget.setRowCount(0)
            self.table_widget.setHorizontalHeaderLabels(headers)


    def apply_styles(self):
        font = QFont()
        font.setPointSize(12)  # Cambiar este valor para ajustar el tamaño de la fuente
        self.setFont(font)

        for widget in self.findChildren(QWidget):
            widget.setFont(font)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    main_window = TicketManagement()
    login_window.login_successful.connect(main_window.show)
    login_window.show()
    sys.exit(app.exec_())
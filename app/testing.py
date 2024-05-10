import sys
import os
from openpyxl import Workbook, load_workbook
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QMessageBox, QTabWidget, QLabel, QListWidget, QListWidgetItem, QStatusBar, QLineEdit, QFileDialog, QHBoxLayout
)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QRect


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
            "WC47 NACP": ["Etiquetadora", "Fallo en elevador"],
            "WC48 POWER 5F": ["Etiquetadora", "AOI (fallo etiqueta)"],
            "WC49 POWER 5H": ["La cámara no detecta Busbar"],
            "WV50 FILTER": ["Fallo cámara ferrite"],
            "SPL": ["Sensor de PCB detecta que hay placa cuando no la hay"]
        }
        self.initUI()

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

        # Sección para Seleccionar Excel
        excel_selector_layout = QVBoxLayout()
        select_excel_button = QPushButton("Seleccionar Archivo Excel", self)
        select_excel_button.clicked.connect(self.select_excel_file)
        excel_selector_layout.addWidget(select_excel_button)
        excel_selector_layout.addStretch()

        excel_selector_widget = QWidget()
        excel_selector_widget.setLayout(excel_selector_layout)
        main_layout.addWidget(excel_selector_widget, 1)

        # Barra de estado para mostrar mensajes
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        timer = QTimer(self)
        timer.timeout.connect(self.update_status_bar)
        timer.start(1000)

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
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.last_incidence_labels[block_name].setText(f"Incidencia confirmada: {incidence_text} a las {timestamp}")
            self.log_incidence_to_excel(block_name, incidence_text)

            # Mostrar el cuadro de diálogo de confirmación
            QMessageBox.information(self, "Confirmación", "Incidencia confirmada.")
        else:
            QMessageBox.warning(self, "Ninguna Incidencia Seleccionada", "Selecciona una incidencia para confirmar.")

    def select_excel_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Archivos Excel (*.xlsx)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.excel_file = file_path
            with open(self.config_file, "w") as config:
                config.write(file_path)
            self.create_excel_if_not_exists(file_path)

    def create_excel_if_not_exists(self, file_path):
        if not os.path.exists(file_path):
            workbook = Workbook()
            sheet = workbook.active
            sheet.append(["Timestamp"] + self.blocks)
            workbook.save(file_path)

    def log_incidence_to_excel(self, block_name, incidence_text):
        if self.excel_file and os.path.exists(self.excel_file):
            try:
                workbook = load_workbook(self.excel_file)
                sheet = workbook.active
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_row = [timestamp] + [""] * len(self.blocks)
                if block_name in self.blocks:
                    new_row[self.blocks.index(block_name) + 1] = incidence_text
                sheet.append(new_row)
                workbook.save(self.excel_file)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al guardar en el archivo Excel: {e}")
        else:
            QMessageBox.warning(self, "Archivo no encontrado", "Selecciona un archivo Excel válido.")

    def update_status_bar(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_bar.showMessage(f"Hora actual: {current_time}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    main_window = TicketManagement()
    login_window.login_successful.connect(main_window.show)
    login_window.show()
    sys.exit(app.exec_())

import sys
import json
import csv
import os

from openpyxl import Workbook, load_workbook

from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QMessageBox, QTabWidget, QLabel, QListWidget, QListWidgetItem, QStatusBar, QHBoxLayout, QLineEdit, QFileDialog
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QUrl, QByteArray, QTimer, Qt, pyqtSignal, QRect


class LoginWindow(QWidget):
    login_successful = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión")
        self.resize(280, 360)

        self.center_window()

        layout = QVBoxLayout()

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("app/logo.png").scaled(180, 180, Qt.KeepAspectRatio)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Etiquetas personalizadas de "Usuario" y "Contraseña"
        user_label = QLabel("Usuario")
        password_label = QLabel("Contraseña")

        # Configura estilos con el método setStyleSheet
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
            }
            QLabel {
                font-size: 20px;
                color: #34495e;
                margin-bottom: 5px;
            }
            QLineEdit {
                font-size: 28px;
                padding: 20px;
                margin: 10px 0;
                border: 2px solid #2980b9;
                border-radius: 8px;
                background-color: #f0f4f8;
            }
            QPushButton {
                background-color: #2980b9;
                color: #ffffff;
                border-radius: 8px;
                font-size: 20px;
                height: 60px;
                margin-top: 15px;
            }
        """)

        # Campo de entrada de "Usuario"
        layout.addWidget(user_label)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("User")
        layout.addWidget(self.username_input)

        # Campo de entrada de "Contraseña"
        layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Botón de inicio de sesión
        login_button = QPushButton("Confirmar")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def center_window(self):
        # Rectángulo del escritorio
        screen_rect = QApplication.desktop().availableGeometry()
        # Coordenadas
        x = (screen_rect.width() - self.width()) // 2
        y = (screen_rect.height() - self.height()) // 2
        # Posicionar la ventana
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
    last_incidence_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.last_incidence_labels = {}
        self.initUI()
        self.network_manager = QNetworkAccessManager(self)
        self.network_manager.finished.connect(self.on_network_reply)
        self.last_incidence = None
        self.blocks = ["WC47 NACP", "WC48 POWER 5F", "WC49 POWER 5H", "WV50 FILTER", "SPL"]
        self.excel_file = None  # Se inicializa como None antes de ser asignado
        self.select_or_create_excel_file()  # Llamar a la nueva función

    def initUI(self):
        # Rectángulo del escritorio
        screen_rect_1 = QApplication.desktop().availableGeometry()
        # Coordenadas
        x = (screen_rect_1.width() - self.width()) // 2
        y = (screen_rect_1.height() - self.height()) // 2
        # Posicionar la ventana
        self.setGeometry(QRect(x, y, self.width(), self.height()))
        self.setWindowTitle("Ticket Management")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f6f7;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                padding: 5px 50px;
                font-size: 18px;
                height: 40px;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QListWidget::item {
                padding: 5px;
                border: 1px solid #dcdcdc;
                border-radius: 3px;
            }
            QTabWidget {
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
            }
        """)

        self.tabWidget = QTabWidget(self)
        self.tabWidget.setFont(QFont('Arial', 12))
        self.setCentralWidget(self.tabWidget)

        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.update_status_bar()

        timer = QTimer(self)
        timer.timeout.connect(self.update_status_bar)
        timer.start(1000)

        self.incidencias = {
            "WC47 NACP": ["Etiquetadora", "Fallo en elevador", "No atornilla tapa", "Fallo tolva",
                        "Fallo en paletizador", "No coge placa", "Palet atascado en la curva",
                        "Ascensor no sube", "No pone tornillo", "Fallo tornillo", "AOI no detecta pieza",
                        "No atornilla clips", "Fallo fijador tapa", "Secuencia atornillador",
                        "Fallo atornillador", "Fallo cámara visión"],
            "WC48 POWER 5F": ["Etiquetadora", "AOI (fallo etiqueta)", "AOI (malla)", "Cámara no detecta Pcb", "Cámara no detecta skeleton",
                            "Cámara no detecta foams", "Cámara no detecta busbar", "Cámara no detecta foam derecho", "No detecta presencia power CP",
                            "Tornillo atascado en tolva", "Cámara no detecta Power CP", "Cámara no detecta Top cover", "Detección de sealling mal puesto",
                            "Robot no coge busbar", "Fallo etiqueta", "Power atascado en prensa, cuesta sacar", "No coloca bien el sealling"],
            "WC49 POWER 5H": ["La cámara no detecta Busbar", "La cámara no detecta Top Cover", "Screw K30 no lo detecta puesto", "Atasco tuerca",
                            "Tornillo atascado", "Etiquetadora", "Detección de sealling mal puesto", "No coloca bien el sealling", "Power atascado en prensa, cuesta sacar",
                            "No lee QR"],
            "WV50 FILTER": ["Fallo cámara ferrite", "NOK Soldadura Plástico", "NOK Soldadura metal", "Traza", "NOK Soldad. Plástico+Metal", "Robot no coloca bien filter en palet",
                            "No coloca bien la pcb", "QR desplazado", "Core enganchado", "Robot no coge PCB", "Fallo atornillador", "Pieza enganchada en HV Test", "Cover atascado",
                            "Robot no coloca bien ferrita", "No coloca bien el core", "Fallo Funcional", "Fallo visión core", "Fallo cámara cover", "Repeat funcional", "Fallo cámara QR",
                            "No coloca bien foam"],
            "SPL": ["Sensor de PCB detecta que hay placa cuando no la hay", "No detecta marcas Power", "Colisión placas", "Fallo dispensación glue", "Marco atascado en parte inferior",
                    "Soldadura defectuosa", "Error en sensor de salida"]
        }

        for name, incidences in self.incidencias.items():
            self.create_tab(name, incidences)

    def create_tab(self, name, incidences):
        tab = QWidget()
        self.tabWidget.addTab(tab, name)
        layout = QVBoxLayout(tab)

        title = QLabel(f"Incidencias - {name}")
        title.setFont(QFont('Arial', 16))
        layout.addWidget(title)

        last_incidence_label = QLabel("Última incidencia: Ninguna")
        last_incidence_label.setFont(QFont('Arial', 40))
        layout.addWidget(last_incidence_label)
        self.last_incidence_labels[name] = last_incidence_label

        list_widget = QListWidget()
        for incidence in incidences:
            item = QListWidgetItem(incidence)
            list_widget.addItem(item)
        list_widget.itemClicked.connect(self.report_incidence)
        layout.addWidget(list_widget)

    def report_incidence(self, item):
        current_tab = self.tabWidget.currentWidget()
        tab_name = self.tabWidget.tabText(self.tabWidget.indexOf(current_tab))
        self.last_incidence = f"Incidencia reportada en {tab_name}: {item.text()} a las {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.last_incidence_labels[tab_name].setText(self.last_incidence)
        self.last_incidence_changed.emit()

        # Llamar a la función para guardar en Excel
        self.log_incidence_to_excel(tab_name, item.text())

    def select_or_create_excel_file(self):
        """Función que permite al usuario seleccionar un archivo Excel existente o crear uno nuevo"""
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        file_dialog.setNameFilter("Excel Files (*.xlsx)")
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setOption(QFileDialog.DontUseNativeDialog, False)
        file_dialog.setLabelText(QFileDialog.Accept, "Abrir")
        file_dialog.setLabelText(QFileDialog.Reject, "Cancelar")
        file_dialog.setWindowTitle("Seleccionar archivo Excel existente o crear uno nuevo")

        # Mostrar el cuadro de diálogo y obtener el nombre del archivo
        if file_dialog.exec_() == QFileDialog.Accepted:
            selected_file = file_dialog.selectedFiles()[0]
            if not selected_file.endswith(".xlsx"):
                selected_file += ".xlsx"

            # Verificar si el archivo ya existe o si es nuevo
            if os.path.exists(selected_file):
                self.excel_file = selected_file
            else:
                self.create_excel_file(selected_file)
        else:
            QMessageBox.warning(self, "Selección de archivo cancelada", "Por favor, seleccione un archivo Excel válido.")

    def create_excel_file(self, file_path):
        """Función para crear un nuevo archivo Excel"""
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Incidencias"
        worksheet.append(["Fecha", "Hora", "Bloque", "Incidencia"])
        workbook.save(file_path)
        self.excel_file = file_path

    def log_incidence_to_excel(self, block_name, incidence):
        """Función para registrar incidencias en el archivo Excel"""
        if self.excel_file:
            try:
                workbook = load_workbook(self.excel_file)
                worksheet = workbook.active
                current_datetime = datetime.now()
                worksheet.append([current_datetime.strftime("%Y-%m-%d"), current_datetime.strftime("%H:%M:%S"), block_name, incidence])
                workbook.save(self.excel_file)
                self.status_bar.showMessage(f"Incidencia '{incidence}' registrada exitosamente.", 5000)
            except Exception as e:
                QMessageBox.critical(self, "Error al guardar", f"No se pudo guardar la incidencia en el archivo Excel: {e}")
        else:
            QMessageBox.warning(self, "Error de archivo Excel", "No se ha seleccionado un archivo Excel válido.")

    def update_status_bar(self):
        if self.last_incidence:
            self.status_bar.showMessage(self.last_incidence)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    ticket_management = TicketManagement()

    login_window.login_successful.connect(ticket_management.show)

    login_window.show()
    sys.exit(app.exec_())
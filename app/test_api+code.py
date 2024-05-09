import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton, QMessageBox, QTabWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QUrl, QByteArray

class TicketManagement(QMainWindow):
    def __init__(self):
        super().__init__()
        self.network_manager = QNetworkAccessManager(self)
        self.network_manager.finished.connect(self.on_network_reply)  # Manejar la respuesta de la red
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ticket Management")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #D1D3C4;
            }
            QTabWidget::pane {
                border-top: 1px solid #D1D3C4;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background: #FBFBFF;
                font: bold 20px;
                border: 1.5px solid #1e1e1e;
                min-width: 40ex;
                padding: 10px;
            }
            QTabBar::tab:selected {
                background: #E2C044;
                margin-bottom: -5px;
            }
            QComboBox {
                border: 0px solid #555;
                border-radius: 5px;
                padding: 1em;
                min-width: 6em;
                font-size: 20px;
                color: #1E2019;
            }
            QPushButton {
                background-color: #E2C044;
                border: none;
                color: black;
                padding: 15px 32px;
                text-align: center;
                display: inline-block;
                font-size: 25px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #393E41;
            }
        """)
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setFont(QFont('Arial', 12))
        self.setCentralWidget(self.tabWidget)

        # Incidencias
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


        for name, incidences in self.incidencias.items():
            self.create_tab(name, incidences)

    def create_tab(self, name, incidences):
        tab = QWidget()
        self.tabWidget.addTab(tab, name)
        layout = QVBoxLayout(tab)
        comboBox = QComboBox()
        comboBox.addItems(incidences)
        layout.addWidget(comboBox)
        confirmButton = QPushButton("Confirmar")
        confirmButton.clicked.connect(lambda: self.on_confirm(name, comboBox))
        layout.addWidget(confirmButton)

    def on_confirm(self, name, comboBox):
        selected_incidence = comboBox.currentText()
        self.send_data(name, selected_incidence)

    def send_data(self, block, incidence):
        data = {
            "bloque": block,
            "incidencia": incidence
        }
        url = QUrl("http://fe80::a038:8aec:6233:c933%10:5000/report_incidence")
        req = QNetworkRequest(url)
        req.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        self.network_manager.post(req, QByteArray(json.dumps(data).encode('utf-8')))

    def on_network_reply(self, reply):
        if reply.error():
            QMessageBox.warning(self, "Network Error", "Failed to communicate with the API: " + reply.errorString())
        else:
            response = json.loads(reply.readAll().data().decode())
            QMessageBox.information(self, "API Response", response.get("message", "No message received"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TicketManagement()
    sys.exit(app.exec_())

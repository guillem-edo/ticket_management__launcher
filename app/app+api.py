import sys
import json
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton, QMessageBox, QTabWidget
from PyQt5.QtGui import QFont
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QUrl, QByteArray

class TicketManagement(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.network_manager = QNetworkAccessManager(self)
        self.network_manager.finished.connect(self.on_network_reply)  # Conectar la respuesta de red

    def initUI(self):
        self.setWindowTitle("Ticket Management")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""<Estilos CSS Aquí>""")
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setFont(QFont('Arial', 12))
        self.setCentralWidget(self.tabWidget)

        # Definición de incidencias
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

        # Creación de pestañas para cada bloque de incidencias
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
        confirmButton.clicked.connect(lambda: self.on_confirm(name, comboBox.currentText()))
        layout.addWidget(confirmButton)

    def on_confirm(self, name, incidence):
        self.send_data_to_api(name, incidence)
        self.write_to_csv(name, incidence)

    def send_data_to_api(self, block, incidence):
        data = {"bloque": block, "incidencia": incidence}
        url = QUrl("http://1000:5000/report_incidence")
        req = QNetworkRequest(url)
        req.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        self.network_manager.post(req, QByteArray(json.dumps(data).encode('utf-8')))

    def write_to_csv(self, block, incidence):
        with open(self.csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([block, incidence, timestamp])
        pass

    def on_network_reply(self, reply):
        err = reply.error()
        if err != QNetworkReply.NoError:
            error_message = reply.errorString()
            QMessageBox.warning(self, "Error de Red", f"Error al comunicar con la API: {error_message}")
        else:
            response = json.loads(reply.readAll().decode())
            QMessageBox.information(self, "Respuesta de la API", response.get("message", "No se recibió mensaje"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TicketManagement()
    sys.exit(app.exec_())
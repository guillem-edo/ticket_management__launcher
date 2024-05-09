import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton, QMessageBox, QTabWidget
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QUrl, QByteArray


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
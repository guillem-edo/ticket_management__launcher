from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import os
from fpdf import FPDF

class SendReportDialog(QDialog):
    def __init__(self, incidencias, email_notifier, parent=None):
        super(SendReportDialog, self).__init__(parent)
        self.incidencias = incidencias
        self.email_notifier = email_notifier
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Enviar Informe por Correo")
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout(self)

        self.label = QLabel("Introduce el correo electrónico del destinatario:", self)
        layout.addWidget(self.label)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("correo@ejemplo.com")
        layout.addWidget(self.email_input)

        self.send_button = QPushButton("Enviar Informe", self)
        self.send_button.setStyleSheet(self.get_button_style())
        self.send_button.clicked.connect(self.send_report)
        layout.addWidget(self.send_button)

        self.close_button = QPushButton("Cerrar", self)
        self.close_button.setStyleSheet(self.get_button_style())
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def get_button_style(self):
        return """
            QPushButton {
                background-color: #5C85FF;
                color: white;
                padding: 10px 20px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #466BB7;
            }
        """

    def send_report(self):
        recipient = self.email_input.text()
        if recipient:
            subject = "Informe de Incidencias"
            message = "Adjunto encontrarás el informe de incidencias."
            attachment = self.create_pdf_report()

            if attachment:
                self.email_notifier.send_email_with_attachment(recipient, subject, message, attachment)
                QMessageBox.information(self, "Enviar Informe", "Informe enviado con éxito.")
                os.remove(attachment)
                self.close()
            else:
                QMessageBox.warning(self, "Error", "No se pudo generar el informe.")
        else:
            QMessageBox.warning(self, "Error", "Por favor, introduce un correo electrónico válido.")

    def create_pdf_report(self):
        file_name = "informe_incidencias.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Informe de Incidencias", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=10)
        for block, incidences in self.incidencias.items():
            pdf.cell(200, 10, txt=f"Bloque: {block}", ln=True, align='L')
            for incidence in incidences:
                pdf.cell(200, 10, txt=f"  - {incidence}", ln=True, align='L')
            pdf.ln(5)
        pdf.output(file_name)
        return file_name

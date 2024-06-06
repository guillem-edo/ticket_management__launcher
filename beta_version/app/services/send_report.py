from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
from fpdf import FPDF
from app.components.email_notifications import EmailNotifier
import os

class SendReportDialog(QDialog):
    def __init__(self, incidencias, parent=None):
        super(SendReportDialog, self).__init__(parent)
        self.incidencias = incidencias
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Enviar Informe por Correo")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout(self)

        self.service_label = QLabel("Selecciona el servicio de correo:", self)
        layout.addWidget(self.service_label)

        self.service_combo = QComboBox(self)
        self.service_combo.addItems(["Gmail", "Outlook"])
        layout.addWidget(self.service_combo)

        self.email_label = QLabel("Introduce tu correo electrónico:", self)
        layout.addWidget(self.email_label)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("tu_correo@example.com")
        layout.addWidget(self.email_input)

        self.password_label = QLabel("Introduce tu contraseña:", self)
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.recipient_label = QLabel("Introduce el correo electrónico del destinatario:", self)
        layout.addWidget(self.recipient_label)

        self.recipient_input = QLineEdit(self)
        self.recipient_input.setPlaceholderText("destinatario@example.com")
        layout.addWidget(self.recipient_input)

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
        service = self.service_combo.currentText().lower()
        email = self.email_input.text()
        password = self.password_input.text()
        recipient = self.recipient_input.text()

        if email and password and recipient:
            email_notifier = EmailNotifier(service, email, password)
            subject = "Informe de Incidencias"
            message = "Adjunto encontrarás el informe de incidencias."
            attachment = self.create_pdf_report()

            if attachment:
                email_notifier.send_email_with_attachment(recipient, subject, message, attachment)
                QMessageBox.information(self, "Enviar Informe", "Informe enviado con éxito.")
                os.remove(attachment)
                self.close()
            else:
                QMessageBox.warning(self, "Error", "No se pudo generar el informe.")
        else:
            QMessageBox.warning(self, "Error", "Por favor, completa todos los campos.")

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
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
import os
from fpdf import FPDF

class ReportExportDialog(QDialog):
    def __init__(self, incidencias, parent=None):
        super(ReportExportDialog, self).__init__(parent)
        self.incidencias = incidencias
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Exportar Informes")
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout(self)

        self.label = QLabel("Seleccione el formato de exportación:", self)
        layout.addWidget(self.label)

        self.csv_button = QPushButton("Exportar como CSV", self)
        self.csv_button.setStyleSheet(self.get_button_style())
        self.csv_button.clicked.connect(self.export_csv)
        layout.addWidget(self.csv_button)

        self.pdf_button = QPushButton("Exportar como PDF", self)
        self.pdf_button.setStyleSheet(self.get_button_style())
        self.pdf_button.clicked.connect(self.export_pdf)
        layout.addWidget(self.pdf_button)

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

    def export_csv(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar Informe CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write("Bloque,Incidencia,Fecha,Hora,Turno,Hora de Reparación,Tiempo de Reparación,MTBF\n")
                for block, incidences in self.incidencias.items():
                    for incidence in incidences:
                        file.write(f"{block},{incidence}\n")
            QMessageBox.information(self, "Exportar Informe", "Informe exportado con éxito en formato CSV.")

    def export_pdf(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar Informe PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if file_name:
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
            QMessageBox.information(self, "Exportar Informe", "Informe exportado con éxito en formato PDF.")
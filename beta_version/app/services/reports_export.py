from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QCheckBox, QPushButton, QFileDialog, QMessageBox
from fpdf import FPDF
import os

class ExportReportDialog(QDialog):
    def __init__(self, incidencias, parent=None):
        super(ExportReportDialog, self).__init__(parent)
        self.incidencias = incidencias
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Exportar Informe")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout(self)

        self.label = QLabel("Seleccione la información a incluir en el informe:", self)
        layout.addWidget(self.label)

        self.include_block = QCheckBox("Incluir Bloque", self)
        self.include_block.setChecked(True)
        layout.addWidget(self.include_block)

        self.include_incidence = QCheckBox("Incluir Incidencia", self)
        self.include_incidence.setChecked(True)
        layout.addWidget(self.include_incidence)

        self.include_date = QCheckBox("Incluir Fecha", self)
        self.include_date.setChecked(True)
        layout.addWidget(self.include_date)

        self.include_time = QCheckBox("Incluir Hora", self)
        self.include_time.setChecked(True)
        layout.addWidget(self.include_time)

        self.include_turno = QCheckBox("Incluir Turno", self)
        self.include_turno.setChecked(True)
        layout.addWidget(self.include_turno)

        self.include_repair_time = QCheckBox("Incluir Hora de Reparación", self)
        self.include_repair_time.setChecked(True)
        layout.addWidget(self.include_repair_time)

        self.include_mtbf = QCheckBox("Incluir MTBF", self)
        self.include_mtbf.setChecked(True)
        layout.addWidget(self.include_mtbf)

        self.export_button = QPushButton("Exportar a PDF", self)
        self.export_button.setStyleSheet(self.get_button_style())
        self.export_button.clicked.connect(self.export_pdf)
        layout.addWidget(self.export_button)

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
                if self.include_block.isChecked():
                    pdf.cell(200, 10, txt=f"Bloque: {block}", ln=True, align='L')
                for incidence in incidences:
                    if self.include_incidence.isChecked():
                        pdf.cell(200, 10, txt=f"  - Incidencia: {incidence['text']}", ln=True, align='L')
                    if self.include_date.isChecked():
                        pdf.cell(200, 10, txt=f"    Fecha: {incidence['date']}", ln=True, align='L')
                    if self.include_time.isChecked():
                        pdf.cell(200, 10, txt=f"    Hora: {incidence['time']}", ln=True, align='L')
                    if self.include_turno.isChecked():
                        pdf.cell(200, 10, txt=f"    Turno: {incidence['turno']}", ln=True, align='L')
                    if self.include_repair_time.isChecked():
                        pdf.cell(200, 10, txt=f"    Hora de Reparación: {incidence['repair_time']}", ln=True, align='L')
                    if self.include_mtbf.isChecked():
                        pdf.cell(200, 10, txt=f"    MTBF: {incidence['mtbf']}", ln=True, align='L')
                    pdf.ln(5)
                pdf.ln(10)
            pdf.output(file_name)
            QMessageBox.information(self, "Exportar Informe", "Informe exportado con éxito en formato PDF.")

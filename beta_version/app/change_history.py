from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton
import json

class ChangeHistoryDialog(QDialog):
    def __init__(self, change_log_file, parent=None):
        super(ChangeHistoryDialog, self).__init__(parent)
        self.change_log_file = change_log_file
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Historial de Cambios")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout(self)

        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)

        self.close_button = QPushButton("Cerrar", self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.load_history()

    def load_history(self):
        try:
            with open(self.change_log_file, 'r') as file:
                for line in file:
                    change = json.loads(line.strip())
                    self.display_change(change)
        except Exception as e:
            print(f"Error loading change history: {e}")

    def display_change(self, change):
        user = change.get("user", "Desconocido")
        action = change.get("action", "Acción Desconocida")
        date = change.get("date", "Fecha Desconocida")
        details = change.get("details", "Detalles no disponibles")
        self.text_edit.append(f"Usuario: {user}\nAcción: {action}\nFecha: {date}\nDetalles: {details}\n{'-'*40}")

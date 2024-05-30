from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem
import json

class ChangeHistoryDialog(QDialog):
    def __init__(self, change_log_file, parent=None):
        super().__init__(parent)
        self.change_log_file = change_log_file
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Historial de Cambios")
        layout = QVBoxLayout(self)

        self.history_table = QTableWidget(self)
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Usuario", "Acción", "Fecha", "Detalles"])
        layout.addWidget(self.history_table)

        self.load_history()

    def load_history(self):
        with open(self.change_log_file, 'r') as file:
            changes = json.load(file)
            self.history_table.setRowCount(len(changes))
            for row, change in enumerate(changes):
                self.history_table.setItem(row, 0, QTableWidgetItem(change["user"]))
                self.history_table.setItem(row, 1, QTableWidgetItem(change["action"]))
                self.history_table.setItem(row, 2, QTableWidgetItem(change["date"]))
                self.history_table.setItem(row, 3, QTableWidgetItem(change["details"]))

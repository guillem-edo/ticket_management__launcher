# app/admin_dialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton, QInputDialog, QMessageBox

class AdminDialog(QDialog):
    def __init__(self, parent=None, incidencias=None):
        super().__init__(parent)
        self.setWindowTitle("Administrar Incidencias")
        self.setGeometry(300, 300, 600, 400)
        self.incidencias = incidencias

        layout = QVBoxLayout()

        self.block_selector = QListWidget()
        for block in self.incidencias.keys():
            self.block_selector.addItem(block)
        self.block_selector.currentItemChanged.connect(self.load_incidents)
        layout.addWidget(self.block_selector)

        self.incident_list = QListWidget()
        layout.addWidget(self.incident_list)

        button_layout = QHBoxLayout()
        add_button = QPushButton("Añadir Incidencia")
        add_button.clicked.connect(self.add_incident)
        button_layout.addWidget(add_button)

        edit_button = QPushButton("Editar Incidencia")
        edit_button.clicked.connect(self.edit_incident)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton("Eliminar Incidencia")
        delete_button.clicked.connect(self.delete_incident)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_incidents(self):
        current_block = self.block_selector.currentItem().text()
        self.incident_list.clear()
        for incident in self.incidencias[current_block]:
            self.incident_list.addItem(incident)

    def add_incident(self):
        current_block = self.block_selector.currentItem().text()
        incident, ok = QInputDialog.getText(self, "Añadir Incidencia", "Nombre de la Incidencia:")
        if ok and incident:
            self.incidencias[current_block].append(incident)
            self.load_incidents()

    def edit_incident(self):
        current_block = self.block_selector.currentItem().text()
        current_item = self.incident_list.currentItem()
        if current_item:
            incident, ok = QInputDialog.getText(self, "Editar Incidencia", "Nombre de la Incidencia:", text=current_item.text())
            if ok and incident:
                self.incidencias[current_block][self.incident_list.currentRow()] = incident
                self.load_incidents()

    def delete_incident(self):
        current_block = self.block_selector.currentItem().text()
        current_item = self.incident_list.currentItem()
        if current_item:
            reply = QMessageBox.question(self, "Eliminar Incidencia", f"¿Estás seguro de eliminar '{current_item.text()}'?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                del self.incidencias[current_block][self.incident_list.currentRow()]
                self.load_incidents()

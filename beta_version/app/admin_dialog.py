# app/admin_dialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QComboBox, QInputDialog
from PyQt5.QtCore import pyqtSignal

class AdminDialog(QDialog):
    incidences_modified = pyqtSignal()

    def __init__(self, parent=None, incidencias=None):
        super().__init__(parent)
        self.setWindowTitle("Administrar Incidencias")
        self.setGeometry(300, 300, 500, 400)
        self.incidencias = incidencias
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.block_selector = QComboBox()
        self.block_selector.addItems(self.incidencias.keys())
        self.block_selector.currentIndexChanged.connect(self.populate_incidences_list)
        layout.addWidget(self.block_selector)

        self.incidences_list = QListWidget()
        self.populate_incidences_list()
        layout.addWidget(self.incidences_list)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Añadir Incidencia")
        self.add_button.clicked.connect(self.add_incidence)
        button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Editar Incidencia")
        self.edit_button.clicked.connect(self.edit_incidence)
        button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Eliminar Incidencia")
        self.delete_button.clicked.connect(self.delete_incidence)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def populate_incidences_list(self):
        self.incidences_list.clear()
        selected_block = self.block_selector.currentText()
        for incidence in self.incidencias[selected_block]:
            self.incidences_list.addItem(incidence)

    def add_incidence(self):
        text, ok = QInputDialog.getText(self, "Añadir Incidencia", "Nombre de la nueva incidencia:")
        if ok and text:
            selected_block = self.block_selector.currentText()
            self.incidencias[selected_block].append(text)
            self.populate_incidences_list()
            self.incidences_modified.emit()

    def edit_incidence(self):
        selected_item = self.incidences_list.currentItem()
        if selected_item:
            incidence_text = selected_item.text()
            new_text, ok = QInputDialog.getText(self, "Editar Incidencia", "Nuevo nombre de la incidencia:", QLineEdit.Normal, incidence_text)
            if ok and new_text:
                selected_block = self.block_selector.currentText()
                self.incidencias[selected_block][self.incidencias[selected_block].index(incidence_text)] = new_text
                self.populate_incidences_list()
                self.incidences_modified.emit()

    def delete_incidence(self):
        selected_item = self.incidences_list.currentItem()
        if selected_item:
            incidence_text = selected_item.text()
            selected_block = self.block_selector.currentText()
            self.incidencias[selected_block].remove(incidence_text)
            self.populate_incidences_list()
            self.incidences_modified.emit()
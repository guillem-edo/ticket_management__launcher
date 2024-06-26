import json
import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QComboBox, QInputDialog, QMessageBox
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont

class AdminDialog(QDialog):
    incidences_modified = pyqtSignal()

    def __init__(self, parent=None, incidencias=None, config_file="incidencias_config.json"):
        super().__init__(parent)
        self.setWindowTitle("Administrar Incidencias")
        self.setGeometry(300, 300, 600, 500)
        self.config_file = config_file
        self.incidencias = self.load_incidencias() if incidencias is None else incidencias
        if not self.incidencias:
            print("Warning: No incidences loaded.")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title_label = QLabel("Administrador")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        self.block_selector = QComboBox()
        if self.incidencias:
            self.block_selector.addItems(self.incidencias.keys())
        else:
            print("Warning: No blocks to add to block selector.")
        self.block_selector.currentIndexChanged.connect(self.populate_incidences_list)
        layout.addWidget(self.block_selector)

        self.incidences_list = QListWidget()
        self.populate_incidences_list()
        layout.addWidget(self.incidences_list)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Añadir")
        self.add_button.clicked.connect(self.add_incidence)
        self.add_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px;")
        button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Editar")
        self.edit_button.clicked.connect(self.edit_incidence)
        self.edit_button.setStyleSheet("background-color: #f0ad4e; color: white; font-size: 16px;")
        button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Eliminar")
        self.delete_button.clicked.connect(self.delete_incidence)
        self.delete_button.setStyleSheet("background-color: #d9534f; color: white; font-size: 16px;")
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def populate_incidences_list(self):
        self.incidences_list.clear()
        selected_block = self.block_selector.currentText()
        if selected_block and selected_block in self.incidencias:
            for incidence in self.incidencias[selected_block]:
                self.incidences_list.addItem(incidence)
        else:
            print(f"Warning: Block '{selected_block}' not found in incidences.")

    def add_incidence(self):
        text, ok = QInputDialog.getText(self, "Añadir Incidencia", "Nombre de la nueva incidencia:")
        if ok and text:
            selected_block = self.block_selector.currentText()
            if text in self.incidencias[selected_block]:
                QMessageBox.warning(self, "Incidencia Duplicada", "La incidencia ya existe en el bloque seleccionado.")
            else:
                self.incidencias[selected_block].append(text)
                self.populate_incidences_list()
                self.save_incidencias()
                self.incidences_modified.emit()

    def edit_incidence(self):
        selected_item = self.incidences_list.currentItem()
        if selected_item:
            incidence_text = selected_item.text()
            new_text, ok = QInputDialog.getText(self, "Editar Incidencia", "Nuevo nombre de la incidencia:", QLineEdit.Normal, incidence_text)
            if ok and new_text:
                selected_block = self.block_selector.currentText()
                if new_text in self.incidencias[selected_block]:
                    QMessageBox.warning(self, "Incidencia Duplicada", "La incidencia ya existe en el bloque seleccionado.")
                else:
                    self.incidencias[selected_block][self.incidencias[selected_block].index(incidence_text)] = new_text
                    self.populate_incidences_list()
                    self.save_incidencias()
                    self.incidences_modified.emit()

    def delete_incidence(self):
        selected_item = self.incidences_list.currentItem()
        if selected_item:
            incidence_text = selected_item.text()
            selected_block = self.block_selector.currentText()
            self.incidencias[selected_block].remove(incidence_text)
            self.populate_incidences_list()
            self.save_incidencias()
            self.incidences_modified.emit()

    def save_incidencias(self):
        with open(self.config_file, "w") as file:
            json.dump(self.incidencias, file, indent=4)

    @staticmethod
    def load_incidencias(config_file="incidencias_config.json"):
        if os.path.exists(config_file):
            with open(config_file, "r") as file:
                try:
                    incidencias = json.load(file)
                    if not incidencias:
                        print("Warning: Loaded incidences are empty.")
                    return incidencias
                except json.JSONDecodeError:
                    print("Error: Failed to decode JSON from incidences file.")
                    return {}
        print(f"Error: Incidences file '{config_file}' not found.")
        return {}
# app/login_window.py
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QApplication
from PyQt5.QtCore import pyqtSignal, Qt, QRect
from PyQt5.QtGui import QFont, QPixmap
from beta_version.app.models.user import User

class LoginWindow(QWidget):
    login_successful = pyqtSignal(User)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión")
        self.resize(280, 360)
        self.center_window()
        self.setStyleSheet("background-color: white;")

        self.users = [
            User("pideu1", "1111", ["WC47 NACP"]),
            User("pideu2", "1111", ["WC48 P5F"]),
            User("pideu3", "1111", ["WC49 P5H"]),
            User("pideu4", "1111", ["WV50 FILTER"]),
            User("pideu5", "1111", ["SPL"]),
            User("admin", "admin", [], is_admin=True)  # Usuario administrador
        ]

        layout = QVBoxLayout()
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
        logo_pixmap = QPixmap(logo_path)

        if not logo_pixmap.isNull():
            logo_label = QLabel()
            logo_label.setPixmap(logo_pixmap.scaled(200, 200, Qt.KeepAspectRatio))
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)
        else:
            print("Warning: Logo not found!")

        font = QFont()
        font.setPointSize(12)

        self.username_input = QLineEdit()
        self.username_input.setFont(font)
        self.username_input.setPlaceholderText("Usuario")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setFont(font)
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        login_button = QPushButton("Confirmar")
        login_button.setFont(font)
        login_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px 20px; font-size: 16px;")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def center_window(self):
        screen_rect = QApplication.desktop().availableGeometry()
        x = (screen_rect.width() - self.width()) // 2
        y = (screen_rect.height() - self.height()) // 2
        self.setGeometry(QRect(x, y, self.width(), self.height()))

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        for user in self.users:
            if username == user.username and password == user.password:
                self.login_successful.emit(user)
                self.close()
                return
        QMessageBox.warning(self, "Error de Inicio de Sesión", "Usuario o contraseña incorrectos")
from PyQt5.QtWidgets import QApplication

def apply_dark_theme():
    app = QApplication.instance()
    dark_stylesheet = """
    QMainWindow {
        background-color: #2b2b2b;
    }
    QLabel, QLineEdit, QListWidget, QTableWidget, QPushButton {
        color: #ffffff;
        background-color: #444444;
        border: 1px solid #555555;
    }
    QPushButton:hover {
        background-color: #666666;
    }
    """
    app.setStyleSheet(dark_stylesheet)

def apply_light_theme():
    app = QApplication.instance()
    light_stylesheet = """
    QMainWindow {
        background-color: #f0f0f0;
    }
    QLabel, QLineEdit, QListWidget, QTableWidget, QPushButton {
        color: #000000;
        background-color: #ffffff;
        border: 1px solid #cccccc;
    }
    QPushButton:hover {
        background-color: #dddddd;
    }
    """
    app.setStyleSheet(light_stylesheet)
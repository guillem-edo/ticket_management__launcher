# theme_manager.py
from PyQt5.QtWidgets import QApplication

def apply_dark_theme():
    dark_stylesheet = """
    QMainWindow {
        background-color: #2e2e2e;
    }
    QLabel, QLineEdit, QPushButton {
        color: #ffffff;
    }
    QPushButton {
        background-color: #444444;
        border: 1px solid #555555;
    }
    """
    QApplication.instance().setStyleSheet(dark_stylesheet)

def apply_light_theme():
    light_stylesheet = """
    QMainWindow {
        background-color: #f5f5f5;
    }
    QLabel, QLineEdit, QPushButton {
        color: #000000;
    }
    QPushButton {
        background-color: #ffffff;
        border: 1px solid #cccccc;
    }
    """
    QApplication.instance().setStyleSheet(light_stylesheet)

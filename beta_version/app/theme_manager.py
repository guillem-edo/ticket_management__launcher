from PyQt5.QtWidgets import QApplication

def apply_dark_theme():
    app = QApplication.instance()
    dark_stylesheet = """
    QMainWindow {
        background-color: #2b2b2b;
        color: #ffffff;
    }
    QLabel, QLineEdit, QListWidget, QTableWidget, QPushButton {
        color: #ffffff;
        background-color: #444444;
        border: 1px solid #555555;
    }
    QPushButton:hover {
        background-color: #666666;
    }
    QTabWidget::pane {
        border: 1px solid #555555;
    }
    QTabBar::tab {
        background: #444444;
        color: #ffffff;
        padding: 10px;
    }
    QTabBar::tab:selected {
        background: #666666;
    }
    QStatusBar {
        background: #444444;
        color: #ffffff;
    }
    """
    app.setStyleSheet(dark_stylesheet)

def apply_light_theme():
    app = QApplication.instance()
    light_stylesheet = """
    QMainWindow {
        background-color: #f0f0f0;
        color: #000000;
    }
    QLabel, QLineEdit, QListWidget, QTableWidget, QPushButton {
        color: #000000;
        background-color: #ffffff;
        border: 1px solid #cccccc;
    }
    QPushButton:hover {
        background-color: #dddddd;
    }
    QTabWidget::pane {
        border: 1px solid #cccccc;
    }
    QTabBar::tab {
        background: #ffffff;
        color: #000000;
        padding: 10px;
    }
    QTabBar::tab:selected {
        background: #dddddd;
    }
    QStatusBar {
        background: #ffffff;
        color: #000000;
    }
    """
    app.setStyleSheet(light_stylesheet)
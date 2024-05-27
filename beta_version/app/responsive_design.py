# responsive_design.py
from PyQt5.QtWidgets import QApplication, QDesktopWidget

def center_window(window):
    screen_rect = QApplication.desktop().availableGeometry()
    window_width = window.width()
    window_height = window.height()
    x = (screen_rect.width() - window_width) // 2
    y = (screen_rect.height() - window_height) // 2
    window.setGeometry(x, y, window_width, window_height)

def adjust_to_screen(window):
    screen = QDesktopWidget().screenGeometry()
    window.resize(screen.width() * 0.8, screen.height() * 0.8)
    center_window(window)
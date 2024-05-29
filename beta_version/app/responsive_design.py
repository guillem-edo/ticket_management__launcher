from PyQt5.QtWidgets import QApplication

def center_window(window):
    screen_geometry = QApplication.desktop().screenGeometry()
    x = (screen_geometry.width() - window.width()) // 2
    y = (screen_geometry.height() - window.height()) // 2
    window.move(x, y)

def adjust_to_screen(window):
    screen = QApplication.desktop().screenGeometry()
    window.resize(int(screen.width() * 0.8), int(screen.height() * 0.8))
    center_window(window)
# notifications.py
from PyQt5.QtWidgets import QSystemTrayIcon, QStyle, QApplication, QMenu

class NotificationManager:
    def __init__(self):
        self.tray_icon = QSystemTrayIcon(QApplication.style().standardIcon(QStyle.SP_MessageBoxInformation))
        self.tray_icon.setVisible(True)

    def show_notification(self, title, message):
        self.tray_icon.showMessage(title, message, QSystemTrayIcon.Information, 3000)
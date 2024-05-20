# beta_version/app/beta_version.py
import sys
import os
from PyQt5.QtWidgets import QApplication

# Asegúrate de que el directorio 'beta_version/app' esté en sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from app.login_window import LoginWindow
from app.ticket_management import TicketManagement

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_window = LoginWindow()

    def on_login_successful(user):
        ticket_management = TicketManagement(user)
        ticket_management.show()

    login_window.login_successful.connect(on_login_successful)
    login_window.show()

    sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import QApplication
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
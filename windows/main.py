from PyQt5.QtWidgets import QApplication, QDialog
from login import LoginPage
from main_app import MainApp

if __name__ == "__main__":
    app = QApplication([])

    login_page = LoginPage()
    if login_page.exec_() == QDialog.Accepted:
        main_app = MainApp()
        main_app.show()

    app.exec_()
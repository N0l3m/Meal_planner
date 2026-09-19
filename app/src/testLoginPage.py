import sys
from PySide6 import QtWidgets

from login.loginPage import LoginPage

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    window = LoginPage()

    window.show()

    sys.exit(app.exec())
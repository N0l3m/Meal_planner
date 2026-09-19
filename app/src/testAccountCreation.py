import sys
from PySide6 import QtWidgets

from login.accountCreationPage import AccountCreationPage

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    window = AccountCreationPage()

    window.show()

    sys.exit(app.exec())
import sys
from PySide6 import QtWidgets

from mainWindow.mainWindow import MainWindow

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())
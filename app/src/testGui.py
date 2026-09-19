import sys
from PySide6 import QtWidgets

from gui.desktop import DesktopApi
from gui.smartphone import SmartphoneApi

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    # window = DesktopApi()
    window = SmartphoneApi()

    window.show()

    sys.exit(app.exec())
import sys
from PySide6 import QtWidgets

from plannerList.plannerListPage import PlannerListPage

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    window = PlannerListPage()

    window.show()

    sys.exit(app.exec())
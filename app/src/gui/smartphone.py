from PySide6 import QtWidgets, QtGui, QtCore
from gui.guiCalender import GuiCalender

class SmartphoneApi(GuiCalender):

    def __init__(self):
        super().__init__()

        self.setPhoneTableConfig()
        self.setPhoneLayout()

    def setTitleFont(self):
        self.titleFont.setPointSize(20)

    def setPhoneTableConfig(self):
        self.table.setRowCount(7)
        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels(
            self.meals
        )

        self.table.setVerticalHeaderLabels(
            self.days
        )

        # -------------------------
        # Fonts
        # -------------------------

        tableFont = QtGui.QFont()
        tableFont.setPointSize(12)
        tableFont.setBold(True)

        self.table.horizontalHeader().setFont(
            tableFont
        )

        self.table.verticalHeader().setFont(
            tableFont
        )

        # -------------------------
        # Row sizes
        # -------------------------

        self.table.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Fixed
        )

        self.table.verticalHeader().setDefaultSectionSize(
            45
        )

        # -------------------------
        # Header sizes
        # -------------------------

        self.table.horizontalHeader().setFixedHeight(
            35
        )

        self.table.verticalHeader().setMinimumWidth(
            95
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )

        # -------------------------
        # Table height
        # -------------------------

        tableHeight = (
            35 +       # horizontal header
            7 * 45 +   # rows
            2          # borders
        )

        self.table.setFixedHeight(
            tableHeight
        )

        # -------------------------
        # Initialize
        # -------------------------

        self.table.initializeTable()

    def setPhoneLayout(self):
        layout = QtWidgets.QVBoxLayout(self)

        # -------------------------
        # Top bar
        # -------------------------

        topLayout = QtWidgets.QHBoxLayout()

        topLayout.setContentsMargins(
            15,
            5,
            15,
            5
        )

        topLayout.setSpacing(
            0
        )

        topLayout.addWidget(
            self.backToPlannerListButton
        )

        topLayout.addStretch()

        topLayout.addWidget(
            self.title
        )

        topLayout.addStretch()

        topLayout.addSpacing(
            33
        )

        layout.addLayout(
            topLayout
        )

        # -------------------------
        # Buttons
        # -------------------------

        layout.addLayout(self.buttonLayout)

        # -------------------------
        # Table
        # -------------------------

        layout.addWidget(
            self.table,
            3
        )

        # -------------------------
        # Ingredients
        # -------------------------

        self.ingredientScroll = QtWidgets.QScrollArea(
            self
        )

        self.ingredientScroll.setWidgetResizable(
            True
        )

        self.ingredientScroll.setWidget(
            self.ingredientList
        )

        self.ingredientScroll.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff
        )

        self.ingredientScroll.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff
        )

        QtWidgets.QScroller.grabGesture(
            self.ingredientScroll.viewport(),
            QtWidgets.QScroller.LeftMouseButtonGesture
        )

        layout.addWidget(
            self.ingredientInput
        )

        layout.addWidget(
            self.ingredientScroll,
            1
        )

    def setPlanner(self, plannerId):
        self.plannerId = plannerId
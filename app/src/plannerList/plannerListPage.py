from PySide6 import QtCore, QtWidgets, QtGui


# =========================================================
# COMBOBOX
# =========================================================

class ToggleComboBox(QtWidgets.QComboBox):

    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):

        super().paintEvent(event)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(
            QtGui.QPainter.Antialiasing
        )

        painter.setPen(
            QtGui.QPen(
                QtGui.QColor("#AFCBEB"),
                2
            )
        )

        x = self.width() - 20
        y = self.height() // 2

        painter.drawLine(
            x - 5,
            y - 2,
            x,
            y + 3
        )

        painter.drawLine(
            x,
            y + 3,
            x + 5,
            y - 2
        )
        
# =========================================================
# PLANNER ITEM
# =========================================================

class PlannerItemWidget(QtWidgets.QWidget):

    def __init__(self, name, ownerName):

        super().__init__()

        self.nameLabel = QtWidgets.QLabel(
            name
        )

        self.ownerLabel = QtWidgets.QLabel(
            f"Owner : {ownerName}"
        )

        # -------------------------
        # Fonts
        # -------------------------

        nameFont = QtGui.QFont()
        nameFont.setPointSize(24)
        nameFont.setBold(True)

        ownerFont = QtGui.QFont()
        ownerFont.setPointSize(12)

        self.nameLabel.setFont(
            nameFont
        )

        self.ownerLabel.setFont(
            ownerFont
        )

        # -------------------------
        # Layout
        # -------------------------

        layout = QtWidgets.QVBoxLayout()

        layout.setContentsMargins(
            15,
            8,
            15,
            8
        )

        layout.setSpacing(
            0
        )

        layout.addWidget(
            self.nameLabel
        )

        layout.addWidget(
            self.ownerLabel
        )

        self.setLayout(
            layout
        )


# =========================================================
# PLANNER LIST PAGE
# =========================================================

class PlannerListPage(QtWidgets.QWidget):

    plannerSelected = QtCore.Signal(
        int,
        str
    )

    createPlannerClicked = QtCore.Signal(
        str
    )

    joinPlannerClicked = QtCore.Signal(
        str,
        int
    )

    backToLoginClicked = QtCore.Signal()

    def __init__(self):

        super().__init__()

        self.createWidgets()

        self.createConnections()

        self.createLayout()

    # =====================================================
    # WIDGETS
    # =====================================================

    def createWidgets(self):

        # =================================================
        # TITLE
        # =================================================

        titleFont = QtGui.QFont()

        titleFont.setPointSize(
            24
        )

        titleFont.setBold(
            True
        )

        self.title = QtWidgets.QLabel(
            "My Planners",
            alignment=QtCore.Qt.AlignCenter,
            font=titleFont
        )

        # =================================================
        # BACK BUTTON
        # =================================================

        self.backToLoginButton = QtWidgets.QPushButton(
            "←"
        )

        self.backToLoginButton.setFixedSize(
            33,
            40
        )

        self.backToLoginButton.setStyleSheet(
            """
            QPushButton {
                border: none;
                font-size: 20px;
            }

            QPushButton:hover {
                background-color: #3c3c3c;
                border-radius: 20px;
            }
            """
        )

        # =================================================
        # PLANNER LIST
        # =================================================

        self.plannerList = QtWidgets.QListWidget()

        # =================================================
        # CREATE PLANNER
        # =================================================

        self.createPlannerName = QtWidgets.QLineEdit()

        self.createPlannerName.setPlaceholderText(
            "Plan. name to create"
        )

        self.createPlannerButton = QtWidgets.QPushButton(
            "Create"
        )

        createStyle = """
        QLineEdit {
            background-color: #3F6FA3;
            border: 1px solid #AFCBEB;
            border-radius: 6px;
            padding: 6px;
            font-size: 14px;
        }

        QPushButton {
            background-color: #3F6FA3;
            border: 1px solid #AFCBEB;
            border-radius: 6px;
            padding: 6px;
            font-size: 14px;
        }

        QPushButton:hover {
            background-color: #315A87;
        }
        """

        self.createPlannerName.setStyleSheet(
            createStyle
        )

        self.createPlannerButton.setStyleSheet(
            createStyle
        )

        # =================================================
        # JOIN PLANNER
        # =================================================

        self.ownerComboBox = ToggleComboBox()

        self.ownerComboBox.setEditable(
            True
        )

        self.ownerComboBox.setInsertPolicy(
            QtWidgets.QComboBox.NoInsert
        )

        self.ownerComboBox.lineEdit().setPlaceholderText(
            "Owner"
        )

        self.ownerComboBox.setCurrentIndex(
            -1
        )

        # -------------------------
        # Owner combo style
        # -------------------------


        self.ownerComboBox.setStyleSheet(
            """
            QComboBox {
                background-color: #3F7A5A;
                border: 1px solid #AFCBEB;
                border-radius: 6px;
                padding: 8px;
                padding-right: 35px;
                font-size: 14px;
            }

            QComboBox::drop-down {
                width: 35px;
                border: none;
                background: transparent;
            }

            QLineEdit {
                background-color: transparent;
                border: none;
                padding: 0px;
                padding-right: 5px;
                font-size: 14px;
            }
            """
        )

        # =================================================
        # JOIN NAME
        # =================================================

        self.joinPlannerName = QtWidgets.QLineEdit()

        self.joinPlannerName.setPlaceholderText(
            "Plan. name to join"
        )

        self.joinPlannerName.setStyleSheet(
            """
            QLineEdit {
                background-color: #3F7A5A;
                border: 1px solid #AFCBEB;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }
            """
        )

        # =================================================
        # JOIN BUTTON
        # =================================================

        self.joinPlannerButton = QtWidgets.QPushButton(
            "Join"
        )

        self.joinPlannerButton.setStyleSheet(
            """
            QPushButton {
                background-color: #3F7A5A;
                border: 1px solid #AFCBEB;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #326247;
            }
            """
        )

        # =================================================
        # COMMON HEIGHT
        # =================================================

        widgetHeight = 45

        self.createPlannerName.setMinimumHeight(
            widgetHeight
        )

        self.createPlannerButton.setMinimumHeight(
            widgetHeight
        )

        self.ownerComboBox.setMinimumHeight(
            widgetHeight
        )

        self.joinPlannerName.setMinimumHeight(
            widgetHeight
        )

        self.joinPlannerButton.setMinimumHeight(
            widgetHeight
        )

        # Le bouton Join doit pouvoir prendre
        # toute la hauteur des deux lignes.

        self.joinPlannerButton.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

    # =====================================================
    # CONNECTIONS
    # =====================================================

    def createConnections(self):

        self.backToLoginButton.clicked.connect(
            self.backToLoginClicked.emit
        )

        self.createPlannerButton.clicked.connect(
            self.createPlanner
        )

        self.joinPlannerButton.clicked.connect(
            self.joinPlanner
        )

        self.plannerList.itemClicked.connect(
            self.selectPlanner
        )

    # =====================================================
    # LAYOUT
    # =====================================================

    def createLayout(self):

        # =================================================
        # TOP BAR
        # =================================================

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
            self.backToLoginButton
        )

        topLayout.addStretch()

        topLayout.addWidget(
            self.title
        )

        topLayout.addStretch()

        topLayout.addSpacing(
            33
        )

        # =================================================
        # CREATE
        # =================================================

        createLayout = QtWidgets.QHBoxLayout()

        createLayout.setSpacing(
            10
        )

        # 75 %
        createLayout.addWidget(
            self.createPlannerName,
            3
        )

        # 25 %
        createLayout.addWidget(
            self.createPlannerButton,
            1
        )

        # =================================================
        # JOIN
        # =================================================

        joinLayout = QtWidgets.QGridLayout()

        joinLayout.setHorizontalSpacing(
            10
        )

        joinLayout.setVerticalSpacing(
            5
        )

        # -------------------------
        # Planner name
        # -------------------------

        joinLayout.addWidget(
            self.joinPlannerName,
            0,
            0
        )

        # -------------------------
        # Owner
        # -------------------------

        joinLayout.addWidget(
            self.ownerComboBox,
            1,
            0
        )

        # -------------------------
        # Join button
        # -------------------------

        joinLayout.addWidget(
            self.joinPlannerButton,
            0,
            1,
            2,
            1
        )

        # -------------------------
        # Column proportions
        # -------------------------

        # 75 % pour les champs
        joinLayout.setColumnStretch(
            0,
            3
        )

        # 25 % pour Join
        joinLayout.setColumnStretch(
            1,
            1
        )

        # =================================================
        # MAIN LAYOUT
        # =================================================

        layout = QtWidgets.QVBoxLayout()

        layout.setContentsMargins(
            10,
            5,
            10,
            10
        )

        layout.addLayout(
            topLayout
        )

        layout.addSpacing(
            20
        )

        layout.addWidget(
            self.plannerList
        )

        layout.addSpacing(
            10
        )

        layout.addLayout(
            createLayout
        )

        layout.addSpacing(
            10
        )

        layout.addLayout(
            joinLayout
        )

        layout.addSpacing(
            75
        )

        self.setLayout(
            layout
        )

    # =====================================================
    # CREATE PLANNER
    # =====================================================

    def createPlanner(self):

        name = (
            self.createPlannerName
            .text()
            .strip()
        )

        if not name:
            return

        self.createPlannerClicked.emit(
            name
        )

        self.createPlannerName.clear()

    # =====================================================
    # JOIN PLANNER
    # =====================================================

    def joinPlanner(self):

        name = (
            self.joinPlannerName
            .text()
            .strip()
        )

        ownerName = (
            self.ownerComboBox
            .currentText()
            .strip()
        )

        if not name:
            return

        if not ownerName:
            return

        index = self.ownerComboBox.findText(
            ownerName,
            QtCore.Qt.MatchFixedString
        )

        if index == -1:
            return

        ownerId = self.ownerComboBox.itemData(
            index
        )

        self.joinPlannerClicked.emit(
            name,
            ownerId
        )

        # -------------------------
        # Reset
        # -------------------------

        self.joinPlannerName.clear()

        self.ownerComboBox.setCurrentIndex(
            -1
        )

        self.ownerComboBox.lineEdit().clear()

        self.ownerComboBox.lineEdit().setPlaceholderText(
            "Owner"
        )

    # =====================================================
    # SELECT PLANNER
    # =====================================================

    def selectPlanner(self, item):

        plannerId = item.data(
            QtCore.Qt.UserRole
        )

        plannerName = item.data(
            QtCore.Qt.UserRole + 1
        )

        self.plannerSelected.emit(
            plannerId,
            plannerName
        )

    # =====================================================
    # PLANNER LIST
    # =====================================================

    def setPlanners(self, planners):

        self.plannerList.clear()

        for planner in planners:

            self.addPlanner(
                planner["plannerId"],
                planner["name"],
                planner["ownerName"]
            )

    def addPlanner(
        self,
        plannerId,
        name,
        ownerName
    ):

        item = QtWidgets.QListWidgetItem()

        item.setData(
            QtCore.Qt.UserRole,
            plannerId
        )

        item.setData(
            QtCore.Qt.UserRole + 1,
            name
        )

        item.setSizeHint(
            QtCore.QSize(
                0,
                120
            )
        )

        self.plannerList.addItem(
            item
        )

        widget = PlannerItemWidget(
            name,
            ownerName
        )

        self.plannerList.setItemWidget(
            item,
            widget
        )

    # =====================================================
    # AVAILABLE OWNERS
    # =====================================================

    def setAvailablePlanners(
        self,
        planners
    ):

        self.ownerComboBox.clear()

        owners = {}

        for planner in planners:

            ownerId = planner["ownerId"]

            ownerName = planner["ownerName"]

            owners[ownerId] = ownerName

        for ownerId, ownerName in owners.items():

            self.ownerComboBox.addItem(
                ownerName,
                ownerId
            )

        # -------------------------
        # Aucun owner sélectionné
        # -------------------------

        self.ownerComboBox.setCurrentIndex(
            -1
        )

        self.ownerComboBox.lineEdit().clear()

        self.ownerComboBox.lineEdit().setPlaceholderText(
            "Owner"
        )
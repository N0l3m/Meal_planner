from PySide6 import QtCore, QtWidgets, QtGui


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
        nameFont.setPointSize(12)
        nameFont.setBold(True)

        ownerFont = QtGui.QFont()
        ownerFont.setPointSize(9)

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
            10,
            5,
            10,
            5
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


class PlannerListPage(QtWidgets.QWidget):

    plannerSelected = QtCore.Signal(int, str)

    createPlannerClicked = QtCore.Signal(str)

    joinPlannerClicked = QtCore.Signal(str, int)

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

        # -------------------------
        # Title
        # -------------------------

        titleFont = QtGui.QFont()
        titleFont.setPointSize(18)
        titleFont.setBold(True)

        self.title = QtWidgets.QLabel(
            "My Planners",
            alignment=QtCore.Qt.AlignCenter,
            font=titleFont
        )

        # -------------------------
        # Back button
        # -------------------------

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

        # -------------------------
        # Planner list
        # -------------------------

        self.plannerList = QtWidgets.QListWidget()

        # -------------------------
        # Create planner
        # -------------------------

        self.createPlannerName = QtWidgets.QLineEdit()

        self.createPlannerName.setPlaceholderText(
            "Planner Name to create"
        )

        self.createPlannerButton = QtWidgets.QPushButton(
            "Create"
        )

        self.createPlannerButton.setFixedWidth(
            120
        )

        createStyle = """
        QLineEdit {
            background-color: #DCEBFF;
            border: 1px solid #AFCBEB;
            border-radius: 6px;
            padding: 6px;
        }

        QPushButton {
            background-color: #DCEBFF;
            border: 1px solid #AFCBEB;
            border-radius: 6px;
            padding: 6px;
        }

        QPushButton:hover {
            background-color: #C8DEFA;
        }
        """

        self.createPlannerName.setStyleSheet(
            createStyle
        )

        self.createPlannerButton.setStyleSheet(
            createStyle
        )

        # -------------------------
        # Join planner
        # -------------------------

        self.ownerComboBox = QtWidgets.QComboBox()

        self.ownerComboBox.setPlaceholderText(
            "Owner"
        )

        self.joinPlannerName = QtWidgets.QLineEdit()

        self.joinPlannerName.setPlaceholderText(
            "Planner name to join"
        )

        self.joinPlannerButton = QtWidgets.QPushButton(
            "Join"
        )

        self.joinPlannerButton.setFixedWidth(
            120
        )

        joinStyle = """
        QLineEdit {
            background-color: #F9DCDC;
            border: 1px solid #E5B5B5;
            border-radius: 6px;
            padding: 6px;
        }

        QComboBox {
            background-color: #F9DCDC;
            border: 1px solid #E5B5B5;
            border-radius: 6px;
            padding: 6px;
        }

        QPushButton {
            background-color: #F9DCDC;
            border: 1px solid #E5B5B5;
            border-radius: 6px;
            padding: 6px;
        }

        QPushButton:hover {
            background-color: #F3C5C5;
        }
        """

        self.ownerComboBox.setStyleSheet(
            joinStyle
        )

        self.joinPlannerName.setStyleSheet(
            joinStyle
        )

        self.joinPlannerButton.setStyleSheet(
            joinStyle
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

        # -------------------------
        # Top bar
        # -------------------------

        topLayout = QtWidgets.QHBoxLayout()

        topLayout.setContentsMargins(
            0,
            0,
            0,
            0
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

        # -------------------------
        # Create planner
        # -------------------------

        createLayout = QtWidgets.QHBoxLayout()

        createLayout.addWidget(
            self.createPlannerName
        )

        createLayout.addWidget(
            self.createPlannerButton
        )

        # -------------------------
        # Join planner
        # -------------------------

        joinLayout = QtWidgets.QGridLayout()

        joinLayout.setHorizontalSpacing(
            10
        )

        joinLayout.setVerticalSpacing(
            5
        )

        # Owner
        joinLayout.addWidget(
            self.ownerComboBox,
            0, 0
        )

        # Planner name
        joinLayout.addWidget(
            self.joinPlannerName,
            1, 0
        )

        # Join button
        joinLayout.addWidget(
            self.joinPlannerButton,
            0, 1, 2, 1
        )

        joinLayout.setColumnStretch(
            0,
            1
        )

        joinLayout.setColumnStretch(
            1,
            0
        )
        # -------------------------
        # Main layout
        # -------------------------

        layout = QtWidgets.QVBoxLayout()

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

        self.setLayout(
            layout
        )

    # =====================================================
    # CREATE PLANNER
    # =====================================================

    def createPlanner(self):

        name = self.createPlannerName.text().strip()

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

        name = self.joinPlannerName.text().strip()

        ownerId = self.ownerComboBox.currentData()

        if not name:
            return

        if ownerId is None:
            return

        self.joinPlannerClicked.emit(
            name,
            ownerId
        )

        self.joinPlannerName.clear()

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
                55
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

    def setAvailablePlanners(self, planners):

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
from PySide6 import QtCore, QtWidgets, QtGui

class ToggleComboBox(QtWidgets.QComboBox):

    def mouseReleaseEvent(self, event):

        if self.view().isVisible():
            self.hidePopup()
        else:
            self.showPopup()

        event.accept()

class OwnerComboBox(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.comboBox = ToggleComboBox(self)

        self.comboBox.setEditable(True)

        self.comboBox.setInsertPolicy(
            QtWidgets.QComboBox.NoInsert
        )

        self.comboBox.setStyleSheet("""
            QComboBox {
                background-color: #3F7A5A;
                border: 1px solid #AFCBEB;
                border-radius: 6px;
                padding: 8px;
                padding-right: 35px;
                font-size: 14px;
            }

            QComboBox::drop-down {
                border: none;
                width: 0px;
            }

            QComboBox::down-arrow {
                image: none;
                width: 0px;
                height: 0px;
            }
        """)

        self.comboBox.lineEdit().setPlaceholderText(
            "Owner"
        )

        self.comboBox.setCurrentIndex(-1)

        # Chevron
        self.arrowLabel = QtWidgets.QLabel(
            "⌄",
            self
        )

        arrowFont = QtGui.QFont()
        arrowFont.setPointSize(18)
        arrowFont.setBold(True)

        self.arrowLabel.setFont(arrowFont)

        self.arrowLabel.setStyleSheet("""
            QLabel {
                color: #AFCBEB;
                background: transparent;
                border: none;
            }
        """)

        self.arrowLabel.setAlignment(
            QtCore.Qt.AlignCenter
        )

        self.arrowLabel.setAttribute(
            QtCore.Qt.WA_TransparentForMouseEvents
        )

    def resizeEvent(self, event):

        super().resizeEvent(event)

        self.comboBox.setGeometry(
            0,
            0,
            self.width(),
            self.height()
        )

        arrowWidth = 30

        self.arrowLabel.setGeometry(
            self.width() - arrowWidth,
            0,
            arrowWidth,
            self.height()
        )

    def __getattr__(self, name):
        return getattr(self.comboBox, name)

    
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
        nameFont.setPointSize(18)
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
            "Plan. name to create"
        )

        self.createPlannerButton = QtWidgets.QPushButton(
            "Create"
        )

        self.createPlannerButton.setFixedWidth(
            100
        )

        createStyle = """
        QLineEdit {
            background-color: #3F6FA3;
            border: 1px solid #AFCBEB;
            border-radius: 6px;
            padding: 6px;
        }

        QPushButton {
            background-color: #3F6FA3;
            border: 1px solid #AFCBEB;
            border-radius: 6px;
            padding: 6px;
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

        # -------------------------
        # Join planner
        # -------------------------

        joinStyle = """ 
        QLineEdit { 
        background-color: #3F7A5A; 
        border: 1px solid #AFCBEB; 
        border-radius: 6px; 
        padding: 8px; 
        font-size: 14px; 
        } 
        
        QComboBox { 
        background-color: #3F7A5A; 
        border: 1px solid #AFCBEB; 
        border-radius: 6px; 
        padding: 8px; 
        padding-right: 30px; 
        font-size: 14px; 
        } 
        
        QComboBox::drop-down { 
        border: none; 
        width: 30px; 
        background: transparent; 
        } 
        
        
        QPushButton { 
        background-color: #3F7A5A; 
        border: 1px solid #AFCBEB; 
        border-radius: 6px; 
        padding: 8px; 
        font-size: 14px; 
        } 
        
        QPushButton:hover { 
        background-color: #326247; 
        } """

        self.ownerComboBox = OwnerComboBox()

        combo = self.ownerComboBox.comboBox

        self.ownerCompleter = QtWidgets.QCompleter(
            combo.model(),
            combo
        )

        self.ownerCompleter.setCaseSensitivity(
            QtCore.Qt.CaseInsensitive
        )

        self.ownerCompleter.setFilterMode(
            QtCore.Qt.MatchContains
        )

        combo.setCompleter(
            self.ownerCompleter
        )

        self.joinPlannerName = QtWidgets.QLineEdit()

        self.joinPlannerName.setPlaceholderText(
            "Plan. name to join"
        )

        self.joinPlannerButton = QtWidgets.QPushButton(
            "Join"
        )

        self.joinPlannerButton.setFixedWidth(100)

        self.joinPlannerButton.setStyleSheet(
            joinStyle
        )

        self.joinPlannerName.setStyleSheet(
            joinStyle
        )

        combo.setStyleSheet(
            joinStyle
        )
        

        widgetHeight = 45
        self.createPlannerName.setFixedHeight(widgetHeight)
        self.createPlannerButton.setFixedHeight(widgetHeight)

        self.ownerComboBox.setFixedHeight(widgetHeight)
        self.joinPlannerName.setFixedHeight(widgetHeight)
        self.joinPlannerButton.setFixedHeight(100)
        widgetWidth = 160
        self.createPlannerName.setFixedWidth(widgetWidth)
        self.ownerComboBox.setFixedWidth(widgetWidth)
        self.createPlannerName.setFixedWidth(widgetWidth)
        self.joinPlannerName.setFixedWidth(widgetWidth)

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
            1, 0
        )

        # Planner name
        joinLayout.addWidget(
            self.joinPlannerName,
            0, 0
        )

        # Join button
        joinLayout.addWidget(
            self.joinPlannerButton,
            0, 1, 2, 1
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

        ownerName = self.ownerComboBox.currentText().strip()

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

        self.joinPlannerName.clear()
        self.ownerComboBox.setCurrentIndex(-1)

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

        # Aucun owner sélectionné par défaut
        self.ownerComboBox.setCurrentIndex(-1)
        self.ownerComboBox.lineEdit().clear()
        self.ownerComboBox.lineEdit().setPlaceholderText(
            "Owner"
        )
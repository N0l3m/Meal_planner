from PySide6 import QtCore, QtWidgets, QtGui


class LoginPage(QtWidgets.QWidget):

    accountCreationClicked = QtCore.Signal()
    loginClicked = QtCore.Signal(str, str)

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
            "Meal Planner",
            alignment=QtCore.Qt.AlignCenter,
            font=titleFont
        )

        # -------------------------
        # Back placeholder
        # -------------------------

        self.backPlaceholder = QtWidgets.QWidget()

        self.backPlaceholder.setFixedSize(
            60,
            60
        )

        # -------------------------
        # Pseudo
        # -------------------------

        self.userName = QtWidgets.QLineEdit()

        self.userName.setPlaceholderText(
            "Username"
        )

        # -------------------------
        # Password
        # -------------------------

        self.psw = QtWidgets.QLineEdit()

        self.psw.setPlaceholderText(
            "Password"
        )

        self.psw.setEchoMode(
            QtWidgets.QLineEdit.Password
        )

        # -------------------------
        # Login button
        # -------------------------

        self.loginButton = QtWidgets.QPushButton("Login", self)
        self.loginButton.setDefault(True)

        # -------------------------
        # Account creation
        # -------------------------

        self.accountCreation = QtWidgets.QPushButton(
            "Create Account",
            self
        )

    # =====================================================
    # CONNECTIONS
    # =====================================================

    def createConnections(self):

        self.accountCreation.clicked.connect(
            self.accountCreationClicked.emit
        )

        self.loginButton.clicked.connect(
            self.login
        )

        self.psw.returnPressed.connect(
            self.login
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
            self.backPlaceholder
        )

        topLayout.addStretch()

        topLayout.addWidget(
            self.title
        )

        topLayout.addStretch()

        topLayout.addSpacing(
            60
        )

        # -------------------------
        # Main layout
        # -------------------------

        layout = QtWidgets.QVBoxLayout()

        layout.addLayout(
            topLayout
        )

        layout.addSpacing(
            30
        )

        layout.addWidget(
            self.userName
        )

        layout.addWidget(
            self.psw
        )

        layout.addSpacing(
            10
        )

        layout.addWidget(
            self.loginButton
        )

        layout.addSpacing(
            20
        )

        layout.addWidget(
            self.accountCreation
        )

        layout.addStretch()

        self.setLayout(
            layout
        )

    # =====================================================
    # LOGIN
    # =====================================================

    def login(self):

        userName = self.userName.text()
        psw = self.psw.text()

        self.loginClicked.emit(
            userName,
            psw
        )
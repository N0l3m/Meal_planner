from PySide6 import QtCore, QtWidgets, QtGui


class AccountCreationPage(QtWidgets.QWidget):

    createAccountClicked = QtCore.Signal(str, str)
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
            "Meal Planner",
            alignment=QtCore.Qt.AlignCenter,
            font=titleFont
        )

        #-----------------------
        # Back to Login Button
        #-----------------------

        self.backToLoginButton = QtWidgets.QPushButton(
            "←",
            self
        )

        self.backToLoginButton.setFixedSize(
            33,
            60
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
        # Pseudo
        # -------------------------

        

        self.userName = QtWidgets.QLineEdit()

        self.userName.setPlaceholderText(
            "Username"
        )

        # -------------------------
        # Pseudo error msg
        # -------------------------

        self.userNameError = QtWidgets.QLabel(
            "Username already exists",
            self
        )

        self.userNameError.setStyleSheet(
            "color: red;"
        )

        self.userNameError.hide()

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
        # Password length error
        # -------------------------

        self.pswError = QtWidgets.QLabel(
            "Password must contain at least 6 characters",
            self
        )

        self.pswError.setStyleSheet(
            "color: red;"
        )

        self.pswError.hide()

        # -------------------------
        # Password confirmation
        # -------------------------

        self.pswConfirmation = QtWidgets.QLineEdit()

        self.pswConfirmation.setPlaceholderText(
            "Confirm password"
        )

        self.pswConfirmation.setEchoMode(
            QtWidgets.QLineEdit.Password
        )

        # ----------------------------
        # Password confirmation error
        # ----------------------------

        self.pswConfirmError = QtWidgets.QLabel(
            "Passwords must be the same ",
            self
        )

        self.pswConfirmError.setStyleSheet(
            "color: red;"
        )

        self.pswConfirmError.hide()

        # -------------------------
        # Account creation button
        # -------------------------

        self.accountCreation = QtWidgets.QPushButton("Create Account",self)
        self.accountCreation.setDefault(True)

    # =====================================================
    # CONNECTIONS
    # =====================================================

    def createConnections(self):

        self.accountCreation.clicked.connect(
            self.createAccount
        )

        self.backToLoginButton.clicked.connect(
            self.backToLoginClicked.emit
        )

        self.pswConfirmation.returnPressed.connect(
            self.createAccount
        )

    # =====================================================
    # ACCOUNT CREATION
    # =====================================================

    def createAccount(self):

        userName = self.userName.text().strip()
        psw = self.psw.text()
        pswConfirmation = self.pswConfirmation.text()

        if not userName:
            return

        if len(psw) < 6:
            self.pswError.show()
            return

        self.pswError.hide()

        if psw != pswConfirmation:
            self.pswConfirmError.show()
            return

        self.pswConfirmError.hide()

        self.createAccountClicked.emit(
            userName,
            psw
        )

    # =====================================================
    # LAYOUT
    # =====================================================

    def createLayout(self):
        topLayout = QtWidgets.QHBoxLayout()

        topLayout.addWidget(
            self.backToLoginButton
        )

        topLayout.addStretch()

        topLayout.addWidget(
            self.title
        )

        topLayout.addStretch()

        topLayout.addSpacing(
            40
        )

        layout = QtWidgets.QVBoxLayout()

        layout.addLayout(
            topLayout
        )

        # -------------------------
        # Formulaire
        # -------------------------

        layout.addSpacing(30)

        layout.addWidget(
            self.userName
        )

        layout.addWidget(
            self.userNameError
        )

        layout.addWidget(
            self.psw
        )

        layout.addWidget(
            self.pswError
        )

        layout.addWidget(
            self.pswConfirmation
        )

        layout.addWidget(
            self.pswConfirmError
        )

        layout.addSpacing(20)

        layout.addWidget(
            self.accountCreation
        )

        layout.addStretch()

        self.setLayout(
            layout
        )

    def showUserNameError(self):
        self.userNameError.show()

    def hideUserNameError(self):
        self.userNameError.hide()
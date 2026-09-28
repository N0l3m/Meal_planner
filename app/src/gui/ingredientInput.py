from PySide6 import QtCore, QtWidgets


class IngredientInput(QtWidgets.QWidget):

    sendIngredient = QtCore.Signal(str)

    def __init__(self, undoStack, parent=None):
        super().__init__(parent)

        # -------------------------
        # Undo / Redo
        # -------------------------

        self.undoStack = undoStack

        # -------------------------
        # Champ de saisie
        # -------------------------

        self.input = QtWidgets.QLineEdit(self)

        self.input.installEventFilter(
            self
        )

        self.input.setPlaceholderText(
            "Add an ingredient..."
        )

        # -------------------------
        # Bouton Send
        # -------------------------

        self.sendButton = QtWidgets.QPushButton(
            "Add",
            self
        )

        # -------------------------
        # Layout
        # -------------------------

        layout = QtWidgets.QHBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.addWidget(
            self.input
        )

        layout.addWidget(
            self.sendButton
        )

        # -------------------------
        # Connections
        # -------------------------

        self.sendButton.clicked.connect(
            self.send
        )

        self.input.returnPressed.connect(
            self.send
        )

    # =====================================================
    # SEND
    # =====================================================

    def send(self):

        text = self.input.text().strip()

        if not text:
            return

        self.sendIngredient.emit(text)
        self.input.clear()


    def eventFilter(self, watched, event):

        if (
            watched == self.input
            and event.type() == QtCore.QEvent.KeyPress
            and event.key() in (
                QtCore.Qt.Key_Return,
                QtCore.Qt.Key_Enter
            )
        ):

            self.send()

            return True

        return super().eventFilter(
            watched,
            event
        )
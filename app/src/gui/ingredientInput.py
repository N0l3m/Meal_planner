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

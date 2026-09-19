from PySide6 import QtWidgets, QtCore

from PySide6 import QtCore, QtWidgets


class IngredientItem(QtWidgets.QWidget):

    editRequested = QtCore.Signal(object)
    deleteRequested = QtCore.Signal(object)

    def __init__(
        self,
        text,
        ingredientId,
        parent=None
    ):
        super().__init__(parent)

        self.ingredientId = ingredientId

        # -------------------------
        # Ingredient text
        # -------------------------

        self.label = QtWidgets.QLabel(
            text,
            self
        )

        # -------------------------
        # Edit button
        # -------------------------

        self.editButton = QtWidgets.QPushButton(
            self
        )

        self.editButton.setIcon(
            self.style().standardIcon(
                QtWidgets.QStyle.SP_FileDialogDetailedView
            )
        )

        # -------------------------
        # Delete button
        # -------------------------

        self.deleteButton = QtWidgets.QPushButton(
            self
        )

        self.deleteButton.setIcon(
            self.style().standardIcon(
                QtWidgets.QStyle.SP_TrashIcon
            )
        )

        # -------------------------
        # Layout
        # -------------------------

        layout = QtWidgets.QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.addWidget(
            self.label
        )

        layout.addStretch()

        layout.addWidget(
            self.editButton
        )

        layout.addWidget(
            self.deleteButton
        )

        # -------------------------
        # Connections
        # -------------------------

        self.editButton.clicked.connect(
            self.edit
        )

        self.deleteButton.clicked.connect(
            self.delete
        )

    # =====================================================
    # EDIT
    # =====================================================

    def edit(self):

        self.editRequested.emit(
            self
        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete(self):

        self.deleteRequested.emit(
            self
        )

class IngredientList(QtWidgets.QWidget):

    addIngredientClicked = QtCore.Signal(str)

    editIngredientClicked = QtCore.Signal(
        object,
        str
    )

    deleteIngredientClicked = QtCore.Signal(
        object,
        int
    )

    def __init__(self, parent=None):
        super().__init__(parent)

        self.items = []

        self.layout = QtWidgets.QVBoxLayout(self)

        self.layout.setContentsMargins(
            0, 0, 0, 0
        )

        self.layout.setSpacing(2)

        self.layout.addStretch()

    def setIngredients(self, ingredients):

        for item in self.items:
            item.deleteLater()

        self.items.clear()

        for ingredientId, text, position in ingredients:

            self.insertIngredient(
                text,
                ingredientId
            )

    def insertIngredient(
        self,
        text,
        ingredientId
    ):

        item = IngredientItem(
            text,
            ingredientId,
            self
        )

        item.editRequested.connect(
            self.editIngredient
        )

        item.deleteRequested.connect(
            self.deleteIngredient
        )

        self.layout.insertWidget(
            self.layout.count() - 1,
            item
        )

        self.items.append(
            item
        )

    def addIngredient(self, text):

        text = text.strip()

        if not text:
            return

        self.addIngredientClicked.emit(
            text
        )

    def editIngredient(self, item):

        text, ok = QtWidgets.QInputDialog.getText(
            self,
            "Edit ingredient",
            "Ingredient:",
            text=item.label.text()
        )

        if not ok:
            return

        text = text.strip()

        if not text:
            return

        self.editIngredientClicked.emit(
            item,
            text
        )

    def deleteIngredient(self, item):

        self.deleteIngredientClicked.emit(
            item,
            item.ingredientId
        )

    def updateIngredient(
        self,
        item,
        text
    ):

        item.label.setText(
            text
        )

    def removeIngredient(
        self,
        item
    ):

        if item in self.items:
            self.items.remove(item)

        item.deleteLater()
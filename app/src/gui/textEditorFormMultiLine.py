from PySide6 import QtWidgets, QtGui
from gui.undoRedo import undoRedo


class TextEditorFormMultiLine(QtWidgets.QStyledItemDelegate):

    def createEditor(self, parent, option, index):

        editor = QtWidgets.QTextEdit(parent)

        # -------------------------
        # Couleur du texte et fond
        # -------------------------

        editor.setStyleSheet(
            "QTextEdit {"
            "color: white;"
            "background-color: #2C2C2C;"
            "}"
        )

        table = self.parent()

        # -------------------------
        # Cellules sélectionnées
        # -------------------------

        if isinstance(
            table,
            QtWidgets.QTableWidget
        ):

            self.selected_cells = (
                table.selectedItems()
            )

            self.old_texts = [
                item.text()
                for item in self.selected_cells
            ]

        # -------------------------
        # Modification en direct
        # -------------------------

        editor.textChanged.connect(
            lambda:
            self.updateSelectedCells(
                editor,
                index
            )
        )

        return editor

    def setEditorData(
        self,
        editor,
        index
    ):

        editor.setPlainText(
            index.data() or ""
        )

    def setModelData(
        self,
        editor,
        model,
        index
    ):

        text = editor.toPlainText()

        table = self.parent()

        if not isinstance(
            table,
            QtWidgets.QTableWidget
        ):

            model.setData(
                index,
                text
            )

            return

        # -------------------------
        # Création Undo / Redo
        # -------------------------

        command = undoRedo(
            cells=self.selected_cells,
            old_texts=self.old_texts,
            new_text=text,
            saveMealCallback=(
                table.saveMealCallback
            ),
            mealData=table.getMealData,
            action="text"
        )

        table.undoStack.push(
            command
        )

    def updateSelectedCells(
        self,
        editor,
        index
    ):

        text = editor.toPlainText()

        # -------------------------
        # Apparence
        # -------------------------

        for item in self.selected_cells:

            item.setForeground(
                QtGui.QColor("white")
            )

            item.setBackground(
                QtGui.QColor("#3c3c3c")
            )

        table = self.parent()

        if not isinstance(
            table,
            QtWidgets.QTableWidget
        ):
            return

        # -------------------------
        # Mise à jour des autres
        # cellules sélectionnées
        # -------------------------

        for item in table.selectedItems():

            # Ne pas modifier
            # la cellule en cours d'édition
            if (
                item.row() == index.row()
                and item.column() == index.column()
            ):
                continue

            item.setText(
                text
            )
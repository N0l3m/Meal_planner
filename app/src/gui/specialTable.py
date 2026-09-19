from PySide6 import QtCore, QtWidgets, QtGui

from gui.undoRedo import undoRedo


class SpecialTable(QtWidgets.QTableWidget):

    def __init__(
        self,
        parent=None,
        undoStack=None,
        saveMealCallback=None
    ):
        super().__init__(parent)

        # -------------------------
        # Undo / Redo
        # -------------------------

        self.undoStack = undoStack

        # -------------------------
        # Sauvegarde serveur
        # -------------------------

        self.saveMealCallback = saveMealCallback

        # -------------------------
        # Couleurs
        # -------------------------

        self.normalColor = "#3c3c3c"
        self.selectedColor = "#2F795E"
        self.dragColor = "#47b1a5"

        # -------------------------
        # Sélection
        # -------------------------

        self.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )

        self.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectItems
        )

        # -------------------------
        # Timer pour appui long
        # -------------------------

        self.longPressTimer = QtCore.QTimer(self)
        self.longPressTimer.setSingleShot(True)
        self.longPressTimer.setInterval(500)

        self.longPressTimer.timeout.connect(
            self.startLongDrag
        )

        # -------------------------
        # Déplacement
        # -------------------------

        self.dragging = False
        self.dragSource = None

    # =====================================================
    # CALLBACK
    # =====================================================

    def setSaveMealCallback(self, callback):

        self.saveMealCallback = callback

    # =====================================================
    # INITIALISATION
    # =====================================================

    def initializeTable(self):

        for row in range(self.rowCount()):

            for column in range(self.columnCount()):

                item = QtWidgets.QTableWidgetItem()

                item.setBackground(
                    QtGui.QColor(
                        self.normalColor
                    )
                )

                self.setItem(
                    row,
                    column,
                    item
                )

        self.updateColors()

    # =====================================================
    # CHARGEMENT DES REPAS
    # =====================================================

    def loadMeals(self, meals):

        # -------------------------
        # Vider les cellules
        # -------------------------

        for row in range(self.rowCount()):

            for column in range(self.columnCount()):

                item = self.item(
                    row,
                    column
                )

                if item is not None:
                    item.setText("")

        # -------------------------
        # Transformer les données
        # en dictionnaire
        # -------------------------

        mealData = {
            (day, meal): content
            for day, meal, content in meals
        }

        # -------------------------
        # Remplir le tableau
        # -------------------------

        for row in range(self.rowCount()):

            for column in range(self.columnCount()):

                item = self.item(
                    row,
                    column
                )

                if item is None:
                    continue

                day, meal = self.getMealData(
                    item
                )

                content = mealData.get(
                    (day, meal),
                    ""
                )

                item.setText(
                    content
                )

        self.updateColors()

    # =====================================================
    # COULEURS
    # =====================================================

    def changeBoxColor(self, item, color):

        if item is not None:

            item.setBackground(
                QtGui.QColor(color)
            )

    def changeHeaderBackgroundColor(self, color):

        for column in range(self.columnCount()):

            item = self.horizontalHeaderItem(
                column
            )

            if item is not None:

                item.setBackground(
                    QtGui.QColor(color)
                )

        for row in range(self.rowCount()):

            item = self.verticalHeaderItem(
                row
            )

            if item is not None:

                item.setBackground(
                    QtGui.QColor(color)
                )

    def updateColors(self):

        # -------------------------
        # Couleur normale des cases
        # -------------------------

        for row in range(self.rowCount()):

            for column in range(self.columnCount()):

                item = self.item(
                    row,
                    column
                )

                if item is not None:

                    self.changeBoxColor(
                        item,
                        self.normalColor
                    )

        # -------------------------
        # Couleur normale headers
        # -------------------------

        for column in range(self.columnCount()):

            header = self.horizontalHeaderItem(
                column
            )

            if header is not None:

                self.changeBoxColor(
                    header,
                    self.normalColor
                )

        for row in range(self.rowCount()):

            header = self.verticalHeaderItem(
                row
            )

            if header is not None:

                self.changeBoxColor(
                    header,
                    self.normalColor
                )

        # -------------------------
        # Couleur sélection
        # -------------------------

        for item in self.selectedItems():

            self.changeBoxColor(
                item,
                self.selectedColor
            )

            column = item.column()

            horizontalHeader = (
                self.horizontalHeaderItem(
                    column
                )
            )

            self.changeBoxColor(
                horizontalHeader,
                self.selectedColor
            )

            row = item.row()

            verticalHeader = (
                self.verticalHeaderItem(
                    row
                )
            )

            self.changeBoxColor(
                verticalHeader,
                self.selectedColor
            )

    def selectionChanged(
        self,
        selected,
        deselected
    ):

        super().selectionChanged(
            selected,
            deselected
        )

        self.updateColors()

    # =====================================================
    # MOUSE
    # =====================================================

    def mousePressEvent(self, event):

        if event.button() == QtCore.Qt.LeftButton:

            item = self.itemAt(
                event.position().toPoint()
            )

            if item is not None:

                self.dragSource = item
                self.dragging = False

                self.longPressTimer.start()

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):

        if self.dragging:
            return

        super().mouseMoveEvent(event)

    def startLongDrag(self):

        item = self.itemUnderMouse()

        if (
            self.dragSource is None
            or self.dragSource != item
        ) and item is not None:
            return

        self.dragging = True

        self.clearSelection()

        self.dragSource.setSelected(
            True
        )

        self.changeBoxColor(
            self.dragSource,
            self.dragColor
        )

    def mouseReleaseEvent(self, event):

        self.longPressTimer.stop()

        # -------------------------
        # Déplacement
        # -------------------------

        if (
            event.button() == QtCore.Qt.LeftButton
            and self.dragging
        ):

            target = self.itemAt(
                event.position().toPoint()
            )

            if (
                target is not None
                and target != self.dragSource
            ):

                self.moveCell(
                    self.dragSource,
                    target
                )

                self.changeBoxColor(
                    target,
                    self.dragColor
                )

                self.changeBoxColor(
                    self.dragSource,
                    self.normalColor
                )

            self.dragging = False
            self.dragSource = None

            return

        # -------------------------
        # Clic normal
        # -------------------------

        self.dragSource = None

        super().mouseReleaseEvent(event)

    # =====================================================
    # DEPLACEMENT
    # =====================================================

    def moveCell(
        self,
        source,
        target
    ):

        if self.undoStack is None:
            return

        command = undoRedo(
            source=source,
            target=target,
            action="move",
            saveMealCallback=self.saveMealCallback,
            mealData=self.getMealData
        )

        self.undoStack.push(
            command
        )

    # =====================================================
    # SUPPRESSION DES CELLULES
    # =====================================================

    def clearSelectedCells(self):

        cells = self.selectedItems()

        if not cells:
            return

        if self.undoStack is None:
            return

        old_texts = [
            item.text()
            for item in cells
        ]

        command = undoRedo(
            cells=cells,
            old_texts=old_texts,
            new_text="",
            action="text",
            saveMealCallback=self.saveMealCallback,
            mealData=self.getMealData
        )

        self.undoStack.push(
            command
        )

    # =====================================================
    # SUPPRESSION TOUT LE TABLEAU
    # =====================================================

    def clearTableContent(self):

        cells = []

        for row in range(self.rowCount()):

            for column in range(self.columnCount()):

                item = self.item(
                    row,
                    column
                )

                if item is not None:
                    cells.append(item)

        if not cells:
            return

        if self.undoStack is None:
            return

        old_texts = [
            item.text()
            for item in cells
        ]

        command = undoRedo(
            cells=cells,
            old_texts=old_texts,
            new_text="",
            action="text",
            saveMealCallback=self.saveMealCallback,
            mealData=self.getMealData
        )

        self.undoStack.push(
            command
        )

    # =====================================================
    # CLAVIER
    # =====================================================

    def keyPressEvent(self, event):

        if event.key() in (
            QtCore.Qt.Key_Delete,
            QtCore.Qt.Key_Backspace
        ):

            self.clearSelectedCells()

            return

        super().keyPressEvent(event)

    # =====================================================
    # ITEM SOUS LA SOURIS
    # =====================================================

    def itemUnderMouse(self):

        globalPosition = QtGui.QCursor.pos()

        localPosition = self.viewport().mapFromGlobal(
            globalPosition
        )

        item = self.itemAt(
            localPosition
        )

        return item

    # =====================================================
    # DONNEES DU REPAS
    # =====================================================

    def getMealData(self, item):

        verticalText = (
            self.verticalHeaderItem(
                item.row()
            ).text()
        )

        horizontalText = (
            self.horizontalHeaderItem(
                item.column()
            ).text()
        )

        # -------------------------
        # Mode calendrier classique
        # -------------------------

        if verticalText in [
            "Lunch",
            "Dinner"
        ]:

            meal = verticalText
            day = horizontalText

        # -------------------------
        # Mode smartphone
        # -------------------------

        else:

            day = verticalText
            meal = horizontalText

        return day, meal
from PySide6 import QtGui


class undoRedo(QtGui.QUndoCommand):

    def __init__(
        self,
        cells=None,
        old_texts=None,
        new_text=None,
        source=None,
        target=None,
        listWidget=None,
        old_list_text=None,
        new_list_text=None,
        saveMealCallback=None,
        mealData=None,
        action="text"
    ):
        super().__init__()

        self.action = action

        # -------------------------
        # Action texte / cellules
        # -------------------------

        self.cells = cells
        self.old_texts = old_texts
        self.new_text = new_text

        # -------------------------
        # Action déplacement
        # -------------------------

        self.source = source
        self.target = target

        if self.action == "move":

            self.source_old_text = source.text()
            self.target_old_text = target.text()

        # -------------------------
        # Action liste
        # -------------------------

        self.listWidget = listWidget
        self.old_list_text = old_list_text
        self.new_list_text = new_list_text

        # -------------------------
        # Sauvegarde des repas
        # -------------------------

        self.saveMealCallback = saveMealCallback
        self.mealData = mealData

    # =====================================================
    # REDO
    # =====================================================

    def redo(self):

        # -------------------------
        # Cellules
        # -------------------------

        if self.action == "text":

            for item in self.cells:

                item.setText(
                    self.new_text
                )

                self.saveMeal(
                    item,
                    self.new_text
                )

        # -------------------------
        # Déplacement
        # -------------------------

        elif self.action == "move":

            self.target.setText(
                self.source_old_text
            )

            self.source.setText("")

            self.saveMeal(
                self.target,
                self.source_old_text
            )

            self.saveMeal(
                self.source,
                ""
            )

        # -------------------------
        # Liste
        # -------------------------

        elif self.action == "list":

            self.listWidget.setPlainText(
                self.new_list_text
            )

    # =====================================================
    # UNDO
    # =====================================================

    def undo(self):

        # -------------------------
        # Cellules
        # -------------------------

        if self.action == "text":

            for item, old_text in zip(
                self.cells,
                self.old_texts
            ):

                item.setText(
                    old_text
                )

                self.saveMeal(
                    item,
                    old_text
                )

        # -------------------------
        # Déplacement
        # -------------------------

        elif self.action == "move":

            self.source.setText(
                self.source_old_text
            )

            self.target.setText(
                self.target_old_text
            )

            self.saveMeal(
                self.source,
                self.source_old_text
            )

            self.saveMeal(
                self.target,
                self.target_old_text
            )

        # -------------------------
        # Liste
        # -------------------------

        elif self.action == "list":

            self.listWidget.setPlainText(
                self.old_list_text
            )

    # =====================================================
    # SAVE MEAL
    # =====================================================

    def saveMeal(self, item, text):

        if self.saveMealCallback is None:
            return

        if self.mealData is None:
            return

        day, meal = self.mealData(
            item
        )

        self.saveMealCallback(
            day,
            meal,
            text
        )
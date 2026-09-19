from PySide6 import QtCore, QtWidgets, QtGui

from gui.textEditorFormMultiLine import TextEditorFormMultiLine
from gui.specialTable import SpecialTable
from gui.ingredientInput import IngredientInput
from gui.ingredientList import IngredientList


class GuiCalender(QtWidgets.QWidget):

    backToPlannerListClicked = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

        self.meals = [
            "Lunch",
            "Dinner"
        ]

        self.plannerId = None

        # -------------------------
        # Base locale
        # -------------------------
        # Temporaire :
        # utilisée encore par
        # les ingrédients.

        # -------------------------
        # Undo / Redo
        # -------------------------

        self.undoStack = QtGui.QUndoStack(
            self
        )

        self.createWidgets()
        self.createConnections()

    # =====================================================
    # WIDGETS
    # =====================================================

    def createWidgets(self):

        #-----------------------
        # Back to Login Button
        #-----------------------

        self.backToPlannerListButton = QtWidgets.QPushButton(
            "←",
            self
        )

        self.backToPlannerListButton.setFixedSize(
            33,
            40
        )

        self.backToPlannerListButton.setStyleSheet(
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
        # Title
        # -------------------------

        titleFont = QtGui.QFont()

        titleFont.setPointSize(
            18
        )

        titleFont.setBold(
            True
        )

        self.title = QtWidgets.QLabel(
            "Meal Planner",
            alignment=(
                QtCore.Qt.AlignTop |
                QtCore.Qt.AlignHCenter
            ),
            font=titleFont
        )

        # -------------------------
        # Table
        # -------------------------

        self.table = SpecialTable(
            self,
            self.undoStack
        )

        # -------------------------
        # Multiline delegate
        # -------------------------

        self.table.setItemDelegate(
            TextEditorFormMultiLine(
                self.table
            )
        )

        # -------------------------
        # Buttons
        # -------------------------

        self.undoButton = QtWidgets.QPushButton(
            "↶",
            self
        )

        self.redoButton = QtWidgets.QPushButton(
            "↷",
            self
        )

        self.clearTable = QtWidgets.QPushButton(
            "Clear",
            self
        )

        self.buttonLayout = QtWidgets.QHBoxLayout()

        self.buttonLayout.addWidget(
            self.undoButton
        )

        self.buttonLayout.addWidget(
            self.redoButton
        )

        self.buttonLayout.addWidget(
            self.clearTable
        )

        # -------------------------
        # Ingredients
        # -------------------------

        self.ingredientInput = IngredientInput(
            self.undoStack,
            self
        )

        self.ingredientList = IngredientList(
            self
        )

        self.ingredientInput.sendIngredient.connect(
            self.ingredientList.addIngredient
        )

    # =====================================================
    # CONNECTIONS
    # =====================================================

    def createConnections(self):

        self.undoButton.clicked.connect(
            self.undoStack.undo
        )

        self.redoButton.clicked.connect(
            self.undoStack.redo
        )

        self.clearTable.clicked.connect(
            self.table.clearTableContent
        )

        self.backToPlannerListButton.clicked.connect(
            self.backToPlannerListClicked.emit
        )

    # =====================================================
    # PLANNER
    # =====================================================

    def setPlanner(
        self,
        plannerId
    ):

        self.plannerId = plannerId

    # =====================================================
    # SAVE CALLBACK
    # =====================================================

    def setSaveMealCallback(
        self,
        callback
    ):

        self.table.setSaveMealCallback(
            callback
        )

    # =====================================================
    # LOAD MEALS
    # =====================================================

    def loadMeals(
        self,
        meals
    ):
        self.table.loadMeals(
            meals
        )

    def setIngredients(self, ingredients):
        self.ingredientList.setIngredients(
            ingredients
        )

    def setTitle(self, plannerName):
        self.title.setText(
            plannerName
        )
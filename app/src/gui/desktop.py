from PySide6 import QtWidgets, QtGui
from gui.guiCalender import GuiCalender


class DesktopApi(GuiCalender):

    def __init__(self):
        super().__init__()

        self.setDesktopTableConfig()
        self.setTitleFont()
        self.setDesktopLayout()

    def setTitleFont(self):

        self.titleFont.setPointSize(20)

    def setDesktopTableConfig(self):

        # 2 lignes : Lunch / Dinner
        # 7 colonnes : Monday -> Sunday

        self.table.setRowCount(2)
        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels(
            self.days
        )

        self.table.setVerticalHeaderLabels(
            self.meals
        )

        tableFont = QtGui.QFont()
        tableFont.setPointSize(14)

        self.table.horizontalHeader().setFont(tableFont)
        self.table.verticalHeader().setFont(tableFont)

        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )

        self.table.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )

        # Initialise les cellules
        self.table.initializeTable()

    def setDesktopLayout(self):

        # Colonne de droite :
        # - champ d'ajout d'ingrédient
        # - liste des ingrédients

        ingredientLayout = QtWidgets.QVBoxLayout()
        ingredientLayout.addWidget(self.ingredientInput)
        ingredientLayout.addWidget(self.ingredientList)

        ingredientLayout.setStretch(0, 0)
        ingredientLayout.setStretch(1, 1)

        layout = QtWidgets.QGridLayout(self)

        layout.addWidget(
            self.title,
            0, 0, 1, 3
        )

        layout.addWidget(
            self.table,
            1, 0, 1, 2
        )

        layout.addLayout(
            ingredientLayout,
            1, 2
        )

        layout.addLayout(
            self.buttonLayout,
            2, 0, 1, 3
        )

        # Largeur relative des colonnes
        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 1)

        # La zone centrale prend l'espace vertical
        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 0)
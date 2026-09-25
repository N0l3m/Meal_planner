import sys

from PySide6 import QtWidgets, QtGui, QtCore

from mainWindow.mainWindow import MainWindow


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    # =====================================================
    # THEME
    # =====================================================

    palette = QtGui.QPalette()

    # Couleurs principales
    background = QtGui.QColor("#1E1E1E")
    background2 = QtGui.QColor("#252526")
    text = QtGui.QColor("#FFFFFF")
    secondaryText = QtGui.QColor("#CFCFCF")

    # Champs / boutons
    inputBackground = QtGui.QColor("#303030")
    buttonBackground = QtGui.QColor("#3F6FA3")

    # Sélection
    selectionBackground = QtGui.QColor("#4F81BD")
    selectionText = QtGui.QColor("#FFFFFF")

    # Fenêtre
    palette.setColor(
        QtGui.QPalette.ColorRole.Window,
        background
    )

    palette.setColor(
        QtGui.QPalette.ColorRole.WindowText,
        text
    )

    # Champs de texte
    palette.setColor(
        QtGui.QPalette.ColorRole.Base,
        inputBackground
    )

    palette.setColor(
        QtGui.QPalette.ColorRole.AlternateBase,
        background2
    )

    palette.setColor(
        QtGui.QPalette.ColorRole.Text,
        text
    )

    # Boutons
    palette.setColor(
        QtGui.QPalette.ColorRole.Button,
        buttonBackground
    )

    palette.setColor(
        QtGui.QPalette.ColorRole.ButtonText,
        text
    )

    # Texte secondaire
    palette.setColor(
        QtGui.QPalette.ColorRole.PlaceholderText,
        secondaryText
    )

    # Sélection
    palette.setColor(
        QtGui.QPalette.ColorRole.Highlight,
        selectionBackground
    )

    palette.setColor(
        QtGui.QPalette.ColorRole.HighlightedText,
        selectionText
    )

    # Tooltips
    palette.setColor(
        QtGui.QPalette.ColorRole.ToolTipBase,
        background2
    )

    palette.setColor(
        QtGui.QPalette.ColorRole.ToolTipText,
        text
    )

    # Texte très important
    palette.setColor(
        QtGui.QPalette.ColorRole.BrightText,
        QtGui.QColor("#FFFFFF")
    )

    # Liens
    palette.setColor(
        QtGui.QPalette.ColorRole.Link,
        QtGui.QColor("#66B3FF")
    )

    app.setPalette(palette)

    # =====================================================
    # STYLE GLOBAL
    # =====================================================

    app.setStyleSheet("""
        QWidget {
            color: #FFFFFF;
        }

        QMainWindow {
            background-color: #1E1E1E;
        }

        QLabel {
            color: #FFFFFF;
        }

        QLineEdit {
            color: #FFFFFF;
            background-color: #303030;
            border: 1px solid #777777;
            border-radius: 6px;
            padding: 6px;
        }

        QLineEdit:focus {
            border: 1px solid #66B3FF;
        }

        QLineEdit::placeholder {
            color: #BDBDBD;
        }

        QPushButton {
            color: #FFFFFF;
            background-color: #3F6FA3;
            border: 1px solid #AFCBEB;
            border-radius: 6px;
            padding: 6px;
        }

        QPushButton:hover {
            background-color: #5186BD;
        }

        QPushButton:pressed {
            background-color: #315A87;
        }

        QComboBox {
            color: #FFFFFF;
            background-color: #303030;
            border: 1px solid #777777;
            border-radius: 6px;
            padding: 6px;
        }

        QComboBox:hover {
            border: 1px solid #66B3FF;
        }

        QComboBox QAbstractItemView {
            color: #FFFFFF;
            background-color: #303030;
            selection-background-color: #4F81BD;
            selection-color: #FFFFFF;
        }

        QListWidget {
            color: #FFFFFF;
            background-color: #252526;
            border: 1px solid #555555;
            border-radius: 6px;
        }

        QListWidget::item {
            color: #FFFFFF;
            background-color: #252526;
            padding: 5px;
        }

        QListWidget::item:hover {
            background-color: #333333;
        }

        QListWidget::item:selected {
            color: #FFFFFF;
            background-color: #4F81BD;
        }

        QScrollBar:vertical {
            background-color: #252526;
            width: 12px;
        }

        QScrollBar::handle:vertical {
            background-color: #555555;
            border-radius: 6px;
            min-height: 25px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: #777777;
        }

        QToolTip {
            color: #FFFFFF;
            background-color: #303030;
            border: 1px solid #777777;
        }
    """)

    # =====================================================
    # APPLICATION
    # =====================================================

    window = MainWindow()

    window.show()

    sys.exit(app.exec())
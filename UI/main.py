import sys

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGraphicsDropShadowEffect, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QFont, QColor
from ui_form import Ui_MainWindow
import os
os.environ["QT_OPENGL"] = "software"


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)


        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        font_id = QFontDatabase.addApplicationFont("Ubuntu-R.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family, 16)
            self.ui.btnStart.setFont(font)
            self.ui.btnOptions.setFont(font)
            self.ui.lblTitle.setFont(font)
        else:
            print("Hiba: Nem sikerült betölteni az Ubuntu fontot!")


        self.setFixedHeight(410)
        self.setFixedWidth(800)

        #Kék alapú díszítősáv elrendezése
        layout = QVBoxLayout(self.ui.frameBlue)
        layout.setContentsMargins(0, 55, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.ui.lblTitle, alignment=Qt.AlignCenter)
        layout.addStretch()
        
        #Gombok elrendezése
        layout = QVBoxLayout(self.ui.frameButtons)
        layout.setContentsMargins(0, 45, 0, 0)

        self.ui.btnStart.setFixedWidth(420)
        self.ui.btnOptions.setFixedWidth(420)
        self.ui.btnOptions.setFixedHeight(80)
        self.ui.btnStart.setFixedHeight(80)


        layout.setSpacing(30)
        layout.addWidget(self.ui.btnStart, alignment=Qt.AlignCenter)
        layout.addWidget(self.ui.btnOptions, alignment=Qt.AlignCenter)
        layout.addStretch()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { background-color: white; }")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QFont
from ui_optionsForm import Ui_OptionsForm

class OptionsMenu(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.ui = Ui_OptionsForm()
        self.ui.setupUi(self)

        font_id = QFontDatabase.addApplicationFont("Ubuntu-R.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family, 16)
            # self.ui.btnStart.setFont(font)
            # self.ui.btnOptions.setFont(font)
            self.ui.lblTitle.setFont(font)
        else:
            print("Hiba: Nem sikerült betölteni az Ubuntu fontot!")


        #Kék alapú díszítősáv elrendezése
        layout = QVBoxLayout(self.ui.frameBlue)
        layout.setContentsMargins(0, 55, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.ui.lblTitle, alignment=Qt.AlignCenter)
        layout.addStretch()
        




    def show_options(self):
        """Váltás a Beállítások oldalra."""
        self.stacked_widget.setCurrentIndex(1)
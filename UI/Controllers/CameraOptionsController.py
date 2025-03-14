import os
import sys

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QFont
from Resources.Stylesheets.styles import *
from Views.ui_cameraOptionsForm import Ui_Form

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Views")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Resources", "Stylesheets")))

class CameraOptionsController(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.stacked_widget = stacked_widget

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.loadFont()

        #Kék alapú díszítősáv elrendezése
        layout = QVBoxLayout(self.ui.frameBlue)
        layout.setContentsMargins(0, 55, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.ui.lblTitle, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.ui.frameBlue.setStyleSheet(sidebar_style)
        self.ui.lblTitle.setStyleSheet(sidebar_title_style)


        self.ui.btnBack.setStyleSheet(options_button_style)
        self.ui.btnBack.setFont(self.font)
        self.ui.btnBack.clicked.connect(lambda event: self.stacked_widget.setCurrentIndex(1))
        self.ui.btnBack.enterEvent = lambda event: self.ui.btnBack.setStyleSheet(options_button_hover_style)
        self.ui.btnBack.leaveEvent = lambda event: self.ui.btnBack.setStyleSheet(options_button_style)


        self.ui.lblCamera.setStyleSheet(train_label_style)
        self.ui.lblCamera.setFont(self.font)

        self.ui.lblHue.setStyleSheet(train_label_style)
        self.ui.lblHue.setFont(self.font)

        self.ui.sliderHue.setStyleSheet(slider_style)

        self.ui.txtInputCamera.setStyleSheet(train_input_style)
        self.ui.txtInputCamera.setFont(self.font)
        self.ui.txtInputCamera.setContextMenuPolicy(Qt.NoContextMenu)




    def loadFont(self):
        font_id = QFontDatabase.addApplicationFont('Resources\\Fonts\\Ubuntu-R.ttf')
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.font = QFont(font_family, 16)
            self.ui.lblTitle.setFont(self.font)
            self.ui.lblDescription.setFont(self.font)
        else:
            print('Hiba: Nem sikerült betölteni az Ubuntu fontot!')
        
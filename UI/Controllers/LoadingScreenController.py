import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QFontDatabase, QFont, QMovie
from PySide6.QtCore import QThread, Signal, QSize
from time import sleep
from Resources.Stylesheets.styles import *
from Views.ui_loadingForm import Ui_Form

class LoadingScreenController(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        font_id = QFontDatabase.addApplicationFont("Resources\\Fonts\\Ubuntu-R.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family, 16)
            self.ui.lblTitle.setFont(font)
        else:
            print("Hiba: Nem sikerült betölteni az Ubuntu fontot!")


        #Kék alapú díszítősáv elrendezése
        layout = QVBoxLayout(self.ui.frameBlue)
        layout.setContentsMargins(0, 55, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.ui.lblTitle, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.ui.frameBlue.setStyleSheet(sidebar_style)
        self.ui.lblTitle.setStyleSheet(sidebar_title_style)
        
        #Töltőikon és szöveg elrendezése
        layout = QVBoxLayout(self.ui.frameButtons)
        layout.addWidget(self.ui.lblLoading, alignment=Qt.AlignCenter)
        layout.setContentsMargins(0, 55, 0, 0)
        layout.setSpacing(0)
        
        self.ui.lblLoading.setFont(font)
        self.ui.lblLoading.setStyleSheet(info_label_style)
        
        self.movie = QMovie("Resources\\Icons\\loading.gif")
        self.ui.lblLoadingSpinner.setMovie(self.movie)
        self.movie.setScaledSize(QSize(70,70))

        self.ui.lblLoadingSpinner.setFixedHeight(100)
        self.ui.lblLoadingSpinner.setFixedWidth(100)
        layout.addWidget(self.ui.lblLoadingSpinner, alignment=Qt.AlignCenter)
        self.movie.start()  # Animáció elindítása
        
        layout.addStretch()
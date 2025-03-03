import os
import sys

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QFont
from Resources.Stylesheets.styles import *
from Views.ui_mainMenuForm import Ui_MainWindow
from Models.RecognizerHandler import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Views")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Resources", "Stylesheets")))

class MainMenuController(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.stacked_widget = stacked_widget
        self.recognizer = RecognizerHandler.getInstance()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.recognizer_active = False

        font_id = QFontDatabase.addApplicationFont("Resources\\Fonts\\Ubuntu-R.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family, 16)
            self.ui.btnStart.setFont(font)
            self.ui.btnOptions.setFont(font)
            self.ui.btnCameraOptions.setFont(font)
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

        

        #Gombok elrendezése
        layout = QVBoxLayout(self.ui.frameButtons)
        layout.setContentsMargins(0, 45, 0, 0)

        self.ui.btnStart.setFixedWidth(420)
        self.ui.btnStart.setFixedHeight(80)
        self.ui.btnStart.setStyleSheet(button_style)
        
        
        self.ui.btnOptions.setFixedWidth(420)
        self.ui.btnOptions.setFixedHeight(80)
        self.ui.btnOptions.setStyleSheet(button_style)


        self.ui.btnCameraOptions.setFixedWidth(420)
        self.ui.btnCameraOptions.setFixedHeight(80)
        self.ui.btnCameraOptions.setStyleSheet(button_style)


        layout.setSpacing(30)
        layout.addWidget(self.ui.btnStart, alignment=Qt.AlignCenter)
        layout.addWidget(self.ui.btnOptions, alignment=Qt.AlignCenter)
        layout.addWidget(self.ui.btnCameraOptions, alignment=Qt.AlignCenter)
        layout.addStretch()

        #Gombok eseménykezelése 
        self.ui.btnStart.clicked.connect(lambda: self.start())
        self.ui.btnStart.enterEvent = lambda event: self.ui.btnStart.setStyleSheet(button_hover_style)
        self.ui.btnStart.leaveEvent = lambda event: self.ui.btnStart.setStyleSheet(button_style)

        self.ui.btnOptions.clicked.connect(self.show_options)
        self.ui.btnOptions.enterEvent = lambda event: self.ui.btnOptions.setStyleSheet(button_hover_style)
        self.ui.btnOptions.leaveEvent = lambda event: self.ui.btnOptions.setStyleSheet(button_style)


        self.ui.btnCameraOptions.enterEvent = lambda event: self.ui.btnCameraOptions.setStyleSheet(button_hover_style)
        self.ui.btnCameraOptions.leaveEvent = lambda event: self.ui.btnCameraOptions.setStyleSheet(button_style)


    def show_options(self):
        """Váltás a Beállítások oldalra."""
        self.stacked_widget.setCurrentIndex(2)


    def start(self):
        if not self.recognizer_active:
            self.recognizer_active = True
            self.ui.btnStart.setText("Gesztusvezérlés kikapcsolása")
            self.ui.btnOptions.setEnabled(False)
            self.recognizer.setCamera(0)
            self.recognizer.start()
        else:
            self.recognizer_active = False
            self.recognizer.stop()
            self.ui.btnStart.setText("Gesztusvezérlés indítása")
            self.ui.btnOptions.setEnabled(True)
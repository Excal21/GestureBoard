from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import Qt
from Resources.Stylesheets.styles import *
from Views.ui_mainMenuForm import Ui_MainWindow
from Models.RecognizerHandler import *
from Controllers.BaseController import BaseController

class MainMenuController(BaseController):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.stacked_widget = stacked_widget
        self.recognizer = RecognizerHandler.getInstance()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUI({
            'btnStart': button_style,
            'btnOptions': button_style,
            'btnCameraOptions': button_style
        })

        self.recognizer_active = False

        
        self.setEventHandlers()
        

        #Gombok elrendezése
        layout = QVBoxLayout(self.ui.frameButtons)
        layout.setContentsMargins(0, 45, 0, 0)

        self.ui.btnStart.setFixedWidth(420)
        self.ui.btnStart.setFixedHeight(80)
        
        self.ui.btnOptions.setFixedWidth(420)
        self.ui.btnOptions.setFixedHeight(80)

        self.ui.btnCameraOptions.setFixedWidth(420)
        self.ui.btnCameraOptions.setFixedHeight(80)


        layout.setSpacing(30)
        layout.addWidget(self.ui.btnStart, alignment=Qt.AlignCenter)
        layout.addWidget(self.ui.btnOptions, alignment=Qt.AlignCenter)
        layout.addWidget(self.ui.btnCameraOptions, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.ui.btnCameraOptions.setText('Kamera-beállítások')


    def show_options(self):
        '''Váltás a Beállítások oldalra.'''
        self.stacked_widget.setCurrentIndex(2)


    def start(self):
        if not self.recognizer_active:
            self.recognizer_active = True
            self.ui.btnStart.setText('Gesztusvezérlés kikapcsolása')
            self.ui.btnOptions.setEnabled(False)
            self.ui.btnCameraOptions.setEnabled(False)
            self.ui.btnOptions.setStyleSheet(button_style + disabled_style)
            self.ui.btnCameraOptions.setStyleSheet(button_style + disabled_style)
            self.ui.btnOptions.enterEvent = lambda event: None
            self.ui.btnOptions.leaveEvent = lambda event: None
    
            self.ui.btnCameraOptions.enterEvent = lambda event: None
            self.ui.btnCameraOptions.leaveEvent = lambda event: None
            self.recognizer.startRecognizer()
        else:
            self.recognizer_active = False
            self.recognizer.stop()
            self.ui.btnStart.setText('Gesztusvezérlés indítása')
            self.ui.btnOptions.setEnabled(True)
            self.ui.btnCameraOptions.setEnabled(True)
            self.ui.btnStart.setStyleSheet(button_hover_style)
            self.ui.btnOptions.setStyleSheet(button_style)
            self.ui.btnCameraOptions.setStyleSheet(button_style)

            self.ui.btnOptions.enterEvent = lambda event: self.ui.btnOptions.setStyleSheet(button_hover_style)
            self.ui.btnOptions.leaveEvent = lambda event: self.ui.btnOptions.setStyleSheet(button_style)

            self.ui.btnCameraOptions.enterEvent = lambda event: self.ui.btnCameraOptions.setStyleSheet(button_hover_style)
            self.ui.btnCameraOptions.leaveEvent = lambda event: self.ui.btnCameraOptions.setStyleSheet(button_style)

    def setEventHandlers(self):
        #Gombok eseménykezelése 
        self.ui.btnStart.clicked.connect(lambda: self.start())
        self.ui.btnStart.enterEvent = lambda event: self.ui.btnStart.setStyleSheet(button_hover_style if not self.recognizer_active else button_hover_style + 'background-color: rgb(201, 97, 97)')
        self.ui.btnStart.leaveEvent = lambda event: self.ui.btnStart.setStyleSheet(button_style if not self.recognizer_active else button_style + 'background-color: rgb(227, 109, 109)')

        self.ui.btnOptions.clicked.connect(self.show_options)
        self.ui.btnOptions.enterEvent = lambda event: self.ui.btnOptions.setStyleSheet(button_hover_style)
        self.ui.btnOptions.leaveEvent = lambda event: self.ui.btnOptions.setStyleSheet(button_style)


        self.ui.btnCameraOptions.enterEvent = lambda event: self.ui.btnCameraOptions.setStyleSheet(button_hover_style)
        self.ui.btnCameraOptions.leaveEvent = lambda event: self.ui.btnCameraOptions.setStyleSheet(button_style)
        self.ui.btnCameraOptions.clicked.connect(lambda event: self.stacked_widget.setCurrentIndex(5))

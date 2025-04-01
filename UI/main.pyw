import os
import sys
import time

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtCore import Qt, QThread, Signal
from PySide6 import QtGui
import Controllers.MainMenuController
import Controllers.OptionsMenuController
import Controllers.LoadingScreenController
import Controllers.TrainMenuController
import Controllers.NewGestureWizardController

import Controllers.CameraOptionsController
from Models.RecognizerHandler import *
from Models.MediaPipeHandler import MediapipeLoader
from Models.Recorder import Recorder

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Controllers')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Models')))



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GestureBoard')
        self.setFixedSize(800, 410)
        self.setStyleSheet('background-color: white;')
        self.setWindowIcon(QtGui.QIcon('Resources/Icons/hand.ico'))

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.main_menu = Controllers.MainMenuController.MainMenuController(self.stacked_widget)
        self.options_menu = Controllers.OptionsMenuController.OptionsMenuController(self.stacked_widget)
        self.loading_screen = Controllers.LoadingScreenController.LoadingScreenController(self.stacked_widget)
        self.teach_menu = Controllers.TrainMenuController.TrainMenuController(self.stacked_widget)
        self.new_gesture_wizard = Controllers.NewGestureWizardController.NewGestureWizardController(self.stacked_widget)
        self.camera_options = Controllers.CameraOptionsController.CameraOptionsController(self.stacked_widget)

        self.stacked_widget.addWidget(self.loading_screen)
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.options_menu)
        self.stacked_widget.addWidget(self.teach_menu)
        self.stacked_widget.addWidget(self.new_gesture_wizard)
        self.stacked_widget.addWidget(self.camera_options)

    def closeEvent(self, event):
        rl.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
  

    window = MainWindow()
    window.show()
    QApplication.processEvents()


    ml = MediapipeLoader()
    rl = RecognizerHandler.getInstance()

    ml.start()
    ml.finished.connect(rl.load)
    rl.finished.connect(lambda: window.stacked_widget.setCurrentIndex(1))
    #window.stacked_widget.setCurrentIndex(1)


    sys.exit(app.exec())
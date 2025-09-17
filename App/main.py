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
from Models.MediaPipeHandler import ImportHandler
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
        self.loading_screen = Controllers.LoadingScreenController.LoadingScreenController(self.stacked_widget)
        self.options_menu = Controllers.OptionsMenuController.OptionsMenuController(self.stacked_widget)
        self.teach_menu = Controllers.TrainMenuController.TrainMenuController(self.stacked_widget)
        self.new_gesture_wizard = Controllers.NewGestureWizardController.NewGestureWizardController(self.stacked_widget)
        self.camera_options = Controllers.CameraOptionsController.CameraOptionsController(self.stacked_widget)

        self.stacked_widget.addWidget(self.loading_screen)
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.options_menu)
        self.stacked_widget.addWidget(self.teach_menu)
        self.stacked_widget.addWidget(self.new_gesture_wizard)
        self.stacked_widget.addWidget(self.camera_options)

        self.ml = ImportHandler()
        self.rl = RecognizerHandler.getInstance()

        self.ml.finished.connect(self.rl.load)
        self.rl.finished.connect(lambda: self.stacked_widget.setCurrentIndex(1))

    def start_background(self):
        self.ml.start()

    def closeEvent(self, event):
        if self.rl is not None:
            self.rl.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    QApplication.processEvents()
    window.start_background()
    sys.exit(app.exec())
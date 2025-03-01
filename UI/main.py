import os
import sys
import time

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtCore import Qt, QThread, Signal
import Views.MainMenu
import Views.OptionsMenu
import Views.Loading

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Views")))

class MediapipeLoader(QThread):
    finished = Signal()  # Jelzés, amikor a betöltés kész

    def run(self):
        print("Mediapipe betöltése...")
        import os
        import cv2
        from mediapipe import solutions, Image, ImageFormat
        from mediapipe.framework.formats import landmark_pb2
        from mediapipe.tasks import python
        import numpy as np
        from datetime import datetime
        import shutil
        import pyautogui
        #time.sleep(10)

        print("Mediapipe betöltve!")
        self.finished.emit()  # Jelzés a fő UI szálnak


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GestureBoard")
        # self.setGeometry(100, 100, 800, 410)
        self.setFixedSize(800, 410)
        self.setStyleSheet("background-color: white;")  # Alap háttérszín

        # QStackedWidget létrehozása
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Nézetek létrehozása és hozzáadása
        self.main_menu = Views.MainMenu.MainMenu(self.stacked_widget)
        self.options_menu = Views.OptionsMenu.OptionsMenu(self.stacked_widget)
        self.loading_screen = Views.Loading.LoadingScreen(self.stacked_widget)

        self.stacked_widget.addWidget(self.loading_screen)
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.options_menu)


if __name__ == "__main__":
    app = QApplication(sys.argv)
  

    window = MainWindow()
    window.show()
    QApplication.processEvents()


    ml = MediapipeLoader()
    ml.finished.connect(lambda: window.stacked_widget.setCurrentIndex(1))
    ml.start()


    sys.exit(app.exec())
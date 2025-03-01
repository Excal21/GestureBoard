from PySide6.QtCore import Qt, QThread, Signal

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
from PySide6.QtCore import Qt, QThread, Signal

class MediapipeLoader(QThread):
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

        print("Mediapipe betöltve!")
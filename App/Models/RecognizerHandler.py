from PySide6.QtCore import Qt, QThread, Signal
import sys
import os
import cv2

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class RecognizerHandler(QThread):
    _instance = None

    finished = Signal()

    @classmethod
    def getInstance(cls):
        if not cls._instance:
            cls._instance = RecognizerHandler()
        return cls._instance

    def __init__(self):
        super().__init__()
        self.__recognizer = None

    def load(self):
        if not self.__recognizer:
            from Models.Recognizer import Recognizer
            self.__recognizer = Recognizer('Config/gesture_recognizer.task', 'Config/UserSettings.json')
            self.getCameras()
            print('Recognizer loaded')
        self.finished.emit()

    def reload(self):
        self.__recognizer.reloadModel()
        print('Reloaded')

    def annotate(self, frame, gestures = False, distance=500):
        return self.__recognizer.annotateImage(frame, gestures, distance)

    def start(self):
        self.__recognizer.camerafeed = False
        self.__recognizer.Run()

    def setCamera(self, camera):
        self.__recognizer.camerafeed = True

    def stop(self):
        self.__recognizer.stop = True
        self.__recognizer.mouse_processor.hideOverlay()
        self.__recognizer.mouse_active = False
        self.__recognizer.framethrottling = self.__recognizer.framethrottling_prevstate
        print('Recognizer stopped')

    def getCameras(self):
        if hasattr(self, '_cached_cameras'):
            return self._cached_cameras

        print('Kamerák keresése...')
        index = 0
        cameras = []
        while True:
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            if not cap.isOpened():
                break
            cameras.append(index)
            cap.release()
            index += 1
        self._cached_cameras = cameras
        return cameras
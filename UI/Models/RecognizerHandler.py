from PySide6.QtCore import Qt, QThread, Signal


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
            self.__recognizer = Recognizer('Models\\gesture_recognizer.task', 'Config\\UserSettings.json')
            print("Recognizer loaded")
        self.finished.emit()

    def start(self):
        self.__recognizer.Run()

    def setCamera(self, camera):
        self.__recognizer.camerafeed = True

    def stop(self):
        self.__recognizer.Stop()
        print("Recognizer stopped")
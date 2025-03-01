from PySide6.QtCore import Qt, QThread, Signal


class RecognizerHandler(QThread):
    recognizer = None
    
    finished = Signal()  # Jelzés, amikor a betöltés kész
    def __init__(self):
        super().__init__()
    
    def load(self):
        if not RecognizerHandler.recognizer:
            from Models.Recognizer import Recognizer
            RecognizerHandler.recognizer = Recognizer('Models\\gesture_recognizer.task')
            print("Recognizer loaded")
        self.finished.emit()

    @staticmethod
    def start():
        RecognizerHandler.recognizer.Run()

    @staticmethod
    def setCamera(camera):
        RecognizerHandler.recognizer.camerafeed = True

    @staticmethod
    def stop():
        RecognizerHandler.recognizer.Stop()
        print("Recognizer stopped")
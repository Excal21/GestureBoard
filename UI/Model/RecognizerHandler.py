from PySide6.QtCore import Qt, QThread, Signal


class RecognizerHandler(QThread):
    recognizer = None
    
    finished = Signal()  # Jelzés, amikor a betöltés kész
    def __init__(self):
        super().__init__()
    
    def load(self):
        from Model.Recognizer import Recognizer
        if not RecognizerHandler.recognizer:
            RecognizerHandler.recognizer = Recognizer('Model/gesture_recognizer.task')
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
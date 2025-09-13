import os
import sys
from PySide6.QtWidgets import QApplication, QStackedWidget, QPushButton, QVBoxLayout
from PySide6.QtGui import QFont, QFontDatabase, QIcon
from PySide6.QtCore import Qt, QPoint, QEvent, QSize
import copy
import cv2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'App')))

if QApplication.instance() is None:
    app = QApplication(sys.argv)

from App.Models.Recognizer import Recognizer
import json

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'App'))
os.chdir(project_root)

recognizer = Recognizer('Config/gesture_recognizer.task', 'Config/UserSettings.json')

def test_loadConfig():
    assert recognizer.loadGestures() != {}

def test_loadCameraSettings():
    recognizer.loadCameraSettings()
    assert recognizer.camera is not None
    assert recognizer.camera in [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert recognizer.confidence >= 0 and recognizer.confidence <= 1
    assert recognizer.hueoffset >= 0 and recognizer.hueoffset <= 255
    assert recognizer.distance >= 0
    assert recognizer.delay >= 0
    assert recognizer.framethrottling in [True, False]

def test_reloadModel():
    recognizer.reloadModel()
    assert recognizer.recognizer is not None

def test_annotateImage():
    img = cv2.imread('Data/Samples/2/2_1')
    annotated_img, gesture = recognizer.annotateImage(img, gestures=True)

    assert not (annotated_img == img).all()
    assert gesture
    assert isinstance(gesture, tuple)
    assert gesture[0] == '2'
    assert isinstance(gesture[1], float)
    assert 1 <= gesture[1] <= 100
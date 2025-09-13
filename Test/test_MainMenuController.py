import os
import sys
from PySide6.QtWidgets import QApplication, QStackedWidget
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtCore import SignalInstance
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'App')))


if QApplication.instance() is None:
    app = QApplication(sys.argv)

stacked_widget = QStackedWidget()

from App.Controllers.MainMenuController import MainMenuController
from App.Resources.Stylesheets.styles import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'App'))
os.chdir(project_root)

mainMenu = MainMenuController(stacked_widget)

def test_buttonSize():
    assert mainMenu.ui.btnStart.width() == 420
    assert mainMenu.ui.btnStart.height() == 80
    assert mainMenu.ui.btnOptions.width() == 420
    assert mainMenu.ui.btnOptions.height() == 80
    assert mainMenu.ui.btnCameraOptions.width() == 420
    assert mainMenu.ui.btnCameraOptions.height() == 80

def test_eventHandlers():
    assert hasattr(mainMenu.ui.btnStart, 'enterEvent')
    assert hasattr(mainMenu.ui.btnStart, 'leaveEvent')
    assert hasattr(mainMenu.ui.btnOptions, 'enterEvent')
    assert hasattr(mainMenu.ui.btnOptions, 'leaveEvent')
    assert hasattr(mainMenu.ui.btnCameraOptions, 'enterEvent')
    assert hasattr(mainMenu.ui.btnCameraOptions, 'leaveEvent')


def test_start_activates_recognizer(qtbot, monkeypatch):
    started = {}
    monkeypatch.setattr(mainMenu.recognizer, "start", lambda: started.setdefault("started", True))
    monkeypatch.setattr(mainMenu.recognizer, "stop", lambda: started.setdefault("stopped", True))

    mainMenu.recognizer_active = False
    mainMenu.ui.btnStart.setText('Gesztusvezérlés indítása')
    mainMenu.ui.btnOptions.setEnabled(True)
    mainMenu.ui.btnCameraOptions.setEnabled(True)

    mainMenu.start()

    assert mainMenu.recognizer_active is True
    assert mainMenu.ui.btnStart.text() == 'Gesztusvezérlés kikapcsolása'
    assert not mainMenu.ui.btnOptions.isEnabled()
    assert not mainMenu.ui.btnCameraOptions.isEnabled()
    assert started.get("started", False)

    assert isinstance(mainMenu.ui.btnOptions.enterEvent, type(lambda: None))
    assert isinstance(mainMenu.ui.btnOptions.leaveEvent, type(lambda: None))
    assert isinstance(mainMenu.ui.btnCameraOptions.enterEvent, type(lambda: None))
    assert isinstance(mainMenu.ui.btnCameraOptions.leaveEvent, type(lambda: None))

    started = {}
    monkeypatch.setattr(mainMenu.recognizer, "start", lambda: started.setdefault("started", True))
    monkeypatch.setattr(mainMenu.recognizer, "stop", lambda: started.setdefault("stopped", True))

    mainMenu.recognizer_active = True
    mainMenu.ui.btnStart.setText('Gesztusvezérlés kikapcsolása')
    mainMenu.ui.btnOptions.setEnabled(False)
    mainMenu.ui.btnCameraOptions.setEnabled(False)

    mainMenu.start()

    assert mainMenu.recognizer_active is False
    assert mainMenu.ui.btnStart.text() == 'Gesztusvezérlés indítása'
    assert mainMenu.ui.btnOptions.isEnabled()
    assert mainMenu.ui.btnCameraOptions.isEnabled()
    assert started.get("stopped", False)
    mainMenu.ui.btnOptions.enterEvent(None)
    assert mainMenu.ui.btnOptions.styleSheet() == button_hover_style
    mainMenu.ui.btnOptions.leaveEvent(None)
    assert mainMenu.ui.btnOptions.styleSheet() == button_style
    mainMenu.ui.btnCameraOptions.enterEvent(None)
    assert mainMenu.ui.btnCameraOptions.styleSheet() == button_hover_style
    mainMenu.ui.btnCameraOptions.leaveEvent(None)
    assert mainMenu.ui.btnCameraOptions.styleSheet() == button_style


import os
import sys
from PySide6.QtWidgets import QApplication, QStackedWidget
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtCore import SignalInstance
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI')))


if QApplication.instance() is None:
    app = QApplication(sys.argv)

stacked_widget = QStackedWidget()

from UI.Controllers.MainMenuController import MainMenuController
from UI.Resources.Stylesheets.styles import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI'))
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
    # Mock recognizer start/stop
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

    def is_lambda(fn):
        return callable(fn) and fn.__name__ == "<lambda>"
    
    assert is_lambda(mainMenu.ui.btnOptions.enterEvent)
    assert is_lambda(mainMenu.ui.btnOptions.leaveEvent)
    assert is_lambda(mainMenu.ui.btnCameraOptions.enterEvent)
    assert is_lambda(mainMenu.ui.btnCameraOptions.leaveEvent)


def test_start_deactivates_recognizer(qtbot, monkeypatch):
    # Mock recognizer start/stop
    started = {}
    monkeypatch.setattr(mainMenu.recognizer, "start", lambda: started.setdefault("started", True))
    monkeypatch.setattr(mainMenu.recognizer, "stop", lambda: started.setdefault("stopped", True))

    # Set recognizer as active
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
    # enterEvent and leaveEvent should set stylesheet
    mainMenu.ui.btnOptions.enterEvent(None)
    assert mainMenu.ui.btnOptions.styleSheet() == button_hover_style
    mainMenu.ui.btnOptions.leaveEvent(None)
    assert mainMenu.ui.btnOptions.styleSheet() == button_style
    mainMenu.ui.btnCameraOptions.enterEvent(None)
    assert mainMenu.ui.btnCameraOptions.styleSheet() == button_hover_style
    mainMenu.ui.btnCameraOptions.leaveEvent(None)
    assert mainMenu.ui.btnCameraOptions.styleSheet() == button_style


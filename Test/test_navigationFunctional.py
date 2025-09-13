import sys
import pytest
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QPushButton

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'App')))
from App.main import MainWindow
from pytest import MonkeyPatch
import pytest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'App'))
os.chdir(project_root)

@pytest.fixture
def app(qtbot, monkeypatch):
    window = MainWindow()
    monkeypatch.setattr(window, "closeEvent", lambda event: event.accept())
    qtbot.addWidget(window)
    window.show()
    window.start_background()
    return window

def test_run(app, qtbot):
    assert app.stacked_widget.currentWidget() == app.loading_screen
    qtbot.wait(10000)
    assert app.stacked_widget.currentWidget() == app.main_menu, 'A főmenü nem jelenik meg vagy nagyon sokat tölt.'

#Főmenü gombok
def test_options_button_click(app, qtbot):
    options_btn = app.main_menu.ui.btnOptions
    qtbot.mouseClick(options_btn, Qt.LeftButton)
    assert app.stacked_widget.currentIndex() == 2

def test_camera_button_click(app, qtbot):
    camera_btn = app.main_menu.ui.btnCameraOptions
    qtbot.mouseClick(camera_btn, Qt.LeftButton)
    assert app.stacked_widget.currentIndex() == 5

#Gesztusbeállítások gombjai
def test_teach_button_click(app, qtbot):
    app.stacked_widget.currentWidget() == app.options_menu
    train_btn = app.options_menu.ui.btnManager
    qtbot.mouseClick(train_btn, Qt.LeftButton)
    assert app.stacked_widget.currentIndex() == 3

def test_options_save_button_click(app, qtbot):
    app.stacked_widget.currentWidget() == app.options_menu
    app.options_menu.loadConfig()
    back_save = app.options_menu.ui.btnSave
    qtbot.mouseClick(back_save, Qt.LeftButton)
    assert app.stacked_widget.currentIndex() == 1

#Kamera beállítások gombjai
def test_camera_back_button_click(app, qtbot):
    app.stacked_widget.currentWidget() == app.camera_options
    back_save = app.camera_options.ui.btnBack
    qtbot.mouseClick(back_save, Qt.LeftButton)
    assert app.stacked_widget.currentIndex() == 1

def test_camera_save_button_click(app, qtbot):
    app.camera_options.loadSettings()
    app.stacked_widget.currentWidget() == app.camera_options
    back_save = app.camera_options.ui.btnSave
    qtbot.mouseClick(back_save, Qt.LeftButton)
    assert app.stacked_widget.currentIndex() == 1
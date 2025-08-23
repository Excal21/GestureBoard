import sys
import pytest
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI')))
from UI.main import MainWindow

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI'))
os.chdir(project_root)

@pytest.fixture
def app(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    window.start_background()
    return window

def test_run(app, qtbot):
    assert app.stacked_widget.currentWidget() == app.loading_screen
    # Szimuláljuk, hogy a loading_screen után a main_menu jelenik meg
    qtbot.wait(10000)
    # app.stacked_widget.setCurrentWidget(app.main_menu)
    assert app.stacked_widget.currentWidget() == app.main_menu

# def test_start_button_click(app, qtbot):
#     # Szimuláljuk a Start gomb megnyomását
#     start_btn = app.main_menu.ui.btnStart
#     qtbot.mouseClick(start_btn, Qt.LeftButton)
    # Ide jöhet assert, hogy mi történik a gombnyomás után
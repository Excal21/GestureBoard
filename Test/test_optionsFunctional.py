import sys
import pytest
import os
from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from PySide6.QtCore import Qt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI')))
from UI.main import MainWindow
from unittest.mock import patch

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI'))
os.chdir(project_root)

@pytest.fixture
def app(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window


def test_predefinedAction(app, qtbot):
    qtbot.wait(100)
    app.stacked_widget.setCurrentIndex(2)
    qtbot.wait(100)
    options_menu = app.options_menu

    gesture_entry = options_menu.scroll_layout.itemAt(0).widget()
    btn_container = gesture_entry.findChildren(QWidget)[1]
    btns = btn_container.findChildren(QPushButton)
    btn_predef = btns[0]
    btn_predef.setFocus()
    qtbot.mouseClick(btn_predef, Qt.LeftButton)
    qtbot.wait(500)
    assert options_menu.sub_menu_active is True
    assert options_menu.ui.scrollCombo.isVisible() is True
    assert options_menu.ui.scrollArea.isEnabled() is True
    qtbot.wait(500)
    qtbot.mouseClick(btn_predef, Qt.LeftButton)
    assert options_menu.sub_menu_active is False
    assert options_menu.ui.scrollCombo.isVisible() is False
    assert options_menu.ui.scrollArea.isEnabled() is True
    
    qtbot.wait(500)        
    qtbot.mouseClick(btn_predef, Qt.LeftButton)
    sub_btn = options_menu.ui.scrollComboWidgetContents.layout().itemAt(0).widget()
    qtbot.mouseClick(sub_btn, Qt.LeftButton)
    qtbot.wait(500)
    assert options_menu.data['1']['description'] == 'Böngésző elindítása\n\n\nTörléshez kattints\njobb gombbal!'
    assert options_menu.data['1']['highlight'] == 0

def test_keyCapture(app, qtbot):
    qtbot.wait(100)
    app.stacked_widget.setCurrentIndex(2)
    qtbot.wait(100)
    options_menu = app.options_menu
    app.activateWindow()
    app.raise_()
    app.setFocus()

    gesture_entry = options_menu.scroll_layout.itemAt(0).widget()
    btn_container = gesture_entry.findChildren(QWidget)[1]
    btns = btn_container.findChildren(QPushButton)
    btn_key = btns[1]
    btn_key.setFocus()

    qtbot.mouseClick(btn_key, Qt.LeftButton)
    qtbot.keyPress(btn_key, Qt.Key_K)
    assert options_menu.data['1']['description'] == 'K\n\n\nTörléshez kattints\njobb gombbal!'
    assert options_menu.data['1']['action'] == "pyautogui.hotkey('k')"

    qtbot.mouseClick(btn_key, Qt.LeftButton)
    qtbot.keyPress(btn_key, Qt.Key_F, modifier=Qt.ControlModifier | Qt.ShiftModifier)
    assert options_menu.data['1']['description'] == 'ctrl + shift + F\n\n\nTörléshez kattints\njobb gombbal!'
    assert options_menu.data['1']['action'] == "pyautogui.hotkey('ctrl', 'shift', 'f')"
    assert options_menu.data['1']['highlight'] == 1

    qtbot.mouseClick(btn_key, Qt.LeftButton)
    qtbot.keyPress(btn_key, Qt.Key_Aacute)
    assert options_menu.data['1']['description'] == 'Á\n\n\nTörléshez kattints\njobb gombbal!'
    assert options_menu.data['1']['action'] == "pyautogui.hotkey('á')"
    assert options_menu.data['1']['highlight'] == 1

    qtbot.mouseClick(btn_key, Qt.LeftButton)
    qtbot.keyPress(btn_key, Qt.Key_Q, modifier=Qt.AltModifier)
    assert options_menu.data['1']['description'] == 'alt + Q\n\n\nTörléshez kattints\njobb gombbal!'
    assert options_menu.data['1']['action'] == "pyautogui.hotkey('alt', 'q')"
    assert options_menu.data['1']['highlight'] == 1
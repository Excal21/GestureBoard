import os
import sys
import copy
import pytest
from PySide6.QtWidgets import QApplication, QStackedWidget, QLabel, QPushButton, QLineEdit
from PySide6.QtCore import Qt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI')))

from UI.Controllers.TrainMenuController import TrainMenuController
from UI.Resources.Stylesheets.styles import *

if QApplication.instance() is None:
    app = QApplication(sys.argv)

stacked_widget = QStackedWidget()

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI'))
os.chdir(project_root)

train_menu = TrainMenuController(stacked_widget)

def test_ubuntu_font_family_on_widgets():
    expected_family = 'Ubuntu'
    widgets = [
        train_menu.ui.lblTitle,
        train_menu.ui.lblDescription,
        train_menu.ui.lblServer,
        train_menu.ui.txtinputServer,
        train_menu.ui.btnBack,
        train_menu.ui.btnRecord,
        train_menu.ui.btnDelete,
        train_menu.ui.btnTrain,
    ]
    for widget in widgets:
        font = widget.font()
        assert expected_family in font.family(), f"{widget.objectName()} font: {font.family()}"

def test_hover_and_leave_events_on_buttons():
    buttons = [
        train_menu.ui.btnBack,
        train_menu.ui.btnRecord,
        train_menu.ui.btnDelete,
        train_menu.ui.btnTrain,
    ]
    for btn in buttons:
        assert callable(btn.enterEvent), f"{btn.objectName()} enterEvent not callable"
        assert callable(btn.leaveEvent), f"{btn.objectName()} leaveEvent not callable"

def test_setLayoutSettings_properties():
    assert train_menu.ui.txtinputServer.placeholderText() == 'http://127.0.0.1:5000'
    assert train_menu.ui.txtinputServer.contextMenuPolicy() == Qt.NoContextMenu
    assert train_menu.ui.lblDescription.text() != ''

def test_updateList_and_select():
    train_menu.data = {
        "1": {"gesture": "Teszt gesztus"}
    }
    train_menu.updateList()
    assert train_menu.scroll_layout.count() == 1
    btn = train_menu.scroll_layout.itemAt(0).widget()
    assert isinstance(btn, QPushButton)
    btn.click()
    assert train_menu.selected_gesture == "1"
    btn.click()
    assert train_menu.selected_gesture is None

def test_delete_removes_selected_gesture():
    train_menu.data = {
        "1": {"gesture": "Teszt gesztus"},
        "2": {"gesture": "Másik gesztus"}
    }
    train_menu.updateList()
    btn = train_menu.scroll_layout.itemAt(0).widget()
    btn.click()
    train_menu.delete()
    assert "1" not in train_menu.data
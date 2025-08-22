import os
import sys
from PySide6.QtWidgets import QApplication, QStackedWidget, QPushButton, QVBoxLayout
from PySide6.QtGui import QFont, QFontDatabase, QIcon
from PySide6.QtCore import Qt, QPoint, QEvent, QSize
import copy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI')))

if QApplication.instance() is None:
    app = QApplication(sys.argv)

stacked_widget = QStackedWidget()

from UI.Controllers.OptionsMenuController import OptionsMenuController
from UI.Resources.Stylesheets.styles import *
import json

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI'))
os.chdir(project_root)

options_menu = OptionsMenuController(stacked_widget)


def test_loadConfig():
    stacked_widget.addWidget(options_menu)
    stacked_widget.setCurrentIndex(1)

    options_menu.loadConfig()
    assert options_menu.data != {}

def test_saveMappings():
    options_menu.loadConfig()
    data = copy.deepcopy(options_menu.data)
    assert options_menu.data is not None, f'Nem sikerült betölteni a konfigurációs fájlt a teszthez'
    options_menu.saveMappings()

    options_menu.loadConfig()
    assert data == options_menu.data, 'A beolvasott és a mentett fájl eltér'

def test_setFont():
    assert options_menu.font is not None

def test_icons():
    icon_paths = ['widget.png', 'Console.png', 'keyboard.png', 'widget_green.png', 'keyboard_green.png', 'Console_green.png']
    for icon_name in icon_paths:
        icon_path = os.path.join(project_root, 'Resources', 'Icons', icon_name)
        assert os.path.exists(icon_path), f'Ikon nem található: {icon_path}'

def test_font_family_on_widgets():
    expected_family = 'Ubuntu'
    widgets = [
        options_menu.ui.lblTitle,
        options_menu.ui.lblDescription,
        options_menu.ui.btnReset,
        options_menu.ui.btnSave,
        options_menu.ui.btnManager,
        options_menu.ui.lblUserGuide,
        options_menu.ui.txtinputCommand,
    ]
    for widget in widgets:
        actual_family = widget.font().family()
        assert actual_family == expected_family, f"{widget.objectName()} fontja nem egyezik: {actual_family} ≠ {expected_family}"



def test_loadComboMenu_button_styles_and_fonts():
    options_menu.loadComboMenu()
    combo_layout = options_menu.ui.scrollComboWidgetContents.layout()
    for i in range(combo_layout.count()-1):
        btn = combo_layout.itemAt(i).widget()
        assert btn.styleSheet() == predefined_label_style
        assert btn.font().family() == 'Ubuntu'
        assert btn.height() == 30


def test_updateEntries():
    options_menu.updateEntries()
    assert options_menu.scroll_layout.count() > 1, 'Nem listázódtak a gesztusok a scrollArea-n'

    for i in range(options_menu.scroll_layout.count()):
        item = options_menu.scroll_layout.itemAt(i)
        widget = item.widget()
        if widget is None:
            continue  # például a stretch miatt
            # Ez a gesture_entry QWidget
        btns = widget.findChildren(QPushButton)
        for j in range(len(btns)):
            assert btns[j].styleSheet() == noborder
            assert not btns[j].icon().isNull(), f'A(z) {j+1}. gomb ikonja hiányzik, vagy hibásan tölt be'

            enter_event = QEvent(QEvent.Enter)
            QApplication.sendEvent(btns[j], enter_event)
            assert options_menu.ui.lblDescription.text() != '', f'A(z) {j+1}. gombnál nem jelenik meg a magyarázat'

            leave_event = QEvent(QEvent.Leave)
            QApplication.sendEvent(btns[j], leave_event)
            assert options_menu.ui.lblDescription.text() == '', f'A(z) {j+1}. gombnál nem tűnik el a magyarázat'
          


    options_menu.data.clear()
    options_menu.updateEntries()
    assert options_menu.scroll_layout.count() == 1, 'Nem törlődött a scrollArea üres konfigurációs fájlal'

def test_loadComboMenu_button_events():
    options_menu.loadComboMenu()
    combo_layout = options_menu.ui.scrollComboWidgetContents.layout()
    for i in range(combo_layout.count()-1): 
        btn = combo_layout.itemAt(i).widget()
        btn.enterEvent(None)
        assert btn.styleSheet() == predefined_hover_label_style
        btn.leaveEvent(None)
        assert btn.styleSheet() == predefined_label_style


def test_setStyles():
    assert options_menu.ui.frameBlue.styleSheet() == sidebar_style
    assert options_menu.ui.lblTitle.styleSheet() == sidebar_title_style
    assert options_menu.ui.lblDescription.styleSheet() == description_style
    assert options_menu.ui.btnReset.styleSheet() == options_button_style
    assert options_menu.ui.btnSave.styleSheet() == options_button_style
    assert options_menu.ui.btnManager.styleSheet() == options_button_style
    assert options_menu.ui.scrollCombo.styleSheet() == scrollbar_style
    assert options_menu.ui.lblUserGuide.styleSheet() == train_label_style
    assert options_menu.ui.txtinputCommand.styleSheet() == train_input_style
    assert options_menu.ui.btnCommandOk.styleSheet() == options_button_style

def test_setLayoutSettings():
    assert options_menu.ui.lblDescription.text() == ''

    #Jobb kattos kontextmenü letiltása
    assert options_menu.ui.scrollArea.verticalScrollBar().contextMenuPolicy() == Qt.NoContextMenu
    assert options_menu.ui.scrollArea.horizontalScrollBar().contextMenuPolicy() == Qt.NoContextMenu
    assert options_menu.ui.scrollCombo.verticalScrollBar().contextMenuPolicy() == Qt.NoContextMenu
    assert options_menu.ui.scrollCombo.horizontalScrollBar().contextMenuPolicy() == Qt.NoContextMenu


    assert options_menu.clicked is None
    assert options_menu.predefined_clicked is None

    assert not options_menu.ui.scrollCombo.isVisible()

    assert not options_menu.ui.btnCommandOk.isVisible()
    assert not options_menu.ui.txtinputCommand.isVisible()
    assert not options_menu.ui.frameHide.isVisible()

    assert options_menu.ui.btnCommandOk.text() == ''
    icon = options_menu.ui.btnCommandOk.icon()
    assert not icon.isNull()


def test_btnSave():
    # Elmentjük az aktuális konfigurációt, hogy vissza tudjuk állítani
    original_data = copy.deepcopy(options_menu.data)

    options_menu.data = {
        "1": {
            "gesture": "Zárt ököl",
            "action": None,
            "description": None,
            "highlight": -1
        },
        "3": {
            "gesture": "Felfelé mutatás",
            "action": None,
            "description": None,
            "highlight": -1
        },
        "4": {
            "gesture": "Két ujjal balra",
            "action": None,
            "description": None,
            "highlight": -1
        },
        "5": {
            "gesture": "Nyílt tenyér",
            "action": None,
            "description": None,
            "highlight": -1
        }
    }
    options_menu.ui.btnSave.click()

    options_menu.loadConfig()
    assert options_menu.data != {}, "Mentés után üres maradt a konfigfájl"

    # Visszaállítjuk az eredeti konfigurációt
    options_menu.data = original_data
    options_menu.saveMappings()


def test_btnReset():
    default = {
        "1": {
            "gesture": "Zárt ököl",
            "action": None,
            "description": None,
            "highlight": -1
        },
        "3": {
            "gesture": "Felfelé mutatás",
            "action": None,
            "description": None,
            "highlight": -1
        },
        "4": {
            "gesture": "Két ujjal balra",
            "action": None,
            "description": None,
            "highlight": -1
        },
        "5": {
            "gesture": "Nyílt tenyér",
            "action": None,
            "description": None,
            "highlight": -1
        }
    }

    options_menu.data['1']['highlight'] = 1

    options_menu.ui.btnReset.click()

    assert options_menu.data == default, 'Az alaphelyzet gomb nem működik, a beállítások maradtak'

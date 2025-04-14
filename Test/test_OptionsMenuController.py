import os
import sys
from PySide6.QtWidgets import QApplication, QStackedWidget
from PySide6.QtGui import QFont, QFontDatabase
import copy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI')))

if QApplication.instance() is None:
    app = QApplication(sys.argv)

stacked_widget = QStackedWidget()

from UI.Controllers.OptionsMenuController import CameraOptionsController
from UI.Resources.Stylesheets import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI'))
os.chdir(project_root)

options_menu = CameraOptionsController(stacked_widget)

def test_loadConfig():
    stacked_widget.addWidget(options_menu)
    stacked_widget.setCurrentIndex(0)

    options_menu.loadConfig()
    assert options_menu.data is not None

def test_saveMappings():
    options_menu.loadConfig()
    data = copy.deepcopy(options_menu.data)
    assert options_menu.data is not None, f'Nem sikerült betölteni a konfigurációs fájlt a teszthez'
    options_menu.saveMappings()

    options_menu.loadConfig()
    assert data == options_menu.data, 'A beolvasott és a mentett fájl eltér'

def test_setFont():
    options_menu.loadFont()
    assert options_menu.font is not None

def test_icons():
    icon_paths = ['widget.png', 'Console.png', 'keyboard.png', 'widget_green.png', 'keyboard_green.png', 'Console_green.png']
    for icon_name in icon_paths:
        icon_path = os.path.join(project_root, 'Resources', 'Icons', icon_name)
        assert os.path.exists(icon_path), f'Ikon nem található: {icon_path}'

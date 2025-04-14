import os
import sys
from PySide6.QtWidgets import QApplication, QStackedWidget
from PySide6.QtGui import QFont, QFontDatabase

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI')))

if QApplication.instance() is None:
    app = QApplication(sys.argv)

stacked_widget = QStackedWidget()

from UI.Controllers.CameraOptionsController import CameraOptionsController
from UI.Resources.Stylesheets import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI'))
os.chdir(project_root)

camera_options_menu = CameraOptionsController(stacked_widget)

def test_setFont():
    camera_options_menu.loadFont()
    assert camera_options_menu.font is not None

def test_icons():
    icon_paths = ['camera.png']
    for icon_name in icon_paths:
        icon_path = os.path.join(project_root, 'Resources', 'Icons', icon_name)
        assert os.path.exists(icon_path), f'Ikon nem található: {icon_path}'

def test_loadConfig():
    camera_options_menu.loadSettings()
    print('Loaded config:', camera_options_menu.data)
    assert camera_options_menu.data is not None

import os
import sys
from PySide6.QtWidgets import QApplication, QStackedWidget
from PySide6.QtGui import QFont, QFontDatabase

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI')))


if QApplication.instance() is None:
    app = QApplication(sys.argv)

stacked_widget = QStackedWidget()

from UI.Controllers.LoadingScreenController import LoadingScreenController
from UI.Resources.Stylesheets import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI'))
os.chdir(project_root)

loading_screen = LoadingScreenController(stacked_widget)

def test_icons():
    icon_paths = ['loading.gif']
    for icon_name in icon_paths:
        icon_path = os.path.join(project_root, 'Resources', 'Icons', icon_name)
        assert os.path.exists(icon_path), f'Ikon nem található: {icon_path}'

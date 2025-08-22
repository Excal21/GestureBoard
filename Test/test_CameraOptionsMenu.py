import os
import sys
from PySide6.QtWidgets import QApplication, QStackedWidget
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt, QPoint, QEvent

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI')))

from UI.Controllers.CameraOptionsController import CameraOptionsController
from UI.Resources.Stylesheets.styles import *

if QApplication.instance() is None:
    app = QApplication(sys.argv)

stacked_widget = QStackedWidget()

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI'))
os.chdir(project_root)

camera_options_menu = CameraOptionsController(stacked_widget)
camera_options_menu.initUI()

def test_icons():
    icon_paths = ['camera.png']
    for icon_name in icon_paths:
        icon_path = os.path.join(project_root, 'Resources', 'Icons', icon_name)
        assert os.path.exists(icon_path), f'Ikon nem található: {icon_path}'

def test_loadConfig():
    print('Loaded config:', camera_options_menu.data)
    assert camera_options_menu.data is not None

def test_saveConfig():
    #Kameraindexet azért nem nézünk, mert ha nincs kamera, akkor -1 -re visszaáll
    camera_options_menu.ui.sliderHue.setValue(255)
    camera_options_menu.ui.spinConfidence.setValue(80)
    camera_options_menu.ui.spinFrameCnt.setValue(10)
    camera_options_menu.ui.spinDelay.setValue(5)

    camera_options_menu.saveSettings()

    camera_options_menu.loadSettings()
    assert camera_options_menu.ui.sliderHue.value() == 255, 'A színeltolás értéke nem mentődött el'
    assert camera_options_menu.ui.spinConfidence.value() == 80, 'A magabiztosság értéke nem mentődött el'
    assert camera_options_menu.ui.spinFrameCnt.value() == 10, 'A frame count nem mentődött el'
    assert camera_options_menu.ui.spinDelay.value() == 5 , 'A delay értéke nem mentődött el'

def test_setStyles():
    camera_options_menu.setStyles()
    assert camera_options_menu.ui.frameBlue.styleSheet() == sidebar_style
    assert camera_options_menu.ui.lblTitle.styleSheet() == sidebar_title_style
    assert camera_options_menu.ui.btnSave.styleSheet() == options_button_style
    assert camera_options_menu.ui.btnBack.styleSheet() == options_button_style
    assert camera_options_menu.ui.btnStartCam.styleSheet() == options_button_style
    assert camera_options_menu.ui.lblCamera.styleSheet() == train_label_style
    assert camera_options_menu.ui.lblHue.styleSheet() == train_label_style
    assert camera_options_menu.ui.lblConfidence.styleSheet() == train_label_style
    assert camera_options_menu.ui.lblFrameCnt.styleSheet() == train_label_style
    assert camera_options_menu.ui.lblDelay.styleSheet() == train_label_style
    assert camera_options_menu.ui.sliderHue.styleSheet() == slider_style
    assert camera_options_menu.ui.comboCamera.styleSheet() == camera_combo_style
    assert camera_options_menu.ui.lblCvImg.styleSheet() == camera_label_style
    assert camera_options_menu.ui.spinConfidence.styleSheet() == train_input_style
    assert camera_options_menu.ui.spinFrameCnt.styleSheet() == train_input_style
    assert camera_options_menu.ui.spinDelay.styleSheet() == train_input_style

def test_ubuntu_font_family():
    expected_family = 'Ubuntu'
    widgets = [
        camera_options_menu.ui.lblTitle,
        camera_options_menu.ui.lblDescription,
        camera_options_menu.ui.comboCamera,
        camera_options_menu.ui.lblCamera,
        camera_options_menu.ui.lblHue,
        camera_options_menu.ui.lblConfidence,
        camera_options_menu.ui.lblFrameCnt,
        camera_options_menu.ui.lblDelay,
        camera_options_menu.ui.btnBack,
        camera_options_menu.ui.btnSave,
        camera_options_menu.ui.btnStartCam,
        camera_options_menu.ui.spinConfidence,
        camera_options_menu.ui.spinFrameCnt,
        camera_options_menu.ui.spinDelay
    ]
    for widget in widgets:
        actual_family = widget.font().family()
        assert actual_family == expected_family, f"{widget.objectName()} betűtípusa nem Ubuntu: {actual_family}"


def test_setEventHandlers():
    assert callable(camera_options_menu.ui.btnSave.enterEvent)
    assert callable(camera_options_menu.ui.btnSave.leaveEvent)
    assert callable(camera_options_menu.ui.btnBack.enterEvent)
    assert callable(camera_options_menu.ui.btnBack.leaveEvent)
    assert callable(camera_options_menu.ui.btnStartCam.enterEvent)
    assert callable(camera_options_menu.ui.btnStartCam.leaveEvent)

    assert callable(camera_options_menu.ui.lblCamera.enterEvent)
    assert callable(camera_options_menu.ui.lblCamera.leaveEvent)
    assert callable(camera_options_menu.ui.lblHue.enterEvent)
    assert callable(camera_options_menu.ui.lblHue.leaveEvent)
    assert callable(camera_options_menu.ui.lblConfidence.enterEvent)
    assert callable(camera_options_menu.ui.lblConfidence.leaveEvent)
    assert callable(camera_options_menu.ui.lblFrameCnt.enterEvent)
    assert callable(camera_options_menu.ui.lblDelay.enterEvent)
    assert callable(camera_options_menu.ui.lblDelay.leaveEvent)


def test_hover_and_leave_events_trigger_styles_and_labels():
    widgets_with_styles = [
        camera_options_menu.ui.btnSave,
        camera_options_menu.ui.btnBack,
    ]

    for widget in widgets_with_styles:
        enter_event = QEvent(QEvent.Enter)
        QApplication.sendEvent(widget, enter_event)
        assert widget.styleSheet() == options_button_hover_style, f"{widget.objectName()} hover stílus nem működik"

        leave_event = QEvent(QEvent.Leave)
        QApplication.sendEvent(widget, leave_event)
        assert widget.styleSheet() == options_button_style, f"{widget.objectName()} nem áll vissza hover stílusról simára"

    # Kameraindító gomb esetén figyelembe vesszük a self.is_camera_on állapotot
    start_cam_widget = camera_options_menu.ui.btnStartCam
    camera_off_style_hover = options_button_hover_style
    camera_off_style_leave = options_button_style
    camera_on_style_hover = options_button_hover_style + 'background-color: rgb(201, 97, 97)'
    camera_on_style_leave = options_button_hover_style + 'background-color: rgb(227, 109, 109)'

    camera_options_menu.is_camera_on = False
    QApplication.sendEvent(start_cam_widget, QEvent(QEvent.Enter))
    assert start_cam_widget.styleSheet() == camera_off_style_hover

    QApplication.sendEvent(start_cam_widget, QEvent(QEvent.Leave))
    assert start_cam_widget.styleSheet() == camera_off_style_leave

    camera_options_menu.is_camera_on = True
    QApplication.sendEvent(start_cam_widget, QEvent(QEvent.Enter))
    assert start_cam_widget.styleSheet() == camera_on_style_hover

    QApplication.sendEvent(start_cam_widget, QEvent(QEvent.Leave))
    assert start_cam_widget.styleSheet() == camera_on_style_leave

    # Tooltip frissítést tesztelünk a label elemeken
    label_tooltips = {
        camera_options_menu.ui.lblCamera: 'Válaszd ki a kamerát, amivel a gesztusokat tudja érzékelni a program!',
        camera_options_menu.ui.lblHue: 'A színek eltolásával beállíthatod, hogy kesztyűben is felismerje a kezedet a program. Kapcsold be a kamerát és állítsd be óvatosan a csúszkával!',
        camera_options_menu.ui.lblConfidence: 'Növelésével csökkenthető a véletlen felismerések száma, de csökken a felismerés érzékenysége.',
        camera_options_menu.ui.lblFrameCnt: 'A program ennyi képkockán keresztül figyeli a gesztust a művelet végrehajtása előtt. Növelésével pontosabb, de lassabb lesz a felismerés.',
        camera_options_menu.ui.lblDelay: 'Két gesztus közt eltelt idő másodpercben. Csökkentésével gyorsabban tudod kiadni a parancsokat.',
    }

    for label, expected_text in label_tooltips.items():
        enter_event = QEvent(QEvent.Enter)
        QApplication.sendEvent(label, enter_event)
        assert expected_text in camera_options_menu.ui.lblDescription.text(), f"{label.objectName()} hover leírása hibás"

        leave_event = QEvent(QEvent.Leave)
        QApplication.sendEvent(label, leave_event)
        assert camera_options_menu.ui.lblDescription.text() == '', f"{label.objectName()} leírása nem törlődik hover után"


def test_user_input_boundaries():
    # Confidence SpinBox: 0 alá és 100 fölé próbálunk beállítani
    spin = camera_options_menu.ui.spinConfidence

    spin.setValue(-10)
    assert spin.value() >= 0, f'Túl kicsi érték engedve: {spin.value()} < 0'
    spin.setValue(150)
    assert spin.value() <= 100, f'Túl nagy érték engedve: {spin.value()} > 100'


    spin = camera_options_menu.ui.spinFrameCnt
    spin.setValue(-5)
    assert spin.value() >= 1, f'Túl kicsi érték engedve: {spin.value()} < 1'
    spin.setValue(1000)
    assert spin.value() <= 30, f'Túl nagy érték engedve: {spin.value()} > 30'


    spin = camera_options_menu.ui.spinDelay
    spin.setValue(-1)
    assert spin.value() >= 0, f'Túl kicsi érték engedve: {spin.value()} < 0'
    spin.setValue(60)
    assert spin.value() <= 5, f'Túl nagy érték engedve: {spin.value()} > 5'


    #Színtoló csúszka
    slider = camera_options_menu.ui.sliderHue

    slider.setValue(-1)
    assert slider.value() >= 0, f'sliderHue túl alacsony értéket engedne: {slider.value()}'
    slider.setValue(256)
    assert slider.value() <= 255, f'sliderHue túl magas értéket engedne: {slider.value()}'
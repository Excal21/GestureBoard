import cv2
import json


from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap, QRegion, QPainterPath, QPainter, QColor


from Resources.Stylesheets.styles import *
from Views.ui_cameraOptionsForm import Ui_Form
from Models.RecognizerHandler import RecognizerHandler
from Models.Recorder import Recorder
from Models.OverlayHandler import OverlayHandler

from time import sleep
from Controllers.BaseController import BaseController
from Resources.Fonts.FontLoader import FontLoader
from PySide6.QtCore import QCoreApplication

class CameraOptionsController(BaseController):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.stacked_widget = stacked_widget

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.initUI(
            {
                'checkFrameThrottling': checkbox_style,
                'checkInvertButtons': checkbox_style
            }
        )
        
        self.setEventHandlers()

        self.rec = Recorder()
        self.is_camera_on = False
        self.data = {}
        self.gesturedata = {}

        self.timer = None

        self.overlay = OverlayHandler.getInstance()

        self.ui.sliderHue.setRange(0, 255)
        self.ui.sliderDistance.setRange(100, 500)
        self.ui.spinConfidence.setRange(0, 100)
        self.ui.spinFrameCnt.setRange(1, 30)
        self.ui.spinDelay.setRange(0, 5)
        self.ui.spinDelay.setSingleStep(0.1)
        self.ui.spinDelay.setDecimals(1)
        self.ui.sliderSensitivity.setRange(5, 30)
        self.ui.sliderDrift.setRange(100, 350)

        self.ui.lblCvImg.setAlignment(Qt.AlignCenter)
        self.ui.lblCvImg.setPixmap(QPixmap('Resources/Icons/camera.png').scaled(100, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # self.loadSettings()
        # self.loadCameraCombo()
        self.setLayoutSettings()


        #TOUCHLESSPAD
        # self.ui.lblRadius.setVisible(False)
        # self.ui.spinRadius.setVisible(False)
        # self.ui.lblSensitivity.setVisible(False)
        # self.ui.sliderSensitivity.setVisible(False)
        
#region Kamerakép
    def startCamera(self):
        with open('Config/UserSettings.json', 'r', encoding='utf-8') as file:
            self.gesturedata = json.load(file)

        if not self.is_camera_on:
            self.rec.loadCameraOnly(self.data['Camera'])
            self.rec.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.rec.cap.set(cv2.CAP_PROP_FPS, 60)
            self.timer = QTimer(self)
            sleep(1)
            self.timer.timeout.connect(self.updateFrame)
            self.timer.start(10)
            self.is_camera_on = True
            self.ui.btnStartCam.setStyleSheet(options_button_active_style + 'background-color: rgb(201, 97, 97)')
            self.ui.btnStartCam.setText(QCoreApplication.translate('CameraOptionsController', 'Leállítás'))
        else:
            self.timer.stop()
            self.rec.cap.release()
            self.ui.lblCvImg.setPixmap(QPixmap('Resources/Icons/camera.png').scaled(100, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.is_camera_on = False
            self.ui.btnStartCam.setText(QCoreApplication.translate('CameraOptionsController', 'Kamerateszt'))
            self.ui.btnStartCam.setStyleSheet(options_button_style)

    def updateFrame(self):
        frame = self.rec.getFrame(self.ui.sliderHue.value())

        frame, gesture = RecognizerHandler.getInstance().annotate(frame, True, self.ui.sliderDistance.value())


        if frame is not None:
            h, w, _ = frame.shape

            crop_width, crop_height = 500, 300
            resize_width, resize_height = 270, 170

            center_x, center_y = w // 2, h // 2

            x1, x2 = center_x - crop_width // 2, center_x + crop_width // 2
            y1, y2 = center_y - crop_height // 2, center_y + crop_height // 2

            cropped_frame = frame[y1:y2, x1:x2].copy()  # C-contiguous hiba elkerülése miatt

            resized_frame = cv2.resize(cropped_frame, (resize_width, resize_height), interpolation=cv2.INTER_AREA)

            if gesture is not None:
                gesture_text = f'{QCoreApplication.translate('Pretrained gesture', self.gesturedata[gesture[0]]['gesture'])}   {int(gesture[1])}%'
            else:
                gesture_text = ''

            h, w, ch = resized_frame.shape
            bytes_per_line = ch * w
            q_image = QImage(resized_frame.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

            #Gesztusvisszajelzés a képre
            p = QPainter(q_image)
            p.setFont(FontLoader.getFont())
            p.setPen(QColor(156, 220, 254))
            p.drawText(30, 40, gesture_text)
            p.end()



            path = QPainterPath()
            radius = 10  # Lekerekítés mértéke
            path.addRoundedRect(0, 0, self.ui.lblCvImg.width(), self.ui.lblCvImg.height(), radius, radius)
            region = QRegion(path.toFillPolygon().toPolygon())

            self.ui.lblCvImg.setMask(region)
            self.ui.lblCvImg.setPixmap(QPixmap.fromImage(q_image))

#endregion

#region Layout beállítások
    def setLayoutSettings(self):
        self.scroll_area = self.ui.scrollArea
        self.scroll_area.setWidgetResizable(True)
        self.ui.scrollArea.verticalScrollBar().setContextMenuPolicy(Qt.NoContextMenu)
        self.scroll_layout = QVBoxLayout(self.ui.scrollAreaWidgetContents)
        self.scroll_area.setWidget(self.ui.scrollAreaWidgetContents)
        self.scroll_layout.setContentsMargins(0, 0, 20, 0)

        self.ui.spinConfidence.setAlignment(Qt.AlignCenter)
        self.ui.spinFrameCnt.setAlignment(Qt.AlignCenter)
        self.ui.spinDelay.setAlignment(Qt.AlignCenter)
        self.ui.spinConfidence.setContentsMargins(0, 0, 0, 0)
        self.ui.spinFrameCnt.setContentsMargins(0, 0, 0, 0)
        self.ui.spinDelay.setContentsMargins(0, 0, 0, 0)
        
        self.scroll_layout.addSpacing(25)
        
        pairs = [
                (self.ui.lblCamera, self.ui.comboCamera),
                (self.ui.lblHue, self.ui.sliderHue),
                (self.ui.lblDistance, self.ui.sliderDistance),
                (self.ui.lblConfidence, self.ui.spinConfidence),
                (self.ui.lblFrameCnt, self.ui.spinFrameCnt),
                (self.ui.lblDelay, self.ui.spinDelay),
                (self.ui.lblFrameThrottling, self.ui.checkFrameThrottling),
                (self.ui.lblMouseSettings, None),
                (self.ui.lblSensitivity, self.ui.sliderSensitivity),
                (self.ui.lblRadius, self.ui.sliderDrift),
                (self.ui.lblInvertButtons, self.ui.checkInvertButtons)
            ]

        for widget1, widget2 in pairs:
            line = QHBoxLayout()
            if widget1: line.addWidget(widget1)
            line.addStretch()
            if widget2: line.addWidget(widget2)
            self.scroll_layout.addLayout(line)
    
        self.scroll_layout.addStretch()

        self.ui.spinConfidence.setFixedWidth(50)
        self.ui.spinFrameCnt.setFixedWidth(50)
        self.ui.spinDelay.setFixedWidth(50)

        self.ui.sliderHue.setFixedWidth(200)
        self.ui.sliderDistance.setFixedWidth(200)
        self.ui.sliderSensitivity.setFixedWidth(200)
        self.ui.sliderDrift.setFixedWidth(200)

        self.ui.lblCamera.setFixedHeight(42)
        self.ui.comboCamera.setFixedHeight(42)
        self.ui.lblHue.setFixedHeight(42)
        self.ui.lblDistance.setFixedHeight(42)
        self.ui.lblConfidence.setFixedHeight(42)
        self.ui.lblFrameCnt.setFixedHeight(42)
        self.ui.lblDelay.setFixedHeight(42)

        self.ui.lblMouseSettings.setContentsMargins(0, 30, 0, 0)
        self.ui.lblMouseSettings.setFixedHeight(72)
        self.ui.lblSensitivity.setFixedHeight(42)
        self.ui.lblRadius.setFixedHeight(42)
        self.ui.btnStartCam.setFixedHeight(42)
        
        self.ui.checkFrameThrottling.setFixedHeight(40) #Ezek csak a placeholderek!! QSS állítja a valósat
        self.ui.checkFrameThrottling.setFixedWidth(50)
        self.ui.checkFrameThrottling.setChecked(True)

        self.ui.checkInvertButtons.setFixedHeight(40)
        self.ui.checkInvertButtons.setFixedWidth(50)
        self.ui.checkInvertButtons.setChecked(False)
#endregion

#region Eseménykezelők
    def updateCameraIndex(self, index):
        self.data['Camera'] = index

    def sliderDriftEnter(self, event):
        self.ui.lblDescription.setText(
        self.textToHTML(QCoreApplication.translate('CameraOptionsController' , 'A szürke körön belül finom mozgást végezhetsz az egérrel, '
                        'míg a körön kívül sodródni fog a kurzor.')))
        self.overlay.show()

    def sliderDriftLeave(self, event):
        self.ui.lblDescription.setText('')
        self.overlay.hide()
    
    def setEventHandlers(self):
        self.stacked_widget.currentChanged.connect(self.onReturn)

        self.ui.comboCamera.currentIndexChanged.connect(self.updateCameraIndex)
    

        self.ui.btnSave.clicked.connect(self.saveSettings)
        self.ui.btnSave.enterEvent = lambda event: self.ui.btnSave.setStyleSheet(options_button_hover_style)
        self.ui.btnSave.leaveEvent = lambda event: self.ui.btnSave.setStyleSheet(options_button_style)

        self.ui.btnBack.enterEvent = lambda event: self.ui.btnBack.setStyleSheet(options_button_hover_style)
        self.ui.btnBack.leaveEvent = lambda event: self.ui.btnBack.setStyleSheet(options_button_style)
        self.ui.btnBack.clicked.connect(self.backToMainMenu)

        self.ui.btnStartCam.enterEvent = lambda event: self.ui.btnStartCam.setStyleSheet(options_button_hover_style if not self.is_camera_on else options_button_hover_style + 'background-color: rgb(201, 97, 97)')
        
        self.ui.btnStartCam.leaveEvent = lambda event: self.ui.btnStartCam.setStyleSheet(options_button_style if not self.is_camera_on else options_button_hover_style + 'background-color: rgb(227, 109, 109)')
        self.ui.btnStartCam.clicked.connect(self.startCamera)



        # QTranslator használata a magyar szövegekhez, fordítás .qm fájlból érkezik

        self.ui.comboCamera.enterEvent = lambda event: self.ui.lblDescription.setText(
            self.textToHTML(QCoreApplication.translate('CameraOptionsController', 'Válaszd ki a kamerát, amivel a gesztusokat tudja érzékelni a program!')))
        self.ui.comboCamera.leaveEvent = lambda event: self.ui.lblDescription.setText('')

        self.ui.sliderHue.enterEvent = lambda event: self.ui.lblDescription.setText(
            self.textToHTML(QCoreApplication.translate('CameraOptionsController', 'A színek eltolásával beállíthatod, hogy kesztyűben is felismerje a kezedet a program. Kapcsold be a kamerát és állítsd be óvatosan a csúszkával!')))
        self.ui.sliderHue.leaveEvent = lambda event: self.ui.lblDescription.setText('')

        self.ui.sliderDistance.enterEvent = lambda event: self.ui.lblDescription.setText(
            self.textToHTML(QCoreApplication.translate('CameraOptionsController', 'A csúszka segítségével állítsd be a kezed távolságát a kamerától! Túl nagy távolság esetén előfordulhat, hogy más ember kezét érzékeli a GestureBoard.')))
        self.ui.sliderDistance.leaveEvent = lambda event: self.ui.lblDescription.setText('')

        self.ui.spinConfidence.enterEvent = lambda event: self.ui.lblDescription.setText(
            self.textToHTML(QCoreApplication.translate('CameraOptionsController', 'Növelésével csökkenthető a véletlen felismerések száma, de csökken a felismerés érzékenysége.')))
        self.ui.spinConfidence.leaveEvent = lambda event: self.ui.lblDescription.setText('')

        self.ui.spinFrameCnt.enterEvent = lambda event: self.ui.lblDescription.setText(
            self.textToHTML(QCoreApplication.translate('CameraOptionsController', 'A program ennyi képkockán keresztül figyeli a gesztust a művelet végrehajtása előtt. Növelésével pontosabb, de lassabb lesz a felismerés.')))
        self.ui.spinFrameCnt.leaveEvent = lambda event: self.ui.lblDescription.setText('')

        self.ui.spinDelay.enterEvent = lambda event: self.ui.lblDescription.setText(
            self.textToHTML(QCoreApplication.translate('CameraOptionsController', 'Két gesztus közt eltelt idő másodpercben. Csökkentésével gyorsabban tudod kiadni a parancsokat.')))
        self.ui.spinDelay.leaveEvent = lambda event: self.ui.lblDescription.setText('')

        self.ui.checkFrameThrottling.enterEvent = lambda event: self.ui.lblDescription.setText(
            self.textToHTML(QCoreApplication.translate('CameraOptionsController', 'Dinamikus képkocka-korlátozás. Csökkenti a CPU használatot, de nagyban növelheti a reakcióidőt.')))
        self.ui.checkFrameThrottling.leaveEvent = lambda event: self.ui.lblDescription.setText('')

        self.ui.sliderSensitivity.enterEvent = lambda event: self.ui.lblDescription.setText(
            self.textToHTML(QCoreApplication.translate('CameraOptionsController', 'Az egérmutató érzékenysége a sodródásmentes zónán kívül. Minél nagyobb az érték, annál gyorsabban mozog az egérmutató.')))
        self.ui.sliderSensitivity.leaveEvent = lambda event: self.ui.lblDescription.setText('')

        self.ui.checkInvertButtons.enterEvent = lambda event: self.ui.lblDescription.setText(
            self.textToHTML(QCoreApplication.translate('CameraOptionsController', 'Felcseréli a jobb és bal egérgombokat egérmódban.')))
        self.ui.checkInvertButtons.leaveEvent = lambda event: self.ui.lblDescription.setText('')

        self.ui.sliderDrift.enterEvent = lambda event: self.sliderDriftEnter(event)
        self.ui.sliderDrift.leaveEvent = lambda event: self.sliderDriftLeave(event)
        self.ui.sliderDrift.valueChanged.connect(lambda value: self.overlay.setRadius(value))
#endregion

#region Beállítások kezelése
    def loadCameraCombo(self):
        self.ui.comboCamera.clear()
        cameras = RecognizerHandler.getInstance().getCameras()
        if cameras == []:
            self.ui.comboCamera.addItem(QCoreApplication.translate('CameraOptionsController' , 'Nem található'))
            self.ui.comboCamera.setEnabled(False)
            self.ui.btnStartCam.setEnabled(False)
            return
        else:
            for cameraIDX in cameras:
                if cameraIDX == 0:
                    self.ui.comboCamera.addItem(QCoreApplication.translate('CameraOptionsController' , 'Beépített kamera'))
                else:
                    self.ui.comboCamera.addItem(f'{cameraIDX + 1}. kamera')

    def onReturn(self, index):
        if index == 1:
            self.loadCameraCombo()
        elif index == 5:
            self.overlay.setCircleOnly(True)
            self.loadSettings()

    def loadSettings(self):
        with open('Config/CameraSettings.json', 'r') as file:
            self.data = json.load(file)
            self.ui.comboCamera.setCurrentIndex(self.data['Camera'])
            self.ui.sliderHue.setValue(self.data['HueOffset'])
            self.ui.sliderDistance.setValue(self.data['Distance'])
            self.ui.spinConfidence.setValue(self.data['Confidence']*100)
            self.ui.spinFrameCnt.setValue(self.data['FrameCount'])
            self.ui.spinDelay.setValue(self.data['Delay'])
            self.ui.checkFrameThrottling.setChecked(self.data['FrameThrottling'])
            self.ui.sliderSensitivity.setValue(self.data['Sensitivity'])
            self.ui.sliderDrift.setValue(self.data['Drift'])
            self.ui.checkInvertButtons.setChecked(self.data['InvertButtons'])


    
    def saveSettings(self):
        self.data['Camera'] = self.ui.comboCamera.currentIndex()
        self.data['HueOffset'] = self.ui.sliderHue.value()
        self.data['Distance'] = self.ui.sliderDistance.value()
        self.data['Confidence'] = self.ui.spinConfidence.value()/100
        self.data['FrameCount'] = self.ui.spinFrameCnt.value()
        self.data['Delay'] = self.ui.spinDelay.value()
        self.data['FrameThrottling'] = self.ui.checkFrameThrottling.isChecked()
        self.data['Sensitivity'] = self.ui.sliderSensitivity.value()
        self.data['Drift'] = self.ui.sliderDrift.value()
        self.data['InvertButtons'] = self.ui.checkInvertButtons.isChecked()

        with open('Config/CameraSettings.json', 'w') as file:
            json.dump(self.data, file, indent=4)
        

        if self.is_camera_on:
            self.startCamera() #A start működése miatt itt pont, hogy le fogja állítani

        self.stacked_widget.setCurrentIndex(1)

    def backToMainMenu(self):
        if self.is_camera_on:
            self.startCamera()
        self.stacked_widget.setCurrentIndex(1)

#endregion

    
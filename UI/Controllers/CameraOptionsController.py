import os
import sys

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QFontDatabase, QFont, QImage, QPixmap, QRegion, QPainterPath, QIcon
import cv2
from Resources.Stylesheets.styles import *
from Views.ui_cameraOptionsForm import Ui_Form
from Models.RecognizerHandler import RecognizerHandler
from Models.Recorder import Recorder
from time import sleep

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Views')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Resources', 'Stylesheets')))

class CameraOptionsController(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.stacked_widget = stacked_widget

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.loadFont()

        self.rec = Recorder()
        
        self.is_camera_on = False

        #Kék alapú díszítősáv elrendezése
        layout = QVBoxLayout(self.ui.frameBlue)
        layout.setContentsMargins(0, 55, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.ui.lblTitle, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.ui.frameBlue.setStyleSheet(sidebar_style)
        self.ui.lblTitle.setStyleSheet(sidebar_title_style)

        self.ui.lblDescription.setText('')

        self.ui.btnBack.setStyleSheet(options_button_style)
        self.ui.btnBack.setFont(self.font)
        self.ui.btnBack.clicked.connect(lambda event: self.stacked_widget.setCurrentIndex(1))
        self.ui.btnBack.enterEvent = lambda event: self.ui.btnBack.setStyleSheet(options_button_hover_style)
        self.ui.btnBack.leaveEvent = lambda event: self.ui.btnBack.setStyleSheet(options_button_style)

        self.ui.btnStartCam.setStyleSheet(options_button_style)
        self.ui.btnStartCam.setFont(self.font)

        self.ui.btnStartCam.enterEvent = lambda event, active = self.is_camera_on: self.ui.btnStartCam.setStyleSheet(options_button_hover_style if not self.is_camera_on else options_button_hover_style + 'background-color: rgb(201, 97, 97)')
        
        self.ui.btnStartCam.leaveEvent = lambda event, active = self.is_camera_on: self.ui.btnStartCam.setStyleSheet(options_button_style if not self.is_camera_on else options_button_hover_style + 'background-color: rgb(227, 109, 109)')
        self.ui.btnStartCam.clicked.connect(self.startCamera)


        self.ui.lblCamera.setStyleSheet(train_label_style)
        self.ui.lblCamera.setFont(self.font)

        self.ui.lblHue.setStyleSheet(train_label_style)
        self.ui.lblHue.setFont(self.font)

        self.ui.lblConfidence.setStyleSheet(train_label_style)
        self.ui.lblConfidence.setFont(self.font)

        self.ui.lblFrameCnt.setStyleSheet(train_label_style)
        self.ui.lblFrameCnt.setFont(self.font)

        self.ui.lblDelay.setStyleSheet(train_label_style)
        self.ui.lblDelay.setFont(self.font)


        self.ui.sliderHue.setStyleSheet(slider_style)

        self.ui.txtInputCamera.setStyleSheet(train_input_style)
        self.ui.txtInputCamera.setFont(self.font)
        self.ui.txtInputCamera.setContextMenuPolicy(Qt.NoContextMenu)

        self.ui.lblCamera.enterEvent = lambda event: self.ui.lblDescription.setText(self.textToHTML('Itt választhatod ki a kamerát a kamera indexével vagy hálózati elérésével. Alapból a beépített kamera van beállítva.'))
        self.ui.lblCamera.leaveEvent = lambda event: self.ui.lblDescription.setText('')


        self.ui.lblHue.enterEvent = lambda event: self.ui.lblDescription.setText(self.textToHTML('A színek eltolásával beállíthatod, hogy kesztyűben is felismerje a kezedet a program. Kapcsold be a kamerát és állítsd be óvatosan a csúszkával!'))
        self.ui.lblHue.leaveEvent = lambda event: self.ui.lblDescription.setText('')

        self.ui.lblConfidence.enterEvent = lambda event: self.ui.lblDescription.setText(self.textToHTML('Növelésével csökkenthető a véletlen felismerések száma, de csökken a felismerés érzékenysége.'))
        self.ui.lblConfidence.leaveEvent = lambda event: self.ui.lblDescription.setText('')

        self.ui.lblFrameCnt.enterEvent = lambda event: self.ui.lblDescription.setText(self.textToHTML('A program ennyi képkockán keresztül figyeli a gesztust a művelet végrehajtása előtt. Növelésével pontosabb, de lassabb lesz a felismerés.'))
        self.ui.lblCvImg.setStyleSheet(camera_label_style)

        self.ui.lblDelay.enterEvent = lambda event: self.ui.lblDescription.setText(self.textToHTML('Két gesztus közt eltelt idő másodpercben. Csökkentésével gyorsabban tudod kiadni a parancsokat.'))
        
            
        self.ui.lblDelay.leaveEvent = lambda event: self.ui.lblDescription.setText('')

        #Gombok ikonjainak beállítása
        self.ui.lblCvImg.setAlignment(Qt.AlignCenter)
        self.ui.lblCvImg.setPixmap(QPixmap('Resources\\Icons\\camera.png').scaled(100, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def startCamera(self):
        if not self.is_camera_on:
            self.rec.loadCameraOnly()
            self.rec.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.rec.cap.set(cv2.CAP_PROP_FPS, 60)
            self.timer = QTimer(self)
            sleep(1)
            self.timer.timeout.connect(self.updateFrame)
            self.timer.start(10)
            self.is_camera_on = True
            self.ui.btnStartCam.setStyleSheet(options_button_active_style)
            self.ui.btnStartCam.setText('Kamera leállítása')
        else:
            self.timer.stop()
            self.rec.cap.release()
            self.ui.lblCvImg.setPixmap(QPixmap('Resources\\Icons\\camera.png').scaled(100, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.is_camera_on = False
            self.ui.btnStartCam.setText('Kamera tesztelése')
            self.ui.btnStartCam.setStyleSheet(options_button_style)

#region Kamerakép
    def updateFrame(self):
        frame = RecognizerHandler.getInstance().annotate(self.rec.cap.read()[1])
        if frame is not None:
            h, w, _ = frame.shape

            crop_width, crop_height = 500, 300
            resize_width, resize_height = 270, 170

            center_x, center_y = w // 2, h // 2

            x1, x2 = center_x - crop_width // 2, center_x + crop_width // 2
            y1, y2 = center_y - crop_height // 2, center_y + crop_height // 2

            cropped_frame = frame[y1:y2, x1:x2].copy()  # C-contiguous hiba elkerülése miatt

            resized_frame = cv2.resize(cropped_frame, (resize_width, resize_height), interpolation=cv2.INTER_AREA)

            h, w, ch = resized_frame.shape
            bytes_per_line = ch * w
            q_image = QImage(resized_frame.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()


            path = QPainterPath()
            radius = 10  # Lekerekítés mértéke
            path.addRoundedRect(0, 0, self.ui.lblCvImg.width(), self.ui.lblCvImg.height(), radius, radius)
            region = QRegion(path.toFillPolygon().toPolygon())

            self.ui.lblCvImg.setMask(region)
            self.ui.lblCvImg.setPixmap(QPixmap.fromImage(q_image))

#endregion

    def textToHTML(self, text):
        return '''<html>
            <style>
                p { line-height: 1.2;
                    font-size: 12pt; }
            </style>
            <body>
                <p align='justify'>'''+ text +'''</p>
                </body>
            </html>'''
            


    def loadFont(self):
        font_id = QFontDatabase.addApplicationFont('Resources\\Fonts\\Ubuntu-R.ttf')
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.font = QFont(font_family, 16)
            self.ui.lblTitle.setFont(self.font)
            self.ui.lblDescription.setFont(self.font)
        else:
            print('Hiba: Nem sikerült betölteni az Ubuntu fontot!')
        
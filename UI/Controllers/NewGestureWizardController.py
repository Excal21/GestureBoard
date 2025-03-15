import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QApplication
from PySide6.QtGui import QFontDatabase, QFont, QMovie, QPixmap, QShortcut, QIcon, QImage, QRegion, QPainterPath
from PySide6.QtCore import QThread, Signal, QSize, QTimer
from time import sleep
from Resources.Stylesheets.styles import *
from Views.ui_newGestureWizardForm import Ui_Form
from Models.Recorder import Recorder
import json
import shutil
import cv2
from Models.RecognizerHandler import RecognizerHandler


class NewGestureWizardController(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        self.ui = Ui_Form()
        self.ui.setupUi(self)
    
        self.loadFont()

        self.recording_stage = 0
        self.__cap = None
        self.rec = Recorder()
        

        self.timer = QTimer(self)


        #Kék alapú díszítősáv elrendezése
        layout = QVBoxLayout(self.ui.frameBlue)
        layout.setContentsMargins(0, 55, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.ui.lblTitle, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.ui.frameBlue.setStyleSheet(sidebar_style)
        self.ui.lblTitle.setStyleSheet(sidebar_title_style)
        

#region Új gesztus varázsló
        #Felbukkanó új gesztus varázsló elrendezése
        self.ui.frameNewGesture_layout = QVBoxLayout(self.ui.frameNewGesture)
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(self.ui.lblInfo, alignment=Qt.AlignCenter)
        horizontal_layout.addStretch()
        self.ui.lblInfo.setStyleSheet(info_label_style)
        self.ui.lblInfo.setFont(self.font)

        self.ui.frameNewGesture_layout.addLayout(horizontal_layout)
        self.ui.frameNewGesture_layout.setContentsMargins(0, 55, 0, 0)
        self.lblImage = QLabel(self.ui.frameNewGesture)
        self.lblImage.setFixedSize(200, 200)
        self.lblImage.setAlignment(Qt.AlignCenter)
        self.ui.frameNewGesture_layout.addWidget(self.lblImage, alignment=Qt.AlignCenter)
        self.ui.frameNewGesture_layout.addWidget(self.ui.lblCvImg, alignment=Qt.AlignCenter)
        self.lblImage.setPixmap(QPixmap(os.path.join(os.path.dirname(__file__), '..', 'Resources', 'Icons', 'hand.png')).scaled(100, 100, Qt.KeepAspectRatio))
        self.ui.lblCvImg.setStyleSheet(camera_label_style)
        self.ui.lblCvImg.hide()

        #Geszuts neve input mező
        vertical_layout = QHBoxLayout()
        self.ui.lblGestureInputLabel.setStyleSheet(train_label_style)
        self.ui.txtinputGestureName.setStyleSheet(train_input_style)
        self.ui.btnNameOK.setStyleSheet(options_button_style)
        self.ui.lblGestureInputLabel.setFont(self.font)
        self.ui.txtinputGestureName.setFont(self.font)
        self.ui.txtinputGestureName.setContextMenuPolicy(Qt.NoContextMenu)


        vertical_layout.addWidget(self.ui.lblGestureInputLabel, alignment=Qt.AlignCenter)
        vertical_layout.addWidget(self.ui.txtinputGestureName, alignment=Qt.AlignCenter)
        vertical_layout.addWidget(self.ui.btnNameOK, alignment=Qt.AlignCenter)

        self.ui.btnNameOK.setIcon(QIcon('Resources\\Icons\\check.png'))
        self.ui.btnNameOK.setIconSize(QSize(30, 30))
        self.ui.btnNameOK.enterEvent = lambda event: self.ui.btnNameOK.setStyleSheet(options_button_hover_style)
        self.ui.btnNameOK.leaveEvent = lambda event: self.ui.btnNameOK.setStyleSheet(options_button_style)
        self.ui.btnNameOK.clicked.connect(self.record)

        #Középre igazított usert segítő szövegdoboz
        self.ui.lblUserGuide.setStyleSheet(guide_style)
        self.ui.lblUserGuide.setAlignment(Qt.AlignCenter) 
        self.ui.lblUserGuide.setFont(self.font)
        self.ui.lblUserGuide.setText('')

        self.ui.frameNewGesture_layout.addWidget(self.ui.lblUserGuide, alignment=Qt.AlignCenter)
        self.ui.frameNewGesture_layout.addStretch()

        shortcut = QShortcut(Qt.Key_Space, self)
        shortcut.setContext(Qt.ApplicationShortcut)
        shortcut.activated.connect(self.record)
#endregion


#region Record

    def record(self):
        self.rec.load(self.stacked_widget.widget(3).data)
        self.rec.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.rec.cap.set(cv2.CAP_PROP_FPS, 60)
        print('Train meghívva')
        self.__gesture_id = int(max(self.stacked_widget.widget(3).data.keys())) + 1 if self.stacked_widget.widget(3).data else 0
        if self.recording_stage == 0:
            self.gesture_name = self.ui.txtinputGestureName.text()

            self.timer = QTimer(self)
                    # QTimer használata while True helyett
            sleep(1)
            self.timer.timeout.connect(self.updateFrame)
            self.timer.start(10)
            self.lblImage.hide()
            self.ui.lblCvImg.show()
            self.ui.frameNewGesture.show()
            self.ui.lblGestureInputLabel.hide()
            self.ui.txtinputGestureName.hide()
            self.ui.btnNameOK.hide()
            self.lblImage.hide()

            self.ui.lblUserGuide.show()
            self.ui.lblUserGuide.setText('Tartsd a kezed a kívánt gesztus pozíciójában, majd nyomj szőközt a másik kezeddel!')
            self.recording_stage = 1
            print('Elindítva!')

        elif self.recording_stage == 1:
            print('Első rész')
            self.rec.record_batch(self.__gesture_id, 20)
            print('Első szakasz rögzítve!')
            self.ui.lblUserGuide.setText('Most picit mozdítsd el ugyanebben a pozícióban a kezed, majd nyomj szőközt a másik kezeddel!')
            self.recording_stage = 2

        elif self.recording_stage == 2:
            self.rec.record_batch(self.__gesture_id, 20)
            print('Második szakasz rögzítve!')
            self.rec.release()
            print('Mentve!')
            self.recording_stage = 0
            self.ui.lblUserGuide.setText('A gesztus sikeresen rögzítve!')
            sleep(2)
            self.ui.lblUserGuide.setText('')
            self.ui.lblUserGuide.hide()
            
            self.ui.lblGestureInputLabel.show()
            self.ui.txtinputGestureName.show()
            self.ui.btnNameOK.show()
            self.ui.lblCvImg.hide()
            self.timer.stop()
            self.lblImage.show()


            gesture_entry = {'gesture' : self.gesture_name, 'action' : None}
            print(self.stacked_widget.widget(3).data)
            self.stacked_widget.widget(3).data[str(self.__gesture_id)] = gesture_entry
            print(self.stacked_widget.widget(3).data)

            self.stacked_widget.setCurrentIndex(3)


#endregion

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
            radius = 10
            path.addRoundedRect(0, 0, self.ui.lblCvImg.width(), self.ui.lblCvImg.height(), radius, radius)
            region = QRegion(path.toFillPolygon().toPolygon())


            self.ui.lblCvImg.setMask(region)
            self.ui.lblCvImg.setPixmap(QPixmap.fromImage(q_image))


#endregion


    def loadFont(self):
        font_id = QFontDatabase.addApplicationFont('Resources\\Fonts\\Ubuntu-R.ttf')
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.font = QFont(font_family, 16)
            self.ui.lblTitle.setFont(self.font)
            self.ui.lblDescription.setFont(self.font)
        else:
            print('Hiba: Nem sikerült betölteni az Ubuntu fontot!')

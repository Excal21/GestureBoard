import cv2
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap, QShortcut, QIcon, QImage, QRegion, QPainterPath
from PySide6.QtCore import QSize, QTimer
from time import sleep
from Resources.Stylesheets.styles import *
from Views.ui_newGestureWizardForm import Ui_Form
from Models.Recorder import Recorder
from Models.RecognizerHandler import RecognizerHandler
from Controllers.BaseController import BaseController

from PySide6.QtCore import QThread, Signal




class NewGestureWizardController(BaseController):


    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.initUI()

        self.setLayoutSettings()
        self.setEventHandlers()

        self.recording_stage = 0
        self.rec = Recorder()

        self.image_count = 0
        self.save = False

        self.timer = None
        self.previous_index = None
        self.ui.btnNameOK.clicked.connect(self.record)

        shortcut = QShortcut(Qt.Key_Space, self)
        shortcut.setContext(Qt.ApplicationShortcut)
    
        shortcut.activated.connect(self.startRecording)

    def startRecording(self):
        self.save = True


    class RecorderThread(QThread):
        finished = Signal()
        def __init__(self, rec, widget):
            super().__init__()
            self.rec = rec
            self.widget = widget

        def run(self):
            self.rec.load(self.widget.data)
            self.rec.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.rec.cap.set(cv2.CAP_PROP_FPS, 60)

    def onReturn(self, index):
        if self.previous_index == 3 and index == 4:
            self.ui.lblGestureInputLabel.show()
            self.ui.btnNameOK.show()
            self.ui.txtinputGestureName.show()
            self.ui.txtinputGestureName.setFocus()
            self.ui.lblInfo.setText("Új gesztus rögzítése")
            self.thread = self.RecorderThread(self.rec, self.stacked_widget.widget(3))
            self.thread.finished.connect(lambda: print("Recorder inicializálva háttérben"))
            self.thread.start()
        print(f'Index changed from {self.previous_index} to {index}')
        self.previous_index = index

#region Record

    def record(self):
        self.timer = QTimer(self)
        
        print('Train meghívva')
        self.gesture_id = max(map(int, self.stacked_widget.widget(3).data.keys())) + 1 if self.stacked_widget.widget(3).data else 0
        if self.recording_stage == 0:
            self.gesture_name = self.ui.txtinputGestureName.text()

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
            self.ui.lblUserGuide.setText('Tartsd a kezed a kívánt gesztus pozíciójában, majd nyomj szőközt a másik kezeddel! A szóköz lenyomása lassan mozgasd a kezed!')
            self.recording_stage = 1
            print('Elindítva!')


    def finishRecording(self):
        self.timer.stop()
        print('Mentve!')
        self.recording_stage = 0
        self.lblImage.setPixmap(QPixmap('Resources/Icons/hand.png').scaled(100, 100, Qt.KeepAspectRatio))
        self.ui.lblUserGuide.setText('')
        self.ui.lblUserGuide.hide()
        
        self.ui.txtinputGestureName.hide()
        self.ui.lblCvImg.hide()
        self.lblImage.show()
        self.ui.lblInfo.setText('Új geszuts rögzítve!')

        gesture_entry = {'gesture' : self.gesture_name, 'action' : None, 'description': None, 'highlight': -1}
        self.rec.release()
        self.stacked_widget.widget(3).data[str(self.gesture_id)] = gesture_entry


        self.ui.btnNameOK.clearFocus()
        self.ui.txtinputGestureName.setText('')
        QTimer.singleShot(1000, lambda: self.stacked_widget.setCurrentIndex(3))
        self.timer = None


#endregion

#region Kamerakép
    def updateFrame(self):
        frame = self.rec.getFrame()
        annotated_frame, gesture = RecognizerHandler.getInstance().annotate(frame)
        if annotated_frame is not None:
            h, w, _ = annotated_frame.shape

            crop_width, crop_height = 500, 300
            resize_width, resize_height = 270, 170

            center_x, center_y = w // 2, h // 2

            x1, x2 = center_x - crop_width // 2, center_x + crop_width // 2
            y1, y2 = center_y - crop_height // 2, center_y + crop_height // 2

            cropped_frame = annotated_frame[y1:y2, x1:x2].copy()  # C-contiguous hiba elkerülése miatt

            resized_frame = cv2.resize(cropped_frame, (resize_width, resize_height), interpolation=cv2.INTER_AREA)

            h, w, ch = resized_frame.shape
            bytes_per_line = ch * w

            if self.save:
                center = (resize_width - 20, 30)
                radius = 10
                color_fill = (0, 0, 220)
                color_outline = (67, 41, 36)
                thickness_outline = 1

                cv2.circle(resized_frame, center, radius, color_fill, -1, lineType=cv2.LINE_AA)
                cv2.circle(resized_frame, center, radius, color_outline, thickness_outline, lineType=cv2.LINE_AA)
       
            q_image = QImage(resized_frame.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()


            path = QPainterPath()
            radius = 10
            path.addRoundedRect(0, 0, self.ui.lblCvImg.width(), self.ui.lblCvImg.height(), radius, radius)
            region = QRegion(path.toFillPolygon().toPolygon())


            self.ui.lblCvImg.setMask(region)
            self.ui.lblCvImg.setPixmap(QPixmap.fromImage(q_image))

            print(self.save)
            if self.save:
                self.rec.save(frame, self.gesture_id)
                if self.rec.saved_images >= 50:
                    self.save = False
                    self.rec.saved_images = 0
                    self.rec.frame_counter = 0
                    print('Kész a rögzítés!')
                    self.finishRecording()


#endregion

#region Eseménykezelők
    def setEventHandlers(self):
        self.ui.btnNameOK.enterEvent = lambda event: self.ui.btnNameOK.setStyleSheet(options_button_hover_style)
        self.ui.btnNameOK.leaveEvent = lambda event: self.ui.btnNameOK.setStyleSheet(options_button_style)

        self.stacked_widget.currentChanged.connect(self.onReturn)


#endregion

#region Layout beállítások
    def setLayoutSettings(self):
        #Felbukkanó új gesztus varázsló elrendezése
        self.ui.frameNewGesture_layout = QVBoxLayout(self.ui.frameNewGesture)
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(self.ui.lblInfo, alignment=Qt.AlignCenter)
        horizontal_layout.addStretch()

        self.ui.frameNewGesture_layout.addLayout(horizontal_layout)
        self.ui.frameNewGesture_layout.setContentsMargins(0, 55, 0, 0)
        self.lblImage = QLabel(self.ui.frameNewGesture)
        self.lblImage.setFixedSize(200, 200)
        self.lblImage.setAlignment(Qt.AlignCenter)
        self.ui.frameNewGesture_layout.addWidget(self.lblImage, alignment=Qt.AlignCenter)
        self.ui.frameNewGesture_layout.addWidget(self.ui.lblCvImg, alignment=Qt.AlignCenter)
        self.lblImage.setPixmap(QPixmap('Resources/Icons/hand.png').scaled(100, 100, Qt.KeepAspectRatio))
        self.ui.lblCvImg.hide()

        #Geszuts neve input mező
        vertical_layout = QHBoxLayout()

        self.ui.txtinputGestureName.setContextMenuPolicy(Qt.NoContextMenu)


        vertical_layout.addWidget(self.ui.lblGestureInputLabel, alignment=Qt.AlignCenter)
        vertical_layout.addWidget(self.ui.txtinputGestureName, alignment=Qt.AlignCenter)
        vertical_layout.addWidget(self.ui.btnNameOK, alignment=Qt.AlignCenter)

        self.ui.btnNameOK.setIcon(QIcon('Resources/Icons/check.png'))
        self.ui.btnNameOK.setIconSize(QSize(30, 30))

        #Középre igazított usert segítő szövegdoboz
        self.ui.lblUserGuide.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.ui.lblUserGuide.setText('')
        self.ui.lblUserGuide.setFixedHeight(240)

        self.ui.frameNewGesture_layout.addWidget(self.ui.lblUserGuide, alignment=Qt.AlignCenter)
        self.ui.frameNewGesture_layout.addStretch()

#endregion
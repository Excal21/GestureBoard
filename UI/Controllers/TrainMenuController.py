import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QApplication
from PySide6.QtGui import QFontDatabase, QFont, QMovie, QPixmap, QShortcut, QIcon
from PySide6.QtCore import QThread, Signal, QSize
from time import sleep
from Resources.Stylesheets.styles import *
from Views.ui_trainOptionsForm import Ui_Form
from Models.Recorder import Recorder
import json
import shutil


class TrainMenuController(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        self.ui = Ui_Form()
        self.ui.setupUi(self)
    
        self.loadFont()

        self.recording_stage = 0
        self.__cap = None
        self.selected_gesture = None
        self.rec = Recorder()



        #Kék alapú díszítősáv elrendezése
        layout = QVBoxLayout(self.ui.frameBlue)
        layout.setContentsMargins(0, 55, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.ui.lblTitle, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.ui.frameBlue.setStyleSheet(sidebar_style)
        self.ui.lblTitle.setStyleSheet(sidebar_title_style)
        
        #Labelek és inputmezők elrendezése
        layout = QVBoxLayout(self.ui.frameButtons)


        server_options_layout = QHBoxLayout() 
        self.ui.lblServer.setStyleSheet(train_label_style)
        self.ui.lblServer.setFont(self.font)
        self.ui.txtinputServer.setStyleSheet(train_input_style)
        self.ui.txtinputServer.setAlignment(Qt.AlignVCenter)
        self.ui.txtinputServer.setFont(self.font)
        self.ui.txtinputServer.setPlaceholderText('127.0.0.1:5000')
        self.ui.txtinputServer.setContextMenuPolicy(Qt.NoContextMenu)

        self.ui.lblDescription.setStyleSheet(description_style)
        self.ui.lblDescription.setFont(self.font)
        self.ui.lblDescription.setText(
        '''<html>
        <style>
                p { line-height: 1.2; }
        </style>
        <body>
                <p align='justify'>
        Add meg a tanítást végző kiszolgáló címét és portját vagy válassz ki egy előre betanított modellt!
                </p>
            </body>
        </html>'''
        )

        self.ui.lblServer.setFixedHeight(30)
        self.ui.txtinputServer.setFixedHeight(30)

        server_options_layout.addWidget(self.ui.lblServer)
        server_options_layout.addWidget(self.ui.txtinputServer)
        
#region Új gesztus varázsló
        #Felbukkanó új gesztus varázsló elrendezése
        self.ui.frameNewGesture.hide()
        self.ui.frameNewGesture_layout = QVBoxLayout(self.ui.frameNewGesture)
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(self.ui.lblInfo, alignment=Qt.AlignCenter)
        horizontal_layout.addStretch()
        self.ui.lblInfo.setStyleSheet(info_label_style)
        self.ui.lblInfo.setFont(self.font)

        self.ui.frameNewGesture_layout.addLayout(horizontal_layout)
        self.ui.frameNewGesture_layout.setContentsMargins(0, 55, 0, 0)
        self.ui.lblImage = QLabel(self.ui.frameNewGesture)
        self.ui.lblImage.setFixedSize(200, 200)
        self.ui.lblImage.setAlignment(Qt.AlignCenter)
        self.ui.frameNewGesture_layout.addWidget(self.ui.lblImage, alignment=Qt.AlignCenter)
        self.ui.lblImage.setPixmap(QPixmap(os.path.join(os.path.dirname(__file__), '..', 'Resources', 'Icons', 'hand.png')).scaled(100, 100, Qt.KeepAspectRatio))


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

        self.ui.btnNameOK.setIcon(QIcon("Resources\\Icons\\check.png"))
        self.ui.btnNameOK.setIconSize(QSize(30, 30))
        self.ui.btnNameOK.enterEvent = lambda event: self.ui.btnNameOK.setStyleSheet(options_button_hover_style)
        self.ui.btnNameOK.leaveEvent = lambda event: self.ui.btnNameOK.setStyleSheet(options_button_style)
        self.ui.btnNameOK.clicked.connect(self.train)

        #Középre igazított usert segítő szövegdoboz
        self.ui.lblUserGuide.setStyleSheet(guide_style)
        self.ui.lblUserGuide.setAlignment(Qt.AlignCenter) 
        self.ui.lblUserGuide.setFont(self.font)
        self.ui.lblUserGuide.setText("")

        self.ui.frameNewGesture_layout.addWidget(self.ui.lblUserGuide, alignment=Qt.AlignCenter)
        self.ui.frameNewGesture_layout.addStretch()


        QShortcut(Qt.Key_Space, self).activated.connect(self.train)
#endregion

#region Gombok
        #Gombok kinézete
        self.ui.btnRecord.setStyleSheet(options_button_style)
        self.ui.btnDelete.setStyleSheet(options_button_style)
        self.ui.btnTrain.setStyleSheet(options_button_style)
        self.ui.btnRecord.setFont(self.font)
        self.ui.btnDelete.setFont(self.font)
        self.ui.btnTrain.setFont(self.font)


        #Gombeventek
        self.ui.btnRecord.enterEvent = lambda event: self.ui.btnRecord.setStyleSheet(options_button_hover_style)
        self.ui.btnRecord.leaveEvent = lambda event: self.ui.btnRecord.setStyleSheet(options_button_style)
        
        self.ui.btnDelete.enterEvent = lambda event: self.ui.btnDelete.setStyleSheet(options_button_hover_style)
        self.ui.btnDelete.leaveEvent = lambda event: self.ui.btnDelete.setStyleSheet(options_button_style)
        self.ui.btnDelete.clicked.connect(self.delete)


        self.ui.btnTrain.enterEvent = lambda event: self.ui.btnTrain.setStyleSheet(options_button_hover_style)
        self.ui.btnTrain.leaveEvent = lambda event: self.ui.btnTrain.setStyleSheet(options_button_style)        
        self.ui.btnTrain.clicked.connect(lambda event: self.openTrainSubWindow())


        #Gesztusok listája
        self.scroll_layout = QVBoxLayout(self.ui.scrollAreaWidgetContents)
        self.ui.lblGestures.setStyleSheet(train_label_style)
        self.ui.lblGestures.setFont(self.font)

        self.ui.scrollArea.setStyleSheet(scrollbar_style)
        self.ui.scrollArea.verticalScrollBar().setContextMenuPolicy(Qt.NoContextMenu)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setSpacing(0)
        self.updateList()


    def showDescription(self, text):
        self.ui.lblDescription.setText(text)

#endregion

#region Record
    def openTrainSubWindow(self):
        self.ui.frameNewGesture.show()
        self.ui.lblUserGuide.hide()
        self.ui.btnNameOK.show()
        self.ui.txtinputGestureName.show()
        self.ui.lblGestureInputLabel.show()
        self.ui.lblDescription.setText("Kövesd a képernyőn megjelenő utasításokat!")
        self.ui.lblGestureInputLabel.setText("Új gesztus neve:")
        self.ui.txtinputGestureName.setPlaceholderText("Gesztus neve")

    def train(self):
        if self.ui.frameNewGesture.isVisible():
            if self.recording_stage == 0:
                self.gesture_name = self.ui.txtinputGestureName.text()
                self.rec.load()
                self.ui.frameNewGesture.show()
                self.ui.lblGestureInputLabel.hide()
                self.ui.txtinputGestureName.hide()
                self.ui.btnNameOK.hide()
                self.ui.lblUserGuide.show()

                self.recording_stage = 1
                self.ui.lblUserGuide.setText("Tartsd a kezed a kívánt gesztus pozíciójában, majd nyomj szőközt a másik kezeddel!")
                print("Elindítva!")

            elif self.recording_stage == 1:
                self.rec.record_batch(self.gesture_name, 0)
                print("Első szakasz rögzítve!")
                self.ui.lblUserGuide.setText("Most picit mozdítsd el ugyanebben a pozícióban a kezed, majd nyomj szőközt a másik kezeddel!")
                self.recording_stage = 2

            elif self.recording_stage == 2:
                self.rec.record_batch(self.gesture_name, 0)
                print("Második szakasz rögzítve!")
                self.rec.save()
                print("Mentve!")
                self.recording_stage = 0
                self.ui.frameNewGesture.hide()
                self.updateList()

#endregion


    def updateList(self):
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        with open('Config\\UserSettings.json', 'r', encoding="UTF-8") as f:
            data = dict(json.load(f))
        for key, value in data.items():
            entry = QPushButton(value['gesture'])
            entry.setStyleSheet(predefined_label_style)
            entry.setFont(self.font)
            entry.setFixedHeight(33)
            
            entry.clicked.connect(lambda event, key=key, entry = entry : self.select(key, entry))
            

            self.scroll_layout.addWidget(entry)

    def select(self, key, label):
        for i in range(self.scroll_layout.count()):
            item = self.scroll_layout.itemAt(i).widget()
            if item != None:
                item.setStyleSheet(predefined_label_style)
        if self.selected_gesture != key:
            self.selected_gesture = key
            label.setStyleSheet(predefined_hover_label_style)
        else:
            label.setStyleSheet(predefined_label_style)
            self.selected_gesture = None
        
    def delete(self):
        def remove_readonly(func, path, _):
            import stat
            os.chmod(path, stat.S_IWRITE)  # Eltávolítja az írásvédettséget
            func(path)

        if self.selected_gesture != None:
            with open('Config\\UserSettings.json', 'r', encoding="UTF-8") as f:
                data = dict(json.load(f))
            data.pop(self.selected_gesture)
            with open('Config\\UserSettings.json', 'w', encoding="UTF-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        shutil.rmtree('Data\\Samples\\' + self.selected_gesture, onerror=remove_readonly)
        self.updateList()
        self.selected_gesture = None

    def loadFont(self):
        font_id = QFontDatabase.addApplicationFont("Resources\\Fonts\\Ubuntu-R.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.font = QFont(font_family, 16)
            self.ui.lblTitle.setFont(self.font)
            self.ui.lblDescription.setFont(self.font)
        else:
            print("Hiba: Nem sikerült betölteni az Ubuntu fontot!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrainMenuController()
    window.show()
    sys.exit(app.exec_())
import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QApplication
from PySide6.QtGui import QFontDatabase, QFont, QMovie
from PySide6.QtCore import QThread, Signal, QSize
from time import sleep
from Resources.Stylesheets.styles import *
from Views.ui_trainOptionsForm import Ui_Form
import json
import shutil


class TrainMenuController(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.loadFont()

        self.selected_gesture = None

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

        shutil.rmtree('Models\\Samples\\' + self.selected_gesture, onerror=remove_readonly)
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
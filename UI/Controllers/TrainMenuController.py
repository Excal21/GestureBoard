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
from Models.Trainer import Trainer
from Controllers.BaseController import BaseController
from Resources.Fonts.FontLoader import FontLoader

class TrainMenuController(BaseController):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget


        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.initUI(overrides={
            'scrollArea': train_scrollBar_style
        })

        self.setLayoutSettings()
        self.setEventHandlers()

        self.recording_stage = 0
        self.__cap = None
        self.selected_gesture = None
        self.rec = Recorder()
        self.data = None
        self.previous_page = 2


        #self.updateList()
#endregion

#region Lista kezelése

    def onReturn(self, index):
        if index == 3 and self.previous_page != 4:
            print(self.previous_page)
            with open('Config/UserSettings.json', 'r', encoding='UTF-8') as f:
                self.data = dict(json.load(f))
            
            print('USerSettings JSON betöltve a TrainMenuController-be')
            self.updateList()

        elif index == 3:
            self.updateList()

    def updateList(self):

        print('Lista frissítése...')
        
        #print('listaadat: ', self.data)
        if self.data is not None:
            while self.scroll_layout.count():
                child = self.scroll_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            if len(self.data) > 0:
                for key, value in self.data.items():
                    entry = QPushButton(value['gesture'])
                    entry.setStyleSheet(predefined_label_style + noborder)
                    entry.setFont(FontLoader.getFont())
                    entry.setFixedHeight(33)
                    
                    entry.clicked.connect(lambda event, key=key, entry = entry : self.select(key, entry))
                    

                    self.scroll_layout.addWidget(entry)

    def select(self, key, label):
        for i in range(self.scroll_layout.count()):
            item = self.scroll_layout.itemAt(i).widget()
            if item != None:
                item.setStyleSheet(predefined_label_style + noborder)
        if self.selected_gesture != key:
            self.selected_gesture = key
            label.setStyleSheet(predefined_hover_label_style)
        else:
            label.setStyleSheet(predefined_label_style + noborder)
            self.selected_gesture = None
        
    def delete(self):
        if self.selected_gesture != None:
            self.data.pop(self.selected_gesture)

        self.updateList()
        self.selected_gesture = None

    def save(self):
        def remove_readonly(func, path, _):
            import stat
            os.chmod(path, stat.S_IWRITE)  # Eltávolítja az írásvédettséget
            func(path)


        print('Mentés előtti adat', self.data)
        with open('Config/UserSettings.json', 'w', encoding='UTF-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        print('JSON dumped')

        for key in os.listdir('Data/Samples'):
            if key not in self.data.keys():
                shutil.rmtree('Data/Samples/' + key, onerror=remove_readonly)

    def startRecord(self):
        self.previous_page = 4
        self.stacked_widget.setCurrentIndex(4)

    def back(self):
        self.previous_page = 2
        self.stacked_widget.setCurrentIndex(2)

#endregion

#region Tanítás kezelése
    def startTraining(self):
        def remove_readonly(func, path, _):
            import stat
            os.chmod(path, stat.S_IWRITE)  # Eltávolítja az írásvédettséget
            func(path)


        for key in os.listdir('Data/Samples'):
            if key not in self.data.keys():
                shutil.rmtree('Data/Samples/' + key, onerror=remove_readonly)
        

        loading_page = self.stacked_widget.widget(0)
        info_widget = loading_page.findChild(QLabel, 'lblLoading')

        info_widget.setText('Várakozás a kiszolgálóra...')
        self.stacked_widget.setCurrentIndex(0)


                
        self.trainer = Trainer()
        self.trainer.ip = self.ui.txtinputServer.text().strip() if self.ui.txtinputServer.text() != '' else '127.0.0.1:5000'
        self.trainer.finished.connect(self.finishTraining)
        self.trainer.progress.connect(lambda text: info_widget.setText(text))
        self.trainer.start()
        

    def finishTraining(self):
        print('sikeres tanítás')
        if self.trainer.trained:
            self.save()
            self.updateList()
            self.previous_page = 2
            self.stacked_widget.setCurrentIndex(2)
        else:
            self.stacked_widget.setCurrentIndex(3)
            

#endregion

#region Eseménykezelők
    def setEventHandlers(self):
        self.stacked_widget.currentChanged.connect(self.onReturn)

        self.ui.btnBack.clicked.connect(self.back)
        self.ui.btnBack.enterEvent = lambda event: self.ui.btnBack.setStyleSheet(options_button_hover_style)
        self.ui.btnBack.leaveEvent = lambda event: self.ui.btnBack.setStyleSheet(options_button_style)

        



        #Gombeventek
        self.ui.btnRecord.enterEvent = lambda event: self.ui.btnRecord.setStyleSheet(options_button_hover_style)
        self.ui.btnRecord.leaveEvent = lambda event: self.ui.btnRecord.setStyleSheet(options_button_style)
        self.ui.btnRecord.clicked.connect(self.startRecord)
        
        self.ui.btnDelete.enterEvent = lambda event: self.ui.btnDelete.setStyleSheet(options_button_hover_style)
        self.ui.btnDelete.leaveEvent = lambda event: self.ui.btnDelete.setStyleSheet(options_button_style)
        self.ui.btnDelete.clicked.connect(self.delete)


        self.ui.btnTrain.enterEvent = lambda event: self.ui.btnTrain.setStyleSheet(options_button_hover_style)
        self.ui.btnTrain.leaveEvent = lambda event: self.ui.btnTrain.setStyleSheet(options_button_style)        
        self.ui.btnTrain.clicked.connect(lambda event: self.startTraining())


#endregion


#region Stílusállítók
    def setLayoutSettings(self):
         #Labelek és inputmezők elrendezése


        server_options_layout = QHBoxLayout() 
        self.ui.txtinputServer.setAlignment(Qt.AlignVCenter)
        self.ui.txtinputServer.setPlaceholderText('127.0.0.1:5000')
        self.ui.txtinputServer.setContextMenuPolicy(Qt.NoContextMenu)
        self.ui.lblDescription.setText(
            self.textToHTML('Add meg a tanítást végző kiszolgáló címét és portját, majd rögzítsd és tanítsd meg saját gesztusaidat!')
        )

        self.ui.lblServer.setFixedHeight(30)
        self.ui.txtinputServer.setFixedHeight(30)



        server_options_layout.addWidget(self.ui.lblServer)
        server_options_layout.addWidget(self.ui.txtinputServer)
        self.scroll_layout = QVBoxLayout(self.ui.scrollAreaWidgetContents)
        self.ui.scrollArea.verticalScrollBar().setContextMenuPolicy(Qt.NoContextMenu)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setSpacing(0)
#endregion
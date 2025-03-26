import os
import sys
import json
from time import sleep


from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMenu
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFontDatabase, QFont, QIcon, QKeyEvent, QKeySequence
from PySide6.QtWidgets import QApplication, QStackedWidget
from Resources.Stylesheets.styles import *
from Views.ui_optionsForm import Ui_OptionsForm


class OptionsMenuController(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.stacked_widget = stacked_widget
        self.ui = Ui_OptionsForm()

        self.ui.setupUi(self)

        self.font = None
        self.setStyles()
        self.setLayoutSettings()
        self.setEventHandlers()


        self.sub_menu_active = False
        self.keycapture_active = False
        self.command_input_active = False
        self.key_command = ''

        self.data = None

        self.loadConfig()


#region Válaszhatók menüje
    def updateEntries(self):
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for key, entry in self.data.items():

            gesture_entry = QWidget()
            gesture_entry_layout = QHBoxLayout(gesture_entry)
            gesture_entry_layout.setSpacing(0) #Távolság a gomb és a hosszabb címke közt
            gesture_entry.setFixedHeight(70)

            label = QLabel(entry['gesture'])
            label.setStyleSheet(entry_label_style)
            label.setFont(self.font)

            btnCombo = QPushButton()
            btnKey = QPushButton()
            btnConsole = QPushButton()                

            #Gombok ikonjainak beállítása
            btnCombo.setIcon(QIcon('Resources\\Icons\\widget.png'))
            btnCombo.setIconSize(QSize(40, 40))

            btnConsole.setIcon(QIcon('Resources\\Icons\\console.png'))
            btnConsole.setIconSize(QSize(50, 45))

            btnKey.setIcon(QIcon('Resources\\Icons\\keyboard.png'))
            btnKey.setIconSize(QSize(60, 60))


            if(entry['highlight'] == 0):
                btnCombo.setIcon(QIcon('Resources\\Icons\\widget_green.png'))
            elif(entry['highlight'] == 1):
                btnKey.setIcon(QIcon('Resources\\Icons\\keyboard_green.png'))
            elif(entry['highlight'] == 2):
                btnConsole.setIcon(QIcon('Resources\\Icons\\console_green.png'))

            #Gombok helyének beállítása
            btnContainer = QWidget()
            btnContainer_layout = QHBoxLayout(btnContainer)
            btnContainer_layout.setSpacing(10)
            btnContainer_layout.addWidget(btnCombo)
            btnContainer_layout.addWidget(btnKey)
            btnContainer_layout.addWidget(btnConsole)

            #Gombeventek
            btnCombo.enterEvent = lambda event, entry = entry: self.showDescription(entry, 0)
            btnCombo.leaveEvent = lambda event: self.ui.lblDescription.setText('')

            btnKey.enterEvent = lambda event, entry = entry: self.showDescription(entry, 1)
            btnKey.leaveEvent = lambda event: self.ui.lblDescription.setText('')

            btnConsole.enterEvent = lambda event, entry = entry: self.showDescription(entry, 2)
            btnConsole.leaveEvent = lambda event: self.ui.lblDescription.setText('')

            btnCombo.clicked.connect(lambda event, key=key: self.showSubSelection(key))
            btnKey.clicked.connect(lambda event, key=key: self.startKeyCapture(key))
            btnConsole.clicked.connect(lambda event, key=key: self.showCommandInput(key))

            gesture_entry_layout.addWidget(label)
            gesture_entry_layout.addWidget(btnContainer)

            self.scroll_layout.addWidget(gesture_entry)
        
        self.scroll_layout.addStretch()


#endregion

#region Előtanított műveletek
    def showSubSelection(self, JSONkey):
        self.keycapture_active = False
        self.command_input_active = False
        self.hideEverything()
        if self.sub_menu_active == False:
            self.sub_menu_active = True
            self.clicked = JSONkey
            print(self.clicked)
            self.ui.scrollArea.setDisabled(False)
            self.ui.scrollCombo.show()
        else:
            self.sub_menu_active = False
            self.ui.scrollCombo.hide()
            self.ui.scrollArea.setDisabled(False)


    def loadComboMenu(self):
        self.ui.scrollCombo.setParent(self.ui.frameButtons)
        combo_layout = QVBoxLayout(self.ui.scrollComboWidgetContents)
        combo_layout.setSpacing(10)

        with open('Config\\PredefinedActionMap.json', 'r', encoding='utf-8') as file:
            predefined_actions_data = dict(json.load(file))

        for predefined_action in predefined_actions_data.items():
            combo_entry = QPushButton(predefined_action[0])
            combo_entry.setFixedHeight(30)
            combo_entry.setStyleSheet(predefined_label_style)
            combo_entry.setFont(self.font)
            
            combo_entry.enterEvent = lambda event, entry=combo_entry: entry.setStyleSheet(predefined_hover_label_style)
            combo_entry.leaveEvent = lambda event, entry=combo_entry: entry.setStyleSheet(predefined_label_style)
            combo_entry.clicked.connect(lambda event, predefined_action = predefined_action: self.saveSubSelection(predefined_action))

            combo_layout.addWidget(combo_entry)

        combo_layout.setContentsMargins(0, 30, 0, 30)
        combo_layout.addStretch()


    def saveSubSelection(self, predefined_action):
        self.data[self.clicked]['action'] = predefined_action[1]
        self.data[self.clicked]['highlight'] = 0
        self.data[self.clicked]['description'] = predefined_action[0]
        self.ui.scrollCombo.hide()
        self.ui.scrollArea.setDisabled(False)
        self.sub_menu_active = False
        self.updateEntries()
        
#endregion

#region Billentyűszimuláció
    def startKeyCapture(self, JSONkey):
        self.command_input_active = False
        self.hideEverything()
        if self.keycapture_active:
            self.keycapture_active = False
            self.ui.frameHide.hide()
        else:
            self.keycapture_active = True
            self.clicked = JSONkey
            self.ui.frameHide.show()
            self.setFocus()
            self.ui.lblUserGuide.setText('Billentyűkombináció')

    def keyPressEvent(self, event: QKeyEvent):
        if self.keycapture_active:
            modifiers = []
            if event.modifiers() & Qt.ControlModifier:
                modifiers.append('ctrl')
            if event.modifiers() & Qt.AltModifier:
                modifiers.append('alt')
            if event.modifiers() & Qt.ShiftModifier:
                modifiers.append('shift')
            key = event.nativeVirtualKey()

            key_map = {
                222: 'Á',
                226: 'Í',
                186: 'É',
                187: 'Ó',
                192: 'Ö',
                219: 'Ő',
                221: 'Ú',
                191: 'Ü',
                220: 'Ű'
            }

            keystr = ''
            
            if modifiers:
                combination = ' , '.join(modifiers)
            else:
                combination = keystr

            if self.keycapture_active:
                print(self.key_command)

            valid = False

            if key in key_map:
                keystr = key_map[key]
                valid = True
            elif 32 <= key <= 126:
                valid = True
                keystr = chr(key)
            
            self.ui.lblUserGuide.setText(f'Billentyűkombináció\n {combination.replace(',', '+') + (' + ' if combination else '') + keystr}')
            
            if valid:
                key_command = 'pyautogui.hotkey('
                for modifier in modifiers:
                    key_command += f'\'{modifier}\', '

                key_command += f'\'{keystr.lower()}\')'

                self.data[self.clicked]['action'] = key_command
                self.data[self.clicked]['description'] = f'{combination.replace(',', '+') + (' + ' if combination else '') + keystr}'
                self.data[self.clicked]['highlight'] = 1

                print(f'Billentyűkombináció\n {combination.replace(',', '+') + (' + ' if combination else '') + keystr}')
                self.ui.lblUserGuide.setText(f'Billentyűkombináció\n {combination.replace(',', '+') + (' + ' if combination else '') + keystr}')
                QApplication.processEvents()
                sleep(0.5)
                self.ui.frameHide.hide()
                self.keycapture_active = False
                self.updateEntries()

    def keyReleaseEvent(self, event):
        if self.keycapture_active:
            self.ui.lblUserGuide.setText('Billentyűkombináció')


#region Parancs megadása
    def showCommandInput(self, key):
        self.hideEverything()
        self.keycapture_active = False
        if self.command_input_active:
            self.command_input_active = False
            self.ui.frameHide.hide()
        else:
            self.command_input_active = True
            self.clicked = key
            self.ui.frameHide.show()
            self.ui.txtinputCommand.show()
            self.ui.btnCommandOk.show()
            self.ui.txtinputCommand.setFocus()
            self.ui.lblUserGuide.setText('Parancs megadása')

    def saveCommand(self):
        action = f'os.system(\'{self.ui.txtinputCommand.text()}\')'
        self.data[self.clicked]['action'] = action
        self.data[self.clicked]['highlight'] = 2
        self.data[self.clicked]['description'] = self.ui.txtinputCommand.text()
        self.ui.txtinputCommand.clear()
        self.ui.txtinputCommand.hide()
        self.ui.btnCommandOk.hide()
        self.ui.frameHide.hide()
        self.command_input_active = False
        self.updateEntries()
#endregion

#region Mentés, reset, stb.
    def loadConfig(self):
        config_path = ('Config\\UserSettings.json')
        with open(config_path, 'r', encoding='utf-8') as file:
            self.data = dict(json.load(file))
        print('UserSettings JSON betöltve')

    def saveMappings(self):
        with open('Config\\UserSettings.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
        print('Beállítások mentve')
        

        self.hideEverything()
        self.sub_menu_active = False
        self.keycapture_active = False
        self.stacked_widget.setCurrentIndex(1)

    
    def resetMappings(self):
        for gesture in self.data.keys():
            self.data[gesture]['action'] = None
            self.data[gesture]['highlight'] = -1
            self.data[gesture]['description'] = None

        self.updateEntries()


    def showDescription(self, entry, hoveridx):
        if entry['highlight'] == hoveridx:
            self.ui.lblDescription.setText(entry['description'])
        else:
            if hoveridx == 0:
                self.ui.lblDescription.setText('Előre definiált művelet')
            elif hoveridx == 1:
                self.ui.lblDescription.setText('Billentyűkombináció')
            elif hoveridx == 2:
                self.ui.lblDescription.setText('Parancs')

    def showOptions(self):
        self.stacked_widget.setCurrentIndex(1)

    def hideEverything(self):
        self.ui.scrollCombo.hide()
        self.ui.frameHide.hide()
        self.ui.txtinputCommand.hide()
        self.ui.btnCommandOk.hide()

    def onReturn(self, index):
        if index == 2:
            self.loadConfig()
            self.updateEntries()

#region Eseménykezelők
    def setEventHandlers(self):
        self.stacked_widget.currentChanged.connect(self.onReturn)

        self.ui.btnTeach.clicked.connect(lambda event: self.stacked_widget.setCurrentIndex(3))
        self.ui.btnTeach.enterEvent = lambda event: self.ui.btnTeach.setStyleSheet(options_button_hover_style)
        self.ui.btnTeach.leaveEvent = lambda event: self.ui.btnTeach.setStyleSheet(options_button_style)

        self.ui.btnSave.clicked.connect(lambda: self.saveMappings())
        self.ui.btnSave.enterEvent = lambda event: self.ui.btnSave.setStyleSheet(options_button_hover_style)
        self.ui.btnSave.leaveEvent = lambda event: self.ui.btnSave.setStyleSheet(options_button_style)

        self.ui.btnReset.clicked.connect(lambda: self.resetMappings())
        self.ui.btnReset.enterEvent = lambda event: self.ui.btnReset.setStyleSheet(options_button_hover_style)
        self.ui.btnReset.leaveEvent = lambda event: self.ui.btnReset.setStyleSheet(options_button_style)

        self.ui.btnCommandOk.clicked.connect(lambda: self.saveCommand())
        self.ui.btnCommandOk.enterEvent = lambda event: self.ui.btnCommandOk.setStyleSheet(options_button_hover_style)
        self.ui.btnCommandOk.leaveEvent = lambda event: self.ui.btnCommandOk.setStyleSheet(options_button_style)

#endregion


#region Stílusállítók
    def setStyles(self):
        self.setFonts()
        self.ui.frameBlue.setStyleSheet(sidebar_style)
        self.ui.lblTitle.setStyleSheet(sidebar_title_style)
        self.ui.lblDescription.setStyleSheet(description_style)
        self.ui.scrollArea.verticalScrollBar().setStyleSheet(scrollbar_style)
        self.ui.btnReset.setStyleSheet(options_button_style)
        self.ui.btnSave.setStyleSheet(options_button_style)
        self.ui.btnTeach.setStyleSheet(options_button_style)
        self.ui.scrollCombo.setStyleSheet(scrollbar_style)
        self.ui.lblUserGuide.setStyleSheet(train_label_style)
        self.ui.txtinputCommand.setStyleSheet(train_input_style)
        self.ui.btnCommandOk.setStyleSheet(options_button_style)



    def setFonts(self):
        self.loadFont()
        self.ui.btnReset.setFont(self.font)
        self.ui.btnSave.setFont(self.font)
        self.ui.btnTeach.setFont(self.font)
        self.ui.lblUserGuide.setFont(self.font)
        self.ui.txtinputCommand.setFont(self.font)


    def setLayoutSettings(self):
        #Kék alapú díszítősáv elrendezése
        layout = QVBoxLayout(self.ui.frameBlue)
        layout.setContentsMargins(0, 55, 0, 0)
        layout.setSpacing(20)
        layout.addWidget(self.ui.lblTitle, alignment=Qt.AlignCenter)
        layout.addWidget(self.ui.lblDescription, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.ui.lblDescription.setText('')

        #Görgethető terület
        self.scroll_area = self.ui.scrollArea
        self.scroll_area.setWidgetResizable(True)
        self.scroll_layout = QVBoxLayout(self.ui.scrollAreaWidgetContents)
        self.scroll_area.setWidget(self.ui.scrollAreaWidgetContents)

        self.ui.scrollArea.verticalScrollBar().setContextMenuPolicy(Qt.NoContextMenu)
        self.ui.scrollArea.horizontalScrollBar().setContextMenuPolicy(Qt.NoContextMenu)
        self.clicked = None


        #Előre definiált beállítások menüje
        self.ui.scrollCombo.hide()

        self.ui.scrollCombo.verticalScrollBar().setContextMenuPolicy(Qt.NoContextMenu)
        self.ui.scrollCombo.horizontalScrollBar().setContextMenuPolicy(Qt.NoContextMenu)
        self.predefined_clicked = None

        self.ui.scrollCombo.setParent(self.ui.frameButtons)
        self.loadComboMenu()
        self.ui.scrollCombo.hide()

        #Keylog
        self.ui.btnCommandOk.hide()
        self.ui.txtinputCommand.hide()
        self.ui.frameHide.hide()
        self.ui.lblUserGuide.setAlignment(Qt.AlignHCenter)


        self.ui.btnCommandOk.setText('')
        self.ui.btnCommandOk.setIcon(QIcon('Resources\\Icons\\check.png'))
        self.ui.btnCommandOk.setIconSize(QSize(30, 30))

        self.ui.lblDescription.setContentsMargins(15, 0, 15, 0)


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

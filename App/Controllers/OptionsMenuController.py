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
from Controllers.BaseController import BaseController
from Resources.Fonts.FontLoader import FontLoader

class OptionsMenuController(BaseController):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.stacked_widget = stacked_widget
        self.ui = Ui_OptionsForm()

        self.ui.setupUi(self)
        self.initUI()

        self.setLayoutSettings()
        self.setEventHandlers()


        self.sub_menu_active = False
        self.keycapture_active = False
        self.command_input_active = False
        self.key_command = ''

        self.data = None

        #self.loadConfig()


#region Válaszhatók menüje
    def updateEntries(self):
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for key, entry in self.data.items():

            gesture_entry = QWidget()
            gesture_entry_layout = QHBoxLayout(gesture_entry)
            gesture_entry_layout.setSpacing(0)
            gesture_entry.setFixedHeight(70)

            label = QLabel(entry['gesture'])
            label.setStyleSheet(entry_label_style)
            label.setFont(FontLoader.getFont())

            btnCombo = QPushButton()
            btnKey = QPushButton()
            btnConsole = QPushButton()                


            btnCombo.setIcon(QIcon('Resources/Icons/widget.png'))
            btnCombo.setIconSize(QSize(40, 40))

            btnKey.setIcon(QIcon('Resources/Icons/keyboard.png'))
            btnKey.setIconSize(QSize(60, 60))

            btnConsole.setIcon(QIcon('Resources/Icons/console.png'))
            btnConsole.setIconSize(QSize(50, 45))
            #Windows világos téma miatt
            btnCombo.setStyleSheet(noborder)
            btnKey.setStyleSheet(noborder)
            btnConsole.setStyleSheet(noborder)

            if(entry['highlight'] == 0):
                btnCombo.setIcon(QIcon('Resources/Icons/widget_green.png'))
                btnCombo.setContextMenuPolicy(Qt.CustomContextMenu)
                btnCombo.customContextMenuRequested.connect(lambda event, key=key: self.resetEntry(key))
            elif(entry['highlight'] == 1):
                btnKey.setIcon(QIcon('Resources/Icons/keyboard_green.png'))
                btnKey.setContextMenuPolicy(Qt.CustomContextMenu)
                btnKey.customContextMenuRequested.connect(lambda event, key=key: self.resetEntry(key))
            elif(entry['highlight'] == 2):
                btnConsole.setIcon(QIcon('Resources/Icons/console_green.png'))
                btnConsole.setContextMenuPolicy(Qt.CustomContextMenu)
                btnConsole.customContextMenuRequested.connect(lambda event, key=key: self.resetEntry(key))

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

    def resetEntry(self, key):
        print('Resetting entry for key:', key)
        self.data[key]['action'] = None
        self.data[key]['highlight'] = -1
        self.data[key]['description'] = None
        self.updateEntries()

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

        with open('Config/PredefinedActionMap.json', 'r', encoding='utf-8') as file:
            predefined_actions_data = dict(json.load(file))

        for predefined_action in predefined_actions_data.items():
            combo_entry = QPushButton(predefined_action[0])
            combo_entry.setFixedHeight(30)
            combo_entry.setFixedWidth(220)
            combo_entry.setStyleSheet(predefined_label_style)
            combo_entry.setFont(FontLoader.getFont())
            
            combo_entry.enterEvent = lambda event, entry=combo_entry: entry.setStyleSheet(predefined_hover_label_style)
            combo_entry.leaveEvent = lambda event, entry=combo_entry: entry.setStyleSheet(predefined_label_style)
            combo_entry.clicked.connect(lambda event, predefined_action = predefined_action: self.saveSubSelection(predefined_action))

            combo_layout.addWidget(combo_entry)

        combo_layout.setContentsMargins(0, 30, 0, 30)
        combo_layout.addStretch()


    def saveSubSelection(self, predefined_action):
        self.data[self.clicked]['action'] = predefined_action[1]
        self.data[self.clicked]['highlight'] = 0
        self.data[self.clicked]['description'] = predefined_action[0] + '\n\n\nTörléshez kattints\njobb gombbal!'
        self.ui.scrollCombo.hide()
        self.ui.scrollArea.setDisabled(False)
        self.sub_menu_active = False
        self.updateEntries()
        
#endregion

#region Billentyűszimuláció
    def startKeyCapture(self, JSONkey):
        self.command_input_active = False
        self.sub_menu_active = False
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
            key = event.key()
            print(key)
            key_map = {
                Qt.Key_Aacute: 'Á',
                Qt.Key_Iacute: 'Í',
                Qt.Key_Eacute: 'É',
                Qt.Key_Oacute: 'Ó',
                Qt.Key_Odiaeresis: 'Ö',
                336: 'Ő',
                Qt.Key_Uacute: 'Ú',
                Qt.Key_Udiaeresis: 'Ü',
                368: 'Ű',
                Qt.Key_Return: 'enter',
                Qt.Key_Enter: 'enter',
                Qt.Key_PageDown: 'pagedown',
                Qt.Key_PageUp: 'pageup',
                Qt.Key_Home: 'home',
                Qt.Key_End: 'end',
                Qt.Key_Insert: 'insert',
                Qt.Key_Delete: 'delete',
                Qt.Key_Left: ['balra', 'left'],
                Qt.Key_Up: ['fel', 'up'],
                Qt.Key_Right: ['jobbra', 'right'],
                Qt.Key_Down: ['le', 'down']
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
                if len(key_map[key]) == 2:
                    print('keymap: ', key_map[key])
                    keystr = key_map[key][1]
                    valid = True
                else:
                    keystr = key_map[key]
                    valid = True
                
            elif 32 <= key <= 126:
                valid = True
                if keystr == ' ':
                    keystr = 'space'
                else:
                    keystr = chr(key)
            
            print('Keystring: ', keystr)
            self.ui.lblUserGuide.setText(f'Billentyűkombináció\n {combination.replace(',', '+') + (' + ' if combination else '') + keystr}')
            
            if valid:
                key_command = 'pyautogui.hotkey('
                for modifier in modifiers:
                    key_command += f'\'{modifier}\', '

                print('Keystr: ', keystr)
                key_command += f'\'{keystr.lower()}\')'

                self.data[self.clicked]['action'] = key_command
                #A ternary alkalmazza az aliast, ahol lehet
                self.data[self.clicked]['description'] = f'{combination.replace(',', '+')
                                                            + (' + ' if combination else '') 
                                                            + (key_map[key][0] if (key in key_map and len(key_map[key]) == 2) else keystr)}'
                self.data[self.clicked]['description'] += '\n\n\nTörléshez kattints\njobb gombbal!'
                self.data[self.clicked]['highlight'] = 1

                print(f'Billentyűkombináció\n {combination.replace(',', '+') + (' + ' if combination else '') + keystr}')
                # self.ui.lblUserGuide.setText(f'Billentyűkombináció\n {combination.replace(',', '+') + (' + ' if combination else '') + keystr}')
                self.ui.lblUserGuide.setText(f'Billentyűkombináció\n {self.data[self.clicked]["description"]}')
                QApplication.processEvents()
                sleep(0.5)
                self.ui.frameHide.hide()
                self.keycapture_active = False
                self.updateEntries()

    # def keyReleaseEvent(self, event):   <== lol ezt minek raktam ide
    #     if self.keycapture_active:
    #         self.ui.lblUserGuide.setText('Billentyűkombináció')


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
        self.data[self.clicked]['description'] = self.ui.txtinputCommand.text() + '\n\n\nTörléshez kattints\njobb gombbal!'
        self.ui.txtinputCommand.clear()
        self.ui.txtinputCommand.hide()
        self.ui.btnCommandOk.hide()
        self.ui.frameHide.hide()
        self.command_input_active = False
        self.updateEntries()
#endregion

#region Mentés, reset, stb.
    def loadConfig(self):
        config_path = ('Config/UserSettings.json')
        with open(config_path, 'r', encoding='utf-8') as file:
            self.data = dict(json.load(file))
        print('UserSettings JSON betöltve az OptionsMenuController-be')

    def saveMappings(self):
        with open('Config/UserSettings.json', 'w', encoding='utf-8') as file:
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

        self.ui.btnManager.clicked.connect(lambda event: self.stacked_widget.setCurrentIndex(3))
        self.ui.btnManager.enterEvent = lambda event: self.ui.btnManager.setStyleSheet(options_button_hover_style)
        self.ui.btnManager.leaveEvent = lambda event: self.ui.btnManager.setStyleSheet(options_button_style)

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


#region Layout beállítások

    def setLayoutSettings(self):
        self.ui.lblDescription.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.ui.lblDescription.setFixedHeight(150)
        self.setContentsMargins(15, 0, 15, 0)

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
        self.ui.scrollCombo.verticalScrollBar().setContentsMargins(0, 20, 0, 0)
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
        self.ui.btnCommandOk.setIcon(QIcon('Resources/Icons/check.png'))
        self.ui.btnCommandOk.setIconSize(QSize(30, 30))



#endregion
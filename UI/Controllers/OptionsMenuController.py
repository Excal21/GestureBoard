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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Views')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Config')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Resources', 'Stylesheets')))

class OptionsMenuController(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.stacked_widget = stacked_widget
        self.stacked_widget.currentChanged.connect(self.load_entries)


        self.ui = Ui_OptionsForm()
        self.ui.setupUi(self)

        self.font = None
        self.loadFont()
        self.setFonts()
        self.setStyles()
        self.setEventHandlers()


        self.sub_menu_active = False

        self.keycapture_active = False
        self.key_command = ''

        self.mappings_to_save = {}

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

        self.load_entries()
        self.ui.scrollCombo.setParent(self.ui.frameButtons)
        self.loadComboMenu()
        self.ui.scrollCombo.hide()

        #Keylog
        self.ui.frameHide.hide()
        self.ui.lblUserGuide.setAlignment(Qt.AlignHCenter)

#region JSON betöltés

    def load_entries(self):
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Config', 'UserSettings.json'))
        with open(config_path, 'r', encoding='utf-8') as file:
            data = dict(json.load(file))


        print('UserSettings JSON loaded')
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for key, entry in data.items():

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

            #Gombok helyének beállítása
            btnContainer = QWidget()
            btnContainer_layout = QHBoxLayout(btnContainer)
            btnContainer_layout.setSpacing(10)
            btnContainer_layout.addWidget(btnCombo)
            btnContainer_layout.addWidget(btnKey)
            btnContainer_layout.addWidget(btnConsole)

            #Gombeventek
            btnCombo.enterEvent = lambda event: self.showDescription('Előre definiált műveletek')
            btnCombo.leaveEvent = lambda event: self.showDescription('')


            btnKey.enterEvent = lambda event: self.showDescription('Billentyűszimuláció')
            btnKey.leaveEvent = lambda event: self.showDescription('')

            btnConsole.enterEvent = lambda event: self.showDescription('Parancssor')
            btnConsole.leaveEvent = lambda event: self.showDescription('')

            btnCombo.clicked.connect(lambda event, key=key: self.showSubSelection(key))
            btnKey.clicked.connect(lambda event, key=key: self.startKeyCapture(key))

            gesture_entry_layout.addWidget(label)
            gesture_entry_layout.addWidget(btnContainer)

            self.scroll_layout.addWidget(gesture_entry)
        
        self.scroll_layout.addStretch()

#endregion

#region Előtanított műveletek
    def showSubSelection(self, JSONkey):
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
            data = dict(json.load(file))

        for gesture, action in data.items():
            combo_entry = QPushButton(gesture)
            combo_entry.setFixedHeight(30)
            combo_entry.setStyleSheet(predefined_label_style)
            combo_entry.setFont(self.font)
            
            combo_entry.enterEvent = lambda event, entry=combo_entry: entry.setStyleSheet(predefined_hover_label_style)
            combo_entry.leaveEvent = lambda event, entry=combo_entry: entry.setStyleSheet(predefined_label_style)
            combo_entry.clicked.connect(lambda event, action=action: self.saveSubSelection(action))

            combo_layout.addWidget(combo_entry)

        combo_layout.setContentsMargins(0, 30, 0, 30)
        combo_layout.addStretch()


    def saveSubSelection(self, action):
        self.predefined_clicked = action
        self.mappings_to_save[self.clicked] = self.predefined_clicked
        self.ui.scrollCombo.hide()
        self.ui.scrollArea.setDisabled(False)
#endregion

#region Billentyűszimuláció
    def startKeyCapture(self, JSONkey):
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

            self.mappings_to_save[self.clicked] = key_command
            print(f'Billentyűkombináció\n {combination.replace(',', '+') + (' + ' if combination else '') + keystr}')
            self.ui.lblUserGuide.setText(f'Billentyűkombináció\n {combination.replace(',', '+') + (' + ' if combination else '') + keystr}')
            QApplication.processEvents()
            sleep(0.5)
            self.ui.frameHide.hide()
            self.keycapture_active = False
            

    def keyReleaseEvent(self, event):
        if self.keycapture_active:
            self.ui.lblUserGuide.setText('Billentyűkombináció')





#region Mentés, reset, stb.

    def saveMappings(self):
        with open('Config\\UserSettings.json', 'r', encoding='utf-8') as file:
            data = dict(json.load(file))
        
        for gesture, action in self.mappings_to_save.items():
            data[gesture]['action'] = action

        with open('Config\\UserSettings.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print('Settings saved')
        

        self.hideEverything()
        self.sub_menu_active = False
        self.keycapture_active = False
        self.stacked_widget.setCurrentIndex(1)

    
    def resetMappings(self):
        with open('Config\\UserSettings.json', 'r', encoding='utf-8') as file:
            data = dict(json.load(file))
        
        for gesture in data.keys():
            data[gesture]['action'] = None

        with open('Config\\UserSettings.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print('Settings reset')
        
        self.stacked_widget.setCurrentIndex(1)


    def showDescription(self, text):
        self.ui.lblDescription.setText(text)

    def showOptions(self):
        self.stacked_widget.setCurrentIndex(1)

    def hideEverything(self):
        self.ui.scrollCombo.hide()
        self.ui.frameHide.hide()

#region Eseménykezelők
    def setEventHandlers(self):
        self.ui.btnTeach.clicked.connect(lambda event: self.stacked_widget.setCurrentIndex(3))
        self.ui.btnTeach.enterEvent = lambda event: self.ui.btnTeach.setStyleSheet(options_button_hover_style)
        self.ui.btnTeach.leaveEvent = lambda event: self.ui.btnTeach.setStyleSheet(options_button_style)

        self.ui.btnSave.clicked.connect(lambda: self.saveMappings())
        self.ui.btnSave.enterEvent = lambda event: self.ui.btnSave.setStyleSheet(options_button_hover_style)
        self.ui.btnSave.leaveEvent = lambda event: self.ui.btnSave.setStyleSheet(options_button_style)

        self.ui.btnReset.clicked.connect(lambda: self.resetMappings())
        self.ui.btnReset.enterEvent = lambda event: self.ui.btnReset.setStyleSheet(options_button_hover_style)
        self.ui.btnReset.leaveEvent = lambda event: self.ui.btnReset.setStyleSheet(options_button_style)


#endregion


#region Stílusállítók
    def setStyles(self):
        self.ui.frameBlue.setStyleSheet(sidebar_style)
        self.ui.lblTitle.setStyleSheet(sidebar_title_style)
        self.ui.lblDescription.setStyleSheet(description_style)
        self.ui.scrollArea.verticalScrollBar().setStyleSheet(scrollbar_style)
        self.ui.btnReset.setStyleSheet(options_button_style)
        self.ui.btnSave.setStyleSheet(options_button_style)
        self.ui.btnTeach.setStyleSheet(options_button_style)
        self.ui.scrollCombo.setStyleSheet(scrollbar_style)
        self.ui.lblUserGuide.setStyleSheet(train_label_style)



    def setFonts(self):
        self.ui.btnReset.setFont(self.font)
        self.ui.btnSave.setFont(self.font)
        self.ui.btnTeach.setFont(self.font)
        self.ui.lblUserGuide.setFont(self.font)


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

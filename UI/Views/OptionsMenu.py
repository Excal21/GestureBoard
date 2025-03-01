import os
import sys

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMenu
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFontDatabase, QFont, QIcon
from PySide6.QtWidgets import QApplication, QStackedWidget
from styles import *
from Forms.ui_optionsForm import Ui_OptionsForm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Forms")))

class OptionsMenu(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.stacked_widget = stacked_widget

        self.ui = Ui_OptionsForm()
        self.ui.setupUi(self)

        self.font = None
        self.load_font()


        #Kék alapú díszítősáv elrendezése
        layout = QVBoxLayout(self.ui.frameBlue)
        layout.setContentsMargins(0, 55, 0, 0)
        layout.setSpacing(20)
        layout.addWidget(self.ui.lblTitle, alignment=Qt.AlignCenter)
        layout.addWidget(self.ui.lblDescription, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.ui.frameBlue.setStyleSheet(sidebar_style)
        self.ui.lblTitle.setStyleSheet(sidebar_title_style)
        self.ui.lblDescription.setStyleSheet(description_style)
        self.ui.lblDescription.setText("")

        #Görgethető terület
        self.scroll_area = self.ui.scrollArea
        self.scroll_area.setWidgetResizable(True)
        self.scroll_layout = QVBoxLayout(self.ui.scrollAreaWidgetContents)
        self.scroll_area.setWidget(self.ui.scrollAreaWidgetContents)
        self.scroll_area.verticalScrollBar().setStyleSheet(scrollbar_style)
        self.ui.scrollArea.verticalScrollBar().setContextMenuPolicy(Qt.NoContextMenu)
        self.ui.scrollArea.horizontalScrollBar().setContextMenuPolicy(Qt.NoContextMenu)
        self.clicked = None

        #Gombok
        self.ui.btnReset.setFont(self.font)
        self.ui.btnSave.setFont(self.font)
        self.ui.btnReset.setStyleSheet(options_button_style)
        self.ui.btnSave.setStyleSheet(options_button_style)

        self.ui.btnSave.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.ui.btnSave.enterEvent = lambda event: self.ui.btnSave.setStyleSheet(options_button_hover_style)
        self.ui.btnSave.leaveEvent = lambda event: self.ui.btnSave.setStyleSheet(options_button_style)

        self.ui.btnReset.enterEvent = lambda event: self.ui.btnReset.setStyleSheet(options_button_hover_style)
        self.ui.btnReset.leaveEvent = lambda event: self.ui.btnReset.setStyleSheet(options_button_style)

        #Előre definiált beállítások menüje
        self.ui.scrollCombo.hide()
        self.ui.scrollCombo.setStyleSheet(scrollbar_style)
        self.ui.scrollCombo.verticalScrollBar().setContextMenuPolicy(Qt.NoContextMenu)
        self.ui.scrollCombo.horizontalScrollBar().setContextMenuPolicy(Qt.NoContextMenu)
        self.predefined_clicked = None

        self.load_entries()
        self.ui.scrollCombo.setParent(self.ui.frameButtons)
        self.loadComboMenu()
        self.ui.scrollCombo.hide()

    def load_entries(self):
        with open("Labels.txt", "r", encoding="utf-8") as file:
            for line in file:
                gesture_entry = QWidget()
                gesture_entry_layout = QHBoxLayout(gesture_entry)
                gesture_entry_layout.setSpacing(0) #Távolság a gomb és a hosszabb címke közt
                gesture_entry.setFixedHeight(70)

                label = QLabel(line.strip())
                label.setStyleSheet(entry_label_style)
                label.setFont(self.font)

                btnCombo = QPushButton()
                btnKey = QPushButton()
                btnConsole = QPushButton()                

                #Gombok ikonjainak beállítása
                btnCombo.setIcon(QIcon("Icons\\widget.png"))
                btnCombo.setIconSize(QSize(40, 40))

                btnConsole.setIcon(QIcon("Icons\\console.png"))
                btnConsole.setIconSize(QSize(50, 45))

                btnKey.setIcon(QIcon("Icons\\keyboard.png"))
                btnKey.setIconSize(QSize(60, 60))

                #Gombok helyének beállítása
                btnContainer = QWidget()
                btnContainer_layout = QHBoxLayout(btnContainer)
                btnContainer_layout.setSpacing(10)
                btnContainer_layout.addWidget(btnCombo)
                btnContainer_layout.addWidget(btnKey)
                btnContainer_layout.addWidget(btnConsole)

                #Gombeventek
                btnCombo.enterEvent = lambda event: self.show_description("Előre definiált műveletek")
                btnCombo.leaveEvent = lambda event: self.show_description("")


                btnKey.enterEvent = lambda event: self.show_description("Billentyűszimuláció")
                btnKey.leaveEvent = lambda event: self.show_description("")

                btnConsole.enterEvent = lambda event: self.show_description("Parancssor")
                btnConsole.leaveEvent = lambda event: self.show_description("")

                btnCombo.clicked.connect(lambda checked, label = label: self.showSubSelection(label))

                gesture_entry_layout.addWidget(label)
                gesture_entry_layout.addWidget(btnContainer)

                self.scroll_layout.addWidget(gesture_entry)

    def loadComboMenu(self):
        self.ui.scrollCombo.setParent(self.ui.frameButtons)
        combo_layout = QVBoxLayout(self.ui.scrollComboWidgetContents)
        

        with open("ComboSettings.txt", "r", encoding="utf-8") as file:
            for line in file:
                #print(line)
                combo_entry = QPushButton(line.strip())
                combo_entry.setFixedHeight(30)
                combo_entry.setStyleSheet(predefined_label_style)
                combo_entry.setFont(self.font)
                
                combo_entry.enterEvent = lambda event, entry=combo_entry: entry.setStyleSheet(predefined_hover_label_style)
                combo_entry.leaveEvent = lambda event, entry=combo_entry: entry.setStyleSheet(predefined_label_style)
                combo_entry.clicked.connect(lambda checked, text=combo_entry.text(): self.saveSubSelection(text))

                combo_layout.addWidget(combo_entry)

    def showSubSelection(self, text):
        self.clicked = text.text()
        print(self.clicked)
        self.ui.scrollArea.setDisabled(True)
        self.ui.scrollCombo.show()


    def saveSubSelection(self, text):
        self.predefined_clicked = text
        print(self.predefined_clicked)
        self.ui.scrollCombo.hide()
        self.ui.scrollArea.setDisabled(False)

    def show_description(self, text):
        self.ui.lblDescription.setText(text)

    def show_options(self):
        self.stacked_widget.setCurrentIndex(1)

    def load_font(self):
        font_id = QFontDatabase.addApplicationFont("Ubuntu-R.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.font = QFont(font_family, 16)
            self.ui.lblTitle.setFont(self.font)
            self.ui.lblDescription.setFont(self.font)
        else:
            print("Hiba: Nem sikerült betölteni az Ubuntu fontot!")

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFontDatabase, QFont, QIcon
from ui_optionsForm import Ui_OptionsForm
from PySide6.QtWidgets import QApplication, QStackedWidget
from styles import *

class OptionsMenu(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.ui = Ui_OptionsForm()
        self.ui.setupUi(self)

        self.font = None

        font_id = QFontDatabase.addApplicationFont("Ubuntu-R.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.font = QFont(font_family, 16)
            self.ui.lblTitle.setFont(self.font)
            self.ui.lblDescription.setFont(self.font)
        else:
            print("Hiba: Nem sikerült betölteni az Ubuntu fontot!")


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


        self.scroll_area = self.ui.scrollArea
        self.scroll_area.setWidgetResizable(True)
        self.scroll_layout = QVBoxLayout(self.ui.scrollAreaWidgetContents)
        self.scroll_area.setWidget(self.ui.scrollAreaWidgetContents)
        self.scroll_area.verticalScrollBar().setStyleSheet(scrollbar_style)


        self.ui.btnReset.setFont(self.font)
        self.ui.btnSave.setFont(self.font)
        self.ui.btnReset.setStyleSheet(options_button_style)
        self.ui.btnSave.setStyleSheet(options_button_style)



        self.load_entries()
    
    def load_entries(self):
        with open("Labels.txt", "r", encoding="utf-8") as file:
            for line in file:
                print(line)
                
                gesture_entry = QWidget()
                gesture_entry_layout = QHBoxLayout(gesture_entry)
                gesture_entry_layout.setSpacing(10) #Távolság a gomb és a hosszabb címke közt
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


                gesture_entry_layout.addWidget(label)
                gesture_entry_layout.addWidget(btnContainer)

                self.scroll_layout.addWidget(gesture_entry)

    def show_description(self, text):
        self.ui.lblDescription.setText(text)

    def show_options(self):
        self.stacked_widget.setCurrentIndex(1)

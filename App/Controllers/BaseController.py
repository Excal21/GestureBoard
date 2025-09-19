from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from Resources.Fonts.FontLoader import FontLoader
from Resources.Stylesheets.styles import *
from PySide6.QtWidgets import QVBoxLayout

class BaseController(QWidget):
    def __init__(self):
        super().__init__()

    def initUI(self, overrides=None):
        self.setFonts()
        self.setStyles(overrides)
        self.setBasicLayout()

    def setFonts(self):
        for attr_name in dir(self.ui):
            widget = getattr(self.ui, attr_name)
            if hasattr(widget, 'setFont'):
                widget.setFont(FontLoader.getFont())

    def setStyles(self, overrides=None):
        prefix_styles = {
            'lbl': train_label_style,
            'btn': options_button_style,
            'txt': train_input_style,
            'spin': train_input_style,
            'combo': camera_combo_style,
            'slider': slider_style,
            'scroll': scrollbar_style,
        }

        # Speciális
        special_styles = {
            'frameBlue': sidebar_style,
            'lblTitle': sidebar_title_style,
            'lblDescription': description_style,
            'lblCvImg': camera_label_style,
            'lblInfo': info_label_style,
            'lblLoading': info_label_style,
            'lblGestureInputLabel': train_label_style,
        }

        if overrides:
            special_styles.update(overrides)

        for attr_name in dir(self.ui):
            widget = getattr(self.ui, attr_name, None)
            if widget and callable(getattr(widget, 'setStyleSheet', None)):
                if attr_name in special_styles:
                    widget.setStyleSheet(special_styles[attr_name])
                else:
                    for prefix, style in prefix_styles.items():
                        if attr_name.startswith(prefix) and not attr_name in special_styles:
                            widget.setStyleSheet(style)
                            break

        for attr_name in dir(self.ui):
            widget = getattr(self.ui, attr_name, None)
            if widget and hasattr(widget, 'setContextMenuPolicy'):
                widget.setContextMenuPolicy(Qt.NoContextMenu)


    def setBasicLayout(self):
        layout = QVBoxLayout(self.ui.frameBlue)
        layout.setContentsMargins(0, 55, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.ui.lblTitle, alignment=Qt.AlignCenter)
        layout.addStretch()

        if hasattr(self.ui, 'lblDescription'):
            self.ui.lblDescription.setText('')
            self.ui.lblDescription.setAlignment(Qt.AlignCenter)



    def textToHTML(self, text):
        return '''<html>
            <style>
                p { line-height: 1.2;
                    font-size: 12pt;
                    color: white; }
            </style>
            <body>
                <p align='justify'>'''+ text +'''</p>
                </body>
            </html>'''
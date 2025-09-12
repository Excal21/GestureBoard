sidebar_title_style = '''
            color: white;
            font-size: 26pt;
'''

sidebar_style = '''
            background-color: rgb(36 , 41 , 67)
'''

button_style = '''
            background-color: white;
            color:  black;
            border: 1px solid rgb(70, 70, 70);
            border-radius: 10px;
            font-size: 20pt;
'''

button_hover_style = button_style + '''
            background-color: lightgray;
'''

entry_button_style = button_style

options_button_style = button_style + '''
            border-radius: 7px;
            font-size: 14pt;
'''

options_button_hover_style = options_button_style + '''
            background-color: lightgray;

'''
options_button_active_style = options_button_style + '''
            background-color: rgb(0, 172, 201);
'''


entry_label_style = '''
            color: rgb(36, 41, 67);
            font-size: 20pt;
            margin: 0px;
'''

predefined_label_style = '''
            color: black;
            font-size: 14pt;
            text-align: left;
            border: none;
'''

predefined_hover_label_style = '''
            color: black;
            font-size: 14pt;
            border: 1px solid rgb(70, 70, 70);
            background-color: lightgray;
            border-radius: 5px;
            text-align: left;
            padding-left: 2px;
'''

gesture_entry_style = '''
            border: 1px solid black;
'''

description_style = '''
            color: white;
            font-size: 14pt;
'''

guide_style = '''
            color: rgb(36, 41, 67);
            font-size: 12pt;
'''

long_desciption_style = '''
            color: white;
            font-size: 12pt;
'''

info_label_style = '''
            color: rgb(36, 41, 67);
            font-size: 24pt;
            '''


scrollbar_style ='''
        QScrollBar:vertical {
            border: none;
            background: rgb(212, 212, 212);
            width: 10px;
            border-radius: 5px;
            margin-top: 10px;
            margin-bottom: 10px;
        }

        QScrollBar::handle:vertical {
            background: rgb(36, 41, 67);
            height: 20px;
            border-radius: 5px;
            border: none;
            background-clip: border-box;
        }

        QScrollBar::handle:vertical:hover {
            background: rgb(0, 172, 201)
        }

        /* Nyilak eltüntetése */
        QScrollBar::sub-line:vertical,
        QScrollBar::add-line:vertical {
            background: none;
            height: 0px;
            border: none;
        }

        /* Görgetősáv végeinek lekerekítése */
        QScrollBar::sub-page:vertical,
        QScrollBar::add-page:vertical {
            border-radius: 5px;
        }
'''

train_scrollBar_style = '''
        QScrollBar:vertical {
            border: none;
            background: rgb(212, 212, 212);
            width: 10px;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical {
            background: rgb(36, 41, 67);
            height: 20px;
            border-radius: 5px;
            border: none;
            background-clip: border-box;
        }

        QScrollBar::handle:vertical:hover {
            background: rgb(0, 172, 201)
        }

        /* Nyilak eltüntetése */
        QScrollBar::sub-line:vertical,
        QScrollBar::add-line:vertical {
            background: none;
            height: 0px;
            border: none;
        }

        /* Görgetősáv végeinek lekerekítése */
        QScrollBar::sub-page:vertical,
        QScrollBar::add-page:vertical {
            border-radius: 5px;
        }

        #scrollArea {
            border: 1px solid rgb(70, 70, 70);
            background: white;
            border-radius: 7px;
        }
        
        #scrollAreaWidgetContents {
            border: none;
            background: transparent;
            border-radius: 7px;
        }
'''

train_label_style = '''
            color: rgb(36, 41, 67);
            font-size: 16pt;
'''

train_input_style = '''
            color: rgb(36, 41, 67);
            font-size: 14pt;
            border: 1px solid rgb(70, 70, 70);
            border-radius: 5px;
            padding-left: 5px;
'''

disabled_style = '''
            background: lightgray;
            color: rgb(100, 100, 100);
'''

train_input_disabled_style = train_input_style + disabled_style

slider_style = '''
        QSlider::groove:horizontal {
            background: lightgray;
            height: 7px;
            border-radius: 3px;
        }

        QSlider::groove:horizontal:hover {
            background: rgb(0, 172, 201);
        }

        QSlider::sub-page:horizontal {
            background: rgb(36 , 41 , 67);
            border-radius: 3px;
        }

        QSlider::handle:horizontal {
            background: white;
            width: 12px;
            height: 12px;
            border-radius: 6px;
            border: 2px solid rgb(70, 70, 70);
            margin: -5px 0; /* Ez mindenképp kell, különben négyzetes lesz a csúszka!!! */
        }

        QSlider::handle:horizontal:hover {
            background: lightgray;
            width: 12px;
            height: 12px;
            border-radius: 5px;
        }
'''

camera_label_style = '''
            background-color: white;
            border-radius: 10px;
'''

camera_combo_style = '''
        QComboBox {
            color: rgb(36, 41, 67);
            font-size: 14pt;
            border: 1px solid rgb(70, 70, 70);
            border-radius: 5px;
            padding-left: 5px;
        }
        QComboBox::drop-down {
            border: 1px solid rgb(70, 70, 70);
            background: transparent;
        }
        QComboBox QAbstractItemView {
            background: white;
            color: rgb(36, 41, 67);
            border: 1px solid rgb(70, 70, 70);
            border-radius: 5px;
        }
        QComboBox::drop-down {
            border: none;
            background: transparent;
        }
        QComboBox::down-arrow {
            width: 0px;
        }
'''

noborder='''
            border: none;
            background: transparent;
'''

checkbox_style = '''
    QCheckBox::indicator {
        width: 47px;
        height: 27px;
    }
    QCheckBox::indicator:unchecked {
        border: 1px solid rgb(70, 70, 70);
        border-radius: 5px;
        background: white;
    }
    QCheckBox::indicator:checked {
        border: 1px solid rgb(70, 70, 70);
        border-radius: 5px;
        background: white;
        image: url(Resources/Icons/check.png);
    }
'''
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from button_QSS import *
from label_QSS import *
from scrollBar_QSS import *



sidebar_style = '''
            background-color: rgb(36 , 41 , 67)
'''

gesture_entry_style = '''
            border: 1px solid black;
'''

description_style = '''
            color: white;
            font-size: 14pt;
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
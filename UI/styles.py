sidebar_title_style = """
            color: white;
            font-size: 26pt;
"""

sidebar_style = """
            background-color: rgb(36 , 41 , 67)
"""

button_style = """
            background-color: white;
            color:  black;
            border: 1px solid rgb(70, 70, 70);
            border-radius: 10px;
            font-size: 20pt;
"""

button_hover_style = """
            color:  black;
            border: 1px solid rgb(70, 70, 70);
            background-color: lightgray;
            border-radius: 10px;
            font-size: 20pt;
"""

entry_button_style = """
            background-color: white;
            color:  black;
            border: 1px solid rgb(70, 70, 70);
            border-radius: 10px;
            font-size: 20pt;
"""

options_button_hover_style = """
            color:  black;
            border: 1px solid rgb(70, 70, 70);
            background-color: lightgray;
            border-radius: 10px;
            font-size: 14pt;
"""

options_button_style = """
            background-color: white;
            color:  black;
            border: 1px solid rgb(70, 70, 70);
            border-radius: 5px;
            font-size: 14pt;
"""

entry_label_style = """
            color: black;
            font-size: 20pt;
            margin: 0px;
"""

predefined_label_style = """
            color: black;
            font-size: 14pt;
            text-align: left;
"""

predefined_hover_label_style = """
            color: black;
            font-size: 14pt;
            border: 1px solid rgb(70, 70, 70);
            background-color: lightgray;
            border-radius: 5px;
            text-align: left;
            padding-left: 7px;
"""

gesture_entry_style = """
            border: 1px solid black;
"""

description_style = """
            color: white;
            font-size: 14pt;
"""

scrollbar_style ="""
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
"""

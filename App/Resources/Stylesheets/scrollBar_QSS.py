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
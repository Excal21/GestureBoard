# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QPushButton,
    QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 410)
        self.frameBlue = QFrame(MainWindow)
        self.frameBlue.setObjectName(u"frameBlue")
        self.frameBlue.setGeometry(QRect(0, 0, 280, 410))
        self.frameBlue.setStyleSheet(u"background-color: rgb(36 , 41 , 67)")
        self.frameBlue.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameBlue.setFrameShadow(QFrame.Shadow.Raised)
        self.lblTitle = QLabel(self.frameBlue)
        self.lblTitle.setObjectName(u"lblTitle")
        self.lblTitle.setGeometry(QRect(10, 20, 240, 50))
        self.lblTitle.setStyleSheet(u"color: white;\n"
"font-size: 26pt;\n"
"")
        self.btnStart = QPushButton(MainWindow)
        self.btnStart.setObjectName(u"btnStart")
        self.btnStart.setGeometry(QRect(330, 30, 420, 80))
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setPointSize(20)
        self.btnStart.setFont(font)
        self.btnStart.setStyleSheet(u"background-color: white;\n"
"color:  black;\n"
"border: 1px solid rgb(70, 70, 70);\n"
"border-radius: 10px;\n"
"font-size: 20pt;\n"
"")
        self.btnOptions = QPushButton(MainWindow)
        self.btnOptions.setObjectName(u"btnOptions")
        self.btnOptions.setGeometry(QRect(330, 150, 420, 80))
        self.btnOptions.setFont(font)
        self.btnOptions.setStyleSheet(u"background-color: white;\n"
"color:  black;\n"
"border: 1px solid  rgb(70, 70, 70);;\n"
"border-radius: 10px;\n"
"font-size: 20pt;\n"
"")
        self.frameButtons = QFrame(MainWindow)
        self.frameButtons.setObjectName(u"frameButtons")
        self.frameButtons.setGeometry(QRect(280, 0, 520, 410))
        self.frameButtons.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameButtons.setFrameShadow(QFrame.Shadow.Raised)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"GestureBoard", None))
        self.lblTitle.setText(QCoreApplication.translate("MainWindow", u"GestureBoard", None))
        self.btnStart.setText(QCoreApplication.translate("MainWindow", u"Gesztusvez\u00e9rl\u00e9s elind\u00edt\u00e1sa", None))
        self.btnOptions.setText(QCoreApplication.translate("MainWindow", u"Be\u00e1ll\u00edt\u00e1sok", None))
    # retranslateUi


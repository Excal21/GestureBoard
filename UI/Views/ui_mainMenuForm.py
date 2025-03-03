# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainMenuForm.ui'
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
        self.frameBlue.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameBlue.setFrameShadow(QFrame.Shadow.Raised)
        self.lblTitle = QLabel(self.frameBlue)
        self.lblTitle.setObjectName(u"lblTitle")
        self.lblTitle.setGeometry(QRect(10, 20, 240, 50))
        self.frameButtons = QFrame(MainWindow)
        self.frameButtons.setObjectName(u"frameButtons")
        self.frameButtons.setGeometry(QRect(280, 0, 520, 410))
        self.frameButtons.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameButtons.setFrameShadow(QFrame.Shadow.Raised)
        self.btnCameraOptions = QPushButton(self.frameButtons)
        self.btnCameraOptions.setObjectName(u"btnCameraOptions")
        self.btnCameraOptions.setGeometry(QRect(50, 250, 420, 80))
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setPointSize(20)
        self.btnCameraOptions.setFont(font)
        self.btnCameraOptions.setStyleSheet(u"")
        self.btnOptions = QPushButton(self.frameButtons)
        self.btnOptions.setObjectName(u"btnOptions")
        self.btnOptions.setGeometry(QRect(50, 140, 420, 80))
        self.btnOptions.setFont(font)
        self.btnOptions.setStyleSheet(u"")
        self.btnStart = QPushButton(self.frameButtons)
        self.btnStart.setObjectName(u"btnStart")
        self.btnStart.setGeometry(QRect(50, 30, 420, 80))
        self.btnStart.setFont(font)
        self.btnStart.setStyleSheet(u"")
        self.frameButtons.raise_()
        self.frameBlue.raise_()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"GestureBoard", None))
        self.lblTitle.setText(QCoreApplication.translate("MainWindow", u"GestureBoard", None))
        self.btnCameraOptions.setText(QCoreApplication.translate("MainWindow", u"Kamerabe\u00e1ll\u00edt\u00e1sok", None))
        self.btnOptions.setText(QCoreApplication.translate("MainWindow", u"Be\u00e1ll\u00edt\u00e1sok", None))
        self.btnStart.setText(QCoreApplication.translate("MainWindow", u"Gesztusvez\u00e9rl\u00e9s elind\u00edt\u00e1sa", None))
    # retranslateUi


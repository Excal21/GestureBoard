# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'trainOptionsForm.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QLineEdit,
    QPushButton, QScrollArea, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 410)
        self.frameBlue = QFrame(Form)
        self.frameBlue.setObjectName(u"frameBlue")
        self.frameBlue.setGeometry(QRect(0, 0, 280, 410))
        self.frameBlue.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameBlue.setFrameShadow(QFrame.Shadow.Raised)
        self.lblTitle = QLabel(self.frameBlue)
        self.lblTitle.setObjectName(u"lblTitle")
        self.lblTitle.setGeometry(QRect(0, 20, 240, 50))
        self.lblDescription = QLabel(self.frameBlue)
        self.lblDescription.setObjectName(u"lblDescription")
        self.lblDescription.setGeometry(QRect(20, 90, 231, 241))
        self.lblDescription.setWordWrap(True)
        self.frameButtons = QFrame(Form)
        self.frameButtons.setObjectName(u"frameButtons")
        self.frameButtons.setGeometry(QRect(280, 0, 520, 410))
        self.frameButtons.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameButtons.setFrameShadow(QFrame.Shadow.Raised)
        self.lblServer = QLabel(self.frameButtons)
        self.lblServer.setObjectName(u"lblServer")
        self.lblServer.setGeometry(QRect(40, 30, 161, 20))
        self.txtinputServer = QLineEdit(self.frameButtons)
        self.txtinputServer.setObjectName(u"txtinputServer")
        self.txtinputServer.setGeometry(QRect(220, 30, 271, 21))
        self.btnRecord = QPushButton(self.frameButtons)
        self.btnRecord.setObjectName(u"btnRecord")
        self.btnRecord.setGeometry(QRect(30, 130, 171, 41))
        self.btnTrain = QPushButton(self.frameButtons)
        self.btnTrain.setObjectName(u"btnTrain")
        self.btnTrain.setGeometry(QRect(30, 270, 171, 41))
        self.btnDelete = QPushButton(self.frameButtons)
        self.btnDelete.setObjectName(u"btnDelete")
        self.btnDelete.setGeometry(QRect(30, 200, 171, 41))
        self.scrollArea = QScrollArea(self.frameButtons)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(223, 130, 271, 181))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 269, 179))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.lblGestures = QLabel(self.frameButtons)
        self.lblGestures.setObjectName(u"lblGestures")
        self.lblGestures.setGeometry(QRect(230, 90, 251, 41))
        self.lblServer.raise_()
        self.txtinputServer.raise_()
        self.btnRecord.raise_()
        self.btnTrain.raise_()
        self.btnDelete.raise_()
        self.lblGestures.raise_()
        self.scrollArea.raise_()
        self.btnBack = QPushButton(Form)
        self.btnBack.setObjectName(u"btnBack")
        self.btnBack.setGeometry(QRect(520, 340, 120, 40))
        self.btnSave = QPushButton(Form)
        self.btnSave.setObjectName(u"btnSave")
        self.btnSave.setGeometry(QRect(650, 340, 120, 40))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lblTitle.setText(QCoreApplication.translate("Form", u"GestureBoard", None))
        self.lblDescription.setText(QCoreApplication.translate("Form", u"Le\u00edr\u00e1s", None))
        self.lblServer.setText(QCoreApplication.translate("Form", u"Kiszolg\u00e1l\u00f3 c\u00edme", None))
        self.btnRecord.setText(QCoreApplication.translate("Form", u"Gesztus felv\u00e9tele", None))
        self.btnTrain.setText(QCoreApplication.translate("Form", u"Gesztusok tan\u00edt\u00e1sa", None))
        self.btnDelete.setText(QCoreApplication.translate("Form", u"Gesztus t\u00f6rl\u00e9se", None))
        self.lblGestures.setText(QCoreApplication.translate("Form", u"Gesztusok:", None))
        self.btnBack.setText(QCoreApplication.translate("Form", u"Vissza", None))
        self.btnSave.setText(QCoreApplication.translate("Form", u"Ment\u00e9s", None))
    # retranslateUi


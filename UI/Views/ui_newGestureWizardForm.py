# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'newGestureWizardForm.ui'
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
    QPushButton, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 410)
        self.frameNewGesture = QFrame(Form)
        self.frameNewGesture.setObjectName(u"frameNewGesture")
        self.frameNewGesture.setGeometry(QRect(280, 0, 521, 411))
        self.frameNewGesture.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameNewGesture.setFrameShadow(QFrame.Shadow.Raised)
        self.lblInfo = QLabel(self.frameNewGesture)
        self.lblInfo.setObjectName(u"lblInfo")
        self.lblInfo.setGeometry(QRect(140, 40, 261, 16))
        self.lblUserGuide = QLabel(self.frameNewGesture)
        self.lblUserGuide.setObjectName(u"lblUserGuide")
        self.lblUserGuide.setGeometry(QRect(0, 240, 521, 171))
        self.lblUserGuide.setWordWrap(True)
        self.lblGestureInputLabel = QLabel(self.frameNewGesture)
        self.lblGestureInputLabel.setObjectName(u"lblGestureInputLabel")
        self.lblGestureInputLabel.setGeometry(QRect(40, 320, 161, 31))
        self.txtinputGestureName = QLineEdit(self.frameNewGesture)
        self.txtinputGestureName.setObjectName(u"txtinputGestureName")
        self.txtinputGestureName.setGeometry(QRect(210, 320, 231, 31))
        self.btnNameOK = QPushButton(self.frameNewGesture)
        self.btnNameOK.setObjectName(u"btnNameOK")
        self.btnNameOK.setGeometry(QRect(450, 320, 31, 31))
        self.lblCvImg = QLabel(self.frameNewGesture)
        self.lblCvImg.setObjectName(u"lblCvImg")
        self.lblCvImg.setGeometry(QRect(60, 100, 391, 201))
        self.lblGestureInputLabel.raise_()
        self.txtinputGestureName.raise_()
        self.btnNameOK.raise_()
        self.lblCvImg.raise_()
        self.lblUserGuide.raise_()
        self.lblInfo.raise_()
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

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lblInfo.setText(QCoreApplication.translate("Form", u"\u00daj gesztus felv\u00e9tele", None))
        self.lblUserGuide.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.lblGestureInputLabel.setText(QCoreApplication.translate("Form", u"Gesztus neve:", None))
        self.btnNameOK.setText("")
        self.lblCvImg.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.lblTitle.setText(QCoreApplication.translate("Form", u"GestureBoard", None))
        self.lblDescription.setText(QCoreApplication.translate("Form", u"Le\u00edr\u00e1s", None))
    # retranslateUi


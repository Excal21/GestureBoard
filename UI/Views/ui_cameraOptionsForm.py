# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cameraOptionsForm.ui'
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
    QPushButton, QSizePolicy, QSlider, QWidget)

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
        self.lblCamera = QLabel(self.frameButtons)
        self.lblCamera.setObjectName(u"lblCamera")
        self.lblCamera.setGeometry(QRect(40, 40, 161, 30))
        self.txtInputCamera = QLineEdit(self.frameButtons)
        self.txtInputCamera.setObjectName(u"txtInputCamera")
        self.txtInputCamera.setGeometry(QRect(220, 40, 271, 30))
        self.btnStartCam = QPushButton(self.frameButtons)
        self.btnStartCam.setObjectName(u"btnStartCam")
        self.btnStartCam.setGeometry(QRect(30, 270, 171, 41))
        self.btnBack = QPushButton(self.frameButtons)
        self.btnBack.setObjectName(u"btnBack")
        self.btnBack.setGeometry(QRect(360, 340, 120, 40))
        self.sliderHue = QSlider(self.frameButtons)
        self.sliderHue.setObjectName(u"sliderHue")
        self.sliderHue.setGeometry(QRect(220, 95, 271, 31))
        self.sliderHue.setOrientation(Qt.Orientation.Horizontal)
        self.lblHue = QLabel(self.frameButtons)
        self.lblHue.setObjectName(u"lblHue")
        self.lblHue.setGeometry(QRect(40, 90, 161, 30))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lblTitle.setText(QCoreApplication.translate("Form", u"GestureBoard", None))
        self.lblDescription.setText(QCoreApplication.translate("Form", u"Le\u00edr\u00e1s", None))
        self.lblCamera.setText(QCoreApplication.translate("Form", u"Kamera:", None))
        self.btnStartCam.setText(QCoreApplication.translate("Form", u"Kamerateszt", None))
        self.btnBack.setText(QCoreApplication.translate("Form", u"Vissza", None))
        self.lblHue.setText(QCoreApplication.translate("Form", u"Hue eltol\u00e1s", None))
    # retranslateUi


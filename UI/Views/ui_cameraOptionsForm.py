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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDoubleSpinBox,
    QFrame, QLabel, QPushButton, QSizePolicy,
    QSlider, QSpinBox, QWidget)

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
        self.lblDescription.setGeometry(QRect(20, 270, 231, 121))
        self.lblDescription.setWordWrap(True)
        self.lblCvImg = QLabel(self.frameBlue)
        self.lblCvImg.setObjectName(u"lblCvImg")
        self.lblCvImg.setGeometry(QRect(20, 110, 241, 141))
        self.frameButtons = QFrame(Form)
        self.frameButtons.setObjectName(u"frameButtons")
        self.frameButtons.setGeometry(QRect(280, 0, 520, 410))
        self.frameButtons.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameButtons.setFrameShadow(QFrame.Shadow.Raised)
        self.lblCamera = QLabel(self.frameButtons)
        self.lblCamera.setObjectName(u"lblCamera")
        self.lblCamera.setGeometry(QRect(40, 40, 161, 30))
        self.btnStartCam = QPushButton(self.frameButtons)
        self.btnStartCam.setObjectName(u"btnStartCam")
        self.btnStartCam.setGeometry(QRect(40, 140, 171, 41))
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
        self.lblFrameCnt = QLabel(self.frameButtons)
        self.lblFrameCnt.setObjectName(u"lblFrameCnt")
        self.lblFrameCnt.setGeometry(QRect(40, 250, 301, 30))
        self.lblDelay = QLabel(self.frameButtons)
        self.lblDelay.setObjectName(u"lblDelay")
        self.lblDelay.setGeometry(QRect(40, 290, 341, 30))
        self.lblConfidence = QLabel(self.frameButtons)
        self.lblConfidence.setObjectName(u"lblConfidence")
        self.lblConfidence.setGeometry(QRect(40, 210, 191, 30))
        self.spinConfidence = QSpinBox(self.frameButtons)
        self.spinConfidence.setObjectName(u"spinConfidence")
        self.spinConfidence.setGeometry(QRect(420, 210, 60, 31))
        self.spinConfidence.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinFrameCnt = QSpinBox(self.frameButtons)
        self.spinFrameCnt.setObjectName(u"spinFrameCnt")
        self.spinFrameCnt.setGeometry(QRect(420, 250, 60, 31))
        self.spinFrameCnt.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinDelay = QDoubleSpinBox(self.frameButtons)
        self.spinDelay.setObjectName(u"spinDelay")
        self.spinDelay.setGeometry(QRect(420, 290, 60, 25))
        self.spinDelay.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.btnSave = QPushButton(self.frameButtons)
        self.btnSave.setObjectName(u"btnSave")
        self.btnSave.setGeometry(QRect(230, 340, 120, 40))
        self.comboCamera = QComboBox(self.frameButtons)
        self.comboCamera.setObjectName(u"comboCamera")
        self.comboCamera.setGeometry(QRect(301, 40, 181, 31))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lblTitle.setText(QCoreApplication.translate("Form", u"GestureBoard", None))
        self.lblDescription.setText(QCoreApplication.translate("Form", u"Le\u00edr\u00e1s", None))
        self.lblCvImg.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.lblCamera.setText(QCoreApplication.translate("Form", u"Kamera", None))
        self.btnStartCam.setText(QCoreApplication.translate("Form", u"Kamerateszt", None))
        self.btnBack.setText(QCoreApplication.translate("Form", u"Vissza", None))
        self.lblHue.setText(QCoreApplication.translate("Form", u"Sz\u00edneltol\u00e1s", None))
        self.lblFrameCnt.setText(QCoreApplication.translate("Form", u"K\u00e9pkocka gesztusonk\u00e9nt", None))
        self.lblDelay.setText(QCoreApplication.translate("Form", u"Sz\u00fcnet gesztusok k\u00f6z\u00f6tt", None))
        self.lblConfidence.setText(QCoreApplication.translate("Form", u"Magabiztoss\u00e1g", None))
        self.btnSave.setText(QCoreApplication.translate("Form", u"Ment\u00e9s", None))
    # retranslateUi


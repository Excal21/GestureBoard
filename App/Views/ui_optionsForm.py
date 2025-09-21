# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'optionsForm.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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

class Ui_OptionsForm(object):
    def setupUi(self, OptionsForm):
        if not OptionsForm.objectName():
            OptionsForm.setObjectName(u"OptionsForm")
        OptionsForm.resize(800, 410)
        self.frameBlue = QFrame(OptionsForm)
        self.frameBlue.setObjectName(u"frameBlue")
        self.frameBlue.setGeometry(QRect(0, 0, 280, 410))
        self.frameBlue.setStyleSheet(u"")
        self.frameBlue.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameBlue.setFrameShadow(QFrame.Shadow.Raised)
        self.lblTitle = QLabel(self.frameBlue)
        self.lblTitle.setObjectName(u"lblTitle")
        self.lblTitle.setGeometry(QRect(10, 20, 240, 50))
        self.lblTitle.setStyleSheet(u"")
        self.lblDescription = QLabel(self.frameBlue)
        self.lblDescription.setObjectName(u"lblDescription")
        self.lblDescription.setGeometry(QRect(20, 130, 231, 20))
        self.frameButtons = QFrame(OptionsForm)
        self.frameButtons.setObjectName(u"frameButtons")
        self.frameButtons.setGeometry(QRect(280, 0, 520, 410))
        self.frameButtons.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameButtons.setFrameShadow(QFrame.Shadow.Raised)
        self.scrollArea = QScrollArea(self.frameButtons)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(30, 10, 471, 321))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 469, 319))
        self.scrollCombo = QScrollArea(self.scrollAreaWidgetContents)
        self.scrollCombo.setObjectName(u"scrollCombo")
        self.scrollCombo.setGeometry(QRect(20, 10, 241, 321))
        self.scrollCombo.setWidgetResizable(True)
        self.scrollComboWidgetContents = QWidget()
        self.scrollComboWidgetContents.setObjectName(u"scrollComboWidgetContents")
        self.scrollComboWidgetContents.setGeometry(QRect(0, 0, 239, 319))
        self.scrollCombo.setWidget(self.scrollComboWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.btnSave = QPushButton(self.frameButtons)
        self.btnSave.setObjectName(u"btnSave")
        self.btnSave.setEnabled(True)
        self.btnSave.setGeometry(QRect(370, 340, 120, 40))
        self.btnReset = QPushButton(self.frameButtons)
        self.btnReset.setObjectName(u"btnReset")
        self.btnReset.setGeometry(QRect(220, 340, 131, 40))
        self.btnManager = QPushButton(self.frameButtons)
        self.btnManager.setObjectName(u"btnManager")
        self.btnManager.setGeometry(QRect(30, 340, 191, 40))
        self.frameHide = QFrame(self.frameButtons)
        self.frameHide.setObjectName(u"frameHide")
        self.frameHide.setGeometry(QRect(20, 20, 251, 311))
        self.frameHide.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameHide.setFrameShadow(QFrame.Shadow.Raised)
        self.lblUserGuide = QLabel(self.frameHide)
        self.lblUserGuide.setObjectName(u"lblUserGuide")
        self.lblUserGuide.setGeometry(QRect(20, 20, 221, 81))
        self.txtinputCommand = QLineEdit(self.frameHide)
        self.txtinputCommand.setObjectName(u"txtinputCommand")
        self.txtinputCommand.setGeometry(QRect(10, 60, 201, 28))
        self.btnCommandOk = QPushButton(self.frameHide)
        self.btnCommandOk.setObjectName(u"btnCommandOk")
        self.btnCommandOk.setGeometry(QRect(220, 60, 31, 29))

        self.retranslateUi(OptionsForm)

        QMetaObject.connectSlotsByName(OptionsForm)
    # setupUi

    def retranslateUi(self, OptionsForm):
        OptionsForm.setWindowTitle(QCoreApplication.translate("OptionsForm", u"Form", None))
        self.lblTitle.setText(QCoreApplication.translate("OptionsForm", u"Be\u00e1ll\u00edt\u00e1sok", None))
        self.lblDescription.setText(QCoreApplication.translate("OptionsForm", u"Le\u00edr\u00e1s", None))
        self.btnSave.setText(QCoreApplication.translate("OptionsForm", u"Ment\u00e9s", None))
        self.btnReset.setText(QCoreApplication.translate("OptionsForm", u"Alaphelyzet", None))
        self.btnManager.setText(QCoreApplication.translate("OptionsForm", u"Gesztusok kezel\u00e9se", None))
        self.lblUserGuide.setText(QCoreApplication.translate("OptionsForm", u"TextLabel", None))
        self.btnCommandOk.setText(QCoreApplication.translate("OptionsForm", u"PushButton", None))
    # retranslateUi


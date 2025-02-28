# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'optionsForm.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QSizePolicy,
    QWidget)

class Ui_OptionsForm(object):
    def setupUi(self, OptionsForm):
        if not OptionsForm.objectName():
            OptionsForm.setObjectName(u"OptionsForm")
        OptionsForm.resize(800, 410)
        self.frameBlue = QFrame(OptionsForm)
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
        self.frameButtons = QFrame(OptionsForm)
        self.frameButtons.setObjectName(u"frameButtons")
        self.frameButtons.setGeometry(QRect(280, 0, 520, 410))
        self.frameButtons.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameButtons.setFrameShadow(QFrame.Shadow.Raised)

        self.retranslateUi(OptionsForm)

        QMetaObject.connectSlotsByName(OptionsForm)
    # setupUi

    def retranslateUi(self, OptionsForm):
        OptionsForm.setWindowTitle(QCoreApplication.translate("OptionsForm", u"Form", None))
        self.lblTitle.setText(QCoreApplication.translate("OptionsForm", u"Be\u00e1ll\u00edt\u00e1sok", None))
    # retranslateUi


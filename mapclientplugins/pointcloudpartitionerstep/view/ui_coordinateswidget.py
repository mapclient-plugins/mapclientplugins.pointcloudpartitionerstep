# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'coordinateswidget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QLabel,
    QSizePolicy, QWidget)

class Ui_Coordinates(object):
    def setupUi(self, Coordinates):
        if not Coordinates.objectName():
            Coordinates.setObjectName(u"Coordinates")
        Coordinates.resize(400, 300)
        self.formLayout = QFormLayout(Coordinates)
        self.formLayout.setObjectName(u"formLayout")
        self.pointsFieldLabel = QLabel(Coordinates)
        self.pointsFieldLabel.setObjectName(u"pointsFieldLabel")
        self.pointsFieldLabel.setMaximumSize(QSize(160, 16777215))

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.pointsFieldLabel)

        self.pointsFieldComboBox = QComboBox(Coordinates)
        self.pointsFieldComboBox.setObjectName(u"pointsFieldComboBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.pointsFieldComboBox)

        self.meshFieldLabel = QLabel(Coordinates)
        self.meshFieldLabel.setObjectName(u"meshFieldLabel")
        self.meshFieldLabel.setMaximumSize(QSize(160, 16777215))

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.meshFieldLabel)

        self.meshFieldComboBox = QComboBox(Coordinates)
        self.meshFieldComboBox.setObjectName(u"meshFieldComboBox")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.meshFieldComboBox)


        self.retranslateUi(Coordinates)

        QMetaObject.connectSlotsByName(Coordinates)
    # setupUi

    def retranslateUi(self, Coordinates):
        Coordinates.setWindowTitle(QCoreApplication.translate("Coordinates", u"Coordinates", None))
        self.pointsFieldLabel.setText(QCoreApplication.translate("Coordinates", u"Points Coordinates Field:", None))
        self.meshFieldLabel.setText(QCoreApplication.translate("Coordinates", u"Mesh Coordinates Field:", None))
    # retranslateUi


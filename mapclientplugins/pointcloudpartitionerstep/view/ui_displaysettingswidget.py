# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'displaysettingswidget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QGridLayout,
    QLabel, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_DisplaySettings(object):
    def setupUi(self, DisplaySettings):
        if not DisplaySettings.objectName():
            DisplaySettings.setObjectName(u"DisplaySettings")
        DisplaySettings.resize(400, 300)
        self.verticalLayout = QVBoxLayout(DisplaySettings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.checkBoxSurfacesVisibility = QCheckBox(DisplaySettings)
        self.checkBoxSurfacesVisibility.setObjectName(u"checkBoxSurfacesVisibility")
        self.checkBoxSurfacesVisibility.setChecked(True)

        self.verticalLayout.addWidget(self.checkBoxSurfacesVisibility)

        self.checkBoxPointsVisibility = QCheckBox(DisplaySettings)
        self.checkBoxPointsVisibility.setObjectName(u"checkBoxPointsVisibility")
        self.checkBoxPointsVisibility.setChecked(True)

        self.verticalLayout.addWidget(self.checkBoxPointsVisibility)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(DisplaySettings)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.pointSizeSpinBox = QDoubleSpinBox(DisplaySettings)
        self.pointSizeSpinBox.setObjectName(u"pointSizeSpinBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pointSizeSpinBox.sizePolicy().hasHeightForWidth())
        self.pointSizeSpinBox.setSizePolicy(sizePolicy1)
        self.pointSizeSpinBox.setDecimals(4)
        self.pointSizeSpinBox.setMinimum(0.000100000000000)
        self.pointSizeSpinBox.setSingleStep(0.100000000000000)

        self.gridLayout.addWidget(self.pointSizeSpinBox, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 196, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(DisplaySettings)

        QMetaObject.connectSlotsByName(DisplaySettings)
    # setupUi

    def retranslateUi(self, DisplaySettings):
        DisplaySettings.setWindowTitle(QCoreApplication.translate("DisplaySettings", u"Display Settings", None))
        self.checkBoxSurfacesVisibility.setText(QCoreApplication.translate("DisplaySettings", u"Surfaces", None))
        self.checkBoxPointsVisibility.setText(QCoreApplication.translate("DisplaySettings", u"Points", None))
        self.label.setText(QCoreApplication.translate("DisplaySettings", u"Point Size:", None))
    # retranslateUi


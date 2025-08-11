# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'selectionwidget.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Selection(object):
    def setupUi(self, Selection):
        if not Selection.objectName():
            Selection.setObjectName(u"Selection")
        Selection.resize(479, 423)
        self.verticalLayout = QVBoxLayout(Selection)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.comboBoxSelectionMode = QComboBox(Selection)
        self.comboBoxSelectionMode.setObjectName(u"comboBoxSelectionMode")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxSelectionMode.sizePolicy().hasHeightForWidth())
        self.comboBoxSelectionMode.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.comboBoxSelectionMode, 1, 1, 1, 1)

        self.comboBoxSelectionType = QComboBox(Selection)
        self.comboBoxSelectionType.setObjectName(u"comboBoxSelectionType")

        self.gridLayout_2.addWidget(self.comboBoxSelectionType, 2, 1, 1, 1)

        self.label_3 = QLabel(Selection)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)

        self.label_2 = QLabel(Selection)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButtonInvertSelection = QPushButton(Selection)
        self.pushButtonInvertSelection.setObjectName(u"pushButtonInvertSelection")

        self.horizontalLayout_3.addWidget(self.pushButtonInvertSelection)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 3, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.labelTolerance = QLabel(Selection)
        self.labelTolerance.setObjectName(u"labelTolerance")
        self.labelTolerance.setEnabled(False)

        self.gridLayout_4.addWidget(self.labelTolerance, 0, 0, 1, 1)

        self.doubleSpinBoxTolerance = QDoubleSpinBox(Selection)
        self.doubleSpinBoxTolerance.setObjectName(u"doubleSpinBoxTolerance")
        self.doubleSpinBoxTolerance.setEnabled(False)
        self.doubleSpinBoxTolerance.setDecimals(6)
        self.doubleSpinBoxTolerance.setMaximum(99.999999000000003)
        self.doubleSpinBoxTolerance.setSingleStep(0.000001000000000)
        self.doubleSpinBoxTolerance.setValue(0.000010000000000)

        self.gridLayout_4.addWidget(self.doubleSpinBoxTolerance, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonSelectPointsOnSurface = QPushButton(Selection)
        self.pushButtonSelectPointsOnSurface.setObjectName(u"pushButtonSelectPointsOnSurface")
        self.pushButtonSelectPointsOnSurface.setEnabled(False)

        self.horizontalLayout.addWidget(self.pushButtonSelectPointsOnSurface)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.pushButtonDeleteSelectedSurfaceSection = QPushButton(Selection)
        self.pushButtonDeleteSelectedSurfaceSection.setObjectName(u"pushButtonDeleteSelectedSurfaceSection")
        self.pushButtonDeleteSelectedSurfaceSection.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.pushButtonDeleteSelectedSurfaceSection)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(Selection)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.comboBoxDeleteSurfaceHistory = QComboBox(Selection)
        self.comboBoxDeleteSurfaceHistory.setObjectName(u"comboBoxDeleteSurfaceHistory")
        self.comboBoxDeleteSurfaceHistory.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.comboBoxDeleteSurfaceHistory)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Selection)

        QMetaObject.connectSlotsByName(Selection)
    # setupUi

    def retranslateUi(self, Selection):
        Selection.setWindowTitle(QCoreApplication.translate("Selection", u"Selection", None))
        self.label_3.setText(QCoreApplication.translate("Selection", u"Selection Type:", None))
        self.label_2.setText(QCoreApplication.translate("Selection", u"Selection Mode:", None))
        self.pushButtonInvertSelection.setText(QCoreApplication.translate("Selection", u"Invert Selection", None))
        self.labelTolerance.setText(QCoreApplication.translate("Selection", u"Surface-Point Tolerance:", None))
        self.pushButtonSelectPointsOnSurface.setText(QCoreApplication.translate("Selection", u"Select Points on Surface", None))
        self.pushButtonDeleteSelectedSurfaceSection.setText(QCoreApplication.translate("Selection", u"Delete Selected Surface Section", None))
        self.label_4.setText(QCoreApplication.translate("Selection", u"Delete History:", None))
    # retranslateUi


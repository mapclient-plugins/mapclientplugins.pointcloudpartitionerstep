# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pointcloudpartitionerwidget.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QComboBox, QDoubleSpinBox, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from mapclientplugins.pointcloudpartitionerstep.view.grouptableview import GroupTableView
from mapclientplugins.pointcloudpartitionerstep.view.zincpointcloudpartitionerwidget import ZincPointCloudPartitionerWidget

class Ui_PointCloudPartitionerWidget(object):
    def setupUi(self, PointCloudPartitionerWidget):
        if not PointCloudPartitionerWidget.objectName():
            PointCloudPartitionerWidget.setObjectName(u"PointCloudPartitionerWidget")
        PointCloudPartitionerWidget.resize(884, 859)
        self.verticalLayout_10 = QVBoxLayout(PointCloudPartitionerWidget)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.groupBox = QGroupBox(PointCloudPartitionerWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.groupBox_2 = QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupTableView = GroupTableView(self.groupBox_2)
        self.groupTableView.setObjectName(u"groupTableView")
        self.groupTableView.setAcceptDrops(True)
        self.groupTableView.setStyleSheet(u"QTableView { padding: 3px; }\n"
"QTableView::item { padding: 3px; }")
        self.groupTableView.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.groupTableView.setDragEnabled(True)
        self.groupTableView.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.groupTableView.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.groupTableView.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.groupTableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.groupTableView.setShowGrid(False)
        self.groupTableView.horizontalHeader().setVisible(False)
        self.groupTableView.horizontalHeader().setMinimumSectionSize(20)
        self.groupTableView.horizontalHeader().setDefaultSectionSize(80)
        self.groupTableView.horizontalHeader().setHighlightSections(False)
        self.groupTableView.verticalHeader().setVisible(False)
        self.groupTableView.verticalHeader().setHighlightSections(False)

        self.verticalLayout_4.addWidget(self.groupTableView)

        self.pushButtonCreateGroup = QPushButton(self.groupBox_2)
        self.pushButtonCreateGroup.setObjectName(u"pushButtonCreateGroup")

        self.verticalLayout_4.addWidget(self.pushButtonCreateGroup)

        self.pushButtonDeleteGroup = QPushButton(self.groupBox_2)
        self.pushButtonDeleteGroup.setObjectName(u"pushButtonDeleteGroup")

        self.verticalLayout_4.addWidget(self.pushButtonDeleteGroup)

        self.pushButtonAddToGroup = QPushButton(self.groupBox_2)
        self.pushButtonAddToGroup.setObjectName(u"pushButtonAddToGroup")
        self.pushButtonAddToGroup.setEnabled(False)

        self.verticalLayout_4.addWidget(self.pushButtonAddToGroup)

        self.pushButtonRemoveFromGroup = QPushButton(self.groupBox_2)
        self.pushButtonRemoveFromGroup.setObjectName(u"pushButtonRemoveFromGroup")
        self.pushButtonRemoveFromGroup.setEnabled(False)

        self.verticalLayout_4.addWidget(self.pushButtonRemoveFromGroup)


        self.verticalLayout_9.addWidget(self.groupBox_2)

        self.groupBox_7 = QGroupBox(self.groupBox)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.gridLayout_5 = QGridLayout(self.groupBox_7)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.pointsFieldComboBox = QComboBox(self.groupBox_7)
        self.pointsFieldComboBox.setObjectName(u"pointsFieldComboBox")

        self.gridLayout_5.addWidget(self.pointsFieldComboBox, 0, 1, 1, 1)

        self.meshFieldLabel = QLabel(self.groupBox_7)
        self.meshFieldLabel.setObjectName(u"meshFieldLabel")
        self.meshFieldLabel.setMaximumSize(QSize(160, 16777215))

        self.gridLayout_5.addWidget(self.meshFieldLabel, 3, 0, 1, 1)

        self.meshFieldComboBox = QComboBox(self.groupBox_7)
        self.meshFieldComboBox.setObjectName(u"meshFieldComboBox")

        self.gridLayout_5.addWidget(self.meshFieldComboBox, 3, 1, 1, 1)

        self.pointsFieldLabel = QLabel(self.groupBox_7)
        self.pointsFieldLabel.setObjectName(u"pointsFieldLabel")
        self.pointsFieldLabel.setMaximumSize(QSize(160, 16777215))

        self.gridLayout_5.addWidget(self.pointsFieldLabel, 0, 0, 1, 1)


        self.verticalLayout_9.addWidget(self.groupBox_7)

        self.groupBox_5 = QGroupBox(self.groupBox)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.comboBoxSelectionMode = QComboBox(self.groupBox_5)
        self.comboBoxSelectionMode.setObjectName(u"comboBoxSelectionMode")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBoxSelectionMode.sizePolicy().hasHeightForWidth())
        self.comboBoxSelectionMode.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.comboBoxSelectionMode, 1, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox_5)
        self.label_2.setObjectName(u"label_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.comboBoxSelectionType = QComboBox(self.groupBox_5)
        self.comboBoxSelectionType.setObjectName(u"comboBoxSelectionType")

        self.gridLayout_2.addWidget(self.comboBoxSelectionType, 2, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox_5)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)


        self.verticalLayout_7.addLayout(self.gridLayout_2)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.labelTolerance = QLabel(self.groupBox_5)
        self.labelTolerance.setObjectName(u"labelTolerance")
        self.labelTolerance.setEnabled(False)

        self.gridLayout_4.addWidget(self.labelTolerance, 0, 0, 1, 1)

        self.doubleSpinBoxTolerance = QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBoxTolerance.setObjectName(u"doubleSpinBoxTolerance")
        self.doubleSpinBoxTolerance.setEnabled(False)
        self.doubleSpinBoxTolerance.setDecimals(6)
        self.doubleSpinBoxTolerance.setMaximum(99.999999000000003)
        self.doubleSpinBoxTolerance.setSingleStep(0.000001000000000)
        self.doubleSpinBoxTolerance.setValue(0.000010000000000)

        self.gridLayout_4.addWidget(self.doubleSpinBoxTolerance, 0, 1, 1, 1)


        self.verticalLayout_7.addLayout(self.gridLayout_4)

        self.pushButtonSelectPointsOnSurface = QPushButton(self.groupBox_5)
        self.pushButtonSelectPointsOnSurface.setObjectName(u"pushButtonSelectPointsOnSurface")
        self.pushButtonSelectPointsOnSurface.setEnabled(False)

        self.verticalLayout_7.addWidget(self.pushButtonSelectPointsOnSurface)

        self.pushButtonDeleteSelectedSurfaceSection = QPushButton(self.groupBox_5)
        self.pushButtonDeleteSelectedSurfaceSection.setObjectName(u"pushButtonDeleteSelectedSurfaceSection")
        self.pushButtonDeleteSelectedSurfaceSection.setEnabled(False)

        self.verticalLayout_7.addWidget(self.pushButtonDeleteSelectedSurfaceSection)


        self.verticalLayout_9.addWidget(self.groupBox_5)

        self.groupBox_6 = QGroupBox(self.groupBox)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.checkBoxSurfacesVisibility = QCheckBox(self.groupBox_6)
        self.checkBoxSurfacesVisibility.setObjectName(u"checkBoxSurfacesVisibility")
        self.checkBoxSurfacesVisibility.setChecked(True)

        self.verticalLayout_6.addWidget(self.checkBoxSurfacesVisibility)

        self.checkBoxPointsVisibility = QCheckBox(self.groupBox_6)
        self.checkBoxPointsVisibility.setObjectName(u"checkBoxPointsVisibility")
        self.checkBoxPointsVisibility.setChecked(True)

        self.verticalLayout_6.addWidget(self.checkBoxPointsVisibility)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.groupBox_6)
        self.label.setObjectName(u"label")
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.pointSizeSpinBox = QDoubleSpinBox(self.groupBox_6)
        self.pointSizeSpinBox.setObjectName(u"pointSizeSpinBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pointSizeSpinBox.sizePolicy().hasHeightForWidth())
        self.pointSizeSpinBox.setSizePolicy(sizePolicy3)
        self.pointSizeSpinBox.setSingleStep(0.100000000000000)

        self.gridLayout.addWidget(self.pointSizeSpinBox, 0, 1, 1, 1)


        self.verticalLayout_6.addLayout(self.gridLayout)


        self.verticalLayout_9.addWidget(self.groupBox_6)

        self.groupBox_3 = QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.pushButtonViewAll = QPushButton(self.groupBox_3)
        self.pushButtonViewAll.setObjectName(u"pushButtonViewAll")

        self.horizontalLayout_3.addWidget(self.pushButtonViewAll)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout_9.addWidget(self.groupBox_3)


        self.horizontalLayout_2.addLayout(self.verticalLayout_9)

        self.widgetZinc = ZincPointCloudPartitionerWidget(self.groupBox)
        self.widgetZinc.setObjectName(u"widgetZinc")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(3)
        sizePolicy4.setVerticalStretch(1)
        sizePolicy4.setHeightForWidth(self.widgetZinc.sizePolicy().hasHeightForWidth())
        self.widgetZinc.setSizePolicy(sizePolicy4)

        self.horizontalLayout_2.addWidget(self.widgetZinc)


        self.verticalLayout_10.addWidget(self.groupBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonContinue = QPushButton(PointCloudPartitionerWidget)
        self.pushButtonContinue.setObjectName(u"pushButtonContinue")

        self.horizontalLayout.addWidget(self.pushButtonContinue)


        self.verticalLayout_10.addLayout(self.horizontalLayout)


        self.retranslateUi(PointCloudPartitionerWidget)

        QMetaObject.connectSlotsByName(PointCloudPartitionerWidget)
    # setupUi

    def retranslateUi(self, PointCloudPartitionerWidget):
        PointCloudPartitionerWidget.setWindowTitle(QCoreApplication.translate("PointCloudPartitionerWidget", u"Point Cloud Partitioner", None))
        self.groupBox.setTitle(QCoreApplication.translate("PointCloudPartitionerWidget", u"Point Cloud Partitioner", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("PointCloudPartitionerWidget", u"Group Points", None))
        self.pushButtonCreateGroup.setText(QCoreApplication.translate("PointCloudPartitionerWidget", u"Create Group", None))
        self.pushButtonDeleteGroup.setText(QCoreApplication.translate("PointCloudPartitionerWidget", u"Delete Group", None))
        self.pushButtonAddToGroup.setText(QCoreApplication.translate("PointCloudPartitionerWidget", u"Add Selected Points to Group", None))
        self.pushButtonRemoveFromGroup.setText(QCoreApplication.translate("PointCloudPartitionerWidget", u"Remove Selected Points from Group", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("PointCloudPartitionerWidget", u"Coordinates", None))
        self.meshFieldLabel.setText(QCoreApplication.translate("PointCloudPartitionerWidget", u"Mesh Coordinates Field:", None))
        self.pointsFieldLabel.setText(QCoreApplication.translate("PointCloudPartitionerWidget", u"Points Coordinates Field:", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("PointCloudPartitionerWidget", u"Selection", None))
        self.label_2.setText(QCoreApplication.translate("PointCloudPartitionerWidget", u"Selection Mode:", None))
        self.label_3.setText(QCoreApplication.translate("PointCloudPartitionerWidget", u"Selection Type:", None))
        self.labelTolerance.setText(QCoreApplication.translate("PointCloudPartitionerWidget", u"Surface-Point Tolerance:", None))
        self.pushButtonSelectPointsOnSurface.setText(QCoreApplication.translate("PointCloudPartitionerWidget", u"Select Points on Surface", None))
        self.pushButtonDeleteSelectedSurfaceSection.setText(QCoreApplication.translate("PointCloudPartitionerWidget", u"Delete Selected Surface Section", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("PointCloudPartitionerWidget", u"Visibility", None))
        self.checkBoxSurfacesVisibility.setText(QCoreApplication.translate("PointCloudPartitionerWidget", u"Surfaces", None))
        self.checkBoxPointsVisibility.setText(QCoreApplication.translate("PointCloudPartitionerWidget", u"Points", None))
        self.label.setText(QCoreApplication.translate("PointCloudPartitionerWidget", u"Point Size:", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("PointCloudPartitionerWidget", u"View", None))
        self.pushButtonViewAll.setText(QCoreApplication.translate("PointCloudPartitionerWidget", u"View All", None))
        self.pushButtonContinue.setText(QCoreApplication.translate("PointCloudPartitionerWidget", u"Continue", None))
    # retranslateUi


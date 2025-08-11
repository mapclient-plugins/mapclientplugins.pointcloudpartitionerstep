# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'grouppointswidget.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QHBoxLayout,
    QHeaderView, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from mapclientplugins.pointcloudpartitionerstep.view.grouptableview import GroupTableView

class Ui_GroupPoints(object):
    def setupUi(self, GroupPoints):
        if not GroupPoints.objectName():
            GroupPoints.setObjectName(u"GroupPoints")
        GroupPoints.resize(379, 282)
        self.verticalLayout = QVBoxLayout(GroupPoints)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupTableView = GroupTableView(GroupPoints)
        self.groupTableView.setObjectName(u"groupTableView")
        self.groupTableView.setAcceptDrops(True)
        self.groupTableView.setStyleSheet(u"QTableView { padding: 3px; }\n"
"QTableView::item { padding: 3px; }")
        self.groupTableView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.groupTableView.setDragEnabled(True)
        self.groupTableView.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.groupTableView.setDefaultDropAction(Qt.IgnoreAction)
        self.groupTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.groupTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.groupTableView.setShowGrid(False)
        self.groupTableView.horizontalHeader().setVisible(False)
        self.groupTableView.horizontalHeader().setMinimumSectionSize(20)
        self.groupTableView.horizontalHeader().setDefaultSectionSize(80)
        self.groupTableView.horizontalHeader().setHighlightSections(False)
        self.groupTableView.verticalHeader().setVisible(False)
        self.groupTableView.verticalHeader().setHighlightSections(False)

        self.verticalLayout.addWidget(self.groupTableView)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButtonCreateGroup = QPushButton(GroupPoints)
        self.pushButtonCreateGroup.setObjectName(u"pushButtonCreateGroup")

        self.horizontalLayout_4.addWidget(self.pushButtonCreateGroup)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButtonDeleteGroup = QPushButton(GroupPoints)
        self.pushButtonDeleteGroup.setObjectName(u"pushButtonDeleteGroup")

        self.horizontalLayout_3.addWidget(self.pushButtonDeleteGroup)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButtonAddToGroup = QPushButton(GroupPoints)
        self.pushButtonAddToGroup.setObjectName(u"pushButtonAddToGroup")
        self.pushButtonAddToGroup.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.pushButtonAddToGroup)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonRemoveFromGroup = QPushButton(GroupPoints)
        self.pushButtonRemoveFromGroup.setObjectName(u"pushButtonRemoveFromGroup")
        self.pushButtonRemoveFromGroup.setEnabled(False)

        self.horizontalLayout.addWidget(self.pushButtonRemoveFromGroup)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(GroupPoints)

        QMetaObject.connectSlotsByName(GroupPoints)
    # setupUi

    def retranslateUi(self, GroupPoints):
        GroupPoints.setWindowTitle(QCoreApplication.translate("GroupPoints", u"Group Points", None))
        self.pushButtonCreateGroup.setText(QCoreApplication.translate("GroupPoints", u"Create Group", None))
        self.pushButtonDeleteGroup.setText(QCoreApplication.translate("GroupPoints", u"Delete Group", None))
        self.pushButtonAddToGroup.setText(QCoreApplication.translate("GroupPoints", u"Add Selected Points to Group", None))
        self.pushButtonRemoveFromGroup.setText(QCoreApplication.translate("GroupPoints", u"Remove Selected Points from Group", None))
    # retranslateUi


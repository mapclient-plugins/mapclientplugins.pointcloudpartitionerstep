# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pointcloudpartitionerwidget.ui'
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
from PySide6.QtWidgets import (QApplication, QMainWindow, QSizePolicy, QVBoxLayout,
    QWidget)

from mapclientplugins.pointcloudpartitionerstep.view.zincpointcloudpartitionerwidget import ZincPointCloudPartitionerWidget

class Ui_PointCloudPartitionerWidget(object):
    def setupUi(self, PointCloudPartitionerWidget):
        if not PointCloudPartitionerWidget.objectName():
            PointCloudPartitionerWidget.setObjectName(u"PointCloudPartitionerWidget")
        PointCloudPartitionerWidget.resize(800, 600)
        self.centralwidget = QWidget(PointCloudPartitionerWidget)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widgetZinc = ZincPointCloudPartitionerWidget(self.centralwidget)
        self.widgetZinc.setObjectName(u"widgetZinc")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widgetZinc.sizePolicy().hasHeightForWidth())
        self.widgetZinc.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.widgetZinc)

        PointCloudPartitionerWidget.setCentralWidget(self.centralwidget)

        self.retranslateUi(PointCloudPartitionerWidget)

        QMetaObject.connectSlotsByName(PointCloudPartitionerWidget)
    # setupUi

    def retranslateUi(self, PointCloudPartitionerWidget):
        PointCloudPartitionerWidget.setWindowTitle(QCoreApplication.translate("PointCloudPartitionerWidget", u"Point Cloud Partitioner", None))
    # retranslateUi


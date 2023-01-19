# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'electrodeprojectionwidget.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDockWidget, QDoubleSpinBox,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

from opencmiss.utils.zinc.widgets.basesceneviewerwidget import BaseSceneviewerWidget
from  . import resources_rc

class Ui_ElectrodeProjectionWidget(object):
    def setupUi(self, ElectrodeProjectionWidget):
        if not ElectrodeProjectionWidget.objectName():
            ElectrodeProjectionWidget.setObjectName(u"ElectrodeProjectionWidget")
        ElectrodeProjectionWidget.resize(1093, 872)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ElectrodeProjectionWidget.sizePolicy().hasHeightForWidth())
        ElectrodeProjectionWidget.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(ElectrodeProjectionWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.dockWidget = QDockWidget(ElectrodeProjectionWidget)
        self.dockWidget.setObjectName(u"dockWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.dockWidget.sizePolicy().hasHeightForWidth())
        self.dockWidget.setSizePolicy(sizePolicy1)
        self.dockWidget.setMinimumSize(QSize(353, 430))
        self.dockWidget.setFeatures(QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.dockWidget.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy2)
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.identifier_frame = QFrame(self.dockWidgetContents)
        self.identifier_frame.setObjectName(u"identifier_frame")
        self.identifier_frame.setMinimumSize(QSize(0, 0))
        self.identifier_frame.setFrameShape(QFrame.StyledPanel)
        self.identifier_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.identifier_frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 5, -1, 3)
        self.identifier_label = QLabel(self.identifier_frame)
        self.identifier_label.setObjectName(u"identifier_label")

        self.verticalLayout_4.addWidget(self.identifier_label)

        self.line = QFrame(self.identifier_frame)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line)


        self.verticalLayout.addWidget(self.identifier_frame)

        self.time_groupBox = QGroupBox(self.dockWidgetContents)
        self.time_groupBox.setObjectName(u"time_groupBox")
        self.gridLayout_4 = QGridLayout(self.time_groupBox)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.timePlayStop_pushButton = QPushButton(self.time_groupBox)
        self.timePlayStop_pushButton.setObjectName(u"timePlayStop_pushButton")

        self.gridLayout_4.addWidget(self.timePlayStop_pushButton, 1, 1, 1, 1)

        self.timeValue_label = QLabel(self.time_groupBox)
        self.timeValue_label.setObjectName(u"timeValue_label")

        self.gridLayout_4.addWidget(self.timeValue_label, 0, 0, 1, 1)

        self.timeValue_doubleSpinBox = QDoubleSpinBox(self.time_groupBox)
        self.timeValue_doubleSpinBox.setObjectName(u"timeValue_doubleSpinBox")
        self.timeValue_doubleSpinBox.setMaximum(12000.000000000000000)

        self.gridLayout_4.addWidget(self.timeValue_doubleSpinBox, 0, 1, 1, 1)

        self.timeLoop_checkBox = QCheckBox(self.time_groupBox)
        self.timeLoop_checkBox.setObjectName(u"timeLoop_checkBox")

        self.gridLayout_4.addWidget(self.timeLoop_checkBox, 1, 2, 1, 1)


        self.verticalLayout.addWidget(self.time_groupBox)

        self.projection_groupBox = QGroupBox(self.dockWidgetContents)
        self.projection_groupBox.setObjectName(u"projection_groupBox")
        self.gridLayout_3 = QGridLayout(self.projection_groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.projectElectrodes_label = QLabel(self.projection_groupBox)
        self.projectElectrodes_label.setObjectName(u"projectElectrodes_label")

        self.gridLayout_3.addWidget(self.projectElectrodes_label, 3, 0, 1, 1)

        self.projectElectrodes_pushButton = QPushButton(self.projection_groupBox)
        self.projectElectrodes_pushButton.setObjectName(u"projectElectrodes_pushButton")

        self.gridLayout_3.addWidget(self.projectElectrodes_pushButton, 3, 2, 1, 1)

        self.projectionDepth_spinBox = QSpinBox(self.projection_groupBox)
        self.projectionDepth_spinBox.setObjectName(u"projectionDepth_spinBox")
        self.projectionDepth_spinBox.setMaximum(9999)

        self.gridLayout_3.addWidget(self.projectionDepth_spinBox, 1, 2, 1, 1)

        self.projectionDepth_label = QLabel(self.projection_groupBox)
        self.projectionDepth_label.setObjectName(u"projectionDepth_label")

        self.gridLayout_3.addWidget(self.projectionDepth_label, 1, 0, 1, 1)

        self.projectionPointScale_label = QLabel(self.projection_groupBox)
        self.projectionPointScale_label.setObjectName(u"projectionPointScale_label")

        self.gridLayout_3.addWidget(self.projectionPointScale_label, 2, 0, 1, 1)

        self.projectionPointScale_doubleSpinBox = QDoubleSpinBox(self.projection_groupBox)
        self.projectionPointScale_doubleSpinBox.setObjectName(u"projectionPointScale_doubleSpinBox")
        self.projectionPointScale_doubleSpinBox.setMinimum(-99.989999999999995)
        self.projectionPointScale_doubleSpinBox.setSingleStep(0.100000000000000)

        self.gridLayout_3.addWidget(self.projectionPointScale_doubleSpinBox, 2, 2, 1, 1)


        self.verticalLayout.addWidget(self.projection_groupBox)

        self.verticalSpacer = QSpacerItem(20, 557, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.frame = QFrame(self.dockWidgetContents)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.viewAll_button = QPushButton(self.frame)
        self.viewAll_button.setObjectName(u"viewAll_button")

        self.horizontalLayout_2.addWidget(self.viewAll_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.done_button = QPushButton(self.frame)
        self.done_button.setObjectName(u"done_button")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.done_button.sizePolicy().hasHeightForWidth())
        self.done_button.setSizePolicy(sizePolicy3)

        self.horizontalLayout_2.addWidget(self.done_button)


        self.verticalLayout.addWidget(self.frame)

        self.dockWidget.setWidget(self.dockWidgetContents)

        self.gridLayout.addWidget(self.dockWidget, 0, 0, 1, 1)

        self.sceneviewer_widget = BaseSceneviewerWidget(ElectrodeProjectionWidget)
        self.sceneviewer_widget.setObjectName(u"sceneviewer_widget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(4)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.sceneviewer_widget.sizePolicy().hasHeightForWidth())
        self.sceneviewer_widget.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.sceneviewer_widget, 0, 1, 1, 1)


        self.retranslateUi(ElectrodeProjectionWidget)

        QMetaObject.connectSlotsByName(ElectrodeProjectionWidget)
    # setupUi

    def retranslateUi(self, ElectrodeProjectionWidget):
        ElectrodeProjectionWidget.setWindowTitle(QCoreApplication.translate("ElectrodeProjectionWidget", u"Electrode Projection", None))
        self.dockWidget.setWindowTitle(QCoreApplication.translate("ElectrodeProjectionWidget", u"Control Panel", None))
        self.identifier_label.setText(QCoreApplication.translate("ElectrodeProjectionWidget", u"Identifier", None))
        self.time_groupBox.setTitle(QCoreApplication.translate("ElectrodeProjectionWidget", u"Time:", None))
        self.timePlayStop_pushButton.setText(QCoreApplication.translate("ElectrodeProjectionWidget", u"Play", None))
        self.timeValue_label.setText(QCoreApplication.translate("ElectrodeProjectionWidget", u"Time value:", None))
        self.timeLoop_checkBox.setText(QCoreApplication.translate("ElectrodeProjectionWidget", u"Loop", None))
        self.projection_groupBox.setTitle(QCoreApplication.translate("ElectrodeProjectionWidget", u"Projection:", None))
        self.projectElectrodes_label.setText(QCoreApplication.translate("ElectrodeProjectionWidget", u"Project electrodes on plane:", None))
        self.projectElectrodes_pushButton.setText(QCoreApplication.translate("ElectrodeProjectionWidget", u"Project electrodes", None))
        self.projectionDepth_label.setText(QCoreApplication.translate("ElectrodeProjectionWidget", u"Projection depth:", None))
        self.projectionPointScale_label.setText(QCoreApplication.translate("ElectrodeProjectionWidget", u"Projection point scale:", None))
        self.viewAll_button.setText(QCoreApplication.translate("ElectrodeProjectionWidget", u"View All", None))
        self.done_button.setText(QCoreApplication.translate("ElectrodeProjectionWidget", u"Done", None))
    # retranslateUi


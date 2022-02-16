# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'filterMes.ui'
##
## Created by: Qt User Interface Compiler version 5.14.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(603, 316)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_7 = QGridLayout(self.centralwidget)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_5, 0, 1, 1, 1)

        self.resetButton = QPushButton(self.centralwidget)
        self.resetButton.setObjectName(u"resetButton")

        self.gridLayout.addWidget(self.resetButton, 0, 0, 1, 1)

        self.applyButton = QPushButton(self.centralwidget)
        self.applyButton.setObjectName(u"applyButton")

        self.gridLayout.addWidget(self.applyButton, 0, 2, 1, 1)

        self.cancleButton = QPushButton(self.centralwidget)
        self.cancleButton.setObjectName(u"cancleButton")

        self.gridLayout.addWidget(self.cancleButton, 0, 3, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.deleteButton = QPushButton(self.centralwidget)
        self.deleteButton.setObjectName(u"deleteButton")

        self.gridLayout_7.addWidget(self.deleteButton, 2, 0, 1, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.rangeOfValuesTab = QWidget()
        self.rangeOfValuesTab.setObjectName(u"rangeOfValuesTab")
        self.gridLayout_10 = QGridLayout(self.rangeOfValuesTab)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer, 0, 0, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setSizeConstraint(QLayout.SetFixedSize)
        self.rangeMin = QLineEdit(self.rangeOfValuesTab)
        self.rangeMin.setObjectName(u"rangeMin")

        self.gridLayout_5.addWidget(self.rangeMin, 0, 0, 1, 1)

        self.rangeMax = QLineEdit(self.rangeOfValuesTab)
        self.rangeMax.setObjectName(u"rangeMax")

        self.gridLayout_5.addWidget(self.rangeMax, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(200, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(200, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)


        self.gridLayout_10.addLayout(self.gridLayout_5, 1, 0, 1, 1)

        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.atLeatLabel = QLabel(self.rangeOfValuesTab)
        self.atLeatLabel.setObjectName(u"atLeatLabel")

        self.gridLayout_8.addWidget(self.atLeatLabel, 0, 0, 1, 1)

        self.atLeatSlider = QSlider(self.rangeOfValuesTab)
        self.atLeatSlider.setObjectName(u"atLeatSlider")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.atLeatSlider.sizePolicy().hasHeightForWidth())
        self.atLeatSlider.setSizePolicy(sizePolicy)
        self.atLeatSlider.setLayoutDirection(Qt.LeftToRight)
        self.atLeatSlider.setOrientation(Qt.Horizontal)
        self.atLeatSlider.setTickPosition(QSlider.TicksBelow)

        self.gridLayout_8.addWidget(self.atLeatSlider, 0, 1, 1, 1)


        self.gridLayout_10.addLayout(self.gridLayout_8, 3, 0, 1, 1)

        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.atMostLabel = QLabel(self.rangeOfValuesTab)
        self.atMostLabel.setObjectName(u"atMostLabel")

        self.gridLayout_9.addWidget(self.atMostLabel, 0, 0, 1, 1)

        self.atMostSlider = QSlider(self.rangeOfValuesTab)
        self.atMostSlider.setObjectName(u"atMostSlider")
        self.atMostSlider.setLayoutDirection(Qt.RightToLeft)
        self.atMostSlider.setStyleSheet(u"\"QSlider::groove:horizontal {background-color:red;}\"")
        self.atMostSlider.setValue(20)
        self.atMostSlider.setTracking(True)
        self.atMostSlider.setOrientation(Qt.Horizontal)
        self.atMostSlider.setInvertedAppearance(False)
        self.atMostSlider.setTickPosition(QSlider.TicksBelow)

        self.gridLayout_9.addWidget(self.atMostSlider, 0, 1, 1, 1)


        self.gridLayout_10.addLayout(self.gridLayout_9, 4, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer_2, 6, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.atLeastValueLabel = QLabel(self.rangeOfValuesTab)
        self.atLeastValueLabel.setObjectName(u"atLeastValueLabel")

        self.gridLayout_2.addWidget(self.atLeastValueLabel, 0, 0, 1, 1)

        self.atMostValueLabel = QLabel(self.rangeOfValuesTab)
        self.atMostValueLabel.setObjectName(u"atMostValueLabel")

        self.gridLayout_2.addWidget(self.atMostValueLabel, 0, 1, 1, 1)


        self.gridLayout_10.addLayout(self.gridLayout_2, 5, 0, 1, 1)

        self.tabWidget.addTab(self.rangeOfValuesTab, QString())
        self.atLeastTab = QWidget()
        self.atLeastTab.setObjectName(u"atLeastTab")
        self.gridLayout_4 = QGridLayout(self.atLeastTab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalSpacer_4 = QSpacerItem(20, 11, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_4, 6, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 11, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_3, 0, 0, 1, 1)

        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setSizeConstraint(QLayout.SetFixedSize)
        self.atLeastMin = QLineEdit(self.atLeastTab)
        self.atLeastMin.setObjectName(u"atLeastMin")

        self.gridLayout_6.addWidget(self.atLeastMin, 0, 0, 1, 1)

        self.atLeastMax = QLineEdit(self.atLeastTab)
        self.atLeastMax.setObjectName(u"atLeastMax")

        self.gridLayout_6.addWidget(self.atLeastMax, 0, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(200, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_3, 0, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(200, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_4, 0, 2, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_6, 1, 0, 1, 1)

        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")

        self.gridLayout_4.addLayout(self.gridLayout_11, 4, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.atLeastValueLabel_3 = QLabel(self.atLeastTab)
        self.atLeastValueLabel_3.setObjectName(u"atLeastValueLabel_3")

        self.gridLayout_3.addWidget(self.atLeastValueLabel_3, 0, 0, 1, 1)

        self.atMostValueLabel_2 = QLabel(self.atLeastTab)
        self.atMostValueLabel_2.setObjectName(u"atMostValueLabel_2")

        self.gridLayout_3.addWidget(self.atMostValueLabel_2, 0, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_3, 5, 0, 1, 1)

        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.atLeatLabel_2 = QLabel(self.atLeastTab)
        self.atLeatLabel_2.setObjectName(u"atLeatLabel_2")

        self.gridLayout_12.addWidget(self.atLeatLabel_2, 0, 0, 1, 1)

        self.atLeatSlider_2 = QSlider(self.atLeastTab)
        self.atLeatSlider_2.setObjectName(u"atLeatSlider_2")
        sizePolicy.setHeightForWidth(self.atLeatSlider_2.sizePolicy().hasHeightForWidth())
        self.atLeatSlider_2.setSizePolicy(sizePolicy)
        self.atLeatSlider_2.setLayoutDirection(Qt.LeftToRight)
        self.atLeatSlider_2.setOrientation(Qt.Horizontal)
        self.atLeatSlider_2.setTickPosition(QSlider.TicksBelow)

        self.gridLayout_12.addWidget(self.atLeatSlider_2, 0, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_12, 3, 0, 1, 1)

        self.tabWidget.addTab(self.atLeastTab, QString())
        self.atMostTab = QWidget()
        self.atMostTab.setObjectName(u"atMostTab")
        self.gridLayout_20 = QGridLayout(self.atMostTab)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.verticalSpacer_5 = QSpacerItem(20, 11, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_20.addItem(self.verticalSpacer_5, 0, 0, 1, 1)

        self.gridLayout_18 = QGridLayout()
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setSizeConstraint(QLayout.SetFixedSize)
        self.atMostMin = QLineEdit(self.atMostTab)
        self.atMostMin.setObjectName(u"atMostMin")

        self.gridLayout_18.addWidget(self.atMostMin, 0, 0, 1, 1)

        self.atMostMax = QLineEdit(self.atMostTab)
        self.atMostMax.setObjectName(u"atMostMax")

        self.gridLayout_18.addWidget(self.atMostMax, 0, 3, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(200, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_7, 0, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(200, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_8, 0, 2, 1, 1)


        self.gridLayout_20.addLayout(self.gridLayout_18, 1, 0, 1, 1)

        self.gridLayout_19 = QGridLayout()
        self.gridLayout_19.setObjectName(u"gridLayout_19")

        self.gridLayout_20.addLayout(self.gridLayout_19, 3, 0, 1, 1)

        self.gridLayout_16 = QGridLayout()
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.atMostLabel_3 = QLabel(self.atMostTab)
        self.atMostLabel_3.setObjectName(u"atMostLabel_3")

        self.gridLayout_16.addWidget(self.atMostLabel_3, 0, 0, 1, 1)

        self.atMostSlider_3 = QSlider(self.atMostTab)
        self.atMostSlider_3.setObjectName(u"atMostSlider_3")
        self.atMostSlider_3.setLayoutDirection(Qt.RightToLeft)
        self.atMostSlider_3.setStyleSheet(u"\"QSlider::groove:horizontal {background-color:red;}\"")
        self.atMostSlider_3.setValue(20)
        self.atMostSlider_3.setTracking(True)
        self.atMostSlider_3.setOrientation(Qt.Horizontal)
        self.atMostSlider_3.setInvertedAppearance(False)
        self.atMostSlider_3.setTickPosition(QSlider.TicksBelow)

        self.gridLayout_16.addWidget(self.atMostSlider_3, 0, 1, 1, 1)


        self.gridLayout_20.addLayout(self.gridLayout_16, 4, 0, 1, 1)

        self.gridLayout_17 = QGridLayout()
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.atLeastValueLabel_4 = QLabel(self.atMostTab)
        self.atLeastValueLabel_4.setObjectName(u"atLeastValueLabel_4")

        self.gridLayout_17.addWidget(self.atLeastValueLabel_4, 0, 0, 1, 1)

        self.atMostValueLabel_3 = QLabel(self.atMostTab)
        self.atMostValueLabel_3.setObjectName(u"atMostValueLabel_3")

        self.gridLayout_17.addWidget(self.atMostValueLabel_3, 0, 1, 1, 1)


        self.gridLayout_20.addLayout(self.gridLayout_17, 5, 0, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 11, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_20.addItem(self.verticalSpacer_6, 6, 0, 1, 1)

        self.tabWidget.addTab(self.atMostTab, QString())

        self.gridLayout_7.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 603, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.resetButton.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.applyButton.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.cancleButton.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.deleteButton.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.atLeatLabel.setText(QCoreApplication.translate("MainWindow", u"At least", None))
        self.atMostLabel.setText(QCoreApplication.translate("MainWindow", u"At most", None))
        self.atLeastValueLabel.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.atMostValueLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">99</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.rangeOfValuesTab), QCoreApplication.translate("MainWindow", u"Range of values", None))
        self.atLeastValueLabel_3.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.atMostValueLabel_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">99</p></body></html>", None))
        self.atLeatLabel_2.setText(QCoreApplication.translate("MainWindow", u"At least", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.atLeastTab), QCoreApplication.translate("MainWindow", u"At least", None))
        self.atMostLabel_3.setText(QCoreApplication.translate("MainWindow", u"At most", None))
        self.atLeastValueLabel_4.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.atMostValueLabel_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">99</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.atMostTab), QCoreApplication.translate("MainWindow", u"At most", None))
    # retranslateUi


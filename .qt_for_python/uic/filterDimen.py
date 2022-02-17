# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'filterDimen.ui'
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
        MainWindow.resize(443, 605)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_4 = QGridLayout(self.tab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.allButton = QPushButton(self.tab)
        self.allButton.setObjectName(u"allButton")

        self.gridLayout_2.addWidget(self.allButton, 0, 0, 1, 1)

        self.noneButton = QPushButton(self.tab)
        self.noneButton.setObjectName(u"noneButton")

        self.gridLayout_2.addWidget(self.noneButton, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.fieldLabel = QLabel(self.tab)
        self.fieldLabel.setObjectName(u"fieldLabel")

        self.gridLayout_4.addWidget(self.fieldLabel, 3, 0, 1, 1)

        self.filterItemListWidget = QListWidget(self.tab)
        self.filterItemListWidget.setObjectName(u"filterItemListWidget")
        self.filterItemListWidget.setFocusPolicy(Qt.NoFocus)
        self.filterItemListWidget.setContextMenuPolicy(Qt.NoContextMenu)
        self.filterItemListWidget.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.filterItemListWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        self.gridLayout_4.addWidget(self.filterItemListWidget, 1, 0, 1, 1)

        self.selectionLabel = QLabel(self.tab)
        self.selectionLabel.setObjectName(u"selectionLabel")

        self.gridLayout_4.addWidget(self.selectionLabel, 4, 0, 1, 1)

        self.summaryLabel = QLabel(self.tab)
        self.summaryLabel.setObjectName(u"summaryLabel")

        self.gridLayout_4.addWidget(self.summaryLabel, 2, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.resetButton = QPushButton(self.tab)
        self.resetButton.setObjectName(u"resetButton")

        self.gridLayout_3.addWidget(self.resetButton, 0, 0, 1, 1)

        self.okButton = QPushButton(self.tab)
        self.okButton.setObjectName(u"okButton")

        self.gridLayout_3.addWidget(self.okButton, 0, 2, 1, 1)

        self.cancleButton = QPushButton(self.tab)
        self.cancleButton.setObjectName(u"cancleButton")

        self.gridLayout_3.addWidget(self.cancleButton, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 0, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_3, 5, 0, 1, 1)

        self.tabWidget.addTab(self.tab, QString())
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tab_2.setEnabled(True)
        self.tabWidget.addTab(self.tab_2, QString())

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 443, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.allButton.setText(QCoreApplication.translate("MainWindow", u"All", None))
        self.noneButton.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.fieldLabel.setText(QCoreApplication.translate("MainWindow", u"Field :", None))
        self.selectionLabel.setText(QCoreApplication.translate("MainWindow", u"Selection : ", None))
        self.summaryLabel.setText(QCoreApplication.translate("MainWindow", u"Summary", None))
        self.resetButton.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.okButton.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.cancleButton.setText(QCoreApplication.translate("MainWindow", u"Cancle", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Genneral", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
    # retranslateUi


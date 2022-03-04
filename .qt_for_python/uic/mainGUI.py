# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainGUI.ui'
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

import FileInDirec
import FileChoose
import rowListClass
import colListClass
import filListClass

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(968, 601)
        MainWindow.setContextMenuPolicy(Qt.ActionsContextMenu)
        MainWindow.setTabShape(QTabWidget.Rounded)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_7 = QGridLayout(self.centralwidget)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.South)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setMovable(False)
        self.dataSourceTab = QWidget()
        self.dataSourceTab.setObjectName(u"dataSourceTab")
        self.gridLayout_6 = QGridLayout(self.dataSourceTab)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.saveButton = QPushButton(self.dataSourceTab)
        self.saveButton.setObjectName(u"saveButton")

        self.gridLayout_5.addWidget(self.saveButton, 0, 1, 1, 1)

        self.loadButton = QPushButton(self.dataSourceTab)
        self.loadButton.setObjectName(u"loadButton")

        self.gridLayout_5.addWidget(self.loadButton, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(700, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer, 0, 0, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout_5, 1, 0, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.selectDimentionLabel = QLabel(self.dataSourceTab)
        self.selectDimentionLabel.setObjectName(u"selectDimentionLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectDimentionLabel.sizePolicy().hasHeightForWidth())
        self.selectDimentionLabel.setSizePolicy(sizePolicy)
        self.selectDimentionLabel.setMinimumSize(QSize(50, 0))
        self.selectDimentionLabel.setSizeIncrement(QSize(50, 0))
        font = QFont()
        font.setPointSize(10)
        self.selectDimentionLabel.setFont(font)

        self.gridLayout.addWidget(self.selectDimentionLabel, 0, 0, 1, 1)

        self.openDirecButton = QPushButton(self.dataSourceTab)
        self.openDirecButton.setObjectName(u"openDirecButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.openDirecButton.sizePolicy().hasHeightForWidth())
        self.openDirecButton.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.openDirecButton, 0, 1, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 2)

        self.FileList = FileInDirec(self.dataSourceTab)
        self.FileList.setObjectName(u"FileList")
        self.FileList.setAcceptDrops(True)
        self.FileList.setEditTriggers(QAbstractItemView.CurrentChanged|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed|QAbstractItemView.SelectedClicked)
        self.FileList.setProperty("showDropIndicator", True)
        self.FileList.setDragEnabled(True)
        self.FileList.setDragDropOverwriteMode(False)
        self.FileList.setDragDropMode(QAbstractItemView.DragDrop)
        self.FileList.setDefaultDropAction(Qt.MoveAction)
        self.FileList.setMovement(QListView.Free)
        self.FileList.setProperty("isWrapping", False)
        self.FileList.setWordWrap(False)

        self.gridLayout_3.addWidget(self.FileList, 1, 0, 1, 2)

        self.FileListChoose = FileChoose(self.dataSourceTab)
        self.FileListChoose.setObjectName(u"FileListChoose")
        self.FileListChoose.setMouseTracking(True)
        self.FileListChoose.setTabletTracking(True)
        self.FileListChoose.setAcceptDrops(True)
        self.FileListChoose.setTabKeyNavigation(True)
        self.FileListChoose.setDragEnabled(True)
        self.FileListChoose.setDragDropOverwriteMode(False)
        self.FileListChoose.setDragDropMode(QAbstractItemView.DragDrop)
        self.FileListChoose.setDefaultDropAction(Qt.MoveAction)
        self.FileListChoose.setSelectionMode(QAbstractItemView.SingleSelection)
        self.FileListChoose.setProperty("isWrapping", False)
        self.FileListChoose.setWordWrap(False)

        self.gridLayout_3.addWidget(self.FileListChoose, 4, 0, 1, 2)

        self.usedFileLabel = QLabel(self.dataSourceTab)
        self.usedFileLabel.setObjectName(u"usedFileLabel")
        self.usedFileLabel.setFont(font)

        self.gridLayout_3.addWidget(self.usedFileLabel, 2, 0, 1, 2)


        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.table = QTableView(self.dataSourceTab)
        self.table.setObjectName(u"table")
        self.table.setAcceptDrops(False)
        self.table.setDragEnabled(False)
        self.table.setDragDropOverwriteMode(False)
        self.table.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.table.setDefaultDropAction(Qt.IgnoreAction)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectColumns)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(False)

        self.gridLayout_4.addWidget(self.table, 0, 1, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout_4, 0, 0, 1, 1)

        self.tabWidget.addTab(self.dataSourceTab, QString())
        self.SheetTab = QWidget()
        self.SheetTab.setObjectName(u"SheetTab")
        self.gridLayout_12 = QGridLayout(self.SheetTab)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setSpacing(10)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setSizeConstraint(QLayout.SetNoConstraint)
        self.filterList = filListClass(self.SheetTab)
        self.filterList.setObjectName(u"filterList")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.filterList.sizePolicy().hasHeightForWidth())
        self.filterList.setSizePolicy(sizePolicy2)
        self.filterList.setMinimumSize(QSize(140, 280))
        self.filterList.setMaximumSize(QSize(100, 16777215))
        self.filterList.setAcceptDrops(True)
        self.filterList.setProperty("showDropIndicator", False)
        self.filterList.setDragDropMode(QAbstractItemView.DragDrop)
        self.filterList.setDefaultDropAction(Qt.MoveAction)

        self.gridLayout_10.addWidget(self.filterList, 1, 2, 2, 1)

        self.MeasureValuesLabel = QLabel(self.SheetTab)
        self.MeasureValuesLabel.setObjectName(u"MeasureValuesLabel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.MeasureValuesLabel.sizePolicy().hasHeightForWidth())
        self.MeasureValuesLabel.setSizePolicy(sizePolicy3)
        self.MeasureValuesLabel.setFont(font)

        self.gridLayout_10.addWidget(self.MeasureValuesLabel, 3, 1, 1, 1)

        self.FileListMes = QListWidget(self.SheetTab)
        self.FileListMes.setObjectName(u"FileListMes")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.FileListMes.sizePolicy().hasHeightForWidth())
        self.FileListMes.setSizePolicy(sizePolicy4)
        self.FileListMes.setMinimumSize(QSize(140, 0))
        self.FileListMes.setMaximumSize(QSize(100, 16777215))
        self.FileListMes.setFocusPolicy(Qt.StrongFocus)
        self.FileListMes.setAcceptDrops(False)
        self.FileListMes.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.FileListMes.setProperty("showDropIndicator", False)
        self.FileListMes.setDragEnabled(True)
        self.FileListMes.setDragDropOverwriteMode(True)
        self.FileListMes.setDragDropMode(QAbstractItemView.DragOnly)
        self.FileListMes.setDefaultDropAction(Qt.CopyAction)
        self.FileListMes.setBatchSize(100)
        self.FileListMes.setWordWrap(False)
        self.FileListMes.setSortingEnabled(True)

        self.gridLayout_10.addWidget(self.FileListMes, 4, 1, 1, 1)

        self.filterLabel = QLabel(self.SheetTab)
        self.filterLabel.setObjectName(u"filterLabel")
        sizePolicy3.setHeightForWidth(self.filterLabel.sizePolicy().hasHeightForWidth())
        self.filterLabel.setSizePolicy(sizePolicy3)
        self.filterLabel.setMinimumSize(QSize(0, 0))
        self.filterLabel.setFont(font)

        self.gridLayout_10.addWidget(self.filterLabel, 0, 2, 1, 2)

        self.DimensionValuesLabel = QLabel(self.SheetTab)
        self.DimensionValuesLabel.setObjectName(u"DimensionValuesLabel")
        sizePolicy3.setHeightForWidth(self.DimensionValuesLabel.sizePolicy().hasHeightForWidth())
        self.DimensionValuesLabel.setSizePolicy(sizePolicy3)
        self.DimensionValuesLabel.setFont(font)

        self.gridLayout_10.addWidget(self.DimensionValuesLabel, 0, 1, 1, 1)

        self.FileListDimension = QTreeWidget(self.SheetTab)
        self.FileListDimension.setObjectName(u"FileListDimension")
        sizePolicy2.setHeightForWidth(self.FileListDimension.sizePolicy().hasHeightForWidth())
        self.FileListDimension.setSizePolicy(sizePolicy2)
        self.FileListDimension.setMinimumSize(QSize(140, 280))
        self.FileListDimension.setMaximumSize(QSize(100, 16777215))
        self.FileListDimension.setFocusPolicy(Qt.StrongFocus)
        self.FileListDimension.setAcceptDrops(False)
        self.FileListDimension.setLineWidth(0)
        self.FileListDimension.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.FileListDimension.setTabKeyNavigation(False)
        self.FileListDimension.setProperty("showDropIndicator", False)
        self.FileListDimension.setDragEnabled(True)
        self.FileListDimension.setDragDropOverwriteMode(True)
        self.FileListDimension.setDragDropMode(QAbstractItemView.DragOnly)
        self.FileListDimension.setDefaultDropAction(Qt.CopyAction)
        self.FileListDimension.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.FileListDimension.setColumnCount(1)

        self.gridLayout_10.addWidget(self.FileListDimension, 1, 1, 2, 1)


        self.gridLayout_12.addLayout(self.gridLayout_10, 0, 0, 2, 1)

        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.RowLabel = QLabel(self.SheetTab)
        self.RowLabel.setObjectName(u"RowLabel")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.RowLabel.sizePolicy().hasHeightForWidth())
        self.RowLabel.setSizePolicy(sizePolicy5)
        self.RowLabel.setMinimumSize(QSize(0, 30))
        self.RowLabel.setFont(font)

        self.gridLayout_8.addWidget(self.RowLabel, 0, 0, 1, 1)

        self.ColLabel = QLabel(self.SheetTab)
        self.ColLabel.setObjectName(u"ColLabel")
        sizePolicy5.setHeightForWidth(self.ColLabel.sizePolicy().hasHeightForWidth())
        self.ColLabel.setSizePolicy(sizePolicy5)
        self.ColLabel.setMinimumSize(QSize(0, 30))
        self.ColLabel.setFont(font)

        self.gridLayout_8.addWidget(self.ColLabel, 2, 0, 1, 1)

        self.RowList = rowListClass(self.SheetTab)
        self.RowList.setObjectName(u"RowList")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.RowList.sizePolicy().hasHeightForWidth())
        self.RowList.setSizePolicy(sizePolicy6)
        self.RowList.setMinimumSize(QSize(0, 40))
        self.RowList.setMaximumSize(QSize(16777215, 40))
        self.RowList.setMouseTracking(False)
        self.RowList.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.RowList.setAcceptDrops(True)
        self.RowList.setLayoutDirection(Qt.LeftToRight)
        self.RowList.setAutoFillBackground(True)
        self.RowList.setFrameShape(QFrame.StyledPanel)
        self.RowList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.RowList.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.RowList.setAutoScroll(True)
        self.RowList.setAutoScrollMargin(5)
        self.RowList.setProperty("showDropIndicator", False)
        self.RowList.setDragEnabled(True)
        self.RowList.setDragDropOverwriteMode(False)
        self.RowList.setDragDropMode(QAbstractItemView.DragDrop)
        self.RowList.setDefaultDropAction(Qt.MoveAction)
        self.RowList.setSelectionMode(QAbstractItemView.SingleSelection)
        self.RowList.setTextElideMode(Qt.ElideMiddle)
        self.RowList.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.RowList.setHorizontalScrollMode(QAbstractItemView.ScrollPerItem)
        self.RowList.setFlow(QListView.LeftToRight)
        self.RowList.setProperty("isWrapping", False)
        self.RowList.setResizeMode(QListView.Adjust)
        self.RowList.setSpacing(5)
        self.RowList.setGridSize(QSize(60, 0))
        self.RowList.setViewMode(QListView.ListMode)
        self.RowList.setModelColumn(0)
        self.RowList.setUniformItemSizes(False)
        self.RowList.setBatchSize(1)
        self.RowList.setWordWrap(False)
        self.RowList.setSelectionRectVisible(False)
        self.RowList.setSortingEnabled(False)

        self.gridLayout_8.addWidget(self.RowList, 0, 1, 1, 1)

        self.ColList = colListClass(self.SheetTab)
        self.ColList.setObjectName(u"ColList")
        sizePolicy6.setHeightForWidth(self.ColList.sizePolicy().hasHeightForWidth())
        self.ColList.setSizePolicy(sizePolicy6)
        self.ColList.setMinimumSize(QSize(0, 40))
        self.ColList.setMaximumSize(QSize(16777215, 40))
        self.ColList.setMouseTracking(False)
        self.ColList.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.ColList.setAcceptDrops(True)
        self.ColList.setLayoutDirection(Qt.LeftToRight)
        self.ColList.setAutoFillBackground(True)
        self.ColList.setFrameShape(QFrame.StyledPanel)
        self.ColList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ColList.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.ColList.setAutoScroll(True)
        self.ColList.setAutoScrollMargin(5)
        self.ColList.setProperty("showDropIndicator", False)
        self.ColList.setDragEnabled(True)
        self.ColList.setDragDropOverwriteMode(False)
        self.ColList.setDragDropMode(QAbstractItemView.DragDrop)
        self.ColList.setDefaultDropAction(Qt.MoveAction)
        self.ColList.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ColList.setTextElideMode(Qt.ElideMiddle)
        self.ColList.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.ColList.setHorizontalScrollMode(QAbstractItemView.ScrollPerItem)
        self.ColList.setFlow(QListView.LeftToRight)
        self.ColList.setProperty("isWrapping", False)
        self.ColList.setResizeMode(QListView.Adjust)
        self.ColList.setSpacing(5)
        self.ColList.setGridSize(QSize(60, 0))
        self.ColList.setViewMode(QListView.ListMode)
        self.ColList.setModelColumn(0)
        self.ColList.setUniformItemSizes(False)
        self.ColList.setBatchSize(1)
        self.ColList.setWordWrap(False)
        self.ColList.setSelectionRectVisible(False)
        self.ColList.setSortingEnabled(False)

        self.gridLayout_8.addWidget(self.ColList, 2, 1, 1, 1)


        self.gridLayout_12.addLayout(self.gridLayout_8, 0, 1, 1, 1)

        self.tabWidget_2 = QTabWidget(self.SheetTab)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_2 = QGridLayout(self.tab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.sheetTable = QTableView(self.tab)
        self.sheetTable.setObjectName(u"sheetTable")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.sheetTable.sizePolicy().hasHeightForWidth())
        self.sheetTable.setSizePolicy(sizePolicy7)
        self.sheetTable.setMinimumSize(QSize(0, 0))
        self.sheetTable.setBaseSize(QSize(0, 1000))
        font1 = QFont()
        font1.setPointSize(8)
        font1.setStyleStrategy(QFont.PreferDefault)
        self.sheetTable.setFont(font1)
        self.sheetTable.setMouseTracking(False)
        self.sheetTable.setTabletTracking(False)
        self.sheetTable.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.sheetTable.setAcceptDrops(False)
        self.sheetTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.sheetTable.setAutoScroll(True)
        self.sheetTable.setDragEnabled(False)
        self.sheetTable.setDragDropOverwriteMode(False)
        self.sheetTable.setDragDropMode(QAbstractItemView.InternalMove)
        self.sheetTable.setDefaultDropAction(Qt.MoveAction)
        self.sheetTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.sheetTable.setSelectionBehavior(QAbstractItemView.SelectColumns)
        self.sheetTable.setShowGrid(True)
        self.sheetTable.setCornerButtonEnabled(True)
        self.sheetTable.horizontalHeader().setHighlightSections(True)
        self.sheetTable.verticalHeader().setHighlightSections(True)

        self.gridLayout_2.addWidget(self.sheetTable, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab, QString())
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_11 = QGridLayout(self.tab_2)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.frame = QFrame(self.tab_2)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.gridLayout_11.addWidget(self.frame, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_2, QString())

        self.gridLayout_12.addWidget(self.tabWidget_2, 1, 1, 1, 1)

        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.horizontalSpacer_2 = QSpacerItem(500, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.chartType = QComboBox(self.SheetTab)
        self.chartType.setObjectName(u"chartType")
        sizePolicy5.setHeightForWidth(self.chartType.sizePolicy().hasHeightForWidth())
        self.chartType.setSizePolicy(sizePolicy5)
        self.chartType.setMaxVisibleItems(10)

        self.gridLayout_9.addWidget(self.chartType, 0, 1, 1, 1)


        self.gridLayout_12.addLayout(self.gridLayout_9, 2, 0, 1, 2)

        self.tabWidget.addTab(self.SheetTab, QString())

        self.gridLayout_7.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 968, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.saveButton.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.loadButton.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.selectDimentionLabel.setText(QCoreApplication.translate("MainWindow", u"Choose Directory", None))
        self.openDirecButton.setText(QCoreApplication.translate("MainWindow", u"Directory", None))
        self.usedFileLabel.setText(QCoreApplication.translate("MainWindow", u"Union File", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dataSourceTab), QCoreApplication.translate("MainWindow", u"Data Source", None))
        self.MeasureValuesLabel.setText(QCoreApplication.translate("MainWindow", u"Measure Values", None))
        self.filterLabel.setText(QCoreApplication.translate("MainWindow", u"Filter", None))
        self.DimensionValuesLabel.setText(QCoreApplication.translate("MainWindow", u"Dimension", None))
        ___qtreewidgetitem = self.FileListDimension.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Dimension", None));
        self.RowLabel.setText(QCoreApplication.translate("MainWindow", u"Row", None))
        self.ColLabel.setText(QCoreApplication.translate("MainWindow", u"Column", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Table", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Chart", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SheetTab), QCoreApplication.translate("MainWindow", u"Sheet", None))
    # retranslateUi


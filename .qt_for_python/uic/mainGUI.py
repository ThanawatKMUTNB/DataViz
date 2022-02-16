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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(760, 601)
        MainWindow.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_7 = QGridLayout(self.centralwidget)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
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

        self.usedFileLabel = QLabel(self.dataSourceTab)
        self.usedFileLabel.setObjectName(u"usedFileLabel")
        self.usedFileLabel.setFont(font)

        self.gridLayout_3.addWidget(self.usedFileLabel, 2, 0, 1, 1)

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
        self.gridLayout_14 = QGridLayout(self.SheetTab)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.horizontalSpacer_2 = QSpacerItem(500, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.chartType = QComboBox(self.SheetTab)
        self.chartType.addItem(QString())
        self.chartType.addItem(QString())
        self.chartType.addItem(QString())
        self.chartType.addItem(QString())
        self.chartType.setObjectName(u"chartType")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.chartType.sizePolicy().hasHeightForWidth())
        self.chartType.setSizePolicy(sizePolicy2)
        self.chartType.setMaxVisibleItems(10)

        self.gridLayout_9.addWidget(self.chartType, 0, 1, 1, 1)

        self.plotButton = QPushButton(self.SheetTab)
        self.plotButton.setObjectName(u"plotButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.plotButton.sizePolicy().hasHeightForWidth())
        self.plotButton.setSizePolicy(sizePolicy3)

        self.gridLayout_9.addWidget(self.plotButton, 0, 2, 1, 1)


        self.gridLayout_11.addLayout(self.gridLayout_9, 1, 0, 1, 3)

        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setSpacing(10)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setSizeConstraint(QLayout.SetNoConstraint)
        self.DimensionValuesLabel = QLabel(self.SheetTab)
        self.DimensionValuesLabel.setObjectName(u"DimensionValuesLabel")
        sizePolicy3.setHeightForWidth(self.DimensionValuesLabel.sizePolicy().hasHeightForWidth())
        self.DimensionValuesLabel.setSizePolicy(sizePolicy3)
        self.DimensionValuesLabel.setFont(font)

        self.gridLayout_10.addWidget(self.DimensionValuesLabel, 0, 0, 1, 1)

        self.FileListDimension = QListWidget(self.SheetTab)
        self.FileListDimension.setObjectName(u"FileListDimension")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.FileListDimension.sizePolicy().hasHeightForWidth())
        self.FileListDimension.setSizePolicy(sizePolicy4)
        self.FileListDimension.setMinimumSize(QSize(100, 0))
        self.FileListDimension.setMaximumSize(QSize(100, 16777215))
        self.FileListDimension.setFocusPolicy(Qt.StrongFocus)
        self.FileListDimension.setAcceptDrops(False)
        self.FileListDimension.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.FileListDimension.setTabKeyNavigation(False)
        self.FileListDimension.setProperty("showDropIndicator", False)
        self.FileListDimension.setDragEnabled(True)
        self.FileListDimension.setDragDropOverwriteMode(True)
        self.FileListDimension.setDragDropMode(QAbstractItemView.DragOnly)
        self.FileListDimension.setDefaultDropAction(Qt.CopyAction)
        self.FileListDimension.setBatchSize(100)
        self.FileListDimension.setWordWrap(False)
        self.FileListDimension.setSortingEnabled(True)

        self.gridLayout_10.addWidget(self.FileListDimension, 1, 0, 2, 1)

        self.MeasureValuesLabel = QLabel(self.SheetTab)
        self.MeasureValuesLabel.setObjectName(u"MeasureValuesLabel")
        sizePolicy3.setHeightForWidth(self.MeasureValuesLabel.sizePolicy().hasHeightForWidth())
        self.MeasureValuesLabel.setSizePolicy(sizePolicy3)
        self.MeasureValuesLabel.setFont(font)

        self.gridLayout_10.addWidget(self.MeasureValuesLabel, 3, 0, 1, 1)

        self.FileListMes = QListWidget(self.SheetTab)
        self.FileListMes.setObjectName(u"FileListMes")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.FileListMes.sizePolicy().hasHeightForWidth())
        self.FileListMes.setSizePolicy(sizePolicy5)
        self.FileListMes.setMinimumSize(QSize(100, 0))
        self.FileListMes.setMaximumSize(QSize(100, 16777215))
        self.FileListMes.setFocusPolicy(Qt.StrongFocus)
        self.FileListMes.setAcceptDrops(False)
        self.FileListMes.setProperty("showDropIndicator", False)
        self.FileListMes.setDragEnabled(True)
        self.FileListMes.setDragDropOverwriteMode(False)
        self.FileListMes.setDragDropMode(QAbstractItemView.DragOnly)
        self.FileListMes.setDefaultDropAction(Qt.CopyAction)
        self.FileListMes.setBatchSize(100)
        self.FileListMes.setWordWrap(True)
        self.FileListMes.setSortingEnabled(True)

        self.gridLayout_10.addWidget(self.FileListMes, 4, 0, 1, 1)

        self.filterLabel = QLabel(self.SheetTab)
        self.filterLabel.setObjectName(u"filterLabel")
        sizePolicy3.setHeightForWidth(self.filterLabel.sizePolicy().hasHeightForWidth())
        self.filterLabel.setSizePolicy(sizePolicy3)
        self.filterLabel.setMinimumSize(QSize(0, 0))
        self.filterLabel.setFont(font)

        self.gridLayout_10.addWidget(self.filterLabel, 0, 1, 1, 2)

        self.filterList = rowListClass(self.SheetTab)
        self.filterList.setObjectName(u"filterList")
        sizePolicy4.setHeightForWidth(self.filterList.sizePolicy().hasHeightForWidth())
        self.filterList.setSizePolicy(sizePolicy4)
        self.filterList.setMinimumSize(QSize(100, 0))
        self.filterList.setMaximumSize(QSize(100, 16777215))
        self.filterList.setAcceptDrops(True)
        self.filterList.setProperty("showDropIndicator", False)
        self.filterList.setDragDropMode(QAbstractItemView.DragDrop)
        self.filterList.setDefaultDropAction(Qt.MoveAction)

        self.gridLayout_10.addWidget(self.filterList, 1, 1, 2, 1)


        self.gridLayout_11.addLayout(self.gridLayout_10, 0, 0, 1, 2)

        self.gridLayout_13 = QGridLayout()
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.RowList = rowListClass(self.SheetTab)
        self.RowList.setObjectName(u"RowList")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.RowList.sizePolicy().hasHeightForWidth())
        self.RowList.setSizePolicy(sizePolicy6)
        self.RowList.setMinimumSize(QSize(0, 40))
        self.RowList.setMaximumSize(QSize(16777215, 40))
        self.RowList.setMouseTracking(True)
        self.RowList.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.RowList.setAcceptDrops(False)
        self.RowList.setLayoutDirection(Qt.LeftToRight)
        self.RowList.setAutoFillBackground(True)
        self.RowList.setAutoScroll(True)
        self.RowList.setAutoScrollMargin(5)
        self.RowList.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed|QAbstractItemView.SelectedClicked)
        self.RowList.setProperty("showDropIndicator", False)
        self.RowList.setDragEnabled(False)
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
        self.RowList.setSpacing(0)
        self.RowList.setGridSize(QSize(100, 0))
        self.RowList.setViewMode(QListView.ListMode)
        self.RowList.setModelColumn(0)
        self.RowList.setUniformItemSizes(False)
        self.RowList.setWordWrap(False)
        self.RowList.setSelectionRectVisible(False)
        self.RowList.setSortingEnabled(False)

        self.gridLayout_8.addWidget(self.RowList, 0, 1, 1, 1)

        self.ColLabel = QLabel(self.SheetTab)
        self.ColLabel.setObjectName(u"ColLabel")
        sizePolicy2.setHeightForWidth(self.ColLabel.sizePolicy().hasHeightForWidth())
        self.ColLabel.setSizePolicy(sizePolicy2)
        self.ColLabel.setMinimumSize(QSize(0, 30))
        self.ColLabel.setFont(font)

        self.gridLayout_8.addWidget(self.ColLabel, 1, 0, 1, 1)

        self.RowLabel = QLabel(self.SheetTab)
        self.RowLabel.setObjectName(u"RowLabel")
        sizePolicy2.setHeightForWidth(self.RowLabel.sizePolicy().hasHeightForWidth())
        self.RowLabel.setSizePolicy(sizePolicy2)
        self.RowLabel.setMinimumSize(QSize(0, 30))
        self.RowLabel.setFont(font)

        self.gridLayout_8.addWidget(self.RowLabel, 0, 0, 1, 1)

        self.ColList = rowListClass(self.SheetTab)
        self.ColList.setObjectName(u"ColList")
        sizePolicy6.setHeightForWidth(self.ColList.sizePolicy().hasHeightForWidth())
        self.ColList.setSizePolicy(sizePolicy6)
        self.ColList.setMinimumSize(QSize(0, 40))
        self.ColList.setMaximumSize(QSize(16777215, 40))
        self.ColList.setMouseTracking(True)
        self.ColList.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.ColList.setAcceptDrops(False)
        self.ColList.setLayoutDirection(Qt.LeftToRight)
        self.ColList.setAutoFillBackground(True)
        self.ColList.setAutoScroll(True)
        self.ColList.setAutoScrollMargin(5)
        self.ColList.setProperty("showDropIndicator", False)
        self.ColList.setDragEnabled(False)
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
        self.ColList.setSpacing(0)
        self.ColList.setGridSize(QSize(100, 0))
        self.ColList.setViewMode(QListView.ListMode)
        self.ColList.setModelColumn(0)
        self.ColList.setUniformItemSizes(False)
        self.ColList.setWordWrap(False)
        self.ColList.setSelectionRectVisible(False)
        self.ColList.setSortingEnabled(False)

        self.gridLayout_8.addWidget(self.ColList, 1, 1, 1, 1)


        self.gridLayout_13.addLayout(self.gridLayout_8, 0, 0, 1, 1)

        self.sheetTable = QTableView(self.SheetTab)
        self.sheetTable.setObjectName(u"sheetTable")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.sheetTable.sizePolicy().hasHeightForWidth())
        self.sheetTable.setSizePolicy(sizePolicy7)
        self.sheetTable.setMinimumSize(QSize(0, 0))
        self.sheetTable.setBaseSize(QSize(0, 1000))
        font1 = QFont()
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

        self.gridLayout_13.addWidget(self.sheetTable, 1, 0, 1, 1)


        self.gridLayout_11.addLayout(self.gridLayout_13, 0, 2, 1, 1)


        self.gridLayout_14.addLayout(self.gridLayout_11, 0, 0, 1, 1)

        self.tabWidget.addTab(self.SheetTab, QString())
        self.chartTab = QWidget()
        self.chartTab.setObjectName(u"chartTab")
        self.gridLayout_20 = QGridLayout(self.chartTab)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_15 = QGridLayout()
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_16 = QGridLayout()
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.horizontalSpacer_3 = QSpacerItem(500, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.chartType_2 = QComboBox(self.chartTab)
        self.chartType_2.addItem(QString())
        self.chartType_2.addItem(QString())
        self.chartType_2.addItem(QString())
        self.chartType_2.addItem(QString())
        self.chartType_2.setObjectName(u"chartType_2")
        sizePolicy2.setHeightForWidth(self.chartType_2.sizePolicy().hasHeightForWidth())
        self.chartType_2.setSizePolicy(sizePolicy2)
        self.chartType_2.setMaxVisibleItems(10)

        self.gridLayout_16.addWidget(self.chartType_2, 0, 1, 1, 1)

        self.plotButton_2 = QPushButton(self.chartTab)
        self.plotButton_2.setObjectName(u"plotButton_2")
        sizePolicy3.setHeightForWidth(self.plotButton_2.sizePolicy().hasHeightForWidth())
        self.plotButton_2.setSizePolicy(sizePolicy3)

        self.gridLayout_16.addWidget(self.plotButton_2, 0, 2, 1, 1)


        self.gridLayout_15.addLayout(self.gridLayout_16, 1, 0, 1, 3)

        self.gridLayout_17 = QGridLayout()
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.widget = QWidget(self.chartTab)
        self.widget.setObjectName(u"widget")
        sizePolicy7.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy7)
        self.widget.setMouseTracking(True)

        self.gridLayout_17.addWidget(self.widget, 1, 0, 1, 1)

        self.gridLayout_18 = QGridLayout()
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.ColList_2 = QListWidget(self.chartTab)
        brush = QBrush(QColor(238, 238, 238, 255))
        brush.setStyle(Qt.Dense4Pattern)
        __qlistwidgetitem = QListWidgetItem(self.ColList_2)
        __qlistwidgetitem.setBackground(brush);
        QListWidgetItem(self.ColList_2)
        QListWidgetItem(self.ColList_2)
        self.ColList_2.setObjectName(u"ColList_2")
        sizePolicy6.setHeightForWidth(self.ColList_2.sizePolicy().hasHeightForWidth())
        self.ColList_2.setSizePolicy(sizePolicy6)
        self.ColList_2.setMinimumSize(QSize(0, 20))
        self.ColList_2.setMaximumSize(QSize(16777215, 30))
        self.ColList_2.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.ColList_2.setAcceptDrops(True)
        self.ColList_2.setLayoutDirection(Qt.LeftToRight)
        self.ColList_2.setAutoFillBackground(True)
        self.ColList_2.setAutoScroll(True)
        self.ColList_2.setAutoScrollMargin(5)
        self.ColList_2.setDragEnabled(True)
        self.ColList_2.setDragDropOverwriteMode(False)
        self.ColList_2.setDragDropMode(QAbstractItemView.DragDrop)
        self.ColList_2.setDefaultDropAction(Qt.MoveAction)
        self.ColList_2.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ColList_2.setTextElideMode(Qt.ElideRight)
        self.ColList_2.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.ColList_2.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.ColList_2.setFlow(QListView.LeftToRight)
        self.ColList_2.setProperty("isWrapping", False)
        self.ColList_2.setSpacing(0)
        self.ColList_2.setGridSize(QSize(100, 0))
        self.ColList_2.setViewMode(QListView.ListMode)
        self.ColList_2.setUniformItemSizes(False)
        self.ColList_2.setWordWrap(True)
        self.ColList_2.setSelectionRectVisible(False)
        self.ColList_2.setSortingEnabled(False)

        self.gridLayout_18.addWidget(self.ColList_2, 1, 1, 1, 1)

        self.ColLabel_2 = QLabel(self.chartTab)
        self.ColLabel_2.setObjectName(u"ColLabel_2")
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.ColLabel_2.sizePolicy().hasHeightForWidth())
        self.ColLabel_2.setSizePolicy(sizePolicy8)
        self.ColLabel_2.setFont(font)

        self.gridLayout_18.addWidget(self.ColLabel_2, 1, 0, 1, 1)

        self.RowLabel_2 = QLabel(self.chartTab)
        self.RowLabel_2.setObjectName(u"RowLabel_2")
        sizePolicy8.setHeightForWidth(self.RowLabel_2.sizePolicy().hasHeightForWidth())
        self.RowLabel_2.setSizePolicy(sizePolicy8)
        self.RowLabel_2.setFont(font)

        self.gridLayout_18.addWidget(self.RowLabel_2, 0, 0, 1, 1)

        self.RowList_2 = QListWidget(self.chartTab)
        brush1 = QBrush(QColor(238, 238, 238, 255))
        brush1.setStyle(Qt.Dense4Pattern)
        __qlistwidgetitem1 = QListWidgetItem(self.RowList_2)
        __qlistwidgetitem1.setBackground(brush1);
        __qlistwidgetitem1.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled|Qt.ItemIsTristate);
        QListWidgetItem(self.RowList_2)
        QListWidgetItem(self.RowList_2)
        self.RowList_2.setObjectName(u"RowList_2")
        sizePolicy6.setHeightForWidth(self.RowList_2.sizePolicy().hasHeightForWidth())
        self.RowList_2.setSizePolicy(sizePolicy6)
        self.RowList_2.setMinimumSize(QSize(0, 20))
        self.RowList_2.setMaximumSize(QSize(16777215, 30))
        self.RowList_2.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.RowList_2.setAcceptDrops(True)
        self.RowList_2.setLayoutDirection(Qt.LeftToRight)
        self.RowList_2.setAutoFillBackground(True)
        self.RowList_2.setAutoScroll(True)
        self.RowList_2.setAutoScrollMargin(5)
        self.RowList_2.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed|QAbstractItemView.SelectedClicked)
        self.RowList_2.setDragEnabled(True)
        self.RowList_2.setDragDropOverwriteMode(True)
        self.RowList_2.setDragDropMode(QAbstractItemView.DragDrop)
        self.RowList_2.setDefaultDropAction(Qt.MoveAction)
        self.RowList_2.setSelectionMode(QAbstractItemView.SingleSelection)
        self.RowList_2.setTextElideMode(Qt.ElideRight)
        self.RowList_2.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.RowList_2.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.RowList_2.setFlow(QListView.LeftToRight)
        self.RowList_2.setProperty("isWrapping", False)
        self.RowList_2.setSpacing(0)
        self.RowList_2.setGridSize(QSize(100, 0))
        self.RowList_2.setViewMode(QListView.ListMode)
        self.RowList_2.setUniformItemSizes(False)
        self.RowList_2.setWordWrap(True)
        self.RowList_2.setSelectionRectVisible(False)
        self.RowList_2.setSortingEnabled(False)

        self.gridLayout_18.addWidget(self.RowList_2, 0, 1, 1, 1)


        self.gridLayout_17.addLayout(self.gridLayout_18, 0, 0, 1, 1)


        self.gridLayout_15.addLayout(self.gridLayout_17, 0, 2, 1, 1)

        self.gridLayout_19 = QGridLayout()
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.DimensionValuesLabel_2 = QLabel(self.chartTab)
        self.DimensionValuesLabel_2.setObjectName(u"DimensionValuesLabel_2")
        sizePolicy9 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.DimensionValuesLabel_2.sizePolicy().hasHeightForWidth())
        self.DimensionValuesLabel_2.setSizePolicy(sizePolicy9)
        self.DimensionValuesLabel_2.setFont(font)

        self.gridLayout_19.addWidget(self.DimensionValuesLabel_2, 0, 0, 1, 1)

        self.FileListDimension_2 = QListWidget(self.chartTab)
        QListWidgetItem(self.FileListDimension_2)
        QListWidgetItem(self.FileListDimension_2)
        QListWidgetItem(self.FileListDimension_2)
        QListWidgetItem(self.FileListDimension_2)
        QListWidgetItem(self.FileListDimension_2)
        self.FileListDimension_2.setObjectName(u"FileListDimension_2")
        sizePolicy10 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.FileListDimension_2.sizePolicy().hasHeightForWidth())
        self.FileListDimension_2.setSizePolicy(sizePolicy10)
        self.FileListDimension_2.setMinimumSize(QSize(0, 100))
        self.FileListDimension_2.setMaximumSize(QSize(16577215, 16777215))
        self.FileListDimension_2.setFocusPolicy(Qt.StrongFocus)
        self.FileListDimension_2.setAcceptDrops(True)
        self.FileListDimension_2.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.FileListDimension_2.setTabKeyNavigation(False)
        self.FileListDimension_2.setDragEnabled(True)
        self.FileListDimension_2.setDragDropOverwriteMode(True)
        self.FileListDimension_2.setDragDropMode(QAbstractItemView.InternalMove)
        self.FileListDimension_2.setDefaultDropAction(Qt.CopyAction)
        self.FileListDimension_2.setBatchSize(100)
        self.FileListDimension_2.setWordWrap(True)
        self.FileListDimension_2.setSortingEnabled(True)

        self.gridLayout_19.addWidget(self.FileListDimension_2, 1, 0, 2, 1)

        self.MeasureValuesLabel_2 = QLabel(self.chartTab)
        self.MeasureValuesLabel_2.setObjectName(u"MeasureValuesLabel_2")
        sizePolicy3.setHeightForWidth(self.MeasureValuesLabel_2.sizePolicy().hasHeightForWidth())
        self.MeasureValuesLabel_2.setSizePolicy(sizePolicy3)
        self.MeasureValuesLabel_2.setFont(font)

        self.gridLayout_19.addWidget(self.MeasureValuesLabel_2, 3, 0, 1, 1)

        self.filterLabel_2 = QLabel(self.chartTab)
        self.filterLabel_2.setObjectName(u"filterLabel_2")
        sizePolicy3.setHeightForWidth(self.filterLabel_2.sizePolicy().hasHeightForWidth())
        self.filterLabel_2.setSizePolicy(sizePolicy3)
        self.filterLabel_2.setMinimumSize(QSize(30, 30))
        self.filterLabel_2.setFont(font)

        self.gridLayout_19.addWidget(self.filterLabel_2, 0, 1, 1, 1)

        self.FileListMes_2 = QListWidget(self.chartTab)
        QListWidgetItem(self.FileListMes_2)
        QListWidgetItem(self.FileListMes_2)
        QListWidgetItem(self.FileListMes_2)
        QListWidgetItem(self.FileListMes_2)
        QListWidgetItem(self.FileListMes_2)
        QListWidgetItem(self.FileListMes_2)
        QListWidgetItem(self.FileListMes_2)
        QListWidgetItem(self.FileListMes_2)
        QListWidgetItem(self.FileListMes_2)
        QListWidgetItem(self.FileListMes_2)
        QListWidgetItem(self.FileListMes_2)
        QListWidgetItem(self.FileListMes_2)
        QListWidgetItem(self.FileListMes_2)
        QListWidgetItem(self.FileListMes_2)
        QListWidgetItem(self.FileListMes_2)
        self.FileListMes_2.setObjectName(u"FileListMes_2")
        sizePolicy11 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.FileListMes_2.sizePolicy().hasHeightForWidth())
        self.FileListMes_2.setSizePolicy(sizePolicy11)
        self.FileListMes_2.setMaximumSize(QSize(16577215, 16777215))
        self.FileListMes_2.setFocusPolicy(Qt.StrongFocus)
        self.FileListMes_2.setAcceptDrops(True)
        self.FileListMes_2.setDragEnabled(True)
        self.FileListMes_2.setDragDropOverwriteMode(True)
        self.FileListMes_2.setDragDropMode(QAbstractItemView.InternalMove)
        self.FileListMes_2.setDefaultDropAction(Qt.CopyAction)
        self.FileListMes_2.setBatchSize(100)
        self.FileListMes_2.setWordWrap(True)
        self.FileListMes_2.setSortingEnabled(True)

        self.gridLayout_19.addWidget(self.FileListMes_2, 4, 0, 1, 1)

        self.filterButton_2 = QPushButton(self.chartTab)
        self.filterButton_2.setObjectName(u"filterButton_2")
        sizePolicy3.setHeightForWidth(self.filterButton_2.sizePolicy().hasHeightForWidth())
        self.filterButton_2.setSizePolicy(sizePolicy3)
        self.filterButton_2.setMinimumSize(QSize(30, 30))

        self.gridLayout_19.addWidget(self.filterButton_2, 0, 2, 1, 1)

        self.filterList_2 = QListWidget(self.chartTab)
        QListWidgetItem(self.filterList_2)
        QListWidgetItem(self.filterList_2)
        QListWidgetItem(self.filterList_2)
        self.filterList_2.setObjectName(u"filterList_2")
        sizePolicy10.setHeightForWidth(self.filterList_2.sizePolicy().hasHeightForWidth())
        self.filterList_2.setSizePolicy(sizePolicy10)
        self.filterList_2.setMinimumSize(QSize(70, 100))
        self.filterList_2.setMaximumSize(QSize(16577215, 16777215))
        self.filterList_2.setAcceptDrops(True)
        self.filterList_2.setDragDropMode(QAbstractItemView.DragDrop)
        self.filterList_2.setDefaultDropAction(Qt.MoveAction)

        self.gridLayout_19.addWidget(self.filterList_2, 1, 1, 2, 2)


        self.gridLayout_15.addLayout(self.gridLayout_19, 0, 0, 1, 1)


        self.gridLayout_20.addLayout(self.gridLayout_15, 0, 0, 1, 1)

        self.tabWidget.addTab(self.chartTab, QString())

        self.gridLayout_7.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 760, 21))
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
        self.saveButton.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.loadButton.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.selectDimentionLabel.setText(QCoreApplication.translate("MainWindow", u"Choose Directory", None))
        self.openDirecButton.setText(QCoreApplication.translate("MainWindow", u"Directory", None))
        self.usedFileLabel.setText(QCoreApplication.translate("MainWindow", u"Union File", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dataSourceTab), QCoreApplication.translate("MainWindow", u"Data Source", None))
        self.chartType.setItemText(0, QCoreApplication.translate("MainWindow", u"New Item5555555555", None))
        self.chartType.setItemText(1, QCoreApplication.translate("MainWindow", u"New Item", None))
        self.chartType.setItemText(2, QCoreApplication.translate("MainWindow", u"New Item", None))
        self.chartType.setItemText(3, QCoreApplication.translate("MainWindow", u"New Item", None))

        self.plotButton.setText(QCoreApplication.translate("MainWindow", u"PLOT", None))
        self.DimensionValuesLabel.setText(QCoreApplication.translate("MainWindow", u"Dimension", None))
        self.MeasureValuesLabel.setText(QCoreApplication.translate("MainWindow", u"Measure Values", None))
        self.filterLabel.setText(QCoreApplication.translate("MainWindow", u"Filter", None))
        self.ColLabel.setText(QCoreApplication.translate("MainWindow", u"Column", None))
        self.RowLabel.setText(QCoreApplication.translate("MainWindow", u"Row", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SheetTab), QCoreApplication.translate("MainWindow", u"Sheet", None))
        self.chartType_2.setItemText(0, QCoreApplication.translate("MainWindow", u"New Item5555555555", None))
        self.chartType_2.setItemText(1, QCoreApplication.translate("MainWindow", u"New Item", None))
        self.chartType_2.setItemText(2, QCoreApplication.translate("MainWindow", u"New Item", None))
        self.chartType_2.setItemText(3, QCoreApplication.translate("MainWindow", u"New Item", None))

        self.plotButton_2.setText(QCoreApplication.translate("MainWindow", u"PLOT", None))

        __sortingEnabled = self.ColList_2.isSortingEnabled()
        self.ColList_2.setSortingEnabled(False)
        ___qlistwidgetitem = self.ColList_2.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qlistwidgetitem1 = self.ColList_2.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"2", None));
        ___qlistwidgetitem2 = self.ColList_2.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow", u"3", None));
        self.ColList_2.setSortingEnabled(__sortingEnabled)

        self.ColLabel_2.setText(QCoreApplication.translate("MainWindow", u"Column", None))
        self.RowLabel_2.setText(QCoreApplication.translate("MainWindow", u"Row", None))

        __sortingEnabled1 = self.RowList_2.isSortingEnabled()
        self.RowList_2.setSortingEnabled(False)
        ___qlistwidgetitem3 = self.RowList_2.item(0)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("MainWindow", u"1111111111", None));
        ___qlistwidgetitem4 = self.RowList_2.item(1)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("MainWindow", u"2", None));
        ___qlistwidgetitem5 = self.RowList_2.item(2)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("MainWindow", u"3", None));
        self.RowList_2.setSortingEnabled(__sortingEnabled1)

        self.DimensionValuesLabel_2.setText(QCoreApplication.translate("MainWindow", u"Dimension", None))

        __sortingEnabled2 = self.FileListDimension_2.isSortingEnabled()
        self.FileListDimension_2.setSortingEnabled(False)
        ___qlistwidgetitem6 = self.FileListDimension_2.item(0)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("MainWindow", u"2", None));
        ___qlistwidgetitem7 = self.FileListDimension_2.item(1)
        ___qlistwidgetitem7.setText(QCoreApplication.translate("MainWindow", u"5", None));
        ___qlistwidgetitem8 = self.FileListDimension_2.item(2)
        ___qlistwidgetitem8.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem9 = self.FileListDimension_2.item(3)
        ___qlistwidgetitem9.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem10 = self.FileListDimension_2.item(4)
        ___qlistwidgetitem10.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        self.FileListDimension_2.setSortingEnabled(__sortingEnabled2)

        self.MeasureValuesLabel_2.setText(QCoreApplication.translate("MainWindow", u"Measure Values", None))
        self.filterLabel_2.setText(QCoreApplication.translate("MainWindow", u"Filter", None))

        __sortingEnabled3 = self.FileListMes_2.isSortingEnabled()
        self.FileListMes_2.setSortingEnabled(False)
        ___qlistwidgetitem11 = self.FileListMes_2.item(0)
        ___qlistwidgetitem11.setText(QCoreApplication.translate("MainWindow", u"10", None));
        ___qlistwidgetitem12 = self.FileListMes_2.item(1)
        ___qlistwidgetitem12.setText(QCoreApplication.translate("MainWindow", u"5", None));
        ___qlistwidgetitem13 = self.FileListMes_2.item(2)
        ___qlistwidgetitem13.setText(QCoreApplication.translate("MainWindow", u"9", None));
        ___qlistwidgetitem14 = self.FileListMes_2.item(3)
        ___qlistwidgetitem14.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem15 = self.FileListMes_2.item(4)
        ___qlistwidgetitem15.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem16 = self.FileListMes_2.item(5)
        ___qlistwidgetitem16.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem17 = self.FileListMes_2.item(6)
        ___qlistwidgetitem17.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem18 = self.FileListMes_2.item(7)
        ___qlistwidgetitem18.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem19 = self.FileListMes_2.item(8)
        ___qlistwidgetitem19.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem20 = self.FileListMes_2.item(9)
        ___qlistwidgetitem20.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem21 = self.FileListMes_2.item(10)
        ___qlistwidgetitem21.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem22 = self.FileListMes_2.item(11)
        ___qlistwidgetitem22.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem23 = self.FileListMes_2.item(12)
        ___qlistwidgetitem23.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem24 = self.FileListMes_2.item(13)
        ___qlistwidgetitem24.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem25 = self.FileListMes_2.item(14)
        ___qlistwidgetitem25.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        self.FileListMes_2.setSortingEnabled(__sortingEnabled3)

        self.filterButton_2.setText(QCoreApplication.translate("MainWindow", u" Filter ", None))

        __sortingEnabled4 = self.filterList_2.isSortingEnabled()
        self.filterList_2.setSortingEnabled(False)
        ___qlistwidgetitem26 = self.filterList_2.item(0)
        ___qlistwidgetitem26.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem27 = self.filterList_2.item(1)
        ___qlistwidgetitem27.setText(QCoreApplication.translate("MainWindow", u"22", None));
        ___qlistwidgetitem28 = self.filterList_2.item(2)
        ___qlistwidgetitem28.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        self.filterList_2.setSortingEnabled(__sortingEnabled4)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.chartTab), QCoreApplication.translate("MainWindow", u"Chart", None))
    # retranslateUi


from email import header
from msilib.schema import Class
from operator import mod
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QChart, QChartView, QBarSet, QPercentBarSeries, QBarCategoryAxis, QLineSeries
import numpy as np
import pandas as pd
from io import StringIO
from Altair_Graph.Bar_Chart import WebEngineView
import csvManager
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QPointF
from PyQt5 import QtCore, QtGui, QtWidgets , QtChart ,QtWebEngineWidgets
from PyQt5.QtChart import QChart
from PyQt5.QtGui import QPainter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import altair as alt
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtChart import QChart, QChartView, QHorizontalBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
#from qgis.PyQt.QtWidgets import QVBoxLayout
cm = csvManager.csvManager()
class WebEngineView(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.page().profile().downloadRequested.connect(self.onDownloadRequested)
        self.windows = []

    @QtCore.pyqtSlot(QtWebEngineWidgets.QWebEngineDownloadItem)
    def onDownloadRequested(self, download):
        if (
            download.state()
            == QtWebEngineWidgets.QWebEngineDownloadItem.DownloadRequested
        ):
            path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, self.tr("Save as"), download.path()
            )
            if path:
                download.setPath(path)
                download.accept()

    def createWindow(self, type_):
        if type_ == QtWebEngineWidgets.QWebEnginePage.WebBrowserTab:
            window = QtWidgets.QMainWindow(self)
            view = QtWebEngineWidgets.QWebEngineView(window)
            window.resize(640, 480)
            window.setCentralWidget(view)
            window.show()
            return view

    def updateChart(self, chart, **kwargs):
        output = StringIO()
        chart.save(output, "html", **kwargs)
        self.setHtml(output.getvalue())
        
class TableModel2(QtCore.QAbstractTableModel):
    data = ""
    def __init__(self, data):
        super(TableModel2, self).__init__()
        #self.itemClicked.connect(self.handleItemClick)
        self._data = data
        #Ui_MainWindow.connectButton()

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role): #show Header on column
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal: #x
                if type(self._data.columns[section]) == tuple:
                    colN =str(list(self._data.columns[section])[0])
                else: colN = self._data.columns[section]
                return colN
                
            if orientation == Qt.Vertical: #y
                if type(self._data.index[section]) == tuple:
                    indexN = str(list(self._data.index[section])[0])
                else: indexN = self._data.index[section]
                return indexN
                
class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        #self.itemClicked.connect(self.handleItemClick)
        self._data = data
        
    def data(self, index, role): 
        if role == Qt.DisplayRole:
            #print(">", len(self._data))
            value = self._data.iloc[index.row(), index.column()]
            #print("----",value)
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role): #show Header on column
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal: #x
                return self._data.columns[section]

            '''if orientation == Qt.Vertical: #y
                return ''.join(self._data.index[section])'''
                
'''class ColLis(object):
    def __init__(self, *args):
        super(ClassName, self).__init__(*args))'''
        
class Ui_MainWindow(object):
    def __init__(self,MainWindow):
        super().__init__()
        #dragDropFinished = QtCore.pyqtSignal()
        self.folderpath = ''
        self.fileNameList = []
        self.selectFile = []
        self.colHeader = []
        self.Measure = ['Sales', 'Quantity', 'Discount', 'Profit']
        self.path = ""
        self.RowChoose = []
        self.ColChoose = []
        self.dataSheet = ""
        #DimenForChoose = []
        self.setupUi(MainWindow)
                
    def DropDup(self):
        itemsTextList =  [str(self.RowList.item(i).text()) for i in range(self.RowList.count())]
        self.RowChoose = itemsTextList
        itemsTextList =  [str(self.ColList.item(i).text()) for i in range(self.ColList.count())]
        self.ColChoose = itemsTextList
        itemsTextList =  [str(self.FileListDimension.item(i).text()) for i in range(self.FileListDimension.count())]
        itemsTextList = list(dict.fromkeys(itemsTextList))
        self.colHeader = itemsTextList
        '''print(self.RowChoose,self.ColChoose)
        print(self.selectFile)'''
        Ui_MainWindow.retranslateUi(self, MainWindow)
        
    def updateList(self):
        #self.__init__(MainWindow)
        itemsTextList =  [str(self.FileListChoose.item(i).text()) for i in range(self.FileListChoose.count())]
        self.selectFile = itemsTextList
        itemsTextList =  [str(self.FileList.item(i).text()) for i in range(self.FileList.count())]
        self.fileNameList = itemsTextList
        self.RowChoose = []
        self.ColChoose = []
        if self.selectFile != []:
            self.colHeader = cm.getHead()
        else: self.colHeader = []
        self.dataSource()
        Ui_MainWindow.setupUi(self, MainWindow)
        
    def launchDialog(self):
        file_filter = 'Excel File (*.xlsx *.csv *.xls)'
        response = QFileDialog.getOpenFileName(
            #parent=self,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Excel File (*.xlsx *.xls *.csv)' #defult filter
        )
        self.selectFile = response
        self.folderpath = os.getcwd()
        filename = os.listdir(self.folderpath)
        tmp = []
        for i in filename:
            if i.endswith(".xls") or i.endswith(".csv") or i.endswith(".xlsx"):
                tmp.append(i)
        self.selectFile = list(self.selectFile)
        self.selectFile = self.selectFile[0].split("/")[-1]
        tmp.remove(self.selectFile)
        #print(tmp)
        self.fileNameList = tmp
        self.path = self.folderpath+"/"+self.selectFile
        cm.path = self.folderpath
        cm.selectFile = self.selectFile
        cm.setPath()
        #print(cm.df)
        self.colHeader = cm.getHead()
        for i in self.Measure:
            if i in self.colHeader:
                self.colHeader.remove(i)
        Ui_MainWindow.setupUi(self, MainWindow)
        
    def RowDelect(self,item):
        if len(self.RowChoose) != 0:
            row = self.RowList.currentRow()
            self.RowList.takeItem(row)
            
    def ColDelect(self,item):
        if len(self.ColChoose) != 0:
            Col = self.ColList.currentRow()
            self.ColList.takeItem(Col)
            
    def plot(self):
        tmp = []
        tmp =  [str(self.RowList.item(i).text()) for i in range(self.RowList.count())]
        self.RowChoose = tmp
        tmp = [] 
        tmp =  [str(self.ColList.item(i).text()) for i in range(self.ColList.count())]
        self.ColChoose = tmp
        if self.ColChoose != [] or self.RowChoose != [] :
            self.sheetPageRowAndCol(self.RowChoose,self.ColChoose)
            self.model = TableModel2(self.dataSheet)
            self.sheetTable.setModel(self.model)
            #self.creatSheet()
            '''self.sheetPageRowAndCol(self.RowChoose,self.ColChoose)
            self.creatSheet()'''
        #print(self.dataSheet)
        #Ui_MainWindow.setupUi(self, MainWindow)
        
    def dataSource(self):
        #print(self.selectFile)
        if type(self.selectFile) != list:
            self.selectFile = [self.selectFile]
        if self.selectFile != [] :
            if len(self.selectFile)>1:
                print("Union")
                self.data = cm.unionFile(self.selectFile)
            else:
                print("Not Union")
                cm.path =self.folderpath
                cm.selectFile = self.selectFile[0] 
                cm.setPath()
                self.data = cm.getDataWithPandas()
            #print(self.data)

    def dataSourceSort(self,dimension):
        self.data = cm.setAllDataByOneDimension(dimension)
        
    def sheetPageRow(self):
        self.dataSheet = cm.setDimensionSort(self.RowChoose)
        if self.RowChoose[-1] not in self.Measure :
            self.dataSheet[" "] = "abc"
        else:
            self.dataSheet[" "] = "abc"
                
    def sheetPageCol(self):
        tmp = cm.setDimensionSort(self.ColChoose)
        tmp[" "] = "abc"
        self.dataSheet = tmp.T
    
    MeasureChoose = ""
    def sheetPageRowAndCol(self,Row,Col):
        print("Start",Row,Col,len(set(Row)),len(set(Col)))
        while (Row.count('')):
            Row.remove('')
        while (Col.count('')):
            Col.remove('')
        print("Start",Row,Col,len(set(Row)),len(set(Col)))
        if len(set(Col)) == 0 : 
            print("Row")
            self.sheetPageRow()
            if Row[-1] in self.Measure:
                self.MeasureChoose = Row[-1]
                self.VerBar()
                self.plotChart()
        elif len(set(Row)) == 0:
            print("Col") 
            self.sheetPageCol()
            if Col[-1] in self.Measure:
                self.MeasureChoose = Col[-1]
                self.HonBar()
                self.plotChart()
        else : 
            print("Row and Col")
            self.dataSheet = cm.setRowAndColumn(Row,Col)
    
    def VerBar(self):
        Measure = self.MeasureChoose
        Di1 = self.RowChoose[0]
        Di2 = 'State'
        c = alt.Chart(self.data).mark_bar().encode(
        x=str(Di1+':N'),
        y=str(Measure+':Q')
        ).facet(row=str(Di1+':N')
        )
        self.Chart = c
    
        '''view = WebEngineView(self.tab_2)
        view.setGeometry(QtCore.QRect(200, 90, 581, 421))
        view.updateChart(c)
        view.show()'''
    
    def HonBar(self):
        Measure = self.MeasureChoose
        Di1 = self.ColChoose[0]
        Di2 = 'State'
        c = alt.Chart(self.data).mark_bar().encode(
        y=str(Di1+':N'),
        x=str(Measure+':Q')
        ).facet(column=str(Di1+':N')
        ).resolve_scale(y = 'independent')
        self.Chart = c

        '''view = WebEngineView(self.tab_2)
        view.setGeometry(QtCore.QRect(200, 90, 581, 401))
        view.updateChart(c)
        view.show()'''
        #MainWindow.setCentralWidget(view)
        #w.resize(640, 480)
    def plotChart(self):
        view = WebEngineView(self.tab_2)
        view.setGeometry(QtCore.QRect(200, 90, 581, 401))
        view.updateChart(self.Chart)
        view.show()

    def plotLineChart(self):
        self.data['Order Date'] = pd.to_datetime(self.data['Order Date'],format='%d/%m/%Y')
        self.data['Ship Date'] = pd.to_datetime(self.data['Ship Date'],format='%d/%m/%Y')
        col = self.ColChoose[0]
        row = self.RowChoose[0]
        fil11 = 'month'
        fil22 = 'sum'
        if col in self.Measure:
            colN = str(fil22+'('+col+'):Q')
        else:
            colN = str(fil11+'('+col+'):T')

        if row in self.Measure:
            rowN = str(fil22+'('+row+'):Q')
        else:
            rowN = str(fil11+'('+row+'):T')

        chart = alt.Chart(self.data).mark_line(point=True).encode(
        alt.X(colN),
        alt.Y(rowN)#,
        #tooltip = str(fil22+'('+Measua+'):Q') 
        )
        return chart
    
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        
        self.tabWidget.setGeometry(QtCore.QRect(4, 0, 791, 571))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        
        self.table = QtWidgets.QTableView(self.tab)
        self.table.setGeometry(QtCore.QRect(190, 10, 591, 471))
        self.dataSource()
        if self.selectFile != [] : 
            self.model = TableModel(self.data)
            self.table.setModel(self.model)

        self.selectFileLabel = QtWidgets.QLabel(self.tab)
        self.selectFileLabel.setGeometry(QtCore.QRect(10, 11, 131, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selectFileLabel.setFont(font)
        self.selectFileLabel.setObjectName("selectFileLabel")
        
        self.usedFile = QtWidgets.QLabel(self.tab)
        self.usedFile.setGeometry(QtCore.QRect(10, 280, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.usedFile.setFont(font)
        self.usedFile.setObjectName("usedFile")
        
        self.selectFileButton = QtWidgets.QPushButton(self.tab)
        self.selectFileButton.setGeometry(QtCore.QRect(142, 10, 41, 28))
        self.selectFileButton.setObjectName("selectFileButton")
        self.selectFileButton.clicked.connect(self.launchDialog)
        
        self.usedFileButton = QtWidgets.QPushButton(self.tab)
        self.usedFileButton.setGeometry(QtCore.QRect(142, 275, 41, 28))
        self.usedFileButton.setObjectName("selectFileButton")
        self.usedFileButton.clicked.connect(self.updateList)
        
        self.FileList = QtWidgets.QListWidget(self.tab)
        self.FileList.setGeometry(QtCore.QRect(10, 50, 171, 221))
        self.FileList.setAcceptDrops(True)
        self.FileList.setDragEnabled(True)
        self.FileList.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.FileList.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.FileList.setProperty("isWrapping", True)
        self.FileList.setWordWrap(True)
        self.FileList.setObjectName("FileList")
        
        if self.fileNameList != []:
            for i in range(len(self.fileNameList)):
                item = QtWidgets.QListWidgetItem()
                #print(self.fileNameList)
                self.FileList.addItem(item)
        
        self.FileListChoose = QtWidgets.QListWidget(self.tab)
        self.FileListChoose.setGeometry(QtCore.QRect(10, 310, 171, 171))
        self.FileListChoose.setAcceptDrops(True)
        self.FileListChoose.setDragEnabled(True)
        self.FileListChoose.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.FileListChoose.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.FileListChoose.setWordWrap(True)
        self.FileListChoose.setObjectName("FileListChoose")
        #print(self.FileListChoose.item)
        for i in range(len(self.selectFile)):
            item = QtWidgets.QListWidgetItem()
            self.FileListChoose.addItem(item)
        self.tabWidget.addTab(self.tab, "Data Source")
        
        self.saveButton = QtWidgets.QPushButton(self.tab)
        self.saveButton.setGeometry(QtCore.QRect(600, 490, 93, 28))
        self.saveButton.setObjectName("saveButton")
        
        self.loadButton = QtWidgets.QPushButton(self.tab)
        self.loadButton.setGeometry(QtCore.QRect(700, 490, 83, 28))
        self.loadButton.setObjectName("loadButton")

        #Tab2
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        
        self.ColLabel = QtWidgets.QLabel(self.tab_2)
        self.ColLabel.setGeometry(QtCore.QRect(200, 55, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ColLabel.setFont(font)
        self.ColLabel.setObjectName("ColLabel")
        
        self.DimensionValuesLabel = QtWidgets.QLabel(self.tab_2)
        self.DimensionValuesLabel.setGeometry(QtCore.QRect(13, 16, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.DimensionValuesLabel.setFont(font)
        self.DimensionValuesLabel.setObjectName("DimensionValuesLabel")
        
        self.FileListDimension = QtWidgets.QListWidget(self.tab_2)
        self.FileListDimension.setGeometry(QtCore.QRect(10, 40, 181, 291))
        self.FileListDimension.setAcceptDrops(True)
        self.FileListDimension.setDragEnabled(True)
        self.FileListDimension.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.FileListDimension.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.FileListDimension.setWordWrap(True)
        self.FileListDimension.setObjectName("FileList")
        for i in range(len(self.colHeader)):
            item = QtWidgets.QListWidgetItem()
            self.FileListDimension.addItem(item)
        self.FileListDimension.clicked.connect(self.DropDup)
        
        self.MeasureValuesLabel = QtWidgets.QLabel(self.tab_2)
        self.MeasureValuesLabel.setGeometry(QtCore.QRect(10, 337, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.MeasureValuesLabel.setFont(font)
        self.MeasureValuesLabel.setObjectName("MeasureValuesLabel")
        
        self.FileListMes = QtWidgets.QListWidget(self.tab_2)
        self.FileListMes.setGeometry(QtCore.QRect(10, 360, 181, 151))
        self.FileListMes.setAcceptDrops(True)
        self.FileListMes.setDragEnabled(True)
        self.FileListMes.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.FileListMes.setDragDropOverwriteMode(True)
        self.FileListMes.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.FileListMes.setWordWrap(True)
        self.FileListMes.setObjectName("FileListMes")
        for i in range(len(self.Measure)):
            item = QtWidgets.QListWidgetItem()
            self.FileListMes.addItem(item)
        self.FileListDimension.clicked.connect(self.DropDup)
        
        self.RowList = QtWidgets.QListWidget(self.tab_2)
        #self.RowListW = RowListWidget()
        #self.RowListW.setGeometry(QtCore.QRect(260, 10, 491, 31))
        self.RowList.setGeometry(QtCore.QRect(260, 10, 491, 31))
        self.RowList.setAcceptDrops(True)
        self.RowList.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.RowList.setAutoFillBackground(True)
        self.RowList.setDragEnabled(True)
        self.RowList.setDragDropOverwriteMode(True)
        self.RowList.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.RowList.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.RowList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.RowList.setFlow(QtWidgets.QListView.LeftToRight)
        self.RowList.setObjectName("RowList")
        for i in range(len(self.RowChoose)):
            item = QtWidgets.QListWidgetItem()
            self.RowList.addItem(item)
            #self.RowList.setModel(self.RowListW)
        self.RowList.itemDoubleClicked.connect(self.RowDelect)
        #self.RowList.clicked.connect(self.DropDup)
        
        self.RowLabel = QtWidgets.QLabel(self.tab_2)
        self.RowLabel.setGeometry(QtCore.QRect(200, 10, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.RowLabel.setFont(font)
        self.RowLabel.setObjectName("RowLabel")
        
        '''self.ColDell = QtWidgets.QPushButton(self.tab_2)
        self.ColDell.setGeometry(QtCore.QRect(750, 50, 31, 31))
        self.ColDell.setObjectName("ColDell")
        self.ColDell.clicked.connect(self.ColDelect)
        
        self.RowDell = QtWidgets.QPushButton(self.tab_2)
        self.RowDell.setGeometry(QtCore.QRect(750, 10, 31, 31))
        self.RowDell.setObjectName("RowDell")
        self.RowDell.clicked.connect(self.RowDelect)'''
        
        self.ColList = QtWidgets.QListWidget(self.tab_2)
        self.ColList.setGeometry(QtCore.QRect(260, 50, 491, 31))
        self.ColList.setAcceptDrops(True)
        self.ColList.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.ColList.setAutoFillBackground(True)
        self.ColList.setDragEnabled(True)
        self.ColList.setDragDropOverwriteMode(True)
        self.ColList.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.ColList.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.ColList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ColList.setFlow(QtWidgets.QListView.LeftToRight)
        self.ColList.setObjectName("ColList")
        for i in range(len(self.ColChoose)):
            item = QtWidgets.QListWidgetItem()
            self.ColList.addItem(item)
        self.ColList.itemDoubleClicked.connect(self.ColDelect)
        
        self.sheetTable = QtWidgets.QTableView(self.tab_2)
        self.sheetTable.setGeometry(QtCore.QRect(200, 90, 581, 421))
        
        '''self.sheetTableW = QtWidgets.QTableWidget(self.tab_2)
        self.sheetTableW.setGeometry(QtCore.QRect(200, 90, 581, 421))
        '''
        self.plotButton = QtWidgets.QPushButton(self.tab_2)
        self.plotButton.setGeometry(QtCore.QRect(730, 510, 41, 31))
        self.plotButton.setObjectName("plotButton")
        self.plotButton.clicked.connect(self.plot)
            
        self.tabWidget.addTab(self.tab_2, "Sheet")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        fileSelectName = "Choose File"
        if self.selectFile != []: fileSelectName = self.selectFile[0]
        #print(fileSelectName)
        
        self.selectFileLabel.setText(_translate("MainWindow", fileSelectName))
        self.usedFile.setText(_translate("MainWindow", "Used File"))
        
        self.usedFileButton.setText(_translate("MainWindow", "Use"))
        self.selectFileButton.setText(_translate("MainWindow", "File"))
        
        #if self.selectFile in self.fileNameList :
        self.FileList.setSortingEnabled(True)
        __sortingEnabled = self.FileList.isSortingEnabled()
        self.FileList.setSortingEnabled(False)
        
        for i,j in zip(range(len(self.fileNameList)),self.fileNameList):
            #print(i,j)
            item = self.FileList.item(i)
            item.setText(_translate("MainWindow", str(j)))
        self.FileList.setSortingEnabled(__sortingEnabled)
        
        self.FileListChoose.setSortingEnabled(True)
        __sortingEnabled = self.FileListChoose.isSortingEnabled()
        self.FileListChoose.setSortingEnabled(False)
        for i,j in zip(range(len(set(self.selectFile))),set(self.selectFile)):
            item = self.FileListChoose.item(i)
            item.setText(_translate("MainWindow", str(j)))
        
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.loadButton.setText(_translate("MainWindow", "Load"))
        
        #tab 2
        self.DimensionValuesLabel.setText(_translate("MainWindow", "Dimension"))
        
        self.FileList.setSortingEnabled(True)
        __sortingEnabled = self.FileListDimension.isSortingEnabled()
        self.FileList.setSortingEnabled(False)
        for i,j in zip(range(len(self.colHeader)),self.colHeader):
            item = self.FileListDimension.item(i)
            item.setText(_translate("MainWindow", str(j)))
        self.FileListDimension.setSortingEnabled(__sortingEnabled)
        
        self.MeasureValuesLabel.setText(_translate("MainWindow", "Measure Values"))
        
        self.FileListMes.setSortingEnabled(True)
        __sortingEnabled = self.FileListMes.isSortingEnabled()
        self.FileListMes.setSortingEnabled(False)
        for i,j in zip(range(len(self.Measure)),self.Measure):
            item = self.FileListMes.item(i)
            item.setText(_translate("MainWindow", str(j)))
        self.FileListMes.setSortingEnabled(__sortingEnabled)
        
        for i,j in zip(range(len(self.ColChoose)),self.ColChoose):
            item = self.ColList.item(i)
            item.setText(_translate("MainWindow", str(j)))
        
        for i,j in zip(range(len(self.RowChoose)),self.RowChoose):
            item = self.RowList.item(i)
            item.setText(_translate("MainWindow", str(j)))
        
        self.ColLabel.setText(_translate("MainWindow", "Column"))
        self.RowLabel.setText(_translate("MainWindow", "Row"))
        
        #self.ColDell.setText(_translate("MainWindow", "DEL"))
        #self.RowDell.setText(_translate("MainWindow", "DEL"))
                    
        self.plotButton.setText(_translate("MainWindow", "PLOT"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    #ui.setupUi(MainWindow)
    MainWindow.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')

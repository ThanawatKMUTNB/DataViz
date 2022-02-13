from email import header
from msilib.schema import Class
from operator import mod
import filterDimen
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QEvent,Qt
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QChart, QChartView, QBarSet, QPercentBarSeries, QBarCategoryAxis, QLineSeries
import numpy as np
import pandas as pd
from io import StringIO
from Altair_Graph.Bar_Chart import WebEngineView
import csvManager as cmpage
import filterMes
import filterDimen
from PyQt5.QtCore import Qt, QPointF
from PyQt5 import QtCore, QtGui, QtWidgets , QtChart ,QtWebEngineWidgets
from PyQt5.QtChart import QChart
from PyQt5.QtGui import QPainter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import altair as alt
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtChart import QChart, QChartView, QHorizontalBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
#from qgis.PyQt.QtWidgets import QVBoxLayout
#from altair import pipe, limit_rows, to_values
import altair_viewer
import graphManager 

'''t = lambda data: pipe(data, limit_rows(max_rows=10000), to_values)
alt.data_transformers.register('custom', t)
alt.data_transformers.enable('custom')'''
alt.data_transformers.disable_max_rows()
altair_viewer._global_viewer._use_bundled_js = False
alt.data_transformers.enable('data_server')

#cm = cmpage.csvManager()
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
        #print(data)
        #Ui_MainWindow.connectButton()

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            #print("Value ",value)
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
                    head = self._data.columns.names
                    head = [ "%s" % x for x in list(head) ]
                    if len(head) > 1 :head = ["\\".join(head)]
                    colN = [ "%s" % x for x in list(self._data.columns[section]) ]
                    colN = "\n".join(colN)
                else: 
                    colN = str(self._data.columns[section])
                return colN
                
            if orientation == Qt.Vertical: #y
                if type(self._data.index[section]) == tuple:
                    head = self._data.index.names
                    head = [ "%s" % x for x in list(head) ]
                    if len(head) > 1 :head = ["\\".join(head)]
                    indexN = [ "%s" % x for x in list(self._data.index[section]) ]
                    indexN = " ".join(indexN)
                else: 
                    indexN = str(self._data.index[section])
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
        self.typeChart = ['Line', 'Bar', 'Pie']
        self.Chart = None
        self.filDic = {}
        self.chartTypeS = ''
        self.setupUi(MainWindow)
        #DimenForChoose = []
    def filChange(self):
        itemsTextList =  [str(self.filterList.item(i).text()) for i in range(self.filterList.count())]
        self.filterList_2.clear()
        for j in itemsTextList:
            self.filterList_2.addItem(j)
            # print(j)
            self.filDic[j] = cm.getDataWithPandasByHead(j).drop_duplicates().to_list()
            # self.filDic = dict.fromkeys(itemsTextList, "")
            # print(self.filDic)
        
    def filChange_2(self):
        itemsTextList =  [str(self.filterList_2.item(i).text()) for i in range(self.filterList_2.count())]
        self.filterList.clear()
        for j in itemsTextList:
            self.filterList.addItem(j)
            # print(j)
            self.filDic[j] = cm.getDataWithPandasByHead(j).drop_duplicates().to_list()
            # self.filDic = dict.fromkeys(itemsTextList, "")
            # print(self.filDic)
            
    def openFilterPage(self):
        # print(self.data)
        filterItem = self.filterList.currentRow()
        strItem = self.filterList.item(filterItem)
        self.Window = QtWidgets.QMainWindow()
        if strItem in self.Measure :
            self.uiM = filterMes.Ui_MainWindowM()
            self.uiM.setupUi(self.Window)
            #fp.setupUi(filPage)
        else :
            fd = filterDimen.Ui_MainWindow()
            # fd.reffil = self.data
            fd.setStart(strItem.text(),self.filDic,self.data)
            fd.setupUi(self.Window)
            self.Window.show()
            #fp.setupUi(filPage)
    
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
        self.path = os.path.join(self.folderpath,self.selectFile) 
        # self.path = self.folderpath+"/"+self.selectFile
        cm.path = self.folderpath
        cm.selectFile = self.selectFile
        cm.setPath()
        #print(cm.self.data)
        self.colHeader = cm.getHead()
        for i in self.Measure:
            if i in self.colHeader:
                self.colHeader.remove(i)
        Ui_MainWindow.setupUi(self, MainWindow)
        
    def fillDel_2(self):
        cur = self.filterList_2.currentRow()
        self.filterList_2.takeItem(cur)
        self.filChange_2()
        
    def fillDel(self):
        cur = self.filterList.currentRow()
        self.filterList.takeItem(cur)
        self.filChange()
            
    def RowDelect_2(self,item):
        if len(self.RowChoose) != 0:
            row_2 = self.RowList_2.currentRow()
            self.RowList_2.takeItem(row_2)
            tmp = []
            tmp =  [str(self.RowList_2.item(i).text()) for i in range(self.RowList_2.count())]
            self.RowChoose = tmp
            tmp = [] 
            tmp =  [str(self.ColList_2.item(i).text()) for i in range(self.ColList_2.count())]
            self.ColChoose = tmp
            self.plot()
            
    def RowDelect(self,item):
        if len(self.RowChoose) != 0:
            row = self.RowList.currentRow()
            self.RowList.takeItem(row)
            tmp = []
            tmp =  [str(self.RowList.item(i).text()) for i in range(self.RowList.count())]
            self.RowChoose = tmp
            tmp = [] 
            tmp =  [str(self.ColList.item(i).text()) for i in range(self.ColList.count())]
            self.ColChoose = tmp
            self.plot()
    
    def ColDelect_2(self,item):
        if len(self.ColChoose) != 0:
            Col_2 = self.ColList_2.currentRow()
            self.ColList_2.takeItem(Col_2)
            tmp = []
            tmp =  [str(self.RowList_2.item(i).text()) for i in range(self.RowList_2.count())]
            self.RowChoose = tmp
            tmp = [] 
            tmp =  [str(self.ColList_2.item(i).text()) for i in range(self.ColList_2.count())]
            self.ColChoose = tmp
            self.plot()
        
    def ColDelect(self,item):
        if len(self.ColChoose) != 0:
            Col = self.ColList.currentRow()
            self.ColList.takeItem(Col)
            tmp = []
            tmp =  [str(self.RowList.item(i).text()) for i in range(self.RowList.count())]
            self.RowChoose = tmp
            tmp = []
            tmp =  [str(self.ColList.item(i).text()) for i in range(self.ColList.count())]
            self.ColChoose = tmp
            self.plot()
            
    def setplot_2(self):
        tmp = []
        tmp =  [str(self.RowList_2.item(i).text()) for i in range(self.RowList_2.count())]
        self.RowChoose = tmp
        tmp = [] 
        tmp =  [str(self.ColList_2.item(i).text()) for i in range(self.ColList_2.count())]
        self.ColChoose = tmp
        self.chartTypeS = self.chartType_2.currentText()
        # print(self.chartTypeS)
        self.plot()
        
    def setplot(self):
        #print("--------",self.RowChoose,self.ColChoose)
        tmp = []
        tmp =  [str(self.RowList.item(i).text()) for i in range(self.RowList.count())]
        self.RowChoose = tmp
        tmp = [] 
        tmp =  [str(self.ColList.item(i).text()) for i in range(self.ColList.count())]
        self.ColChoose = tmp
        
        self.chartTypeS = self.chartType.currentText()
        # print(self.chartTypeS)
        #print("--------",self.RowChoose,self.ColChoose)
        self.plot()
        
    def plot(self):
        while (self.RowChoose.count('')):
            self.RowChoose.remove('')
        while (self.ColChoose.count('')):
            self.ColChoose.remove('')
            
        isInterRow = list(set.intersection(set(self.RowChoose),set(self.Measure)))
        isInterCol = list(set.intersection(set(self.ColChoose),set(self.Measure)))
        # print("--------",self.RowChoose,self.ColChoose)
        print(str(self.chartTypeS))
        
        if  isInterRow != [] or isInterCol != []:
            # print(self.chartType.currentText())
            if isInterRow != [] and isInterCol == []:
                gm = graphManager.graphManager()
                '''for i in isInterRow:
                    self.RowChoose.remove(i)
                self.ColChoose = self.ColChoose + isInterRow'''
                gm.setList(self.RowChoose,self.ColChoose,self.data)
                self.Chart = gm.chooseChart(str(self.chartTypeS))
                    #self.RowList.addItems(self.RowChoose)
                    #self.ColList.addItems(self.ColChoose)
                    #self.tab3(MainWindow)
            
            if isInterRow == [] and isInterCol != []:
                gm = graphManager.graphManager()
                '''for i in isInterCol:
                    self.ColChoose.remove(i)
                self.RowChoose = self.RowChoose + isInterCol'''
                gm.setList(self.RowChoose,self.ColChoose,self.data)
                self.Chart = gm.chooseChart(str(self.chartTypeS))
                    #self.RowList.addItems(self.RowChoose)
                    #self.ColList.addItems(self.ColChoose)
                    #self.tab3(MainWindow)
        self.tab2(MainWindow)
        self.tab3(MainWindow)
        
        if self.ColChoose != [] or self.RowChoose != [] :
            #print(self.dataSheet)
            self.sheetPageRowAndCol(self.RowChoose,self.ColChoose)
            self.model = TableModel2(self.dataSheet)
            self.sheetTable.setModel(self.model)
        
        if self.ColChoose == [] and self.RowChoose == [] :
            self.sheetTable.reset()
            self.sheetTable.setModel(None)
            
    def dataSource(self):
        # print(self.selectFile)
        if type(self.selectFile) != list:
            self.selectFile = [self.selectFile]
        # print(self.selectFile)
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
    
    MeasureChoose = ""
    def sheetPageRowAndCol(self,Row,Col):
        print("Start",Row,Col,len(set(Row)),len(set(Col)))
        while (Row.count('')):
            Row.remove('')
        while (Col.count('')):
            Col.remove('')
        print("Start",Row,Col,len(set(Row)),len(set(Col)))
        '''if len(set(Col)) == 0 : 
            print("Row")
            self.sheetPageRow()
            if Row[-1] in self.Measure:
                self.MeasureChoose = Row[-1]
                #self.plotBarChart()
        elif len(set(Row)) == 0:
            print("Col") 
            self.sheetPageCol()
            if Col[-1] in self.Measure:
                self.MeasureChoose = Col[-1]
                #self.plotBarChart()
        else : 
            print("Row and Col")
            #self.plotLineChart()'''
        if Row!=[] or Col!=[]:
            self.dataSheet = cm.setRowAndColumn(Row,Col)

    def on_header_doubleClicked(self,index):
        #headCur = index
        self.data = cm.setAllDataByOneDimension(self.colHeader[index])
        self.model = TableModel(self.data)
        self.table.setModel(self.model)
        
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.gridLayout_7 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_7.setObjectName("gridLayout_7")
        
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        #self.tabWidget.setGeometry(QtCore.QRect(4, 0, 791, 571))
        self.tabWidget.setObjectName("tabWidget")
        
        # self.tab = QtWidgets.QWidget()
        # self.tab.setObjectName("tab")
        
        self.dataSourceTab = QtWidgets.QWidget()
        self.dataSourceTab.setObjectName("dataSourceTab")
        
        self.gridLayout_6 = QtWidgets.QGridLayout(self.dataSourceTab)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        
        self.saveButton = QtWidgets.QPushButton(self.dataSourceTab)
        self.saveButton.setObjectName("saveButton")
        
        self.gridLayout_5.addWidget(self.saveButton, 0, 1, 1, 1)
        
        self.loadButton = QtWidgets.QPushButton(self.dataSourceTab)
        self.loadButton.setObjectName("loadButton")
        
        self.gridLayout_5.addWidget(self.loadButton, 0, 2, 1, 1)
        
        spacerItem = QtWidgets.QSpacerItem(700, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        
        self.gridLayout_5.addItem(spacerItem, 0, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_5, 1, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        
        self.selectDimentionLabel = QtWidgets.QLabel(self.dataSourceTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectDimentionLabel.sizePolicy().hasHeightForWidth())
        self.selectDimentionLabel.setSizePolicy(sizePolicy)
        self.selectDimentionLabel.setMinimumSize(QtCore.QSize(50, 0))
        self.selectDimentionLabel.setSizeIncrement(QtCore.QSize(50, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selectDimentionLabel.setFont(font)
        self.selectDimentionLabel.setObjectName("selectDimentionLabel")
        self.gridLayout.addWidget(self.selectDimentionLabel, 0, 0, 1, 1)
        
        self.selectDimentionButton = QtWidgets.QPushButton(self.dataSourceTab)
        #self.selectDimentionLabel.setGeometry(QtCore.QRect(142, 10, 41, 28))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectDimentionButton.sizePolicy().hasHeightForWidth())
        self.selectDimentionButton.setSizePolicy(sizePolicy)
        self.selectDimentionButton.setObjectName("selectDimentionButton")
        self.selectDimentionButton.clicked.connect(self.launchDialog)
        
        self.gridLayout.addWidget(self.selectDimentionButton, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 2)
        
        self.usedFileLabel = QtWidgets.QLabel(self.dataSourceTab)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.usedFileLabel.setFont(font)
        self.usedFileLabel.setObjectName("usedFileLabel")
        self.gridLayout_3.addWidget(self.usedFileLabel, 2, 0, 1, 1)
        
        self.FileListChoose = QtWidgets.QListWidget(self.dataSourceTab)
        self.FileListChoose.setTabletTracking(True)
        self.FileListChoose.setAcceptDrops(True)
        self.FileListChoose.setDragEnabled(True)
        self.FileListChoose.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.FileListChoose.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.FileListChoose.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.FileListChoose.setObjectName("FileListChoose")
        if type(self.selectFile) != list:
            self.selectFile = [self.selectFile]
        for i in range(len(self.selectFile)):
            item = QtWidgets.QListWidgetItem()
            self.FileListChoose.addItem(item)
            
        self.tabWidget.addTab(self.dataSourceTab, "Data Source")
        
        self.gridLayout_3.addWidget(self.FileListChoose, 3, 0, 1, 2)
        
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        
        self.usedFileButton = QtWidgets.QPushButton(self.dataSourceTab)
        self.usedFileButton.setObjectName("usedFileButton")
        self.usedFileButton.clicked.connect(self.updateList)
        
        self.gridLayout_2.addWidget(self.usedFileButton, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 2, 1, 1, 1)
        
        self.FileList = QtWidgets.QListWidget(self.dataSourceTab)
        #self.FileList.setGeometry(QtCore.QRect(10, 50, 171, 221))
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
        
        self.gridLayout_3.addWidget(self.FileList, 1, 0, 1, 2)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        
        self.table = QtWidgets.QTableView(self.dataSourceTab)
        #self.table.setGeometry(QtCore.QRect(190, 10, 591, 471))
        self.table.horizontalHeader().setStretchLastSection(True)
        #self.table.verticalHeader().setStretchLastSection(True)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.dataSource()
        if self.selectFile != [] : 
            self.model = TableModel(self.data)
            self.table.setModel(self.model)
        #self.table.clicked.connect(self.on_header_doubleClicked)
        self.table.horizontalHeader().sectionClicked.connect(self.on_header_doubleClicked)
        
        self.gridLayout_4.addWidget(self.table, 0, 1, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        
        self.tabWidget.addTab(self.dataSourceTab, "Data Source")
        
        #self.tabWidget.addTab(self.dataSourceTab, "Data Souce")




        #Tab2 ############################################################
        self.SheetTab = QtWidgets.QWidget()
        self.SheetTab.setObjectName("SheetTab")
        
        self.gridLayout_14 = QtWidgets.QGridLayout(self.SheetTab)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        
        spacerItem1 = QtWidgets.QSpacerItem(500, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem1, 0, 0, 1, 1)
        
        self.chartType = QtWidgets.QComboBox(self.SheetTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chartType.sizePolicy().hasHeightForWidth())
        self.chartType.setObjectName("chartType")
        for i in self.typeChart :
            self.chartType.addItem(i)
        self.chartType.activated.connect(self.setplot)
        
        self.gridLayout_9.addWidget(self.chartType, 0, 1, 1, 1)
        
        self.plotButton = QtWidgets.QPushButton(self.SheetTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotButton.sizePolicy().hasHeightForWidth())
        self.plotButton.setSizePolicy(sizePolicy)
        self.plotButton.setObjectName("plotButton")
        self.plotButton.clicked.connect(self.setplot)
        
        self.gridLayout_9.addWidget(self.plotButton, 0, 2, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_9, 1, 0, 1, 3)
        
        self.gridLayout_13 = QtWidgets.QGridLayout()
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        
        self.ColList = QtWidgets.QListWidget(self.SheetTab)
        #self.ColList.setGeometry(QtCore.QRect(260, 50, 521, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ColList.sizePolicy().hasHeightForWidth())
        self.ColList.setSizePolicy(sizePolicy)
        self.ColList.setMinimumSize(QtCore.QSize(0, 20))
        self.ColList.setMaximumSize(QtCore.QSize(16777215, 30))
        self.ColList.setAcceptDrops(True)
        self.ColList.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.ColList.setAutoFillBackground(True)
        self.ColList.setDragEnabled(True)
        self.ColList.setDragDropOverwriteMode(True)
        self.ColList.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.ColList.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.ColList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ColList.setFlow(QtWidgets.QListView.LeftToRight)
        self.ColList.setGridSize(QtCore.QSize(100, 0))
        self.ColList.setObjectName("ColList")
        self.ColList.itemDoubleClicked.connect(self.ColDelect)
        # self.ColList.itemChanged.connect(self.setplot)
        #self.ColList.itemClicked.connect(self.cw)
        
        self.gridLayout_8.addWidget(self.ColList, 1, 1, 1, 1)
        
        self.ColLabel = QtWidgets.QLabel(self.SheetTab)
        #self.ColLabel.setGeometry(QtCore.QRect(200, 55, 61, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ColLabel.sizePolicy().hasHeightForWidth())
        self.ColLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ColLabel.setFont(font)
        self.ColLabel.setObjectName("ColLabel")
        
        self.gridLayout_8.addWidget(self.ColLabel, 1, 0, 1, 1)
        
        self.RowLabel = QtWidgets.QLabel(self.SheetTab)
        #self.RowLabel.setGeometry(QtCore.QRect(200, 10, 61, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RowLabel.sizePolicy().hasHeightForWidth())
        self.RowLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.RowLabel.setFont(font)
        self.RowLabel.setObjectName("RowLabel")
        
        self.gridLayout_8.addWidget(self.RowLabel, 0, 0, 1, 1)
        
        self.RowList = QtWidgets.QListWidget(self.SheetTab)
        #self.RowList.setGeometry(QtCore.QRect(260, 10, 521, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RowList.sizePolicy().hasHeightForWidth())
        self.RowList.setSizePolicy(sizePolicy)
        self.RowList.setMinimumSize(QtCore.QSize(0, 20))
        self.RowList.setMaximumSize(QtCore.QSize(16777215, 30))
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
        # self.RowList.itemChanged.connect(self.setplot)
        self.RowList.itemDoubleClicked.connect(self.RowDelect)
        
        self.gridLayout_8.addWidget(self.RowList, 0, 1, 1, 1)
        self.gridLayout_13.addLayout(self.gridLayout_8, 0, 0, 1, 1)
        
        self.sheetTable = QtWidgets.QTableView(self.SheetTab)
        #self.sheetTable.setGeometry(QtCore.QRect(200, 90, 581, 421))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sheetTable.sizePolicy().hasHeightForWidth())
        self.sheetTable.setSizePolicy(sizePolicy)
        self.sheetTable.setMinimumSize(QtCore.QSize(0, 0))
        self.sheetTable.setBaseSize(QtCore.QSize(0, 1000))
        self.sheetTable.resizeColumnsToContents()
        self.sheetTable.resizeRowsToContents()
        self.sheetTable.horizontalHeader().setCascadingSectionResizes(True)
        self.sheetTable.verticalHeader().setCascadingSectionResizes(True)
        #self.sheetTable.verticalHeader().hide()
        #self.sheetTable.horizontalHeader().hide()
        
        self.gridLayout_13.addWidget(self.sheetTable, 1, 0, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_13, 0, 2, 1, 1)
        
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        
        self.DimensionValuesLabel = QtWidgets.QLabel(self.SheetTab)
        #self.DimensionValuesLabel.setGeometry(QtCore.QRect(13, 16, 161, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DimensionValuesLabel.sizePolicy().hasHeightForWidth())
        self.DimensionValuesLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.DimensionValuesLabel.setFont(font)
        self.DimensionValuesLabel.setObjectName("DimensionValuesLabel")
        
        self.gridLayout_10.addWidget(self.DimensionValuesLabel, 0, 0, 1, 1)
        
        self.FileListDimension = QtWidgets.QListWidget(self.SheetTab)
        #self.FileListDimension.setGeometry(QtCore.QRect(10, 40, 181, 291))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FileListDimension.sizePolicy().hasHeightForWidth())
        self.FileListDimension.setSizePolicy(sizePolicy)
        self.FileListDimension.setAcceptDrops(True)
        self.FileListDimension.setDragEnabled(True)
        self.FileListDimension.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.FileListDimension.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.FileListDimension.setWordWrap(True)
        self.FileListDimension.setObjectName("FileListDimension")
        for i in range(len(self.colHeader)):
            item = QtWidgets.QListWidgetItem()
            self.FileListDimension.addItem(item)
        self.FileListDimension.clicked.connect(self.DropDup)
        
        self.gridLayout_10.addWidget(self.FileListDimension, 1, 0, 2, 1)
        
        self.MeasureValuesLabel = QtWidgets.QLabel(self.SheetTab)
        #self.MeasureValuesLabel.setGeometry(QtCore.QRect(10, 337, 161, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MeasureValuesLabel.sizePolicy().hasHeightForWidth())
        self.MeasureValuesLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.MeasureValuesLabel.setFont(font)
        self.MeasureValuesLabel.setObjectName("MeasureValuesLabel")

        self.gridLayout_10.addWidget(self.MeasureValuesLabel, 3, 0, 1, 1)
        
        self.filterLabel = QtWidgets.QLabel(self.SheetTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterLabel.sizePolicy().hasHeightForWidth())
        self.filterLabel.setSizePolicy(sizePolicy)
        self.filterLabel.setMinimumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.filterLabel.setFont(font)
        self.filterLabel.setObjectName("filterLabel")
        
        self.gridLayout_10.addWidget(self.filterLabel, 0, 1, 1, 1)
        
        self.FileListMes = QtWidgets.QListWidget(self.SheetTab)
        #self.FileListMes.setGeometry(QtCore.QRect(10, 360, 181, 151))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FileListMes.sizePolicy().hasHeightForWidth())
        self.FileListMes.setSizePolicy(sizePolicy)
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
        self.FileListMes.clicked.connect(self.DropDup)
        
        self.gridLayout_10.addWidget(self.FileListMes, 4, 0, 1, 1)
        
        self.filterButton = QtWidgets.QPushButton(self.SheetTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterButton.sizePolicy().hasHeightForWidth())
        self.filterButton.setSizePolicy(sizePolicy)
        self.filterButton.setMinimumSize(QtCore.QSize(30, 30))
        self.filterButton.setObjectName("filterButton")
        
        self.gridLayout_10.addWidget(self.filterButton, 0, 2, 1, 1)
        
        self.filterList = QtWidgets.QListWidget(self.SheetTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterList.sizePolicy().hasHeightForWidth())
        self.filterList.setSizePolicy(sizePolicy)
        self.filterList.setMinimumSize(QtCore.QSize(70, 100))
        self.filterList.setAcceptDrops(True)
        self.filterList.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.filterList.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.filterList.setObjectName("filterList")
        self.filterList.itemClicked.connect(self.openFilterPage)
        self.filterList.itemChanged.connect(self.filChange)
        #self.filterList.itemDoubleClicked.connect(self.fillDel)
        
        self.gridLayout_10.addWidget(self.filterList, 1, 1, 2, 2)
        self.gridLayout_11.addLayout(self.gridLayout_10, 0, 0, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout_11, 0, 0, 1, 1)
        
        self.tabWidget.addTab(self.SheetTab, "Sheet")
        
        
        
        
        
        
        
        # Tab 3 ######################################################################################Tab3
        self.chartTab = QtWidgets.QWidget()
        self.chartTab.setObjectName("chartTab")
        
        self.gridLayout_20 = QtWidgets.QGridLayout(self.chartTab)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.gridLayout_15 = QtWidgets.QGridLayout()
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.gridLayout_16 = QtWidgets.QGridLayout()
        self.gridLayout_16.setObjectName("gridLayout_16")
        
        spacerItem2 = QtWidgets.QSpacerItem(500, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        
        self.gridLayout_16.addItem(spacerItem2, 0, 0, 1, 1)
        
        self.chartType_2 = QtWidgets.QComboBox(self.chartTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chartType_2.sizePolicy().hasHeightForWidth())
        self.chartType_2.setSizePolicy(sizePolicy)
        self.chartType_2.setObjectName("chartType_2")
        for i in self.typeChart :
            self.chartType_2.addItem(i)
        self.chartType_2.activated.connect(self.setplot_2)
        
        self.gridLayout_16.addWidget(self.chartType_2, 0, 1, 1, 1)
        
        self.plotButton_2 = QtWidgets.QPushButton(self.chartTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotButton_2.sizePolicy().hasHeightForWidth())
        self.plotButton_2.setSizePolicy(sizePolicy)
        self.plotButton_2.setObjectName("plotButton_2")
        self.plotButton_2.clicked.connect(self.setplot_2)
        
        self.gridLayout_16.addWidget(self.plotButton_2, 0, 2, 1, 1)
        
        self.gridLayout_15.addLayout(self.gridLayout_16, 1, 0, 1, 3)
        
        self.gridLayout_17 = QtWidgets.QGridLayout()
        self.gridLayout_17.setObjectName("gridLayout_17")
        
        self.view = WebEngineView(self.chartTab)
        if self.Chart != None :
            print("Chart not none")
            self.view.updateChart(self.Chart)
            self.view.show()
                  
        self.gridLayout_17.addWidget(self.view, 1, 0, 1, 1)
        
        # self.widget = QtWidgets.QWidget(self.chartTab)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        # self.widget.setSizePolicy(sizePolicy)
        # self.widget.setObjectName("widget")
        
        # self.gridLayout_17.addWidget(self.widget, 1, 0, 1, 1)
        
        self.gridLayout_18 = QtWidgets.QGridLayout()
        self.gridLayout_18.setObjectName("gridLayout_18")
        
        self.ColList_2 = QtWidgets.QListWidget(self.chartTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ColList_2.sizePolicy().hasHeightForWidth())
        self.ColList_2.setSizePolicy(sizePolicy)
        self.ColList_2.setMinimumSize(QtCore.QSize(0, 20))
        self.ColList_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.ColList_2.setAcceptDrops(True)
        self.ColList_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.ColList_2.setAutoScroll(True)
        self.ColList_2.setDragEnabled(True)
        self.ColList_2.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.ColList_2.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.ColList_2.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ColList_2.setTextElideMode(QtCore.Qt.ElideRight)
        self.ColList_2.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.ColList_2.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.ColList_2.setFlow(QtWidgets.QListView.LeftToRight)
        self.ColList_2.setProperty("isWrapping", False)
        self.ColList_2.setGridSize(QtCore.QSize(100, 0))
        self.ColList_2.setViewMode(QtWidgets.QListView.ListMode)
        self.ColList_2.setUniformItemSizes(False)
        self.ColList_2.setWordWrap(True)
        self.ColList_2.setSelectionRectVisible(False)
        self.ColList_2.setObjectName("ColList_2")
        # self.ColList_2.itemChanged.connect(self.setplot_2)
        self.ColList_2.itemDoubleClicked.connect(self.ColDelect_2)
        
        self.gridLayout_18.addWidget(self.ColList_2, 1, 1, 1, 1)
        
        self.ColLabel_2 = QtWidgets.QLabel(self.chartTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ColLabel_2.sizePolicy().hasHeightForWidth())
        self.ColLabel_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ColLabel_2.setFont(font)
        self.ColLabel_2.setObjectName("ColLabel_2")
        
        self.gridLayout_18.addWidget(self.ColLabel_2, 1, 0, 1, 1)
        
        self.RowLabel_2 = QtWidgets.QLabel(self.chartTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RowLabel_2.sizePolicy().hasHeightForWidth())
        self.RowLabel_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.RowLabel_2.setFont(font)
        self.RowLabel_2.setObjectName("RowLabel_2")
        
        self.gridLayout_18.addWidget(self.RowLabel_2, 0, 0, 1, 1)
        
        self.RowList_2 = QtWidgets.QListWidget(self.chartTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RowList_2.sizePolicy().hasHeightForWidth())
        self.RowList_2.setSizePolicy(sizePolicy)
        self.RowList_2.setMinimumSize(QtCore.QSize(0, 20))
        self.RowList_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.RowList_2.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.RowList_2.setAcceptDrops(True)
        self.RowList_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.RowList_2.setAutoFillBackground(True)
        self.RowList_2.setAutoScroll(True)
        self.RowList_2.setAutoScrollMargin(5)
        self.RowList_2.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)
        self.RowList_2.setDragEnabled(True)
        self.RowList_2.setDragDropOverwriteMode(False)
        self.RowList_2.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.RowList_2.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.RowList_2.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.RowList_2.setTextElideMode(QtCore.Qt.ElideRight)
        self.RowList_2.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.RowList_2.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.RowList_2.setFlow(QtWidgets.QListView.LeftToRight)
        self.RowList_2.setProperty("isWrapping", False)
        self.RowList_2.setGridSize(QtCore.QSize(100, 0))
        self.RowList_2.setViewMode(QtWidgets.QListView.ListMode)
        self.RowList_2.setUniformItemSizes(False)
        self.RowList_2.setWordWrap(True)
        self.RowList_2.setSelectionRectVisible(False)
        self.RowList_2.setObjectName("RowList_2")
        self.RowList_2.itemDoubleClicked.connect(self.RowDelect_2)
        # self.RowList_2.itemChanged.connect(self.setplot_2)
        
        self.gridLayout_18.addWidget(self.RowList_2, 0, 1, 1, 1)
        
        self.gridLayout_17.addLayout(self.gridLayout_18, 0, 0, 1, 1)
        self.gridLayout_15.addLayout(self.gridLayout_17, 0, 2, 1, 1)
        
        self.gridLayout_19 = QtWidgets.QGridLayout()
        self.gridLayout_19.setObjectName("gridLayout_19")
        
        self.DimensionValuesLabel_2 = QtWidgets.QLabel(self.chartTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DimensionValuesLabel_2.sizePolicy().hasHeightForWidth())
        self.DimensionValuesLabel_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.DimensionValuesLabel_2.setFont(font)
        self.DimensionValuesLabel_2.setObjectName("DimensionValuesLabel_2")
        
        self.gridLayout_19.addWidget(self.DimensionValuesLabel_2, 0, 0, 1, 1)
        
        self.FileListDimension_2 = QtWidgets.QListWidget(self.chartTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FileListDimension_2.sizePolicy().hasHeightForWidth())
        self.FileListDimension_2.setSizePolicy(sizePolicy)
        self.FileListDimension_2.setMinimumSize(QtCore.QSize(0, 100))
        self.FileListDimension_2.setAcceptDrops(True)
        self.FileListDimension_2.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.FileListDimension_2.setDragEnabled(True)
        self.FileListDimension_2.setDragDropOverwriteMode(True)
        self.FileListDimension_2.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.FileListDimension_2.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.FileListDimension_2.setBatchSize(100)
        self.FileListDimension_2.setWordWrap(True)
        self.FileListDimension_2.setObjectName("FileListDimension_2")
        for i in range(len(self.colHeader)):
            item = QtWidgets.QListWidgetItem()
            self.FileListDimension_2.addItem(item)
        self.FileListDimension_2.clicked.connect(self.DropDup)
        
        self.gridLayout_19.addWidget(self.FileListDimension_2, 1, 0, 2, 1)
        
        self.MeasureValuesLabel_2 = QtWidgets.QLabel(self.chartTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MeasureValuesLabel_2.sizePolicy().hasHeightForWidth())
        self.MeasureValuesLabel_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.MeasureValuesLabel_2.setFont(font)
        self.MeasureValuesLabel_2.setObjectName("MeasureValuesLabel_2")
        
        self.gridLayout_19.addWidget(self.MeasureValuesLabel_2, 3, 0, 1, 1)
        
        self.filterLabel_2 = QtWidgets.QLabel(self.chartTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterLabel_2.sizePolicy().hasHeightForWidth())
        self.filterLabel_2.setSizePolicy(sizePolicy)
        self.filterLabel_2.setMinimumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.filterLabel_2.setFont(font)
        self.filterLabel_2.setObjectName("filterLabel_2")
        
        self.gridLayout_19.addWidget(self.filterLabel_2, 0, 1, 1, 1)
        
        self.FileListMes_2 = QtWidgets.QListWidget(self.chartTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FileListMes_2.sizePolicy().hasHeightForWidth())
        self.FileListMes_2.setSizePolicy(sizePolicy)
        self.FileListMes_2.setAcceptDrops(True)
        self.FileListMes_2.setDragEnabled(True)
        # self.FileListMes_2.setDragDropOverwriteMode(True)
        self.FileListMes_2.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.FileListMes_2.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.FileListMes_2.setBatchSize(100)
        # self.FileListMes_2.setWordWrap(True)
        self.FileListMes_2.setObjectName("FileListMes_2")
        for i in range(len(self.Measure)):
            item = QtWidgets.QListWidgetItem()
            self.FileListMes_2.addItem(item)
        #self.FileListMes3.clicked.connect(self.DropDup)
        
        self.gridLayout_19.addWidget(self.FileListMes_2, 4, 0, 1, 1)
        
        self.filterButton_2 = QtWidgets.QPushButton(self.chartTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterButton_2.sizePolicy().hasHeightForWidth())
        self.filterButton_2.setSizePolicy(sizePolicy)
        self.filterButton_2.setMinimumSize(QtCore.QSize(30, 30))
        self.filterButton_2.setObjectName("filterButton_2")
        
        self.gridLayout_19.addWidget(self.filterButton_2, 0, 2, 1, 1)
        
        self.filterList_2 = QtWidgets.QListWidget(self.chartTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterList_2.sizePolicy().hasHeightForWidth())
        self.filterList_2.setSizePolicy(sizePolicy)
        self.filterList_2.setMinimumSize(QtCore.QSize(70, 100))
        self.filterList_2.setAcceptDrops(True)
        self.filterList_2.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.filterList_2.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.filterList_2.setObjectName("filterList_2")
        self.filterList_2.itemClicked.connect(self.openFilterPage)
        self.filterList_2.itemChanged.connect(self.filChange_2)
        # self.filterList.itemDoubleClicked.connect(self.fillDel_2)
        
        self.gridLayout_19.addWidget(self.filterList_2, 1, 1, 2, 2)
        self.gridLayout_15.addLayout(self.gridLayout_19, 0, 0, 1, 1)
        self.gridLayout_20.addLayout(self.gridLayout_15, 0, 0, 1, 1)
        
        self.tabWidget.addTab(self.chartTab, "Chart")
        
        self.gridLayout_7.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 932, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        fileSelectName = "Choose File"
        if self.selectFile != []: fileSelectName = self.selectFile[0]
        #print(fileSelectName)
        
        self.selectDimentionLabel.setText(_translate("MainWindow", fileSelectName))
        self.usedFileLabel.setText(_translate("MainWindow", "Used File"))
        
        self.usedFileButton.setText(_translate("MainWindow", "Use"))
        self.selectDimentionButton.setText(_translate("MainWindow", "Directory"))
        
        #if self.selectFile in self.fileNameList :
        self.FileList.setSortingEnabled(True)
        __sortingEnabled = self.FileList.isSortingEnabled()
        self.FileList.setSortingEnabled(False)
        
        for i,j in zip(range(len(self.fileNameList)),self.fileNameList):
            #print(i,j)
            item = self.FileList.item(i)
            item.setText(_translate("MainWindow", str(j)))
        self.FileList.setSortingEnabled(__sortingEnabled)
        
        self.FileListChoose.setSortingEnabled(False)
        __sortingEnabled = self.FileListChoose.isSortingEnabled()
        print("Select file ",self.selectFile)
        for i,j in zip(range(len(set(self.selectFile))),set(self.selectFile)):
            item = self.FileListChoose.item(i)
            item.setText(_translate("MainWindow", str(j)))
        # self.FileListChoose.setSortingEnabled(True)
        
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.loadButton.setText(_translate("MainWindow", "Load"))
        
        #tab 2
        
        self.DimensionValuesLabel.setText(_translate("MainWindow", "Dimension"))
        self.filterLabel.setText(_translate("MainWindow", " Filter "))
        self.filterButton.setText(_translate("MainWindow", " Filter "))
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
        if self.selectFile != []:
            for i,j in zip(range(len(self.Measure)),self.Measure):
                item = self.FileListMes.item(i)
                item.setText(_translate("MainWindow", str(j)))
        self.FileListMes.setSortingEnabled(__sortingEnabled)
        
        self.ColLabel.setText(_translate("MainWindow", "Column"))
        self.RowLabel.setText(_translate("MainWindow", "Row"))
        self.plotButton.setText(_translate("MainWindow", "PLOT"))
        
        #TAB3
        self.ColLabel_2.setText(_translate("MainWindow", "Column"))
        self.RowLabel_2.setText(_translate("MainWindow", "Row"))
        self.filterLabel_2.setText(_translate("MainWindow", "Filter"))
        self.filterButton_2.setText(_translate("MainWindow", " Filter "))
                    
        self.plotButton_2.setText(_translate("MainWindow", "PLOT"))
        
        self.DimensionValuesLabel_2.setText(_translate("MainWindow", "Dimension"))
        __sortingEnabled = self.FileListDimension_2.isSortingEnabled()
        for i,j in zip(range(len(self.colHeader)),self.colHeader):
            item = self.FileListDimension_2.item(i)
            item.setText(_translate("MainWindow", str(j)))
        self.FileListDimension_2.setSortingEnabled(__sortingEnabled)
        
        self.MeasureValuesLabel_2.setText(_translate("MainWindow", "Measure Values"))
        
        self.FileListMes_2.setSortingEnabled(True)
        __sortingEnabled = self.FileListMes_2.isSortingEnabled()
        self.FileListMes_2.setSortingEnabled(False)
        if self.selectFile != []:
            for i,j in zip(range(len(self.Measure)),self.Measure):
                item = self.FileListMes_2.item(i)
                item.setText(_translate("MainWindow", str(j)))
        self.FileListMes_2.setSortingEnabled(__sortingEnabled)
        
    def tab2(self,MainWindow):
        print(self.RowChoose,self.ColChoose)
        self.RowList.clear()
        for i in range(len(self.RowChoose)):
            item = QtWidgets.QListWidgetItem()
            self.RowList.addItem(item)
            #self.RowList3.setModel(self.RowList3W)
        self.RowList.itemDoubleClicked.connect(self.RowDelect)
        #self.RowList.clicked.connect(self.DropDup)
        self.ColList.clear()
        for i in range(len(self.ColChoose)):
            item = QtWidgets.QListWidgetItem()
            self.ColList.addItem(item)
        self.ColList.itemDoubleClicked.connect(self.ColDelect)
        
        #tab 2
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        
        for i,j in zip(range(len(self.ColChoose)),self.ColChoose):
            item = QListWidgetItem('Blue')
            item = self.ColList.item(i)
            
            item.setText(_translate("MainWindow", str(j)))
        
        for i,j in zip(range(len(self.RowChoose)),self.RowChoose):
            item = self.RowList.item(i)
            item.setText(_translate("MainWindow", str(j)))

    def tab3(self,MainWindow):
        alt.data_transformers.disable_max_rows()
        altair_viewer._global_viewer._use_bundled_js = False
        alt.data_transformers.enable('data_server')
        
        self.RowList_2.clear()
        for i in range(len(self.RowChoose)):
            item = QtWidgets.QListWidgetItem()
            self.RowList_2.addItem(item)
            #self.RowList3.setModel(self.RowList3W)
        #self.RowList3.itemDoubleClicked.connect(self.RowDelect)
        
        self.ColList_2.clear()
        for i in range(len(self.ColChoose)):
            item = QtWidgets.QListWidgetItem()
            self.ColList_2.addItem(item)
        #self.ColList3.itemDoubleClicked.connect(self.ColDelect)
        
        # view = WebEngineView(self.chartTab)
        #view.setGeometry(QtCore.QRect(200, 90, 581, 421))
        if self.Chart != None :
            print("Chart not none")
            self.view.updateChart(self.Chart)
            self.view.show()
        
        #tab 3
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        
        for i,j in zip(range(len(self.ColChoose)),self.ColChoose):
            item = self.ColList_2.item(i)
            item.setText(_translate("MainWindow", str(j)))
        
        for i,j in zip(range(len(self.RowChoose)),self.RowChoose):
            item = self.RowList_2.item(i)
            item.setText(_translate("MainWindow", str(j)))
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    #ui.setupUi(MainWindow)
    cm = cmpage.csvManager()
    MainWindow.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')

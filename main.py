from email import header
from operator import mod
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QChart, QChartView, QBarSet, QPercentBarSeries, QBarCategoryAxis, QLineSeries
import numpy as np
import pandas as pd
import csvManager
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QPointF
from PyQt5 import QtCore, QtGui, QtWidgets , QtChart
from PyQt5.QtChart import QChart
from PyQt5.QtGui import QPainter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtChart import QChart, QChartView, QHorizontalBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
#from qgis.PyQt.QtWidgets import QVBoxLayout
cm = csvManager.csvManager()
class TableModel(QtCore.QAbstractTableModel):
    data = ""
    def __init__(self, data):
        super(TableModel, self).__init__()
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
                return self._data.columns[section]

            '''if orientation == Qt.Vertical: #y
                return ''.join(self._data.index[section])'''
                
class Ui_MainWindow(object):
    #dragDropFinished = QtCore.pyqtSignal()
    folderpath = ''
    fileNameList = []
    selectFile = []
    colHeader = []
    Measure = ['Sales', 'Quantity', 'Discount', 'Profit']
    path = ""
    RowChoose = []
    ColChoose = []
    dataSheet = ""
    #DimenForChoose = []
                
    def DropDup(self):
        itemsTextList =  [str(self.RowList.item(i).text()) for i in range(self.RowList.count())]
        self.RowChoose = itemsTextList
        itemsTextList =  [str(self.ColList.item(i).text()) for i in range(self.ColList.count())]
        self.ColChoose = itemsTextList
        itemsTextList =  [str(self.FileListDimension.item(i).text()) for i in range(self.FileListDimension.count())]
        itemsTextList = list(dict.fromkeys(itemsTextList))
        self.colHeader = itemsTextList
        print(self.RowChoose,self.ColChoose)
        print(self.selectFile)
        Ui_MainWindow.retranslateUi(self, MainWindow)
        
    def updateList(self):
        itemsTextList =  [str(self.FileListChoose.item(i).text()) for i in range(self.FileListChoose.count())]
        self.selectFile = itemsTextList
        itemsTextList =  [str(self.FileList.item(i).text()) for i in range(self.FileList.count())]
        self.fileNameList = itemsTextList
        self.dataSource()
        Ui_MainWindow.setupUi(self, MainWindow)
        
    def dropEvent(self, event):
        print('dropEvent')
        
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
        
    def creatSheet(self):
        '''self.sheetTable = QtWidgets.QTableWidget(self.tab_2)
        self.sheetTable.setGeometry(QtCore.QRect(200, 90, 581, 421))'''
        while (self.sheetTable.rowCount() > 0):
            self.sheetTable.removeRow(0)
        
        self.df_rows = len(self.dataSheet)
        self.df_cols = len(self.dataSheet.columns)
        self.df = self.dataSheet
        self.sheetTable.setRowCount(self.df_rows)
        self.sheetTable.setColumnCount(self.df_cols)
        for i in range(self.df_rows):
            for j in range(self.df_cols):
                x = format(self.df.iloc[i, j])
                #print(x)
                self.sheetTable.setItem(i, j, QTableWidgetItem(x))

    def plot(self):
        tmp = []
        tmp =  [str(self.RowList.item(i).text()) for i in range(self.RowList.count())]
        print("TMP",tmp)
        self.RowList = tmp
        tmp = [] 
        tmp =  [str(self.ColList.item(i).text()) for i in range(self.ColList.count())]
        self.ColList = tmp
        print(len(self.RowList),len(self.ColList))
        if len(set(self.ColList)) > 0 or len(set(self.RowList)) > 0:
            self.sheetPageRowAndCol(self.RowList,self.ColList)
            self.creatSheet()
            #self.setupUi(MainWindow)
        
    def dataSource(self):
        if type(self.selectFile) != list:
            self.selectFile = [self.selectFile]
        if self.selectFile != [] :
            if len(self.selectFile)>1:
                self.data = cm.unionFile(self.selectFile)
            else:
                self.path = self.folderpath+"/"+self.selectFile[0]
                self.data = cm.getDataWithPandas()

    def dataSourceSort(self,dimension):
        self.data = cm.setAllDataByOneDimension(dimension)
        
    def sheetPageRow(self):
        #print(self.RowList)
        self.dataSheet = cm.setDimensionSort(self.RowList)
        self.dataSheet[" "] = "abc"
                
    def sheetPageCol(self):
        tmp = cm.setDimensionSort(self.ColList)
        tmp[" "] = "abc"
        self.dataSheet = tmp.T
        
    '''def sheetPageAddCol(self,Row,Col):
        tmp = cm.getDataWithPandasByHead(Col)
        tmp = tmp.sort_values(by=Col)
        tmp = tmp.drop_duplicates().values
        res = list(map(list, zip(*tmp)))
        newDf = []
        for i in res:
            newDf.append(Row+i)
        self.data.columns = tuple(newDf[-1])
        df = pd.DataFrame(newDf)
        
    def sheetPageAddRow(self,Row):
        lists = [list(x) for x in self.data.index]
        print(len(lists))
        subRow = np.array(lists).T.tolist()
        for i,j in zip(reversed(subRow),Row):
            self.data.insert(0,j,i)'''
        
    def sheetPageRowAndCol(self,Row,Col):
        print("Start",Row,Col)
        if len(set(Col)) == 0 : 
            print("Row")
            self.sheetPageRow()
        elif len(set(Row)) == 0:
            print("Col") 
            self.sheetPageCol()
        else : 
            print("Row and Col")
            self.dataSheet = cm.setRowAndColumn(Row,Col)
    
    def handleSelectionChanged(self, selected, deselected):
        for index in self.table.selectionModel().selectedRows():
            print('Row %d is selected' % index.row())

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
        self.RowList.clicked.connect(self.DropDup)
        
        self.RowLabel = QtWidgets.QLabel(self.tab_2)
        self.RowLabel.setGeometry(QtCore.QRect(200, 10, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.RowLabel.setFont(font)
        self.RowLabel.setObjectName("RowLabel")
        
        self.ColDell = QtWidgets.QPushButton(self.tab_2)
        self.ColDell.setGeometry(QtCore.QRect(750, 50, 31, 31))
        self.ColDell.setObjectName("ColDell")
        
        self.RowDell = QtWidgets.QPushButton(self.tab_2)
        self.RowDell.setGeometry(QtCore.QRect(750, 10, 31, 31))
        self.RowDell.setObjectName("RowDell")
        
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
        self.ColList.clicked.connect(self.DropDup)
        
        self.sheetTable = QtWidgets.QTableWidget(self.tab_2)
        self.sheetTable.setGeometry(QtCore.QRect(200, 90, 581, 421))
        #print(self.dataSheet != "")
        if type(self.dataSheet) != str:
            self.creatSheet()
        
        self.plotButton = QtWidgets.QPushButton(self.tab_2)
        self.plotButton.setGeometry(QtCore.QRect(730, 470, 41, 31))
        self.plotButton.setObjectName("plotButton")
        self.plotButton.clicked.connect(self.plot)
            
        self.tabWidget.addTab(self.tab_2, "Sheet")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
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
        
        self.ColLabel.setText(_translate("MainWindow", "Column"))
        self.RowLabel.setText(_translate("MainWindow", "Row"))
        
        self.ColDell.setText(_translate("MainWindow", "DEL"))
        self.RowDell.setText(_translate("MainWindow", "DEL"))
        
        if self.RowChoose != [] and self.ColChoose != [] :
            if self.folderpath != '' :
                self.sheetPageRowAndCol(self.RowChoose,self.ColChoose)
                self.DataSource = QtWidgets.QTableWidget(self.tab_2)
                self.DataSource.setGeometry(QtCore.QRect(200, 120, 581, 391))
                self.DataSource.setObjectName("DataSource")
                if self.selectFile != [] : 
                    self.model = TableModel(self.data)
                    self.DataSource.setModel(self.model)
                    
        self.plotButton.setText(_translate("MainWindow", "PLOT"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')

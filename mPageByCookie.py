from operator import mod
import os
import pathlib
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

class TableModel(QtCore.QAbstractTableModel):
    data = None
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
    folderpath = ''
    fileNameList = []
    def launchDialog(self):
        self.folderpath = QFileDialog.getExistingDirectory()
        filename = os.listdir(self.folderpath)
        tmp = []
        for i in filename:
            if i.endswith(".xls") or i.endswith(".csv") or i.endswith(".xlsx"):
                tmp.append(i)
        self.fileNameList = tmp
        Ui_MainWindow.setupUi(self, MainWindow)
        #print(self.fileNameList)

    def dataSource(self):
        self.data = csvManager.getDataWithPandas()

    def dataSourceSort(self,dimention):
        self.data = csvManager.setAllDataByOneDimention(dimention)
        
    def sheetPageRow(self,dimention):
        self.data = csvManager.setDimentionSort(dimention)
        self.data[" "] = "abc"
                
    def sheetPageCol(self,dimention):
        tmp = csvManager.setDimentionSort(dimention)
        tmp[" "] = "abc"
        self.data = tmp.T
        
    def sheetPageAddCol(self,Row,Col):
        tmp = csvManager.getDataWithPandasByHead(Col)
        tmp = tmp.sort_values(by=Col)
        tmp = tmp.drop_duplicates().values
        res = list(map(list, zip(*tmp)))
        print(res)
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
            self.data.insert(0,j,i)
        
    def sheetPageRowAndCol(self,Row,Col):
        if len(set(Col)) == 0: MainWindow.sheetPageRow(self,Row)
        elif len(set(Row)) == 0: MainWindow.sheetPageCol(self,Col)
        else : 
            self.data = csvManager.setRowAndColumn(Row,Col)
            MainWindow.sheetPageAddRow(self,Row)
            MainWindow.sheetPageAddCol(self,Row,Col)
    
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
        
        '''data = csvManager.getDataWithPandas()
        dataCol = csvManager.getHead()
        #print(len(data))
        self.DataSource_2 = QtWidgets.QTableWidget(self.tab)
        self.DataSource_2.setGeometry(QtCore.QRect(190, 10, 581, 501))
        self.DataSource_2.setObjectName("DataSource_2")
        self.DataSource_2.setColumnCount(len(dataCol))
        self.DataSource_2.setRowCount(len(data))'''
        
        self.table = QtWidgets.QTableView(self.tab)
        self.table.setGeometry(QtCore.QRect(190, 10, 581, 501))
        Ui_MainWindow.dataSource(self)
        self.model = TableModel(self.data)
        '''model =  QtGui.QStandardItemModel(len(self.data), len(self.data.columns), self.table)
        for row in range(len(self.data)):
            for column in range(len(self.data.columns)):
                item = QtGui.QStandardItem('(%d, %d)' % (row, column))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                model.setItem(row, column, item)'''
        self.table.setModel(self.model)
        '''selection = self.table.selectionModel()
        selection.selectionChanged.connect(self.handleSelectionChanged)'''
        #layout = QtGui.QVBoxLayout(self)
        #layout.addWidget(self.table)
        
        '''for i,r in zip(range(len(dataCol)),dataCol):
            #print(i,r)
            item = QtWidgets.QTableWidgetItem()
            self.DataSource_2.setHorizontalHeaderItem(i, item)
            
        for i,r in zip(range(len(data)),list(data)):
            #print(i,r)
            item = QtWidgets.QTableWidgetItem()
            self.DataSource_2.setVerticalHeaderItem(i, item)'''
        
        #self.DataSource_2.setItem(0, 0, item)
        
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(50, 490, 93, 28))
        self.pushButton.setObjectName("Select File")
        self.pushButton.clicked.connect(self.launchDialog)
        print(self.fileNameList)
        self.FileList = QtWidgets.QListWidget(self.tab)
        self.FileList.setGeometry(QtCore.QRect(10, 10, 171, 271))
        self.FileList.setObjectName("listView")
        for i in range(len(self.fileNameList)):
            item = QtWidgets.QListWidgetItem()
            self.FileList.addItem(item)
            
        
        '''self.listView = QtWidgets.QListView(self.tab)
        self.listView.setGeometry(QtCore.QRect(10, 10, 171, 271))
        self.listView.setObjectName("listView")'''
        
        self.listView_2 = QtWidgets.QListView(self.tab)
        self.listView_2.setGeometry(QtCore.QRect(10, 290, 171, 191))
        self.listView_2.setObjectName("listView_2")
        model = QtGui.QStandardItemModel()
        #self.listView.setModel(model)
        '''for i in self.fileNameList:
            item = QtGui.QStandardItem(i)
            model.appendRow(item)
        self.listView.setGeometry(QtCore.QRect(10, 10, 171, 271))'''
        
        self.tabWidget.addTab(self.tab, "")

        #Tab2
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_2.setGeometry(QtCore.QRect(270, 50, 511, 31))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(4)
        self.tableWidget_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(200, 50, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.DataSource = QtWidgets.QTableWidget(self.tab_2)
        self.DataSource.setGeometry(QtCore.QRect(200, 90, 581, 421))
        self.DataSource.setObjectName("DataSource")
        self.DataSource.setColumnCount(3)
        self.DataSource.setRowCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.DataSource.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.DataSource.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.DataSource.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.DataSource.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.DataSource.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.DataSource.setHorizontalHeaderItem(2, item)
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setGeometry(QtCore.QRect(200, 10, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        '''self.FileList = QtWidgets.QListWidget(self.tab_2)
        self.FileList.setGeometry(QtCore.QRect(10, 10, 181, 501))
        self.FileList.setObjectName("FileList")
        item = QtWidgets.QListWidgetItem()
        self.FileList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.FileList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.FileList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.FileList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.FileList.addItem(item)'''
        
        self.tableWidget = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget.setGeometry(QtCore.QRect(270, 10, 511, 31))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tabWidget.addTab(self.tab_2, "")

        #tab3
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        """self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")"""
        self.Linegraph = QtWidgets.QPushButton(self.tab_3)
        self.Linegraph.setGeometry(QtCore.QRect(20, 430, 93, 28))
        self.Linegraph.setObjectName("Linegraph")
        self.Label = QtWidgets.QPushButton(self.tab_3)
        self.Label.setGeometry(QtCore.QRect(20, 110, 93, 28))
        self.Label.setObjectName("Label")
        self.Color = QtWidgets.QPushButton(self.tab_3)
        self.Color.setGeometry(QtCore.QRect(20, 80, 93, 28))
        self.Color.setObjectName("Color")
        self.Size = QtWidgets.QPushButton(self.tab_3)
        self.Size.setGeometry(QtCore.QRect(20, 170, 93, 28))
        self.Size.setObjectName("Size")
        self.Piechart = QtWidgets.QPushButton(self.tab_3)
        self.Piechart.setGeometry(QtCore.QRect(20, 460, 93, 28))
        self.Piechart.setObjectName("Piechart")
        self.Barchart = QtWidgets.QPushButton(self.tab_3)
        self.Barchart.setGeometry(QtCore.QRect(20, 400, 93, 28))
        self.Barchart.setObjectName("Barchart")
        self.stackbar = QtWidgets.QPushButton(self.tab_3)
        self.stackbar.setGeometry(QtCore.QRect(20, 490, 93, 28))
        self.stackbar.setObjectName("stackbar")
        self.Showgraph = QtWidgets.QListView(self.tab_3)
        self.Showgraph.setGeometry(QtCore.QRect(120, 80, 661, 441))
        self.Showgraph.setObjectName("Showgraph")
        self.Tooltips = QtWidgets.QPushButton(self.tab_3)
        self.Tooltips.setGeometry(QtCore.QRect(20, 140, 93, 28))
        self.Tooltips.setObjectName("Tooltips")
        self.Detail = QtWidgets.QPushButton(self.tab_3)
        self.Detail.setGeometry(QtCore.QRect(20, 200, 93, 28))
        self.Detail.setObjectName("Detail")
        MainWindow.setCentralWidget(self.tab_3)
        self.menubar = QtWidgets.QMenuBar(self.tab_3)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.tab_3)
        self.tabWidget.addTab(self.tab_3, "")


        
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
        '''data = csvManager.getDataWithPandas()
        dataCol = csvManager.getHead()
        #print(dataCol)
        #print(list(data["Row ID"]))
        
        for i,r in zip(range(len(dataCol)),dataCol):
            #print(i,r)
            item = self.DataSource_2.horizontalHeaderItem(i) 
            item.setText(_translate("MainWindow", str(r)))
            #for j in range(len(data)):
            
        for i,r in zip(range(len(list(data))),list(data)):
            #print(i,r)
            item = self.DataSource_2.verticalHeaderItem(i)
            #print(item)
            #item.setText(_translate("MainWindow", "kkk"))'''
        
            
        '''item = self.DataSource_2.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "0"))
        item = self.DataSource_2.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "1"))
        item = self.DataSource_2.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "2"))'''
        
        '''item = self.DataSource_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "0"))
        item = self.DataSource_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "1"))
        item = self.DataSource_2.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "2"))'''
        
        #__sortingEnabled = self.DataSource_2.isSortingEnabled()
        #self.DataSource_2.setSortingEnabled(False)
        
        #item = self.DataSource_2.item(0, 0)
        #item.setText(_translate("MainWindow", "kkk"))
        
        #self.DataSource_2.setSortingEnabled(__sortingEnabled)
        
        self.pushButton.setText(_translate("MainWindow", "Select File"))
        
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "New Column"))
        self.label_2.setText(_translate("MainWindow", "Column"))
        item = self.DataSource.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "0"))
        item = self.DataSource.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "1"))
        item = self.DataSource.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "2"))
        item = self.DataSource.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "0"))
        item = self.DataSource.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "1"))
        item = self.DataSource.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "2"))
        self.label.setText(_translate("MainWindow", "Row"))
        
        __sortingEnabled = self.FileList.isSortingEnabled()
        self.FileList.setSortingEnabled(False)
        for i,j in zip(range(len(self.fileNameList)),self.fileNameList):
            item = self.FileList.item(i)
            item.setText(_translate("MainWindow", str(j)))
        '''item = self.FileList.item(0)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.FileList.item(1)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.FileList.item(2)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.FileList.item(3)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.FileList.item(4)
        item.setText(_translate("MainWindow", "New Item"))'''
        self.FileList.setSortingEnabled(__sortingEnabled)
        
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "New Column"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        #Tab3
        self.Linegraph.setText(_translate("MainWindow", "Line graph"))
        self.Label.setText(_translate("MainWindow", "Label"))
        self.Color.setText(_translate("MainWindow", "Color"))
        self.Size.setText(_translate("MainWindow", "Size"))
        self.Piechart.setText(_translate("MainWindow", "Pie chart"))
        self.Barchart.setText(_translate("MainWindow", "Bar chart"))
        self.stackbar.setText(_translate("MainWindow", "Stack bar"))
        self.Tooltips.setText(_translate("MainWindow", "Tooltips"))
        self.Detail.setText(_translate("MainWindow", "Detail"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Tab 3"))
        
        #self.button = self.findChild(QtWidgets.QPushButton, 'Color') # Find the button
        self.Color.clicked.connect(AnyButton.changeColor) # Remember to pass the definition/method, not the return value!
        #self.button = self.findChild(QtWidgets.QPushButton, 'Size') 
        self.Size.clicked.connect(AnyButton.buttonsize)
        #self.button = self.findChild(QtWidgets.QPushButton, 'Label') 
        self.Label.clicked.connect(AnyButton.buttonlabel)
        #self.button = self.findChild(QtWidgets.QPushButton, 'Detail') 
        self.Detail.clicked.connect(AnyButton.Buttondetail)
        #self.button = self.findChild(QtWidgets.QPushButton, 'Tooltips') 
        self.Tooltips.clicked.connect(AnyButton.ButtonTooltips)
        #self.button = self.findChild(QtWidgets.QPushButton, 'Barchart') 
        self.Barchart.clicked.connect(lambda checked: ShowGraph.showbarchart(self))
        #self.button.clicked.connect(ShowGraph.showbarchart)
        #self.button = self.findChild(QtWidgets.QPushButton, 'Piechart') 
        self.Piechart.clicked.connect(lambda checked: ShowGraph.showpiechart(self))
        #.button = self.findChild(QtWidgets.QPushButton, 'Linegraph') 
        self.Linegraph.clicked.connect(lambda checked: ShowGraph.showlinegraph(self))
        #self.button = self.findChild(QtWidgets.QPushButton, 'stackbar') 
        self.stackbar.clicked.connect(lambda checked: ShowGraph.showstackbar(self))
    
        
        
class AnyButton() :
        
    def changeColor() :
        print("Hello color")
    def buttonsize() :
        print("Hello size")
    def buttonlabel() :
        print("Hello label")
    def Buttondetail() :
        print("Hello detail")
    def ButtonTooltips() :
        print("Hello Tooltips")
   

class ShowGraph(FigureCanvas):
    def __init__(self):
        super().__init__()
 
        self.setWindowTitle("PyQt BarChart")
        #self.setGeometry(100,100, 680,500)
        self.show()
        self.create_bar()
    def showlinegraph(self) :
        print("Show line")
        series = QLineSeries(self)
        series.append(0,6)
        series.append(2, 4)
        series.append(3, 8)
        series.append(7, 4)
        series.append(10, 5)
 
        series << QPointF(11, 1) << QPointF(13, 3) << QPointF(17, 6) << QPointF(18, 3) << QPointF(20, 2)
 
 
        chart =  QChart()
 
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Line Chart Example")
 
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
 
 
        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)
 
        self.setCentralWidget(chartview)
    def showbarchart(self) :
        df = pd.read_csv('Superstore.csv', encoding='windows-1252')
        Reg = []
		
        for i in df['Region'].values:
            if i not in Reg:
                Reg.append(i)

        df.set_index('Region',inplace=True)
        profit = []
        disc = []
        quan = []
        sale = []

        for i in Reg:
            profit.append(sum(df.loc[i,'Profit']))
            disc.append(sum(df.loc[i,'Discount']))
            quan.append(sum(df.loc[i,'Quantity']))
            sale.append(sum(df.loc[i,'Sales']))

        tmp = [profit,disc,quan,sale]
        

        set0 = QBarSet('Profit')
        set1 = QBarSet('Discount') 
        set2 = QBarSet('Quantity')
        set3 = QBarSet('Sales')

        for i in range(len(Reg)):
            set0.append(tmp[i][0])
            set1.append(tmp[i][1])
            set2.append(tmp[i][2])
            set3.append(tmp[i][3])

        '''print(profit)
        print(disc)
        print(quan)
        print(sale)'''
        
        series = QPercentBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
 
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Percent Example")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        meslist = ['Profit','Discount','Quantity','Sales']
        axis = QBarCategoryAxis()
        axis.append(meslist)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)
 
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
 
        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)
 
        self.setCentralWidget(chartView)

    def showpiechart(self) :
        print("Show Pie")
        series = QtChart.QPieSeries()
        series.append("Jane", 1)
        series.append("Joe", 2)
        series.append("Andy", 3)
        series.append("Barbara", 4)
        series.append("Axel", 5)

        chart = QtChart.QChart()
        chart.addSeries(series)
        chart.setTitle("Simple piechart example")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().hide()

        series.setLabelsVisible()
        #series.setLabelsPosition(QtChart.QPieSlice.LabelInsideHorizontal)

        for slice in series.slices():
            slice.setLabel("{:.1f}%".format(100 * slice.percentage()))

        chartView = QtChart.QChartView(chart)
        chartView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setCentralWidget(chartView)
        

    def showstackbar(self) :
        print("Show stack")
        set0 = QBarSet("Parwiz")
        set1 = QBarSet("Bob")
        set2 = QBarSet("Tom")
        set3 = QBarSet("Logan")
        set4 = QBarSet("Karim")
 
        set0 << 1 << 2 << 3 << 4 << 5 << 6  #Jan -> Jun
        set1 << 5 << 0 << 0 << 4 << 0 << 7
        set2 << 3 << 5 << 8 << 13 << 8 << 5
        set3 << 5 << 6 << 7 << 3 << 4 << 5
        set4 << 9 << 7 << 5 << 3 << 1 << 2
 
        series = QPercentBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
        series.append(set4)
 
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Percent Example")
        chart.setAnimationOptions(QChart.SeriesAnimations)
 
        categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        axis = QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)
 
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
 
        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)
 
        self.setCentralWidget(chartView)

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

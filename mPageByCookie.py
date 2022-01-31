import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import numpy as np
import pandas as pd
import csvManager
#from qgis.PyQt.QtWidgets import QVBoxLayout

class TableModel(QtCore.QAbstractTableModel):
    data = None
    def __init__(self, data):
        super(TableModel, self).__init__()
        #self.itemClicked.connect(self.handleItemClick)
        self._data = data
        

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
        self.listView = QtWidgets.QListView(self.tab)
        self.listView.setGeometry(QtCore.QRect(10, 10, 171, 271))
        self.listView.setObjectName("listView")
        self.listView_2 = QtWidgets.QListView(self.tab)
        self.listView_2.setGeometry(QtCore.QRect(10, 290, 171, 191))
        self.listView_2.setObjectName("listView_2")
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(50, 490, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.tabWidget.addTab(self.tab, "")
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
        self.FileList = QtWidgets.QListWidget(self.tab_2)
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
        self.FileList.addItem(item)
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
        
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
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
        item = self.FileList.item(0)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.FileList.item(1)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.FileList.item(2)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.FileList.item(3)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.FileList.item(4)
        item.setText(_translate("MainWindow", "New Item"))
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

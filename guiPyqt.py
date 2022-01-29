import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import Qt
import pandas as pd
import csvManager

class TableModel(QtCore.QAbstractTableModel):
    
    def __init__(self, data):
        super(TableModel, self).__init__()
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
                return str(self._data.columns[section])

            if orientation == Qt.Vertical: #y
                return str(self._data.index[section])


class MainWindow(QtWidgets.QMainWindow):
    
    def dataSource(self):
        self.data = csvManager.getDataWithPandas()

    def dataSourceSort(self,dimention):
        self.data = csvManager.setAllDataByOneDimention(dimention)
        
    def sheetPageRow(self,dimention):
        self.data = csvManager.setDimentionSort(dimention)
        
    def sheetPageCol(self,dimention):
        tmp = csvManager.setDimentionSort(dimention)
        self.data = tmp.T
    
    def __init__(self):
        super().__init__()
        self.data = None
        
        dimention = ["Country/Region","City","State","Postal Code","Region","Product ID"]
        self.table = QtWidgets.QTableView()
        
        #data = csvManager.setRowAndColumn(["City","State"],["Row ID"])
        #self.model = TableModel(data)
        
        #MainWindow.dataSource(self)
        
        #MainWindow.dataSourceSort(self,"Sales")
        
        #MainWindow.sheetPageRow(self,dimention)
        
        #MainWindow.sheetPageCol(self,dimention)
        
        self.model = TableModel(self.data)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)

app=QtWidgets.QApplication(sys.argv)
window=MainWindow()
window.showMaximized()
sys.exit(app.exec())
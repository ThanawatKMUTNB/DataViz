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
    def __init__(self):
        super().__init__()
        
        dimention = ["Country/Region","City","State","Postal Code","Region","Product ID"]
        dimention2 = ["Country/Region","Region","State","City","Postal Code","Product ID"]
        self.table = QtWidgets.QTableView()
        
        data = csvManager.getDataWithPandasByHead(dimention)
        sortedData = csvManager.setDimentionSort(dimention)
        self.model = TableModel(sortedData.T)
        
        #data = csvManager.getDataWithPandas()
        #self.model = TableModel(data.T)
        
        #data = csvManager.setAllDataByOneDimention("Sales")
        #self.model = TableModel(data)
        
        #data = csvManager.getDataWithPandasByHead(dimention)
        #sortedData = csvManager.setDimentionSort(dimention)
        #self.model = TableModel(sortedData)
        
        #data = csvManager.getDataWithPandas()
        #data = pd.DataFrame(databuf,columns=[databuf.columns.tolist()],index=databuf["Row ID"])

        #self.model = TableModel(data)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)

app=QtWidgets.QApplication(sys.argv)
window=MainWindow()
window.showMaximized()
sys.exit(app.exec())
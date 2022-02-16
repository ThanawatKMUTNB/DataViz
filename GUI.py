import os
import sys
from typing import ItemsView
from PyQt5.QtCore import Qt
import csvManager as cmpage
from matplotlib import widgets
from PyQt5 import uic,QtCore
# from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QDialog,QApplication,QMainWindow,QTableWidget,QFileDialog
                             ,QPushButton,QListWidget,QAbstractItemView,QTableWidgetItem
                             ,QVBoxLayout,QTableView,QMessageBox)

# SF =[]

class FileChoose(QtWidgets.QListWidget):
    def __init__(self,parent=None):
        super(FileChoose, self).__init__(parent)
        self.setAcceptDrops(True)
        # self.setText(" Accept Drops")
        # self.setStyleSheet("QLabel { background-color : #ccd; color : blue; font-size: 20px;}")

    def dropEvent(self, QDropEvent):
        source_Widget=QDropEvent.source()
        items=source_Widget.selectedItems()
        # if self.currentItem() != None:
        #     print(self.currentItem().text())
        for i in items:
            source_Widget.takeItem(source_Widget.indexFromItem(i).row())
            self.addItem(i)
        mainW.useFile()
        print('drop event')
        
    def Clicked(self,item):
          QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())
            
class FileInDirec(QtWidgets.QListWidget):
    def __init__(self,parent=None):
        super(FileInDirec, self).__init__(parent)
        self.setAcceptDrops(True)
        # self.setText(" Accept Drops")
        # self.setStyleSheet("QLabel { background-color : #ccd; color : blue; font-size: 20px;}")

    # def dragEnterEvent(self, e):
    #     e.accept()
        # print("DragEnter")

    # def dragLeaveEvent(self,event) -> None:
    #     if self.count():
    #         self.takeItem(self.currentRow())
    #         self.clearSelection()

    # def dragMoveEvent(self, e):
    #     e.accept()
    #     print("DragMove")

    def dropEvent(self, QDropEvent):
        source_Widget=QDropEvent.source()
        items=source_Widget.selectedItems()
        # if self.currentItem() != None:
        #     print(self.currentItem().text())
        for i in items:
            source_Widget.takeItem(source_Widget.indexFromItem(i).row())
            self.addItem(i)
        mainW.useFile()
        print('drop event2')

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

class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow,self).__init__()
        uic.loadUi("mainGUI.ui",self)
        # loadUi("mainGUI.ui",self)
        self.Measure = ['Sales', 'Quantity', 'Discount', 'Profit']
        self.fileNameList = []
        self.selectFile = []
        self.data = ""
        
        # defind
        self.openDirecButton = self.findChild(QPushButton,"openDirecButton")
        
        self.dataSourceTable = self.findChild(QTableView,"table")
        self.dataSourceTable.horizontalHeader().setStretchLastSection(True)
        self.dataSourceTable.resizeColumnsToContents()
        self.dataSourceTable.resizeRowsToContents()
        
        # self.useButton = self.findChild(QPushButton,"useButton")
        # self.FileListChoose = FileChoose()
        # self.print_info()
        # # self.FileList = self.findChild(FileInDirec,"FileList")
        self.FileListChoose = self.findChild(FileChoose,"FileListChoose")
        
        # # function
        self.openDirecButton.clicked.connect(self.launchDialog)
        self.dataSourceTable.horizontalHeader().sectionClicked.connect(self.on_header_doubleClicked)
        # self.useButton.clicked.connect(self.useFile)
        # self.useButton.clicked.connect(self.setList)
        # self.FileListChoose.currentItemChanged.connect(self.print_info)
        print(self.selectFile)
        self.show()
        
    def on_header_doubleClicked(self,index):
        #headCur = index
        self.colHeader = cm.getHead()
        self.data = cm.setAllDataByOneDimension(self.colHeader[index])
        self.model = TableModel(self.data)
        self.dataSourceTable.setModel(self.model)
        
    def useFile(self):
        # print("kk")
        #self.__init__(MainWindow)
        itemsTextList =  [str(self.FileListChoose.item(i).text()) for i in range(self.FileListChoose.count())]
        self.selectFile = itemsTextList
        # print(self.selectFile)
        
        while (self.selectFile.count('')):
            self.selectFile.remove('')
        itemsTextList =  [str(self.FileList.item(i).text()) for i in range(self.FileList.count())]
        self.fileNameList = itemsTextList
        while (self.fileNameList.count('')):
            self.fileNameList.remove('')
        self.RowChoose = []
        self.ColChoose = []
        if self.selectFile != []:
            self.colHeader = cm.getHead()
        else: self.colHeader = []
        self.dataSource()
        
    def setTable(self):
        print("set data")
        print(self.selectFile)
        if self.selectFile != [] : 
            self.dataSource()
            print(self.data)
            self.model = TableModel(self.data)
            self.dataSourceTable.setModel(self.model)
            
    def dataSource(self):
        # print(self.selectFile)
        if type(self.selectFile) != list:
            self.selectFile = [self.selectFile]
        if self.selectFile != [] :
            if len(self.selectFile)>1:
                print("Union")
                self.data = cm.unionFile(self.selectFile)
                self.colHeader = cm.getHead()
            else:
                print("Not Union")
                cm.path =self.folderpath
                cm.selectFile = self.selectFile[0] 
                cm.setPath()
                self.data = cm.getDataWithPandas()
        self.model = TableModel(self.data)
        self.dataSourceTable.setModel(self.model)
            #print(self.data)
        
    def setFileInDirectory(self):
        self.FileList.clear()
        if self.fileNameList != []:
            self.FileList.addItems(self.fileNameList)
    
    def setFileChoose(self):
        print("bf",self.selectFile)
        self.FileListChoose.clear()
        if self.selectFile != []:
            self.FileListChoose.addItems([self.selectFile])
            # self.setTable()
        # if self.selectFile != []:
        #     self.loaddata()
            
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
        cm.path = self.folderpath
        cm.selectFile = self.selectFile
        cm.setPath()
        # print(cm.df)
        self.colHeader = cm.getHead()
        for i in self.Measure:
            if i in self.colHeader:
                self.colHeader.remove(i)
                
        self.setFileInDirectory()
        self.setFileChoose()
        self.dataSource()
        # self.data = cm.getDataWithPandas()
        # Ui_MainWindow.setupUi(self, MainWindow)

class filterMesWindow(QMainWindow):
    def __init__(self):
        super(filterMesWindow,self).__init__()
        uic.loadUi("filterMes.ui",self)
        self.show()

class filterDimenWindow(QMainWindow):
    def __init__(self):
        super(filterDimenWindow,self).__init__()
        uic.loadUi("filterDimen.ui",self)
        self.show()

app = QApplication(sys.argv)
# widget = QtWidgets.QStackedWidget()
cm = cmpage.csvManager()
mainW = mainWindow()
# filD = filterDimenWindow()
# filM = filterMesWindow()
# widget.addWidget(mainW)
# widget.addWidget(filM)
# widget.addWidget(filD)
# widget.show()
try:
    sys.exit(app.exec_())
except SystemExit:
    print('Closing Window...')
# window = uic.loadUi("mainGUI.ui")
# window.show()
# app.exec()
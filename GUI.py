import os
import sys
from PyQt5.QtCore import Qt,QEvent
import csvManager as cmpage
from PyQt5 import uic,QtCore
# from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication,QMainWindow,QFileDialog,QTableWidget
                             ,QPushButton,QListWidget,QTableView,QMessageBox,QMenu)

# SF =[]
class colListClass(QtWidgets.QListWidget):
    def __init__(self,parent=None):
        super(colListClass, self).__init__(parent)
        self.setAcceptDrops(True)
        
    # def dragEnterEvent(self, event):
    #     #if event.mimeData().hasUrls():
    #     event.accept()

    # def dragMoveEvent(self, event):
    #     #if event.mimeData().hasUrls():
    #     event.accept()

    def dropEvent(self, QDropEvent):
        source_Widget=QDropEvent.source()
        items=source_Widget.selectedItems()
        QDropEvent.setDropAction(QtCore.Qt.MoveAction)
        for i in items:
            source_Widget.takeItem(source_Widget.indexFromItem(i).row())
            self.addItem(i)
        mainW.setFileListDimension()
        mainW.setplot()
        # mainW.useFile()
        # print('drop event Col')
        
class rowListClass(QtWidgets.QListWidget):
    def __init__(self,parent=None):
        super(rowListClass, self).__init__(parent)
        self.setAcceptDrops(True)
        # self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        
    # def dragEnterEvent(self, event):
    #     #if event.mimeData().hasUrls():
    #     event.accept()

    # def dragMoveEvent(self, event):
    #     #if event.mimeData().hasUrls():
    #     event.accept()
            
    def dropEvent(self, QDropEvent):
        source_Widget=QDropEvent.source()
        items=source_Widget.selectedItems()
        QDropEvent.setDropAction(QtCore.Qt.MoveAction)
        for i in items:
            source_Widget.takeItem(source_Widget.indexFromItem(i).row())
            self.addItem(i)
        mainW.setFileListDimension()
        mainW.setplot()
        # mainW.useFile()
        # print('drop event Row')
            
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
        self.dataSheet = ""
        self.data = ""
        
        # defind
        self.openDirecButton = self.findChild(QPushButton,"openDirecButton")
        
        self.RowList  = self.findChild(QListWidget,"RowList")
        self.ColList  = self.findChild(QListWidget,"ColList")
        
        self.dataSourceTable = self.findChild(QTableView,"table")
        self.dataSourceTable.horizontalHeader().setStretchLastSection(True)
        self.dataSourceTable.resizeColumnsToContents()
        self.dataSourceTable.resizeRowsToContents()
        
        self.sheetTable  = self.findChild(QTableView,"sheetTable")
        
        self.FileListDimension = self.findChild(QListWidget,"FileListDimension")
        self.FileListMes = self.findChild(QListWidget,"FileListMes")
        
        self.FileListChoose = self.findChild(FileChoose,"FileListChoose")
        
        # function
        self.openDirecButton.clicked.connect(self.launchDialog)
        self.dataSourceTable.horizontalHeader().sectionClicked.connect(self.on_header_doubleClicked)
        
        print(self.selectFile)
        self.show()
        # self.FileListDimension.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.FileListDimension:
            menu = QMenu()
            menu.addAction('Action 1')
            menu.addAction('Action 2')
            menu.addAction('Action 3')

            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                # print(item.text())
            return True
        return super().eventFilter(source, event)
    
    def setplot(self):
        #print("--------",self.RowChoose,self.ColChoose)
        tmp = []
        tmp =  [str(self.RowList.item(i).text()) for i in range(self.RowList.count())]
        self.RowChoose = tmp
        tmp = [] 
        tmp =  [str(self.ColList.item(i).text()) for i in range(self.ColList.count())]
        self.ColChoose = tmp
        while (self.RowChoose.count('')):
            self.RowChoose.remove('')
        while (self.ColChoose.count('')):
            self.ColChoose.remove('')
        self.setSheetTable()
        # self.chartTypeS = self.chartType.currentText()#choose detect row column (recommend graph)
        # print(self.chartTypeS)
        # print("--------",self.RowChoose,self.ColChoose)
        # self.plot()
        
    def setSheetTable(self):
        if self.selectFile != [] : 
            self.sheetPageRowAndCol(self.RowChoose,self.ColChoose)
            self.model = TableModel2(self.dataSheet)
            self.sheetTable.setModel(self.model)
    
    def sheetPageRowAndCol(self,Row,Col):
        print("Start",Row,Col,len(set(Row)),len(set(Col)))
        if Row!=[] or Col!=[]:
            self.dataSheet = cm.setRowAndColumn(Row,Col)
            
    # def plot(self):
    #     isInterRow = list(set.intersection(set(self.RowChoose),set(self.Measure)))
    #     isInterCol = list(set.intersection(set(self.ColChoose),set(self.Measure)))
    #     # print("--------",self.RowChoose,self.ColChoose)
    #     # print(str(self.chartTypeS))
    #     if  isInterRow != [] and isInterCol != []:
    #         self.chartType.clear()
    #         self.chartType.addItems([""])
    #     else :
    #         if  isInterRow != [] or isInterCol != []:
    #             # print(self.chartType.currentText())
    #             if isInterRow != [] and isInterCol == []:
    #                 gm = graphManager.graphManager()
    #                 '''for i in isInterRow:
    #                     self.RowChoose.remove(i)
    #                 self.ColChoose = self.ColChoose + isInterRow'''
    #                 gm.setList(self.RowChoose,self.ColChoose,self.data)
    #                 self.Chart = gm.chooseChart(str(self.chartTypeS))
    #                     #self.RowList.addItems(self.RowChoose)
    #                     #self.ColList.addItems(self.ColChoose)
    #                     #self.tab3(MainWindow)
                
    #             if isInterRow == [] and isInterCol != []:
    #                 gm = graphManager.graphManager()
    #                 '''for i in isInterCol:
    #                     self.ColChoose.remove(i)
    #                 self.RowChoose = self.RowChoose + isInterCol'''
    #                 gm.setList(self.RowChoose,self.ColChoose,self.data)
    #                 # print(str(self.chartTypeS))
    #                 self.Chart = gm.chooseChart(str(self.chartTypeS))
    #                     #self.RowList.addItems(self.RowChoose)
    #                     #self.ColList.addItems(self.ColChoose)
    #                     #self.tab3(MainWindow)
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
            self.setFileListDimension()
        else: 
            self.colHeader = []
            self.dataSourceTable.reset()
            self.FileListDimension.clear()
            self.FileListDimension.addItems(self.colHeader)
            self.FileListMes.clear()
            self.FileListMes.addItems([])
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
        else:
            self.dataSourceTable.reset()
            self.dataSourceTable.setModel(None)
            #print(self.data)
        
    def setFileInDirectory(self):
        self.FileList.clear()
        if self.fileNameList != []:
            self.FileList.addItems(self.fileNameList)
    
    def setFileChoose(self):
        print("bf",self.selectFile)
        self.FileListChoose.clear()
        if type(self.selectFile) != list:
            self.selectFile = [self.selectFile]
        if self.selectFile != []:
            self.FileListChoose.addItems(self.selectFile)
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
        # self.selectFile = response
        self.folderpath = os.getcwd()
        filename = os.listdir(self.folderpath)
        tmp = []
        for i in filename:
            if i.endswith(".xls") or i.endswith(".csv") or i.endswith(".xlsx"):
                tmp.append(i)
        response = list(response)
        self.selectFile = os.path.split(response[0])
        # print(self.selectFile)
        self.selectFile = list(self.selectFile)[1]
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
        self.setFileListDimension()
        self.setFileInDirectory()
        self.setFileChoose()
        self.dataSource()
        # self.data = cm.getDataWithPandas()
        # Ui_MainWindow.setupUi(self, MainWindow)
    def setFileListDimension(self):
        if self.FileListDimension != None:
            self.FileListDimension.clear()
            self.FileListDimension.addItems(self.colHeader)
        if self.FileListMes != None:
            self.FileListMes.clear()
            self.FileListMes.addItems(self.Measure)
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
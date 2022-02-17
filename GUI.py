import os
import sys
from PyQt5.QtCore import Qt,QEvent
from matplotlib import widgets
import csvManager as cmpage
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import uic,QtCore,QtWebEngineWidgets
# from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from Altair_Graph.Bar_Chart import WebEngineView
from io import StringIO
import graphManager 

import altair as alt
import altair_viewer

alt.data_transformers.disable_max_rows()
altair_viewer._global_viewer._use_bundled_js = False
alt.data_transformers.enable('data_server')

class filterMesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("filterMes.ui",self)
        self.show()

class filterDimenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("filterDimen.ui",self)
        self.show()
        self.dimen = ''
        self.sheet = ''
        self.filtered = {}
        self.checkedList = []
        # defind
        self.allButton = self.findChild(QPushButton,"allButton")
        self.filterItemListWidget = self.findChild(QListWidget,"filterItemListWidget")
        self.noneButton = self.findChild(QPushButton,"noneButton")
        self.fieldLabel = self.findChild(QLabel,"fieldLabel")
        self.selectionLabel = self.findChild(QLabel,"selectionLabel")
        self.selectionLabel = self.findChild(QLabel,"selectionLabel")
        self.resetButton = self.findChild(QPushButton,"resetButton")
        self.cancleButton = self.findChild(QPushButton,"cancleButton")
        self.okButton = self.findChild(QPushButton,"okButton")
        #  func
        self.allButton.clicked.connect(self.allBut)
        self.noneButton.clicked.connect(self.noneBut)
        self.resetButton.clicked.connect(self.resetBut)
        self.cancleButton.clicked.connect(self.cancleBut)
        self.okButton.clicked.connect(self.ApplyBut)
        
        self.filterItemListWidget.itemChanged.connect(self.checked)
        self.filterItemListWidget.doubleClicked.connect(self.reverseCheck)
        self.setUp()
        self.setList()
        self.resetBut()
    
    def ApplyBut(self):
        self.filtered[self.dimen] = self.checkedList
        mainW.filDic = self.filtered
        mainW.setSheetTable()
        self.close()
        
    def cancleBut(self):
        self.close()
        
    def resetBut(self):
        for i in range(self.filterItemListWidget.count()):
            if self.filterItemListWidget.item(i).text() in self.filtered[self.dimen]:
                self.filterItemListWidget.item(i).setCheckState(QtCore.Qt.Checked)
            else:
                self.filterItemListWidget.item(i).setCheckState(QtCore.Qt.Unchecked)
            
    def reverseCheck(self):
        filterItem = self.filterItemListWidget.currentRow()
        strItem = self.filterItemListWidget.item(filterItem)
        if strItem.checkState() == 2:
            strItem.setCheckState(QtCore.Qt.Unchecked)
        else:
            strItem.setCheckState(QtCore.Qt.Checked)
        self.checked()
            
    def allBut(self):
        for i in range(self.filterItemListWidget.count()):
            self.filterItemListWidget.item(i).setCheckState(QtCore.Qt.Checked)
        self.checked()
    
    def noneBut(self):
        for i in range(self.filterItemListWidget.count()):
            self.filterItemListWidget.item(i).setCheckState(QtCore.Qt.Unchecked)
        self.checked()
        
    def checked(self):
        self.fieldLabel.setText("Field : "+ str(self.dimen))

        filterItem = self.filterItemListWidget.currentRow()
        strItem = self.filterItemListWidget.item(filterItem)
        itemsTextList =  [str(self.filterItemListWidget.item(i).text()) for i in range(self.filterItemListWidget.count())]
        self.checkedList = []
        for i in range(self.filterItemListWidget.count()):
            if self.filterItemListWidget.item(i).checkState() == 2:
                self.checkedList.append(self.filterItemListWidget.item(i).text())
        
        self.selectionLabel.setText("Selection : "+ str(len(self.checkedList))+" of "+str(len(self.filtered[self.dimen]))+" values.")
        
        #     print(i)
        #     print(self.filterItemListWidget.item(i).checkState())
        #     print(self.filterItemListWidget.item(i).text())
        
    def setUp(self):
        self.dimen = mainW.diForFil
        self.sheet = mainW.data
        self.filtered = mainW.filDic
        # print("BF--------",self.filtered,self.filtered[self.dimen])
        if self.filtered[self.dimen] == "":
            self.filtered[self.dimen] = list(set(self.sheet[self.dimen].values))
        # print(self.filtered)
    
    def setList(self):
        _translate = QtCore.QCoreApplication.translate
        for i in self.sheet[self.dimen].drop_duplicates():
            # print(type(self.filtered[self.dimen]))
            item = QtWidgets.QListWidgetItem()
            if i in self.filtered[self.dimen] :
                item.setCheckState(QtCore.Qt.Checked) #2
            else:
                item.setCheckState(QtCore.Qt.Unchecked) #0
            self.filterItemListWidget.addItem(item)
        n=0
        for i in self.sheet[self.dimen].drop_duplicates():
            # print(str(i))
            item = self.filterItemListWidget.item(n)
            item.setText(_translate("MainWindow", str(i)))
            n+=1

class WebEngineView(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.page().profile().downloadRequested.connect(self.onDownloadRequested)
        # self.windows = win

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
            window.resize(500, 500)
            window.setCentralWidget(view)
            window.showMaximized()
            return view

    def updateChart(self, chart, **kwargs):
        output = StringIO()
        chart.save(output, "html", **kwargs)
        self.setHtml(output.getvalue())
        
class rowListClass(QtWidgets.QListWidget):
    def __init__(self,parent=None):
        super(rowListClass, self).__init__(parent)
        self.setAcceptDrops(True)
        # self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        
    def dragLeaveEvent(self,event) -> None:
        if self.count():
            if self.item(self.currentRow()) != None:
                mainW.filJustAdd = self.item(self.currentRow()).text()
            self.takeItem(self.currentRow())
            self.clearSelection()
        mainW.filChangeD()
        mainW.rowcolChangeD()
        # mainW.setChart()
        mainW.setplot()
        
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
        # if self.item(self.currentRow()) != None:
        #     mainW.filJustAdd = self.item(self.currentRow()).text()
        mainW.filChange()
        mainW.rowcolChange()
        # mainW.setChart()
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
        self.typeChart = ['Bar','Line', 'Pie']
        self.typeDate = ['Order Date','Ship Date']
        self.fileNameList = []
        self.selectFile = []
        self.dataSheet = ""
        self.data = ""
        self.filDic = {}
        self.RowChoose = []
        self.ColChoose = []
        self.Chart = None
        self.chartTypeS = ""
        self.diForFil = ''
        self.filJustAdd = ''
        
        # defind
        self.openDirecButton = self.findChild(QPushButton,"openDirecButton")
        
        self.RowList  = self.findChild(QListWidget,"RowList")
        self.ColList  = self.findChild(QListWidget,"ColList")
        self.RowList_2 = self.findChild(QListWidget,"RowList_2")
        self.ColList_2 = self.findChild(QListWidget,"ColList_2")
        
        self.filterList  = self.findChild(QListWidget,"filterList")
        self.filterList_2  = self.findChild(QListWidget,"filterList_2")
        
        self.dataSourceTable = self.findChild(QTableView,"table")
        self.dataSourceTable.horizontalHeader().setStretchLastSection(True)
        self.dataSourceTable.resizeColumnsToContents()
        self.dataSourceTable.resizeRowsToContents()
        
        self.sheetTable  = self.findChild(QTableView,"sheetTable")
        
        self.FileListDimension = self.findChild(QListWidget,"FileListDimension")
        self.FileListMes = self.findChild(QListWidget,"FileListMes")
        
        self.FileListDimension_2 = self.findChild(QListWidget,"FileListDimension_2")
        self.FileListMes_2 = self.findChild(QListWidget,"FileListMes_2")
        
        self.FileListChoose = self.findChild(FileChoose,"FileListChoose")
        
        self.chartType = self.findChild(QComboBox,"chartType")
        self.chartType_2 = self.findChild(QComboBox,"chartType_2")
        
        self.chartTab = self.findChild(QTabWidget,"chartTab")
        # QtWidgets.QMainWindow
        self.frame = self.findChild(QFrame,"frame")
        
        # function
        self.openDirecButton.clicked.connect(self.launchDialog)
        self.dataSourceTable.horizontalHeader().sectionClicked.connect(self.on_header_doubleClicked)
        self.filterList.installEventFilter(self)
        self.filterList.doubleClicked.connect(self.whichClicked)
        self.RowList.installEventFilter(self)
        self.ColList.installEventFilter(self)
        self.chartType_2.activated.connect(self.showChart)
        self.chartType.activated.connect(self.showChart)
        self.show()
        
    def whichClicked(self):
        filterItem = self.filterList.currentRow()
        strItem = self.filterList.item(filterItem)
        self.selectFil(strItem.text())
        
    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and (source is self.filterList or source is self.ColList or source is self.RowList):
            menu = QMenu()
            filterAc = menu.addAction('Filter')
            # menu.addAction('Action 2')
            # menu.addAction('Action 3')
            # if menu.exec_(event.globalPos()):
                # action = menu.exec_(self.mapToGlobal())
            if menu.exec_(event.globalPos()) == filterAc:
                item = source.itemAt(event.pos())
                self.selectFil(item.text())
            return True
        return super().eventFilter(source, event)
    
    def windowM(self):
        self.w = filterMesWindow()
        self.w.show()
        # self.hide()
    
    def windowD(self):                                             # <===
        self.w = filterDimenWindow()
        self.w.show()
        # self.hide()
        
    def selectFil(self,dimen):
        self.diForFil = dimen
        if dimen in self.Measure:
            self.windowM()
        else:
            self.windowD()
            
    def setplot(self):
        self.setSheetTable()
    
    def setChart(self):
        print("set chart")
        # print("--------R C",self.RowChoose,self.ColChoose)
        isInterRow = [value for value in self.RowChoose if value in self.Measure]
        isInterCol = [value for value in self.ColChoose if value in self.Measure]
        print("--------IR IC",isInterRow,isInterCol)
        self.typeChart = []
        if (len(isInterRow)>0 and len(isInterCol)==0) or (len(isInterCol)>0 and len(isInterRow)==0):
            # print("Have Mes")
            if (self.RowChoose != [] and self.ColChoose == []) or (self.RowChoose == [] and self.ColChoose != []) :
                if (len(self.RowChoose)-len(isInterRow) == 1 and len(isInterRow)>=1 and len(isInterCol)==0) or (len(self.ColChoose)-len(isInterCol) == 1 and len(isInterCol)>=1 and len(isInterRow)==0) :
                    self.typeChart = ['Bar', 'Pie']
                    # print("1 di")
                    for i in self.typeDate:
                        if i in self.RowChoose + self.ColChoose:
                            self.typeChart.append('Line')
                if (len(self.RowChoose)-len(isInterRow) == 2 and len(isInterRow)>=1 and len(isInterCol)==0) or (len(self.ColChoose)-len(isInterCol) == 2 and len(isInterCol)>=1 and len(isInterRow)==0) :
                    self.typeChart = ['Bar']
                    # print("2 di")
                    for i in self.typeDate:
                        if i in self.RowChoose + self.ColChoose:
                            self.typeChart.append('Line')
                if (len(self.RowChoose)-len(isInterRow) == 3 and len(isInterRow)>=1 and len(isInterCol)==0) or (len(self.ColChoose)-len(isInterCol) == 3 and len(isInterCol)>=1 and len(isInterRow)==0) :
                    self.typeChart = ['Bar']
                    # print("3 di")
        self.typeChart = list(set(self.typeChart))
        print("--->",self.typeChart)
        self.chartType.clear()
        self.chartType_2.clear()
        self.chartType.addItems(self.typeChart)
        self.chartType_2.addItems(self.typeChart)
        self.showChart()
    
    def showChart(self):
        vbox = QVBoxLayout()
        self.chartTypeS = self.chartType.currentText()
        print(self.chartTypeS)
        if self.chartTypeS != "": 
            # if self.chartTypeS != "":
            self.Chart = gm.chooseChart(str(self.chartTypeS))
            self.view = WebEngineView()
            # self.widget.setLayout(self.view)
            if self.Chart != None:
                self.view.updateChart(self.Chart)
                # self.view.show()
                vbox.addWidget(self.view)
                self.frame.setLayout(vbox)
                self.frame.show()
            
    def rowcolChangeD(self):
        tmpr = []
        tmpr =  [str(self.RowList.item(i).text()) for i in range(self.RowList.count())]
        tmpc = [] 
        tmpc =  [str(self.ColList.item(i).text()) for i in range(self.ColList.count())]
        tmpr2 = []
        tmpr2 =  [str(self.RowList_2.item(i).text()) for i in range(self.RowList_2.count())]
        tmpc2 = [] 
        tmpc2 =  [str(self.ColList_2.item(i).text()) for i in range(self.ColList_2.count())]
        
        # print(tmpr,tmpc,tmpr2,tmpc2)
        
        while (tmpr.count('')): tmpr.remove('')
        while (tmpr2.count('')): tmpr2.remove('')
        
        if tmpr == tmpr2 or len(tmpr) < len(tmpr2):
            # self.RowList.clear()
            # self.RowList.addItems(tmpr)
            # self.RowList_2.clear()
            # self.RowList_2.addItems(tmpr)
            self.RowChoose = tmpr
        else:
            # self.RowList.clear()
            # self.RowList.addItems(tmpr2)
            # self.RowList_2.clear()
            # self.RowList_2.addItems(tmpr2)
            self.RowChoose = tmpr2
        while (tmpc.count('')): tmpc.remove('')
        while (tmpc2.count('')): tmpc2.remove('')
        if tmpc == tmpc2 or len(tmpc) < len(tmpc2):
            # self.ColList.clear()
            # self.ColList.addItems(tmpc)
            # self.ColList_2.clear()
            # self.ColList_2.addItems(tmpc)
            self.ColChoose = tmpc
        else:
            # self.ColList.clear()
            # self.ColList.addItems(tmpc2)
            # self.ColList_2.clear()
            # self.ColList_2.addItems(tmpc2)
            self.ColChoose = tmpc2
            
        isInterRow = [value for value in self.RowChoose if value in self.Measure]
        isInterCol = [value for value in self.ColChoose if value in self.Measure]
        
        new_list = [i for i in self.RowChoose if i not in isInterRow]
        
        self.RowList.clear()
        self.RowList.addItems(new_list)
        self.RowList_2.clear()
        self.RowList_2.addItems(new_list)
        
        new_list = [i for i in self.ColChoose if i not in isInterCol]
        
        self.ColList.clear()
        self.ColList.addItems(new_list)
        self.ColList_2.clear()
        self.ColList_2.addItems(new_list)
        
    def filChangeD(self):
        # print("Just D ",self.filJustAdd)
        # print(self.filDic)
        itemsTextList =  [str(self.filterList.item(i).text()) for i in range(self.filterList.count())]
        itemsTextList_2 =  [str(self.filterList_2.item(i).text()) for i in range(self.filterList_2.count())]
        itemsTextList =  list(set(itemsTextList))
        itemsTextList_2 =  list(set(itemsTextList_2))
        # print(itemsTextList,itemsTextList_2)
        while (itemsTextList.count('')):
            itemsTextList.remove('')
        while (itemsTextList_2.count('')):
            itemsTextList_2.remove('')
        if not(itemsTextList == [] and itemsTextList_2 == []):
            if itemsTextList == itemsTextList_2 or len(itemsTextList) < len(itemsTextList_2):
                self.filterList.clear()
                self.filterList.addItems(itemsTextList)
                self.filterList_2.clear()
                self.filterList_2.addItems(itemsTextList)
                
            else:
                self.filterList.clear()
                self.filterList.addItems(itemsTextList_2)
                self.filterList_2.clear()
                self.filterList_2.addItems(itemsTextList_2)
            
            if self.filJustAdd in self.filDic.keys():
                del self.filDic[self.filJustAdd]
         
    def rowcolChange(self):
        tmpr = []
        tmpr =  [str(self.RowList.item(i).text()) for i in range(self.RowList.count())]
        tmpc = [] 
        tmpc =  [str(self.ColList.item(i).text()) for i in range(self.ColList.count())]
        tmpr2 = []
        tmpr2 =  [str(self.RowList_2.item(i).text()) for i in range(self.RowList_2.count())]
        tmpc2 = [] 
        tmpc2 =  [str(self.ColList_2.item(i).text()) for i in range(self.ColList_2.count())]
        # print(tmpr,tmpc,tmpr2,tmpc2)
        
        while (tmpr.count('')): tmpr.remove('')
        while (tmpr2.count('')): tmpr2.remove('')
        if tmpr == tmpr2 or len(tmpr) > len(tmpr2):
            self.RowList.clear()
            self.RowList.addItems(tmpr)
            self.RowList_2.clear()
            self.RowList_2.addItems(tmpr)
            self.RowChoose = tmpr
        else:
            self.RowList.clear()
            self.RowList.addItems(tmpr2)
            self.RowList_2.clear()
            self.RowList_2.addItems(tmpr2)
            self.RowChoose = tmpr2
        
        while (tmpc.count('')): tmpc.remove('')
        while (tmpc2.count('')): tmpc2.remove('')
        if tmpc == tmpc2 or len(tmpc) > len(tmpc2):
            self.ColList.clear()
            self.ColList.addItems(tmpc)
            self.ColList_2.clear()
            self.ColList_2.addItems(tmpc)
            self.ColChoose = tmpc
        else:
            self.ColList.clear()
            self.ColList.addItems(tmpc2)
            self.ColList_2.clear()
            self.ColList_2.addItems(tmpc2)
            self.ColChoose = tmpc2
        self.setChart()
        
    def filChange(self):
        # print(self.filDic)
        itemsTextList =  [str(self.filterList.item(i).text()) for i in range(self.filterList.count())]
        itemsTextList_2 =  [str(self.filterList_2.item(i).text()) for i in range(self.filterList_2.count())]
        itemsTextList =  list(set(itemsTextList))
        itemsTextList_2 =  list(set(itemsTextList_2))
        # print(itemsTextList,itemsTextList_2)
        while (itemsTextList.count('')):
            itemsTextList.remove('')
        while (itemsTextList_2.count('')):
            itemsTextList_2.remove('')
        if not(itemsTextList == [] and itemsTextList_2 == []):
            if itemsTextList == itemsTextList_2 or len(itemsTextList) > len(itemsTextList_2):
                self.filterList.clear()
                self.filterList.addItems(itemsTextList)
                self.filterList_2.clear()
                self.filterList_2.addItems(itemsTextList)
                for i in itemsTextList:
                    if i not in list(self.filDic.keys()):
                        self.filDic[i] = ""
            else:
                self.filterList.clear()
                self.filterList.addItems(itemsTextList_2)
                self.filterList_2.clear()
                self.filterList_2.addItems(itemsTextList_2)
                for i in itemsTextList_2:
                    if i not in list(self.filDic.keys()):
                        self.filDic[i] = ""
        # print(itemsTextList,itemsTextList_2)
        # print(self.filDic)
        
    def setSheetTable(self):
        isInterRow = list(set.intersection(set(self.RowChoose),set(self.Measure)))
        isInterCol = list(set.intersection(set(self.ColChoose),set(self.Measure)))
        if self.selectFile != [] : 
            self.sheetPageRowAndCol(self.RowChoose,self.ColChoose)
            self.model = TableModel2(self.dataSheet)
            if (self.RowChoose == [] and self.ColChoose == []) or (isInterRow != [] and isInterCol != []):
                self.sheetTable.setModel(None)
            else:
                self.sheetTable.setModel(self.model)
    
    def sheetPageRowAndCol(self,Row,Col):
        # print("Start",Row,Col,len(set(Row)),len(set(Col)))
        if Row!=[] or Col!=[]:
            cm.filter = self.filDic
            # print("BF table",self.filDic)
            self.dataSheet = cm.setRowAndColumn(Row,Col)
          
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
            
            self.FileListDimension_2.clear()
            self.FileListDimension_2.addItems(self.colHeader)
            
            self.FileListMes_2.clear()
            self.FileListMes_2.addItems([])
        self.dataSource()
        
    def setTable(self):
        # print("set data")
        # print(self.selectFile)
        if self.selectFile != [] : 
            self.dataSource()
            # print(self.data)
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
        if self.FileListChoose != None :
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
        self.FileListDimension.clear()
        self.FileListDimension.addItems(self.colHeader)
        self.FileListDimension_2.clear()
        self.FileListDimension_2.addItems(self.colHeader)
        self.FileListMes_2.clear()
        self.FileListMes_2.addItems(self.Measure)
        self.FileListMes.clear()
        self.FileListMes.addItems(self.Measure)

app = QApplication(sys.argv)
# widget = QtWidgets.QStackedWidget()
gm = graphManager.graphManager()
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
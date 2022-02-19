import os
import sys
from PyQt5.QtCore import Qt,QEvent
import csvManager as cmpage
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import uic,QtCore,QtWebEngineWidgets,QtGui
# from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from Altair_Graph.Bar_Chart import WebEngineView
from io import StringIO
import graphManager 

import altair as alt
import altair_viewer
from vega_datasets import data

class filterMesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("filterMes.ui",self)
        self.show()
        self.dimen = ''
        self.minVa = ''
        self.maxVa = ''
        self.sheet = ''
        self.filtered = {}
        self.checkedList = []
        
        # defind
        self.atLeatSlider = self.findChild(QSlider,"atLeatSlider")
        self.atMostSlider = self.findChild(QSlider,"atMostSlider")
        self.atLeatSlider_2 = self.findChild(QSlider,"atLeatSlider_2")
        self.atMostSlider_2 = self.findChild(QSlider,"atMostSlider_2")
        
        self.rangeMax = self.findChild(QLineEdit,"rangeMax")
        self.rangeMin = self.findChild(QLineEdit,"rangeMin")
        self.atLeastMax = self.findChild(QLineEdit,"atLeastMax")
        self.atLeastMin = self.findChild(QLineEdit,"atLeastMin")
        self.atMostMax = self.findChild(QLineEdit,"atMostMax")
        self.atMosttMin = self.findChild(QLineEdit,"atMostMin")
        
        self.atLeastValueLabel = self.findChild(QLabel,"atLeastValueLabel")
        self.atMostValueLabel = self.findChild(QLabel,"atMostValueLabel")
        self.atLeastValueLabel_2 = self.findChild(QLabel,"atLeastValueLabel_2")
        self.atMostValueLabel_2 = self.findChild(QLabel,"atMostValueLabel_2")
        self.atLeastValueLabel_3 = self.findChild(QLabel,"atLeastValueLabel_3")
        self.atMostValueLabel_3 = self.findChild(QLabel,"atMostValueLabel_3")
        
        self.setUp()
        
    def setUp(self):
        self.dimen = mainW.diForFil
        self.sheet = mainW.data
        self.filtered = mainW.filDic
        if self.filtered[self.dimen] == "":
            self.filtered[self.dimen] = [self.sheet[self.dimen].min(),self.sheet[self.dimen].max()]
        self.maxVa = str(self.sheet[self.dimen].max())
        self.minVa = str(self.sheet[self.dimen].min())
        self.setValues()
    
    def setValues(self):
        # print(self.minVa,self.maxVa)
        self.rangeMin.setText(str(self.filtered[self.dimen][0]))
        self.rangeMax.setText(str(self.filtered[self.dimen][1]))
        self.atLeastMax.setText(str(self.filtered[self.dimen][1]))
        self.atLeastMin.setText(str(self.filtered[self.dimen][0]))
        self.atMostMax.setText(str(self.filtered[self.dimen][1]))
        self.atMosttMin.setText(str(self.filtered[self.dimen][0]))
        
        self.atLeastValueLabel.setText(self.minVa)
        self.atMostValueLabel.setText(self.maxVa)
        self.atLeastValueLabel_2.setText(self.minVa)
        self.atMostValueLabel_2.setText(self.maxVa)
        self.atLeastValueLabel_3.setText(self.minVa)
        self.atMostValueLabel_3.setText(self.maxVa)
                
class filterDimenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("filterDimen.ui",self)
        self.show()
        self.dimen = ''
        self.sheet = ''
        self.filtered = {}
        self.checkedList = []
        self.isInterRow = []        
        self.isInterCol = []
        
        # defind
        self.allButton = self.findChild(QPushButton,"allButton")
        self.filterItemListWidget = self.findChild(QListWidget,"filterItemListWidget")
        self.noneButton = self.findChild(QPushButton,"noneButton")
        self.fieldLabel = self.findChild(QLabel,"fieldLabel")
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
        
        self.selectionLabel.setText("Selection : "+ str(len(self.checkedList))+" of "+str(len(mainW.data[self.dimen].drop_duplicates))+" values.")
        
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
    # Disabling MaxRowsError
    alt.data_transformers.disable_max_rows()
    altair_viewer._global_viewer._use_bundled_js = False
    alt.data_transformers.enable('data_server')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.page().profile().downloadRequested.connect(self.onDownloadRequested)
        self.windows = []
        # self.setZoomFactor(1.24) # 0.25 to 5

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
        chart.save(output,'html', embed_options={'renderer':'svg'})
        self.setHtml(output.getvalue())
        
class colListClass(QtWidgets.QListWidget):
    def __init__(self,parent=None):
        super(colListClass, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        # self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        
    def dragLeaveEvent(self,event) -> None:
        if self.count():
            if self.item(self.currentRow()) != None:
                mainW.filJustAdd = self.item(self.currentRow()).text()
            self.takeItem(self.currentRow())
            self.clearSelection()
        # mainW.filChangeD()
        mainW.rowcolChange()
        # mainW.setChart()
        # mainW.setplot()

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
        # mainW.filChange()
        mainW.rowcolChange()
        # mainW.setChart()
        # mainW.setplot()
        
class rowListClass(QtWidgets.QListWidget):
    def __init__(self,parent=None):
        super(rowListClass, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        # self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        
    def dragLeaveEvent(self,event) -> None:
        if self.count():
            if self.item(self.currentRow()) != None:
                mainW.filJustAdd = self.item(self.currentRow()).text()
            self.takeItem(self.currentRow())
            self.clearSelection()
        # mainW.filChangeD()
        mainW.rowcolChange()
        # mainW.setChart()
        # mainW.setplot()

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
        # mainW.filChange()
        mainW.rowcolChange()
        # mainW.setChart()
        # mainW.setplot()
        
class filListClass(QtWidgets.QListWidget):
    def __init__(self,parent=None):
        super(filListClass, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        # self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        
    def dragLeaveEvent(self,event) -> None:
        if self.count():
            if self.item(self.currentRow()) != None:
                mainW.filJustAdd = self.item(self.currentRow()).text()
            self.takeItem(self.currentRow())
            self.clearSelection()
        mainW.filChangeD()
        # mainW.rowcolChange()
        # # mainW.setChart()
        mainW.setplot()

    # def dragMoveEvent(self, event):
    #     #if event.mimeData().hasUrls():
    #     event.accept()
            
    def dropEvent(self, QDropEvent):
        source_Widget=QDropEvent.source()
        items=source_Widget.selectedItems()
        # QDropEvent.setDropAction(QtCore.Qt.MoveAction)
        for i in items:
            source_Widget.takeItem(source_Widget.indexFromItem(i).row())
            self.addItem(i)
        mainW.setFileListDimension()
        mainW.filChange()
        # mainW.rowcolChange()
        # # mainW.setChart()
        mainW.setplot()
            
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
        self.Measure = {'Sales':"sum",'Quantity':"sum",'Discount':"sum",'Profit':"sum"}
        
        self.typeChart = ['Bar','Line', 'Pie']
        self.typeDate = [['Order Date',"month"],['Ship Date',"month"]]
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
        
        self.RowList = self.findChild(rowListClass,"RowList")
        self.ColList  = self.findChild(colListClass,"ColList")
        
        self.filterList  = self.findChild(filListClass,"filterList")
        
        self.dataSourceTable = self.findChild(QTableView,"table")
        self.dataSourceTable.horizontalHeader().setStretchLastSection(True)
        self.dataSourceTable.resizeColumnsToContents()
        self.dataSourceTable.resizeRowsToContents()
        
        self.sheetTable  = self.findChild(QTableView,"sheetTable")
        
        self.FileListDimension = self.findChild(QListWidget,"FileListDimension")
        self.FileListMes = self.findChild(QListWidget,"FileListMes")
        
        
        self.FileListChoose = self.findChild(FileChoose,"FileListChoose")
        
        self.chartType = self.findChild(QComboBox,"chartType")
        
        self.tabWidget_2 = self.findChild(QTabWidget,"tabWidget_2")
        
        self.widget = self.findChild(QWidget,"widget")
        
        self.gridLayout_11 = self.findChild(QGridLayout,"gridLayout_11")
        self.gridLayout_11.addWidget(self.widget, 0, 0, 1, 1)
            
        # function
        self.openDirecButton.clicked.connect(self.launchDialog)
        self.dataSourceTable.horizontalHeader().sectionClicked.connect(self.on_header_doubleClicked)
        if self.filterList != None:
            self.filterList.installEventFilter(self)
            self.filterList.doubleClicked.connect(self.whichClicked)
        if self.RowList != None:
            self.RowList.installEventFilter(self)
        if self.ColList != None:
            self.ColList.installEventFilter(self)
        self.chartType.activated.connect(self.showChart)
        self.showMaximized()
        
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
                if item.text() not in list(self.filDic.keys()):
                    tmpr =  [str(self.filterList.item(i).text()) for i in range(self.filterList.count())]
                    tmpr.append(item.text())
                    self.filterList.addItems(tmpr)
                    self.filDic[item.text()] = ""
                    print(self.filDic)
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
        if dimen in list(self.Measure.keys()):
            self.windowM()
        else:
            self.windowD()
            
    def setplot(self):
        print("--------R C",self.RowChoose,self.ColChoose)
        self.setSheetTable()
        self.setChart()
        self.showChart()
    
    def setChart(self):
        # print("set chart")
        # print("--------R C",self.RowChoose,self.ColChoose)
        # self.isInterRow = [value for value in self.RowChoose if value in [self.Measure.keys()]]
        # self.isInterCol = [value for value in self.ColChoose if value in [self.Measure.keys()]]
        # print("--------IR IC",self.isInterRow,self.isInterCol)
        gm.setList(self.RowChoose,self.ColChoose,self.Measure,self.data)
        self.typeChart = []
        print("--->",self.typeChart)
        if len(self.isInterRow)>0 or len(self.isInterCol)>0 :
            # if (len(self.isInterRow)>0 and len(self.isInterCol)==0) or (len(self.isInterCol)>0 and len(self.isInterRow)==0):
            self.typeChart = ['Bar']
            # print("Have Mes")
            # if (self.RowChoose != [] and self.ColChoose == []) or (self.RowChoose == [] and self.ColChoose != []) :
            
            #     if (len(self.RowChoose)-len(self.isInterRow) == 1 and (len(self.isInterRow)>=1 or len(self.isInterCol)>=1) ) or (len(self.ColChoose)-len(self.isInterCol) == 1 and (len(self.isInterRow)>=1 or len(self.isInterCol)>=1) ) :
            #         self.typeChart = ['Bar', 'Pie']
            #         # print("1 di")
            #         for i in self.typeDate:
            #             if i in self.RowChoose + self.ColChoose:
            #                 self.typeChart.append('Line')
            #     if (len(self.RowChoose)-len(self.isInterRow) == 2 and (len(self.isInterRow)>=1 or len(self.isInterCol)>=1)) or (len(self.ColChoose)-len(self.isInterCol) == 2 and (len(self.isInterRow)>=1 or len(self.isInterCol)>=1) ) :
            #         self.typeChart = ['Bar']
            #         # print("2 di")
            #         for i in self.typeDate:
            #             if i in self.RowChoose + self.ColChoose:
            #                 self.typeChart.append('Line')
            #     if (len(self.RowChoose)-len(self.isInterRow) == 3 and (len(self.isInterRow)>=1 or len(self.isInterCol)>=1) ) or (len(self.ColChoose)-len(self.isInterCol) == 3 and (len(self.isInterRow)>=1 or len(self.isInterCol)>=1) ) :
            #         self.typeChart = ['Bar']
            #         # print("3 di")
        
        self.typeChart = list(set(self.typeChart))
        self.typeChart = sorted(self.typeChart)
        # print("--->",self.typeChart)
        self.chartType.clear()
        self.chartType.addItems(self.typeChart)
        # self.chartType_2.addItems(self.typeChart)
        if self.typeChart != []:
            self.showChart()
    
    def showChart(self):
        # vbox = QtWidgets.QVBoxLayout(self)
        # vbox.setContentsMargins(0, 0, 0, 0)
        self.chartTypeS = self.chartType.currentText()
        # print(self.chartTypeS)
        
        if self.chartTypeS != "": 
            # if self.chartTypeS != "":
            gm.setList(self.RowChoose,self.ColChoose,self.Measure,self.data)
            self.Chart = gm.chooseChart(str(self.chartTypeS))
            
            self.view = WebEngineView()
            # self.widget.setLayout(self.view)
            if self.Chart != None:
                # print(type(self.Chart))
                self.view.updateChart(self.Chart)
                # self.view.show()
                # vbox.addWidget(self.view)
            
    def rowcolChange(self):
        tmpr = []
        tmpr =  [str(self.RowList.item(i).text()) for i in range(self.RowList.count())]
        tmpc = [] 
        tmpc =  [str(self.ColList.item(i).text()) for i in range(self.ColList.count())]
        
        # print("Before",tmpr,tmpc)
        
        while (tmpr.count('')): tmpr.remove('')
        while (tmpc.count('')): tmpc.remove('')
        
        self.RowChoose = tmpr
        self.ColChoose = tmpc

        self.isInterRow = [value for value in self.RowChoose if value in list(self.Measure.keys())]
        self.isInterCol = [value for value in self.ColChoose if value in list(self.Measure.keys())]
        
        for i in self.isInterRow:
            if i in tmpr:
                tmpr.remove(i)
        tmpr += self.isInterRow
        
        for i in self.isInterCol:
            if i in tmpc:
                tmpc.remove(i)
        tmpc += self.isInterCol
            
        self.ColList.clear()
        self.ColList.addItems(tmpc)
        
        self.RowList.clear()
        self.RowList.addItems(tmpr)
        
        for i in range(len(tmpr)):
            self.RowList.item(i).setForeground(QtGui.QColor('white'))
            if str(self.RowList.item(i).text()) in list(self.Measure.keys()):
                self.RowList.item(i).setBackground(QtGui.QColor('green'))
            else: 
                self.RowList.item(i).setBackground(QtGui.QColor('blue'))
            
        for i in range(len(tmpc)):
            self.ColList.item(i).setForeground(QtGui.QColor('white'))
            if str(self.ColList.item(i).text()) in list(self.Measure.keys()):
                self.ColList.item(i).setBackground(QtGui.QColor('green'))
            else: 
                self.ColList.item(i).setBackground(QtGui.QColor('blue'))
                
        self.RowChoose = tmpr
        self.ColChoose = tmpc
        
        # print("After",tmpr,tmpc)
        # tmpr2 = []
        # tmpr2 =  [str(self.RowList.item(i).text()) for i in range(self.RowList.count())]
        # tmpc2 = [] 
        # tmpc2 =  [str(self.ColList.item(i).text()) for i in range(self.ColList.count())]
        
        # print("Before",tmpr2,tmpc2)
        self.setplot()
        
    def filChangeD(self):
        if self.filJustAdd in self.filDic.keys():
            del self.filDic[self.filJustAdd]
        self.filChange()
        
    def filChange(self):
        
        #print(self.filDic)
        itemsTextList =  [str(self.filterList.item(i).text()) for i in range(self.filterList.count())]
        itemsTextList =  list(set(itemsTextList))
        # print(itemsTextList)
        
        while (itemsTextList.count('')):
            itemsTextList.remove('')
            
        if itemsTextList != []:
                self.filterList.clear()
                self.filterList.addItems(itemsTextList)
                
                for i in itemsTextList:
                    if i not in list(self.filDic.keys()):
                        self.filDic[i] = ""
        # print(self.filDic)
        
    def setSheetTable(self):
        # self.isInterRow = [value for value in self.RowChoose if value in list(self.Measure.keys())]
        # self.isInterCol = [value for value in self.ColChoose if value in list(self.Measure.keys())]
        print(self.RowChoose,self.ColChoose)
        if self.selectFile != [] : 
            # print(not(self.RowChoose == [] and self.ColChoose == []))
            if self.RowChoose == [] and self.ColChoose == []:
                self.sheetTable.setModel(None)
            else:
                self.sheetPageRowAndCol(self.RowChoose,self.ColChoose)
                self.model = TableModel2(self.dataSheet)
                # print(self.RowChoose,self.ColChoose)
                # print("in")
                # print(type(self.model))
                # print(self.model)
                if self.isInterRow != [] and self.isInterCol !=[]:
                    self.sheetTable.setModel(None)
                else:
                    self.sheetTable.setModel(self.model)
        print("Row Col after set sheet",self.RowChoose,self.ColChoose)
    
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
                
                for i in list(self.Measure.keys()):
                    if i in self.colHeader:
                        self.colHeader.remove(i)
                self.setFileListDimension()
                self.model = TableModel(self.data)
                self.dataSourceTable.setModel(self.model)
            else:
                print("Not Union")
                cm.path =self.folderpath
                cm.selectFile = self.selectFile[0] 
                cm.setPath()
                self.data = cm.getDataWithPandas()
                self.model = TableModel(self.data)
                self.dataSourceTable.setModel(self.model)
        else:
            self.RowList.clear()
            self.ColList.clear()
            self.RowChoose = []
            self.ColChoose = []
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
        print(response)
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
        if self.selectFile in tmp:
            tmp.remove(self.selectFile)
        #print(tmp)
        self.fileNameList = tmp
        self.path = os.path.join(self.folderpath,self.selectFile)
        cm.path = self.folderpath
        cm.selectFile = self.selectFile
        cm.setPath()
        # print(self.selectFile,self.data)
        # print(response[0])
        if response[0] != "":
            self.dataSource()
            self.colHeader = cm.getHead()
            for i in list(self.Measure.keys()):
                if i in self.colHeader:
                    self.colHeader.remove(i)
                
            self.setFileListDimension()
            self.setFileInDirectory()
            self.setFileChoose()
        
    def setFileListDimension(self):
        self.FileListDimension.clear()
        self.FileListDimension.addItems(self.colHeader)
        # self.FileListDimension_2.clear()
        # self.FileListDimension_2.addItems(self.colHeader)
        # self.FileListMes_2.clear()
        # self.FileListMes_2.addItems(list(self.Measure.keys()))
        self.FileListMes.clear()
        self.FileListMes.addItems(list(self.Measure.keys()))

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
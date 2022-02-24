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
        self.original = {}
        self.filtered = {}
        self.checkedList = []
        self.row = []
        self.col = []
        
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
        self.atMostMin = self.findChild(QLineEdit,"atMostMin")
        
        self.atLeastValueLabel = self.findChild(QLabel,"atLeastValueLabel")
        self.atMostValueLabel = self.findChild(QLabel,"atMostValueLabel")
        self.atLeastValueLabel_2 = self.findChild(QLabel,"atLeastValueLabel_2")
        self.atMostValueLabel_2 = self.findChild(QLabel,"atMostValueLabel_2")
        self.atLeastValueLabel_3 = self.findChild(QLabel,"atLeastValueLabel_3")
        self.atMostValueLabel_3 = self.findChild(QLabel,"atMostValueLabel_3")
        
        self.resetButton = self.findChild(QPushButton,"resetButton")
        self.applyButton = self.findChild(QPushButton,"applyButton")
        self.cancleButton = self.findChild(QPushButton,"cancleButton")
        
        #  func
        self.atLeatSlider.valueChanged.connect(self.valuechange)
        self.atMostSlider.valueChanged.connect(self.valuechange1)
        self.atLeatSlider_2.valueChanged.connect(self.valuechange2)
        self.atMostSlider_2.valueChanged.connect(self.valuechange3)
        
        self.rangeMin.textChanged.connect(self.rangeMinchange)
        self.rangeMax.textChanged.connect(self.rangeMaxchange)
        self.atLeastMax.textChanged.connect(self.atLeastMaxchange)
        self.atLeastMin.textChanged.connect(self.atLeastMinchange)
        self.atMostMax.textChanged.connect(self.atMostMaxchange)
        self.atMostMin.textChanged.connect(self.atMostMinchange)
        
        self.resetButton.clicked.connect(self.resetBut)
        self.cancleButton.clicked.connect(self.cancleBut)
        self.applyButton.clicked.connect(self.ApplyBut)
        
        self.setUp()
    
    def ApplyBut(self):
        mainW.filDic = self.filtered
        # mainW.dataSheet = mainW.dataSheet.loc[mainW.dataSheet[self.dimen] > self.filtered[self.dimen][0]]
        # mainW.dataSheet = mainW.dataSheet.loc[mainW.dataSheet[self.dimen] < self.filtered[self.dimen][1]] 
        mainW.setChart()
        mainW.showChart()
        mainW.showSheet()
        self.close()
        
    def cancleBut(self):
        self.close()
        
    def resetBut(self):
        self.setUp()
        self.setValues()
        
    def rangeMaxchange(self):
        self.filtered[self.dimen][1] =self.rangeMax.text()
        self.setValues()
    
    def rangeMinchange(self):
        self.filtered[self.dimen][0] =self.rangeMin.text()
        self.setValues()
        
    def atLeastMaxchange(self):
        self.filtered[self.dimen][1] =self.atLeastMax.text()
        self.setValues()
    
    def atLeastMinchange(self):
        self.filtered[self.dimen][0] =self.atLeastMin.text()
        self.setValues()
        
    def atMostMaxchange(self):
        self.filtered[self.dimen][1] =self.atMostMax.text()
        self.setValues()
    
    def atMostMinchange(self):
        self.filtered[self.dimen][0] =self.atMostMin.text()
        self.setValues()
        
    def valuechange(self):
        atLeatSlider = float(self.atLeatSlider.value())
        atMostSlider = float(self.atMostSlider.value())
        self.filtered[self.dimen][0] = atLeatSlider
        if atLeatSlider >= atMostSlider:
            self.filtered[self.dimen][1] = atLeatSlider
        self.setValues()
        
    def valuechange1(self):
        atMostSlider = float(self.atMostSlider.value())
        atLeatSlider = float(self.atLeatSlider.value())
        self.filtered[self.dimen][1] = atMostSlider
        if atMostSlider <= atLeatSlider:
            self.filtered[self.dimen][0] = atMostSlider
        self.setValues()
        
    def valuechange2(self):
        atLeatSlider = float(self.atLeatSlider_2.value())
        self.filtered[self.dimen][0] = atLeatSlider
        # self.filtered[self.dimen][1] = self.maxVa
        self.setValues()
    
    def valuechange3(self):
        atMostSlider_2 = float(self.atMostSlider_2.value())
        self.filtered[self.dimen][1] = atMostSlider_2
        # self.filtered[self.dimen][0] = self.minVa
        self.setValues()
    
    def setRC(self):
        self.row = mainW.RowChoose
        self.col = mainW.ColChoose
        for i in range(len(self.row)):
            if type(self.row[i]) == list:
                self.row[i] = self.row[i][0]
        for i in range(len(self.col)):
            if type(self.col[i]) == list:
                self.col[i] = self.col[i][0]
                
    def setUp(self):
        self.dimen = mainW.diForFil
        self.setRC()
        # print(self.dimen,mainW.RowChoose,mainW.ColChoose)
        if (self.dimen in self.row) or (self.dimen in self.col):
            # print("K")
            self.sheet = mainW.dataSheet
        else :
            # print("J")
            self.sheet = mainW.data
        self.filtered = mainW.filDic
        print("start",self.filtered)
        if self.filtered[self.dimen] == "" or len(self.filtered[self.dimen])>2:
            self.filtered[self.dimen] = [min(self.sheet[self.dimen]),max(self.sheet[self.dimen])]
        print("set up",self.filtered)
        self.maxVa = float(max(self.sheet[self.dimen]))
        self.minVa = float(min(self.sheet[self.dimen]))
        # print(self.dimen)
        # print(self.filtered)
        format(self.maxVa, '.2f')
        format(self.minVa, '.2f')
        
        maxVa = float(max(self.sheet[self.dimen]))
        minVa = float(min(self.sheet[self.dimen]))
        format(maxVa, '.2f')
        format(minVa, '.2f')
        
        sliderLList = [self.atLeatSlider,self.atLeatSlider_2]
        sliderMList = [self.atMostSlider,self.atMostSlider_2]
        
        for i,j in zip(sliderLList,sliderMList):
            i.setMinimum(minVa)
            i.setMaximum(maxVa)
            j.setMinimum(minVa)
            j.setMaximum(maxVa)
            i.setValue(minVa)
            j.setValue(maxVa)
            
        self.atLeastValueLabel.setText(str(self.minVa))
        self.atMostValueLabel.setText(str(self.maxVa))
        self.atLeastValueLabel_2.setText(str(self.minVa))
        self.atMostValueLabel_2.setText(str(self.maxVa))
        self.atLeastValueLabel_3.setText(str(self.minVa))
        self.atMostValueLabel_3.setText(str(self.maxVa))
            # i.setValue(minVa)
        # print(self.filtered,self.original)
        self.setValues()
    
    def setValues(self):
        # print(self.filtered)
        # print(self.minVa,self.maxVa)
        # print(self.dimen,self.filtered)
        self.rangeMax.setText(str(float(self.filtered[self.dimen][1])))
        self.rangeMin.setText(str(float(self.filtered[self.dimen][0])))
        self.atLeastMax.setText(str(float(self.filtered[self.dimen][1])))
        self.atLeastMin.setText(str(float(self.filtered[self.dimen][0])))
        self.atMostMax.setText(str(float(self.filtered[self.dimen][1])))
        self.atMostMin.setText(str(float(self.filtered[self.dimen][0])))
        # print("set value",self.filtered)
        self.atMostSlider.setValue(float(self.filtered[self.dimen][1]))
        self.atMostSlider_2.setValue(float(self.filtered[self.dimen][1]))
        self.atLeatSlider.setValue(float(self.filtered[self.dimen][0]))
        self.atLeatSlider_2.setValue(float(self.filtered[self.dimen][0]))
                
class filterDimenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("filterDimen.ui",self)
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
        self.show()
    
    def ApplyBut(self):
        self.filtered[self.dimen] = self.checkedList
        mainW.filDic = self.filtered
        print(mainW.filDic)
        mainW.setplot()
        # mainW.setSheetTable()
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
        if strItem != None:
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
        cc = []
        ck = []
        for i in range(self.filterItemListWidget.count()):
            if self.filterItemListWidget.item(i).checkState() == 2:
                self.checkedList.append(self.filterItemListWidget.item(i).text())
            cc.append(self.filterItemListWidget.item(i).checkState())
            ck.append(self.filterItemListWidget.item(i).text())
        # print(cc)
        # print(ck)
        
    def setUp(self):
        print("Filter Page",mainW.diForFil)
        self.dimen = mainW.getPlainText(mainW.diForFil)
        self.sheet = cm.df
        self.filtered = mainW.filDic
        print("BF--------",self.filtered)
        # self.setList()
    
    def setList(self):
        _translate = QtCore.QCoreApplication.translate
        # print("Check",self.dimen,mainW.typeDate.keys())
        if self.dimen not in list(mainW.typeDate.keys()):
            print("Di")
            print(self.dimen)
            print(self.filtered[self.dimen])
            for i in self.sheet[self.dimen].drop_duplicates().to_list():
                # print(type(self.filtered[self.dimen]))
                item = QtWidgets.QListWidgetItem()
                if i in self.filtered[self.dimen] :
                    item.setCheckState(QtCore.Qt.Checked) #2
                else:
                    item.setCheckState(QtCore.Qt.Unchecked) #0
                self.filterItemListWidget.addItem(item)
            n=0
            for i in self.sheet[self.dimen].drop_duplicates().to_list():
                # print(str(i))
                item = self.filterItemListWidget.item(n)
                item.setText(_translate("MainWindow", str(i)))
                n+=1
        else:
            print("Date")
            # print(self.filtered[self.dimen])
            print(cm.df[self.dimen+' '+mainW.typeDate[self.dimen]].drop_duplicates().to_list())
            for i in cm.df[self.dimen+' '+mainW.typeDate[self.dimen]].drop_duplicates().to_list():
                # print(i)
                
                print(self.dimen)
                print(self.filtered[self.dimen])
                
                self.item2 = QtWidgets.QListWidgetItem()
                if i in self.filtered[self.dimen] :
                    # print("Check ////")
                    self.item2.setCheckState(QtCore.Qt.Checked) #2
                else:
                    self.item2.setCheckState(QtCore.Qt.Unchecked) #0
                self.filterItemListWidget.addItem(self.item2)
            n=0
            for i in cm.df[self.dimen+' '+mainW.typeDate[self.dimen]].drop_duplicates().to_list():
                # print(str(i))
                self.item2 = self.filterItemListWidget.item(n)
                self.item2.setText(_translate("MainWindow", str(i)))
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
            # window.resize(1000, 1000)
            # window.setCentralWidget(view)
            # window.showFullScreen()
            return view

    def updateChart(self, chart, **kwargs):
        output = StringIO()
        chart.save(output,'html', **kwargs)
        # chart.save(output,'html', embed_options={'renderer':'svg'})
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
            mainW.filJustAdd = i.text()
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
                # if self._data.size != 0:
                # print(self._data.columns)
                # print("---------head--------",self._data.columns[section])
                if type(self._data.columns[section]) == tuple:
                    self._data.columns[section] = tuple(map( str , self._data.columns[section]) )
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
                    head = self._data.index.names # [None,0,1,2... Row-1]
                    # print("hxh")
                    # print("head ---------" , head)
                    head = [ "%s" % x for x in list(head) ]
                    if len(head) > 1 :
                        head = ["\\".join(head)]
                    # print(head)
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
        # self.Measure = {'Sales':"sum",'Quantity':"sum",'Discount':"sum",'Profit':"sum"}
        self.Measure = {}
        self.isInterRow = ''
        self.isInterCol = ''
        self.typeChart = ['Bar','Line', 'Pie']
        self.typeDate = {}
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
        self.dfOriginal = None
        
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
        
        self.FileList = self.findChild(FileInDirec,"FileList")
        self.FileListChoose = self.findChild(FileChoose,"FileListChoose")
        self.chartType = self.findChild(QComboBox,"chartType")
        
        # self.tabWidget_2 = self.findChild(QTabWidget,"tabWidget_2")
        
        # self.frame = self.findChild(QFrame,"frame")
        self.view = WebEngineView()
        self.vbox = QVBoxLayout(self.frame)
        self.vbox.addWidget(self.view)
        # self.vbox.SetMaximumSize()
        
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
            
        self.FileListDimension.installEventFilter(self)
        self.FileListMes.installEventFilter(self)
              
        self.chartType.activated.connect(self.showChart)
        # self.show()
        
    def whichClicked(self):
        filterItem = self.filterList.currentRow()
        strItem = self.filterList.item(filterItem)
        self.selectFil(strItem.text())
    
    def clickFunc(self):
        menu = self.sender()
        pt = self.getPlainText(str(self.item2.text()))
        # print(menu.text().lower())
        if pt in list(self.typeDate.keys()):
            self.typeDate[pt] = menu.text().lower()
            self.subMenuDate.setTitle(pt+'('+self.typeDate[pt]+')')
        if pt in list(self.Measure.keys()):
            self.Measure[pt] = menu.text().lower()
            self.subMenu.setTitle('Measure ('+self.Measure[pt]+')')
        # print(self.filDic)
        for i in self.acList:
            if pt == i.text().lower():
                i.setChecked(True)
            else:
                i.setChecked(False)
        self.rowcolChange()
    
    def toConvert(self):
        pt = self.getPlainText(str(self.item2.text()))
        if self.where == 'di':
            print( pt +" can convert to measure")
        else:
            print( pt +" can convert to dimension")
            
        # print("cc")
        
    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and (source is self.FileListDimension or source is self.FileListMes or source is self.filterList or source is self.ColList or source is self.RowList):
            menu = QMenu()
            self.item2 = source.itemAt(event.pos())
            # pt = self.getPlainText(str(self.item2.text()))
            if self.item2 != None:
                pt = self.getPlainText(str(self.item2.text()))
                if event.type() == QEvent.ContextMenu and (source is self.FileListDimension or source is self.FileListMes ):
                    # print("Convert")
                    if event.type() == QEvent.ContextMenu and (source is self.FileListDimension) :
                        # print('Convert to Measure')
                        if cm.isMeasure(pt):
                            self.cvAc = menu.addAction('Convert to Measure')
                            self.where = 'di'
                        else:
                            self.cvAc = menu.addAction('Convert to Measure')
                            self.where = ' '
                    else:
                        # print('Convert to Dimension')
                        self.cvAc = menu.addAction('Convert to Dimension')
                        self.where = 'mes'
                    if menu.exec_(event.globalPos()) == self.cvAc:
                        if self.where != ' ':
                            self.toConvert()
                    # menu.addMenu(cvAc)
                else:
                    filterAc = menu.addAction('Filter')
                    if pt in list(self.typeDate.keys()):
                        self.subMenuDate = QMenu(pt+'('+self.typeDate[pt]+')')
                        yearAc = self.subMenuDate.addAction("Year",self.clickFunc)
                        # quarterAc = self.subMenuDate.addAction("Quarter",self.clickFunc)
                        mounthAc = self.subMenuDate.addAction("Month",self.clickFunc)
                        dayAc = self.subMenuDate.addAction("Date",self.clickFunc)
                        self.acList = [yearAc,mounthAc,dayAc]
                        # print(self.typeDate)
                        for i in self.acList:
                            i.setCheckable(True)
                            if self.typeDate[pt] == i.text().lower():
                                i.setChecked(True)
                            else:
                                i.setChecked(False)
                        menu.addMenu(self.subMenuDate)
                    if pt in list(self.Measure.keys()):
                        # mesAc = menu.addAction('Measure ('+self.Measure[self.item2.text()]+')')
                        self.subMenu = QMenu('Measure ('+self.Measure[pt]+')')
                        avgAc = self.subMenu.addAction("Average",self.clickFunc)
                        sumAc = self.subMenu.addAction("Sum",self.clickFunc)
                        medAc = self.subMenu.addAction("Median",self.clickFunc)
                        countAc = self.subMenu.addAction("Count",self.clickFunc)
                        maxAc = self.subMenu.addAction("Max",self.clickFunc)
                        minAc = self.subMenu.addAction("Min",self.clickFunc)
                        self.acList = [avgAc,sumAc,medAc,countAc,maxAc,minAc]
                        for i in self.acList:
                            i.setCheckable(True)
                            if self.Measure[pt] == i.text().lower():
                                i.setChecked(True)
                            else:
                                i.setChecked(False)
                        # print(sumAc.text())
                        menu.addMenu(self.subMenu)
                        # print(menu.exec_(event.globalPos()).text())
                    if menu.exec_(event.globalPos()) == filterAc:
                        item = source.itemAt(event.pos())
                        if item.text() not in list(self.filDic.keys()):
                            tmpr =  [str(self.filterList.item(i).text()) for i in range(self.filterList.count())]
                            tmpr.append(item.text())
                            self.filterList.addItems(tmpr)
                            
                            # self.filDic[self.getPlainText(item.text())] = ""
                            self.setFilterValue(self.filJustAdd)
                            
                            # print(self.filDic)
                        self.selectFil(item.text())
                    self.rowcolChange()
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
        
    def lenDimen(self,row,col):
        r = 0
        c = 0
        Measure = list(self.Measure.keys())
        for i in row:
            if type(i) == type(['list']):
                if i[0] not in Measure:
                    r += 1
            elif i not in Measure:
                r +=1
        
        for j in col:
            if type(j) == type(['list']):
                if j[0] not in Measure:
                    c += 1
            elif j not in Measure:
                c +=1
        return [r,c]
            
    def setplot(self):
        print("--------R C",self.RowChoose,self.ColChoose)
        self.setSheetTable()
        self.setChart()
        if self.typeChart != []:
            self.showChart()
    
    def setChart(self):
        # print("set chart")
        # print("--------R C",self.RowChoose,self.ColChoose)
        # self.isInterRow = [value for value in self.RowChoose if value in [self.Measure.keys()]]
        # self.isInterCol = [value for value in self.ColChoose if value in [self.Measure.keys()]]
        # print("--------IR IC",self.isInterRow,self.isInterCol)
        #gm.setList(self.RowChoose,self.ColChoose,self.Measure,self.dfOriginal,self.typeDate)
        gm.setList(self.RowChoose,self.ColChoose,self.Measure,self.data,self.typeDate,self.dfOriginal)
        Measure = list(self.Measure.keys())
        self.typeChart = []
        print("--->",self.isInterRow,self.isInterCol)
        #print('RC CH',self.RowChoose,self.ColChoose)
        if (len(self.isInterRow)>0 and len(self.isInterCol)==0) or (len(self.isInterCol)>0 and len(self.isInterRow)==0):    #Measurement same line
            if (self.lenDimen(self.RowChoose,self.ColChoose)[0] == 0 and self.lenDimen(self.RowChoose,self.ColChoose)[1] == 0 and len(self.isInterCol)>0) or (self.lenDimen(self.RowChoose,self.ColChoose)[1] == 0 and self.lenDimen(self.RowChoose,self.ColChoose)[0] == 0 and len(self.isInterRow)>0):
                self.typeChart = []
            elif (len(self.RowChoose)==1 and len(self.isInterCol)>0) or (len(self.ColChoose)==1 and len(self.isInterRow)>0):
                self.typeChart = ['Bar','Pie','Line']
            elif (len(self.RowChoose)==2 and len(self.isInterCol)>0 and self.lenDimen(self.RowChoose,self.ColChoose)[1] == 0) or (len(self.ColChoose)==2 and len(self.isInterRow)>0 and self.lenDimen(self.RowChoose,self.ColChoose)[0] == 0):
                self.typeChart = ['Bar','Line']
            elif (self.lenDimen(self.RowChoose,self.ColChoose)[0] == 2 and  self.lenDimen(self.RowChoose,self.ColChoose)[1] == 1) or (self.lenDimen(self.RowChoose,self.ColChoose)[0] == 1 and  self.lenDimen(self.RowChoose,self.ColChoose)[1] == 2):
                self.typeChart = ['Bar','Line']
            elif ((self.lenDimen(self.RowChoose,self.ColChoose)[0] == 1 and len(self.isInterRow)>0) or (self.lenDimen(self.RowChoose,self.ColChoose)[1] == 1and len(self.isInterCol)>0)):
                self.typeChart = ['Bar']
            elif (len(self.RowChoose)==3 and len(self.isInterCol)==1) or (len(self.ColChoose)==3 and len(self.isInterRow)==1):
                self.typeChart = ['Bar']
            elif (len(self.RowChoose)==2 and len(self.isInterCol)==1 and len(self.ColChoose)==3) or (len(self.ColChoose)==2 and len(self.isInterRow)==1 and len(self.RowChoose)==3):
                self.typeChart = ['Bar']
            else:
                self.typeChart = []
        self.typeChart = list(set(self.typeChart))
        self.typeChart = sorted(self.typeChart)
        # print("--->",self.typeChart)
        self.chartType.clear()
        self.chartType.addItems(self.typeChart)
        # self.chartType_2.addItems(self.typeChart)
    
    def showChart(self):
        #cm.print()
        # vbox = QtWidgets.QVBoxLayout(self)
        # vbox.setContentsMargins(0, 0, 0, 0)
        self.chartTypeS = self.chartType.currentText()
        # print(self.chartTypeS)
        
        if self.chartTypeS != "": 
            # if self.chartTypeS != "":
            # print("----------------",self.chartTypeS)
            #gm.setList(self.RowChoose,self.ColChoose,self.Measure,self.dfOriginal,self.typeDate)
            gm.setList(self.RowChoose,self.ColChoose,self.Measure,self.data,self.typeDate,self.dfOriginal)
            self.Chart = gm.chooseChart(str(self.chartTypeS))
    
            # self.widget.setLayout(self.view)
            if self.Chart != None:
                # print(type(self.Chart))
                self.view.updateChart(self.Chart)
    
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
        
        # set Measure to last #################
        r = self.getRow()
        c = self.getCol()
        
        self.isInterRow = [value for value in r if value in list(self.Measure.keys())]
        self.isInterCol = [value for value in c if value in list(self.Measure.keys())]
        
        for i in self.isInterRow:
            if i in tmpr:
                tmpr.remove(i)
        tmpr += self.isInterRow
        
        for i in self.isInterCol:
            if i in tmpc:
                tmpc.remove(i)
        tmpc += self.isInterCol
        
        ##########################################
        
        ########## Set For Show ###################
        self.ColList.clear()
        # self.ColList.addItem(tmpc)
        for i in range(len(tmpc)):
            if tmpc[i] in self.Measure.keys():
                func = str(self.Measure[tmpc[i]])
                tmpc[i] = func.upper()+"("+str(tmpc[i])+")"
            if tmpc[i] in self.typeDate.keys():
                func = str(self.typeDate[tmpc[i]])
                tmpc[i] = func.upper()+"("+str(tmpc[i])+")"
        self.ColList.addItems(tmpc)
        
        self.RowList.clear()
        # self.RowList.addItem(tmpr)
        for i in range(len(tmpr)):
            if tmpr[i] in self.Measure.keys():
                func = str(self.Measure[tmpr[i]])
                tmpr[i] = func.upper()+"("+str(tmpr[i])+")"
            if tmpr[i] in self.typeDate.keys():
                func = str(self.typeDate[tmpr[i]])
                tmpr[i] = func.upper()+"("+str(tmpr[i])+")"
        self.RowList.addItems(tmpr)
        # print(self.colHeader)
        # print(tmpr,tmpc)
        for i in range(len(tmpr)):
            self.RowList.item(i).setForeground(QtGui.QColor('white'))
            m = self.getDi(str(self.RowList.item(i).text()))
            if m in self.Measure.keys() :
                self.RowList.item(i).setBackground(QtGui.QColor('#00b180'))
                # self.RowList.item(i).resizeColumnToContents(m)
            else: 
                self.RowList.item(i).setBackground(QtGui.QColor('#4996b2'))
                # self.RowList.item(i).resizeColumnToContents(m)
        
        for i in range(len(tmpc)):
            self.ColList.item(i).setForeground(QtGui.QColor('white'))
            m = self.getDi(str(self.ColList.item(i).text()))
            if m in self.Measure.keys():
                self.ColList.item(i).setBackground(QtGui.QColor('#00b180'))
            else: 
                self.ColList.item(i).setBackground(QtGui.QColor('#4996b2'))
        
        ##########################################
        
        self.RowChoose = tmpr
        self.ColChoose = tmpc
        
        self.RowChoose = self.getRow()
        self.ColChoose = self.getCol()
        
        ################ set func ##############
        
        for i in range(len(self.RowChoose)):
            buf = self.RowChoose[i]
            if buf in list(self.Measure.keys()):
                self.RowChoose[i] = [buf,self.Measure[buf]]
            if buf in list(self.typeDate.keys()):
                self.RowChoose[i] = [buf,self.typeDate[buf]]
                
        for i in range(len(self.ColChoose)):
            buf = self.ColChoose[i]
            if buf in list(self.Measure.keys()):
                self.ColChoose[i] = [buf,self.Measure[buf]]
            if buf in list(self.typeDate.keys()):
                self.ColChoose[i] = [buf,self.typeDate[buf]]
                
        # print(self.RowChoose,self.ColChoose)
        self.setplot()
        
    def filChangeD(self):
        self.filJustAdd = self.getPlainText(self.filJustAdd)
        if self.filJustAdd in self.filDic.keys():
            del self.filDic[self.filJustAdd]
        self.filChange()
    
    def setFilterValue(self,key):
        print("Key : ",key)
        print("Date Key : ",list(self.typeDate.keys()))
        print("Measure Key : ",list(self.Measure.keys()))
        if key in list(self.typeDate.keys()):        
            self.filDic[key] = cm.getDateByFunc(key,self.typeDate[key])
        elif key in list(self.Measure.keys()):
            self.filDic[key] = [min(self.dataSheet[key]),max(self.dataSheet[key])]
        else:
            buf = cm.getDataWithPandasByHead(key)
            self.filDic[key] = buf.drop_duplicates().to_list()
        print("Filter : ",self.filDic)
        
    def filChange(self):
        # print(self.filDic)
        # print(self.filterList.count())
        itemsTextList =  [str(self.filterList.item(i).text()) for i in range(self.filterList.count())]
        itemsTextList =  list(set(itemsTextList))
        # print(itemsTextList)
        while (itemsTextList.count('')):
            itemsTextList.remove('')
        
        print(self.filJustAdd)
        self.setFilterValue(self.filJustAdd)
        print(self.filDic)
        
        if itemsTextList != []:
            self.filterList.clear()
            self.filterList.addItems(itemsTextList)
            
            for i in itemsTextList:
                if i not in list(self.filDic.keys()):
                    if i in self.Measure.keys():
                        self.filDic[i] = "sum"
                    if i in self.Measure.keys():
                        self.filDic[i] = "year"
            
            # print(self.filDic)
            
    def showSheet(self):
        # cm.filter = self.filDic
        buf = self.dataSheet
        # print(buf)
        for i in self.filDic.keys():
            if i in self.Measure.keys():
                print("show sheet",self.filDic)
                buf = self.dataSheet[self.dataSheet[i].between(min(self.filDic[i]), max(self.filDic[i]))]
        self.model = TableModel2(buf)
        # self.model = TableModel2(self.dataSheet)
        self.sheetTable.setModel(self.model)
    
    def getDi(self,n):
        if n[-1] == ")":
            j = n.index("(")
            n = n[j+1:len(n)-1]
        return n
    
    def getPlainText(self,oldText):
        listHaveMes = str(oldText)
        if "(" in list(listHaveMes) and ")" in list(listHaveMes):
            if listHaveMes[-1] == ")":
                j = listHaveMes.index("(")
                listHaveMes = listHaveMes[j+1:len(listHaveMes)-1]
        # print(listHaveMes)
        return listHaveMes
    
    def getRow(self):
        listHaveMes = self.RowChoose
        if listHaveMes != []:
            for i in range(len(listHaveMes)):
                if listHaveMes[i][-1] == ")":
                    j = listHaveMes[i].index("(")
                    listHaveMes[i] = listHaveMes[i][j+1:len(listHaveMes[i])-1]
        return listHaveMes
    
    def getCol(self):
        listHaveMes = self.ColChoose
        if listHaveMes != []:
            for i in range(len(listHaveMes)):
                if listHaveMes[i][-1] == ")":
                    j = listHaveMes[i].index("(")
                    listHaveMes[i] = listHaveMes[i][j+1:len(listHaveMes[i])-1]
        return listHaveMes
                
        
    def setSheetTable(self):
        # print("filter",self.filDic)
        # print(self.RowChoose,self.ColChoose)
        r = self.getRow()
        c = self.getCol()
        # print(r,c)
        # print(self.RowChoose,self.ColChoose)
        if self.selectFile != [] : 
            # print(not(self.RowChoose == [] and self.ColChoose == []))
            if r == [] and c == []:
                self.sheetTable.setModel(None)
            else:
                # print(self.RowChoose,self.ColChoose)
                self.sheetPageRowAndCol(r,c)
                self.model = TableModel2(self.dataSheet)
                if self.isInterRow != [] and self.isInterCol !=[]:
                    self.sheetTable.setModel(None)
                else:
                    self.sheetTable.setModel(self.model)
        # print("Row Col after set sheet",self.RowChoose,self.ColChoose)
    
    def sheetPageRowAndCol(self,Row,Col):
        # print("Start",Row,Col)
        if Row!=[] or Col!=[]:
            
            cm.filter = self.filDic
            cm.Measure = self.Measure
            cm.typeDate = self.typeDate
            print("BF table",self.filDic,self.Measure,self.typeDate)
            self.dataSheet = cm.setRowAndColumn(Row,Col)
            print(self.dataSheet)
    
    def setColH(self,colname):
        colname = list(set(colname))
        for i in colname:
            if i in list(self.Measure.keys()):
                colname.remove(i)
        return colname
                
    def on_header_doubleClicked(self,index):
        #headCur = index
        self.colHeader = cm.getHead()
        self.data = cm.setAllDataByOneDimension(self.colHeader[index])
        self.model = TableModel(self.data)
        self.dataSourceTable.setModel(self.model)
        
    def useFile(self):
        
        itemsTextList =  [str(self.FileListChoose.item(i).text()) for i in range(self.FileListChoose.count())]
        self.selectFile = itemsTextList
        
        while (self.selectFile.count('')):
            self.selectFile.remove('')
            
        itemsTextList =  [str(self.FileList.item(i).text()) for i in range(self.FileList.count())]
        self.fileNameList = itemsTextList
        while (self.fileNameList.count('')):
            self.fileNameList.remove('')
        
        
        if self.selectFile != []:
            self.setForDataSource()
            self.dataSource()
            # print("Path : ",cm.path)
            # print("File : ",cm.selectFile)
            # print("Dimen : ",cm.di)
            # print("Date : ",cm.typeDate)
            # print("Meas : ",cm.Measure)
            # print("Filter : ",cm.filter)
            # print("Row : ",self.RowChoose)
            # print("Row : ",self.ColChoose)
            # print("\n---------------------\n")
        else: 
            self.setNull()
            self.dataSource()

    def setNull(self):
        cm.di = []
        cm.typeDate = {}
        cm.Measure = {}
        cm.filter = {}
        
        self.colHeader = []
        self.dataSourceTable.reset()
        self.dataSourceTable.setModel(None)
        self.sheetTable.reset()
        self.sheetTable.setModel(None)
        
        self.FileListDimension.clear()
        self.FileListDimension.addItems([])
        self.FileListMes.clear()
        self.FileListMes.addItems([])
        
        self.RowList.clear()
        self.ColList.clear()
        self.RowChoose = []
        self.ColChoose = []
        self.Measure = {}
        self.filterList = []
        self.filterList.clear()

    def setTable(self):
        # print("set data")
        # print(self.selectFile)
        if self.selectFile != [] : 
            self.dataSource()
            # print(self.data)
            self.model = TableModel(self.data)
            self.dataSourceTable.setModel(self.model)
            
    def dataSource(self):
        if type(self.selectFile) != list:
            self.selectFile = [self.selectFile]
        if self.selectFile != [] :
            if len(self.selectFile)>1:
                print("Union")
                self.data = cm.unionFile(self.selectFile)
                # self.setFileListDimension()
                self.model = TableModel(self.data)
                self.dataSourceTable.setModel(self.model)
            else:
                # print("Not Union")
                cm.path =self.folderpath
                cm.selectFile = self.selectFile[0] 
                self.data = cm.getDataWithPandas()
                self.model = TableModel(self.data)
                self.dataSourceTable.setModel(self.model)
        else:
            self.setNull()
        
    def setFileInDirectory(self):
        self.FileList.clear()
        if self.fileNameList != []:
            self.FileList.addItems(self.fileNameList)
    
    def setFileChoose(self):
        if self.FileListChoose != None :
            self.FileListChoose.clear()
        if type(self.selectFile) != list:
            self.selectFile = [self.selectFile]
        if self.selectFile != [] and self.selectFile != None:
            self.FileListChoose.addItems(self.selectFile)
            
    def launchDialog(self):
        file_filter = 'Excel File (*.xlsx *.csv *.xls)'
        self.response = QFileDialog.getOpenFileName(
            #parent=self,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Excel File (*.xlsx *.xls *.csv)' #defult filter
        )
        # print(response)
        # self.selectFile = response
        self.folderpath = os.getcwd()
        filename = os.listdir(self.folderpath)
        tmp = []
        for i in filename:
            if i.endswith(".xls") or i.endswith(".csv") or i.endswith(".xlsx"):
                tmp.append(i)
        self.response = list(self.response)
        self.selectFile = os.path.split(self.response[0])
        # print(self.selectFile)
        self.selectFile = list(self.selectFile)[1]
        if self.selectFile in tmp:
            tmp.remove(self.selectFile)
        #print(tmp)
        self.fileNameList = tmp
        self.path = os.path.join(self.folderpath,self.selectFile)
        cm.path = self.folderpath
        cm.selectFile = self.selectFile
        print("Start")
        self.setForDataSource()
        if self.response[0] != "":
            self.dataSource()
        
    def setForDataSource(self):
        cm.setPath()
        self.colHeader = cm.getHead()
        self.Measure = cm.Measure
        self.typeDate = cm.typeDate
        if self.response[0] != "":
            self.setFileListDimension()
            self.setFileInDirectory()
            self.setFileChoose()
        
    def setFileListDimension(self):
        self.FileListDimension.clear()
        self.FileListDimension.addItems(cm.di)
        self.FileListMes.clear()
        self.FileListMes.addItems(list(cm.Measure.keys()))

app = QApplication(sys.argv)
# widget = QtWidgets.QStackedWidget()
gm = graphManager.graphManager()
cm = cmpage.csvManager()
mainW = mainWindow()
mainW.show()
try:
    sys.exit(app.exec_())
except SystemExit:
    sys.exit()
    # app.exec()
    print('Closing Window...')
from PyQt5 import QtCore, QtGui, QtWidgets
import csvManager
cm = csvManager.csvManager()
class Ui_MainWindow(object):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.filtered = {}
        self.head = ''
        self.sheet = ''
    
    def setStart(self,filHead,dic,data):
        # print(filHead)
        self.filtered = dic
        self.head = filHead
        self.sheet = data
        # print("sheet ",self.sheet)
        # self.setupUi(MainWindow)
    
    def setAll(self):
        print("kk")
        print(self.filtered)
        self.filtered[self.head] = self.sheet[self.head].drop_duplicates().tolist()
        print(self.filtered)
        self.setupUi(MainWindow)
    
    def clickApply(self):
        print("kk")
        for index in range(self.filterItemListWidget.count()):
            print(self.filterItemListWidget.item(index).checkState())
            # if self.filterItemListWidget.item(index).checkState() == 2:
            #     checked_items.append(self.listWidgetLabels.item(index))
            
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(443, 605)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        
        self.allButton = QtWidgets.QPushButton(self.tab)
        self.allButton.setObjectName("allButton")
        self.allButton.clicked.connect(self.setAll)
        
        self.gridLayout_2.addWidget(self.allButton, 0, 0, 1, 1)
        self.noneButton = QtWidgets.QPushButton(self.tab)
        self.noneButton.setObjectName("noneButton")
        self.gridLayout_2.addWidget(self.noneButton, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 2, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.filterItemListWidget = QtWidgets.QListWidget(self.tab)
        self.filterItemListWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.filterItemListWidget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.filterItemListWidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.filterItemListWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.filterItemListWidget.setObjectName("filterItemListWidget")
        # print(type(self.sheet[self.head]))
        for i in self.sheet[self.head].drop_duplicates():
            item = QtWidgets.QListWidgetItem()
            if i in self.filtered[self.head]:
                item.setCheckState(QtCore.Qt.Checked) #2
            else:
                item.setCheckState(QtCore.Qt.Unchecked) #0
            self.filterItemListWidget.addItem(item)
        
        # print(self.filterItemListWidget.item(0).checkState())
        # self.filterItemListWidget.addItems(self.sheet[self.head].drop_duplicates().setCheckState(QtCore.Qt.Checked))
        
        self.gridLayout_4.addWidget(self.filterItemListWidget, 1, 0, 1, 1)
        self.summaryLabel = QtWidgets.QLabel(self.tab)
        self.summaryLabel.setObjectName("summaryLabel")
        self.gridLayout_4.addWidget(self.summaryLabel, 2, 0, 1, 1)
        self.fieldLabel = QtWidgets.QLabel(self.tab)
        self.fieldLabel.setObjectName("fieldLabel")
        self.gridLayout_4.addWidget(self.fieldLabel, 3, 0, 1, 1)
        self.selectionLabel = QtWidgets.QLabel(self.tab)
        self.selectionLabel.setObjectName("selectionLabel")
        self.gridLayout_4.addWidget(self.selectionLabel, 4, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.resetButton = QtWidgets.QPushButton(self.tab)
        self.resetButton.setObjectName("resetButton")
        self.gridLayout_3.addWidget(self.resetButton, 0, 0, 1, 1)
        self.okButton = QtWidgets.QPushButton(self.tab)
        self.okButton.setObjectName("okButton")
        self.okButton.clicked.connect(self.clickApply)
        
        self.gridLayout_3.addWidget(self.okButton, 0, 2, 1, 1)
        self.cancleButton = QtWidgets.QPushButton(self.tab)
        self.cancleButton.setObjectName("cancleButton")
        self.gridLayout_3.addWidget(self.cancleButton, 0, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 5, 0, 1, 1)
        self.deleteButton = QtWidgets.QPushButton(self.tab)
        self.deleteButton.setObjectName("deleteButton")
        self.gridLayout_4.addWidget(self.deleteButton, 6, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        # self.tab_2 = QtWidgets.QWidget()
        # self.tab_2.setEnabled(True)
        # self.tab_2.setObjectName("tab_2")
        # self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 443, 26))
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
        self.allButton.setText(_translate("MainWindow", "All"))
        
        self.noneButton.setText(_translate("MainWindow", "None"))
        __sortingEnabled = self.filterItemListWidget.isSortingEnabled()
        n=0
        for i in self.sheet[self.head].drop_duplicates():
            item = self.filterItemListWidget.item(n)
            item.setText(_translate("MainWindow", i))
            n+=1
        # self.filterItemListWidget.setSortingEnabled(False)
        # item = self.filterItemListWidget.item(0)
        # item.setText(_translate("MainWindow", "New Item"))
        # item = self.filterItemListWidget.item(1)
        # item.setText(_translate("MainWindow", "New Item"))
        # item = self.filterItemListWidget.item(2)
        # item.setText(_translate("MainWindow", "New Item"))
        self.filterItemListWidget.setSortingEnabled(__sortingEnabled)
        self.summaryLabel.setText(_translate("MainWindow", "Summary : "))
        self.fieldLabel.setText(_translate("MainWindow", "Field :"))
        self.selectionLabel.setText(_translate("MainWindow", "Selection : "))
        self.resetButton.setText(_translate("MainWindow", "Reset"))
        self.okButton.setText(_translate("MainWindow", "Apply"))
        self.okButton.clicked.connect(self.clickApply)
        
        self.cancleButton.setText(_translate("MainWindow", "Cancle"))
        self.deleteButton.setText(_translate("MainWindow", "Delete from Filter"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Genneral"))
        # self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

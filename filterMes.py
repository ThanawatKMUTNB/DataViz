from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
        self.filtered = {}
        self.head = ''
        self.sheet = ''
        self.min = ''
        self.max = ''
        # self.atMostSlider.valueChanged.connect(self.valuechange)
    
    def setStart(self,filHead,dic,data):
        # print(filHead)
        self.filtered = dic
        self.head = filHead
        self.sheet = data
        self.max = self.sheet[self.head].max()
        self.min = self.sheet[self.head].min()
        # print(self.min,self.max)
        
    def clickDeleteButton(self):
        print("Delete")
    
    def valuechange(self):
        txt = str(self.atMostSlider.value())
        self.rangeMax.setText(txt)
        txt = str(self.atLeatSlider.value())
        self.rangeMin.setText(txt)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(603, 316)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.resetButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetButton.setObjectName("resetButton")
        self.gridLayout.addWidget(self.resetButton, 0, 0, 1, 1)
        self.applyButton = QtWidgets.QPushButton(self.centralwidget)
        self.applyButton.setObjectName("applyButton")
        self.gridLayout.addWidget(self.applyButton, 0, 2, 1, 1)
        self.cancleButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancleButton.setObjectName("cancleButton")
        self.gridLayout.addWidget(self.cancleButton, 0, 3, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout, 1, 0, 1, 1)
        
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.clicked.connect(self.clickDeleteButton)
        
        self.gridLayout_7.addWidget(self.deleteButton, 2, 0, 1, 1)
        
        
        
        
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        
        self.rangeOfValuesTab = QtWidgets.QWidget()
        self.rangeOfValuesTab.setObjectName("rangeOfValuesTab")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.rangeOfValuesTab)
        self.gridLayout_10.setObjectName("gridLayout_10")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_10.addItem(spacerItem1, 0, 0, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout_5.setObjectName("gridLayout_5")
        
        self.rangeMin = QtWidgets.QLineEdit(self.rangeOfValuesTab)
        self.rangeMin.setObjectName("rangeMin")
        self.rangeMin.setText(str(self.min))
        self.gridLayout_5.addWidget(self.rangeMin, 0, 0, 1, 1)
        
        self.rangeMax = QtWidgets.QLineEdit(self.rangeOfValuesTab)
        self.rangeMax.setObjectName("rangeMax")
        self.rangeMax.setText(str(self.max))
        
        self.gridLayout_5.addWidget(self.rangeMax, 0, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem2, 0, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem3, 0, 2, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_5, 1, 0, 1, 1)
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        
        self.atLeatLabel = QtWidgets.QLabel(self.rangeOfValuesTab)
        self.atLeatLabel.setObjectName("atLeatLabel")
        
        self.gridLayout_8.addWidget(self.atLeatLabel, 0, 0, 1, 1)
        
        self.atLeatSlider = QtWidgets.QSlider(self.rangeOfValuesTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.atLeatSlider.sizePolicy().hasHeightForWidth())

        self.atLeatSlider.setSizePolicy(sizePolicy)
        self.atLeatSlider.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.atLeatSlider.setOrientation(QtCore.Qt.Horizontal)
        self.atLeatSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.atLeatSlider.setObjectName("atLeatSlider")
        # self.atLeatSlider.setMinimum(float(self.min))
        # self.atLeatSlider.setMaximum(float(self.max))
        self.atLeatSlider.valueChanged.connect(self.valuechange)
        
        self.gridLayout_8.addWidget(self.atLeatSlider, 0, 1, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_8, 3, 0, 1, 1)
        
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        
        self.atMostLabel = QtWidgets.QLabel(self.rangeOfValuesTab)
        
        self.atMostLabel.setObjectName("atMostLabel")
        self.gridLayout_9.addWidget(self.atMostLabel, 0, 0, 1, 1)
        
        self.atMostSlider = QtWidgets.QSlider(self.rangeOfValuesTab)
        self.atMostSlider.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.atMostSlider.setStyleSheet("\"QSlider::groove:horizontal {background-color:red;}\"")
        # self.atMostSlider.setMinimum(float(self.min))
        # self.atMostSlider.setMaximum(float(self.max))
        # self.atMostSlider.setProperty("value", 20)
        self.atMostSlider.setTracking(True)
        self.atMostSlider.setOrientation(QtCore.Qt.Horizontal)
        self.atMostSlider.setInvertedAppearance(False)
        self.atMostSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.atMostSlider.setObjectName("atMostSlider")
        
        self.gridLayout_9.addWidget(self.atMostSlider, 0, 1, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_9, 4, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_10.addItem(spacerItem4, 6, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.atLeastValueLabel = QtWidgets.QLabel(self.rangeOfValuesTab)
        self.atLeastValueLabel.setObjectName("atLeastValueLabel")
        self.gridLayout_2.addWidget(self.atLeastValueLabel, 0, 0, 1, 1)
        
        self.atMostValueLabel = QtWidgets.QLabel(self.rangeOfValuesTab)
        self.atMostValueLabel.setObjectName("atMostValueLabel")
        self.gridLayout_2.addWidget(self.atMostValueLabel, 0, 1, 1, 1)
        
        self.gridLayout_10.addLayout(self.gridLayout_2, 5, 0, 1, 1)
        self.tabWidget.addTab(self.rangeOfValuesTab, "")
        
        
        
        
        
        
        self.atLeastTab = QtWidgets.QWidget()
        self.atLeastTab.setObjectName("atLeastTab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.atLeastTab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        spacerItem5 = QtWidgets.QSpacerItem(20, 11, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem5, 6, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 11, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem6, 0, 0, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.atLeastMin = QtWidgets.QLineEdit(self.atLeastTab)
        self.atLeastMin.setObjectName("atLeastMin")
        self.gridLayout_6.addWidget(self.atLeastMin, 0, 0, 1, 1)
        self.atLeastMax = QtWidgets.QLineEdit(self.atLeastTab)
        self.atLeastMax.setObjectName("atLeastMax")
        self.gridLayout_6.addWidget(self.atLeastMax, 0, 3, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem7, 0, 1, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem8, 0, 2, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_6, 1, 0, 1, 1)
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.gridLayout_4.addLayout(self.gridLayout_11, 4, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.atLeastValueLabel_3 = QtWidgets.QLabel(self.atLeastTab)
        self.atLeastValueLabel_3.setObjectName("atLeastValueLabel_3")
        self.gridLayout_3.addWidget(self.atLeastValueLabel_3, 0, 0, 1, 1)
        self.atMostValueLabel_2 = QtWidgets.QLabel(self.atLeastTab)
        self.atMostValueLabel_2.setObjectName("atMostValueLabel_2")
        self.gridLayout_3.addWidget(self.atMostValueLabel_2, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 5, 0, 1, 1)
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.atLeatLabel_2 = QtWidgets.QLabel(self.atLeastTab)
        self.atLeatLabel_2.setObjectName("atLeatLabel_2")
        self.gridLayout_12.addWidget(self.atLeatLabel_2, 0, 0, 1, 1)
        self.atLeatSlider_2 = QtWidgets.QSlider(self.atLeastTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.atLeatSlider_2.sizePolicy().hasHeightForWidth())
        self.atLeatSlider_2.setSizePolicy(sizePolicy)
        self.atLeatSlider_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.atLeatSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.atLeatSlider_2.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.atLeatSlider_2.setObjectName("atLeatSlider_2")
        self.gridLayout_12.addWidget(self.atLeatSlider_2, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_12, 3, 0, 1, 1)
        self.tabWidget.addTab(self.atLeastTab, "")
        
        
        
        
        
        
        
        self.atMostTab = QtWidgets.QWidget()
        self.atMostTab.setObjectName("atMostTab")
        self.gridLayout_20 = QtWidgets.QGridLayout(self.atMostTab)
        self.gridLayout_20.setObjectName("gridLayout_20")
        spacerItem9 = QtWidgets.QSpacerItem(20, 11, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_20.addItem(spacerItem9, 0, 0, 1, 1)
        self.gridLayout_18 = QtWidgets.QGridLayout()
        self.gridLayout_18.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.atMostMin = QtWidgets.QLineEdit(self.atMostTab)
        self.atMostMin.setObjectName("atMostMin")
        self.gridLayout_18.addWidget(self.atMostMin, 0, 0, 1, 1)
        self.atMostMax = QtWidgets.QLineEdit(self.atMostTab)
        self.atMostMax.setObjectName("atMostMax")
        self.gridLayout_18.addWidget(self.atMostMax, 0, 3, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_18.addItem(spacerItem10, 0, 1, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_18.addItem(spacerItem11, 0, 2, 1, 1)
        self.gridLayout_20.addLayout(self.gridLayout_18, 1, 0, 1, 1)
        self.gridLayout_19 = QtWidgets.QGridLayout()
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.gridLayout_20.addLayout(self.gridLayout_19, 3, 0, 1, 1)
        self.gridLayout_16 = QtWidgets.QGridLayout()
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.atMostLabel_3 = QtWidgets.QLabel(self.atMostTab)
        self.atMostLabel_3.setObjectName("atMostLabel_3")
        self.gridLayout_16.addWidget(self.atMostLabel_3, 0, 0, 1, 1)
        self.atMostSlider_3 = QtWidgets.QSlider(self.atMostTab)
        self.atMostSlider_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.atMostSlider_3.setStyleSheet("\"QSlider::groove:horizontal {background-color:red;}\"")
        # self.atMostSlider_3.setProperty("value", 20)
        self.atMostSlider_3.setTracking(True)
        self.atMostSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.atMostSlider_3.setInvertedAppearance(False)
        self.atMostSlider_3.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.atMostSlider_3.setObjectName("atMostSlider_3")
        self.gridLayout_16.addWidget(self.atMostSlider_3, 0, 1, 1, 1)
        self.gridLayout_20.addLayout(self.gridLayout_16, 4, 0, 1, 1)
        self.gridLayout_17 = QtWidgets.QGridLayout()
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.atLeastValueLabel_4 = QtWidgets.QLabel(self.atMostTab)
        self.atLeastValueLabel_4.setObjectName("atLeastValueLabel_4")
        self.gridLayout_17.addWidget(self.atLeastValueLabel_4, 0, 0, 1, 1)
        self.atMostValueLabel_3 = QtWidgets.QLabel(self.atMostTab)
        self.atMostValueLabel_3.setObjectName("atMostValueLabel_3")
        self.gridLayout_17.addWidget(self.atMostValueLabel_3, 0, 1, 1, 1)
        self.gridLayout_20.addLayout(self.gridLayout_17, 5, 0, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(20, 11, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_20.addItem(spacerItem12, 6, 0, 1, 1)
        self.tabWidget.addTab(self.atMostTab, "")
        self.gridLayout_7.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 603, 21))
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
        self.resetButton.setText(_translate("MainWindow", "Reset"))
        self.applyButton.setText(_translate("MainWindow", "Apply"))
        self.cancleButton.setText(_translate("MainWindow", "Cancel"))
        self.deleteButton.setText(_translate("MainWindow", "Delete"))
        self.atLeatLabel.setText(_translate("MainWindow", "At least"))
        self.atMostLabel.setText(_translate("MainWindow", "At most"))
        
        self.atLeastValueLabel.setText(_translate("MainWindow", str(self.min)))
        self.atMostValueLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\">"+str(self.max)+"</p></body></html>"))
        
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.rangeOfValuesTab), _translate("MainWindow", "Range of values"))
        
        self.atLeastValueLabel_3.setText(_translate("MainWindow", str(self.min)))
        self.atMostValueLabel_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\">"+str(self.max)+"</p></body></html>"))
        
        self.atLeatLabel_2.setText(_translate("MainWindow", "At least"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.atLeastTab), _translate("MainWindow", "At least"))
        
        self.atMostLabel_3.setText(_translate("MainWindow", "At most"))

        self.atLeastValueLabel_4.setText(_translate("MainWindow", str(self.min)))
        self.atMostValueLabel_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\">"+str(self.max)+"</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.atMostTab), _translate("MainWindow", "At most"))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())

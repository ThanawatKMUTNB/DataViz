import sys
from PyQt5 import uic
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow ,QDialog, QApplication, QTabWidget, QWidget,QPushButton,QListWidget,QMenuBar,QStatusBar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtChart import QChart, QChartView, QBarSet, QPercentBarSeries, QBarCategoryAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets , QtChart
from PyQt5.QtChart import QChart
import pandas as pd
#import csvManagergdkjf

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("untitled.ui",self)
        #sc = MplCanvas(self, width=5, height=4, dpi=100)
        
        #self.setCentralWidget(sc)
        self.button = self.findChild(QtWidgets.QPushButton, 'Color') # Find the button
        self.button.clicked.connect(AnyButton.changeColor) # Remember to pass the definition/method, not the return value!
        self.button = self.findChild(QtWidgets.QPushButton, 'Size') # Find the button
        self.button.clicked.connect(AnyButton.buttonsize)
        self.button = self.findChild(QtWidgets.QPushButton, 'Label') # Find the button
        self.button.clicked.connect(AnyButton.buttonlabel)
        self.button = self.findChild(QtWidgets.QPushButton, 'Detail') # Find the button
        self.button.clicked.connect(AnyButton.Buttondetail)
        self.button = self.findChild(QtWidgets.QPushButton, 'Tooltips') # Find the button
        self.button.clicked.connect(AnyButton.ButtonTooltips)
        self.button = self.findChild(QtWidgets.QPushButton, 'Barchart') # Find the button
        self.button.clicked.connect(lambda checked: ShowGraph.showbarchart(self))
        #self.button.clicked.connect(ShowGraph.showbarchart)
        self.button = self.findChild(QtWidgets.QPushButton, 'Piechart') # Find the button
        self.button.clicked.connect(lambda checked: ShowGraph.showpiechart(self))
        self.button = self.findChild(QtWidgets.QPushButton, 'Linegraph') # Find the button
        self.button.clicked.connect(ShowGraph.showlinegraph)
        self.button = self.findChild(QtWidgets.QPushButton, 'stackbar') # Find the button
        self.button.clicked.connect(lambda checked: ShowGraph.showstackbar(self))
        self.show()

class AnyButton() :
    def changeColor() :
        print("Hello color")
    def buttonsize() :
        print("Hello size")
    def buttonlabel() :
        print("Hello label")
    def Buttondetail() :
        print("Hello detail")
    def ButtonTooltips() :
        print("Hello Tooltips")
   

class ShowGraph(FigureCanvas):
    def __init__(self):
        super().__init__()
 
        self.setWindowTitle("PyQt BarChart")
        self.setGeometry(100,100, 680,500)
        self.show()
        self.create_bar()
    def showlinegraph() :
        print("Show line")
    def showbarchart(self) :
        df = pd.read_csv('Superstore.csv', encoding='windows-1252')
        Reg = []
		
        for i in df['Region'].values:
            if i not in Reg:
                Reg.append(i)

        df.set_index('Region',inplace=True)
        profit = []
        disc = []
        quan = []
        sale = []

        for i in Reg:
            profit.append(sum(df.loc[i,'Profit']))
            disc.append(sum(df.loc[i,'Discount']))
            quan.append(sum(df.loc[i,'Quantity']))
            sale.append(sum(df.loc[i,'Sales']))

        tmp = [profit,disc,quan,sale]
        

        set0 = QBarSet('Profit')
        set1 = QBarSet('Discount') 
        set2 = QBarSet('Quantity')
        set3 = QBarSet('Sales')

        for i in range(len(Reg)):
            set0.append(tmp[i][0])
            set1.append(tmp[i][1])
            set2.append(tmp[i][2])
            set3.append(tmp[i][3])

        '''print(profit)
        print(disc)
        print(quan)
        print(sale)'''
        
        series = QPercentBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
 
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Percent Example")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        meslist = ['Profit','Discount','Quantity','Sales']
        axis = QBarCategoryAxis()
        axis.append(meslist)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)
 
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
 
        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)
 
        self.setCentralWidget(chartView)

    def showpiechart(self) :
        print("Show Pie")
        series = QtChart.QPieSeries()
        series.append("Jane", 1)
        series.append("Joe", 2)
        series.append("Andy", 3)
        series.append("Barbara", 4)
        series.append("Axel", 5)

        chart = QtChart.QChart()
        chart.addSeries(series)
        chart.setTitle("Simple piechart example")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().hide()

        series.setLabelsVisible()
        #series.setLabelsPosition(QtChart.QPieSlice.LabelInsideHorizontal)

        for slice in series.slices():
            slice.setLabel("{:.1f}%".format(100 * slice.percentage()))
        chartView = QtChart.QChartView(chart)
        chartView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setCentralWidget(chartView)
        

    def showstackbar(self) :
        print("Show stack")
        set0 = QBarSet("Parwiz")
        set1 = QBarSet("Bob")
        set2 = QBarSet("Tom")
        set3 = QBarSet("Logan")
        set4 = QBarSet("Karim")
 
        set0 << 1 << 2 << 3 << 4 << 5 << 6  #Jan -> Jun
        set1 << 5 << 0 << 0 << 4 << 0 << 7
        set2 << 3 << 5 << 8 << 13 << 8 << 5
        set3 << 5 << 6 << 7 << 3 << 4 << 5
        set4 << 9 << 7 << 5 << 3 << 1 << 2
 
        series = QPercentBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
        series.append(set4)
 
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Percent Example")
        chart.setAnimationOptions(QChart.SeriesAnimations)
 
        categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        axis = QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)
 
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
 
        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)
 
        self.setCentralWidget(chartView)


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()

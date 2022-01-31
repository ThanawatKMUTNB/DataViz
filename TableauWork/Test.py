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
        self.button.clicked.connect(ShowGraph.showbarchart)
        self.button = self.findChild(QtWidgets.QPushButton, 'Piechart') # Find the button
        self.button.clicked.connect(ShowGraph.showpiechart)
        self.button = self.findChild(QtWidgets.QPushButton, 'Linegraph') # Find the button
        self.button.clicked.connect(ShowGraph.showlinegraph)
        self.button = self.findChild(QtWidgets.QPushButton, 'stackbar') # Find the button
        self.button.clicked.connect(ShowGraph.showstackbar)
        
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
        print("Show Bar")
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

    def showpiechart() :
        print("Show Pie")
    def showstackbar() :
        print("Show stack")

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtChart import QChart, QChartView, QBarSet, QPercentBarSeries, QBarCategoryAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
import pandas as pd

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
 
        self.setWindowTitle("PyQt BarChart")
        self.setGeometry(100,100, 680,500)
        self.show()
        self.create_bar()
 
    def create_bar(self):
        
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
        

        set0 = QBarSet('1')
        set1 = QBarSet('2') 
        set2 = QBarSet('3')
        set3 = QBarSet('4')

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
 

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec_())
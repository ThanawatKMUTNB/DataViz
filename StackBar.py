from audioop import reverse
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtChart import QChart, QChartView, QBarSet, QPercentBarSeries, QBarCategoryAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
import pandas as pd
import csvManager

class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        Dimention = 'Region'
        Measure = ['Profit','Discount','Quantity']
        self.setWindowTitle("PyQt BarChart")
        self.resize(800, 600)
        self.show()
        self.create_bar(Dimention,Measure)
 
    def create_bar(self,Dimention,Measure):
        
        df = pd.read_csv('Superstore.csv', encoding='windows-1252')
        df.set_index(Dimention,inplace=True)
        ValueDi = csvManager.getValueDimention(Dimention)
        ValueDi = sorted(ValueDi)
        ValueDi = ValueDi[::-1]
        print(ValueDi)
        series = QPercentBarSeries()

        Meskey = []
        for i in Measure:
            Meskey.append(csvManager.getDataForBar([Dimention],[i]))
        #Meskey = Meskey[::-1]
        for j in range(len(ValueDi)):
            set0 = QBarSet(ValueDi[j])
            for k in range(len(Measure)):
                set0.append(Meskey[k][j])
            series.append(set0)

        series.setLabelsVisible()
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Percent Example")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        #meslist = ['Profit','Discount','Quantity','Sales']
        
        axis = QBarCategoryAxis()
        axis.append(Measure)
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
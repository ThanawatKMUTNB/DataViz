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

        Dimension = 'Region'
        Measure = []
        for M in csvManager.getHead():
            #print(M)
            if not csvManager.isDimension(M):
                Measure.append(M)

        self.setWindowTitle("PyQt BarChart")
        self.resize(1000, 800)
        self.show()
        self.create_bar(Dimension,Measure)
 
    def create_bar(self,Dimension,Measure):
        
        df = pd.read_csv('Superstore.csv', encoding='windows-1252')
        df.set_index(Dimension,inplace=True)
        ValueDi = csvManager.getValueDimension(Dimension)
        ValueDi = sorted(ValueDi)
        ValueDi = ValueDi[::-1]
        #print(ValueDi)
        series = QPercentBarSeries()

        Meskey = []
        for i in Measure:
            Meskey.append(csvManager.getDataForBar([Dimension],[i]))
        #Meskey = Meskey[::-1]
        for j in range(len(ValueDi)):
            set0 = QBarSet(ValueDi[j])
            for k in range(len(Measure)):
                set0.append(Meskey[k][j])
            series.append(set0)

        series.setLabelsVisible()
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Percent Stack Bar")
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
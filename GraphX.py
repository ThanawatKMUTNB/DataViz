import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtChart import QChart, QChartView, QHorizontalBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter
import pandas as pd

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.resize(800, 600)

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

		set0 = QBarSet('Profit')    #set label
		set1 = QBarSet('Discount') 
		set2 = QBarSet('Quantity')
		set3 = QBarSet('Sales')


		set0.append(profit) #data each month
		set1.append(disc)
		set2.append(quan)
		set3.append(sale)


		series = QHorizontalBarSeries()
		series.append(set0)
		series.append(set1)
		series.append(set2)
		series.append(set3)

		chart = QChart()
		chart.addSeries(series)
		chart.setTitle('Horizontal Bar Chart Demo')

		chart.setAnimationOptions(QChart.SeriesAnimations)

		months = tuple(Reg)

		axisY = QBarCategoryAxis()
		axisY.append(months)
		chart.addAxis(axisY, Qt.AlignLeft)
		series.attachAxis(axisY)

		axisX = QValueAxis()
		chart.addAxis(axisX, Qt.AlignBottom)
		series.attachAxis(axisX)

		axisX.applyNiceNumbers()

		chart.legend().setVisible(True)
		chart.legend().setAlignment(Qt.AlignBottom)

		chartView = QChartView(chart)
		chartView.setRenderHint(QPainter.Antialiasing)
		self.setCentralWidget(chartView)

if __name__ == '__main__':
	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()

	sys.exit(app.exec_())
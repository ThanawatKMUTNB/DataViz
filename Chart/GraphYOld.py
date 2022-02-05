import sys, random
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter
import pandas as pd

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.resize(800, 600)

		Dimen = 'Ship Mode'
		df = pd.read_csv('Superstore.csv', encoding='windows-1252')
		Reg = []
		for i in df[Dimen].values:
			if i not in Reg:
				Reg.append(i)

		df.set_index(Dimen,inplace=True)
		profit = []
		disc = []
		quan = []
		sale = []
		for i in Reg:
			profit.append(sum(df.loc[i,'Profit']))
			disc.append(sum(df.loc[i,'Discount']))
			quan.append(sum(df.loc[i,'Quantity']))
			sale.append(sum(df.loc[i,'Sales']))


		set0 = QBarSet('Profit')
		set1 = QBarSet('Discount') 
		set2 = QBarSet('Quantity')
		set3 = QBarSet('Sales')


		set0.append(profit)
		set1.append(disc)
		set2.append(quan)
		set3.append(sale)



		series = QBarSeries()
		series.append(set0)
		series.append(set1)
		series.append(set2)
		series.append(set3)

		#series.setLabelsVisible()


		chart = QChart()
		chart.addSeries(series)
		chart.setTitle('Bar Chart Demo')
		chart.setAnimationOptions(QChart.SeriesAnimations)

		#months = ('test1')
		months = tuple(Reg)

		axisX = QBarCategoryAxis()
		axisX.append(months)

		axisY = QValueAxis()
		axisY.setRange(0, max(profit))

		chart.addAxis(axisX, Qt.AlignBottom)
		chart.addAxis(axisY, Qt.AlignLeft)

		chart.legend().setVisible(True)
		chart.legend().setAlignment(Qt.AlignBottom)

		chartView = QChartView(chart)
		self.setCentralWidget(chartView)

if __name__ == '__main__':
	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()

	sys.exit(app.exec_())
from itertools import chain
import sys, random
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter
import pandas as pd
import csvManager

class MainWindow(QMainWindow):
	def __init__(self,Dimension,Measure):
		super().__init__()
		self.resize(800, 600)

		df = pd.read_csv('Superstore.csv', encoding='windows-1252')
		Reg = csvManager.getAxisYName([Dimension])
		tmp = csvManager.getDataForBar([Dimension],[Measure])
		#print(df)
		set0 = QBarSet(Measure)
		set0.append(reversed(tmp))
		oneList = list(chain.from_iterable(Reg))
		#print(tuple(oneList))
		series = QBarSeries()
		series.append(set0)
		#series.setLabelsVisible()
		chart = QChart()
		chart.addSeries(series)
		chart.setTitle('Bar Chart Demo')
		chart.setAnimationOptions(QChart.SeriesAnimations)
		#months = ('test1')
		months = tuple(reversed(oneList))
		#print(months)
		series.setLabelsVisible()
		axisX = QBarCategoryAxis()
		axisX.append(months)
		axisY = QValueAxis()
		axisY.setRange(0, max(tmp))

		chart.addAxis(axisX, Qt.AlignBottom)
		chart.addAxis(axisY, Qt.AlignLeft)

		chart.legend().setVisible(True)
		chart.legend().setAlignment(Qt.AlignBottom)

		chartView = QChartView(chart)
		self.setCentralWidget(chartView)

if __name__ == '__main__':
	app = QApplication(sys.argv)

	window = MainWindow('Ship Mode','Discount')
	window.show()

	sys.exit(app.exec_())
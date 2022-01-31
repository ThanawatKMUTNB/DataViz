from itertools import chain
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtChart import QChart, QChartView, QHorizontalBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter
import pandas as pd
import csvManager

class MainWindow(QMainWindow):
        
	def __init__(self,Dimention,Measure):
		super().__init__()
		self.resize(800, 600)

		series = QHorizontalBarSeries()
		#colList = ['Discount','Profit','Sales']
		#for col in colList:
		tmp = csvManager.getDataForBar([Dimention],[Measure])
		set0 = QBarSet(Measure)
		set0.append(tmp)
		series.append(set0)

		chart = QChart()
		chart.addSeries(series)
		s = str(Dimention+' '+Measure)
		chart.setTitle(s)

		chart.setAnimationOptions(QChart.SeriesAnimations)

		series.setLabelsVisible()

		reg2 = csvManager.getAxisYName([Dimention])

		oneList = list(chain.from_iterable(reg2))
		months = tuple(oneList)


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

	window = MainWindow('Region','Discount')
	#window2 = MainWindow('Region','Profit')
	window.show()
	sys.exit(app.exec_())


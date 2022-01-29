from itertools import chain
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtChart import QChart, QChartView, QHorizontalBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter
import pandas as pd
import csvManager

class MainWindow(QMainWindow):
        
	def __init__(self):
		super().__init__()
		self.resize(800, 600)
		series = QHorizontalBarSeries()
  
		row = 'Region'
		colList = ['Discount','Profit','Sales']
		for col in colList:
			tmp = csvManager.getDataForBar([row],[col])
			set = QBarSet(col)
			set.append(tmp)
			series.append(set)
  
		chart = QChart()
		chart.addSeries(series)
		chart.setTitle('Horizontal Bar Chart Demo')

		chart.setAnimationOptions(QChart.SeriesAnimations)

		reg2 = csvManager.getAxisYName([row])
		months = tuple(reg2)

		'''axisY = QBarCategoryAxis()
		axisY.append(months)
		chart.addAxis(axisY, Qt.AlignLeft)
		series.attachAxis(axisY)
		axisX = QValueAxis()
		chart.addAxis(axisX, Qt.AlignBottom)
		series.attachAxis(axisX)
		axisX.applyNiceNumbers()
		chart.legend().setVisible(True)
		chart.legend().setAlignment(Qt.AlignBottom)'''

		chartView = QChartView(chart)
		chartView.setRenderHint(QPainter.Antialiasing)
		self.setCentralWidget(chartView)

if __name__ == '__main__':
	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()

	sys.exit(app.exec_())
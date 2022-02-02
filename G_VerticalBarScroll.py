from calendar import month
from PyQt5 import QtCore, QtGui, QtWidgets, QtChart
from PyQt5.Qt import Qt
import math
import numpy as np
import pandas as pd
import csvManager
from itertools import chain

############edit name under bar 
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        Dimention = 'State'
        Measure = 'Quantity'

        n = csvManager.getsizeDimention(Dimention)
        r = False
        if n > 500:
            self.step = 0.01
        elif n > 300:
            self.step = 0.02
        elif n > 100:
            self.step = 0.03
        elif n > 50:
            self.step = 0.05
        elif n > 20:
            self.step = 0.08
        elif n > 10:
            self.step = 0.1
        else:
            self.step = 1
            r = True

        self._chart_view = QtChart.QChartView()
        self.scrollbar = QtWidgets.QScrollBar(
            QtCore.Qt.Horizontal,
            sliderMoved=self.onAxisSliderMoved,
            pageStep=self.step * 100,
        )

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        lay = QtWidgets.QVBoxLayout(central_widget)
        for w in (self._chart_view, self.scrollbar):
            lay.addWidget(w)
        
        self.resize(840, 480)
        self._chart = QtChart.QChart()
        self.series = QtChart.QBarSeries()

        tmp = csvManager.getDataForBar([Dimention],[Measure])

            #all graph
        set0 = QtChart.QBarSet(Measure)
        set0.append(tmp)
        print(list(set0))
        self.series.append(set0)

        reg2 = csvManager.getAxisYName([Dimention])
        oneList = list(chain.from_iterable(reg2))
        oneList = map(str,oneList)
        months = tuple(oneList)

        min_x, max_x = 0, len(months)+10  

        self._chart.addSeries(self.series)
        self._chart.createDefaultAxes()
        self._chart.legend().hide()
        #self._chart.setAnimationOptions(QtChart.QChart.SeriesAnimations)

        months = tuple(months)

        '''axisX = QtChart.QBarCategoryAxis()
        axisX.append(months)

        axisY = QtChart.QValueAxis()
        axisY.applyNiceNumbers()'''

        #self._chart.addAxis(axisX, Qt.AlignBottom)
        #self._chart.addAxis(axisY, Qt.AlignLeft)

        '''self._chart.legend().setVisible(True)
        self._chart.legend().setAlignment(Qt.AlignBottom)'''
        if r:
            self._chart.axisX(self.series).setCategories(months) #############
        #self._chart.axisX(self.series).setVisible(False)
        
        self.series.setLabelsVisible()
        self._chart.setTitle(str(Dimention+'\twith\t'+Measure))
        self._chart_view.setChart(self._chart)
        self.adjust_axes(0, 100)
        self.lims = np.array([min_x, max_x])

        self.onAxisSliderMoved(self.scrollbar.value())

    def adjust_axes(self, value_min, value_max):
        self._chart.axisX(self.series).setRange(
            str(value_min), str(value_max)
        )
        self._chart.axisX(self.series).setRange(str(value_min), str(value_max))

    @QtCore.pyqtSlot(int)
    def onAxisSliderMoved(self, value):
        r = value / ((1 + self.step) * 100)
        l1 = self.lims[0] + r * np.diff(self.lims)
        l2 = l1 + np.diff(self.lims) * self.step 
        self.adjust_axes(math.floor(l1), math.ceil(l2))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
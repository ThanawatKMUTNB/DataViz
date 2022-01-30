from PyQt5 import QtCore, QtGui, QtWidgets, QtChart
from PyQt5.Qt import Qt
import math
import numpy as np
import pandas as pd


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.step = 0.1
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
        
        self.resize(640, 480)
        self._chart = QtChart.QChart()
        self.series = QtChart.QBarSeries()

        df = pd.read_csv('Superstore.csv', encoding='windows-1252')
        Reg = []
        for i in df['Region'].values:
            if i not in Reg:
                Reg.append(i)

        df.set_index('Region',inplace=True)
        profit = []
        for i in Reg:
            profit.append(sum(df.loc[i,'Profit']))
        
        min_x, max_x = 0, 2
        set0 = QtChart.QBarSet('Profit')
        set0.append(profit)
        self.series.append(set0)

        self._chart.addSeries(self.series)
        self._chart.createDefaultAxes()
        self._chart.legend().hide()
        #self._chart.setAnimationOptions(QtChart.QChart.SeriesAnimations)

        months = tuple(Reg)

        axisX = QtChart.QBarCategoryAxis()
        axisX.append(months)

        axisY = QtChart.QValueAxis()
        axisY.setRange(0, max(profit))

        #self._chart.addAxis(axisX, Qt.AlignBottom)
        #self._chart.addAxis(axisY, Qt.AlignLeft)

        self._chart.legend().setVisible(True)
        self._chart.legend().setAlignment(Qt.AlignBottom)

        self._chart.axisX(self.series).setCategories(Reg)
        #self._chart.axisX(self.series).setVisible(False)

        self._chart_view.setChart(self._chart)
        self.adjust_axes(100, 200)
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
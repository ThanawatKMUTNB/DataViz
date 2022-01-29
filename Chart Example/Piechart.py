import sys
from PyQt5 import QtCore, QtGui, QtWidgets , QtChart
from PyQt5.QtChart import QChart

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    series = QtChart.QPieSeries()
    series.append("Jane", 1)
    series.append("Joe", 2)
    series.append("Andy", 3)
    series.append("Barbara", 4)
    series.append("Axel", 5)

    chart = QtChart.QChart()
    chart.addSeries(series)
    chart.setTitle("Simple piechart example")
    chart.setAnimationOptions(QChart.SeriesAnimations)
    chart.legend().hide()

    series.setLabelsVisible()
    #series.setLabelsPosition(QtChart.QPieSlice.LabelInsideHorizontal)

    for slice in series.slices():
        slice.setLabel("{:.1f}%".format(100 * slice.percentage()))

    chartView = QtChart.QChartView(chart)
    chartView.setRenderHint(QtGui.QPainter.Antialiasing)

    window = QtWidgets.QMainWindow()
    window.setCentralWidget(chartView)
    window.resize(640, 480)
    window.show()

    sys.exit(app.exec())


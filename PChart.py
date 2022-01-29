import sys
from PyQt5 import QtCore, QtGui, QtWidgets , QtChart
from PyQt5.QtChart import QChart
import pandas as pd

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    df = pd.read_csv('Superstore.csv', encoding='windows-1252')
    Reg = []
    for i in df['Region'].values:
        if i not in Reg:
            Reg.append(i)

    df.set_index('Region',inplace=True)
    profit = []
    for i in Reg:
        profit.append(sum(df.loc[i,'Profit']))

    series = QtChart.QPieSeries()
    for i in range(len(Reg)):
        series.append(Reg[i], profit[i])

    chart = QtChart.QChart()
    chart.addSeries(series)
    chart.setTitle("Simple piechart example(Profit)")
    chart.setAnimationOptions(QChart.SeriesAnimations)
    chart.legend().hide()

    series.setLabelsVisible()
    #series.setLabelsPosition(QtChart.QPieSlice.LabelInsideHorizontal)

    for slice , i in zip(series.slices(),Reg):
        slice.setLabel(i)

    chartView = QtChart.QChartView(chart)
    chartView.setRenderHint(QtGui.QPainter.Antialiasing)

    window = QtWidgets.QMainWindow()
    window.setCentralWidget(chartView)
    window.resize(640, 480)
    window.show()

    sys.exit(app.exec())
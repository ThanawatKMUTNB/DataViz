import sys
from PyQt5 import QtCore, QtGui, QtWidgets , QtChart
from PyQt5.QtChart import QChart
import pandas as pd
import csvManager

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    df = pd.read_csv('Superstore.csv', encoding='windows-1252')
    Dimention = 'Sub-Category'
    Measure = 'Profit'

    M = csvManager.getValueDimention(Dimention)
    df.set_index(Dimention,inplace=True)
    profit = []
    for i in M:
        profit.append(sum(df.loc[i,Measure]))

    series = QtChart.QPieSeries()
    for i in range(len(M)):
        series.append(M[i], profit[i])

    chart = QtChart.QChart()
    chart.addSeries(series)
    chart.setTitle(str(Dimention+'\twith\t'+Measure))
    chart.setAnimationOptions(QChart.SeriesAnimations)
    chart.legend().hide()

    series.setLabelsVisible()
    #series.setLabelsPosition(QtChart.QPieSlice.LabelInsideHorizontal)

    for slice , i in zip(series.slices(),M):
        s = str(i+"\t{:.1f}%".format(100 * slice.percentage()))
        slice.setLabel(s)

    chartView = QtChart.QChartView(chart)
    chartView.setRenderHint(QtGui.QPainter.Antialiasing)

    window = QtWidgets.QMainWindow()
    window.setCentralWidget(chartView)
    window.resize(840, 680)
    window.show()

    sys.exit(app.exec())
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from io import StringIO
import altair as alt

from altair import pipe, limit_rows, to_values
t = lambda data: pipe(data, limit_rows(max_rows=10000), to_values)
alt.data_transformers.register('custom', t)
alt.data_transformers.enable('custom')


class WebEngineView(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.page().profile().downloadRequested.connect(self.onDownloadRequested)
        self.windows = []

    @QtCore.pyqtSlot(QtWebEngineWidgets.QWebEngineDownloadItem)
    def onDownloadRequested(self, download):
        if (
            download.state()
            == QtWebEngineWidgets.QWebEngineDownloadItem.DownloadRequested
        ):
            path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, self.tr("Save as"), download.path()
            )
            if path:
                download.setPath(path)
                download.accept()

    def createWindow(self, type_):
        if type_ == QtWebEngineWidgets.QWebEnginePage.WebBrowserTab:
            window = QtWidgets.QMainWindow(self)
            view = QtWebEngineWidgets.QWebEngineView(window)
            window.resize(640, 480)
            window.setCentralWidget(view)
            window.show()
            return view

    def updateChart(self, chart, **kwargs):
        output = StringIO()
        chart.save(output, "html", **kwargs)
        self.setHtml(output.getvalue())

def VerticalBar(df):
    c = alt.Chart(df).mark_bar().encode(
        x=str(Di2+':N'),
        y=str(Measure+':Q')
        #color=str(Di1+':N')
    ).facet(column=str(Di1+':N')
    ).resolve_scale(x = 'independent')

    view = WebEngineView()
    view.updateChart(c)
    w.setCentralWidget(view)
    #w.resize(640, 480)
    w.show()
    
def HoriBar(df):
    c = alt.Chart(df).mark_bar().encode(
        y=str(Di1+':O'),
        x=str(Measure)
    ).facet(row=str(Di2+':N')
    ).resolve_scale(y = 'independent')

    view = WebEngineView()
    view.updateChart(c)
    w.setCentralWidget(view)
    #w.resize(640, 480)
    w.show()

if __name__ == "__main__":
    import sys
    import pandas as pd
    from vega_datasets import data

    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QMainWindow()

    Di1 = "State"
    Di2 = 'Region'
    Measure = 'Quantity'
    f1 = 'SS_20lines.csv'
    f2 = 'SS_100lines.csv'
    f3 = 'Superstore.csv'
    df = pd.read_csv(f2, encoding='windows-1252')
    HoriBar(df)
    
    sys.exit(app.exec_())
import sys
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import pyqtSlot, Qt, QTimer

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(700, 100, 350, 380)
        self.createTable()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.button = QPushButton('Print DataFrame', self)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.print_my_df)
        self.tableWidget.doubleClicked.connect(self.on_click_table)
        self.show()

    def createTable(self):
        self.tableWidget = QTableWidget()
        self.df_rows = 10
        self.df_cols = 3
        self.df = pd.DataFrame(np.random.randn(self.df_rows, self.df_cols))
        self.tableWidget.setRowCount(self.df_rows)
        self.tableWidget.setColumnCount(self.df_cols)
        for i in range(self.df_rows):
            for j in range(self.df_cols):
                x = format(self.df.iloc[i, j])
                self.tableWidget.setItem(i, j, QTableWidgetItem(x))

    @pyqtSlot()
    def print_my_df(self):
        print(self.df)

    @pyqtSlot()
    def on_click_table(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print((currentQTableWidgetItem.row(), currentQTableWidgetItem.column()))
            self.print_my_df()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
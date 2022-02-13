import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox, QGridLayout, QWidget, QPushButton, QListWidget

lines2 = []
lines3 = []
Name = []
AmountF = ['5','20','0.5','2','1']
AmountV = ['0.25','0.2','14','6']


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        self.setGeometry(50, 50, 500, 500)
        self.dropdown = QComboBox()
        self.Open = QPushButton('Open')
        self.ListBox = QListWidget()
        self.dropdown.activated.connect(self.enter)
        self.Open.clicked.connect(self.open)
        self.show()

        layout = QGridLayout(centralWidget)
        layout.addWidget(self.dropdown)
        layout.addWidget(self.ListBox)
        layout.addWidget(self.Open)


    def open(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'Select File')
        file = open(name[0], 'r')
        lines = file.readlines()

        for L in lines[0:6]:
            LI = L.replace('\n','')
            lines2.insert(0,LI)

        for L in lines[6:]:
            Li = L.replace('\n','')
            lines3.insert(0,Li)

        Name.insert(0,lines2[-1])
        Name.insert(0,lines3[4])
        del lines2[-1]
        del lines3[-1]
        for items in lines3:
            self.ListBox.insertItem(0, items)
        for item in Name:
            self.dropdown.insertItem(0, item)


    def enter(self):
        self.ListBox.clear()
        if self.dropdown.itemText(0) == Name[0]:
            for items in lines3:
                self.ListBox.insertItem(0, items)
        elif self.dropdown.itemText(1) == Name[1]:
            for item in lines2:
                self.ListBox.insertItems(0, item)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
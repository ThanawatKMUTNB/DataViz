from pyface.qt import QtGui, QtCore
import sys

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.vbox = QtGui.QVBoxLayout()
        self.label3 = QtGui.QLabel()
        self.slider = QtGui.QSlider()
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setTickPosition(QtGui.QSlider.TicksLeft)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.vbox.addWidget(self.slider,QtCore.Qt.AlignBottom)
        self.vbox.addWidget(self.label3)
        self.setLayout(self.vbox)
        self.setGeometry(300, 300, 300, 150)
        self.slider.valueChanged.connect(self.valuechange)
        self.show()

    def valuechange(self):
        txt = str(self.slider.value())
        self.label3.setText(txt)

def main():    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
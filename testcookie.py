from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu
import sys
from PyQt5.QtCore import QEvent


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.createWidgets()

    def createWidgets(self):
        self.my_button = QtWidgets.QPushButton(self)
        self.my_button.setText("My Widget")

        self.buttonMenu = QMenu(self.my_button)
        self.buttonMenu.addAction("Option 1")
        self.buttonMenu.addAction("Option 2")
        self.buttonMenu.addAction("Option 3")

        self.subMenu = QMenu(self.buttonMenu)
        self.subMenu.addAction("Sub Option 1")
        self.subMenu.addAction("Sub Option 2")
        self.subMenu.addAction("Sub Option 3")

        self.my_button.installEventFilter(self)
        self.buttonMenu.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu:
            if source == self.my_button:
                self.buttonMenu.exec_(event.globalPos())
                return True
            elif source == self.buttonMenu:
                self.subMenu.exec_(event.globalPos())
                return True

        return super().eventFilter(source, event)




def showWindow():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

showWindow()
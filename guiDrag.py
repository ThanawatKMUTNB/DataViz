import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

class Button(QPushButton):
    def __init__(self, button_text, parent):
        super().__init__(button_text, parent)
        self.setStyleSheet('width: 200px; height: 50px; font-size: 30px')

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            mimeData = QMimeData()
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.exec_(Qt.MoveAction)

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 400)
        self.setAcceptDrops(True)

        self.button = Button('My Button', self)
        self.button.move(50, 50)

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        position = event.pos()
        self.button.move(position)
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec_())
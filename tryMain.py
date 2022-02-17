import sys, os
from PyQt4 import QtCore, QtGui   
class ThumbListWidget(QtGui.QListWidget):
    def __init__(self, type, parent=None):
        super(ThumbListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setIconSize(QtCore.QSize(124, 124))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(QtCore.SIGNAL("dropped"), links)
        else:
            event.ignore()


class Dialog_01(QtGui.QMainWindow):
    def __init__(self):
        super(QtGui.QMainWindow,self).__init__()
        self.listItems={}

        myQWidget = QtGui.QWidget()
        myBoxLayout = QtGui.QVBoxLayout()
        myQWidget.setLayout(myBoxLayout)
        self.setCentralWidget(myQWidget)

        self.listWidgetA = ThumbListWidget(self)
        for i in range(12): 
            QtGui.QListWidgetItem( 'Item '+str(i), self.listWidgetA )
        myBoxLayout.addWidget(self.listWidgetA)

        self.listWidgetB = ThumbListWidget(self)
        myBoxLayout.addWidget(self.listWidgetB)   

        self.listWidgetA.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.listWidgetA.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.connect(self.listWidgetA, QtCore.SIGNAL("dropped"), self.items_dropped)
        self.listWidgetA.currentItemChanged.connect(self.item_clicked)

        self.listWidgetB.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.listWidgetB.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.connect(self.listWidgetB, QtCore.SIGNAL("dropped"), self.items_dropped)
        self.listWidgetB.currentItemChanged.connect(self.item_clicked)

    def items_dropped(self, arg):
        print arg

    def item_clicked(self, arg):
        print arg

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dialog_1 = Dialog_01()
    dialog_1.show()
    dialog_1.resize(480,320)
    sys.exit(app.exec_())
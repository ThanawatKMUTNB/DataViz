from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem
import sys

class Tree(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDragDropMode(self.DragDrop)
        self.setSelectionMode(self.ExtendedSelection)
        self.setAcceptDrops(True)

        for text in ['tree1','tree2','tree3']:
            treeItem = QtWidgets.QTreeWidgetItem(self, [text])
            treeItem.setFlags(treeItem.flags() & ~QtCore.Qt.ItemIsDropEnabled)
            self.addTopLevelItem(treeItem)

    def dropEvent(self, event):
        if event.source() == self:
            event.setDropAction(QtCore.Qt.MoveAction)
            super().dropEvent(event)
        elif isinstance(event.source(), QtWidgets.QListWidget):
            item = self.itemAt(event.pos())
            ix = self.indexAt(event.pos())
            col = 0 if item is None else ix.column()
            item = self.invisibleRootItem() if item is None else item
            ba = event.mimeData().data('application/x-qabstractitemmodeldatalist')
            data_items = decode_data(ba)
            for data_item in data_items:
                it = QtWidgets.QTreeWidgetItem()
                item.addChild(it)
                for data in data_items:
                    for r, v in data.items():
                        it.setData(col, r, v)


class List(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDragDropMode(self.DragDrop)
        self.setSelectionMode(self.ExtendedSelection)
        self.setAcceptDrops(True)

        for text in ['list1','list2','list3']:
            self.addItem(text)

    def dropEvent(self, event):
        if event.source() == self:
            event.setDropAction(QtCore.Qt.MoveAction)
            QtWidgets.QListWidget.dropEvent(self, event)
        elif isinstance(event.source(), QtWidgets.QTreeWidget):
            item = self.itemAt(event.pos())
            row = self.row(item) if item else self.count()
            ba = event.mimeData().data('application/x-qabstractitemmodeldatalist')
            data_items = decode_data(ba)
            for i, data_item in enumerate(data_items):
                it = QtWidgets.QListWidgetItem()
                self.insertItem(row+i, it)
                for r, v in data_item.items():
                    it.setData(r,v)


def decode_data(bytearray):

    data = []
    item = {}

    ds = QtCore.QDataStream(bytearray)
    while not ds.atEnd():

        row = ds.readInt32()
        column = ds.readInt32()

        map_items = ds.readInt32()
        for i in range(map_items):
            key = ds.readInt32()

            value = QtCore.QVariant()
            ds >> value
            item[Qt.ItemDataRole(key)] = value

        data.append(item)
    return data

if __name__=='__main__':

    app = QtWidgets.QApplication(sys.argv)

    layout = QtWidgets.QHBoxLayout()
    layout.addWidget(Tree())
    layout.addWidget(List())

    container = QtWidgets.QWidget()
    container.setLayout(layout)
    container.show()

    app.exec_()
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createSample.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from ultis import *
import numpy as np
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtCore import Qt


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        uic.loadUi('test.ui', self)
        aa = self.frame.size()
        canvas = QtGui.QPixmap(aa.height(), aa.width())
        self.x, self.y = aa.height(), aa.width()
        self.resize(self.y, self.x)
        canvas.fill(Qt.transparent)
        self.label.setPixmap(canvas)
        # self.label.setStyleSheet("background-color: (255,0,0,0)")
        # self.frame.addWidget(self.label)
        self.box = QVBoxLayout(self.frame)
        self.box.setObjectName(u"box")
        self.box.addWidget(self.label)
        self.setCentralWidget(self.frame)
        self.draw_something()

    def draw_something(self):
        painter = QtGui.QPainter(self.label.pixmap())
        painter.drawLine(self.y//2, self.x//2, 0, self.x//2)
        painter.end()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    # ui.setupUi()
    ui.show()
    sys.exit(app.exec_())

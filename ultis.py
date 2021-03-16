from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
import argparse
from PyQt5.QtCore import Qt


class textSpinBox(QSpinBox):
    def __init__(self, parent=None):
        super(textSpinBox, self).__init__(parent)
        self.colors = arg.colors
        self.setRange(0, len(self.colors) - 1)

    def textFromValue(self, value):
        self.setStyleSheet("color: {}".format(self.colors[self.value()]))
        return self.colors[value]


class sampleNumber(QFrame):
    """docstring for sampleNumber"""

    def __init__(self, arg=None):
        super(sampleNumber, self).__init__()
        self.id = arg
        self.sample()
        self.cl = -1
        self.num = -1
        self.label = None

    def sample(self):
        self.setObjectName(u"frame" + str(self.id))
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        self.box = QVBoxLayout(self)
        self.box.setObjectName(u"box")
        self.pushButton = QPushButton()
        self.pushButton.setObjectName(u"pushButton")
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.font = font
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);border: none;color: white;")
        # self.pushButton.setText(str(self.id))

        self.box.addWidget(self.pushButton, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.resetStyleSheet()

    def updateStyleSheet(self, color):
        self.setStyleSheet(u"border-width: 1;\n"
                           "border-radius: 3;\n"
                           "border-style: dashed;\n"
                           "border-color: rgb(10, 10, 10);\n"
                           "background-color: {}".format(color))

    def setText(self, text):
        self.pushButton.setText(text)

    def setPos(self, idy, idx):
        self.idy = idy
        self.idx = idx

    def getPos(self):
        return self.idy, self.idx

    def resetStyleSheet(self):
        self.setStyleSheet(u"border-width: 1;\n"
                           "border-radius: 3;\n"
                           "border-style: dashed;\n"
                           "border-color: rgb(10, 10, 10);\n")

    def addLabel(self):
        y, x = self.size().height(), self.size().width()
        canvas = QtGui.QPixmap(y, x)
        canvas.fill(Qt.transparent)
        self.label = QtWidgets.QLabel()
        self.label.setStyleSheet("border: 0px;")
        self.label.setPixmap(canvas)
        self.pushButton.setParent(None)
        self.box.addWidget(self.label)

    def displayPos(self, d):
        y, x = self.size().height(), self.size().width()
        if d == 2:
            return x // 2, y // 2, 0, y // 2
        if d == 4:
            return x // 2, y // 2, x, y // 2
        if d == 1:
            return x // 2, y // 2, x // 2, 0

        return x // 2, y // 2, x // 2, y

    def plotLabel(self, d):
        if self.label is None:
            self.addLabel()
        y1, x1, y2, x2 = self.displayPos(d)
        painter = QtGui.QPainter(self.label.pixmap())
        painter.drawLine(x1, y1, x2, y2)
        painter.setPen(QtGui.QColor("white"))
        painter.setFont(self.font)
        if self.num != -1:
            painter.drawText(self.rect(), Qt.AlignCenter, str(self.num))
        painter.end()


class arguments(argparse.Namespace):
    colors = ['aqua', 'aquamarine', 'blue', 'brown', 'chartreuse', 'chocolate', 'coral',
              'crimson', 'cyan', 'darkblue', 'darkgreen', 'fuchsia', 'gold', 'goldenrod', 'green', 'grey', 'indigo',
              'ivory', 'khaki', 'lavender', 'lightblue', 'lightgreen', 'lime', 'magenta', 'maroon', 'navy', 'olive',
                       'orange', 'orangered', 'orchid', 'pink', 'plum', 'purple', 'red', 'salmon', 'sienna', 'silver', 'tan',
                       'teal', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'yellow', 'yellowgreen']


arg = arguments

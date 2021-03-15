from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
import argparse


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


class arguments(argparse.Namespace):
    colors = ['aqua', 'aquamarine', 'black', 'blue', 'brown', 'chartreuse', 'chocolate', 'coral',
              'crimson', 'cyan', 'darkblue', 'darkgreen', 'fuchsia', 'gold', 'goldenrod', 'green', 'grey', 'indigo',
              'ivory', 'khaki', 'lavender', 'lightblue', 'lightgreen', 'lime', 'magenta', 'maroon', 'navy', 'olive',
                       'orange', 'orangered', 'orchid', 'pink', 'plum', 'purple', 'red', 'salmon', 'sienna', 'silver', 'tan',
                       'teal', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'yellow', 'yellowgreen']


arg = arguments

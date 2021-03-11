# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createSample.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        uic.loadUi('numberLink.ui', self)

        self.setObjectName("NumberLink")
        self.resize(int(1500), int(850))
        widget = QtWidgets.QWidget()
        widget.setLayout(self.horizontalLayout)
        self.setCentralWidget(widget)

        self.listColor = []
        self.colors = ['aqua', 'aquamarine', 'black', 'blue', 'brown', 'chartreuse', 'chocolate', 'coral',
                  'crimson', 'cyan', 'darkblue', 'darkgreen', 'fuchsia', 'gold', 'goldenrod', 'green', 'grey', 'indigo',
                  'ivory', 'khaki', 'lavender', 'lightblue', 'lightgreen', 'lime', 'magenta', 'maroon', 'navy', 'olive',
                  'orange', 'orangered', 'orchid', 'pink', 'plum', 'purple', 'red', 'salmon', 'sienna', 'silver', 'tan',
                  'teal', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'yellow', 'yellowgreen']
        self.createEvent()

    def createEvent(self):
        self.createMatrixBtn.clicked.connect(self.genMatrix)
        self.numSizeMatrix.setMinimum(2)
        self.numSizeMatrix.setMaximum(10)

    def genMatrix(self):
        self.sizeMatrix = self.numSizeMatrix.value()
        self.listObject = []
        for idy in range(self.sizeMatrix):
            for idx in range(self.sizeMatrix):
                newId = idy * self.sizeMatrix + idx
                newObj = sampleNumber(newId)
                newObj.updateStyleSheet(self.colors[newId % 30])
                self.gridLayout.addWidget(newObj, idy, idx)

class sampleNumber(QFrame):
    """docstring for sampleNumber"""

    def __init__(self, arg=None):
        super(sampleNumber, self).__init__()
        self.id = arg
        self.sample()

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
        self.pushButton.setText(str(self.id))

        self.box.addWidget(self.pushButton, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def updateStyleSheet(self, color):
        self.setStyleSheet(u"border-width: 1;\n"
                                 "border-radius: 3;\n"
                                 "border-style: dashed;\n"
                                 "border-color: rgb(10, 10, 10);\n"                                 
                                 "background-color: {}".format(color))

    def setText(self, text):
        self.pushButton.setText(text)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    # ui.setupUi()
    ui.show()
    sys.exit(app.exec_())

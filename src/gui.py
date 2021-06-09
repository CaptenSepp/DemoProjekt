# -*- coding: utf-8 -*-

import sys

import matplotlib
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class App(QMainWindow):
    def __init__(self, plotFunction, guiReadyFunction = None):
        super().__init__()
        self.plotFunction = plotFunction

        TopVLayout = QVBoxLayout()

        self.mplcanvas = MplCanvas()
        TopVLayout.addWidget(self.mplcanvas)

        paramWidget = QHBoxLayout()
        self.BundeslandSelect = QComboBox()
        paramWidget.addWidget(self.BundeslandSelect)
        self.BundeslandSelect.setMinimumWidth(300)

        paramWidget.addStretch()
        TopVLayout.addLayout(paramWidget)

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(TopVLayout)
        self.setWindowTitle("Demo Datenauswertung")
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(800, 400)
        self.BundeslandSelect.currentTextChanged.connect(self.parameterChanged)
        self.show()


        if guiReadyFunction:
            guiReadyFunction(self)

    def showStatusText(self, msg, executeEventLoop=False):
        self.statusBar().showMessage(msg)

        if executeEventLoop:
            QApplication.processEvents()
            QApplication.processEvents()

    def parameterChanged(self, *args):
        bundesland = self.BundeslandSelect.currentText()

        ax = self.mplcanvas.ax
        ax.cla()
        self.plotFunction(ax, bundesland)
        self.mplcanvas.draw()

    def setBundeslaender(self, listeBundeslaender):
        self.BundeslandSelect.clear()
        for bl in listeBundeslaender:
            self.BundeslandSelect.addItem(bl)

if __name__ == '__main__':
    import numpy as np


    def plotFunction(ax, bundesland):
        print("PlotFunction('{}')".format(bundesland))


    app = QApplication(sys.argv)
    window = App(plotFunction=plotFunction)
    window.setBundeslaender("ns,by,mp".split(','))
    sys.exit(app.exec_())

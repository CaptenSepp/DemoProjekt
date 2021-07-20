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
        self.GeschlechtSelect = QComboBox()
        paramWidget.addWidget(self.GeschlechtSelect)
        self.GeschlechtSelect.setMinimumWidth(300)

        paramWidget.addStretch()
        TopVLayout.addLayout(paramWidget)

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(TopVLayout)
        self.setWindowTitle("Demo Datenauswertung")
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(800, 400)
        self.GeschlechtSelect.currentTextChanged.connect(self.parameterChanged)
        self.show()


        if guiReadyFunction:
            guiReadyFunction(self)

    def showStatusText(self, msg, executeEventLoop=False):
        """
        Hiermit kann von der main.py aus der Text der Statusleiste festgelegt werden
        :param msg: Test, der angezeigt werden soll.
        :param executeEventLoop: Wenn True, dann wird die Eventloop abgearbeitet, damit es zur sofortigen Anzeige kommt.
        :return: None

        This can be used to define the text of the status-bar from main.py
         : param msg: test to be displayed.
         : param executeEventLoop: If True, the event loop is processed so that it is displayed immediately.
         : return: None
        """
        self.statusBar().showMessage(msg)

        if executeEventLoop:
            QApplication.processEvents()
            QApplication.processEvents()

    def parameterChanged(self, *args):
        """
        Aufrufe, wenn sich ein Parameter der GUI ändert.
        :return: None

        Calls when a parameter of the GUI changes.
         : return: None
        """
        # geschlecht = self.Geschlechtselect.currentText()
        ax = self.mplcanvas.ax
        ax.cla()
        # if geschlecht == 'M':
        #     self.plotFunction(ax, 'M')
        # elif geschlecht == 'W':
        #     self.plotFunction(ax, 'W')
        # elif geschlecht == 'unbekannt':
        #     self.plotFunction(ax, 'unbekannt')
        # else:
        self.plotFunction(ax, 'M')
        self.plotFunction(ax, 'W')
        self.plotFunction(ax, 'unbekannt')
        self.mplcanvas.draw()

    def setGeschlecht(self, listeGeschlecht):
        """
        Listeneinträge in der Combobox festlegen.
        :param listeBundeslaender: Liste mit Strings der Bundesland-Namen
        :return: None

        Define list entries in the combo-box.
         : param listeBundeslaender: List with strings of the state names
         : return: None
        """
        self.GeschlechtSelect.clear()
        # for bl in listeGeschlecht:
        #     self.GeschlechtSelect.addItem(bl)
        self.GeschlechtSelect.addItem("M-W-Unbekannt")


if __name__ == '__main__':
    import numpy as np


    def plotFunction(ax, bundesland):
        print("PlotFunction('{}')".format(bundesland))

    app = QApplication(sys.argv)
    window = App(plotFunction=plotFunction)
    window.setGeschlecht("ns,by,mp".split(',')) # bayad baraye analyze dovomam benevisim???
    sys.exit(app.exec_())

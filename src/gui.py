# -*- coding: utf-8 -*-

import sys

import matplotlib
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):  #
    def __init__(self, parent=None, width=5, height=4, dpi=100):  # 100 hamechi ro taghir mide
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class App(QMainWindow):
    def __init__(self, plotFunction, guiReadyFunction=None):
        super().__init__()
        self.plotFunction = plotFunction

        TopVLayout = QVBoxLayout()

        self.mplcanvas = MplCanvas()  # inja Classe Mplcanvas estefade shode
        TopVLayout.addWidget(self.mplcanvas)

        paramWidget = QHBoxLayout()
        self.AnalyseSelect = QComboBox()
        paramWidget.addWidget(self.AnalyseSelect)
        self.AnalyseSelect.setMinimumWidth(150)

        self.BundeslandSelect = QComboBox()  # todo Bundesland addieren
        paramWidget.addWidget(self.BundeslandSelect)
        self.BundeslandSelect.setMinimumWidth(200)

        self.StartDateSelect = QComboBox()
        paramWidget.addWidget(self.StartDateSelect)
        self.StartDateSelect.setMinimumWidth(200)

        self.EndDateSelect = QComboBox()
        paramWidget.addWidget(self.EndDateSelect)
        self.EndDateSelect.setMinimumWidth(200)

        paramWidget.addStretch()
        TopVLayout.addLayout(paramWidget)

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(TopVLayout)
        self.setWindowTitle("COVID-19 Datenauswertung")
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(800, 400)
        self.AnalyseSelect.currentTextChanged.connect(self.parameterChanged)
        self.BundeslandSelect.currentTextChanged.connect(self.parameterChanged)
        self.StartDateSelect.currentTextChanged.connect(self.parameterChanged)
        self.EndDateSelect.currentTextChanged.connect(self.parameterChanged)
        self.show()

        if guiReadyFunction:
            guiReadyFunction(self)

    def showStatusText(self, msg, executeEventLoop=False):
        """
        Hiermit kann von der main.py aus der Text der Statusleiste festgelegt werden
        :param msg: Test, der angezeigt werden soll.
        :param executeEventLoop: Wenn True, dann wird die Eventloop abgearbeitet, damit es zur sofortigen Anzeige kommt.
        :return: None
        """
        self.statusBar().showMessage(msg)

        if executeEventLoop:
            QApplication.processEvents()
            QApplication.processEvents()

    def parameterChanged(self, *args):
        """
        Aufrufe, wenn sich ein Parameter der GUI ändert.
        :return: None
        """
        choice = self.AnalyseSelect.currentText()
        bundesland = self.BundeslandSelect.currentText()
        startDate = self.StartDateSelect.currentText()
        endDate = self.EndDateSelect.currentText()
        ax = self.mplcanvas.ax
        # object az mplcanvas   fig.add_subplot(111)
        ax.cla()
        # ax nemudaras ke ma mikhaym
        if (choice != "" and bundesland != "" and startDate != "" and endDate!= ""):
            if (choice == 'M-W-Unbekannt'):
                self.plotFunction(ax, 'M', bundesland, startDate, endDate)
                self.plotFunction(ax, 'W', bundesland, startDate, endDate)
                self.plotFunction(ax, 'unbekannt', bundesland, startDate, endDate)
            elif (choice == 'Tod-Anzahlfall'):
                self.plotFunction(ax, 'AnzahlFall', bundesland, startDate, endDate)
            self.mplcanvas.draw()

    def setter(self, bundeslands, dates):  # todo
        """
        Listeneinträge in der Combobox festlegen.
        :param Analyse: Liste mit Strings der Analyse
        :return: None
        """
        self.AnalyseSelect.clear()
        self.AnalyseSelect.addItem("M-W-Unbekannt")
        self.AnalyseSelect.addItem("Tod-Anzahlfall")

        self.BundeslandSelect.clear()
        for i in bundeslands:
            self.BundeslandSelect.addItem(i)

        self.StartDateSelect.clear()
        for i in dates:
            self.StartDateSelect.addItem(i)

        self.EndDateSelect.clear()
        for i in dates:
            self.EndDateSelect.addItem(i)

    def setBundesland(self, listeBundeslaender):  # todo inja bayad
        """
        Listeneinträge in der Combobox festlegen.
        :param listeBundeslaender: Liste mit Strings der Bundesland-Namen
        :return: None
        """
        self.BundeslandSelect.clear()
        for bl in listeBundeslaender:
            self.BundeslandSelect.addItem(bl)

# if __name__ == '__main__': # todo in code payin kari nemikone, baraye chi neveshte shode, ma kamentesh kardim baz kar mikone
#     import numpy as np
#
#     def plotFunction(ax, bundesland):
#         print("PlotFunction('{}')".format(bundesland))
#
#     app = QApplication(sys.argv)
#     window = App(plotFunction=plotFunction)
#     window.setGeschlecht("ns,by,mp".split(',')) # bayad baraye analyze dovomam benevisim???
#     sys.exit(app.exec_())

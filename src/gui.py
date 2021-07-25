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
        self.AnalyseSelect.setToolTip("Hier Können Sie die Analysen auswählen")
        paramWidget.addWidget(self.AnalyseSelect)
        self.AnalyseSelect.setMinimumWidth(250)

        self.BundeslandSelect = QComboBox()  # Bundesland addieren
        self.BundeslandSelect.setToolTip("Hier Können Sie die Bundesland auswählen")
        paramWidget.addWidget(self.BundeslandSelect)
        self.BundeslandSelect.setMinimumWidth(150)

        self.AltersgruppeSelect = QComboBox()
        self.AltersgruppeSelect.setToolTip("Hier Können Sie die Altersgruppe auswählen")
        paramWidget.addWidget(self.AltersgruppeSelect)
        self.AltersgruppeSelect.setMinimumWidth(100)

        self.StartDateSelect = QComboBox()
        self.StartDateSelect.setToolTip("Hier Können Sie die Start Datum auswählen")
        paramWidget.addWidget(self.StartDateSelect)
        self.StartDateSelect.setMinimumWidth(100)

        self.EndDateSelect = QComboBox()
        self.EndDateSelect.setToolTip("Hier Können Sie die Ende Datum auswählen")
        paramWidget.addWidget(self.EndDateSelect)
        self.EndDateSelect.setMinimumWidth(100)
        # **********************************************************************************
        saveWidget = QHBoxLayout()  # todo hier funktioniert leider den Speichern nicht
        saveWidget.addStretch()
        saveWidget.addStretch()
        self.SaveButton = QPushButton('Save Graph', self)
        self.SaveButton.setToolTip("Name der Datei über Input rechts eingeben (ohne Dateiendung)")
        saveWidget.addWidget(self.SaveButton)
        self.SaveName = QLineEdit()
        saveWidget.addWidget(self.SaveName)
        saveWidget.addStretch()
        TopVLayout.addLayout(saveWidget)
        # ********************************************************************************
        paramWidget.addStretch()
        TopVLayout.addLayout(paramWidget)

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(TopVLayout)
        self.setWindowTitle("COVID-19 Datenauswertung")
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(800, 800)
        self.AnalyseSelect.currentTextChanged.connect(self.parameterChanged)
        self.BundeslandSelect.currentTextChanged.connect(self.parameterChanged)
        self.AltersgruppeSelect.currentTextChanged.connect(self.parameterChanged)
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
        altersgruppe = self.AltersgruppeSelect.currentText()
        startDate = self.StartDateSelect.currentText()
        endDate = self.EndDateSelect.currentText()  # todo give the last date in the list
        ax = self.mplcanvas.ax  # object az mplcanvas   fig.add_subplot(111)
        ax.cla()  # ax nemudaras ke ma mikhaym

        if (choice != "" and bundesland != "" and startDate != "" and endDate != ""):
            if (choice == 'M-W-Unbekannt'):
                if (
                        bundesland == 'Alle Bundesländer'):  # todo, hier muss Bundesland filter nicht mehr betrachtet werden
                    self.plotFunction(ax, 'M', True, altersgruppe, startDate, endDate)
                    self.plotFunction(ax, 'W', True, altersgruppe, startDate, endDate)
                    self.plotFunction(ax, 'unbekannt', True, altersgruppe, startDate, endDate)
                else:
                    self.plotFunction(ax, 'M', bundesland, altersgruppe, startDate, endDate)
                    self.plotFunction(ax, 'W', bundesland, altersgruppe, startDate, endDate)
                    self.plotFunction(ax, 'unbekannt', bundesland, altersgruppe, startDate, endDate)
            elif (choice == "M"):
                self.plotFunction(ax, 'M', bundesland, altersgruppe, startDate, endDate)
            elif (choice == "W"):
                self.plotFunction(ax, 'W', bundesland, altersgruppe, startDate, endDate)
            elif (choice == 'Vergleich Todesfälle und Neuinfektionen'):
                self.plotFunction(ax, 'AnzahlFall', bundesland, altersgruppe, startDate, endDate)
            self.mplcanvas.draw()

    def ComboBoxSetter(self, bundeslands, altersgruppe, dates):  # todo
        """
        Listeneinträge in der Combobox festlegen.
        :param Analyse: Liste mit Strings der Analyse
        :return: None
        """
        self.AnalyseSelect.clear()
        self.AnalyseSelect.addItem('M-W-Unbekannt')
        self.AnalyseSelect.addItem('M')  # todo die getrennt machen, wenn ich zeit habe
        self.AnalyseSelect.addItem('W')
        self.AnalyseSelect.addItem('Vergleich Todesfälle und Neuinfektionen')

        self.BundeslandSelect.clear()
        for i in bundeslands:
            self.BundeslandSelect.addItem(i)
        self.BundeslandSelect.addItem('Alle Bundesländer')

        self.AltersgruppeSelect.clear()
        for i in altersgruppe:
            self.AltersgruppeSelect.addItem(i)
        self.AltersgruppeSelect.addItem('Alle Altersgruppen')

        self.StartDateSelect.clear()
        for i in dates:
            self.StartDateSelect.addItem(str(i)[0:10])

        self.EndDateSelect.clear()
        for i in range(len(dates)):
            self.EndDateSelect.addItem(str(dates[len(dates) - i - 1])[
                                       0:10])  # todo hier will ich die letzte option von Datum liegen, letzte was im Datei gibt

    # def setBundesland(self, listeBundeslaender):                                      # todo inja bayad
    #     """
    #     Listeneinträge in der Combobox festlegen.
    #     :param listeBundeslaender: Liste mit Strings der Bundesland-Namen
    #     :return: None
    #     """
    #
    #     self.BundeslandSelect.clear()
    #     for bl in listeBundeslaender:
    #         self.BundeslandSelect.addItem(bl)

    def SaveGraph(self):  # todo das funktioniert leider nicht
        """
        Save-Button führt zu dieser Funktion.
        Es öffnet sich ein Dialog der das abspeichern nocheinmal hinterfragen soll.
        Funktion Speichervorgang abbrechen leider mehrmals versucht, aber gescheitert.
        param: None
        return: None
        """
        msgbox = QMessageBox()
        msgbox.setText(
            "Wenn sie den Graphen unter einem bereits existierenden Namen abspeichern, wird der alte Graph automatisch überschrieben.\n"
            "Möchten Sie trotzdem fortfahren?\n"
            "\n")
        msgbox.addButton(QMessageBox.Ok)
        msgbox.setIcon(QMessageBox.Question)
        msgbox.exec()
        savetext = self.SaveName.text()
        img = self.mplcanvas
        img.print_figure(
            '//home//student//prog1_ss2021//2438125_Partsch//Projekt//Saved Figures//{}.png'.format(savetext))
        # print("Speichern hat funktioniert")

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

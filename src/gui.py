# -*- coding: utf-8 -*-
from RKIAnalyzer import RKIAnalyzer
import matplotlib
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
        self.mplcanvas = MplCanvas()

        paramWidget = QHBoxLayout()
        self.AnalyseSelect = QComboBox()
        self.AnalyseSelect.setToolTip("Hier Können Sie die Analysen auswählen")
        paramWidget.addWidget(self.AnalyseSelect)
        self.AnalyseSelect.setMinimumWidth(250)
        # Hier werden die verschiedenen Parameter in Comboboxen addiert
        self.BundeslandSelect = QComboBox()
        self.BundeslandSelect.setMaxVisibleItems(20)
        tooltip = "Hier Können Sie das Bundesland auswählen" # todo beabrbeiten
        self.BundeslandSelect.setToolTip(tooltip)
        paramWidget.addWidget(self.BundeslandSelect)
        self.BundeslandSelect.setMinimumWidth(150)

        self.AltersgruppeSelect = QComboBox()
        self.AltersgruppeSelect.setToolTip("Hier Können Sie die Altersgruppe auswählen")
        paramWidget.addWidget(self.AltersgruppeSelect)
        self.AltersgruppeSelect.setMinimumWidth(100)

        self.StartDateSelect = QComboBox()
        self.StartDateSelect.setMaxVisibleItems(50)
        self.StartDateSelect.setToolTip("Hier Können Sie das Startdatum auswählen")
        paramWidget.addWidget(self.StartDateSelect)
        self.StartDateSelect.setMinimumWidth(100)

        self.EndDateSelect = QComboBox()
        self.EndDateSelect.setMaxVisibleItems(50)
        self.EndDateSelect.setToolTip("Hier Können Sie das Endedatum auswählen")
        paramWidget.addWidget(self.EndDateSelect)
        self.EndDateSelect.setMinimumWidth(100)

        saveWidget = QHBoxLayout()
        saveWidget.addStretch()
        self.SaveButton = QPushButton('Save Graph', self)
        self.SaveButton.setToolTip("Name der Datei über Input rechts eingeben (ohne Dataiformat)")
        saveWidget.addWidget(self.SaveButton)
        self.SaveName = QLineEdit()
        saveWidget.addWidget(self.SaveName)
        saveWidget.addStretch()
        TopVLayout.addLayout(saveWidget)
        self.SaveButton.clicked.connect(self.SaveGraph)

        saveExcelWidget = QHBoxLayout()
        saveExcelWidget.addStretch()
        self.SaveExcelButton = QPushButton('Save Excel', self)
        self.SaveExcelButton.setToolTip("Hier Können Sie die Datai als Excel speichern")
        saveExcelWidget.addWidget(self.SaveExcelButton)
        self.SaveExcelName = QLineEdit()
        saveExcelWidget.addWidget(self.SaveExcelName)
        saveExcelWidget.addStretch()
        TopVLayout.addLayout(saveExcelWidget)
        self.SaveExcelButton.clicked.connect(self.SaveExcel)

        paramWidget.addStretch()
        TopVLayout.addLayout(paramWidget)
        TopVLayout.addWidget(self.mplcanvas)

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
        endDate = self.EndDateSelect.currentText()
        ax = self.mplcanvas.ax
        ax.cla()

        if (choice != "" and bundesland != "" and startDate != "" and endDate != ""):
            if (choice == 'M-W-Unbekannt'):
                self.plotFunction(ax, 'M', bundesland, altersgruppe, startDate, endDate)
                self.plotFunction(ax, 'W', bundesland, altersgruppe, startDate, endDate)
                self.plotFunction(ax, 'unbekannt', bundesland, altersgruppe, startDate, endDate)
            elif (choice == "M"):
                self.plotFunction(ax, 'M', bundesland, altersgruppe, startDate, endDate)
            elif (choice == "W"):
                self.plotFunction(ax, 'W', bundesland, altersgruppe, startDate, endDate)
            elif (choice == 'Vergleich Anzahl der Genesen und Neuinfektionen'):
                self.plotFunction(ax, 'AnzahlGenesen', bundesland, altersgruppe, startDate, endDate)
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
        self.AnalyseSelect.addItem('M')
        self.AnalyseSelect.addItem('W')
        self.AnalyseSelect.addItem('Vergleich Anzahl der Genesen und Neuinfektionen')
        self.AnalyseSelect.addItem('Vergleich Todesfälle und Neuinfektionen')

        self.BundeslandSelect.clear()
        for i in bundeslands:
            self.BundeslandSelect.addItem(i)
        self.AltersgruppeSelect.clear()
        for i in altersgruppe:
            self.AltersgruppeSelect.addItem(i)
        self.StartDateSelect.clear()
        for i in dates:
            self.StartDateSelect.addItem(str(i)[0:10])
        self.EndDateSelect.clear()
        for i in range(len(dates)):
            self.EndDateSelect.addItem(str(dates[len(dates) - i - 1])[0:10])

    def SaveGraph(self):  # todo das funktioniert leider nicht
        """
        Save-Button führt zu dieser Funktion.
        Es öffnet sich ein Dialog der das abspeichern nocheinmal hinterfragen soll.
        Funktion Speichervorgang abbrechen leider mehrmals versucht, aber gescheitert.
        param: None
        return: None
        """
        msgbox = QMessageBox()
        msgbox.setText("Die Datai wurde in der gleichen Repository gespeichert")
        msgbox.addButton(QMessageBox.Ok)
        msgbox.exec()
        savetext = self.SaveName.text()
        img = self.mplcanvas
        save = __file__.replace('src\\gui.py', savetext + '.png')
        img.print_figure(save)

    def SaveExcel(self): # todo
        """
        Save-Button führt zu dieser Funktion.
        Es öffnet sich ein Dialog der das abspeichern nocheinmal hinterfragen soll.
        Funktion Speichervorgang abbrechen leider mehrmals versucht, aber gescheitert.
        param: None
        return: None
        """
        analyzer = RKIAnalyzer()
        msgbox = QMessageBox()
        msgbox.setText("Die Datai wurde in der gleichen Repository gespeichert")
        msgbox.addButton(QMessageBox.Ok)
        msgbox.exec()
        savetext = self.SaveExcelName.text()
        print(analyzer.ExcelMaker.newDf)
            # .newDf.to_excel('src\\gui.py', savetext + '.xlsx')


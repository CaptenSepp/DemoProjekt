from PyQt5.QtWidgets import QApplication
import sys

from RKIAnalyzer import RKIAnalyzer
from gui import App

def plotFunction(ax, geschlecht):
    """
    Diese Funktion wird aufgerufen, wenn der Benutzer ein anderes Bundesland wählt oder direkt nach dem Start.
    :param ax: Matplotlib Ax-Objekt. Mit z. b. ax.plot kann gezeichnet werden.
    :param bundesland: Name des ausgewählten Bundeslands
    :return: None

    This function is called when the user selects a different state or immediately after the program start.
     : param ax: Matplotlib Ax object. With z. b. ax.plot can be drawn.
     : param state: Name of the selected state
     : return: None
    """
    data = analyzer.getWeeklyCumulatedDataForBundesland(columnName='AnzahlFall', geschlecht=geschlecht)
    ax.plot(data.index, data, label=geschlecht)
    ax.legend()
    ax.set_title('Fallzahlen')
    ax.grid()

def guiReadyFunction(window):
    """
    Wird aufgerufen, wenn alle Elemente der GUI aufgebaut sind.
    :param window: Verweis auf das GUI-Fenster. Hiermit kann z. B. die Statuszeile verändert werden.
    :return: None

    Is called when all elements of the GUI have been set up.
     : param window: Reference to the GUI window. This z. B. the status line can be changed.
     : return: None
    """
    window.showStatusText("Lese Daten. Bitte warten....", executeEventLoop=True)

    fn = '../daten/RKI_COVID19_short.csv'
    analyzer.loadDataFromFile(fn, filetype='csv')

    window.setGeschlecht(analyzer.getGeschlecht())
    window.showStatusText("Halloooooo")


if __name__ == '__main__':
    analyzer = RKIAnalyzer()

    app = QApplication(sys.argv)
    w = App(plotFunction=plotFunction, guiReadyFunction=guiReadyFunction)

    sys.exit(app.exec_())

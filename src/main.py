from PyQt5.QtWidgets import QApplication
import sys

from RKIAnalyzer import RKIAnalyzer
from gui import App


def plotFunction(ax, geschlecht, nutzerWahl):
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

    if (geschlecht == 'AnzahlFall'):
        data = analyzer.getWeeklyCumulatedDataForAnzahfall(columnName='AnzahlFall')  # maghadire nemudar migire az getWeek... az RKI Analiz
        ax.plot(data.index, data, label=geschlecht)  # plot misaze azash
        data_dead = analyzer.getWeeklyCumulatedDataForAnzahfall(columnName='AnzahlTodesfall')
        ax.plot(data_dead.index, data_dead, label='AnzahlTodesfall')

        # sharedDataBundesland=analyzer.getWeeklyCumulatedDataForAnzahfall(columnName='Bundesland')
        # sharedDataDatum=analyzer.getWeeklyCumulatedDataForAnzahfall(columnName='Bundesland')

        ax.set_title('Tod- und Anzahlfälle')
        ax.legend()
        ax.grid()
    else:
        data = analyzer.getWeeklyCumulatedDataForBundesland(columnName='AnzahlFall', geschlecht=geschlecht)
        ax.plot(data.index, data, label=geschlecht)

        # sharedDataBundesland = analyzer.getWeeklyCumulatedDataForAnzahfall(columnName='Bundesland')
        # sharedDataDatum = analyzer.getWeeklyCumulatedDataForAnzahfall(columnName='Bundesland')

        ax.set_title('Männer/Frauen/Unbekannt')
        ax.legend()
        ax.grid()


# def plotFunctionTodes(ax, geschlecht):
#     """
#     Diese Funktion wird aufgerufen, wenn der Benutzer ein anderes Bundesland wählt oder direkt nach dem Start.
#     :param ax: Matplotlib Ax-Objekt. Mit z. b. ax.plot kann gezeichnet werden.
#     :param bundesland: Name des ausgewählten Bundeslands
#     :return: None
#
#     This function is called when the user selects a different state or immediately after the program start.
#      : param ax: Matplotlib Ax object. With z. b. ax.plot can be drawn.
#      : param state: Name of the selected state
#      : return: None
#     """
#

def guiReadyFunction(window):
    """
    Wird aufgerufen, wenn alle Elemente der GUI aufgebaut sind.
    :param window: Verweis auf das GUI-Fenster. Hiermit kann z. B. die Statuszeile verändert werden.
    :return: None
    """
    window.showStatusText("Lese Daten. Bitte warten....", executeEventLoop=True)

    fn = '../daten/RKI_COVID19_short.csv'  # import etelaat az file
    analyzer.loadDataFromFile(fn, filetype='csv')

    window.setAnalyse(analyzer.getGeschlecht())
    window.showStatusText("Bereit")


if __name__ == '__main__':
    analyzer = RKIAnalyzer()  # todo , IN NEMIDOONAM CHIKAR MIKONE

    app = QApplication(sys.argv)
    w = App(plotFunction=plotFunction, guiReadyFunction=guiReadyFunction)

    # App(plotFunction=plotFunctionAnzahl,guiReadyFunction=guiReadyFunction)  # Starte Mane injas, ke ettelaat mire be Classe App az GUI # todo inja oomadim bokonimesh dota plotfunction
    # App(plotFunction=plotFunctionTodes, guiReadyFunction=guiReadyFunction)
    sys.exit(app.exec_())

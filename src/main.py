from PyQt5.QtWidgets import QApplication
import sys

from RKIAnalyzer import RKIAnalyzer
from gui import App


def plotFunction(ax, choice, bundesland, altersgruppe, startDate, endDate):
    """
    Diese Funktion wird aufgerufen, wenn der Benutzer ein anderes Bundesland, Altersgruppe, Start- und Enddatum wählt um
    diese zu analysieren. Direkt nach dem Start des Programms wird ein Default Setting / eine Vorauswahl angezeigt.

    Prameter: Bundesland, Altersgruppe, Start- und Enddatum
    Analyse: Neuinfizierte im Vergleich zu Todesfällen
             Neuinfizierte im Vergleich zu den Genesenen
             Geschlecht der Infizierten

    :return: None
    """
    if (choice == 'AnzahlFall'):
        dataIll = analyzer.getWeeklySumOfAllData(columnName='AnzahlFall', bundesland=bundesland,
                                                 altersgruppe=altersgruppe, startDate=startDate,
                                                 endDate=endDate)  # maghadire nemudar migire az getWeek... az RKI Analiz
        ax.plot(dataIll.index, dataIll, label=choice)  # plot misaze azash
        dataDead = analyzer.getWeeklySumOfAllData(columnName='AnzahlTodesfall', bundesland=bundesland,
                                                  altersgruppe=altersgruppe,
                                                  startDate=startDate,
                                                  endDate=endDate)
        ax.plot(dataDead.index, dataDead, label='AnzahlTodesfall')
        ax.set_title('Anzahl der Neuinfektionen im Vergleich zu den Todesfällen')
        ax.legend()
        ax.grid()
        # todo genesen und infizierten und ...

    elif (choice == 'AnzahlGenesen'):
        dataGenesen = analyzer.getWeeklySumOfAllDataGenesen(columnName='AnzahlGenesen', bundesland=bundesland,
                                                 altersgruppe=altersgruppe, startDate=startDate,
                                                 endDate=endDate)  # maghadire nemudar migire az getWeek... az RKI Analiz
        ax.plot(dataGenesen.index, dataGenesen, label=choice)  # plot misaze azash
        dataIll= analyzer.getWeeklySumOfAllDataGenesen(columnName='AnzahlFall', bundesland=bundesland,
                                                  altersgruppe=altersgruppe,
                                                  startDate=startDate,
                                                  endDate=endDate)
        ax.plot(dataIll.index, dataIll, label='AnzahlFall')
        ax.set_title('Anzahl der Neuinfektionen im Vergleich zu den Fällen der Genesenen')
        ax.legend()
        ax.grid()

    else:
        dataIll = analyzer.getWeeklySumOfEachSexuality(columnName='AnzahlFall', sexuality=choice,
                                                       bundesland=bundesland, altersgruppe=altersgruppe,
                                                       startDate=startDate,
                                                       endDate=endDate)
        ax.plot(dataIll.index, dataIll, label=choice)
        ax.set_title('Anzahl der Neuinfizierten nach Geschlecht')
        ax.legend()
        ax.grid()

def guiReadyFunction(window):
    """
    Wird aufgerufen, wenn alle Elemente der GUI aufgebaut sind.
    :param window: Verweis auf das GUI-Fenster. Hiermit kann z. B. die Statuszeile verändert werden.
    :return: None
    """
    window.showStatusText("Lese Daten. Bitte warten....", executeEventLoop=True)

    fn = '../daten/RKI_COVID19_pickle.zip'                               # import etelaat az file
    analyzer.loadDataFromFile(fn, filetype='pickle')

    window.ComboBoxSetter(analyzer.getBundesland(), analyzer.getAltersgruppe(), analyzer.getDate())
    window.showStatusText("Bereit")


if __name__ == '__main__':
    analyzer = RKIAnalyzer()

    app = QApplication(sys.argv)
    w = App(plotFunction=plotFunction, guiReadyFunction=guiReadyFunction)
    sys.exit(app.exec_())

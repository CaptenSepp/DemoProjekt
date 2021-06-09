from PyQt5.QtWidgets import QApplication
import sys

from RKIAnalyzer import RKIAnalyzer
from gui import App

def plotFunction(ax, bundesland):
    data = analyzer.getWeeklyCumulatedDataForBundesland(columnName='AnzahlFall', bundesland=bundesland)
    ax.plot(data.index, data, label=bundesland)
    ax.legend()
    ax.set_title('Fallzahlen')
    ax.grid()

def guiReadyFunction(window):
    window.showStatusText("Lese Daten. Bitte warten....", executeEventLoop=True)

    fn = '../daten/RKI_COVID19_pickle.zip'
    analyzer.loadDataFromFile(fn, filetype='pickle')
    window.setBundeslaender(analyzer.getBundeslaender())
    window.showStatusText("Bereit")


if __name__ == '__main__':
    analyzer = RKIAnalyzer()

    app = QApplication(sys.argv)
    w = App(plotFunction=plotFunction, guiReadyFunction=guiReadyFunction)

    sys.exit(app.exec_())

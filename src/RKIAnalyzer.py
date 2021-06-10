import pandas as pd
import datetime as dt

class RKIAnalyzer:
    def __init__(self):
        data = pd.DataFrame()
        pass

    def loadDataFromFile(self, filename, filetype='pickle'):
        """
        Lädt die Daten des RKI von der Festplatte. Diese können als pickle-Datei (lädt sehr schnell) und csv-Datei
        vorliegen. Letztere ist das Format, welches auch vom RKI geliefert wird. Beide Dateien können als ZIP gepackt
        werden.
        :param filename: Pfad zu den Daten (.pickle, .csv, .zip)
        :param filetype: Typ der Datei (pickle/csv)
        :return: None
        """
        if filetype == 'pickle':
            self.data = pd.read_pickle(filename)
        elif filetype == 'csv':
            self.data = pd.read_csv(filename, parse_dates=['Meldedatum', 'Refdatum'], index_col='Refdatum')
        else:
            raise NotImplementedError()

    def getBundeslaender(self):
        """
        Ermittelt aus dem Datensatz eine Liste der aufgeführten Bundesländer.
        :return: Liste der Bundesländer als Datentyp "set"
        """
        result = self.data.Bundesland.unique()

        return set( result )

    def getWeeklyCumulatedDataForBundesland(self, columnName, bundesland):
        """
        Ermittelt aus dem Datensatz wöchentlich gruppiert und aufsummiert die Zahlen einer Spalte.
        Wenn <columnName> z. B. "AnzahlFall" ist, dann werden die aufsummierten (Kumulierten) Gesamtinfektionen pro Bundesland
        und pro Woche zurückgegeben.

        Beispiel:
            Woche 1: 10 Fälle
            Woche 2: 5 Fälle
            Woche 3: 15 Fälle
            Kumuliert ist das dann
            Woche 1: 10 Fälle
            Woche 2: 15 Fälle
            Woche 3: 30 Fälle

        :param columnName: Name der Spalte
        :param bundesland: Name des Bundeslands
        :return: pd.Series mit dem Wochenstart-Datum als Index und den Kumulierten Werten.
        """
        df = self.data[self.data.Bundesland == bundesland]
        col = df[columnName]
        col = col.resample('w').agg({columnName:'sum'})
        col = col.droplevel(0)
        return col.cumsum()


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

        Loads the RKI data from the hard drive. These can be available as pickle files (loads very quickly) and csv files.
        The latest is the format that is also supplied by the RKI. Both files can be packed as a ZIP
         become.
         : param filename: Path to the data (.pickle, .csv, .zip)
         : param filetype: type of file (pickle / csv)
         : return: None
        """
        if filetype == 'pickle':
            self.data = pd.read_pickle(filename)
        elif filetype == 'csv':
            self.data = pd.read_csv(filename, parse_dates=['Meldedatum', 'Refdatum'], index_col='Refdatum')
        else:
            raise NotImplementedError()

    def getGeschlecht(self):
        """
        Ermittelt aus dem Datensatz eine Liste der aufgeführten Geschlecht, Bundesländer und Datum.
        :return: Liste der Bundesländer als Datentyp "set"
        """
        result = self.data.Geschlecht.unique()
        return set(result)

    def getBundesland(self):
        result = self.data.Bundesland.unique()
        return set(result)

    def getDate(self):
        result = []
        dates = self.data.Meldedatum.unique()
        for i in range(len(dates)):
            j = str(dates[i])[0:7]
            result.append(j)
        result.sort() # todo chikar konim in lanati in order beshe???
        return set(result)

    def getWeeklySumOfEachSexuality(self, columnName, sexualityTarget):
        """
        Ermittelt aus dem Datensatz wöchentlich gruppiert und aufsummiert die Zahlen einer Spalte.
        Wenn <columnName> z. B. "AnzahlFall" ist, dann werden die aufsummierten (Kumulierten) Gesamtinfektionen pro Bundesland
        und pro Woche zurückgegeben.

        :param columnName: Name der Spalte
        :param bundesland: Name des Bundeslands
        :return: pd.Series mit dem Wochenstart-Datum als Index und den Kumulierten Werten.

        """
        df = self.data[self.data.Geschlecht == sexualityTarget]  # matrisi az hame zan ha ya ...
        col = df[columnName]  # teedade mariza dar yek sotun
        col = col.resample('w').agg({columnName: 'sum'})  # majmooee hame aadade sotun
        col = col.droplevel(0)
        return col.cumsum()

    def getWeeklySumOfAllData(self, columnName):
        """
        Diese Funktion unterscheidet die Zahlen von Tote mit Infizierte Personen.

        :param columnName: Name der Spalte
        :param bundesland: Name des Bundeslands
        :return: pd.Series mit dem Wochenstart-Datum als Index und den Kumulierten Werten.
        """
        df = self.data  # matrisi az hame zan ha ya ...
        col = df[columnName]  # teedade mariza dar yek sotun
        col = col.resample('M').agg({columnName: 'sum'})  # majmooee hame aadade sotun
        col = col.droplevel(0)
        return col.cumsum()

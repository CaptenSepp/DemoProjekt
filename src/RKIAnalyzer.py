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
        Ermittelt aus dem Datensatz eine Liste der aufgeführten Bundesländer.
        :return: Liste der Bundesländer als Datentyp "set"

        Determines a list of the federal states listed from the data set.
         : return: List of federal states as data type "set"
        """
        result = self.data.Geschlecht.unique()

        return set( result )

    def getWeeklyCumulatedDataForBundesland(self, columnName, geschlecht):
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



        Determines from the data set, grouped weekly and adds up the numbers in a column.
        For example, if <columnName> is "NumberCases", then the total (cumulative) total infections per state and per week are returned.

         Example:
             Week 1: 10 cases
             Week 2: 5 cases
             Week 3: 15 cases
             That is then cumulative
             Week 1: 10 cases
             Week 2: 15 cases
             Week 3: 30 cases

         : param columnName: name of the column
         : param state: Name of the state
         : return: pd.Series with the week start date as index and the cumulative values.
        """
        df = self.data[self.data.Geschlecht == geschlecht] # matrisi az hame zan ha ya ...
        col = df[columnName] # teedade mariza dar yek sotun
        col = col.resample('w').agg({columnName:'sum'}) # majmooee hame aadade sotun
        col = col.droplevel(0)
        return col.cumsum()

    def getWeeklyCumulatedDataForBundesland(self, columnName, geschlecht):
        """
        Diese Funktion unterscheidet die Zahlen von Tote mit Infizierte Personen.


        :param columnName: Name der Spalte
        :param bundesland: Name des Bundeslands
        :return: pd.Series mit dem Wochenstart-Datum als Index und den Kumulierten Werten.

        """
        df = self.data[self.data.Geschlecht == geschlecht] # matrisi az hame zan ha ya ...
        col = df[columnName] # teedade mariza dar yek sotun
        col = col.resample('w').agg({columnName:'sum'}) # majmooee hame aadade sotun
        col = col.droplevel(0)
        return col.cumsum()

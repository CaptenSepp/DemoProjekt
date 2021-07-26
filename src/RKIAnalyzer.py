import pandas as pd



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
        if filetype == 'pickle':  # todo muss hier unbedings pickle sein
            self.data = pd.read_pickle(filename)
        elif filetype == 'csv':
            self.data = pd.read_csv(filename, parse_dates=['Meldedatum', 'Refdatum'], index_col='Refdatum')
        else:
            raise NotImplementedError()

    def getGeschlecht(self):
        """
        Ermittelt aus dem Datensatz eine Liste aller aufgeführten Geschlechter.
        :return: Liste der Geschlechter als Datentyp "set"
        """
        result = self.data.Geschlecht.unique()
        return set(result)

    def getBundesland(self):
        """
        Ermittelt aus dem Datensatz eine Liste aller aufgeführten Bundesländer.
        :return: Liste der Bundesländer als Datentyp "List"
        """
        result = self.data.Bundesland.unique()
        result = set(result)
        return sorted(result)

    def getAltersgruppe(self):
        """
        Ermittelt aus dem Datensatz eine Liste aller aufgeführten Altersgruppen.
        :return: Liste der Altersgruppen als Datentyp "List"
        """
        result = self.data.Altersgruppe.unique()
        result = set(result)
        return sorted(result)

    def getDate(self):
        """
        Ermittelt aus dem Datensatz eine Liste aller aufgeführten Meldedaten.
        :return: Liste der Daten als Meldedaten "List"
        """
        result = []
        dates = self.data['Meldedatum'].unique()
        for i in range(len(dates)):
            j = (dates[i])
            result.append(j)
        result = set(result)
        return sorted(result)

    def getWeeklySumOfEachSexuality(self, columnName, sexuality, bundesland, altersgruppe, startDate, endDate):
        """
        Ermittelt aus dem Datensatz wöchentlich gruppiert und aufsummiert die Zahlen einer Spalte.
        Wenn <columnName> z. B. "AnzahlFall" ist, dann werden die aufsummierten Gesamtinfektionen pro Bundesland
        und pro Woche zurückgegeben.

        :param columnName: Name der Spalte
        :param bundesland: Name des Bundeslands, altersgrupper, Startdatum, Enddatum und Geschlechts
        :return: pd.Series mit dem Wochenstart-Datum als Index und den Kumulierten Werten.
        """
        self.ExcelMaker(bundesland, altersgruppe, startDate, endDate) # todo
        df = self.data[self.data.Geschlecht == sexuality]  # matrisi az hame zan ha ya ...
        df = df[df.Bundesland == bundesland]
        df = df[df.Altersgruppe == altersgruppe]

        # Hier wird der gewünschte Zeitraum aus der Liste ausgelesen
        newDf = df.loc[(df["Meldedatum"] >= startDate) & (df["Meldedatum"] <= endDate)]
        col = newDf[columnName]

        col = col.resample('w').agg({columnName: 'sum'})  # majmooee hame aadade sotun
        col = col.droplevel(0)
        return col.cumsum()

    def getWeeklySumOfAllData(self, columnName, bundesland, altersgruppe, startDate, endDate):
        """
        Diese Funktion liest die Zahlen von toten und infizierten Personen aus.

        :param columnName: Name der Spalte
        :param bundesland: Name des Bundeslands, altersgrupper, Startdatum, Enddatum
        :return: pd.Series mit dem Wochenstart-Datum als Index und den Kumulierten Werten.
        """
        self.ExcelMaker(bundesland, altersgruppe, startDate, endDate) # todo
        df = self.data[self.data.Bundesland == bundesland]  # matrisi az hame zan ha ya ...
        df = df[df.Altersgruppe == altersgruppe]
        newDf = df.loc[(df["Meldedatum"] >= startDate) & (df["Meldedatum"] <= endDate)]
        col = newDf[columnName]  # teedade mariza dar yek sotun
        col = col.resample('w').agg({columnName: 'sum'})  # majmooee hame aadade sotun
        col = col.droplevel(0)
        return col.cumsum()

    def getWeeklySumOfAllDataGenesen(self, columnName, bundesland, altersgruppe, startDate, endDate):
        """
        Diese Funktion liest die Zahlen von genesenen und infizierten Personen aus.

        :param columnName: Name der Spalte
        :param bundesland: Name des Bundeslands, Altersgruppen, Startdatum, Enddatum
        :return: pd.Series mit dem Wochenstart-Datum als Index und den kumulierten Werten.
        """
        self.ExcelMaker(bundesland, altersgruppe, startDate, endDate) # todo
        df = self.data[self.data.Bundesland == bundesland]  # matrisi az hame zan ha ya ...
        df = df[df.Altersgruppe == altersgruppe]
        newDf = df.loc[(df["Meldedatum"] >= startDate) & (df["Meldedatum"] <= endDate)]
        col = newDf[columnName]  # teedade mariza dar yek sotun
        col = col.resample('w').agg({columnName: 'sum'})  # majmooee hame aadade sotun
        col = col.droplevel(0)
        return col.cumsum()

    def ExcelMaker(self, sexuality, bundesland, altersgruppe, startDate, endDate): # todo
        """
        Nach jeder Analyse wird diese Funktion durchgefört und die Ergebnisse als pd.Series gespeichert.

        :param columnName: Name der Spalte
        :param bundesland: Name des Bundeslands, Altersgruppen, Startdatum, Enddatum und Geschlecht
        :return: pd.Series mit dem Wochenstart-Datum als Index und den kumulierten Werten.
        """
        df = self.data[self.data.Geschlecht == sexuality]  # matrisi az hame zan ha ya ...
        df = df[df.Bundesland == bundesland]
        df = df[df.Altersgruppe == altersgruppe]
        newDf = df.loc[(df["Meldedatum"] >= startDate) & (df["Meldedatum"] <= endDate)]
        return newDf


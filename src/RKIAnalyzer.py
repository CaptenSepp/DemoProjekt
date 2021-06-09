import pandas as pd
import datetime as dt

class RKIAnalyzer:
    def __init__(self):
        data = pd.DataFrame()
        pass

    def loadDataFromFile(self, filename, filetype='pickle'):
        if filetype == 'pickle':
            self.data = pd.read_pickle(filename)
        elif filetype == 'csv':
            self.data = pd.read_csv(filename, parse_dates=['Meldedatum', 'Refdatum'], index_col='Refdatum')
        else:
            raise NotImplementedError()

    def getBundeslaender(self):
        result = self.data.Bundesland.unique()

        return set( result )

    def getWeeklyCumulatedDataForBundesland(self, columnName, bundesland):
        df = self.data[self.data.Bundesland == bundesland]
        col = df[columnName]
        col = col.resample('w').agg({columnName:'sum'})
        col = col.droplevel(0)
        return col.cumsum()


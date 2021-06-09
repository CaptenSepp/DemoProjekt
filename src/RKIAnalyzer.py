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

    def getWeeklyCumulatedDataForBundesland(self, rowname, bundesland):
        df = self.data[self.data.Bundesland == bundesland]
        df = df.resample('w').agg({rowname:lambda x: x.sum()})
        df = df.cumsum()
        return df[rowname]


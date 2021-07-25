import os
import unittest
from unittest.mock import call
from unittest.mock import MagicMock
from io import StringIO
from src.RKIAnalyzer import RKIAnalyzer
import datetime as dt
import tempfile

import pandas as pd


class testRKIData(unittest.TestCase):
    def setUp(self) -> None:
        datastr = """
            FID,IdBundesland,Bundesland,Landkreis,Altersgruppe,Geschlecht,AnzahlFall,AnzahlTodesfall,Meldedatum,IdLandkreis,Datenstand,NeuerFall,NeuerTodesfall,Refdatum,NeuGenesen,AnzahlGenesen,IstErkrankungsbeginn,Altersgruppe2
            995033,8,Baden-Württemberg,LK Karlsruhe,A60-A79,W,1,0,2020/11/02 00:00:00,8215,"31.05.2021, 00:00 Uhr",0,-9,2020/10/28 00:00:00,0,1,1,Nicht übermittelt
            1520840,9,Bayern,LK Ostallgäu,A60-A79,W,1,0,2020/12/22 00:00:00,9777,"31.05.2021, 00:00 Uhr",0,-9,2020/12/15 00:00:00,0,1,1,Nicht übermittelt
            981853,8,Baden-Württemberg,SK Karlsruhe,A15-A34,M,1,0,2020/11/29 00:00:00,8212,"31.05.2021, 00:00 Uhr",0,-9,2020/11/27 00:00:00,0,1,1,Nicht übermittelt
            1692033,12,Brandenburg,LK Oberhavel,A80+,W,1,1,2021/03/29 00:00:00,12065,"31.05.2021, 00:00 Uhr",0,0,2021/03/29 00:00:00,-9,0,0,Nicht übermittelt
            47782,2,Hamburg,SK Hamburg,A00-A04,W,2,0,2020/11/12 00:00:00,2000,"31.05.2021, 00:00 Uhr",0,-9,2020/10/30 00:00:00,0,2,1,Nicht übermittelt
            1624379,11,Berlin,SK Berlin Neukölln,A80+,W,5,0,2021/01/25 00:00:00,11008,"31.05.2021, 00:00 Uhr",0,-9,2021/01/25 00:00:00,0,5,0,Nicht übermittelt
            1657540,12,Brandenburg,SK Potsdam,A15-A34,W,1,0,2020/04/03 00:00:00,12054,"31.05.2021, 00:00 Uhr",0,-9,2020/03/24 00:00:00,0,1,1,Nicht übermittelt
            1465112,9,Bayern,LK Kitzingen,A35-A59,M,1,0,2021/04/28 00:00:00,9675,"31.05.2021, 00:00 Uhr",0,-9,2021/04/21 00:00:00,0,1,1,Nicht übermittelt
            1183331,9,Bayern,SK München,A35-A59,W,1,0,2020/11/15 00:00:00,9162,"31.05.2021, 00:00 Uhr",0,-9,2020/11/13 00:00:00,0,1,1,Nicht übermittelt
            226722,3,Niedersachsen,LK Vechta,A35-A59,W,1,1,2020/12/22 00:00:00,3460,"31.05.2021, 00:00 Uhr",0,0,2020/12/22 00:00:00,-9,0,0,Nicht übermittelt
            1100715,8,Baden-Württemberg,LK Konstanz,A35-A59,M,3,0,2021/02/21 00:00:00,8335,"31.05.2021, 00:00 Uhr",0,-9,2021/02/21 00:00:00,0,3,0,Nicht übermittelt
            1199762,9,Bayern,LK Berchtesgadener Land,A15-A34,M,1,0,2020/05/05 00:00:00,9172,"31.05.2021, 00:00 Uhr",0,-9,2020/05/05 00:00:00,0,1,0,Nicht übermittelt
            353467,5,Nordrhein-Westfalen,SK Bonn,A05-A14,W,1,0,2021/04/15 00:00:00,5314,"31.05.2021, 00:00 Uhr",0,-9,2021/04/10 00:00:00,0,1,1,Nicht übermittelt
            612735,5,Nordrhein-Westfalen,LK Märkischer Kreis,A60-A79,W,1,1,2021/02/17 00:00:00,5962,"31.05.2021, 00:00 Uhr",0,0,2021/02/16 00:00:00,-9,0,1,Nicht übermittelt
            791307,7,Rheinland-Pfalz,SK Koblenz,A60-A79,W,3,0,2021/03/25 00:00:00,7111,"31.05.2021, 00:00 Uhr",0,-9,2021/03/25 00:00:00,0,3,0,Nicht übermittelt
            66855,2,Hamburg,SK Hamburg,A35-A59,W,6,0,2021/02/25 00:00:00,2000,"31.05.2021, 00:00 Uhr",0,-9,2021/02/22 00:00:00,0,6,1,Nicht übermittelt
            1809841,14,Sachsen,SK Dresden,A80+,M,1,0,2021/02/06 00:00:00,14612,"31.05.2021, 00:00 Uhr",0,-9,2021/02/05 00:00:00,0,1,1,Nicht übermittelt
            1296364,9,Bayern,LK Landshut,A15-A34,M,1,0,2021/03/25 00:00:00,9274,"31.05.2021, 00:00 Uhr",0,-9,2021/03/17 00:00:00,0,1,1,Nicht übermittelt
            1424617,9,Bayern,LK Erlangen-Höchstadt,A35-A59,W,1,0,2020/10/15 00:00:00,9572,"31.05.2021, 00:00 Uhr",0,-9,2020/10/13 00:00:00,0,1,1,Nicht übermittelt
        """
        self.datastream = StringIO(datastr)

    def testBundeslaender(self):
        mut = RKIAnalyzer()
        mut.loadDataFromFile(self.datastream, filetype='csv')
        result = mut.getBundesland()
        expected = {'Niedersachsen', 'Bayern', 'Hamburg', 'Brandenburg', 'Nordrhein-Westfalen', 'Rheinland-Pfalz',
                    'Sachsen', 'Berlin', 'Baden-Württemberg'}

        self.assertSetEqual(result, expected)

    def testGeschlecht(self):
        mut = RKIAnalyzer()
        mut.loadDataFromFile(self.datastream, filetype='csv')
        result = mut.getGeschlecht()
        expected = {'M', 'W'}
        # expected = {'M', 'W', 'unbekannt'} # todo what about unbekannt??, it doesn't find it in the first Bundesland and time, so Error i guess
        self.assertSetEqual(result, expected)

    def testDate(self):
        mut = RKIAnalyzer()
        mut.loadDataFromFile(self.datastream, filetype='csv')
        result = mut.getDate()
        expected = {}

        self.assertSetEqual(result, expected)

    def testWeeklySumOfEachSexuality(self):
        mut = RKIAnalyzer()
        columnName = 'AnzahlFall'
        sexuality = 'W'
        bundesland = 'Hamburg'
        altersgruppe = 'A35-A59'
        startDate = '2020/11/02 00:00:00'
        endDate = '2021/02/25 00:00:00'

        mut.loadDataFromFile(self.datastream, filetype='csv')
        result = mut.getWeeklySumOfEachSexuality(columnName, sexuality, bundesland, altersgruppe, startDate, endDate)
        result = result.values.tolist()
        expected = [6]                                                     # die Summe bleibt gleich bis zum letze Woche

        self.assertEqual(result, expected)

    def testBundeslaender(self):
        mut = RKIAnalyzer()
        mut.loadDataFromFile(self.datastream, filetype='csv')
        result = mut.getBundesland()
        expected = {'Niedersachsen', 'Bayern', 'Hamburg', 'Brandenburg', 'Nordrhein-Westfalen', 'Rheinland-Pfalz',
                    'Sachsen', 'Berlin', 'Baden-Württemberg'}

        self.assertSetEqual(result, expected)


class testFileTypes(unittest.TestCase):
    def testUnknown(self):
        mut = RKIAnalyzer()
        with self.assertRaises(NotImplementedError):
            mut.loadDataFromFile('doesnotexistfile.data', filetype='xxx')


class testReadPickle(unittest.TestCase):
    def setUp(self) -> None:
        datastr = """
            FID,IdBundesland,Bundesland,Landkreis,Altersgruppe,Geschlecht,AnzahlFall,AnzahlTodesfall,Meldedatum,IdLandkreis,Datenstand,NeuerFall,NeuerTodesfall,Refdatum,NeuGenesen,AnzahlGenesen,IstErkrankungsbeginn,Altersgruppe2
            995033,8,Baden-Württemberg,LK Karlsruhe,A60-A79,W,1,0,2020/11/02 00:00:00,8215,"31.05.2021, 00:00 Uhr",0,-9,2020/10/28 00:00:00,0,1,1,Nicht übermittelt
            1520840,9,Bayern,LK Ostallgäu,A60-A79,W,1,0,2020/12/22 00:00:00,9777,"31.05.2021, 00:00 Uhr",0,-9,2020/12/15 00:00:00,0,1,1,Nicht übermittelt
        """
        datastream = StringIO(datastr)
        dataframe = pd.read_csv(datastream, parse_dates=['Meldedatum', 'Refdatum'], index_col='Refdatum')

        self.tempdir = tempfile.TemporaryDirectory()
        dirname = self.tempdir.name
        self.fn = os.path.join(dirname, 'data.pickle')
        dataframe.to_pickle(self.fn)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def testLoad(self):
        mut = RKIAnalyzer()
        mut.loadDataFromFile(self.fn, filetype='pickle')
        result = mut.getBundesland()
        expected = {'Baden-Württemberg', 'Bayern'}
        self.assertSetEqual(expected, result)


class testBerechnungen(unittest.TestCase):
    def testGetCummulated_FallZahlen(self):
        data = [
            "FID,IdBundesland,Bundesland,Landkreis,Altersgruppe,Geschlecht,AnzahlFall,AnzahlTodesfall,Meldedatum,IdLandkreis,Datenstand,NeuerFall,NeuerTodesfall,Refdatum,NeuGenesen,AnzahlGenesen,IstErkrankungsbeginn,Altersgruppe2"]
        rowtmpl = '995033,8,{Bundesland},LK Karlsruhe,A60-A79,W,{AnzahlFall},{AnzahlTodesfall},2020/01/01 00:00:00,8215,"31.05.2021, 00:00 Uhr",0,-9,{Refdatum},0,1,1,Nicht übermittelt'.format
        for tag in range(14):
            startdate = dt.datetime.strptime('2021/05/03 00:00:00', '%Y/%m/%d %H:%M:%S')
            rowdate = startdate + dt.timedelta(days=tag)
            rowdatestr = rowdate.strftime('%Y/%m/%d %H:%M:%S')
            row = rowtmpl(Bundesland='xx', Refdatum=rowdatestr, AnzahlFall=tag, AnzahlTodesfall=0)
            data.append(row)

        datastream = StringIO('\n'.join(data))
        mut = RKIAnalyzer()
        mut.loadDataFromFile(datastream, filetype='csv')
        result = mut.getWeeklySumOfEachSexuality(columnName='AnzahlFall', bundesland='xx')
        expected = pd.Series([sum(range(7)), sum(range(14))],
                             index=pd.date_range(start='2021/05/03 00:00:00', freq='w', periods=2))
        expected.index.name = 'Refdatum'
        expected.name = 'AnzahlFall'

        pd.testing.assert_series_equal(expected, result)

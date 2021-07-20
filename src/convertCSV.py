import pandas as pd

fnin = '../daten/RKI_COVID19_short.zip'
fnout = '../daten/RKI_COVID19_pickle.zip'

chunks = pd.read_csv(fnin, parse_dates=['Meldedatum', 'Refdatum'], index_col='Refdatum', chunksize=10000, iterator=True)
chunklist = []
rowcounter = 0
for chunk in chunks:
    rowcounter += len(chunk)
    print("Read {:10d} rows".format(rowcounter))
    chunklist.append(chunk)

data = pd.concat(chunklist)
data.to_pickle(fnout)


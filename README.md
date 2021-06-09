Demo-Implementierung für das Programmierprojekt des Kurses
Programmieren 1 im Sommersemester 2021


Installation der nötigen Pakete
=

Im Hauptverzeichnis `pip install -r requirements.txt` ausführen.


Coverage-Analyse
=
Im Hauptverzeichnis ausführen:
- `coverage run --source src -m unittest`
- `coverage report`

Der letzte Befehl erzeugt einen kleinen Textreport:
```
Name                 Stmts   Miss  Cover
----------------------------------------
src\RKIAnalyzer.py      20      0   100%
src\__init__.py          0      0   100%
src\convertCSV.py       12     12     0%
src\gui.py              58     58     0%
src\main.py             21     21     0%
----------------------------------------
TOTAL                  111     91    18%
```

Hier zu sehen, dass die Datei mit der Programmlogik `RKIAnalyzer.py` zu 100% durch die Tests abgedeckt ist.
`gui.py` und `main.py` werden gar nicht getestet. Solange dort keine Verarbeitung der RKI-Daten stattfindet, ist
das völlig i.O.


Mit dem Befehl `coverage html` können Sie statt einem Textreport einen HTML-Report
erzeugen, bei dem Sie dann auch sehen können, welche Quelltextzeilen noch nicht 
abgetestet wurden.

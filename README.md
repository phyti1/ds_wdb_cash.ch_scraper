# wdb_mc2

## Quickstart

Folgende Komponente sind Voraussetzung für das lauffähige System:

- Chrome Browser (Version 107.0.5304.107)
- Python 3.9 Installation

Um das Pipenv Environment zu erstellen, muss folgender Befehl ausgeführt werden:

```
pipenv install
```

Die Version des Chrome Browsers ist im Chrome unter "...", "Hilfe", "Über Google Chrome" zu finden.

Ist Chrome in einer anderen Version installiert, muss eine Paketversion folgendermassen geändert werden:

```
pipenv uninstall chromedriver-binary
pipenv install chromedriver-binary==neueVersion
```

Die Daten sind bereits geladen und liegen unter: ```src/data/cash_news.csv```.
Um die Daten neu zu laden, muss diese Datei vor Ausführung gelöscht werden.

Um das Programm zu starten, muss folgender Befehl ausgeführt werden:

```
pipenv run python ./src/frontend.py
```

Um die Tests auszuführen, muss folgender Befehl ausgeführt werden:

```
pipenv run python ./tests/test.py
```

#### Branching System

In diesem Projekt arbeiten wir mit dem "Gitflow Workflow". Dabei wird pro Feature lokal ein Feature-Branch erstellt, nach Beedigung lokal mit dem "dev" Branch gemerged und nach "origin/dev" gepusht. 
Für die Auslieferung der Software müssen gemäss Kapitel "Test" alle Tests erflogreich durchlaufen werden. Erst dann darf der Fortschritt in den "main" Branch gemerged werden. Als Tag wird der Versionscode im Branch "main" gekenntzeichnet.

Weitere Informationen: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow

## Report

Sie finden unseren Bericht in ```./docs/report.md```.

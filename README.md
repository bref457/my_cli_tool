# my_cli_tool

Ein einfaches Kommandozeilen-Tool zur Dateiverwaltung.

## Funktionen

*   **Verzeichnis auflisten:** Zeigt den Inhalt des aktuellen Verzeichnisses an.
*   **Ordner erstellen:** Erstellt neue Verzeichnisse.
*   **Leere Datei erstellen:** Erstellt neue, leere Dateien.

## Installation und Nutzung

1.  Klone das Repository:
    ```bash
    git clone https://github.com/bref457/my_cli_tool.git
    ```
2.  Navigiere in das Projektverzeichnis:
    ```bash
    cd my_cli_tool
    ```
3.  Führe das Tool aus (Beispiele):
    ```bash
    python main.py list
    python main.py create_folder my_new_folder
    python main.py create_file my_new_file.txt
    ```

## Warum dieses Tool?

Dieses `my_cli_tool` dient als praktisches Lernprojekt, um die Grundlagen der Kommandozeilen-Tool-Entwicklung in Python zu verstehen. Während viele der Funktionen auch direkt über die Standardbefehle deines Betriebssystems im Terminal verfügbar sind, bietet dieses Tool eine Plattform für:

*   **Lernen und Experimentieren:** Verstehen, wie CLI-Anwendungen aufgebaut sind und mit dem Dateisystem interagieren.
*   **Plattformübergreifende Konsistenz:** Potenzial für einheitliche Befehle über verschiedene Betriebssysteme hinweg.
*   **Anpassung und Automatisierung:** Die Möglichkeit, maßgeschneiderte Funktionen für spezifische Aufgaben zu entwickeln und komplexe Arbeitsabläufe zu automatisieren, die über Standardbefehle hinausgehen.

Es ist nicht primär dazu gedacht, bestehende Terminalbefehle zu ersetzen, sondern als Basis für die Entwicklung spezialisierterer und automatisierter Dateiverwaltungsaufgaben.

## Geplante Funktionen

*   Dateien/Ordner löschen
*   Dateien/Ordner umbenennen/verschieben
*   Dateiinhalte anzeigen
*   Dateien suchen
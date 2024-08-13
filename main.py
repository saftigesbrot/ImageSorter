import os
import exifread
from datetime import datetime
import json
import shutil
from colorama import *
init(autoreset=True)

# Legt alle benötigiten Formate fest
fileformat = [".png", ".jpg", ".jpeg", ".gif", ".tiff", ".svg", ".mp4", ".mov", ".PNG", ".JPG", ".JPEG", ".GIF", ".TIFF", ".SVG", ".MP4", ".MOV",]
new_time_format = "%Y:%m:%d %H:%M:%S"
months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
json_log = {}

# Gibt entsprechende Formate an den Nutzer weiter und fragt nach dem zu sortierendem Ordner
print("\nDer ImageSorter ist bereit. Ich übernehme folgenden Konfigurationen:")
print("\nDateiformate:" + str(fileformat))
print("Zeitformat:" + new_time_format)
print("Monate:" + str(months))

# Fragt nach dem Ordnerlink und überprüft diesen auf seine Richtigkeit
print("\nBitte gebe deinen Pfad an (Beispiel: C:/Users/Marius/Documents/Python/ImageSorter/Freunde):")
path = input()
log_path = path + "/Log & Errors/log.json"

# Lädt alle Dateien in die files Liste
files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]

# Arbeitet für jede Datei einzeln
for x in files:

    # Trennt Dateiname und Dateiformat
    file_name, file_extension = os.path.splitext(x)

    # Prüft, ob es sich um ein Bild oder ein Video handelt, das akzeptiert wird.
    if file_extension in fileformat:
        # Legt den Pfad zur Datei fest
        image_path = "{}/{}".format(path, x)
        
        # Öffnet die Exifread Daten der Datei 
        with open(image_path, 'rb') as image_file:
            tags = exifread.process_file(image_file)

        # Sucht nach dem Aufnahmedatum (Nicht dem Erstelldatum!) und extrahiert dieses
        if 'Image DateTime' in tags:
            date_taken = tags['Image DateTime']
            date_taken_str = str(date_taken)

            # Vollständiges Datum im datetime Zeit Format (z. B. 2020-01-31 14:23:48)
            date_taken_new_time = datetime.strptime(date_taken_str, new_time_format)
            
            # Extrahiert das Aufnahmejahr (z. B. 2020)
            date_taken_str_new_time_year = str(date_taken_new_time.year)
            
            # Extrahiert den Aufnahmemonat (-1 weil bei 0 begonnen wird, z. B. "0" = Januar)
            date_taken_new_time_month = date_taken_new_time.month - 1
            
            # Extrahiert den Aufnahmemonat ausgeschrieben (z. B. "Januar")
            date_taken_str_new_time_month = months[date_taken_new_time_month]

            # Überprüft, ob bereits ein Ordner mit dem jeweiligen Jahr existiert (Sonst wird ein entsprechender Ordner erstellt, z. B. "2020")
            if not os.path.isdir(os.path.join(path, date_taken_str_new_time_year)): 
                os.makedirs(os.path.join(path, date_taken_str_new_time_year)) 

            # Überprüft, ob bereits ein Ordner mit dem jeweiligen Monat existiert (Sonst wird ein entsprechender Ordner erstellt, z. B. "1 Januar")
            monthnumber = str(date_taken_new_time_month + 1) + " " + date_taken_str_new_time_month
            monthpath= path + "/" + date_taken_str_new_time_year
            if not os.path.isdir(os.path.join(monthpath, monthnumber)): 
                os.makedirs(os.path.join(monthpath, monthnumber)) 

            # Erstellt auf grundlage des Erstelldatums einen Pfad und verschiebt die jeweilige Datei dorthin
            new_image_path = path + "/" + date_taken_str_new_time_year + "/" + monthnumber
            shutil.move(image_path, os.path.join(new_image_path, x))

            # Erstellt einen Log Eintrag, wohin die jeweilige Datei verschoben wurde
            json_log.update({"AUFNAHMEDATUM " + x: "Endung (Extension): " + file_extension + " || Verschoben in Ordner: " + date_taken_str_new_time_year + "/" + date_taken_str_new_time_month})
            
        # Falls keine Exifread vorhanden ist, wird das letzte Änderungsdatum verwendet, um zu sortieren
        else:

            # Vollständiges Datum UTC Format
            timestamp = os.stat(image_path).st_mtime

            # Vollständiges Datum im datetime Zeit Format (z. B. 2020-01-31 14:23:48)
            date = datetime.fromtimestamp(timestamp)

            # Extrahiert das Aufnahmejahr (z. B. 2020)
            date_str_year = str(date.year)

            # Extrahiert den Aufnahmemonat (-1 weil bei 0 begonnen wird, z. B. "0" = Januar)
            date_month = date.month - 1

            # Extrahiert den Aufnahmemonat ausgeschrieben (z. B. "Januar")
            date_str_month = months[date_month]

            # Überprüft, ob bereits ein Ordner mit dem jeweiligen Jahr existiert (Sonst wird ein entsprechender Ordner erstellt, z. B. "2020")
            if not os.path.isdir(os.path.join(path, date_str_year)): 
                os.makedirs(os.path.join(path, date_str_year))

            # Überprüft, ob bereits ein Ordner mit dem jeweiligen Monat existiert (Sonst wird ein entsprechender Ordner erstellt, z. B. "1 Januar")
            monthnumber = str(date_month + 1) + " " + date_str_month
            monthpath= path + "/" + date_str_year
            if not os.path.isdir(os.path.join(monthpath, monthnumber)): 
                os.makedirs(os.path.join(monthpath, monthnumber))

            # Erstellt auf grundlage des Erstelldatums einen Pfad und verschiebt die jeweilige Datei dorthin
            new_image_path = path + "/" + date_str_year + "/" + monthnumber
            shutil.move(image_path, os.path.join(new_image_path, x))

            # Erstellt einen Log Eintrag, wohin die jeweilige Datei verschoben wurde
            json_log.update({"LETZTES AENDERUNGSDATUM " + x: "Endung (Extension): " + file_extension + " || Verschoben in Ordner: " + date_str_year + "/" + date_str_month})

# Überprüft ob bereits ein Ordner für den log existiert (Legt einen an, wenn dies nicht der Fall ist)
if not os.path.isdir(os.path.join(path, "Log & Errors")):
    os.makedirs(os.path.join(path, "Log & Errors"))

# Erstellt die Log Datei und speichert den Log darin ab
with open(log_path, "w") as f:
    json.dump(json_log, f, indent=4)

# Bestätigt die Erfolgreiche Ausführung des Programms
print("Das Programm ist abgeschlossen. Eine Dokumentation meiner Arbeit ist unter " + log_path + " zu finden!")
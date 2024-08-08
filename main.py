import os
import exifread
from datetime import datetime
import json
import shutil

fileformat = [".png", ".jpg", ".jpeg", ".gif", ".tiff", ".svg", ".mp4", ".mov", ]
new_time_format = "%Y:%m:%d %H:%M:%S"
months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
json_log = {}

print("\nDer ImageSorter ist bereit. Ich übernehme folgenden Konfigurationen:")
print("\nDateiformate:" + str(fileformat))
print("Zeitformat:" + new_time_format)
print("Monate:" + str(months))
print("\nBitte gebe deinen Pfad an (Beispiel: C:/Users/Marius/Documents/Python/ImageSorter/Freunde):")
path = input()
log_path = path + "/Log & Errors/log.json"

files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
for x in files:

    file_name, file_extension = os.path.splitext(x)

    if file_extension in fileformat:
        image_path = "{}/{}".format(path, x)

        with open(image_path, 'rb') as image_file:
            tags = exifread.process_file(image_file)

        if 'Image DateTime' in tags:
            date_taken = tags['Image DateTime']
            date_taken_str = str(date_taken)

            date_taken_new_time = datetime.strptime(date_taken_str, new_time_format)
            date_taken_str_new_time_year = str(date_taken_new_time.year)
            date_taken_new_time_month = date_taken_new_time.month - 1
            date_taken_str_new_time_month = months[date_taken_new_time_month]

            if not os.path.isdir(os.path.join(path, date_taken_str_new_time_year)): #Überprüft ob schon ein Ordner vorhanden ist
                os.makedirs(os.path.join(path, date_taken_str_new_time_year)) #Falls "false" erstellt einen neuen Ordner

            monthnumber = str(date_taken_new_time_month + 1) + " " + date_taken_str_new_time_month
            monthpath= path + "/" + date_taken_str_new_time_year
            if not os.path.isdir(os.path.join(monthpath, monthnumber)): #Überprüft ob schon ein Ordner vorhanden ist
                os.makedirs(os.path.join(monthpath, monthnumber)) #Falls "false" erstellt einen neuen Ordner

            new_image_path = path + "/" + date_taken_str_new_time_year + "/" + monthnumber
            shutil.move(image_path, os.path.join(new_image_path, x))

            json_log.update({"AUFNAHMEDATUM " + x: "Endung (Extension): " + file_extension + " || Verschoben in Ordner: " + date_taken_str_new_time_year + "/" + date_taken_str_new_time_month})
            print("Bild " + x + " wurde verschoben")

        else:
            timestamp = os.stat(image_path).st_mtime
            date = datetime.fromtimestamp(timestamp)
            date_str_year = str(date.year)
            date_month = date.month - 1
            date_str_month = months[date_month]

            if not os.path.isdir(os.path.join(path, date_str_year)): #Überprüft ob schon ein Ordner vorhanden ist
                os.makedirs(os.path.join(path, date_str_year)) #Falls "false" erstellt einen neuen Ordner

            monthnumber = str(date_month + 1) + " " + date_str_month
            monthpath= path + "/" + date_str_year

            if not os.path.isdir(os.path.join(monthpath, monthnumber)): #Überprüft ob schon ein Ordner vorhanden ist
                os.makedirs(os.path.join(monthpath, monthnumber)) #Falls "false" erstellt einen neuen Ordner

            new_image_path = path + "/" + date_str_year + "/" + monthnumber
            shutil.move(image_path, os.path.join(new_image_path, x))
            json_log.update({"LETZTES AENDERUNGSDATUM " + x: "Endung (Extension): " + file_extension + " || Verschoben in Ordner: " + date_str_year + "/" + date_str_month})
            print("Bild " + x + " wurde verschoben")

if not os.path.isdir(os.path.join(path, "Log & Errors")):
    os.makedirs(os.path.join(path, "Log & Errors"))

    with open(log_path, "w") as f:
        json.dump(json_log, f, indent=4)

print("Das Programm ist abgeschlossen. Eine Dokumentation meiner Arbeit ist unter " + log_path + " zu finden!")
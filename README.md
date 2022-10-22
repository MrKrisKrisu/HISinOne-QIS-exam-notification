# HISinOne QIS -> Benachrichtigungen über bewertete Prüfungsleistungen

> **Warning**
> Dieses Skript wird von mir nicht mehr weiterentwickelt, da ich leider keinen Zugriff mehr auf eine Installation von
> HISinOne QIS habe. Ich empfehle einen Blick in folgenden Fork zu werfen:
> https://github.com/binsky08/HISinOne-QIS-exam-notification
>
> **Warning**
> This script will no longer be developed by me, since I unfortunately no longer have access to an installation of
> HISinOne QIS. I recommend to have a look at the following fork:
> https://github.com/binsky08/HISinOne-QIS-exam-notification

## Was ist das?

Ein Python Script, das sich für dich in iCMS einloggt und schaut, ob sich Änderungen (zum Beispiel eine neue
eingetragene Note) in der Prüfungsübersicht bei dir ergeben haben. Das Script benachrichtigt dich dann direkt per
Telegram. Es ist also dafür gedacht, beispielsweise alle 10 Minuten ausgeführt zu werden.

> Tut dem Hochschulserver einen Gefallen und fragt **nicht** alle 10 Sekunden ab!

## Kompatible Hochschulen

Die QIS-Software aus dem Paket HISinOne wird bei vielen Hochschulen in Deutschland eingesetzt. Sofern keine
individuellen Programmierungen vorhanden sind, sollte dieses Script bei diesen dann auch funktionieren.

Bislang sind folgende kompatible Hochschulen bekannt:

- Hochschule Hannover
- TU Braunschweig
- Leibniz Universität Hannover
- Hochschule Bremerhaven
- Westfälische Hochschule Gelsenkirchen
- Hochschule Koblenz
- FernUniversität in Hagen
- Hochschule Karlsruhe Technik und Wirtschaft

Alternative Skripts für weitere Hochschulen:

- [Hochschule Fulda (horstl)](https://github.com/binsky08/HISinOne-QIS-exam-notification)

## Installationsanleitung

### Telegram einrichten

#### Telegram Bot erstellen

Erstelle über den [BotFather](https://t.me/botfather) einen neuen Bot und schreibe dir den Token heraus. Mehr
Informationen zum erstellen von Telegram Bots: [https://core.telegram.org/bots](https://core.telegram.org/bots)

#### Telegram Chat ID herausfinden

* Erstelle eine neue Gruppe und füge deinen Bot hinzu, sowie den [TelegramRawBot](https://t.me/RawDataBot)
* Schreibe nun eine Nachricht in die Gruppe, der RawBot wird dir antworten
* Schreibe dir deine ID heraus, die unter **message -> from -> id** steht

### Python Umgebung

Die Module requests und lxml sind standardmäßig nicht installiert. Diese können mit pip nachinstalliert werden:
> pip install requests
> pip install lxml

### Script installieren

Lade das Script in deine Python Umgebung und passe in den oberen Zeilen die Werte für den Telegram Token und die
Telegram ChatID an. Außerdem musst du deine iCMS Zugangsdaten eingeben. Wenn du das Script jetzt ausführst solltest du
einmalig über **alle** eingetragenen Prüfungen benachrichtigt werden.

### Automatisches ausführen

Du kannst dein Script automatisch regelmäßig ausführen lassen (dafür ist es ja auch gedacht). Das kannst du mit einem
CronJob realisieren. Erstelle einfach folgenden CronJob:

> */15 * * * * /path/to/script.py

Dies führt dein Script automatisch alle 15 Minuten aus. Den Wert kannst du anpassen, aber denk dabei bitte an die armen,
armen Hochschulserver! Um das ganze noch mehr einzuschränken kann man die Ausführung auf die Prüfungsrelevanten Monate
begrenzen:
> */15 * * 1,2,6,7 * /path/to/script.py

## Sicherheitshinweis

Du musst dein zentrales Passwort für deinen Hochschulaccount in **Klartext** in dieses Script speichern. Achte daher
bitte darauf, dass es nur in einer gesicherten Umgebung läuft und durch geeignete Berechtigungen von dem Zugriff Dritter
geschützt ist.

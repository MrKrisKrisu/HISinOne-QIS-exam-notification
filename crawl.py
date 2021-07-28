#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import sys
import urllib.parse as urlparse
from pathlib import Path
from urllib.parse import parse_qs
import lxml.html as lh
import requests
from bs4 import BeautifulSoup

icms_username = '***-***-u1'
icms_password = '****'
telegram_bot_token = '****'
telegram_chatID = '****'


def telegram_bot_sendtext(bot_message):
    send_text = 'https://api.telegram.org/bot' + telegram_bot_token + '/sendMessage?chat_id=' \
                + telegram_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


payload = {
    "asdf": icms_username,
    "fdsa": icms_password,
    "name": "submit"
}

session_requests = requests.session()
session_requests.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'})

login_url = "https://icms.hs-hannover.de/qisserver/rds?state=user&type=0"
print("Rufe Startseite auf")
result = session_requests.get(login_url)

# login...
print("Einloggen...")
url_loginPost = "https://icms.hs-hannover.de/qisserver/rds?state=user&type=1&category=auth.login&startpage=portal.vm"
result = session_requests.post(
    url_loginPost,
    data=payload
)

# Extract SessionID
asi = None

soup = BeautifulSoup(str(result.content), 'html.parser')
for link in soup.find_all('a'):
    parsed = urlparse.urlparse(link.get('href'))
    params = parse_qs(parsed.query)
    if "asi" in params:
        asi = params.get("asi")[0]

if asi is None:
    print("SessionID couldn't be extracted")
    sys.exit()

print("Rufe Notenuebersicht Seite auf...")
result = session_requests.get(
    "https://icms.hs-hannover.de/qisserver/rds?state=notenspiegelStudent&next=list.vm&nextdir=qispos/notenspiegel/student&createInfos=Y&struct=auswahlBaum&nodeID=auswahlBaum%7Cabschluss%3Aabschl%3D84%2Cstgnr%3D1&expand=0&asi=" + asi,
    headers=dict(referer="https://icms.hs-hannover.de/qisserver/rds?state=sitemap&topitem=leer&breadCrumbSource=portal")
)

doc = lh.fromstring(str(result.content))
table_elements = doc.xpath('//table')
notenuebersicht_table = table_elements[1]

noten = {}

for tr in notenuebersicht_table:
    i = 0
    pruefungsnr = 0
    pruefungstext = 0
    art = 0
    note = 0
    status = 0
    credits = 0
    semester = 0
    for td in tr:
        text = str(td.text.replace("\\t", "").replace("\\r", "").replace("\\n", "").strip())

        i = i + 1
        if i == 1:
            pruefungsnr = text
        if i == 2:
            pruefungstext = text
        if i == 3:
            art = text
        if i == 4:
            note = text
        if i == 5:
            status = text
        if i == 7:
            credits = text
        if i == 9:
            semester = text

    if art != "PL":
        continue

    if semester not in noten:
        noten[semester] = dict()
    noten[semester][pruefungsnr] = {
        'pruefungstext': pruefungstext,
        'note': note,
        'status': status,
        'credits': int(credits)
    }

for semester in noten:
    for pruefungsnr in noten[semester]:
        toHash = semester + pruefungsnr + noten[semester][pruefungsnr]["status"]
        hash = hashlib.md5(toHash.encode("UTF-8")).hexdigest()

        knownHashes = Path('examcheck.txt').read_text()
        f = open('examcheck.txt', 'a+')
        if hash not in knownHashes:
            f.write(hash + "\n")

            message = "Neuer Pruefungsstatus " \
                      "\nModul: " + noten[semester][pruefungsnr]["pruefungstext"] + \
                      "\nStatus: " + noten[semester][pruefungsnr]["status"] + \
                      "\nNote: " + noten[semester][pruefungsnr]["note"]
            telegram_bot_sendtext(message)
        f.close()

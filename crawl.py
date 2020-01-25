#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import sys
import re
import json
import lxml.html as lh
import os.path
import os
import hashlib

icms_username = '***-***-u1'
icms_password = '****'
telegram_bot_token = '****'
telegram_chatID = '****'

def telegram_bot_sendtext(bot_message):
	send_text = 'https://api.telegram.org/bot' + telegram_bot_token + '/sendMessage?chat_id=' + telegram_chatID + '&parse_mode=Markdown&text=' + bot_message
	response = requests.get(send_text)
	return response.json()

payload = {
	"asdf": icms_username,
	"fdsa": icms_password,
	"name": "submit"
}

session_requests = requests.session()
session_requests.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'})

login_url = "https://icms.hs-hannover.de/qisserver/rds?state=user&type=0"
print("Rufe Startseite auf")
result = session_requests.get(login_url)

#login...
print("Einloggen...")
url_loginPost = "https://icms.hs-hannover.de/qisserver/rds?state=user&type=1&category=auth.login&startpage=portal.vm"
result = session_requests.post(
	url_loginPost,
	data = payload
)


result = session_requests.get("https://icms.hs-hannover.de/qisserver/rds?state=sitemap&topitem=leer&breadCrumbSource=portal")

try:
	link_notenspiegel = re.search('<a href="(.+?)" class="regular">Notenspiegel</a>', result.content).group(1)
	print("Link gefunden!")
	link_notenspiegel = link_notenspiegel.replace("amp;", "")
	print(link_notenspiegel)
except AttributeError:
	print("Error: Link Notelspiegel wurde nicht gefunden.")
	sys.exit()

print("Rufe Notespiegel Seite auf...")
result = session_requests.get(
	link_notenspiegel,
	headers=dict(referer="https://icms.hs-hannover.de/qisserver/rds?state=sitemap&topitem=leer&breadCrumbSource=portal")
)

try:
	link_notenuebersicht = re.search('<a href="(.+?)" title="Leistungen für Abschluss', result.content).group(1)
	print("Link gefunden!")
	link_notenuebersicht = link_notenuebersicht.replace("amp;", "")
	print(link_notenuebersicht)
except AttributeError:
	print("Error: Link Notenuebersicht wurde nicht gefunden.")
	sys.exit()

print("Rufe Notenuebersicht Seite auf...")
result = session_requests.get(
	link_notenuebersicht,
	headers=dict(referer="https://icms.hs-hannover.de/qisserver/rds?state=sitemap&topitem=leer&breadCrumbSource=portal")
)

doc = lh.fromstring(result.content)
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
		i = i + 1
		if(i == 1):
			pruefungsnr = td.text.strip()
		if(i == 2):
			pruefungstext = td.text.strip()
		if(i == 3):
			art = td.text.strip()
		if(i == 4):
			note = td.text.strip()
		if(i == 5):
			status = td.text.strip()
		if(i == 7):
			credits = td.text.strip()
		if(i == 9):
			semester = td.text.strip()
	if(art != "PL"):
		continue

	if semester not in noten:
		noten[semester] = dict()
	noten[semester][pruefungsnr] = {
	'pruefungstext': pruefungstext,
	'note': note,
	'status': status,
	'credits': credits
	}

for semester in noten:
	for pruefungsnr in noten[semester]:
		hash = hashlib.md5(semester + pruefungsnr + noten[semester][pruefungsnr]["status"]).hexdigest()
		f = open('examcheck.txt', 'a+')
		if hash not in f.read():
			f.write(hash + "\n")
			telegram_bot_sendtext("Neuer Pruefungsstatus \nModul: " + noten[semester][pruefungsnr]["pruefungstext"] + "\nStatus: " + noten[semester][pruefungsnr]["status"] + "\nNote: " + noten[semester][pruefungsnr]["note"])
		f.close()

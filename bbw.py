#!/usr/bin/python3

import os
import sys
import json
import time
import requests
from bs4 import BeautifulSoup

def parse(resp):
	#Function to parse response object
	#And return the writeups in json
	soup = BeautifulSoup(resp.content, "html5lib")
	trs = soup.find_all("tr")[1:]

	writeups = []
	for tds in trs:
		raw_tds = tds.findChildren()
		
		#Getting writeup title & URL
		raw_title = raw_tds[0].findChildren()
		if len(raw_title) > 0:
			link = raw_title[0]["href"]
			title = raw_title[0].get_text()
			if not title:
				title = "<No title given>"
			writeups.append({"Title": title.strip("\n"), "URL": link.strip("\n")})

	return writeups

def getWriteups():
	#Function to request for writeups
	#And return all of the writeups
	url = "https://pentester.land/list-of-bug-bounty-writeups.html"
	headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"}
	resp = requests.get(url, headers=headers)
	return parse(resp)

def printable(writeup):
	return f"""  Title: {writeup['Title']}
  URL: {writeup['URL']}
------------------------------"""

def saveWriteup(writeup, config):
	with open(config, "w") as wf:
		wf.write(json.dumps(writeup))

def getLatestWriteups():

	#Accessing the configuration file
	homeDir = os.path.expanduser("~")
	config = f"{homeDir}/.bbw.json"

	#Fetch all writeups
	allWriteups = getWriteups()

	latestWriteups = []
	if os.path.exists(config):
		with open(config, "r") as rf:
			lastWriteup = json.loads(rf.read())

			for writeup in allWriteups:
				if writeup == lastWriteup:
					break
				else:
					latestWriteups.append(writeup)

		#Save the latest writeup
		saveWriteup(allWriteups[0], config)

		if len(latestWriteups) == 0:
			return None
		else:
			return latestWriteups
	else:
		#Save the latest writeup
		saveWriteup(allWriteups[0], config)

		#Print the latest writeup
		return [allWriteups[0]]

def cron():
	while True:
		time.sleep(3600)
		latestWriteups = getLatestWriteups()
		if latestWriteups != None and len(latestWriteups) > 0:
			print("------------------------------")
			for writeup in latestWriteups:
				print(printable(writeup))
		else:
			print("No new writeups found.")

if __name__ == '__main__':

	if len(sys.argv) > 1 and sys.argv[1].lower() == "nocron":
		latestWriteups = getLatestWriteups()
		if latestWriteups != None and len(latestWriteups) > 0:
			print("------------------------------")
			for writeup in latestWriteups:
				print(printable(writeup))
		else:
			print("No new writeups found.")
	else:
		cron()

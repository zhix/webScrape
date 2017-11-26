#!/usr/bin/env python3

## using this script by running this "sudo python3 webScrape2.py" on terminal

import urllib.request
from bs4 import BeautifulSoup
import re
from threading import Thread
import json
from pprint import pprint
import csv

listNum = list(range(7400, 100000))

for i in range(0,len(listNum)):
	if len(str(listNum[i]))<5:
		listNum[i] = "0"+str(listNum[i])
	else: 
		listNum[i] = str(listNum[i])

storeIDlist = []

with open("outputStore3.csv", 'w') as myFile: 
	csvFile = csv.writer(myFile, delimiter=',', quoting=csv.QUOTE_ALL)
	csvFile.writerow(["Name", "StoreID", "City", "County", "PostCode", "Phone", "Manager", "URL"])

	for i in listNum: 
		print("checking zipcode: " + i)

		url='https://www.homedepot.com/l/search/' + i + '/full/'

		## function that will do actual scraping job
		html = urllib.request.urlopen(url).read()
		soup = BeautifulSoup(html, "lxml") 
		#print(soup) ## this prints the entire scrape from web
		script = soup.find('script', text=re.compile('THD_GLOBAL\.JSON_REP'))
		#print(script)

		## convert into json_text 
		json_text = re.search(r'^\s*THD_GLOBAL\.JSON_REP\s*=\s*({.*?})\s*;\s*$',
			script.string, flags=re.DOTALL | re.MULTILINE).group(1)
		##print (json_text)


		try: 
			## extract only the store information
			data = json.loads(json_text)['stores']

			# pprint(data[0])
			j = 0

			while j <len(data): 

				name = data[j]['name']
				storeid = data[j]['storeId']
				uri = data[j]['url']
				
				# address
				city = data[j]['address']['city']
				county = data[j]['address']['county']
				postcode = data[j]['address']['postalCode']

				# contact
				phone = data[j]['phone']
				manager = data[j]['storeContacts'][0]['name']

				dataList = [name, storeid, city, county, postcode, phone, manager, uri]

				## check if the row has already existed before writing the row 
				if storeid in storeIDlist: 
					print("Store ID: " + storeid + " already exists")
				else: 
					storeIDlist.append(storeid)
					csvFile.writerow(dataList)	
				
				j = j+1
		except: 
			pass
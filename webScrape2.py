#!/bin/usr/python3

import urllib.request
from bs4 import BeautifulSoup
import re
from threading import Thread
import json
from pprint import pprint
import csv

listNum = [35801, 35802, 35803, 35804]

with open("trial.csv", 'w') as myFile: 
	csvFile = csv.writer(myFile, delimiter=',', quoting=csv.QUOTE_ALL)
	csvFile.writerow(["Name", "StoreID", "City", "County", "PostCode", "Phone", "Manager", "URL"])

	for i in listNum: 
		url='https://www.homedepot.com/l/search/' + str(i) + '/full/'

		## function that will do actual scraping job
		html = urllib.request.urlopen(url).read()
		soup = BeautifulSoup(html)
		#print(soup) ## this prints the entire scrape from web
		script = soup.find('script', text=re.compile('THD_GLOBAL\.JSON_REP'))
		#print(script)

		## convert into json_text 
		json_text = re.search(r'^\s*THD_GLOBAL\.JSON_REP\s*=\s*({.*?})\s*;\s*$',
			script.string, flags=re.DOTALL | re.MULTILINE).group(1)

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
			#print(dataList)
			csvFile.writerow(dataList)
			j = j+1
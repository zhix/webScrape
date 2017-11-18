#!/bin/usr/python3

import urllib.request
from bs4 import BeautifulSoup
import re
from threading import Thread
import json
from pprint import pprint
import csv

url=['https://www.homedepot.com/l/search/' + str(35801) + '/full/']

i=0

#function that will do actual scraping job
def scrape(ur):

	html = urllib.request.urlopen(ur).read()
	soup = BeautifulSoup(html)
	#print(soup) ## this is the entire scrape from web
	script = soup.find('script', text=re.compile('THD_GLOBAL\.JSON_REP'))
	# print(script)

	## convert into json_text 
	json_text = re.search(r'^\s*THD_GLOBAL\.JSON_REP\s*=\s*({.*?})\s*;\s*$',
                      script.string, flags=re.DOTALL | re.MULTILINE).group(1)

threadlist = []

#making threads
while i<len(url):
	t = Thread(target=scrape,args=(url[i],))

	t.start()
	threadlist.append(t)
	i=i+1

for b in threadlist:
          b.join()


data = json.load(json_text)['stores']

# pprint(data[0])

i=0

with open("trial.csv", 'w') as myFile: 
	csvFile = csv.writer(myFile, delimiter=',', quoting=csv.QUOTE_ALL)
	csvFile.writerow(["Name", "StoreID", "City", "County", "PostCode", "Phone", "Manager", "URL"])
	while i<len(data): 
		name = data[i]['name']
		storeid = data[i]['storeId']
		url = data[i]['url']
		
		# address
		city = data[i]['address']['city']
		county = data[i]['address']['county']
		postcode = data[i]['address']['postalCode']

		# contact
		phone = data[i]['phone']
		manager = data[i]['storeContacts'][0]['name']


		dataList = [name, storeid, city, county, postcode, phone, manager, url]
		print(dataList)
		csvFile.writerow(dataList)
		i = i+1
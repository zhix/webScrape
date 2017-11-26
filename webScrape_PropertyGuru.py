#!/usr/bin/env python3

## using this script by running this "sudo python3 webScrape2.py" on terminal

import urllib.request
from bs4 import BeautifulSoup
import re
from threading import Thread
import json
from pprint import pprint
import csv

place	= "Puchong"
market	= "commercial"
minprice= 
minsize	= 
maxsize	= 
minppa 	= 
maxppa 	= 
tenure 	= 
furnishing = 

url="https://www.propertyguru.com.my/property-for-sale?freetext=" + place 
	+ "&market=" + market 
	+ "&minprice=" + int(minprice)
	+ "&minsize=" + int(minsize) 
	+ "&maxsize=" + int (maxsize) 
	+ "&minPricePerArea=" + int(minppa) 
	+ "&maxPricePerArea=" + int(maxppa)
	+ "&tenure%5B%5D=" + tenure 
	+ "&furnishing%5B%5D=" + furnishing

print(url)

## function that will do actual scraping job
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, "lxml") 
#print(soup) ## this prints the entire scrape from web
script = soup.find('script', text=re.compile('THD_GLOBAL\.JSON_REP'))
#print(script)
from bs4 import BeautifulSoup
from uszipcode import SearchEngine
import requests
import sys, os

#used for handling library print statements
# Disable printing
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restores printing
def enablePrint():
    sys.stdout = sys.__stdout__


#functions to get various data from weather.gov using bs4
def getData(locationUrl): #gets the main soup object
	res = requests.get(locationUrl) #gets all of html
	soup = BeautifulSoup(res.text,features="html.parser") #parses html w/ bs4
	return soup

def getLocationName(locationUrl):
	elems = getData(locationUrl).select('#current-conditions > div.panel-heading > div > h2')#gets info with given tag
	return elems[0].text.strip() #returns that info as text

def getCurrentTempF(locationUrl):
	elems = getData(locationUrl).select('#current_conditions-summary > p.myforecast-current-lrg')
	return elems[0].text.strip()

def getCurrentTempC(locationUrl):
	elems = getData(locationUrl).select('#current_conditions-summary > p.myforecast-current-sm')
	return elems[0].text.strip()

def getFirstForecastTitle(locationUrl):
	elems = getData(locationUrl).select('#detailed-forecast-body > div:nth-child(1) > div.col-sm-2.forecast-label')
	return elems[0].text.strip()

def getFirstForecastInfo(locationUrl):
	elems = getData(locationUrl).select('#detailed-forecast-body > div:nth-child(1) > div.col-sm-10.forecast-text')
	return elems[0].text.strip()

def getSecondForecastTitle(locationUrl):
	elems = getData(locationUrl).select('#detailed-forecast-body > div:nth-child(2) > div.col-sm-2.forecast-label')
	return elems[0].text.strip()

def getSecondForecastInfo(locationUrl):
	elems = getData(locationUrl).select('#detailed-forecast-body > div:nth-child(2) > div.col-sm-10.forecast-text')
	return elems[0].text.strip()

def output(givenLat,givenLng):
	url = 'https://forecast.weather.gov/MapClick.php?lat='+givenLat+'&lon='+givenLng
	print('The current temperature is '+ getCurrentTempF(url) + ' or '+getCurrentTempC(url) + ' in ' + getLocationName(url))
	print('\n The forecast for '+getFirstForecastTitle(url)+' is "' + getFirstForecastInfo(url) + '"')
	print('\n The forecast for '+getSecondForecastTitle(url)+' is "' + getSecondForecastInfo(url)+ '"')

goAgain = 'Y'
while goAgain == 'Y' or goAgain == 'y': #while loop allows users to enter new zipcodes
	choice = input("City(C) or Zipcode(Z): ")
	if(choice == 'Z'):
		try:
			givenzipCode = input('Enter a zipcode: ')
			print('Loading weather info...\n')
			blockPrint()
			search = SearchEngine(simple_zipcode=True) # set simple_zipcode=False to use rich info database
			zipcode = search.by_zipcode(givenzipCode)
			givenLat = str(zipcode.lat)
			givenLng = str(zipcode.lng)

			enablePrint()
			output(givenLat,givenLng)
			goAgain = input('\nTry another city/zipcode? (Y/N): ')
			print('\n')
		except IndexError: #handles if given zipcode doesn't exist
			print('Could not find zipcode. Please try again with a different zipcode')
			goAgain = input('\nTry another city/zipcode? (Y/N): ')
			print('\n')
	elif(choice == 'C'):
		try:
			givenName = input('Enter a city name: ')
			print('Loading weather info...\n')
			blockPrint()
			search = SearchEngine(simple_zipcode=True) # set simple_zipcode=False to use rich info database
			city = search.by_city(givenName)
			zipcode = city[0]
			givenLat = str(zipcode.lat)
			givenLng = str(zipcode.lng)
			
			enablePrint()
			print('Displaying weather forcast for ' + zipcode.major_city + ', ' + zipcode.state)
			output(givenLat,givenLng)
			goAgain = input('\nTry another city/zipcode? (Y/N): ')
			print('\n')
		except IndexError: #handles if given zipcode doesn't exist
			print('Could not find zipcode. Please try again with a different zipcode')
			goAgain = input('\nTry another city/zipcode? (Y/N): ')
			print('\n')

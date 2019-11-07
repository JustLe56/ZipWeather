from bs4 import BeautifulSoup
from uszipcode import SearchEngine
import requests

def getData(locationUrl):
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
def getTomorrowDayForecast(locationUrl):
	elems = getData(locationUrl).select('#detailed-forecast-body > div:nth-child(3) > div.col-sm-10.forecast-text')
	return elems[0].text.strip()


goAgain = 'Y'
while goAgain == 'Y' or goAgain == 'y':
	try:
		givenzipCode = input('Enter a zipcode: ')
		print('Loading weather info...\n')
		
		search = SearchEngine(simple_zipcode=True) # set simple_zipcode=False to use rich info database
		zipcode = search.by_zipcode(givenzipCode)
		zipInfo = zipcode.values()
		givenLat = str(zipInfo[7])
		givenLng = str(zipInfo[8])

		url = 'https://forecast.weather.gov/MapClick.php?lat='+givenLat+'&lon='+givenLng

		print('The current temperature is '+ getCurrentTempF(url) + ' or '+getCurrentTempC(url) + ' in ' + getLocationName(url))
		print('The forecast for tomorrow is "' + getTomorrowDayForecast(url) + '"')
		goAgain = input('Try another zipcode? (Y/N): ')
	except IndexError:
		print('Could not find zipcode. Please try again with a different zipcode')
		goAgain = input('\nTry another zipcode? (Y/N): ')


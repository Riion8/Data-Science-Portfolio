# Term  Project
# DSC510
# Author: Nathan Soer
# 3/2/2024
# This program will allow the user to look up the current weather and 5 day forcast for any US city or zip code.

import requests
import json
from columnar import columnar
import pandas
import os
import datetime

# Class to hold weather information
class Weather:
    time = 0
    weatherCondition = 'none'
    weatherConDetail = 'none'
    temperature = 0.0
    feelsLikeTemp = 0.0
    pressure = 0.0
    windSpeed = 'none'
    windDirecton = 'none'
    windGust = 'none'
    clouds = 'none'
    rain1hour = 0
    rain3hour = 0
    snow1hour = 0
    snow3hour = 0
    timezone = 0
    sunrise = 0
    sunset = 0
    minTemp = 0.0
    maxTemp = 0.0
    humidity = 0.0
    
    def __init__(self, time, weatherCondition, weatherConDetail, temperature, feelsLikeTemp, pressure, 
                 windSpeed, windDirecton, windGust, clouds, timezone, sunrise, sunset, minTemp, maxTemp,
                 humidity):
        self.time = time
        self.weatherCondition = weatherCondition
        self.weatherConDetail = weatherCondition
        self.temperature = float(temperature)
        self.feelsLikeTemp = float(feelsLikeTemp)
        self.pressure = pressure
        self.windSpeed = windSpeed
        self.windDirecton = windDirecton
        self.windGust = windGust
        self.clouds = clouds
        self.timezone = timezone
        self.sunrise = sunrise
        self.sunset = sunset
        self.minTemp = float(minTemp)
        self.maxTemp = float(maxTemp)
        self.humidity = humidity
    
    # Headers for use in printing the formated table of conditioins.    
    def getWeatherHeaders(self):
        return ['City Local Time', 'Condition', 'Temperature', 'Feels Like', 'Min Temp', 'Max Temp', 'Pressure', 'Humidity']
    
    # Body for use in printing the formated table of conditioins.
    def getWeatherBody(self, units):
        match units:
            case 'Standard':
                tUnit = 'K'
            case 'Metric':
                tUnit = 'C'
            case 'Imperial':
                tUnit = 'F'

        return [datetime.datetime.strftime(datetime.datetime.fromtimestamp(self.time+self.timezone, datetime.UTC),'%a %d %b %Y, %I:%M%p'),
                self.weatherConDetail, f'{self.temperature:.1f} {tUnit}', f'{self.feelsLikeTemp:.1f} {tUnit}', f'{self.minTemp:.1f} {tUnit}', f'{self.maxTemp:.1f} {tUnit}', f'{self.pressure:.0f} kPa', f'{self.humidity}%']

# Class the represents a City.
class Location:
    city = 'none'
    state = 'none'
    contry = 'none'
    lat = 'none'
    lon = 'none'
    
    def __init__(self, city = 'none', state = 'none', country = 'none', lon = 'none', lat = 'none'):
        self.city = city
        self.state = state
        self.country = country
        self.lon = lon
        self.lat = lat 

    def getCityState(self):
        if self.state == 'none':
            return self.city
        else:
            return self.city + ', ' + self.state + ' ' + self.country
    
    def getLatLon(self):
        return f'lat={self.lat}&lon={self.lon}'

# Function for Geo Coding a zip code using Open Weather Maps.
def apiGeoCodeZip(zip,apiKey):
    try:
        apiCall = f'http://api.openweathermap.org/geo/1.0/zip?zip={zip}&appid={apiKey}'
        response = requests.get(apiCall)
    except ConnectionError:
        print('Unable to connect to the server.  Please check your internet connection, close the program, and try again.')
        while True:
            pass
    except requests.HTTPError:
        print('Server Error.  Please close the program and try again later.')
        while True:
            pass
    except requests.Timeout:
        print('The server took too long to respond.  Please close the program and try again later.')
        while True:
            pass
    else:
        return response

# Function for Deo Coding a City using Open Weather Maps.
def apiGeoCodeCity(city,apiKey, state = 'none', country = 'US'):
    query = f'q={city}'
    # if a state is passed add the additional paramaters.
    if state != 'none':
        query +=f',{state},{country}'
    query += f'&limit=5&appid={apiKey}'
    
    try:
        apiCall = f'http://api.openweathermap.org/geo/1.0/direct?{query}'
        response = requests.get(apiCall)
    except ConnectionError:
        print('Unable to connect to the server.  Please check your internet connection, close the program, and try again.')
        while True:
            pass
    except requests.HTTPError:
        print('Server Error.  Please close the program and try again later.')
        while True:
            pass
    except requests.Timeout:
        print('The server took too long to respond.  Please close the program and try again later.')
        while True:
            pass
    else:
        return response

# Function to get the current conditions of the provided location
def getCurrentWeather(location, apiKey, units):
    try:
        apiCall = f'https://api.openweathermap.org/data/2.5/weather?{location.getLatLon()}&appid={apiKey}&units={units}'
        tempWeather = requests.get(apiCall)
        tempWeather = json.loads(tempWeather.content.decode("utf-8"))
    except ConnectionError:
        print('Unable to connect to the server.  Please check your internet connection, close the program, and try again.')
        while True:
            pass
    except requests.HTTPError:
        print('Server Error.  Please close the program and try again later.')
        while True:
            pass
    except requests.Timeout:
        print('The server took too long to respond.  Please close the program and try again later.')
        while True:
            pass
    else:    
        currentWeather = Weather(time = tempWeather['dt'], weatherCondition = tempWeather["weather"][0]['main'], 
            weatherConDetail = tempWeather["weather"][0]["description"], temperature = tempWeather['main']["temp"], 
            feelsLikeTemp = tempWeather['main']["feels_like"], pressure = tempWeather['main']["pressure"], 
            windSpeed = tempWeather['wind'], windDirecton = tempWeather['wind'], windGust = tempWeather['wind'], 
            clouds = tempWeather['clouds'], timezone = tempWeather['timezone'], 
            sunrise = tempWeather['sys']['sunrise'], sunset = tempWeather['sys']['sunset'],
            minTemp = tempWeather['main']['temp_min'], maxTemp = tempWeather['main']['temp_max'], humidity = tempWeather['main']['humidity'])
        return currentWeather

# Function to get the 5 day forcast weather.
def getWeatherForecast(location, apiKey, units):
    forcastWeather = []
    try:
        apiCall = f'https://api.openweathermap.org/data/2.5/forecast?{location.getLatLon()}&appid={apiKey}&units={units}'
        tempWeather = requests.get(apiCall)
        tempWeather = json.loads(tempWeather.content.decode("utf-8"))
    except ConnectionError:
        print('Unable to connect to the server.  Please check your internet connection, close the program, and try again.')
        while True:
            pass
    except requests.HTTPError:
        print('Server Error.  Please close the program and try again later.')
        while True:
            pass
    except requests.Timeout:
        print('The server took too long to respond.  Please close the program and try again later.')
        while True:
            pass
    else:    
        for x in range(len(tempWeather["list"])):
            forcastWeather.append(Weather(time = tempWeather["list"][x]["dt"], weatherCondition = tempWeather["list"][x]["weather"][0]["main"], 
                weatherConDetail = tempWeather["list"][x]["weather"][0]["description"], temperature = tempWeather["list"][x]["main"]["temp"], 
                feelsLikeTemp = tempWeather["list"][x]["main"]["feels_like"], pressure = tempWeather["list"][x]["main"]["pressure"], 
                windSpeed = tempWeather["list"][x]["wind"], windDirecton = tempWeather["list"][x]["wind"], windGust = tempWeather["list"][x]["wind"], 
                clouds = tempWeather["list"][x]["clouds"],sunrise = tempWeather['city']['sunrise'], sunset = tempWeather['city']['sunset'],
                timezone = tempWeather['city']['timezone'], minTemp = tempWeather['list'][x]["main"]['temp_min'], maxTemp = tempWeather['list'][x]["main"]['temp_max'], 
                humidity = tempWeather['list'][x]["main"]['humidity']))        
    
        return forcastWeather

# Checks that a zipcode is in a valid format
def checkValidZip(zipToCheck):
    zipToCheck = zipToCheck.strip()
    if len(zipToCheck)>5:
        zipToCheck = zipToCheck[0:4]
    elif len(zipToCheck)<5:
        return 'Invalid Zip Code'
    else:
        pass
        
    try:
        int(zipToCheck)
    except:
        return 'Invalid Zip Code'
    else:
        return zipToCheck
    
    
def main():
    print('Welcome to weather app.')
    #Start of program loop
    while True:
        cityList = []
        tempUnits = {1: 'Imperial',2: 'Metric',3: 'Standard'}
        apikey = ''
        skipWeather = False
    
        # Load Resource Files
        try:
            with open('USStateABBREVIATIONS.csv','r') as file:
                stateList = pandas.read_csv(file)
        except FileNotFoundError:
            print(f'Unable to find USStateABBREVIATIONS.csv.  Please ensure that the file exists here and restart the program: \n{os.path.dirname(__file__)}')
            while True:
                pass

        #Units Setting
        while True:
            print('What Units would you like the temperature in?')
            print('1) Fahrenheit')
            print('2) Celsius')
            print('3) Kelvin')
            print('Enter your selection: ')
            try:
                tempSelection = int(input())
                if tempSelection not in [1,2,3]:
                    raise ValueError
            except ValueError:
                print('Invalid input.  Please select a number from the list.\n')
            else:
                break
            
        #Determines if the user wants to use a city or zip code to search
        while True:
            print('Please select search method.')
            print('1) City, State')
            print('2) Zip Code')
            print('Enter your selection: ')
            try:
                searchSelection = int(input())
                if searchSelection not in [1,2]:
                    raise ValueError
            except ValueError:
                print('Invalid input.  Please select a number from the list.\n')
            else:
                break

        #Get City, State Input
        if searchSelection == 1:
            city = input('Please enter the city:  ')
            cityOnly = 'n'
            while True:
                state = input('Please enter the state (Abbreviation or Name):  ')
                if len(state.strip()) == 2 and len(stateList.loc[stateList['Abbreviation'] == state.upper().strip()]) > 0:
                    stateName = stateList.loc[stateList['Abbreviation'] == state.upper().strip(),'State'].iloc[0]
                    break
                elif len(state.strip()) == 2 and len(stateList.loc[stateList['Abbreviation'] == state.upper().strip()]) == 0:
                    print('Invalid State Abbreviation Entered.')
                    cityOnly = input('Search On City Name Only? (Y/N) ')
                elif len(state.strip()) > 2 and len(stateList.loc[stateList['State'] == state.capitalize().strip()]) > 0:
                    stateName = state.capitalize().strip()
                    break
                elif len(state.strip()) > 2 and len(stateList.loc[stateList['State'] == state.capitalize().strip()]) == 0:
                    print('Invalid State')
                    cityOnly = input('Search On City Name Only? (Y/N) ')
                else:
                    print('Invalid Text')
                    cityOnly = input('Search On City Name Only? (Y/N) ')
                if cityOnly.lower() == 'y':
                    stateName = 'none'
                    break
        
            response = apiGeoCodeCity(city= city.capitalize(),apiKey= apikey, state= stateName)
            citycontent = response.content.decode("utf-8")
            parsedjson = json.loads(citycontent)
            for x in parsedjson:
                cityList.append(Location(city = x['name'], lat = x['lat'],lon = x['lon'],country = x['country'],state = x['state']))
        #Gets Zip Code Input
        else:
            while True:
                zipcode = input('Please enter the zip code:  ')
                zipcode = checkValidZip(zipcode)
                if zipcode =='Invalid Zip Code':
                    print('Invalid zip code detected.  Please enter a valid 5 digit zip code.\n')
                else:
                    break
        
            response = apiGeoCodeZip(zip= zipcode,apiKey= apikey)
            citycontent = response.content.decode("utf-8")
            parsedjson = json.loads(citycontent)
            cityList.append(Location(city = parsedjson['name'], lat = parsedjson['lat'],lon = parsedjson['lon'],country = parsedjson['country']))
    
        #Checks to see if more than 1 city was returned. If there was it presents a list of cities for the user to select from.
        if len(cityList) > 1:
            while True:
                for x in range(len(cityList)):
                    print(str(x+1) + ' ' + cityList[x].getCityState())
                try:
                    selection = int(input('Please enter the number that corresponds to the city.'))-1
                except ValueError:
                    print('Invalid Selection')
                else:
                    break
        elif len(cityList) == 1:
            selection = 0
        #If no location was returned then print message and skip getting the weather.
        elif len(cityList) == 0:
            print('Loation Not Found')
            skipWeather = True

    
        if not skipWeather:
            currentWeather = getCurrentWeather(cityList[selection], apikey, tempUnits[tempSelection]) 
            forecastWeather = getWeatherForecast(cityList[selection], apikey, tempUnits[tempSelection]) 
    
            data = []
            data.append(currentWeather.getWeatherBody(tempUnits[tempSelection]))
        
            print(f'\n\nWeather for {cityList[selection].getCityState()}\n')    

            for x in range(len(forecastWeather)):
                 data.append(forecastWeather[x].getWeatherBody(tempUnits[tempSelection]))
    
            #Print the Weather to the screen as a table
            table = columnar(data, headers = currentWeather.getWeatherHeaders(),max_column_width=25,terminal_width = 200  )
            print(table)
        
        stopLoop = input('Get weather for another location? (Y/N)  ')
        if stopLoop.lower() != 'y':
            break

if __name__ == "__main__":
    main()

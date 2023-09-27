#Uses OpenWeatherMap to get the current weather. Position is determined via IP

import requests
import geocoder
import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)), 'NovaEngine'))

import ConfigInteraction

key = ConfigInteraction.GetKey("OpenWeather")

def Initialize():
    pass

def GetWeather():
    #Get position
    pos = geocoder.ip('me').latlng
    lat = float(pos[0])
    long = float(pos[1])

    response = requests.get(f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={long}&exclude=minutely,hourly,daily,alerts&appid=" + key).json()

    #The temperature is converted from kelvin to celcius and rounded
    return(f"Weather: {response['current']['weather'][0]['description']} Temp: {round(response['current']['temp'] - 273.15)}°C")
    
import os
import environ
import requests
from django.shortcuts import render

# Create your views here.
env = environ.Env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
# api_key = str(env('WEATHER_API_KEY'))
api_key = "f1cff3f042bece694e866a30de2127bf"


def get_weather_data(lat, lon):

    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    # Send the HTTP request
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Convert the response to JSON format
        #
        # weather_main = response["weather"][0]["main"]
        # wind_speed = response["wind"]["speed"]
        # pressure = response["main"]["pressure"]
        # city_name = response["name"]
        # temperature = response["main"]["temp"]
        # humidity = response["main"]["humidity"]
        # weather_description = response["weather"][0]["description"]
        #
        # print("Weather main:", weather_main)
        # print("Wind speed:", wind_speed)
        # print("Pressure:", pressure)
        # print("City name:", city_name)
        # print("Temperature:", temperature)
        # print("Humidity:", humidity)
        # print("Weather description:", weather_description)

        return response.json()

    else:
        print('Error:', response.status_code)

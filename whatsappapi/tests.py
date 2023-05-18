import requests

# Replace YOUR_API_KEY with your actual API key
api_key = 'f1cff3f042bece694e866a30de2127bf'

# Set the URL for the API endpoint
url = f'https://api.openweathermap.org/data/2.5/weather?lat=30.4211&lon=-9.5831&appid={api_key}'
# Send the HTTP request
response = requests.get(url)
# Check if the request was successful
if response.status_code == 200:
    # Convert the response to JSON format
    data = response.json()

    response = requests.get(url).json()

    weather_main = response["weather"][0]["main"]
    wind_speed = response["wind"]["speed"]
    pressure = response["main"]["pressure"]
    city_name = response["name"]
    temperature = response["main"]["temp"]
    humidity = response["main"]["humidity"]
    weather_description = response["weather"][0]["description"]

    print("Weather main:", weather_main)
    print("Wind speed:", wind_speed)
    print("Pressure:", pressure)
    print("City name:", city_name)
    print("Temperature:", temperature)
    print("Humidity:", humidity)
    print("Weather description:", weather_description)


else:
    print('Error:', response.status_code)

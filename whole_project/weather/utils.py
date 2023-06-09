import requests


class WeatherData:
    @staticmethod
    def get_weather_data():
        url = f'http://ip-api.com/json/'

        if url:
            location = requests.get(url).json()
            city = location['city']
            country = location['country']
            lat = location['lat']
            lon = location['lon']

            weather_prams = {
                'lat': lat,
                'lon': lon,
                'appid': '900df223f73677a3705eaa7ba19b13bb',
                'units': 'metric'
            }

            weather_api_url = 'http://api.openweathermap.org/data/2.5/weather'
            weather_data = requests.get(weather_api_url, params=weather_prams).json()

            temperature = round(weather_data['main']['temp'])
            condition = weather_data['weather'][0]['description']

            weather = {
                'city': city,
                'country': country,
                'temperature': temperature,
                'description': condition.capitalize(),
                'icon': weather_data['weather'][0]['icon']
            }

        else:
            weather = {
                'city': 'CityName',
                'country': 'CountryName',
                'temperature': None,
                'icon': None
            }

        return weather

from django.shortcuts import render, redirect
from django.views import View

from weather.utils import WeatherData

from datetime import datetime
import requests


class WeatherView(View):
    def get(self, request):
        weather_view = WeatherData()
        weather = weather_view.get_weather_data()

        context = {
            'weather': weather,
            'date_now': datetime.now()
        }

        return render(request, 'weather/test.html', context=context)


from django.shortcuts import render
from django.views import View
from django.views import generic

from weather.utils import WeatherData
from blog.models import Blog, Tag, Categories

from datetime import datetime


class HomeView(View):

    def get(self, request):
        weather_view = WeatherData()
        weather = weather_view.get_weather_data()

        model_blog = Blog.objects.order_by('-id')[:5]  # need check
        model_tag = Tag.objects.all()[::-1]
        model_category = Categories.objects.all()[::-1]

        context = {
            'weather': weather,
            'date_now': datetime.now(),
            'model_blog': model_blog,
            'model_tag': model_tag,
            'model_category': model_category,
        }
        return render(request, 'home.html', context=context)

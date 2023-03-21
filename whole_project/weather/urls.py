from django.urls import path
from . import views

urlpatterns = [
    path('weather_check/', views.WeatherView.as_view(), name='weather_check')
]
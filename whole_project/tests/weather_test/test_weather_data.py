import pytest

from weather.utils import WeatherData


@pytest.mark.django_db
def test_weather_data():
    weather = WeatherData().get_weather_data()
    assert weather is not None

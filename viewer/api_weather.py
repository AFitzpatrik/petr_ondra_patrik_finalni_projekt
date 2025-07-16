import requests

from django.conf import settings
from django.core.cache import cache


def get_weather_for_city(city_name):
    """
    Provede dotaz na OpenWeatherMap API na aktuální počasí pro zadané město.
    Vrací slovník: {'description':...., 'temperature':....}'. Při chybě vrátí None.
    """
    key = f"weather_{city_name.lower()}"
    cached_weather = cache.get(key)

    if cached_weather:
        return cached_weather

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city_name,
            'appid':settings.WEATHER_API_KEY,
            'units': 'metric',
            'lang': 'cz'
        }

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            result = {
                'description': data['weather'][0]['description'],  # posílá se tam list slovníků i když je tam většinou jenom jeden
                'temperature': round(data['main']['temp'], 1),
            }
            cache.set(key, result, timeout=60 * 15)
            return result

    except Exception as e:
        print(f"Weather API error: {e}")

    return None



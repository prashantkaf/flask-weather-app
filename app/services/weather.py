import requests
from flask import current_app


class WeatherServiceError(Exception):
    pass


def get_current_weather(city: str):
    """
    Fetch current weather for `city` from OpenWeatherMap.
    Returns a dict with keys: temp, humidity, description, icon, city, country
    Raises WeatherServiceError on failures.
    """
    api_key = current_app.config.get('OPENWEATHER_API_KEY')
    if not api_key:
        raise WeatherServiceError("OpenWeather API key is not configured")

    params = {
        'q': city,
        'appid': api_key,
        'units': current_app.config.get('WEATHER_UNITS', 'metric'),
    }
    try:
        resp = requests.get(current_app.config.get(
            'OPENWEATHER_URL'), params=params, timeout=8)
    except requests.RequestException as e:
        raise WeatherServiceError(f"Network error: {e}")

    if resp.status_code != 200:
        # try to extract message if present
        try:
            message = resp.json().get('message', resp.text)
        except Exception:
            message = resp.text
        raise WeatherServiceError(
            f"OpenWeather API error: {message} (status {resp.status_code})")

    try:
        data = resp.json()
        weather = {
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
            "city": data.get("name"),
            "country": data["sys"].get("country")
        }
        return weather
    except (KeyError, ValueError) as e:
        raise WeatherServiceError(f"Failed to parse weather data: {e}")

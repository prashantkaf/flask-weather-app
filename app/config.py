import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env file if present (development)
env_path = Path('.') / '.env'
if env_path.exists():
    load_dotenv(env_path)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', '')
    # OpenWeather base url
    OPENWEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
    # Temperature unit (metric = Celsius)
    WEATHER_UNITS = 'metric'

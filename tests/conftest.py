import pytest
from app import create_app


@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SECRET_KEY": "test",
        "OPENWEATHER_API_KEY": "test-api-key",
        "OPENWEATHER_URL": "https://api.openweathermap.org/data/2.5/weather",
        "WEATHER_UNITS": "metric"
    }
    app = create_app(test_config)
    yield app


@pytest.fixture
def client(app):
    return app.test_client()

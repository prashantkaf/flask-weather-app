import pytest
from app.services.weather import get_current_weather, WeatherServiceError


def test_get_current_weather_success(monkeypatch, app):
    sample_api_response = {
        "weather": [{"description": "clear sky", "icon": "01d"}],
        "main": {"temp": 20.5, "humidity": 40},
        "sys": {"country": "GB"},
        "name": "London"
    }

    class DummyResp:
        status_code = 200

        def json(self):
            return sample_api_response

    def fake_get(url, params, timeout):
        return DummyResp()

    monkeypatch.setattr('requests.get', fake_get)
    with app.app_context():
        result = get_current_weather("London")
        assert (result["temp"] - 20.5) < 1e-9
        assert result["humidity"] == 40
        assert result["description"] == "Clear Sky"
        assert result["icon"] == "01d"
        assert result["city"] == "London"


def test_get_current_weather_api_key_missing(app):
    # simulate missing api key
    with app.app_context():
        app.config['OPENWEATHER_API_KEY'] = ''
        with pytest.raises(WeatherServiceError):
            get_current_weather("Paris")


def test_get_current_weather_api_error(monkeypatch, app):
    class DummyResp:
        status_code = 404
        text = "city not found"

        def json(self):
            return {"message": "city not found"}

    def fake_get(url, params, timeout):
        return DummyResp()

    monkeypatch.setattr('requests.get', fake_get)
    with app.app_context():
        with pytest.raises(WeatherServiceError) as ei:
            get_current_weather("UnknownCity")
        assert "city not found" in str(ei.value)

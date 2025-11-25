from flask import Blueprint, render_template, request, current_app, flash
from .services.weather import get_current_weather, WeatherServiceError

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    error = None
    city = None

    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        if not city:
            flash("Please enter a city name.", "warning")
        else:
            try:
                weather = get_current_weather(city)
            except WeatherServiceError as e:
                error = str(e)
                # flash to show on UI
                flash(error, "danger")

    return render_template('index.html',
                           weather=weather,
                           error=error,
                           city=city,
                           api_key=current_app.config.get(
                               'OPENWEATHER_API_KEY'
                           ))

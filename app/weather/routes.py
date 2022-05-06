from flask import Blueprint
from weather.controller import get_weather

weather_bp = Blueprint('weather_bp', __name__)

weather_bp.route('/weather', methods=['GET'])(get_weather)
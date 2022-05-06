from flask import request, jsonify
from decouple import config
import requests
import json

API_KEY = config('WEATHER_API_KEY')

def get_weather():
    lat = request.args.get('lat')
    long = request.args.get('long')
    print(lat, long)
    response_API = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={API_KEY}")
    data = json.loads(response_API.text)
    return jsonify(data)
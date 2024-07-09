from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve
from datetime import datetime

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    #Check for empty string or spaces
    if not bool(city.strip()):
        city = "Dallas"

    weather_data = get_current_weather(city)

    #City not found by API
    if not weather_data['cod'] == 200:
        return render_template('city-not-found.html')
    
    print(weather_data)

    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data["main"]["temp"]:.1f}",
        h=f"{weather_data["main"]["temp_max"]:.1f}",
        l=f"{weather_data["main"]["temp_min"]:.1f}",
        feels_like=f"{weather_data["main"]["feels_like"]:.1f}",
        icon = weather_data['weather'][0]['icon'],
        wind=f"{weather_data["wind"]["speed"]:.1f}",
        windkph = f"{weather_data["wind"]["speed"] *1.609 :.1f}",
        precip = f"{weather_data['rain']['1h']:.2f}" if 'rain' in weather_data and '1h' in weather_data['rain'] else "0",
        precipcm = f"{weather_data['rain']['1h'] * 25.4:.2f}" if 'rain' in weather_data and '1h' in weather_data['rain'] else "0",
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
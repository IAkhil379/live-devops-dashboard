from flask import Flask, render_template_string
import requests
import os

app = Flask(__name__)

# You'll need to get your own API key from OpenWeatherMap
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "YOUR_OPENWEATHERMAP_API_KEY")
WEATHER_CITY = "New York"

@app.route('/')
def index():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        weather_data = response.json()
        
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        
        # This is a very basic HTML template for now
        html = f"""
        <!doctype html>
        <html>
        <head><title>Weather Dashboard</title></head>
        <body>
            <h1>Live Weather in {WEATHER_CITY}</h1>
            <p>Temperature: {temperature}°C</p>
            <p>Conditions: {description}</p>
        </body>
        </html>
        """
        return render_template_string(html)
    except Exception as e:
        return f"Error fetching weather data: {e}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
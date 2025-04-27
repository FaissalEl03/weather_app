from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv('OPENWEATHER_API_KEY')

@app.route('/')
def home():
    return render_template('weather.html')

@app.route('/weather')
def weather():
    city = request.args.get('city')
    if not city:
        return render_template('weather.html', error="Please enter a city name")
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        return render_template('weather.html', error="City not found")
    
    data = response.json()
    weather_data = {
        'city': city,
        'temp': round(data['main']['temp']),
        'description': data['weather'][0]['description'].capitalize(),
        'icon': data['weather'][0]['icon']
    }
    return render_template('weather.html', weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
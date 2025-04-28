from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

app = Flask(__name__)
API_KEY = "b703854d4471c3da2906c2d7cc8d5f71"

@app.route('/')
def home():
    return render_template('weather.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city', '').strip()
    
    if not city:
        return {"error": "Please enter a city name"}, 400
    
    try:
        # Get weather data
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        data = response.json()

        # Handle API errors
        if response.status_code != 200:
            return {"error": data.get('message', 'Weather service unavailable')}, response.status_code

        # Return clean response
        return {
            "city": data.get('name', city),
            "temp": round(data['main']['temp']),
            "description": data['weather'][0]['description'].capitalize(),
            "icon": data['weather'][0]['icon']
        }
        
    except Exception as e:
        return {"error": "Service temporarily unavailable"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
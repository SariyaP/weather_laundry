from decouple import config
from django.shortcuts import render
import requests

# Create your views here.
def index(request):
    city = config('CITY_NAME', default='Bangkok')
    api_key = config('OPENWEATHER_API_KEY')

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    context = {
        'city': city,
        'current_temp': int(data['main']['temp']),
        'humidity': data['main']['humidity'],
        'wind_speed': round(data['wind']['speed']),
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon'],
    }

    return render(request, 'index.html', context)
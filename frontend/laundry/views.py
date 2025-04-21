import requests
from django.shortcuts import render

def index(request):
    try:
        response = requests.get("http://127.0.0.1:8080/laundry-api/v1/api/latest")
        data = response.json()

        context = {
            'city': 'Bangkok',
            'current_temp': int(data['temp']),
            'humidity': data['humidity'],
            'wind_speed': round(data['wind_kph']),
            'description': data['w_condition'],
            'icon': None
        }

    except Exception as e:
        print("Error fetching data from API:", e)
        context = {
            'city': 'N/A',
            'current_temp': 'N/A',
            'humidity': 'N/A',
            'wind_speed': 'N/A',
            'description': 'API error',
            'icon': None
        }

    return render(request, 'index.html', context)


def data_visualization(request):
    return render(request, 'data_visualization.html')

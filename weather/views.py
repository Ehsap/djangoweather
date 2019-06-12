from django.shortcuts import render
from .models import City
from .forms import CityForm
from django.contrib import messages
import requests

# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=47eb67d0a23764571719195cdccbcb0c'

    cities = City.objects.all() 

    if request.method == 'POST':
        city_name = request.POST['name']
        r = requests.get(url.format(city_name))
        if r.status_code == 200 and not cities.filter(name=city_name).exists():
            form = CityForm(request.POST)
            form.save()

    form = CityForm()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city))
        if r.status_code != 200:
            continue

        r = r.json()
    
        city_weather = {
            'city' : city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'weather/weather.html', context)
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from calls.models import City
import requests

weather_types = ['Thunderstorm', 'Drizzle', 'Rain',
                'Snow', 'Atmosphere', 'Clear', 'Clouds']
start = 0

def index(request):
    template = loader.get_template('calls/base.html')
    context = {'types': weather_types}
    return HttpResponse(template.render(context, request))

def weather(request):
    template = loader.get_template('calls/cities.html')
    try:
        selected_choice = request.POST['choice']
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'calls/base.html', {
            'error_message': "Error making request",
        })
    requested = City.objects.filter(weather=selected_choice)
    clean_city_name = []
    clean_state_name = []
    for city in requested:
        clean_city_name.append(city.name.replace('+', ' '))
        clean_state_name.append(city.state.replace('+', ' '))
    zipped_data = zip(requested, clean_city_name, clean_state_name)
    context = {'chosen': selected_choice, 'types': weather_types,
               'requested':zipped_data}
    return HttpResponse(template.render(context, request))

def update(request):
    global start
    first_updated_city = start
    cities = City.objects.all()
    for city in cities[start:start+50]:
        URL = 'http://api.openweathermap.org/data/2.5/weather?units=Imperial&appid=bdfe6e6e001622cbb1f213249316f8e4&q='
        URL = URL + city.name + ',' + city.state + ',ISO 3166-2:US'
        r = requests.get(url = URL)
        data = r.json()
        city_to_be_updated = city
        city_to_be_updated.weather = data['weather'][0]['main']
        city_to_be_updated.temperature = data['main']['temp']
        city_to_be_updated.wind = data['wind']['speed']
        city_to_be_updated.save()
        if city == cities.last():
            start = -50
    start += 50
    template = loader.get_template('calls/base.html')
    context = {'types': weather_types, 'updating': 'Caching Weather Data from index ' + str(first_updated_city)}
    return HttpResponse(template.render(context, request))

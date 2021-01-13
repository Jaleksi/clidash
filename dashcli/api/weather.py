import requests
from datetime import datetime
from secret import WEATHER_API_KEY
from conf import COORDINATES_FOR_WEATHER


def fetch_data():
    '''
    returns:
        {
            current_temp
            current_icon
            day_corecast: [{day, temp_max, temp_min, icon} ...] (next 5 days)
            hour_forecast: [{time, temp, icon} ...] (next 8 hours)
        }
    '''
    api_url = 'http://api.openweathermap.org/data/2.5/onecall'
    param = {
        'appid': WEATHER_API_KEY,
        'lat': COORDINATES_FOR_WEATHER['oulu']['lat'],
        'lon': COORDINATES_FOR_WEATHER['oulu']['lon'],
        'exclude': 'minutely,alerts',
        'units': 'metric'
    }

    req = requests.get(url=api_url, params=param)

    if req.status_code != 200:
        return None

    data = req.json()

    weather_data = {
        'current_temp': data['current']['temp'],
        'current_icon': data['current']['weather'][0]['icon'],
        'day_forecast': [],
        'hour_forecast': []
    }

    for day in data['daily'][1:6]:
        weekday = datetime.utcfromtimestamp(int(day['dt'])).strftime('%A')
        temp_max = int(day['temp']['max'])
        temp_min = int(day['temp']['min'])
        icon = day['weather'][0]['icon']
        
        weather_data['day_forecast'].append({
            'day': weekday,
            'temp_max': temp_max,
            'temp_min': temp_min,
            'icon': icon
        })

    now = datetime.now()
    for hour in data['hourly']:
        if len(weather_data['hour_forecast']) == 8:
            break
        time = datetime.utcfromtimestamp(int(hour['dt']))
        if time < now:
            continue
        weather_data['hour_forecast'].append({
            'time': time.strftime('%H'),
            'temp': hour['temp'],
            'icon': hour['weather'][0]['icon']
        })
    
    return weather_data 

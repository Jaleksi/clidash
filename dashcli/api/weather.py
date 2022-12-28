import requests
from datetime import datetime
from ruuvitag_sensor.ruuvi import RuuviTagSensor

from secret import WEATHER_API_KEY, RUUVITAG_MAC
from conf import COORDINATES_FOR_WEATHER, USE_ROOVITAG_FOR_CURRENT_WEATHER


def fetch_data(days_to_fetch=5, hours_to_fetch=8):
    '''
    returns:
        {
            dt (current time in epoch)
            current_temp
            current_icon
            current_desc
            day_corecast: [{day, temp_max, temp_min, icon, cor} ...]
            hour_forecast: [{time, temp, icon, cor} ...]
            sun_data: {rise, set}
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

    current_temp = data['current']['temp']
    if USE_ROOVITAG_FOR_CURRENT_WEATHER:
        sensor_data = RuuviTagSensor.get_data_for_sensors([RUUVITAG_MAC], 10)
        current_temp = sensor_data[RUUVITAG_MAC]['temperature']

    weather_data = {
        'dt': data['current']['dt'],
        'current_temp': current_temp,
        'current_icon': data['current']['weather'][0]['icon'],
        'current_desc': data['current']['weather'][0]['main'],
        'day_forecast': [],
        'hour_forecast': [],
        'sun_data': {
            'rise': data['current']['sunrise'],
            'set': data['current']['sunset']
        }
    }

    for day in data['daily'][1:days_to_fetch + 1]:
        weekday = datetime.utcfromtimestamp(int(day['dt'])).strftime('%A')
        temp_max = int(day['temp']['max'])
        temp_min = int(day['temp']['min'])
        icon = day['weather'][0]['icon']
        cor = int(day['pop'] * 100)

        weather_data['day_forecast'].append({
            'day': weekday,
            'temp_max': temp_max,
            'temp_min': temp_min,
            'icon': icon,
            'cor': cor
        })

    now = datetime.now()
    for hour in data['hourly']:
        if len(weather_data['hour_forecast']) == hours_to_fetch:
            break
        time = datetime.utcfromtimestamp(int(hour['dt']))
        if time < now:
            continue
        weather_data['hour_forecast'].append({
            'time': time.strftime('%H'),
            'temp': hour['temp'],
            'icon': hour['weather'][0]['icon'],
            'cor': int(hour['pop'] * 100)
        })

    return weather_data 

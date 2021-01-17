import urwid
from api.weather import fetch_data
from conf import WEEKDAYS_ABR, WEATHER_ICON_MAP
from datetime import datetime

class WeatherBlock(urwid.Pile):
    def __init__(self, use_emojis=True):
        self.icons = use_emojis
        self.update_interval = 1800
        self.daily_forecast_count = 5
        self.hourly_forecast_count = 8
        
        self.text_map = {
            'current_temp': None,
            'last_updated': None,
            'hourly_forecasts': [],
            'daily_forecasts': []
        }

        self.current_weather = self.build_current_weather()
        self.hourly_forecast = self.build_hourly_forecast()
        self.daily_forecast = self.build_daily_forecast()
        self.layout = [
            (11, self.current_weather),
            urwid.Pile([
                self.hourly_forecast,
                self.daily_forecast
            ])
        ]
        super().__init__(self.layout)

    def update(self, main_loop, data=None):
        weather_data = fetch_data()

        temp_now = int(weather_data['current_temp'])
        temp_now = f'+{temp_now}' if temp_now > 0 else str(temp_now)
        self.text_map['current_temp'].set_text(temp_now)

        assert len(weather_data['hour_forecast']) == len(self.text_map['hourly_forecasts'])

        for forecast, hour_slot in zip(weather_data['hour_forecast'], self.text_map['hourly_forecasts']):
                hour_slot['time'].set_text(str(forecast['time']))
                hour_slot['temp'].set_text(str(int(forecast['temp'])))
                if self.icons:
                    hour_slot['icon'].set_text(WEATHER_ICON_MAP[forecast['icon']])
                else:
                    hour_slot['icon'].set_text(f'{forecast["cor"]}%')

        for forecast, day_slot in zip(weather_data['day_forecast'], self.text_map['daily_forecasts']):
                day_slot['day'].set_text(WEEKDAYS_ABR[forecast['day']])
                day_slot['temp'].set_text(f'{forecast["temp_max"]}/{forecast["temp_min"]}')
                if self.icons:
                    day_slot['icon'].set_text(WEATHER_ICON_MAP[forecast['icon']])
                else:
                    day_slot['icon'].set_text(f'{forecast["cor"]}%')

        updated_text = weather_data['current_desc'] + datetime.now().strftime(' [%H:%M]')
        self.text_map['last_updated'].set_text(updated_text)
        main_loop.set_alarm_in(self.update_interval, self.update)

    def build_current_weather(self):
        # Eri fontti?
        font = urwid.HalfBlock5x4Font()
        self.text_map['current_temp'] = urwid.BigText('Loading...', font)
        padding = urwid.Padding(self.text_map['current_temp'], width='clip', align='center')
        fill = urwid.Filler(padding, valign='bottom')
        
        self.text_map['last_updated'] = urwid.Text('loading...', align='center')
        description_fill = urwid.Filler(self.text_map['last_updated'], valign='top')
        
        return urwid.Pile([fill, description_fill])

    def build_hourly_forecast(self):
        hour_layouts = []

        for _ in range(self.hourly_forecast_count):
            text_objects = {
                'time': urwid.Text('--', align='center'),
                'icon': urwid.Text('--', align='center'),
                'temp': urwid.Text('--', align='center'),
            }
            hour_layout = urwid.LineBox(
                urwid.Pile([
                    urwid.Filler(text_objects['time'], valign='middle'),
                    urwid.Filler(text_objects['icon'], valign='middle'),
                    urwid.Filler(text_objects['temp'], valign='middle')
                ])
            )
            self.text_map['hourly_forecasts'].append(text_objects)
            hour_layouts.append(hour_layout)

        hourly_forecast_column = urwid.Columns(hour_layouts)
        return urwid.LineBox(hourly_forecast_column, title='Tuntiennuste')

    def build_daily_forecast(self):
        day_layouts = []

        for _ in range(self.daily_forecast_count):
            text_objects = {
                'day': urwid.Text('--', align='center'),
                'icon': urwid.Text('--', align='center'),
                'temp': urwid.Text('--', align='center'),
            }
            day_layout = urwid.LineBox(
                urwid.Pile([
                    urwid.Filler(text_objects['day'], valign='middle'),
                    urwid.Filler(text_objects['icon'], valign='middle'),
                    urwid.Filler(text_objects['temp'], valign='middle')
                ])
            )
            self.text_map['daily_forecasts'].append(text_objects)
            day_layouts.append(day_layout)

        day_forecast_column = urwid.Columns(day_layouts)
        return urwid.LineBox(day_forecast_column, title='Päiväennuste')


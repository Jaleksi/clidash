import datetime
import urwid
from api.weather import fetch_data
from conf import WEEKDAYS_ABR, WEATHER_ICON_MAP, WEATHER_DESC_FI

class WeatherBlock(urwid.Pile):
    def __init__(self, use_emojis=True):
        self.icons = use_emojis
        self.update_interval = 300 # 5 min
        self.daily_forecast_count = 7 # 7 is max
        self.hourly_forecast_count = 16
        
        self.text_map = {
            'current_temp': None,
            'current_desc': None,
            'hourly_forecasts': [],
            'daily_forecasts': [],
            'sun': {
                'rise': None,
                'set': None,
                'until': None,
                'bar': None
            }
        }

        self.current_weather = self.build_current_weather()
        self.hourly_forecast = self.build_hourly_forecast()
        self.daily_forecast = self.build_daily_forecast()
        self.sun_status = self.build_sun_status()
        self.layout = [
            (11, self.current_weather),
            urwid.Columns([
                self.hourly_forecast,
                urwid.Pile([
                    self.daily_forecast,
                    self.sun_status
                ])
            ])
        ]
        super().__init__(self.layout)

    def update(self, main_loop, data=None):
        weather_data = fetch_data(
            days_to_fetch=self.daily_forecast_count,
            hours_to_fetch=self.hourly_forecast_count
        )

        temp_now = int(weather_data['current_temp'])
        temp_now = f'+{temp_now}' if temp_now > 0 else str(temp_now)
        self.text_map['current_temp'].set_text(temp_now)

        for forecast, hour_slot in zip(weather_data['hour_forecast'], self.text_map['hourly_forecasts']):
                hour_slot['time'].set_text(str(forecast['time']))
                temp = int(forecast['temp'])
                prefix = '+' if temp > 0 else '-'
                hour_slot['temp'].set_text(prefix + str(temp))
                if self.icons:
                    hour_slot['icon'].set_text(WEATHER_ICON_MAP[forecast['icon']])
                else:
                    hour_slot['icon'].set_text(f'{forecast["cor"]}%')

        for forecast, day_slot in zip(weather_data['day_forecast'], self.text_map['daily_forecasts']):
                day_slot['day'].set_text(WEEKDAYS_ABR[forecast['day']])
                max_temp, min_temp = forecast['temp_max'], forecast['temp_min']
                max_temp_prefix = '+' if max_temp > 0 else '-'
                min_temp_prefix = '+' if min_temp > 0 else '-'
                day_slot['temp'].set_text(f'{max_temp_prefix}{max_temp}/{min_temp_prefix}{min_temp}')
                if self.icons:
                    day_slot['icon'].set_text(WEATHER_ICON_MAP[forecast['icon']])
                else:
                    day_slot['icon'].set_text(f'{forecast["cor"]}%')

        now = int(weather_data['dt'])
        sun_rise = int(weather_data['sun_data']['rise'])
        sun_set = int(weather_data['sun_data']['set'])
        if now < sun_rise:
            until_text = 'Nousuun: '
            delta = sun_rise - now
            bar_status = int((1 - (delta / 43200)) * 100)
            h, m, s = str(datetime.timedelta(seconds=delta)).split(':')
            until_time = f'{h}h {m}min'
        elif now < sun_set:
            until_text = 'Laskuun: '
            delta = sun_set - now
            bar_status = int((1 - (delta / (sun_set - sun_rise))) * 100)
            h, m, s = str(datetime.timedelta(seconds=delta)).split(':')
            until_time = f'{h}h {m}min'
        else:
            until_text = 'Nousuun: '
            until_time = '--:--'
            bar_status = 100

        self.text_map['sun']['rise'].set_text(
            'Auringonnousu: ' +
            datetime.datetime.fromtimestamp(sun_rise).strftime('%H:%M')
        )
        self.text_map['sun']['set'].set_text(
            'Auringonlasku: ' +
            datetime.datetime.fromtimestamp(sun_set).strftime('%H:%M')
        )
        self.text_map['sun']['until'].set_text(until_text + until_time)
        self.text_map['sun']['bar'].set_completion(bar_status)

        desc_text = WEATHER_DESC_FI[weather_data['current_desc']]
        self.text_map['current_desc'].set_text(desc_text)
        main_loop.set_alarm_in(self.update_interval, self.update)

    def build_current_weather(self):
        # Eri fontti?
        font = urwid.HalfBlock5x4Font()
        self.text_map['current_temp'] = urwid.BigText('Loading...', font)
        padding = urwid.Padding(self.text_map['current_temp'], width='clip', align='center')
        fill = urwid.Filler(padding, valign='bottom')

        self.text_map['current_desc'] = urwid.Text('loading...', align='center')
        description_fill = urwid.Filler(self.text_map['current_desc'], valign='top')

        return urwid.Pile([fill, description_fill])

    def build_hourly_forecast(self):
        hour_layouts = []
        hourly_header = urwid.Columns([
            urwid.Filler(urwid.Text('', align='left'), valign='middle'),
            urwid.Filler(urwid.Text('Sade', align='center'), valign='middle'),
            urwid.Filler(urwid.Text('°C', align='center'), valign='middle')
        ])
        hour_layouts.append(hourly_header)

        for _ in range(self.hourly_forecast_count):
            text_objects = {
                'time': urwid.Text('--', align='left'),
                'icon': urwid.Text('--', align='center'),
                'temp': urwid.Text('--', align='center'),
            }
            hour_layout = urwid.Columns([
                urwid.Filler(text_objects['time'], valign='middle'),
                urwid.Filler(text_objects['icon'], valign='middle'),
                urwid.Filler(text_objects['temp'], valign='middle')
            ])
            self.text_map['hourly_forecasts'].append(text_objects)
            hour_layouts.append(hour_layout)

        hourly_forecast_column = urwid.Pile(hour_layouts)
        return urwid.LineBox(hourly_forecast_column, title='Tuntiennuste')

    def build_daily_forecast(self):
        day_layouts = []
        daily_header = urwid.Columns([
            urwid.Filler(urwid.Text('', align='left'), valign='middle'),
            urwid.Filler(urwid.Text('Sade', align='center'), valign='middle'),
            urwid.Filler(urwid.Text('max/min', align='center'), valign='middle')
        ])
        day_layouts.append(daily_header)

        for _ in range(self.daily_forecast_count):
            text_objects = {
                'day': urwid.Text('--', align='left'),
                'icon': urwid.Text('--', align='center'),
                'temp': urwid.Text('--', align='center'),
            }
            day_layout = urwid.Columns([
                urwid.Filler(text_objects['day'], valign='middle'),
                urwid.Filler(text_objects['icon'], valign='middle'),
                urwid.Filler(text_objects['temp'], valign='middle')
            ])
            self.text_map['daily_forecasts'].append(text_objects)
            day_layouts.append(day_layout)

        day_forecast_column = urwid.Pile(day_layouts)
        return urwid.LineBox(day_forecast_column, title='Päiväennuste')

    def build_sun_status(self):
        self.text_map['sun']['rise'] = urwid.Text('--', align='center')
        self.text_map['sun']['set'] = urwid.Text('--', align='center')
        self.text_map['sun']['until'] = urwid.Text('--', align='center')
        self.text_map['sun']['bar'] = urwid.ProgressBar('normal', 'inverse', 50, 100)
        sun_layout = urwid.Pile([
            urwid.Filler(self.text_map['sun']['rise']),
            urwid.Filler(self.text_map['sun']['set']),
            urwid.Filler(self.text_map['sun']['until']),
            urwid.Filler(self.text_map['sun']['bar'])
        ])

        return urwid.LineBox(sun_layout, title='Aurinko')

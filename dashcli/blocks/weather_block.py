import urwid
from api.weather import fetch_data
from conf import WEEKDAYS_ABR, WEATHER_ICON_MAP

class WeatherBlock(urwid.Pile):
    def __init__(self):
        self.vertical_label_count = 12
        self.weather_data = fetch_data()

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

    def update(self):
        self.weather_data = fetch_data()

    def build_current_weather(self):
        # Eri fontti?
        font = urwid.HalfBlock5x4Font()
        temp_now = int(self.weather_data['current_temp'])
        temp_now = f'+{temp_now}' if temp_now > 0 else str(temp_now)
        text = urwid.BigText(temp_now, font)
        padding = urwid.Padding(text, width='clip', align='center')
        fill = urwid.Filler(padding, valign='bottom')
        
        weather_description = 'Puolipilvistä'
        text = urwid.Text(weather_description, align='center')
        description_fill = urwid.Filler(text, valign='top')
        
        return urwid.Pile([fill, description_fill])

    def build_hourly_forecast(self):
        hourly_temps = self.weather_data['hour_forecast']
        hourly_texts = []
        for hour in hourly_temps:
            hour_layout = urwid.LineBox(
                urwid.Pile([
                    urwid.Filler(urwid.Text(str(hour['time']), align='center'), valign='middle'),
                    urwid.Filler(urwid.Text(WEATHER_ICON_MAP[hour['icon']],align='center'), valign='middle'),
                    urwid.Filler(urwid.Text(str(int(hour['temp'])), align='center'), valign='middle')
                ])
            )
            hourly_texts.append(hour_layout)

        hourly_forecast_column = urwid.Columns(hourly_texts)
        return urwid.LineBox(hourly_forecast_column, title='Tuntiennuste')

    def build_daily_forecast(self):
        days = self.weather_data['day_forecast']
        day_texts = []
        for day in days:
            day_str = WEEKDAYS_ABR[day['day']]
            icon_str = WEATHER_ICON_MAP[day['icon']]
            temp_str = f'{day["temp_min"]}/{day["temp_max"]}'
            day_layout = urwid.LineBox(
                urwid.Pile([
                    urwid.Filler(urwid.Text(day_str, align='center'), valign='middle'),
                    urwid.Filler(urwid.Text(icon_str, align='center'), valign='middle'),
                    urwid.Filler(urwid.Text(temp_str, align='center'), valign='middle')
                ])
            )
            day_texts.append(day_layout)

        day_forecast_column = urwid.Columns(day_texts)
        return urwid.LineBox(day_forecast_column, title='Päiväennuste')


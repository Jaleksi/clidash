import unittest

class TestKarpatApi(unittest.TestCase):
    def setUp(self):
        from api.karpat import fetch_data
        self.games_to_fetch = 5
        self.games_data = fetch_data(self.games_to_fetch)

    def test_data_length(self):
        self.assertEqual(len(self.games_data), self.games_to_fetch)

    def test_data_type(self):
        self.assertEqual(type(self.games_data), list)
        for game in self.games_data:
            self.assertEqual(type(game), dict)

    def test_keys_exist(self):
        must_exist_keys = ['date', 'location', 'opponent', 'result']
        for game in self.games_data:
            for key in must_exist_keys:
                assert key in game and game[key] is not None

    def test_location_validity(self):
        for game in self.games_data:
            location = game['location']
            assert location in ['[KOTI]', '[VIERAS]'], f'Invalid location: {location}'

    def test_score_validity(self):
        for game in self.games_data:
            if 'won' in game:
                self.assertRegex(game['result'], '\d+-\d+', f'Invalid result: {game["result"]}')
            else:
                self.assertRegex(game['result'], '\d{2}:\d{2}', f'Invalid result: {game["result"]}')
                
    def test_opponent_validity(self):
        valid_opponents = [
            'Ässät',
            'HIFK',
            'HPK',
            'Ilves',
            'Jukurit',
            'JYP',
            'KalPa',
            'KooKoo',
            'Lukko',
            'Pelicans',
            'SaiPa',
            'Sport',
            'Tappara',
            'TPS',
        ]
        for game in self.games_data:
            assert game['opponent'] in valid_opponents, f'Invalid opponent: {game["opponent"]}'

    def test_date_validity(self):
        for game in self.games_data:
            date = game['date']
            self.assertRegex(date, '\d{1,2}\.\d{1,2}', f'Invalid date: {date}')
        

class TestWeatherApi(unittest.TestCase):
    def setUp(self):
        from api.weather import fetch_data
        from conf import WEATHER_DESC_FI, WEATHER_ICON_MAP, WEEKDAYS_ABR

        self.desc_map = WEATHER_DESC_FI
        self.icons_map = WEATHER_ICON_MAP
        self.weekdays_map = WEEKDAYS_ABR

        self.days_to_fetch = 5
        self.hours_to_fetch = 8
        self.data = fetch_data(self.days_to_fetch, self.hours_to_fetch)

    def test_data_type(self):
        self.assertEqual(type(self.data), dict)

    def test_keys_exist(self):
        keys = [
            'dt',
            'current_temp',
            'current_icon',
            'current_desc',
            'day_forecast',
            'hour_forecast',
            'sun_data',
        ]
        for key in keys:
            assert key in self.data and self.data[key] is not None

    def test_days_length(self):
        self.assertEqual(self.days_to_fetch, len(self.data['day_forecast']))

    def test_hours_length(self):
        self.assertEqual(self.hours_to_fetch, len(self.data['hour_forecast']))

    def test_current_data(self):
        assert self.data['current_icon'] in self.icons_map
        assert self.data['current_desc'] in self.desc_map

    def test_sun_data(self):
        sunrise = self.data['sun_data']['rise']
        sunset = self.data['sun_data']['set']
        
        assert sunrise is not None
        assert sunset is not None

        self.assertEqual(int, type(sunrise))
        self.assertEqual(int, type(sunset))

        assert sunrise < sunset

    def test_hourly_data(self):
        keys = ['time', 'temp', 'icon', 'cor']

        for hourly in self.data['hour_forecast']:
            for key in keys:
                assert key in hourly and hourly[key] is not None
            assert -1 < int(hourly['time']) < 24, f'Time out of range: {hourly["time"]}'
            assert hourly['icon'] in self.icons_map

    def test_daily_data(self):
        keys = ['day', 'temp_max', 'temp_min', 'icon', 'cor']

        for daily in self.data['day_forecast']:
            for key in keys:
                assert key in daily and daily[key] is not None
            assert daily['icon'] in self.icons_map
            assert daily['day'] in self.weekdays_map
            assert daily['temp_min'] <= daily['temp_max']
            assert -1 < daily['cor'] < 101


if __name__ == '__main__':
    unittest.main()

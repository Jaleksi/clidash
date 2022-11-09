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

    def test_keys_exists(self):
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
        

if __name__ == '__main__':
    unittest.main()

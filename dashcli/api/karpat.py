import requests
from datetime import date as _date
from bs4 import BeautifulSoup


def fetch_data():
    URL = 'https://www.liiga.fi/fi/joukkueet/karpat/otteluohjelma'
    req = requests.get(URL)

    content = BeautifulSoup(req.content, 'html.parser')
    games_table = content.find('table', {'class': 'games-list-table'}).find('tbody')

    game_infos = []

    for game in games_table.find_all('tr'):
        date = __format_date(game['data-time'])
        time = game.find('td', {'class': 'h-l'}).string
        teams = game.find('a', {'href': True}).string.split()
        home_game = teams[0] == 'Kärpät'
        opponent = teams[2] if home_game else teams[0]
        won = None
        for i in range(4):
            found_match = game.find('div', {'class': f'points-{i}'})
            if found_match:
                won = i > 0

        result = None if won is None else game.find_all('td')[5].string.replace(' — ', '-')

        game_infos.append(GameInfo(date, home_game, time, opponent, result, won))
        if len(game_infos) > 4:
            game_infos.pop(0)
        if won is None:
            break

    return game_infos


class GameInfo:
    def __init__(self, date, home_game, time, opponent, result=None, won=None):
        self.date = date
        self.home_game = home_game
        self.time = time
        self.opponent = opponent
        self.result = result
        self.won = won

    def pretty_line(self):
        h = '[Koti]' if self.home_game else '[Vieras]'
        t = '[V]' if self.won else '[H]'
        if self.won is None:
            return f'{h} {self.date} {self.time} {t} {self.opponent}'
        else:
            return f'{h} {self.date} {self.time} {t} {self.opponent} {self.result}'


def __format_date(date_string):
    '''
        from 20210708 to 8.7.
    '''
    year_stripped = date_string[4:]
    day, month = int(year_stripped[2:]), int(year_stripped[:2])
    return f'{day}.{month}.'

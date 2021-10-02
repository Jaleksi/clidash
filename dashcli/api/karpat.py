import requests
from bs4 import BeautifulSoup


def fetch_data():
    '''
        Dict keys match keys in blocks/sport_block.KarpatBlock text object dict.
    '''
    URL = 'https://old.liiga.fi/fi/ottelut/2021-2022/runkosarja/?team=karpat'
    req = requests.get(URL)

    content = BeautifulSoup(req.content, 'html.parser')
    games_table = content.find('table', {'class': 'games-list-table'}).find('tbody')

    game_infos = []

    for game in games_table.find_all('tr'):
        playing_teams = game.find('a', {'href': True}).string.split()
        home_game = playing_teams[0] == 'Kärpät'
        opponent = playing_teams[2] if home_game else playing_teams[0]
        time = game.find('td', {'class': 'h-l'}).string

        game_info = {
            'date': __format_date(game['data-time']),
            'location': '[KOTI]' if home_game else '[VIERAS]',
            'opponent': opponent
        }

        for i in range(4):
            found_match = game.find('div', {'class': f'points-{i}'})
            if found_match:
                game_info['won'] = '[V]' if i > 0 else '[H]'
                game_info['result'] = game.find_all('td')[5].string.replace(' — ', '-')

        game_infos.append(game_info)

        if len(game_infos) > 6:
            game_infos.pop(0)

        if 'result' not in game_info:
            game_info['result'] = time
            break

    return game_infos


def __format_date(date_string):
    '''
        from 20210708 to 8.7.
    '''
    year_stripped = date_string[4:]
    day, month = int(year_stripped[2:]), int(year_stripped[:2])
    return f'{day}.{month}.'

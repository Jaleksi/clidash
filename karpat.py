import requests
from bs4 import BeautifulSoup


def fetch_data(matches_to_fetch=7):
    '''
        Dict keys match keys in blocks/sport_block.KarpatBlock text object dict.
    '''
    URL = 'https://www.jatkoaika.com/Joukkue/karpat/ottelut?season=48258'
    req = requests.get(URL)

    content = BeautifulSoup(req.content, 'html.parser')
    games_table = content.find('h3', string='runkosarja').find_next_siblings('div')
    game_infos = []
    num_of_upcoming_games = 0

    for game in games_table:
        playing_teams = game.find('div', {'class': 'schedule-teams'}).text.split()
        home_game = playing_teams[0] == 'Kärpät'
        opponent = playing_teams[2] if home_game else playing_teams[0]
        date_and_time = game.findAll('span', {'class': 'date-display-single'})
        time = date_and_time[1].text.replace('.', ':')
        date = date_and_time[0].text[3:]
        game_info = {
            'date': date,
            'location': '[KOTI]' if home_game else '[VIERAS]',
            'opponent': opponent
        }
        score = game.find('div', {'class': 'schedule-score line'}).text.strip()
        if score:
            win = game.find('div', {'class': 'win'})
            ot_win = game.find('div', {'class': 'ot-win'})
            game_info['won'] = '[V]' if win or ot_win else '[H]'
            game_info['result'] = score

        game_infos.append(game_info)

        if len(game_infos) > matches_to_fetch:
            game_infos.pop(0)

        if 'result' not in game_info:
            game_info['result'] = time
            num_of_upcoming_games += 1

        if num_of_upcoming_games > 2:
            break

    return game_infos


def __format_date(date_string):
    '''
        from 20210708 to 8.7.
    '''
    year_stripped = date_string[4:]
    day, month = int(year_stripped[2:]), int(year_stripped[:2])
    return f'{day}.{month}.'

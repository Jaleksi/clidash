import requests
from datetime import datetime, timedelta

def fetch_data():
    two_weeks = timedelta(days=30)
    today = datetime.now()
    date_two_weeks_ago = today - two_weeks

    base_url = 'https://api.covid19tracking.narrativa.com/api/country/finland'
    params = {
        'date_from': date_two_weeks_ago.strftime('%Y-%m-%d'),
        'date_to': today.strftime('%Y-%m-%d')
    }

    req = requests.get(url=base_url, params=params)
    if req.status_code != 200:
        return None

    data = req.json()

    data = [
        {
            'date': day['countries']['Finland']['date'],
            'new_cases': day['countries']['Finland']['today_new_confirmed']
        }
        for _, day in data['dates'].items()
    ]
    return data

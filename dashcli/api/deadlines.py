import requests
import datetime

def fetch_data():
    '''
        returns
        {
            'code': int,
            'deadlines': [{'title': str, 'date': datetime object}...]
        }
    '''
    URL = 'http://jaleksi.pythonanywhere.com/deadlines'
    req = requests.get(URL)
    deadlines_data = req.json()

    # convert date strings to datetime objects
    # and add display string
    for deadline in deadlines_data:
        deadline['date'] = __to_datetime_object(deadline['date'])
        deadline['date_string'] = deadline['date'].strftime('%d.%m.%Y')

    # sort by date
    deadlines_data.sort(key=lambda d: d['date'])

    return {
        'code': req.status_code,
        'deadlines': deadlines_data,
    }


def __to_datetime_object(date_string):
    # datestring: '2022-01-01'
    # returns datetime object
    return datetime.datetime.strptime(date_string, '%Y-%m-%d')

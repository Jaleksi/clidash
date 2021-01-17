import random
import populartimes

from secret import GOOGLE_API_KEY
from conf import LOCATION_IDS


def fetch_data(debug=False):
    popularities = {}

    for name, place_id in LOCATION_IDS.items():
        if debug:
            popularities[name] = random.randint(1, 99)
        else:
            data = populartimes.get_id('123', place_id)
            popularities[name] = data.get('current_popularity', 'N/A')

    return popularities

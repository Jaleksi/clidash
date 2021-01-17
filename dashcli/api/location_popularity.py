import random
import populartimes

from secret import GOOGLE_API_KEY
from conf import LOCATION_IDS


def fetch_data(debug=False):
    popularities = {}

    for name, place_id in LOCATION_IDS.items():
        if debug:
            popularities[name] = random.randint(0, 100)
        else:
            data = populartimes.get_id(GOOGLE_API_KEY, place_id)
            popularities[name] = data['current_popularity']

    return popularities

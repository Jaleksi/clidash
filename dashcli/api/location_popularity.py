#import populartimes
import random
#from secret import GOOGLE_API_KEY

PLACE_IDS = {
    'Toppila fbg': 'ChIJDfknSXYtgEYRpNpayW1z8_k',
    'Hiironen fbg': 'ChIJz8lmVRPNgUYRxN5b-bhkveA',
    'Citymarket Rusko': 'hakematta',
    'K-Market Hiukkavaara': 'hakematta'
}


def fetch_data():
    popularities = {}

    for name, place_id in PLACE_IDS.items():
        #data = populartimes.get_id(GOOGLE_API_KEY, place_id)
        #cur_popularity = data['current_popularity']
        popularities[name] = random.randint(0, 100)

    return popularities

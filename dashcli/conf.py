PALETTE = [
    ('normal', 'dark blue', 'dark gray'),
    ('inverse', 'dark gray', 'dark blue'),
]

COORDINATES_FOR_WEATHER = {
    'oulu': {
        'lat': 65.012011,
        'lon': 25.483423
    }
}

WEATHER_ICON_MAP = {
    '01d': b'\xE2\x98\x80', # ☀
    '01n': b'\xF0\x9F\x8C\x99', # 🌙
    '02d': b'\xE2\x9B\x85', # ⛅
    '02n': b'\xE2\x9B\x85', # ⛅
    '03d': b'\xE2\x98\x81', # ☁
    '03n': b'\xE2\x98\x81', # ☁
    '04d': b'\xE2\x9B\x85', # ⛅
    '04n': b'\xE2\x9B\x85', # ⛅
    '09d': b'\xF0\x9F\x8C\xA7', # 🌧
    '09n': b'\xF0\x9F\x8C\xA7', # 🌧
    '10d': b'\xF0\x9F\x8C\xA7', # 🌧
    '10n': b'\xF0\x9F\x8C\xA7', # 🌧
    '11d': b'\xE2\x9A\xA1', # ⚡
    '11n': b'\xE2\x9A\xA1', # ⚡
    '13d': b'\xE2\x9D\x84\xEF\xB8\x8F', # ❄️
    '13n': b'\xE2\x9D\x84\xEF\xB8\x8F', # ❄️
    '50d': b'\xF0\x9F\x8C\x81', # 🌁 ???????
    '50n': b'\xF0\x9F\x8C\x81' # 🌁 should be rain
}

WEEKDAYS_ABR = {
    'Sunday': 'Su',
    'Monday': 'Ma',
    'Tuesday': 'Ti',
    'Wednesday': 'Ke',
    'Thursday': 'To',
    'Friday': 'Pe',
    'Saturday': 'La'
}

WEATHER_DESC_FI = {
    'Thunderstorm': 'Ukkosta',
    'Drizzle': 'Tihkusadetta',
    'Rain': 'Sadetta',
    'Snow': 'Lumisadetta',
    'Mist': 'Sumua',
    'Smoke': 'Savua',
    'Haze': 'Sumua',
    'Dust': 'Polya',
    'Fog': 'Sumua',
    'Sand': 'Hiekkaa',
    'Dust': 'Hiekkaa',
    'Ash': 'Tuhkaa',
    'Squall': 'Tuulenpuuskia',
    'Tornado': 'Tornado',
    'Clear': 'Kirkasta',
    'Clouds': 'Pilvista'
}

LOCATION_IDS = {
    'Toppila fbg': 'ChIJDfknSXYtgEYRpNpayW1z8_k',
    'Hiironen fbg': 'ChIJz8lmVRPNgUYRxN5b-bhkveA',
    'Citymarket Rusko': 'ChIJqdRMPc_SgUYRPQB5U8pNbxg',
    'K-Market Hiukkavaara': 'ChIJtVmZk_fTgUYRJbPtnsgVFEU'
}

import urwid
from api.location_popularity import fetch_data

class LocationPopularityBlock(urwid.LineBox):
    def __init__(self):
        self.update_interval = 1800
        self.places_text = urwid.Text('---', align='left')
        self.popularity_text = urwid.Text('---', align='right')
        self.layout = self.build_place_table()
        super().__init__(self.layout, title='Sijaintien suosio')

    def update(self, main_loop, user_data=None):
        popularity_data = fetch_data()
        places, popularities = '', ''

        for name, popularity in popularity_data.items():
            popularities += f'{popularity} %\n'
            places += f'{name}\n'

        self.places_text.set_text(places)
        self.popularity_text.set_text(popularities)
        main_loop.set_alarm_in(self.update_interval, self.update)

    def build_place_table(self):
        place_layout = urwid.Columns([
                urwid.Filler(self.places_text, valign='middle'),
                (5, urwid.Filler(self.popularity_text, valign='middle'))
            ])
        return place_layout

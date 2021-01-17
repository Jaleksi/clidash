import urwid
from api.location_popularity import fetch_data

class LocationPopularityBlock(urwid.LineBox):
    def __init__(self):
        self.popularity = fetch_data(debug=True)

        self.layout = self.build_place_table()
        super().__init__(self.layout, title='Sijaintien suosio')

    def update(self):
        self.popularity = fetch_data(debug=True)

    def build_place_table(self):
        pop_text = ''
        places_text = ''

        for name, popularity in self.popularity.items():
            pop_text += f'{popularity} %\n'
            places_text += f'{name}\n'
        
        place_layout = urwid.Columns([
                urwid.Filler(urwid.Text(places_text, align='left'), valign='middle'),
                (4, urwid.Filler(urwid.Text(pop_text, align='right'), valign='middle'))
            ])
        return place_layout

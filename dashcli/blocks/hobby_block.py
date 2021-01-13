import urwid
from api.location_popularity import fetch_data

class HobbyBlock(urwid.LineBox):
    def __init__(self):
        self.popularity = fetch_data()

        self.layout = urwid.Pile(self.build_place_table())
        super().__init__(self.layout, title='Sijaintien suosio')

    def update(self):
        self.popularity = fetch_data()

    def build_place_table(self):
        table_items = []

        for name, popularity in self.popularity.items():
            pop_text = f'{popularity} %'
            place_layout = urwid.Columns([
                    urwid.Filler(urwid.Text(name, align='left'), valign='middle'),
                    urwid.Filler(urwid.Text(pop_text, align='right'), valign='middle')
                ])
            table_items.append(place_layout)
        
        return table_items

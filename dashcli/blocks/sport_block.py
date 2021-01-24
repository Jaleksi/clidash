import urwid
from api.karpat import fetch_data

class KarpatBlock(urwid.Columns):
    def __init__(self):
        self.update_interval = 1800
        self.text_columns = {
            'location': urwid.Text('', align='left'),
            'date': urwid.Text('', align='left'),
            'won': urwid.Text('', align='left'),
            'opponent': urwid.Text('', align='left'),
            'result': urwid.Text('', align='left'),
        }
        self.layout = self.build_layout()
        super().__init__(self.layout)

    def update(self, main_loop, user_data=None):
        games_data = fetch_data()

        for data_title, text_obj in self.text_columns.items():
            new_text = ''
            for game in games_data:
                new_text += f'{game.get(data_title, "")}\n'
            text_obj.set_text(new_text)

        main_loop.set_alarm_in(self.update_interval, self.update)

    def build_layout(self):
        return [urwid.Filler(t, valign='middle') for _, t in self.text_columns.items()]

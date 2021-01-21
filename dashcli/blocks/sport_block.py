import urwid
from api.karpat import fetch_data

class KarpatBlock(urwid.Pile):
    def __init__(self):
        self.update_interval = 1800
        self.game_texts = []
        self.layout = self.build_layout()
        super().__init__(self.layout)

    def update(self, main_loop, user_data=None):
        games_data = fetch_data()
        for game, text_object in zip(games_data, self.game_texts):
            text_object.set_text(game.pretty_line())

        main_loop.set_alarm_in(self.update_interval, self.update)

    def build_layout(self):
        lines = []
        for _ in range(4):
            text = urwid.Text('----', align='left')
            self.game_texts.append(text)
            filler = urwid.Filler(text, valign='middle')
            lines.append(filler)

        return lines

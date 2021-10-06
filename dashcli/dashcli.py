import urwid

from blocks.sport_block import KarpatBlock
from blocks.timedate_block import TimedateBlock
from blocks.weather_block import WeatherBlock
from blocks.korona_block import KoronaBlock
from conf import PALETTE


class DashCli:
    def __init__(self):
        self.blocks = {
            'timedate': TimedateBlock(),
            'weather': WeatherBlock(use_emojis=False),
            'korona': KoronaBlock(),
            'karpat': KarpatBlock()
        }
        main_pile = urwid.Columns([
            urwid.Pile([
                (11, self.blocks['timedate']),
                urwid.Pile([
                    self.blocks['korona'],
                    self.blocks['karpat']
                ])
            ]),
            self.blocks['weather'],
        ])
        self.layout = urwid.Frame(body=main_pile)
        self.loop = urwid.MainLoop(self.layout, palette=PALETTE, unhandled_input=self.handle_input)

    def handle_input(self, key):
        if key == 'q':
            raise urwid.ExitMainLoop

    def start(self):
        self.init_alarms()
        self.loop.run()

    def init_alarms(self):
        for _, block in self.blocks.items():
            block.update(self.loop)


if __name__ == '__main__':
    dash = DashCli()
    dash.start()

import urwid

from blocks.hobby_block import HobbyBlock
from blocks.timedate_block import TimedateBlock
from blocks.weather_block import WeatherBlock

PALETTE = [
    ('normal', 'dark blue', 'dark gray'),
    ('inverse', 'dark gray', 'dark blue'),
]

class DashCli:
    def __init__(self):
        self.blocks = {
            'timedate': TimedateBlock(self.set_update),
            'weather': WeatherBlock(),
            'hobby': HobbyBlock()
        }
        main_pile = urwid.Columns([
            urwid.Pile([
                (11, self.blocks['timedate']),
                self.blocks['hobby']
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
        for block in [self.blocks['timedate']]:
            block.update()

    def set_update(self, interval, requester):
        self.loop.set_alarm_in(interval, requester.update)


if __name__ == '__main__':
    dash = DashCli()
    dash.start()

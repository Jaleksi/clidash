import urwid
from datetime import datetime as dt
from conf import WEEKDAYS_ABR


class TimedateBlock(urwid.Pile):
    def __init__(self, update_method):
        self.update_interval = 1
        self.request_update = update_method
        self.current_time = None
        self.current_date = None

        self.layout = [
            self.build_time(),
            self.build_date()
        ]
        super().__init__(self.layout)

    def update(self, *args):
        '''
            mainloop gives self and userdata=None as arguments
            when calling trough loop.set_alarm_in
        '''
        now = dt.now()
        time_now = now.strftime('%H:%M:%S')
        date_now = WEEKDAYS_ABR[now.strftime('%A')] + now.strftime(' %d.%m.%Y')
        self.current_time.set_text(time_now)
        self.current_date.set_text(date_now)
        self.request_update(self.update_interval, self)

    def build_time(self):
        time_now = 'Loading...'
        font = urwid.HalfBlock5x4Font()
        self.current_time = urwid.BigText(time_now, font)
        pad = urwid.Padding(self.current_time, width='clip', align='center')
        fill = urwid.Filler(pad, valign='bottom', top=3)
        return fill

    def build_date(self):
        date_now = 'Loading...'
        self.current_date = urwid.Text(date_now, align='center')
        fill = urwid.Filler(self.current_date, valign='top', top=0, bottom=0)
        return fill


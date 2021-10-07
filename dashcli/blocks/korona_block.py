import urwid
from api.corona import fetch_data

class KoronaBlock(urwid.LineBox):
    def __init__(self):
        self.update_interval = 10800 # 3 hours
        self.graph = urwid.BarGraph(
            ['normal', 'inverse'],
            {(1, 0): 'normal'}
        )   
        super().__init__(self.graph, title='Korona')

    def update(self, main_loop, data=None):
        corona_data = fetch_data()
        max_value = max(i['new_cases'] for i in corona_data)

        cases = [day['new_cases'] for day in corona_data]
        daily_cases = [(i,) for i in cases]
        self.graph.set_data(daily_cases, max_value)

        main_loop.set_alarm_in(self.update_interval, self.update)

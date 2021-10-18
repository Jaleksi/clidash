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
        data_values = [day['new_cases'] for day in corona_data]
        data_values = fill_zero_values_in_data(data_values)
        max_value = max(data_values)

        daily_cases = [(i,) for i in data_values]
        self.graph.set_data(daily_cases, max_value)

        main_loop.set_alarm_in(self.update_interval, self.update)



def fill_zero_values_in_data(data):
    zeroes_in_queue = []
    last_numeric_value = 0

    for i, val in enumerate(data):
        if val == 0:
            zeroes_in_queue.append(i)
            if i != len(data) - 1:
                continue

        if not zeroes_in_queue:
            last_numeric_value = val
            continue

        last_numeric_value = val if last_numeric_value == 0 else last_numeric_value
        fill_step = (last_numeric_value - val) // (len(zeroes_in_queue) + 1)

        for j, zero_index in enumerate(zeroes_in_queue):
            data[zero_index] = last_numeric_value - fill_step * (j + 1)

        last_numeric_value = val
        zeroes_in_queue = []

    return data

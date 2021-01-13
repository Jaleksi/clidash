def build_hourly_graph(self):
    hourly_temps = [0, -7, -3, 3, 6, 9, -1, -7, -3, 5, 10, 4]
    temp_offset = abs(min(hourly_temps)) + 1 # +1 jotta alin näyttää jotain
    temps_range = abs(min(hourly_temps)) + abs(max(hourly_temps)) + 1
    #hour_forecasts = [(hour['temp'],) for hour in weather_data['hour_forecast']]
    hour_forecasts = [(i + temp_offset,) for i in hourly_temps]
    graph = urwid.BarGraph(
        ['normal', 'inverse'],
        ['normal', 'inverse'],
        {(1, 0): 'normal'}
    )   
    graph.set_data(hour_forecasts, temps_range)
    graph_with_scale = urwid.Pile([
        self.build_hourly_graph_labels(),
        urwid.Columns([
            ('fixed', 3, self.build_hourly_graph_vertical_scale()),
            graph
        ]) 
    ])  
    return urwid.LineBox(graph_with_scale, title='Hourly forecast')

def build_hourly_graph_vertical_scale(self):
    mn = -7
    mx = 10
    values = []
    for i, value in enumerate(range(mn, mx+1)):
        values.append((i, str(value)))
    graph_scale = urwid.GraphVScale(values, len(values))
    print(values)
    return graph_scale

def build_hourly_graph_labels(self):
    hour_labels = [urwid.Text(str(i)) for i in range(12)]
    hour_labels = [urwid.Filler(label, valign='middle', top=0, bottom=0) for label in hour_labels
    label_wrapper = urwid.Columns(hour_labels)
    wrapper_padding = urwid.Padding(label_wrapper, left=4)
    return wrapper_padding

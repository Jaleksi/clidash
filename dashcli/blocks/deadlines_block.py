import urwid
from api.deadlines import fetch_data

class DeadlinesBlock(urwid.LineBox):
    def __init__(self):
        self.update_interval = 900 # 15 minutes
        self.text_columns = {
            'title': urwid.Text('', align='left', wrap='ellipsis'),
            'date_string': urwid.Text('', align='right', wrap='ellipsis'),
        }
        self.layout = self.build_layout()
        super().__init__(self.layout, title='Deadlinet')

    def update(self, main_loop, user_data=None):
        # deadlines should be in correct order (earliest first)
        deadlines_data = fetch_data()

        for data_title, text_obj in self.text_columns.items():
            new_text = ''
            for dl in deadlines_data:
                title = dl.get(data_title, "")
                new_text += f'{title}\n'
            text_obj.set_text(new_text)

        main_loop.set_alarm_in(self.update_interval, self.update)

    def build_layout(self):
        cols = [
            urwid.Filler(self.text_columns['title']
            , valign='middle'),
            (11, urwid.Filler(self.text_columns['time'], valign='middle'))
        ]
        return urwid.Columns(cols)

import urwid

class TestBlock(urwid.LineBox):
    def __init__(self):
        txt2 = urwid.Text('HELLO WORLD', align='center')
        fill2 = urwid.Filler(txt2, valign='middle', top=0, bottom=0)
        super().__init__(fill2)

    def update(self, *args, **kwargs):
        pass

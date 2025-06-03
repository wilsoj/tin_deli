from tkinter import *
from tkinter import ttk

PADX = 10
PADY = 10

TAB_DISPLAY_WIDTH = 53
TAB_DISPLAY_HEIGHT = 30

TAB_INFO_WIDTH = 53
TAB_INFO_HEIGHT = 10

SEP_HEIGHT = 342

BUTTON_WIDTH = 10


class Application(Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Tin Deli")
        self.resizable(width=False, height=False)

        self.selector = TabSelector(self)
        self.selector.grid(column=0, row=0, rowspan=3, sticky=N)

        self.separator = ttk.Separator(self, orient='vertical')
        self.separator.grid(column=1, row=0, rowspan=3, ipady=SEP_HEIGHT, padx=PADX*2)

        self.controls = TabControls(self)
        self.controls.grid(column=2, row=0)

        self.display = TabDisplay(self)
        self.display.grid(column=2, row=1)

        self.info = TabInfo(self)
        self.info.grid(column=2, row=2)


class TabSelector(ttk.Frame):
    """Tab selection including search bar and list of tabs"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.search_bar = SearchBar(self)
        self.search_bar.grid(column=0, row=0)

        self.scroller = TabScroller(self)
        self.scroller.grid(column=0, row=1, sticky=NW)


class SearchBar(ttk.Frame):
    """Search for tabs"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.label = ttk.Label(self, text='🔎')
        self.label.grid(column=0, row=0)

        self.search = ttk.Entry(self)
        self.search.grid(column=1, row=0)


class TabScroller(ttk.Frame):
    """Scrolls all tabs"""

    def __init__(self, parent, *args , **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.scroll_bar = Scrollbar(self, orient=VERTICAL)
        self.scroll_bar.grid()


class TabDisplay(ttk.Frame):
    """Harmonica tab player"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.contents = "This is text!"

        self.textbox = Text(self, width=TAB_DISPLAY_WIDTH,
                            height=TAB_DISPLAY_HEIGHT)
        self.textbox.insert('1.0', self.contents)
        self.textbox.config(state='disabled')
        self.textbox.grid(padx=(0,PADX), pady=PADY)


class TabControls(ttk.Frame):
    """Contains buttons to control tab playback"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.play = ttk.Button(self, text='⏵', width=BUTTON_WIDTH)
        self.play.grid(column=0, row=0)

        self.pause = ttk.Button(self, text='⏸', width=BUTTON_WIDTH)
        self.pause.grid(column=1, row=0)

        self.fastfwd = ttk.Button(self, text='⏩', width=BUTTON_WIDTH)
        self.fastfwd.grid(column=2, row=0)

        self.rewind = ttk.Button(self, text='⏪', width=BUTTON_WIDTH)
        self.rewind.grid(column=3, row=0)

        self.restart = ttk.Button(self, text='↻', width=BUTTON_WIDTH)
        self.restart.grid(column=4, row=0)

        self.practice = ttk.Button(self, text='practice', width=BUTTON_WIDTH)
        self.practice.grid(column=5, row=0)



class TabInfo(ttk.Frame):
    """Contains tab information: name, creator, etc."""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.contents = "This is also text!"

        self.textbox = Text(self, height=TAB_INFO_HEIGHT,
                            width=TAB_DISPLAY_WIDTH)
        self.textbox.insert('1.0', self.contents)
        self.textbox.config(state='disabled')
        self.textbox.grid(padx=(0,PADX), pady=PADY)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
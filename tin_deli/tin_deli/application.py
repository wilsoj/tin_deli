from tkinter import *
from tkinter import ttk

from . import models as m

PADX = 10
PADY = 10

TABS_LIST_WIDTH = 35
TABS_LIST_HEIGHT = 40

TAB_DISPLAY_WIDTH = 53
TAB_DISPLAY_HEIGHT = 30

TAB_INFO_WIDTH = 53
TAB_INFO_HEIGHT = 10

SEP_HEIGHT = 342

SEARCH_BAR_WIDTH = 35

BUTTON_WIDTH = 10

MAX_NOTE_DISPLAY = 10


class Application(Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Tin Deli")
        self.resizable(width=False, height=False)

        self.selector = TabSelector(self)
        self.selector.grid(column=0, row=0, rowspan=3, sticky=EW)

        self.separator = ttk.Separator(self, orient='vertical')
        self.separator.grid(column=1, row=0, rowspan=3, ipady=SEP_HEIGHT, padx=PADX*2)

        self.controls = TabControls(self)
        self.controls.grid(column=2, row=0)

        self.display = TabDisplay(self)
        self.display.grid(column=2, row=1)

        self.info = TabInfo(self)
        self.info.grid(column=2, row=2)

    def update_tab_display(self, *args):

        idx = self.selector.tabs.curselection()
        idx = int(idx[0]) + 1
        entry = m.TabModel().retrieve_entry(idx)

        self.display.update_tab(entry)
        self.info.update_info(entry)


class TabSelector(ttk.Frame):
    """Tab selection including search bar and list of tabs"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.label = ttk.Label(self, text='🔎')
        self.label.grid(column=0, row=0, sticky=NW)

        self.search = ttk.Entry(self, width=SEARCH_BAR_WIDTH)
        self.search.grid(column=1, row=0, sticky=EW)

        self.tabs = Listbox(self, width=TABS_LIST_WIDTH, height=TABS_LIST_HEIGHT)
        self.tabs.bind('<<ListboxSelect>>', parent.update_tab_display)
        self.tabs.grid(column=1, row=1, pady=PADY)

        self.scroll_bar_y = Scrollbar(self, orient=VERTICAL,
                                    command=self.tabs.yview)
        self.scroll_bar_y.grid(column=0, row=1, sticky=NS)

        self.scroll_bar_x = Scrollbar(self, orient=HORIZONTAL,
                                    command=self.tabs.xview)
        self.scroll_bar_x.grid(column=0, row=2, columnspan=2, sticky=EW)

        self.tabs['yscrollcommand'] = self.scroll_bar_y.set
        self.tabs['xscrollcommand'] = self.scroll_bar_x.set


        for name,creator in m.TabModel().retrieve_all_name_creators():
            self.tabs.insert('end', name + ' by ' + creator + ' ')


class TabDisplay(ttk.Frame):
    """Harmonica tab player"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.textbox = Text(self, width=TAB_DISPLAY_WIDTH,
                            height=TAB_DISPLAY_HEIGHT)
        self.textbox.tag_add('all', '1.0', END)
        self.textbox.tag_configure('all', justify='center')
        self.textbox.config(state='disabled')
        self.textbox.grid(padx=(0,PADX), pady=PADY)

        self.textbox.bindtags((str(self.textbox), str(parent), "all"))

    def update_tab(self, entry):
        self.textbox.config(state='normal')
        self.textbox.delete('1.0', END)
        self.textbox.insert('1.0', self.format_tab(entry["tab"]), ('all'))
        self.textbox.config(state='disabled')

    def format_tab(self, tab):
        notes = tab.split(" ")
        notes_split = [' '.join(notes[i:i+MAX_NOTE_DISPLAY]) for i in range(0, len(notes), 3)]
        return "\n\n".join(notes_split)


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

        self.textbox = Text(self, height=TAB_INFO_HEIGHT,
                            width=TAB_DISPLAY_WIDTH)
        self.textbox.config(state='disabled')
        self.textbox.grid(padx=(0,PADX), pady=PADY)

        self.textbox.bindtags((str(self.textbox), str(parent), "all"))

    def update_info(self, entry):
        self.textbox.config(state='normal')
        self.textbox.delete('1.0', END)
        self.textbox.insert('1.0', 'Name: ' + entry['name'] + '\n\n'
                                 + 'Creator: ' + entry['creator'] + '\n\n'
                                 + 'Key: ' + entry['key'])
        self.textbox.config(state='disabled')
        


if __name__ == "__main__":
    app = Application()
    app.mainloop()
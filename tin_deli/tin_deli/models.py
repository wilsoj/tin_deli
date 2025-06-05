import csv
import os
from pathlib import Path

KEYS = ["name", "creator", "key", "tab"]
MAX_TABS = 15


class TabModel:
    """Harmonica tab storage and access."""

    def __init__(self):

        self.datapath = Path(__file__).parent / ".." / "data" / "tabs.csv"

        with open(self.datapath, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            self.n_tabs = sum(1 for row in reader)


    def get_entry(self, id):
        with open(self.datapath, 'r') as f:
            reader = csv.reader(f)
            next(reader)

            for _ in range(id+1):
                values = next(reader)

            return dict(zip(KEYS, values))
        
    def get_entries(self, start_id, end_id):
        entries = []
        for i in range(start_id, end_id+1):
            entries.append(self.get_entry(i))

        return entries

    # def get_all_name_creators(self):

    #     entry_list = []
    #     for i in range(1, self.tab_count):
    #         entry = self.get_entry(i)
    #         entry_list.append((entry["name"],
    #                            entry["creator"]))
    #     return entry_list


if __name__ == "__main__":
    model = TabModel()
    entry = model.get_entry(1)
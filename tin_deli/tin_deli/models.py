import csv
from pathlib import Path

KEYS = ["name", "creator", "key", "tab"]


class TabModel:
    """Harmonica tab storage and access."""

    def __init__(self):
        self.datapath = Path(__file__).parent / ".." / "data" / "tabs.csv"

        with open(self.datapath, 'r') as f:
            reader = csv.reader(f)

            self.tab_count = sum(1 for row in reader)

    def retrieve_entry(self, index):
        with open(self.datapath, 'r') as f:
            reader = csv.reader(f)

            for _ in range(index+1):
                values = next(reader)

            return dict(zip(KEYS, values))

    def retrieve_all_name_creators(self):

        entry_list = []
        for i in range(1, self.tab_count):
            entry = self.retrieve_entry(i)
            entry_list.append((entry["name"],
                               entry["creator"]))
        return entry_list


if __name__ == "__main__":
    model = TabModel()
    entry = model.retrieve_entry(1)
    print(entry)
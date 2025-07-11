import csv
import os
from pathlib import Path
import re
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

def extract_tab_info(url):

    # Get webpage
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    web_byte = urlopen(req).read()

    webpage = web_byte.decode('utf-8')

    # Extract name, creator, key, and tab
    soup = BeautifulSoup(webpage, features="html.parser")
    text = soup.get_text()
    
    # Search for Song Name:\nSONG_NAME and extract SONG_NAME only
    name = re.search('Song Name:\n.*', text)[0]
    name = name.split('\n')[1] # ['Song Name:', 'SONG_NAME']
    name = name.title()
    
    if name == '':
        return None

    # Text also has 'Posted By:' that should be ignored (only want 'By:')
    creator = re.search('(?<!Posted\s)By:\n.*', text)[0]
    creator = creator.split('\n')[1]
    creator = creator.title()

    key = re.search('Key:\n.*', text)[0]
    key = key.split('\n')[1]

    # Raw tab text is pretty gross in terms of formatting
    # Assumes tabs eventually ends with 'Translate this page'
    # Sometimes has 'X users have Favorited this tab' so remove in case
    # Then remove all non-numeric chars, but keep some special chars
    # i.e. * only
    tab = re.search('Song:\n.*[0-9]*Translate', text, re.DOTALL)[0]
    tab = re.sub('\d* users have Favorited this tab', "", tab)
    tab = re.findall('(?<!-)-?\d\*?', tab)
    tab = " ".join(tab)

    return name, creator, key, tab

if __name__ == "__main__":
    # 4351 1i and 1o for blow and draw
    # 665
    # 25619
    # 28382 dots to extend notes -8.. and -7 . and .9 and .-9 and . 8
    # 16701 Numbers beside each other 555 4444 -8 -8 7
    # Brackets 23551 (-4 4) -3
    # 12641 Numbers beside each other with *: -4 -3    4*   4* -4-3-2*2
    # 20412 Less than symbol: -7      -8  +9 -7-7   +7<
    # 10138 Overblow and two harps? ( -6 6 5o 5 5o 5 -4 ) second harp
    # 12826 + for out: +9 -8 -7 +7 -6< -6 -5 +5
    # 17567: -2 -2 +3< -3 +5 +5 -5 +5 -5< -5 -5< -5 +5 -3
    # 10910: numbers beside each other and words (67) -(67) (67) (67) -(54) (54) -(54) (54) 4(long) -5 5 -4 -4
    # 11355: to apostrophes 4 -4 5 -5 5 -4 4 -3 -3''
    # 29669: (3) 4 (3)u (2) (2) (2) 5 (4)
    # 16070: 3   4  4  3  -3� 3
    # 13241 text with missing char:-3 -3    -3   -3   -3� 3  3   3   3 \n I said, I�ve been here a time or two. 
    # 24658 tab is good but text missing char:4   -4   4   -4  -3 -5   3   -5  -5* Mis-�ry loves com-pa-ny, wait and see.
    # 24006 overblow?: -4 5 -4 5 -4 5 5 -4 5 -4 5 -4 6 5o 

    url_base = "https://www.harptabs.com/song.php?ID={}"

    datapath = Path(__file__).parent / "tabs.csv"

    with open(datapath, 'w', newline='') as f:
        f.seek(0, os.SEEK_END)
        writer = csv.writer(f, delimiter=',')

        for i in range(101):
            tab_info = extract_tab_info(url_base.format(i))
            if tab_info != None:
                print("Writing tab")
                print(tab_info)
                writer.writerow(list(tab_info))
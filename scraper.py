import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import os

urls = ['https://acclaimedmusic.net/year/1940-49a.htm','https://acclaimedmusic.net/year/1950-59a.htm', 'https://acclaimedmusic.net/year/1960-69a.htm', 'https://acclaimedmusic.net/year/1970-79a.htm', 'https://acclaimedmusic.net/year/1980-89a.htm', 'https://acclaimedmusic.net/year/1990-99a.htm', 'https://acclaimedmusic.net/year/2000-09a.htm', 'https://acclaimedmusic.net/year/2010-19a.htm']

albums = {'Rank': [], 'All_Time': [], 'Artist': [], 'Album': [], 'Genres': [], 'Year': [], 'Decade': []}

def get_csv_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), 'albums.csv')
    else:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'albums.csv')
    
csv_path = get_csv_path()

def getGenres(row):
    genres = [genre.text for genre in row.find_all('a')[2:6] if genre.text != ' ']
    return ', '.join(genres)

for url in urls:
    source_code = requests.get(url).content
    soup = BeautifulSoup(source_code, 'html.parser')
    rows = soup.find_all('tr')[1:]
    for row in rows:
        if "the all-time top 3000:" in row.text:
            continue
        if row.find_all('div')[0].text == ' ':
            albums['Rank'].append(-1)
            albums['All_Time'].append(-1)
        else:
            albums['Rank'].append(int(row.find_all('div')[0].text))
            albums['All_Time'].append(int(row.find_all('div')[1].text))
        albums['Artist'].append(row.find_all('a')[0].text)
        albums['Album'].append(row.find_all('a')[1].text)
        albums['Genres'].append(getGenres(row))
        albums['Year'].append(int(row.find_all('a')[-1].text))
        albums['Decade'].append(str(albums['Year'][-1])[:-1] + '0s')

albums_df = pd.DataFrame(albums)
albums_df["In_Pool"] = "Y"
albums_df.to_csv(csv_path, index_label='ID')
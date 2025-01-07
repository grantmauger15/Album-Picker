import pandas as pd
import argparse
from datetime import datetime
import re
import os
import sys

def get_csv_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), 'albums.csv')
    else:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'albums.csv')


csv_path = get_csv_path()

parser = argparse.ArgumentParser(description='Album management tool.')
subparsers = parser.add_subparsers(dest="command", help='Available commands')

get_parser = subparsers.add_parser("get", help='Retrieve a random album based on filters.')
get_parser.add_argument('-y', '--year', type=str, help='Provide a decade, a year range, a year, or a combination of these to select an album from (e.g. "2010s", "2010-2018", "1994", "2010-2014, 2015").')
get_parser.add_argument('-g', '--genre', type=str, help='Provide a genre or a list of genres to select an album from (e.g. "Punk Rock" or "Jazz, Soul, Country").')
get_parser.add_argument('-t', '--top', type=int, help='Provide a number of albums that you want to select from. For example, if you want the top 1000 only do -t 1000')
get_parser.add_argument('-t100', '--top100', action='store_true', help='Limit selection to albums in the top 100 of its decade.')

remove_parser = subparsers.add_parser("remove", help='Remove an album from the pool given ID.')
remove_parser.add_argument('album_id', type=int, help='Remove an album from the selection pool by providing the ID of the album.')

list_parser = subparsers.add_parser("list", help='List the albums that have been removed from the selection pool.')

reset_parser = subparsers.add_parser("reset", help='Reset the pool of albums to select from.')

albums = pd.read_csv(csv_path)
args = parser.parse_args()


if args.command == "get":
    album_choices = albums

    if args.year:
        year_args = [arg.strip() for arg in args.year.split(',')]
        conditions = []

        for arg in year_args:
            if re.match(r'\d{4}s$', arg):
                conditions.append(f"Decade == '{arg}'")
            elif range := re.match(r'(\d{4})-(\d{4})$', arg):
                start, end = range.group(1), range.group(2)
                conditions.append(f"Year >= {start} & Year <= {end}")
            elif re.match(r'\d{4}$', arg):
                conditions.append(f"Year == {arg}")
            else:
                print("There was an issue parsing your arguments. Please try again.")
        
        conditions = " | ".join(conditions)
        album_choices = album_choices.query(conditions)

    if args.genre:
        genre_args = [arg.strip() for arg in args.genre.split(',')]
        conditions = []

        for arg in genre_args:
            conditions.append(f"Genres.str.contains('{arg}', case=False, na=False)")
            
        conditions = " | ".join(conditions)
        album_choices = album_choices.query(conditions)

    if args.top100:
        album_choices = album_choices.query('Rank <= 100 & Rank > 0')

    if args.top:
        album_choices = album_choices.query('All_Time <= @args.top & All_Time > 0')

    album_choices_pool = album_choices.query('In_Pool == "Y"')
    if album_choices_pool.empty:
        print("There are no albums that fit your requirements. Please try again.")
    else:
        choice = album_choices_pool.sample()
        print(f"Album: {choice['Album'].iloc[0]} by {choice['Artist'].iloc[0]}\nGenre(s): {choice['Genres'].iloc[0]}\nYear: {choice['Year'].iloc[0]}\nID: {choice['ID'].iloc[0]}")

elif args.command == "remove":
    if args.album_id in albums["ID"].values:

        albums.loc[albums["ID"] == args.album_id, ["In_Pool", "Date"]] = ["N", datetime.now()]
        albums.to_csv(csv_path, index=False)
        print(f"Album with ID {args.album_id} has been removed.")
    else:
        print(f"No album found with ID {args.album_id}.")

elif args.command == "reset":
    albums["In_Pool"] = "Y"
    albums.to_csv(csv_path, index=False)
    print("The pool has been reset.")

elif args.command == "list":
    removed_albums = albums.query('In_Pool == "N"')
    if not removed_albums.empty:
        removed_albums = removed_albums.sort_values(by="Date", ascending=True)
    list = []

    if not removed_albums.empty:
        for _, row in removed_albums.iterrows():
            album = row['Album']
            artist = row['Artist']
            date = row['Date']
            list.append(f"{album} by {artist} | {date}")
        print("\n".join(list))
    else:
        print("There are no albums in the list.")
else:
    parser.print_help()
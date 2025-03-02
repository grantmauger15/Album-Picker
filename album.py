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
get_parser.add_argument('-g', '--genre', type=str, help='Provide a genre or a list of genres to select an album from (e.g. "Punk Rock" or "Jazz; Soul; Country").')
get_parser.add_argument('-a', '--artist', type=str, help='Provide an artist or a list of artists to select an album from (e.g. "The Beatles" or "Led Zeppelin; Rolling Stones").')
get_parser.add_argument('-t', '--title', type=str, help='Provide a string or a list of strings to match against titles (e.g. "Lonely; Rock; Man").')
get_parser.add_argument('-r', '--rank', type=int, help='Provide rank requirements for your selection (e.g. 1000-, 50-100, 42).')
get_parser.add_argument('-t100', '--top100', action='store_true', help='Limit selection to albums in the top 100 of its decade.')
get_parser.add_argument('-c', '--count', type=str, help='Provide a number of albums that you want to receive. If you want every album that follows your requirements, put all.')

remove_parser = subparsers.add_parser("remove", help='Remove an album from the pool given ID.')
remove_parser.add_argument('album_id', type=int, help='Remove an album from the selection pool by providing the ID of the album.')

list_parser = subparsers.add_parser("list", help='List the albums that have been removed from the selection pool.')

reset_parser = subparsers.add_parser("reset", help='Reset the pool of albums to select from.')

albums = pd.read_csv(csv_path)
args = parser.parse_args()

def getConditional(command, column):
    comm = [command.split(',') for command in command.split(';')]

    for i in range(len(comm)):
        for j in range(len(comm[i])):
            c = comm[i][j].strip()

            if c.startswith('!'):
                comm[i][j] = f"~{column}.str.contains('{c[1:]}', case=False, na=False)"
            else:
                comm[i][j] = f"{column}.str.contains('{c}', case=False, na=False)"

    for i in range(len(comm)):
        comm[i] = " & ".join(comm[i])

    comm = " | ".join(comm)

    return comm

if args.command == "get":
    album_choices = albums

    if args.year:
        year_args = [arg.strip() for arg in args.year.split(',')]
        conditions = []

        for arg in year_args:
            if re.fullmatch(r'\d{3}0s', arg):
                conditions.append(f"Year >= {int(arg[:-1])} & Year <= {int(arg[:-1]) + 9}")
            elif range := re.fullmatch(r'(\d{4})-(\d{4})', arg):
                start, end = range.group(1), range.group(2)
                conditions.append(f"Year >= {start} & Year <= {end}")
                del range
            elif re.fullmatch(r'\d{4}', arg):
                conditions.append(f"Year == {arg}")
            elif re.fullmatch(r'\d{4}[\-+]', arg):
                if arg[-1] == '-':
                    conditions.append(f"Year <= {arg[:-1]} & Year > 0")
                if arg[-1] == '+':
                    conditions.append(f"Year >= {arg[:-1]} & Year > 0")
            else:
                print("The year flag takes either year ranges, like 2000-2009 or 2000+, years like 1979, or decades like 1960s. Please try again.")
                quit()
        
        conditions = " | ".join(conditions)
        album_choices['Year'] = pd.to_numeric(album_choices['Year'], errors='coerce').fillna(-1)
        album_choices['Year'] = album_choices['Year'].astype(int)
        album_choices = album_choices.query(conditions)

    if args.genre:
        album_choices = album_choices.query(getConditional(args.genre, "Genres"))

    if args.artist:
        album_choices = album_choices.query(getConditional(args.artist, "Artist"))

    if args.title:
        album_choices = album_choices.query(getConditional(args.title, "Album"))

    if args.top100:
        album_choices = album_choices.query('Rank <= 100 & Rank > 0')

    if args.rank:
        rank_args = [arg.strip() for arg in args.rank.split(',')]
        conditions = []

        for arg in rank_args:
            if range := re.fullmatch(r'(\d+)-(\d+)', arg):
                start, end = range.group(1), range.group(2)
                conditions.append(f"All_Time >= {start} & All_Time <= {end}")
            elif re.fullmatch(r'\d+[\-+]', arg):
                rank = int(arg[:-1])
                if arg[-1] == '-':
                    conditions.append(f"All_Time <= {rank} & All_Time >= 0")
                if arg[-1] == '+':
                    conditions.append(f"All_Time >= {rank} & All_Time >= 0")
            elif re.fullmatch(r'\d+', arg):
                rank = int(arg)
                conditions.append(f"All_Time == {rank}")
            else:
                print("The rank flag takes either rank ranges, like 50-100 or 1000-, or ranking numbers like 42. Please try again.")
                quit()

        conditions = " | ".join(conditions)
        album_choices['All_Time'] = pd.to_numeric(album_choices['All_Time'], errors='coerce').fillna(-1)
        album_choices['All_Time'] = album_choices['All_Time'].astype(int)
        album_choices = album_choices.query(conditions)

    album_choices_pool = album_choices.query('In_Pool == "Y"')
    if album_choices_pool.empty:
        print("There are no albums that fit your requirements. Please try again.")
    else:
        albums = []
        if args.count:
            if re.fullmatch(r'\d+', args.count):
                if int(args.count) <= 0:
                    print("A non-negative integer must be provided for the count flag. Please try again.")
                    quit()
                elif int(args.count) > 0 and int(args.count) > album_choices_pool.shape[0]:
                    print("Count number cannot be larger than the number of albums that fulfill requirements. Please try again.")
                    quit()
                else:
                    choices = album_choices_pool.sample(int(args.count))
            elif args.count == 'all':
                choices = album_choices_pool
            else:
                print("Either a positive integer or \"all\" must be provided for the count flag. Please try again.")
                quit()
        else:
            choices = album_choices_pool.sample()

        for _, choice in choices.iterrows():
            albums.append(f"Album: {choice['Album']} by {choice['Artist']} [{len(album_choices_pool)} total]\nGenre(s): {choice['Genres']}\nYear: {choice['Year']}\nID: {choice['ID']}")
        
        print("\033[34m-------------------------\033[0m\n" + "\n\033[31m-------------------------\033[0m\n".join(albums) + "\n\033[34m-------------------------\033[0m")

elif args.command == "remove":
    if args.album_id in albums["ID"].values:
        if albums.loc[albums["ID"] == args.album_id, "In_Pool"].iloc[0] == "Y":
            albums.loc[albums["ID"] == args.album_id, ["In_Pool", "Date"]] = ["N", datetime.now()]
            albums.to_csv(csv_path, index=False)
            print(f"Album with ID {args.album_id} has been removed.")
        else:
            print("That album has already been removed from the pool.")
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
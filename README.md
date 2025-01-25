## Album Picker CLI Tool
A simple command-line tool (CLI) to randomly pick albums based on year, genre, and other filters from a local album database.

## Features
- Retrieve a random album with the option to use year and/or genre as a filter.
- Mark albums as listened to by removing them from the pool of albums that can be selected.
- List all albums that are removed from the selection pool.
## Installation
### 1) Download the repository using CMD
```powershell
git clone "https://github.com/grantmauger15/Album-Picker.git"
cd Album-Picker
```
### 2) Run install.bat
```powershell
install.bat
```

#### You can now access the tool by using the "album" command in your preferred command line interface.
## Usage
Once installed, the tool can be used from anywhere in your terminal.
### Basic Commands
```bash
album get -y 2014 -g "Punk Rock" -t 2000
```
- The above command will fetch a random punk rock album that was released in 2014.
- The "-t 2000" part will filter out albums that are not in the top 2000 of all time. Change this value to what you like.
- Only the top 3000 albums of all time are ranked, so making the number greater than 3000 is pointless and will not include more albums.
```bash
Album: Transgender Dysphoria Blues by Against Me!
Genre(s): Punk Rock
Year: 2014
ID: 5315
```
- This is one possible output of the command stated above.
```bash
album get -y "2014, 1980s, 1974-1977" -g "Jazz, Soul, Country" -t100
```
- The above command uses more complex filtering criteria. 
- The album must be either jazz, soul, or country, and must have been released in either 2014, between 1974 and 1977, or in the 1980s.
- The -t100 flag will filter out albums that weren't in the top 100 for their respective decade.
```bash
album get
```
- All of the flags are optional, so if you simply want an album of any genre, year, or ranking, use the above command.
```bash
album get -c 5
```
- The above command does the same as the one before, except it picks 5 albums instead of only 1. If you want all albums that meet your criteria, do -c 0.
```bash
album remove 5315
```
- The above command removes an album (the one with ID 5315) from the pool of possible albums that can be selected using "album get".
- This command allows users to mark albums they've already listened to and do not want the tool to recommend again.
```bash
album list
```
- This command will list all albums that were removed using the "album remove" command. The date and time of removal will also be shown for each album.
```bash
Transgender Dysphoria Blues by Against Me! | 2025-01-06 02:36:15.418298
Mothership Connection by Parliament | 2025-01-06 02:36:23.785923
Katy Lied by Steely Dan | 2025-01-06 02:36:33.975701
```
- The above is one possible output of the "album list" command.
```bash
album reset
```
- This command will cause all albums to once again be selectable via the "album get" command.
```bash
album -h
```
- The -h flag can be applied to any command or subcommand to get more help with using the tool.
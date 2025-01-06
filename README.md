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
album get -y 2014 -g "Punk Rock" -t
```
- The above command will fetch a random punk rock album that was released in 2014.
- The -t flag will filter out albums that did not rank in the top 100 of their decade.
```bash
Album: Deep Fantasy by White Lung
Genre(s): Noise Rock, Punk Rock
Year: 2014
ID: 5963
```
- This is one possible output of the command stated above.
```bash
album get -y "2014, 1980s, 1974-1977" -g "Jazz, Soul, Country" -t3
```
- The above command uses more complex filtering criteria. 
- The album must be either jazz, soul, or country, and must have been released in either 2014, between 1974 and 1977, or in the 1980s.
- The -t3 flag will filter out albums that did not rank in the top 3000 of all albums in the database. There are 7019 albums in the database.
```bash
album get
```
- All of the flags are optional, so if you simply want an album of any genre, year, or ranking, use the above command.
```bash
album remove 5963
```
- The above command removes an album (the one with ID 5963) from the pool of possible albums that can be selected using "album get".
- This command allows users to mark albums they've already listened to and do not want the tool to recommend again.
```bash
album list
```
- This command will list all albums that were removed using the "album remove" command. The date and time of removal will also be shown for each album.
```bash
Deep Fantasy by White Lung | 2025-01-06 02:36:15.418298
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
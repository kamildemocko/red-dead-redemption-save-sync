# Red Dead Redemption Save File Sync

This Python script facilitates the synchronization of save files for the game **"Red Dead Redemption"** between Windows and Linux systems.  
It allows users to copy save files from one platform to another while creating **backups** of existing saves.
> For use when running game with **Non-steam** game from Steam app using proton.  

## Features

Cross-Platform Support: Easily copy save files between Windows and Linux.  
Backup Creation: Automatically creates timestamped backups of save files before overwriting.  
Command-Line Interface: Simple command-line arguments to specify the direction of the copy operation.  

## Requirements

Python 3.x
arrow

## Installation
```
uv sync
```

## Usage

1. Clone the repository or download the script.  
2. Edit settings.ini and set correct values, you can use $login instead of your unix username

```
[DEFAULT]
WIN_LOGIN_NAME=YOUR_WINDOWS_USERNAME
DRIVES_MOUNT_POINT=/run/media/$login
```
- some systems use `/mnt` or `/mount/USERNAME`

3. Run the script with the desired option:  

From Windows to Linux:
```
uv run python ./src/main.py --windows
```

From Linux to Windows:
```
uv run python ./src/main.py --linux
```

## Backup Location

Backups are stored in the ./backups/ directory with a timestamp in the filename.

## Notes
Ensure that the specified folder paths in the script match your system configuration.  
This is set-up in the **constants** group at the beginning of the file _main.py_

## License
This project is licensed under the MIT License. See the LICENSE file for details.
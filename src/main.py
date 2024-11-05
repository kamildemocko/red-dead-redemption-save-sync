import os
import argparse
from pathlib import Path
import tarfile
from shutil import copytree

import arrow

# constants
WIN_LOGIN_NAME = "kamil"
LINUX_DISK_C_DRIVE_ID = "01DAC57B4841EBE0"
LINUX_STEAM_FOLDER_ID = "3746069430"

LINUX_STEAM_SAVE_FOLDER = Path(
    f"~/.steam/steam/steamapps/compatdata/{LINUX_STEAM_FOLDER_ID}/pfx"
    "/drive_c/users/steamuser/AppData/Roaming/.1911/Red Dead Redemption"
).expanduser()

WIN_SAVE_FOLDER = Path(
    f"/run/media/{os.getlogin()}"
    f"/{LINUX_DISK_C_DRIVE_ID}/Users/{WIN_LOGIN_NAME}"
    "/AppData/Roaming/.1911/Red Dead Redemption"
)


def copy_from_windows() -> None:
    # check if dir exists in win
    if not WIN_SAVE_FOLDER.exists():
        raise FileNotFoundError(f"windows save folder not found at {WIN_SAVE_FOLDER}")

    # create backup
    timestamp = arrow.now().format("YYYY-MM-DDTHH-mm-ss")
    with tarfile.open(Path(f"./backups/backup_win_{timestamp}.tar"), "w:gz") as tar:
        tar.add(WIN_SAVE_FOLDER, recursive=True)

    # copy and overwrite
    copytree(WIN_SAVE_FOLDER, LINUX_STEAM_SAVE_FOLDER, dirs_exist_ok=True)


def copy_from_linux() -> None:
    # check if dir exists in win
    if not LINUX_STEAM_SAVE_FOLDER.exists():
        raise FileNotFoundError(f"linux steam save folder not found at {LINUX_STEAM_SAVE_FOLDER}")

    # create backup
    timestamp = arrow.now().format("YYYY-MM-DDTHH-mm-ss")
    with tarfile.open(Path(f"./backups/backup_lnx_{timestamp}.tar"), "w:gz") as tar:
        tar.add(LINUX_STEAM_SAVE_FOLDER, recursive=True)

    # copy and overwrite
    copytree(LINUX_STEAM_SAVE_FOLDER, WIN_SAVE_FOLDER, dirs_exist_ok=True)


def get_args() -> argparse.Namespace | None:
    parser = argparse.ArgumentParser(
        f"Copies saves for Red Dead Redemption game from and to Linux/Windows\n{Path(__file__).name}"
    )
    parser.add_argument("-w", "--windows", action="store_true", help="Copy from Windows to Linux")
    parser.add_argument("-l", "--linux", action="store_true", help="Copy from Linux to Windows")
    args = parser.parse_args()

    if not args.windows and not args.linux:
        parser.print_help()
        return None
    
    return args


def start(from_win: bool, from_lnx: bool) -> None:
    if from_lnx:
        copy_from_linux()

    elif from_win:
        copy_from_windows()


if __name__ == "__main__":
    args = get_args()

    if args is not None:
        start(args.windows, args.linux)


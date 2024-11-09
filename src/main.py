import argparse
from pathlib import Path
from configparser import ConfigParser

from copier import Copier


def get_args() -> argparse.Namespace | None:
    """
    Sets and gets arguments
    """
    parser = argparse.ArgumentParser(
        "Copies saves for Red Dead Redemption game from and to Linux/Windows\n"
        f"{Path(__file__).name}"
    )
    parser.add_argument(
        "-w", "--windows", action="store_true", help="Copy from Windows to Linux"
    )
    parser.add_argument(
        "-l", "--linux", action="store_true", help="Copy from Linux to Windows"
    )
    parsed_args = parser.parse_args()

    if not parsed_args.windows and not parsed_args.linux:
        parser.print_help()
        return None

    return parsed_args


def start(
    windows_user: str, drives_mount_point: str, from_win: bool, from_lnx: bool
) -> None:
    """
    runs program
    :param windows_user: (str)
    :param from_win: (bool)
    :param from_lnx: (bool)
    """
    copier = Copier("sda2", windows_user=windows_user, mount_point=drives_mount_point)

    if from_lnx:
        copier.copy_from_linux()

    elif from_win:
        copier.copy_from_windows()


if __name__ == "__main__":
    args = get_args()

    config = ConfigParser()
    config.read("settings.ini")
    win_login_name = config.get("DEFAULT", "WIN_LOGIN_NAME")
    drives_mnt_point = config.get("DEFAULT", "DRIVES_MOUNT_POINT")

    if args is not None:
        start(win_login_name, drives_mnt_point, args.windows, args.linux)

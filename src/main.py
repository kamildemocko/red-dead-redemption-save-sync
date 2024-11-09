import argparse
from pathlib import Path

from copier import Copier


def get_args() -> argparse.Namespace | None:
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
    args = parser.parse_args()

    if not args.windows and not args.linux:
        parser.print_help()
        return None

    return args


def start(from_win: bool, from_lnx: bool) -> None:
    copier = Copier()

    if from_lnx:
        copier.copy_from_linux()

    elif from_win:
        copier.copy_from_windows()


if __name__ == "__main__":
    args = get_args()

    if args is not None:
        start(args.windows, args.linux)

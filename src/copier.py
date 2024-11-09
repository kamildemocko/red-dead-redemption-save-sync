import os
from pathlib import Path
import tarfile
from shutil import copytree

import arrow

# constants
STEAM_ROOT = Path("~/.steam/steam/steamapps/compatdata").expanduser()
WIN_LOGIN_NAME = "kamil"
LINUX_DISK_C_DRIVE_ID = "01DAC57B4841EBE0"


class Copier:
    def __init__(self) -> None:
        self.linux_steam_save_folder = STEAM_ROOT.joinpath(
            f"{self._lookup_steam_folder_id()}/pfx/drive_c/users/steamuser/AppData/"
            "Roaming/.1911/Red Dead Redemption"
        )

        self.win_save_folder = Path(
            f"/run/media/{os.getlogin()}"
            f"/{LINUX_DISK_C_DRIVE_ID}/Users/{WIN_LOGIN_NAME}"
            "/AppData/Roaming/.1911/Red Dead Redemption"
        )

    @staticmethod
    def _lookup_steam_folder_id():
        profile = list(STEAM_ROOT.rglob("Red Dead Redemption/profile"))
        if len(profile) != 1:
            raise ValueError("cannot find steam profile folder")

        folder_id = profile[0].parents[8].name

        return folder_id

    def copy_from_windows(self) -> None:
        print("copying file from Windows")

        # check if dir exists in win
        if not self.win_save_folder.exists():
            raise FileNotFoundError(
                f"windows save folder not found at {self.win_save_folder}"
            )

        # create backup
        timestamp = arrow.now().format("YYYY-MM-DDTHH-mm-ss")
        with tarfile.open(Path(f"./backups/backup_win_{timestamp}.tar"), "w:gz") as tar:
            tar.add(self.win_save_folder, recursive=True)

        # copy and overwrite
        copytree(self.win_save_folder, self.linux_steam_save_folder, dirs_exist_ok=True)

        print("> done")

    def copy_from_linux(self) -> None:
        print("copying file from linux")

        # check if dir exists in win
        if not self.linux_steam_save_folder.exists():
            raise FileNotFoundError(
                f"linux steam save folder not found at {self.linux_steam_save_folder}"
            )

        # create backup
        timestamp = arrow.now().format("YYYY-MM-DDTHH-mm-ss")
        with tarfile.open(Path(f"./backups/backup_lnx_{timestamp}.tar"), "w:gz") as tar:
            tar.add(self.linux_steam_save_folder, recursive=True)

        # copy and overwrite
        copytree(self.linux_steam_save_folder, self.win_save_folder, dirs_exist_ok=True)

        print("> done")

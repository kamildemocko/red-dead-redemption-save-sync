import os
import sys
import subprocess
from pathlib import Path
import tarfile
from shutil import copytree

import arrow

STEAM_ROOT = Path("~/.steam/steam/steamapps/compatdata").expanduser()


class Copier:
    """
    The class that copies files along with few utils
    """

    def __init__(
        self, device: str, windows_user: str, mount_point: str = "/run/media/$login"
    ) -> None:
        """
        :param device: (str) device to look for, example: sda2
        :param mount_point: (str) path where disks are mounted,
            default is /run/media/username (arch)
            other systems might put it under /media/username or /mnt
            pass $login to get current user login (os.getlogin)
        """
        self.device = device
        self.mount_point_path = Path(mount_point.replace("$login", os.getlogin()))

        self.linux_steam_save_folder = STEAM_ROOT.joinpath(
            f"{self._lookup_steam_folder_id()}/pfx/drive_c/users/steamuser/AppData/"
            "Roaming/.1911/Red Dead Redemption"
        )

        self.win_save_folder = Path(
            f"{self.mount_point_path}/{self._get_drive_id(device)}/Users/{windows_user}"
            "/AppData/Roaming/.1911/Red Dead Redemption"
        )

    @staticmethod
    def _lookup_steam_folder_id():
        """
        looks up folder Red Dead Redemption in steam root folder
        """
        profile = list(STEAM_ROOT.rglob("Red Dead Redemption/profile"))
        if len(profile) != 1:
            raise ValueError("cannot find steam profile folder")

        folder_id = profile[0].parents[8].name

        return folder_id

    def _try_mount_win_device(self, device: str) -> bool:
        """
        try mount drive if not found
        this might ask for root password
        :param device: (str) device name
        :returns: (bool) successful or not
        """
        print(f"Trying to mount device {device}, you might be prompted for password")

        dev_id = self._get_drive_id(device)

        try:
            subprocess.run(
                ["sudo", "mkdir", "-p", self.mount_point_path.joinpath(dev_id)],
                check=True,
            )

            subprocess.run(
                [
                    "sudo",
                    "mount",
                    f"/dev/{device}",
                    f"{self.mount_point_path}/{dev_id}",
                ],
                check=True,
            )

            return True

        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def _get_drive_id(device: str) -> str:
        """
        Get drive ID, under which it is mounted
        :param device: (str) device to look for, example: sda2
        """
        sp = subprocess.run(
            [f"lsblk -o NAME,UUID | grep {device}"],
            check=True,
            text=True,
            capture_output=True,
            shell=True,
        )

        return sp.stdout.strip().split()[-1]

    def copy_from_windows(self) -> None:
        """
        Windows -> Linux
        """
        print("copying file from Windows")

        # check if dir exists in win
        if not self.win_save_folder.exists():
            mounted = self._try_mount_win_device(self.device)
            if not mounted:
                print(f"windows save folder not found at {self.win_save_folder}")
                sys.exit()

        # create backup
        timestamp = arrow.now().format("YYYY-MM-DDTHH-mm-ss")
        with tarfile.open(Path(f"./backups/backup_win_{timestamp}.tar"), "w:gz") as tar:
            tar.add(self.win_save_folder, recursive=True)

        # copy and overwrite
        copytree(self.win_save_folder, self.linux_steam_save_folder, dirs_exist_ok=True)

        print("> done")

    def copy_from_linux(self) -> None:
        """
        Linux -> Windows
        """
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

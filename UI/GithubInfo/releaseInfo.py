import os
from pathlib import Path
from typing import Optional

import requests
from packaging import version

from PySide6.QtWidgets import QMessageBox, QProgressDialog

from Module import platformutils
from Module.version import LOCAL_UI_VERSION

WINDOWS_ASSET_NAME = "KH2.Randomizer.exe"
LINUX_ASSET_NAME = "KH2.Randomizer-x86_64.AppImage"


def _is_platform_asset(asset_name: str) -> bool:
    """True if a release asset is the download for the current platform."""
    if platformutils.is_windows():
        return asset_name == WINDOWS_ASSET_NAME
    else:
        return asset_name == LINUX_ASSET_NAME


def update_install_target() -> Optional[Path]:
    """
    Where a downloaded update gets installed, or None if self-updating isn't possible
    (on Linux, only an AppImage can replace itself; a source checkout updates via git).
    """
    if platformutils.is_windows():
        return Path(WINDOWS_ASSET_NAME).absolute()
    else:
        return platformutils.appimage_path()


class GithubReleaseInfo:
    def __init__(self, info_json):
        self.notes = info_json["body"]
        self.prerelease = info_json["prerelease"]
        self.draft = info_json["draft"]
        self.version_tag = info_json["tag_name"]
        if "v" in self.version_tag:
            self.version_tag = self.version_tag.replace("v","")
        self.version = version.parse(self.version_tag)
        self.download_link = None
        self.updated_time = None
        matching_assets = [asset for asset in info_json["assets"] if _is_platform_asset(asset["name"])]
        if len(matching_assets) == 1:
            asset = matching_assets[0]
            self.download_link = asset["browser_download_url"]
            self.updated_time = asset["updated_at"]

    def download_release(self):
        if self.download_link is None:
            message = QMessageBox(text="This release does not contain an update for this platform.")
            message.setWindowTitle("KH2 Seed Generator")
            message.exec()
            return False

        target = update_install_target()
        if target is None:
            message = QMessageBox(text=(
                "The seed generator can't update itself when running from source."
                " Update your checkout (for example, with git pull) instead."
            ))
            message.setWindowTitle("KH2 Seed Generator")
            message.exec()
            return False

        temp_target = target.parent / (target.name + ".tmp")

        progress = QProgressDialog(
            f"Downloading version {self.version}", None, 0, 100, None
        )
        progress.setWindowTitle("Downloading...")
        progress.setModal(True)
        progress.show()
        try:
            with requests.get(self.download_link, stream=True, timeout=(5, 60)) as response:
                response.raise_for_status()
                content_length = response.headers.get("Content-Length")
                num_bytes = int(content_length) if content_length is not None else None
                bytes_downloaded = 0
                with open(temp_target, mode="wb") as file:
                    release_chunk_size = 50 * 1024
                    for chunk in response.iter_content(chunk_size=release_chunk_size):
                        if not chunk:
                            continue
                        bytes_downloaded += len(chunk)
                        if num_bytes:
                            progress.setValue(min(100, int(bytes_downloaded * 100.0 / num_bytes)))
                        file.write(chunk)
            if num_bytes is not None and bytes_downloaded != num_bytes:
                raise IOError(f"Expected {num_bytes} bytes but downloaded {bytes_downloaded}.")
            if bytes_downloaded == 0:
                raise IOError("The downloaded release asset was empty.")
            if not platformutils.is_windows():
                os.chmod(temp_target, 0o755)
            os.replace(temp_target, target)
            return True
        except (OSError, requests.RequestException, ValueError) as error:
            try:
                temp_target.unlink(missing_ok=True)
            except OSError:
                pass
            message = QMessageBox(text=f"The update could not be installed:\n{error}")
            message.setWindowTitle("KH2 Seed Generator")
            message.exec()
            return False
        finally:
            progress.close()

    def __str__(self):
        return f"{self.version} {self.updated_time} : {self.notes}"

class KH2RandomizerGithubReleases:
    def __init__(self):
        self.infos = []
        self.potential_updates = []
        try:
            response = requests.get("https://api.github.com/repos/tommadness/KH2Randomizer/releases",timeout=5)
            if response.ok:
                for release_info in response.json():
                    self.infos.append(GithubReleaseInfo(release_info))
                # get info about current generator version
                # THIS LINE IS FOR TESTING PURPOSES ONLY
                # self.current_version = version.parse("2.2.0")
                self.current_version = version.parse(LOCAL_UI_VERSION)
                # if we have a version that is higher than current version and has a
                # download for this platform, add it to update list
                for info in self.infos:
                    if self.current_version < info.version and info.download_link is not None:
                        self.potential_updates.append(info)
        except:
            # not doing anything if we can't connect to internet or other error occurs
            pass
    def get_update_infos(self):
        return self.potential_updates

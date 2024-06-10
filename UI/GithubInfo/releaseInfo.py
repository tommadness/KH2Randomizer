import os
import requests
from packaging import version

from PySide6.QtWidgets import QProgressDialog

from Module.version import LOCAL_UI_VERSION

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
        for asset in info_json["assets"]:
            if ".exe" in asset["name"]:
                self.download_link = asset["browser_download_url"]
                self.updated_time = asset["updated_at"]

    def download_release(self):
        progress = QProgressDialog(
            f"Downloading version {self.version}", None, 0, 100, None
        )
        progress.setWindowTitle("Downloading...")
        progress.setModal(True)
        progress.show()
        with requests.get(self.download_link, stream=True) as response:
            num_bytes = int(response.headers["Content-Length"])
            bytes_downloaded = 0
            with open("KH2.Randomizer.exe.tmp", mode="wb") as file:
                release_chunk_size = 50 * 1024
                for chunk in response.iter_content(chunk_size=release_chunk_size):
                    bytes_downloaded += release_chunk_size
                    progress.setValue(bytes_downloaded*100.0/num_bytes)
                    file.write(chunk)
        os.replace("KH2.Randomizer.exe.tmp", "KH2.Randomizer.exe")
        progress.close()
        return True
    
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
                # if we have a version that is higher than current version, add it to update list
                for info in self.infos:
                    if self.current_version < info.version:
                        self.potential_updates.append(info)
        except:
            # not doing anything if we can't connect to internet or other error occurs
            pass
    def get_update_infos(self):
        return self.potential_updates
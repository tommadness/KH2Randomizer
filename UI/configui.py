from pathlib import Path

from PySide6.QtWidgets import QFileDialog

from Module import appconfig
from Module.cosmetics import CosmeticsMod
from UI.qtlib import show_alert


CUSTOM_MUSIC_NOT_CHOSEN = "Custom Music Folder has not been chosen."
CUSTOM_VISUALS_NOT_CHOSEN = "Custom Visuals Folder has not been chosen."
OPENKH_LOCATION_NOT_CHOSEN = "OpenKH installation location has not been chosen."


def openkh_folder_getter() -> bool:
    save_file_widget = QFileDialog()
    selected_directory = save_file_widget.getExistingDirectory(caption="Select OpenKH Folder")

    if selected_directory is None or selected_directory == "":
        return False

    selected_path = Path(selected_directory)
    if not (selected_path / "OpenKh.Tools.ModsManager.exe").is_file():
        show_alert("Not a valid OpenKH folder.")
        return False
    else:
        appconfig.write_openkh_path(selected_directory)
        return True


def custom_music_folder_getter() -> bool:
    save_file_widget = QFileDialog()
    selected_directory = save_file_widget.getExistingDirectory(caption="Select Custom Music Folder")

    if selected_directory is None or selected_directory == "":
        return False

    CosmeticsMod.bootstrap_custom_music_folder(Path(selected_directory))
    appconfig.write_custom_music_path(selected_directory)
    return True


def custom_visuals_folder_getter() -> bool:
    save_file_widget = QFileDialog()
    selected_directory = save_file_widget.getExistingDirectory(caption="Select Custom Visuals Folder")

    if selected_directory is None or selected_directory == "":
        return False

    CosmeticsMod.bootstrap_custom_visuals_folder(Path(selected_directory))
    appconfig.write_custom_visuals_path(selected_directory)
    return True

import json
import os
import shutil
import string
from pathlib import Path
from typing import Any, Optional

from PySide6.QtWidgets import QWidget, QInputDialog, QLineEdit, QMessageBox, QDialog, QGridLayout, QListWidget, \
    QPushButton, QFileDialog

from Class.exceptions import SettingsException
from Class.seedSettings import SeedSettings
from Module import appconfig
from Module.resources import resource_path


class SettingsPreset:

    def __init__(self, display_name: str, file_path: Path, bundled: bool):
        super().__init__()
        self.display_name = display_name
        self.file_path = file_path
        self.bundled = bundled
        self.cached_json: Optional[dict[str, Any]] = None

    def settings_json(self) -> dict[str, Any]:
        cached = self.cached_json
        if cached is None:
            with open(self.file_path) as preset_data:
                loaded_json = json.load(preset_data)
                self.cached_json = loaded_json
                return loaded_json
        else:
            return cached


def _list_presets(path: Path, bundled: bool) -> list[SettingsPreset]:
    result: list[SettingsPreset] = []
    if not path.is_dir():
        return result

    for preset_file_name in os.listdir(path):
        preset_name, extension = os.path.splitext(preset_file_name)
        if extension == ".json":
            preset_file = path / preset_file_name
            result.append(SettingsPreset(display_name=preset_name, file_path=preset_file, bundled=bundled))
    return result


def _bundled_presets_path() -> Path:
    return Path(resource_path("static/bundled_presets"))


def bootstrap_presets():
    """Creates the user presets folder if needed and cleans up old copies of bundled presets."""
    presets_folder = appconfig.settings_presets_folder()
    if not presets_folder.is_dir():
        presets_folder.mkdir(parents=True)
    else:
        bundled_preset_names = set(p.display_name for p in list_bundled_presets())
        for user_preset in list_user_presets():
            if user_preset.display_name in bundled_preset_names:
                print(f"Deleting extra copy of bundled preset [{user_preset.display_name}] from user presets")
                user_preset.file_path.unlink()


def list_user_presets() -> list[SettingsPreset]:
    return _list_presets(appconfig.settings_presets_folder(), bundled=False)


def list_bundled_presets() -> list[SettingsPreset]:
    return _list_presets(_bundled_presets_path(), bundled=True)


def bundled_starter_preset() -> SettingsPreset:
    preset_name = "StarterSettings"
    preset = next((p for p in list_bundled_presets() if p.display_name == preset_name), None)
    if preset is None:
        raise SettingsException(f"Bundled {preset_name} preset not found")
    else:
        return preset


def prompt_save_preset(parent: QWidget, settings: SeedSettings) -> bool:
    """Prompts the user to save the current preset. Returns true if saved."""
    message = "Enter a name for your preset"
    preset_name, ok = QInputDialog.getText(parent, "New Preset", message, QLineEdit.EchoMode.Normal)
    if not ok:
        return False

    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    preset_name = "".join(c for c in preset_name if c in valid_chars)

    if preset_name in set(p.display_name for p in list_bundled_presets()):
        message = QMessageBox(text=f"The name [{preset_name}] is already in use by a bundled preset.")
        message.setWindowTitle("KH2 Seed Generator")
        message.exec()
        return False

    with open(appconfig.settings_presets_folder() / f"{preset_name}.json", "w") as preset_file:
        json.dump(settings.settings_json(), preset_file, indent=4, sort_keys=True)

    return True


def prompt_import_preset(parent: QWidget) -> Optional[str]:
    """Prompts the user to import a preset. Returns the preset name if imported, or None if not."""
    chosen_file, _ = QFileDialog.getOpenFileName(parent, filter="Settings Preset (*.json)")
    if chosen_file:
        preset_file = Path(chosen_file)
        preset_name = preset_file.stem

        if preset_name in set(p.display_name for p in list_bundled_presets()):
            message = QMessageBox(text=f"The name [{preset_name}] is already in use by a bundled preset.")
            message.setWindowTitle("KH2 Seed Generator")
            message.exec()
            return None

        shutil.copy2(preset_file, appconfig.settings_presets_folder())
        return preset_name
    else:
        return None


class RandomPresetDialog(QDialog):

    def __init__(self, preset_list: list[SettingsPreset]):
        super().__init__()
        self.preset_list = preset_list
        self.setWindowTitle("Randomly Pick a Preset")
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)

        box = QGridLayout()

        self.preset_list_widget = QListWidget(self)
        self.preset_list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for preset in preset_list:
            self.preset_list_widget.addItem(preset.display_name)

        select_all_button = QPushButton("Select All Presets")
        select_all_button.clicked.connect(self._select_all_presets_from_list)

        cancel_button = QPushButton("Cancel")
        choose_button = QPushButton("Randomly Pick From Selected Presets")
        cancel_button.clicked.connect(self.reject)
        choose_button.clicked.connect(self.accept)

        box.addWidget(self.preset_list_widget, 0, 0)
        box.addWidget(choose_button, 0, 1)
        box.addWidget(select_all_button, 1, 0)
        box.addWidget(cancel_button, 1, 1)

        self.setLayout(box)

    def _select_all_presets_from_list(self):
        for index in range(self.preset_list_widget.count()):
            self.preset_list_widget.item(index).setSelected(True)

    def save(self) -> list[SettingsPreset]:
        result: list[SettingsPreset] = []
        for index in self.preset_list_widget.selectedIndexes():
            result.append(self.preset_list[index.row()])
        return result

import json
from pathlib import Path
from typing import Optional

import yaml

AUTOSAVE_FOLDER = "auto-save"
PRESET_FOLDER = "presets"


def read_app_config() -> dict:
    config_path = Path('randomizer-config.json').absolute()
    if config_path.is_file():
        with open(config_path, encoding='utf-8') as config_file:
            return json.load(config_file)
    else:
        return {}

def read_boss_enemy_override_files() -> str:
    result_string = ""
    location_override_path = Path('override_enemies.yaml').absolute()
    if location_override_path.is_file():
        with open(location_override_path, encoding='utf-8') as location_override:
            result_string += location_override.read()
    enemy_override_path = Path('override_enemies.yaml').absolute()
    if enemy_override_path.is_file():
        with open(enemy_override_path, encoding='utf-8') as enemy_override:
            result_string += enemy_override.read()
    return result_string
            

def write_app_config(config: dict):
    config_path = Path('randomizer-config.json').absolute()
    with open(config_path, mode='w', encoding='utf-8') as config_file:
        json.dump(config, config_file, indent=4)


def update_app_config(key: str, value):
    randomizer_config = read_app_config()
    randomizer_config[key] = value
    write_app_config(randomizer_config)


def remove_app_config(key: str):
    randomizer_config = read_app_config()
    if key in randomizer_config:
        del randomizer_config[key]
        write_app_config(randomizer_config)


def auto_save_folder() -> Path:
    return Path(AUTOSAVE_FOLDER)


def read_openkh_path() -> Optional[Path]:
    randomizer_config = read_app_config()
    openkh_path = Path(randomizer_config.get('openkh_folder', 'to-nowhere'))
    if openkh_path.is_dir():
        return openkh_path
    else:
        return None


def write_openkh_path(selected_directory):
    update_app_config('openkh_folder', selected_directory)


def read_custom_music_path() -> Optional[Path]:
    randomizer_config = read_app_config()
    custom_music_path = Path(randomizer_config.get('custom_music_folder', 'to-nowhere'))
    if custom_music_path.is_dir():
        return custom_music_path
    else:
        return None


def write_custom_music_path(selected_directory):
    update_app_config('custom_music_folder', selected_directory)


def read_custom_visuals_path() -> Optional[Path]:
    randomizer_config = read_app_config()
    custom_visuals_path = Path(randomizer_config.get('custom_visuals_folder', 'to-nowhere'))
    if custom_visuals_path.is_dir():
        return custom_visuals_path
    else:
        return None


def write_custom_visuals_path(selected_directory):
    update_app_config('custom_visuals_folder', selected_directory)


def extracted_data_path() -> Optional[Path]:
    """Returns the path to extracted game data."""
    openkh_path = read_openkh_path()
    if openkh_path is None:
        return None

    mods_manager_yml_path = openkh_path / "mods-manager.yml"
    if not mods_manager_yml_path.is_file():
        return None

    with open(mods_manager_yml_path, encoding="utf-8") as mod_manager_file:
        mod_manager_yaml = yaml.safe_load(mod_manager_file)
        game_data_path = mod_manager_yaml.get("gameDataPath", "to-nowhere")
        extracted_data = Path(game_data_path)
        if extracted_data.is_dir():
            return extracted_data
        else:
            return None

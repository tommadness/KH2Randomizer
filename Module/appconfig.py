import json
from pathlib import Path


def read_app_config() -> dict:
    config_path = Path('randomizer-config.json').absolute()
    if config_path.is_file():
        with open(config_path, encoding='utf-8') as config_file:
            return json.load(config_file)
    else:
        return {}


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

import json
from pathlib import Path


class CustomCosmetics:

    def __init__(self):
        super().__init__()

        config_path = Path('auto-save') / 'custom-cosmetics.json'
        self.config_path = config_path
        self.external_executables: list[str] = []

        if config_path.is_file():
            with open(config_path, encoding='utf-8') as config_file:
                raw_json: dict = json.load(config_file)
                self.external_executables = raw_json.get('external_executables', [])

    def add_custom_executable(self, path_str: str):
        self.external_executables.append(path_str)

    def remove_at_index(self, index: int):
        del self.external_executables[index]

    def write_file(self):
        with open(self.config_path, 'w', encoding='utf-8') as config_file:
            raw_json = {
                'external_executables': self.external_executables
            }
            json.dump(raw_json, config_file, indent=4)

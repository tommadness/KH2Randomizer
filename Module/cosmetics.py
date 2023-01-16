import json
import os
import random
import shutil
from pathlib import Path
from typing import Optional

import yaml

from Class import settingkey
from Class.seedSettings import SeedSettings
from Module.RandomizerSettings import RandomizerSettings
from Module.music import default_music_list
from Module.resources import resource_path


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


class CosmeticsMod:

    @staticmethod
    def cosmetics_mod_path(openkh_path: Path, create_if_missing: bool) -> Optional[Path]:
        """Returns the path to the cosmetics mod (within OpenKH `mods` folder)."""
        cosmetics_mod_path = openkh_path / 'mods' / 'kh2' / 'KH2Randomizer-Cosmetics-PC'
        if create_if_missing:
            cosmetics_mod_path.mkdir(parents=True, exist_ok=True)
        if cosmetics_mod_path.is_dir():
            return cosmetics_mod_path
        else:
            return None

    @staticmethod
    def extracted_data_path() -> Optional[Path]:
        """Returns the path to extracted kh2 data"""
        openkh_path = CosmeticsMod.read_openkh_path()
        with open(openkh_path / "mods-manager.yml", mode="r") as mod_manager_file:
            mod_manager_yaml = yaml.safe_load(mod_manager_file)
            extracted_data_path = Path(mod_manager_yaml["gameDataPath"])
            if extracted_data_path.is_dir():
                return extracted_data_path
            else:
                return None

    @staticmethod
    def bootstrap_mod():
        """Creates any empty folders and default files needed for the cosmetics mod."""
        openkh_path = CosmeticsMod.read_openkh_path()
        if openkh_path is None:
            raise Exception('OpenKH path not found')

        cosmetics_mod_path = CosmeticsMod.cosmetics_mod_path(openkh_path, create_if_missing=True)

        music_path = cosmetics_mod_path / 'music'

        # Create empty default music folders if needed
        if not music_path.is_dir():
            music_path.mkdir(parents=True)
            for folder in ['battle', 'boss', 'cutscene', 'field', 'title', 'wild', 'your-own-category']:
                (music_path / folder).mkdir()

        # Create a default music config file if needed
        music_list_file_path = cosmetics_mod_path / 'musiclist.json'
        if not music_list_file_path.is_file():
            with open(music_list_file_path, mode='w', encoding='utf-8') as music_list_file:
                json.dump(default_music_list, music_list_file, indent=4)

        mod_yml_path = cosmetics_mod_path / 'mod.yml'
        if not mod_yml_path.is_file():
            with open(mod_yml_path, 'w', encoding='utf-8') as mod_yml_file:
                mod_yml = CosmeticsMod._get_mod_yml(cosmetics_mod_path, settings=None)
                yaml.dump(mod_yml, mod_yml_file, encoding='utf-8')

        icon_path = cosmetics_mod_path / 'icon.png'
        if not icon_path.is_file():
            resource = Path(resource_path('UI/Submenus/icons/misc/concert.png'))
            shutil.copyfile(src=resource, dst=icon_path)

    @staticmethod
    def randomize_cosmetics(settings: RandomizerSettings):
        music_rando_enabled = settings.ui_settings.get(settingkey.MUSIC_RANDO_ENABLED_PC)
        if not music_rando_enabled:
            return

        openkh_path = CosmeticsMod.read_openkh_path()
        if openkh_path is None:
            return

        CosmeticsMod.bootstrap_mod()
        cosmetics_mod_path = CosmeticsMod.cosmetics_mod_path(openkh_path, create_if_missing=False)

        with open(cosmetics_mod_path / 'mod.yml', 'w', encoding='utf-8') as mod_yml_file:
            mod_yml = CosmeticsMod._get_mod_yml(cosmetics_mod_path, settings.ui_settings)
            yaml.dump(mod_yml, mod_yml_file, encoding='utf-8')

    @staticmethod
    def get_music_summary() -> dict[str, int]:
        openkh_path = CosmeticsMod.read_openkh_path()
        if openkh_path is None:
            return {}

        cosmetics_mod_path = openkh_path / 'mods' / 'kh2' / 'KH2Randomizer-Cosmetics-PC'
        music_files = CosmeticsMod._collect_music_files(cosmetics_mod_path)

        return {category: len(song_list) for category, song_list in music_files.items()}

    @staticmethod
    def _collect_music_files(cosmetics_mod_path: Path) -> dict[str, list[Path]]:
        """Returns music files grouped by category, based on what folder they reside."""
        result: dict[str, list[Path]] = {}
        music_path = cosmetics_mod_path / 'music'
        if not music_path.is_dir():
            return result

        for child in [str(category_file).lower() for category_file in os.listdir(music_path)]:
            child_path = music_path / child
            if child_path.is_dir():
                category_songs: list[Path] = []
                for root, dirs, files in os.walk(child_path):
                    root_path = Path(root)
                    for file in files:
                        _, extension = os.path.splitext(file)
                        if extension.lower() == '.scd':
                            relative_path = (root_path / file).relative_to(cosmetics_mod_path)
                            category_songs.append(relative_path)
                result[child] = category_songs
        
        default_music_path = CosmeticsMod.extracted_data_path() / "kh2"
        if default_music_path.is_dir():
            for default_song in default_music_list:
                relative_path = default_music_path / default_song["filename"]
                result[default_song["type"][0].lower()].append(relative_path)
        

        return result

    @staticmethod
    def _get_mod_yml(cosmetics_mod_path: Path, settings: Optional[SeedSettings]) -> dict:
        raw_yaml = {
            'title': 'KH2 Randomizer Cosmetics (PC only)',
            'description': 'Contains randomized cosmetics from the KH2 Randomizer seed generator.'
        }

        assets = []
        if settings is not None:
            assets += CosmeticsMod._get_music_assets(cosmetics_mod_path, settings)

        raw_yaml['assets'] = assets
        return raw_yaml

    @staticmethod
    def _get_music_assets(cosmetics_mod_path: Path, settings: SeedSettings) -> list[dict]:
        music_list_file_path = cosmetics_mod_path / 'musiclist.json'

        allow_duplicates = settings.get(settingkey.MUSIC_RANDO_PC_ALLOW_DUPLICATES)

        # Primary copy of the music. Songs are removed as they are chosen.
        music_files_by_categories: dict[str, list[Path]] = {}
        # Secondary copy of the music. Used to refill the lists once all are gone.
        backup_files_by_categories: dict[str, list[Path]] = {}

        music_files = CosmeticsMod._collect_music_files(cosmetics_mod_path)
        for category, song_list in music_files.items():
            main_list = song_list.copy()
            random.shuffle(main_list)
            music_files_by_categories[category] = main_list

            backup_files_by_categories[category] = song_list

        assets = []
        replacements = {}

        with open(music_list_file_path, encoding='utf-8') as music_list_file:
            music_metadata = json.load(music_list_file)
        for info in music_metadata:
            filename = info['filename']
            title = info['title']
            types = [song_type.lower() for song_type in info['type'] if song_type.lower() in music_files_by_categories]
            if len(types) > 0:
                random.shuffle(types)

                for chosen_type in types:
                    songs_for_chosen_type = music_files_by_categories[chosen_type]

                    # If there aren't any songs left for the type, attempt to refill the list if duplicates are allowed.
                    # If duplicates are not allowed and we run out of replacements, more will end up un-randomized.
                    if len(songs_for_chosen_type) == 0 and allow_duplicates:
                        refill_list = backup_files_by_categories[chosen_type].copy()
                        random.shuffle(refill_list)
                        music_files_by_categories[chosen_type] = refill_list
                        songs_for_chosen_type = refill_list

                    if len(songs_for_chosen_type) > 0:
                        chosen_song = str(songs_for_chosen_type.pop())

                        asset = {
                            'name': filename,
                            'vanilla_song': title,
                            'song_type': chosen_type,
                            'method': 'copy',
                            'source': [{'name': chosen_song}]
                        }
                        assets.append(asset)

                        replacements[title] = chosen_song

                        break

        spoiler_path = cosmetics_mod_path / 'music-replacement-list.txt'
        with open(spoiler_path, mode='w', encoding='utf-8') as spoiler_file:
            for original, replacement in replacements.items():
                spoiler_file.write('[{}] was replaced by [{}]\n'.format(original, replacement))

        return assets

    @staticmethod
    def read_openkh_path() -> Optional[Path]:
        config_path = Path("randomizer-config.json").absolute()
        if config_path.is_file():
            with open(config_path, encoding='utf-8') as music_config:
                raw_json = json.load(music_config)
                openkh_path = Path(raw_json.get('openkh_folder', 'to-nowhere'))
                if openkh_path.is_dir():
                    return openkh_path
        return None

    @staticmethod
    def write_openkh_path(selected_directory):
        config_path = Path("randomizer-config.json").absolute()
        with open(config_path, mode='w', encoding='utf-8') as music_config:
            out_data = {'openkh_folder': selected_directory}
            json.dump(out_data, music_config, indent=4)

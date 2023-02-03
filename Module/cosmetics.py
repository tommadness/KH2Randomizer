import json
import os
import random
from pathlib import Path
from typing import Optional, Tuple

import yaml

from Class import settingkey
from Class.seedSettings import SeedSettings
from Module import appconfig, music
from Module.RandomizerSettings import RandomizerSettings


class CustomCosmetics:

    def __init__(self):
        super().__init__()

        config_path = Path('auto-save') / 'custom-cosmetics.json'
        self.config_path = config_path
        self.external_executables: list[str] = []

        if config_path.is_file():
            with open(config_path, encoding='utf-8') as config_file:
                try:
                    raw_json: dict = json.load(config_file)
                    self.external_executables = raw_json.get('external_executables', [])
                except Exception:
                    print('Error decoding custom-cosmetics.json, using empty list of external executables')

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
    def extracted_data_path() -> Optional[Path]:
        """Returns the path to extracted game data"""
        openkh_path = CosmeticsMod.read_openkh_path()
        if openkh_path is None:
            return None

        mods_manager_yml_path = openkh_path / 'mods-manager.yml'
        if not mods_manager_yml_path.is_file():
            return None

        with open(mods_manager_yml_path, encoding='utf-8') as mod_manager_file:
            mod_manager_yaml = yaml.safe_load(mod_manager_file)
            game_data_path = mod_manager_yaml.get('gameDataPath', 'to-nowhere')
            extracted_data_path = Path(game_data_path)
            if extracted_data_path.is_dir():
                return extracted_data_path
            else:
                return None

    @staticmethod
    def bootstrap_music_list_file() -> Path:
        """Creates the musiclist file if needed."""
        music_list_file_path = Path('musiclist.json')
        if not music_list_file_path.is_file():
            with open(music_list_file_path, mode='w', encoding='utf-8') as music_list_file:
                json.dump(music.kh2_music_list, music_list_file, indent=4)
        return music_list_file_path

    @staticmethod
    def bootstrap_custom_music_folder(custom_music_path: Path):
        """Creates folders for each of the default music categories."""
        for folder in ['atlantica', 'battle', 'boss', 'cutscene', 'field', 'title', 'wild']:
            (custom_music_path / folder).mkdir(exist_ok=True)

    @staticmethod
    def randomize_music(settings: RandomizerSettings) -> Tuple[list[dict], dict[str, str]]:
        """
        Randomizes music, returning a list of assets to be added to the seed mod and a dictionary of which song was
        replaced by which replacement.
        """
        return CosmeticsMod._get_music_assets(settings.ui_settings)

    @staticmethod
    def get_music_summary(settings: SeedSettings) -> dict[str, int]:
        music_files = CosmeticsMod._collect_music_files(settings)

        return {category: len(song_list) for category, song_list in music_files.items()}

    @staticmethod
    def _collect_music_files(settings: SeedSettings) -> dict[str, list[Path]]:
        """Returns music files grouped by category."""
        result: dict[str, list[Path]] = {}

        categorize = settings.get(settingkey.MUSIC_RANDO_PC_USE_CATEGORIES)
        dmca_safe = settings.get(settingkey.MUSIC_RANDO_PC_DMCA_SAFE)

        if settings.get(settingkey.MUSIC_RANDO_PC_INCLUDE_CUSTOM):
            custom_music_path = CosmeticsMod.read_custom_music_path()
            if custom_music_path is not None:
                for child in [str(category_file).lower() for category_file in os.listdir(custom_music_path)]:
                    child_path = custom_music_path / child
                    if child_path.is_dir():
                        category_songs: list[Path] = []
                        for root, dirs, files in os.walk(child_path):
                            root_path = Path(root)
                            for file in files:
                                _, extension = os.path.splitext(file)
                                if extension.lower() == '.scd':
                                    file_path = root_path / file
                                    category_songs.append(file_path)
                        resolved_category = child
                        if not categorize:
                            resolved_category = 'wild'
                        if resolved_category not in result:
                            result[resolved_category] = []
                        result[resolved_category] += category_songs

        extracted_data_path = CosmeticsMod.extracted_data_path()
        if extracted_data_path is not None:
            def add_game_song(song_file_path: Path, category: str, song_dmca: bool):
                if not categorize:
                    category = 'wild'
                if category not in result:
                    result[category] = []
                if not dmca_safe or not song_dmca:
                    result[category].append(song_file_path)

            if settings.get(settingkey.MUSIC_RANDO_PC_INCLUDE_KH2):
                kh2_path = extracted_data_path / 'kh2'
                if kh2_path.is_dir():
                    for kh2_song in music.kh2_music_list:
                        add_game_song(
                            song_file_path=kh2_path / kh2_song['filename'],
                            category=kh2_song['type'][0].lower(),
                            song_dmca=kh2_song.get('dmca', False)
                        )

            def add_other_game_music(enabled_key: str, game_music_path: Path, game_music_list: list):
                if settings.get(enabled_key) and game_music_path.is_dir():
                    for song in game_music_list:
                        add_game_song(
                            song_file_path=game_music_path / song['name'],
                            category=song['kind'],
                            song_dmca=song.get('dmca', False)
                        )
            add_other_game_music(
                enabled_key=settingkey.MUSIC_RANDO_PC_INCLUDE_KH1,
                game_music_path=extracted_data_path / 'kh1' / 'remastered' / 'amusic',
                game_music_list=music.kh1_music_list
            )
            add_other_game_music(
                enabled_key=settingkey.MUSIC_RANDO_PC_INCLUDE_RECOM,
                game_music_path=extracted_data_path / 'recom' / 'STREAM' / '0001',
                game_music_list=music.recom_music_list
            )
            add_other_game_music(
                enabled_key=settingkey.MUSIC_RANDO_PC_INCLUDE_BBS,
                game_music_path=extracted_data_path / 'bbs' / 'sound' / 'win' / 'bgm',
                game_music_list=music.bbs_music_list
            )

        return result

    @staticmethod
    def _get_music_assets(settings: SeedSettings) -> Tuple[list[dict], dict[str, str]]:
        music_rando_enabled = settings.get(settingkey.MUSIC_RANDO_ENABLED_PC)
        if not music_rando_enabled:
            return [], {}

        allow_duplicates = settings.get(settingkey.MUSIC_RANDO_PC_ALLOW_DUPLICATES)

        # Primary copy of the music. Songs are removed as they are chosen.
        music_files_by_categories: dict[str, list[Path]] = {}
        # Secondary copy of the music. Used to refill the lists once all are gone.
        backup_files_by_categories: dict[str, list[Path]] = {}

        music_files = CosmeticsMod._collect_music_files(settings)
        for category, song_list in music_files.items():
            main_list = song_list.copy()
            random.shuffle(main_list)
            music_files_by_categories[category] = main_list

            backup_files_by_categories[category] = song_list

        assets = []
        replacements: dict[str, str] = {}

        music_list_file_path = CosmeticsMod.bootstrap_music_list_file()
        with open(music_list_file_path, encoding='utf-8') as music_list_file:
            music_metadata = json.load(music_list_file)
        random.shuffle(music_metadata)
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

        return assets, replacements

    @staticmethod
    def read_openkh_path() -> Optional[Path]:
        randomizer_config = appconfig.read_app_config()
        openkh_path = Path(randomizer_config.get('openkh_folder', 'to-nowhere'))
        if openkh_path.is_dir():
            return openkh_path
        else:
            return None

    @staticmethod
    def write_openkh_path(selected_directory):
        appconfig.update_app_config('openkh_folder', selected_directory)

    @staticmethod
    def read_custom_music_path() -> Optional[Path]:
        randomizer_config = appconfig.read_app_config()
        custom_music_path = Path(randomizer_config.get('custom_music_folder', 'to-nowhere'))
        if custom_music_path.is_dir():
            return custom_music_path
        else:
            return None

    @staticmethod
    def write_custom_music_path(selected_directory):
        appconfig.update_app_config('custom_music_folder', selected_directory)

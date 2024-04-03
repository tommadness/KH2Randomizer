import os
import random
from pathlib import Path

from Class.openkhmod import Asset
from List import configDict
from Module import appconfig


class EndingPictureRandomizer:

    @staticmethod
    def endingpic_rando_options() -> dict[str, str]:
        return {
            configDict.VANILLA: "Vanilla",
            configDict.RANDOMIZE_IN_GAME_ONLY: "Randomize (in-game only)",
            configDict.RANDOMIZE_CUSTOM_ONLY: "Randomize (custom only)",
            configDict.RANDOMIZE_ALL: "Randomize (in-game + custom)",
        }

    @staticmethod
    def randomize_end_screen(setting: str) -> list[Asset]:
        """Randomizes the ending screen, returning a list of assets to be added to a mod."""

        assets: list[Asset] = []
        if setting == configDict.VANILLA:
            return assets

        vanilla_by_locale: dict[str, list[str]] = {
            "fr": [
                "remastered/menu/fr/ending.2ld/FR_ending_2ld2.png",
                "remastered/menu/fr/ending.2ld/FR_ending_2ld3.png",
                "remastered/menu/fr/ending.2ld/FR_ending_2ld4.png",
                "remastered/menu/fr/ending.2ld/FR_ending_2ld5.png",
                "remastered/menu/fr/ending.2ld/FR_ending_2ld6.png",
                "remastered/menu/fr/ending.2ld/FR_ending_2ld7.png",
            ],
            "gr": [
                "remastered/menu/gr/ending.2ld/GR_ending_2ld2.png",
                "remastered/menu/gr/ending.2ld/GR_ending_2ld3.png",
                "remastered/menu/gr/ending.2ld/GR_ending_2ld4.png",
                "remastered/menu/gr/ending.2ld/GR_ending_2ld5.png",
                "remastered/menu/gr/ending.2ld/GR_ending_2ld6.png",
                "remastered/menu/gr/ending.2ld/GR_ending_2ld7.png",
            ],
            "it": [
                "remastered/menu/it/ending.2ld/IT_ending_2ld2.png",
                "remastered/menu/it/ending.2ld/IT_ending_2ld3.png",
                "remastered/menu/it/ending.2ld/IT_ending_2ld4.png",
                "remastered/menu/it/ending.2ld/IT_ending_2ld5.png",
                "remastered/menu/it/ending.2ld/IT_ending_2ld6.png",
                "remastered/menu/it/ending.2ld/IT_ending_2ld7.png",
            ],
            "sp": [
                "remastered/menu/sp/ending.2ld/SP_ending_2ld2.png",
                "remastered/menu/sp/ending.2ld/SP_ending_2ld3.png",
                "remastered/menu/sp/ending.2ld/SP_ending_2ld4.png",
                "remastered/menu/sp/ending.2ld/SP_ending_2ld5.png",
                "remastered/menu/sp/ending.2ld/SP_ending_2ld6.png",
                "remastered/menu/sp/ending.2ld/SP_ending_2ld7.png",
            ],
            "us": [
                "remastered/menu/us/ending.2ld/US_ending_2ld2.png",
                "remastered/menu/us/ending.2ld/US_ending_2ld3.png",
                "remastered/menu/us/ending.2ld/US_ending_2ld4.png",
                "remastered/menu/us/ending.2ld/US_ending_2ld5.png",
                "remastered/menu/us/ending.2ld/US_ending_2ld6.png",
                "remastered/menu/us/ending.2ld/US_ending_2ld7.png",
            ],
        }

        custom = EndingPictureRandomizer._collect_custom_endpics()

        if setting == configDict.RANDOMIZE_ALL:
            if len(custom) == 0:
                # No custom ones, so fall back to in-game
                setting = configDict.RANDOMIZE_IN_GAME_ONLY
            else:
                # We're only choosing one in the end, so flip a coin to choose between in-game one or custom
                coinflip = random.randint(0, 1)
                if coinflip == 0:
                    setting = configDict.RANDOMIZE_IN_GAME_ONLY
                else:
                    setting = configDict.RANDOMIZE_CUSTOM_ONLY

        if setting == configDict.RANDOMIZE_IN_GAME_ONLY:
            for endpic_list in vanilla_by_locale.values():
                choice = random.choice(endpic_list)
                assets.append({
                    "name": endpic_list[0],
                    "platform": "pc",
                    "multi": [{"name": endpic} for endpic in endpic_list[1:]],
                    "method": "copy",
                    "source": [{
                        "name": choice,
                        "type": "internal",
                    }]
                })

        if setting == configDict.RANDOMIZE_CUSTOM_ONLY and len(custom) > 0:
            choice = random.choice(custom)
            for endpic_list in vanilla_by_locale.values():
                assets.append({
                    "name": endpic_list[0],
                    "platform": "pc",
                    "multi": [{"name": endpic} for endpic in endpic_list[1:]],
                    "method": "copy",
                    "source": [{"name": str(choice)}]
                })

        return assets

    @staticmethod
    def _collect_custom_endpics() -> list[Path]:
        result: list[Path] = []

        custom_visuals_path = appconfig.read_custom_visuals_path()
        if custom_visuals_path is not None:
            ending_pictures_path = custom_visuals_path / "ending-pictures"
            if ending_pictures_path.is_dir():
                for root, dirs, files in os.walk(ending_pictures_path):
                    root_path = Path(root)
                    for file in files:
                        name, extension = os.path.splitext(file)
                        if extension.lower() == ".png":
                            file_path = root_path / file
                            result.append(file_path)

        return result

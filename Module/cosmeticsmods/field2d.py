import os
import random
from pathlib import Path

from Class.openkhmod import Asset
from List import configDict
from Module import appconfig

AGRABAH = "al0"
BEAST_CASTLE = "bb0"
PORT_ROYAL = "ca0"
DISNEY_CASTLE = "dc0"
LINGERING_WILL = "dc1"
DESTINY_ISLANDS = "di0"
TWTNW = "eh0"
ROXAS = "eh1"
AGRABAH_ALT = "es0"
HOLLOW_BASTION = "hb0"
GARDEN_OF_ASSEMBLAGE = "hb1"
ABSENT_SILHOUETTE = "hb2"
OLYMPUS_COLISEUM = "he0"
UNDERWORLD = "he1"
PRIDE_LANDS = "lk0"
ATLANTICA = "lm0"
LAND_OF_DRAGONS = "mu0"
HALLOWEEN_TOWN = "nm0"
CHRISTMAS_TOWN = "nm1"
HUNDRED_ACRE_WOOD = "po0"
SPACE_PARANOIDS = "tr0"
TWILIGHT_TOWN = "tt0"
STATION_OF_CALLING = "tt1"
MYSTERIOUS_TOWER = "tt2"
MANSION_BASEMENT = "tt3"
WHITE_ROOM = "tt4"
MANSION = "tt5"
BETWIXT_BETWEEN = "tt6"
TIMELESS_RIVER = "wi0"
WORLD_MAP = "wm0"
KINGDOM_HEARTS_1 = "zz0"


class CommandMenuRandomizer:

    def __init__(self, command_menu_choice: str):
        super().__init__()
        self.command_menu_choice = command_menu_choice

    @staticmethod
    def command_menu_options() -> dict[str, str]:
        return {
            configDict.VANILLA: "Vanilla",
            configDict.RANDOMIZE_ONE: "Randomize (one)",
            configDict.RANDOMIZE_ALL: "Randomize (all)",
            AGRABAH: "Agrabah",
            BEAST_CASTLE: "Beast's Castle",
            PORT_ROYAL: "Port Royal",
            DISNEY_CASTLE: "Disney Castle",
            LINGERING_WILL: "Lingering Will",
            # DESTINY_ISLANDS: "Destiny Island",  # no visible difference from KH1
            TWTNW: "The World That Never Was",
            ROXAS: "Roxas Fight",  # looks like KH1 but with classic icons
            # AGRABAH_ALT: "Agrabah (alt),  # for carpet minigames? need to check for differences.
            HOLLOW_BASTION: "Hollow Bastion",
            GARDEN_OF_ASSEMBLAGE: "Garden of Assemblage",
            ABSENT_SILHOUETTE: "Absent Silhouette",
            OLYMPUS_COLISEUM: "Olympus Coliseum",
            UNDERWORLD: "The Underworld",
            PRIDE_LANDS: "Pride Lands",
            ATLANTICA: "Atlantica (PCSX2 Only)",
            LAND_OF_DRAGONS: "Land of Dragons",
            HALLOWEEN_TOWN: "Halloween Town",
            CHRISTMAS_TOWN: "Christmas Town",
            HUNDRED_ACRE_WOOD: "100 Acre Wood",
            SPACE_PARANOIDS: "Space Paranoids",
            TWILIGHT_TOWN: "Twilight Town",
            STATION_OF_CALLING: "Station of Calling",  # looks like kh1 but with classic icons.
            MYSTERIOUS_TOWER: "Mysterious Tower",
            MANSION_BASEMENT: "Mansion Basement",
            WHITE_ROOM: "The White Room",
            MANSION: "Mansion",
            BETWIXT_BETWEEN: "Betwixt & Between",
            TIMELESS_RIVER: "Timeless River",
            # WORLD_MAP: "World Map",  # no visible difference from Betwixt & Between
            KINGDOM_HEARTS_1: "Kingdom Hearts 1"
        }

    def randomize_command_menus(self) -> list[Asset]:
        if self.command_menu_choice == configDict.VANILLA:
            return []
        assets = []
        assets.extend(self._randomize_ps2())
        assets.extend(self._randomize_pc())
        return assets

    def _randomize_ps2(self) -> list[Asset]:
        menu_replacements = self._compute_menu_replacements(pc=False)
        assets: list[Asset] = []
        for old_menu, new_menu in menu_replacements.items():
            assets.append({
                "platform": "ps2",
                "name": f"field2d/jp/{old_menu}command.2dd",
                "multi": [
                    {"name": f"field2d/us/{old_menu}command.2dd"}
                ],
                "method": "copy",
                "source": [
                    {
                        "name": f"field2d/jp/{new_menu}command.2dd",
                        "type": "internal"
                    }
                ]
            })
        return assets

    def _randomize_pc(self) -> list[Asset]:
        menu_replacements = self._compute_menu_replacements(pc=True)
        assets: list[Asset] = []
        for old_menu, new_menu in menu_replacements.items():
            if new_menu == ATLANTICA:
                # Unsupported on PC - just leave it vanilla
                continue

            for region in ["fr", "gr", "it", "sp", "us"]:
                assets.append({
                    "platform": "pc",
                    "name": f"field2d/{region}/{old_menu}command.2dd",
                    "method": "copy",
                    "source": [
                        {
                            "name": f"field2d/{region}/{new_menu}command.2dd",
                            "type": "internal"
                        }
                    ]
                })

                remastered_region = f"remastered/field2d/{region}"
                cap_region = region.upper()
                assets.append({
                    "platform": "pc",
                    "name": f"{remastered_region}/{old_menu}command.2dd/{cap_region}_{old_menu}command_2dd0.png",
                    "method": "copy",
                    "source": [
                        {
                            "name": f"{remastered_region}/{new_menu}command.2dd/{cap_region}_{new_menu}command_2dd0.png",
                            "type": "internal"
                        }
                    ]
                })
        return assets

    def _compute_menu_replacements(self, pc: bool) -> dict[str, str]:
        unsupported = [configDict.VANILLA, configDict.RANDOMIZE_ONE, configDict.RANDOMIZE_ALL]
        if pc:
            unsupported.append(ATLANTICA)
        supported_menus = [menu for menu in self.command_menu_options().keys() if menu not in unsupported]

        command_menu_choice = self.command_menu_choice

        menu_replacements: dict[str, str] = {}
        if command_menu_choice == configDict.RANDOMIZE_ALL:
            shuffled_menus = supported_menus.copy()
            random.shuffle(shuffled_menus)
            for index, old_menu in enumerate(supported_menus):
                menu_replacements[old_menu] = shuffled_menus[index]
        elif command_menu_choice == configDict.RANDOMIZE_ONE:
            new_menu = random.choice(supported_menus)
            for old_menu in supported_menus:
                menu_replacements[old_menu] = new_menu
        else:  # A specific command menu was chosen
            for old_menu in supported_menus:
                menu_replacements[old_menu] = command_menu_choice
        return menu_replacements


class RoomTransitionImageRandomizer:

    def __init__(self, transition_choice: str):
        super().__init__()
        self.transition_choice = transition_choice

    @staticmethod
    def room_transition_options() -> dict[str, str]:
        return {
            configDict.VANILLA: "Vanilla",
            configDict.RANDOMIZE_IN_GAME_ONLY: "Randomize (in-game only)",
            configDict.RANDOMIZE_CUSTOM_ONLY: "Randomize (custom only)",
            configDict.RANDOMIZE_ALL: "Randomize (in-game + custom)",
        }

    def randomize_room_transitions(self) -> list[Asset]:
        if self.transition_choice == configDict.VANILLA:
            return []
        assets = []
        # assets.extend(self._randomize_ps2())
        assets.extend(self._randomize_pc())
        return assets

    def _randomize_pc(self) -> list[Asset]:
        transition_replacements = self._compute_transition_replacements()
        assets: list[Asset] = []
        for old_image, new_image in transition_replacements.items():
            if new_image.startswith("$x$"):  # It's a custom one with a full path
                replacement_source = {
                    "name": new_image[3:]
                }
            else:
                replacement_source = {
                    "name": f"remastered/field2d/us/{new_image}field.2dd/US_{new_image}field_2dd2.png",
                    "type": "internal"
                }
            # These images aren't any different between the regions, so save some mod space by using a multi
            assets.append({
                "platform": "pc",
                "name": f"remastered/field2d/us/{old_image}field.2dd/US_{old_image}field_2dd2.png",
                "multi": [
                    {"name": f"remastered/field2d/fr/{old_image}field.2dd/FR_{old_image}field_2dd2.png"},
                    {"name": f"remastered/field2d/gr/{old_image}field.2dd/GR_{old_image}field_2dd2.png"},
                    {"name": f"remastered/field2d/it/{old_image}field.2dd/IT_{old_image}field_2dd2.png"},
                    {"name": f"remastered/field2d/sp/{old_image}field.2dd/SP_{old_image}field_2dd2.png"}
                ],
                "method": "copy",
                "source": [replacement_source]
            })
        return assets

    def _compute_transition_replacements(self) -> dict[str, str]:
        supported_transitions = [
            AGRABAH,
            BEAST_CASTLE,
            PORT_ROYAL,
            DISNEY_CASTLE,
            TWTNW,
            HOLLOW_BASTION,
            OLYMPUS_COLISEUM,
            PRIDE_LANDS,
            ATLANTICA,
            LAND_OF_DRAGONS,
            HALLOWEEN_TOWN,
            HUNDRED_ACRE_WOOD,
            SPACE_PARANOIDS,
            TWILIGHT_TOWN,
            TIMELESS_RIVER
        ]

        transition_choice = self.transition_choice

        source_list: list[str] = []
        if transition_choice == configDict.RANDOMIZE_IN_GAME_ONLY:
            source_list = supported_transitions.copy()
        elif transition_choice == configDict.RANDOMIZE_CUSTOM_ONLY:
            source_list = [f"$x${path}" for path in self._custom_room_transition_images().values()]
        elif transition_choice == configDict.RANDOMIZE_ALL:
            source_list = []
            source_list.extend(supported_transitions)
            source_list.extend([f"$x${path}" for path in self._custom_room_transition_images().values()])

        transition_replacements: dict[str, str] = {}
        if len(source_list) == 0:
            return transition_replacements

        candidates: list[str] = []
        for index, old_transition in enumerate(supported_transitions):
            if len(candidates) == 0:
                candidates = source_list.copy()
                random.shuffle(candidates)
            transition_replacements[old_transition] = candidates.pop()

        return transition_replacements

    @staticmethod
    def _custom_room_transition_images() -> dict[str, Path]:
        result: dict[str, Path] = {}

        custom_visuals_path = appconfig.read_custom_visuals_path()
        if custom_visuals_path is None:
            return result

        room_transition_images_path = custom_visuals_path / "room-transition-images"
        if not room_transition_images_path.is_dir():
            return result

        for root, dirs, files in os.walk(room_transition_images_path):
            root_path = Path(root)
            for file in files:
                name, extension = os.path.splitext(file)
                if extension.lower() == ".png":
                    file_path = root_path / file
                    result[name] = file_path

        return result

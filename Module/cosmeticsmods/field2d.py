import os
import random
from pathlib import Path
from typing import Optional

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


class ReplacementCommandMenu:

    def __init__(self):
        super().__init__()

    def ps2_command_menu_assets(self, old_menu: str) -> list[Asset]:
        return []

    def pc_command_menu_assets(self, old_menu: str, regions: list[str]) -> list[Asset]:
        return []


class VanillaCommandMenu(ReplacementCommandMenu):

    def __init__(self, code: str):
        super().__init__()
        self.code = code

    def ps2_command_menu_assets(self, old_menu: str) -> list[Asset]:
        new_menu = self.code
        return [{
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
        }]

    def pc_command_menu_assets(self, old_menu: str, regions: list[str]) -> list[Asset]:
        new_menu = self.code

        assets: list[Asset] = []
        for region in regions:
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


class CustomCommandMenu(ReplacementCommandMenu):

    def __init__(self, name: str, containing_path: Path, original_file: Path, remastered_file: Optional[Path]):
        super().__init__()
        self.name = name
        self.containing_path = containing_path
        self.original_file = original_file
        self.remastered_file = remastered_file

    def ps2_command_menu_assets(self, old_menu: str) -> list[Asset]:
        original_file = self.original_file
        return [{
            "platform": "ps2",
            "name": f"field2d/jp/{old_menu}command.2dd",
            "multi": [
                {"name": f"field2d/us/{old_menu}command.2dd"}
            ],
            "method": "copy",
            "source": [
                {"name": f"{original_file}"}
            ]
        }]

    def pc_command_menu_assets(self, old_menu: str, regions: list[str]) -> list[Asset]:
        original_names = []
        remastered_names = []
        for region in regions:
            original_names.append(f"field2d/{region}/{old_menu}command.2dd")
            remastered_names.append(
                f"remastered/field2d/{region}/{old_menu}command.2dd/{region.upper()}_{old_menu}command_2dd0.png"
            )

        return [
            {
                "platform": "pc",
                "name": original_names[0],
                "multi": [{"name": original_name} for original_name in original_names[1:]],
                "method": "copy",
                "source": [
                    {"name": f"{self.original_file}"}
                ]
            },
            {
                "platform": "pc",
                "name": remastered_names[0],
                "multi": [{"name": remastered_name} for remastered_name in remastered_names[1:]],
                "method": "copy",
                "source": [
                    {"name": f"{self.remastered_file}"}
                ]
            }
        ]


class CommandMenuRandomizer:

    def __init__(self, command_menu_choice: str):
        super().__init__()
        self.command_menu_choice = command_menu_choice

    @staticmethod
    def command_menu_options() -> dict[str, str]:
        return {
            configDict.VANILLA: "Vanilla",
            configDict.RANDOMIZE_ONE: "Randomize (one)",
            configDict.RANDOMIZE_IN_GAME_ONLY: "Randomize (in-game only)",
            configDict.RANDOMIZE_CUSTOM_ONLY: "Randomize (custom only)",
            configDict.RANDOMIZE_ALL: "Randomize (in-game + custom)",
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
        assets = []
        assets.extend(self._randomize_ps2())
        assets.extend(self._randomize_pc())
        return assets

    def _randomize_ps2(self) -> list[Asset]:
        menu_replacements = self._compute_menu_replacements(pc=False)
        assets: list[Asset] = []
        for old_menu, new_menu in menu_replacements.items():
            assets.extend(new_menu.ps2_command_menu_assets(old_menu))
        return assets

    def _randomize_pc(self) -> list[Asset]:
        menu_replacements = self._compute_menu_replacements(pc=True)
        assets: list[Asset] = []
        for old_menu, new_menu in menu_replacements.items():
            assets.extend(new_menu.pc_command_menu_assets(old_menu, regions=["fr", "gr", "it", "sp", "us"]))
        return assets

    def _supported_menu_list(self, pc: bool) -> list[str]:
        unsupported = [
            configDict.VANILLA,
            configDict.RANDOMIZE_ONE,
            configDict.RANDOMIZE_IN_GAME_ONLY,
            configDict.RANDOMIZE_CUSTOM_ONLY,
            configDict.RANDOMIZE_ALL,
        ]
        if pc:
            unsupported.append(ATLANTICA)
        return [menu for menu in self.command_menu_options().keys() if menu not in unsupported]

    def _vanilla_command_menus(self, pc: bool) -> list[VanillaCommandMenu]:
        return [VanillaCommandMenu(menu) for menu in self._supported_menu_list(pc)]

    @staticmethod
    def _custom_command_menus() -> list[CustomCommandMenu]:
        result: list[CustomCommandMenu] = []

        custom_visuals_path = appconfig.read_custom_visuals_path()
        if custom_visuals_path is None:
            return result

        command_menus_path = custom_visuals_path / "command-menus"
        if not command_menus_path.is_dir():
            return result

        for child in os.listdir(command_menus_path):
            command_menu_path = command_menus_path / child

            original: Optional[Path] = None
            remastered: Optional[Path] = None

            if command_menu_path.is_dir():
                for file in os.listdir(command_menu_path):
                    _, extension = os.path.splitext(file)
                    if extension == ".2dd":
                        original = command_menu_path / file
                    elif extension == ".dds" or extension == ".png":
                        remastered = command_menu_path / file

            if original is not None:
                result.append(CustomCommandMenu(
                    name=child,
                    containing_path=command_menu_path,
                    original_file=original,
                    remastered_file=remastered
                ))

        return result

    def _replacement_menu_list(self, pc: bool) -> list[ReplacementCommandMenu]:
        command_menu_choice = self.command_menu_choice

        if command_menu_choice == configDict.VANILLA:
            return []

        elif command_menu_choice == configDict.RANDOMIZE_ONE:
            # If any custom, use one of those, and fall back to in-game if needed.
            # This should hopefully be good enough for now without needing to add even more options.
            custom_menus = self._custom_command_menus()
            if len(custom_menus) > 0:
                return [random.choice(custom_menus)]
            else:
                return [random.choice(self._vanilla_command_menus(pc))]

        elif command_menu_choice == configDict.RANDOMIZE_IN_GAME_ONLY:
            return self._vanilla_command_menus(pc)

        elif command_menu_choice == configDict.RANDOMIZE_CUSTOM_ONLY:
            return self._custom_command_menus()

        elif command_menu_choice == configDict.RANDOMIZE_ALL:
            replacements: list[ReplacementCommandMenu] = []
            replacements.extend(self._vanilla_command_menus(pc))
            replacements.extend(self._custom_command_menus())
            return replacements

        else:  # A specific command menu was chosen
            return [VanillaCommandMenu(code=command_menu_choice)]

    def _compute_menu_replacements(self, pc: bool) -> dict[str, ReplacementCommandMenu]:
        replacement_list = self._replacement_menu_list(pc)
        if len(replacement_list) == 0:
            return {}

        menu_replacements: dict[str, ReplacementCommandMenu] = {}
        candidates: list[ReplacementCommandMenu] = []
        for index, old_menu in enumerate(self._supported_menu_list(pc)):
            if len(candidates) == 0:
                candidates = replacement_list.copy()
                random.shuffle(candidates)
            menu_replacements[old_menu] = candidates.pop()

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

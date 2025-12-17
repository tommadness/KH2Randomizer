import random
from pathlib import Path, PurePath
from typing import Optional, Iterator

from Class.openkhmod import ModAsset, AssetPlatform, ModSourceFile, AssetMethod
from List import configDict
from Module import appconfig
from Module.paths import walk_files_with_extension

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

    def ps2_command_menu_assets(self, old_menu: str) -> list[ModAsset]:
        return []

    def pc_command_menu_assets(self, old_menu: str, regions: list[str]) -> list[ModAsset]:
        return []


class VanillaCommandMenu(ReplacementCommandMenu):

    def __init__(self, code: str):
        super().__init__()
        self.code = code

    def ps2_command_menu_assets(self, old_menu: str) -> list[ModAsset]:
        new_menu = self.code
        return [ModAsset.make_copy_asset(
            game_files=[f"field2d/jp/{old_menu}command.2dd", f"field2d/us/{old_menu}command.2dd"],
            platform=AssetPlatform.PS2,
            source_file=f"field2d/jp/{new_menu}command.2dd",
            internal=True,
        )]

    def pc_command_menu_assets(self, old_menu: str, regions: list[str]) -> list[ModAsset]:
        new_menu = self.code

        assets: list[ModAsset] = []
        for region in regions:
            assets.append(ModAsset.make_copy_asset(
                game_files=[f"field2d/{region}/{old_menu}command.2dd"],
                platform=AssetPlatform.PC,
                source_file=f"field2d/{region}/{new_menu}command.2dd",
                internal=True,
            ))

            remastered_region = f"remastered/field2d/{region}"
            cap_region = region.upper()
            assets.append(ModAsset.make_copy_asset(
                game_files=[f"{remastered_region}/{old_menu}command.2dd/{cap_region}_{old_menu}command_2dd0.png"],
                platform=AssetPlatform.PC,
                source_file=f"{remastered_region}/{new_menu}command.2dd/{cap_region}_{new_menu}command_2dd0.png",
                internal=True,
            ))

        return assets

    def image_for_preview(self, extracted_game_data: Path) -> Optional[Path]:
        remastered_field2d = extracted_game_data / "remastered" / "field2d"
        code = self.code
        for region in ["us", "fr", "gr", "it", "sp"]:
            path = remastered_field2d / region / f"{code}command.2dd" / f"{region.upper()}_{code}command_2dd0.png"
            if path.is_file():
                return path
        return None


class CustomCommandMenu(ReplacementCommandMenu):

    def __init__(self, name: str, original_file: Path, remastered_file: Optional[Path]):
        super().__init__()
        self.name = name
        self.original_file = original_file
        self.remastered_file = remastered_file

    def ps2_command_menu_assets(self, old_menu: str) -> list[ModAsset]:
        return [ModAsset.make_copy_asset(
            game_files=[f"field2d/jp/{old_menu}command.2dd", f"field2d/us/{old_menu}command.2dd"],
            platform=AssetPlatform.PS2,
            source_file=self.original_file,
        )]

    def pc_command_menu_assets(self, old_menu: str, regions: list[str]) -> list[ModAsset]:
        original_names = []
        remastered_names = []
        for region in regions:
            original_names.append(f"field2d/{region}/{old_menu}command.2dd")
            remastered_names.append(
                f"remastered/field2d/{region}/{old_menu}command.2dd/{region.upper()}_{old_menu}command_2dd0.png"
            )

        return [
            ModAsset.make_copy_asset(
                game_files=original_names,
                platform=AssetPlatform.PC,
                source_file=self.original_file,
            ),
            ModAsset.make_copy_asset(
                game_files=remastered_names,
                platform=AssetPlatform.PC,
                source_file=self.remastered_file,
            ),
        ]


class CommandMenuRandomizer:

    def __init__(self, command_menu_choice: str):
        super().__init__()
        self.command_menu_choice = command_menu_choice

    @staticmethod
    def directory_name() -> str:
        return "command-menus"

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

    def randomize_command_menus(self) -> list[ModAsset]:
        assets = []
        assets.extend(self._randomize_ps2())
        assets.extend(self._randomize_pc())
        return assets

    def _randomize_ps2(self) -> list[ModAsset]:
        menu_replacements = self._compute_menu_replacements(pc=False)
        assets: list[ModAsset] = []
        for old_menu, new_menu in menu_replacements.items():
            assets.extend(new_menu.ps2_command_menu_assets(old_menu))
        return assets

    def _randomize_pc(self) -> list[ModAsset]:
        menu_replacements = self._compute_menu_replacements(pc=True)
        assets: list[ModAsset] = []
        for old_menu, new_menu in menu_replacements.items():
            assets.extend(new_menu.pc_command_menu_assets(old_menu, regions=["fr", "gr", "it", "sp", "us"]))
        return assets

    @staticmethod
    def _supported_menu_list(pc: bool) -> list[str]:
        unsupported = [
            configDict.VANILLA,
            configDict.RANDOMIZE_ONE,
            configDict.RANDOMIZE_IN_GAME_ONLY,
            configDict.RANDOMIZE_CUSTOM_ONLY,
            configDict.RANDOMIZE_ALL,
        ]
        if pc:
            unsupported.append(ATLANTICA)
        return [menu for menu in CommandMenuRandomizer.command_menu_options().keys() if menu not in unsupported]

    @staticmethod
    def _vanilla_command_menus(pc: bool) -> list[VanillaCommandMenu]:
        return [VanillaCommandMenu(menu) for menu in CommandMenuRandomizer._supported_menu_list(pc)]

    @staticmethod
    def _custom_command_menus() -> list[CustomCommandMenu]:
        result: list[CustomCommandMenu] = []

        custom_visuals_path = appconfig.read_custom_visuals_path()
        if custom_visuals_path is None:
            return result

        command_menus_path = custom_visuals_path / CommandMenuRandomizer.directory_name()
        if not command_menus_path.is_dir():
            return result

        for command_menu_dir in command_menus_path.iterdir():
            if command_menu_dir.is_dir():
                original: Optional[Path] = None
                remastered: Optional[Path] = None

                for file in command_menu_dir.iterdir():
                    extension = file.suffix
                    if extension == ".2dd":
                        original = file
                    elif extension == ".dds" or extension == ".png":
                        remastered = file

                if original is not None:
                    result.append(CustomCommandMenu(
                        name=command_menu_dir.name,
                        original_file=original,
                        remastered_file=remastered,
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

    @staticmethod
    def collect_custom_images() -> list[Path]:
        result: list[Path] = []

        for menu in CommandMenuRandomizer._custom_command_menus():
            image_path = menu.remastered_file
            if image_path is not None:
                result.append(image_path)

        return result

    @staticmethod
    def collect_vanilla_images() -> list[Path]:
        result: list[Path] = []

        extracted_data_path = appconfig.extracted_game_path("kh2")
        if extracted_data_path is None:
            return result

        vanilla_menus = CommandMenuRandomizer._vanilla_command_menus(pc=True)
        for menu in vanilla_menus:
            image_path = menu.image_for_preview(extracted_data_path)
            if image_path is not None:
                result.append(image_path)

        return result


class RoomTransitionImageRandomizer:

    def __init__(self, transition_choice: str):
        super().__init__()
        self.transition_choice = transition_choice

    @staticmethod
    def directory_name() -> str:
        return "room-transition-images"

    @staticmethod
    def room_transition_options() -> dict[str, str]:
        return {
            configDict.VANILLA: "Vanilla",
            configDict.RANDOMIZE_IN_GAME_ONLY: "Randomize (in-game only)",
            configDict.RANDOMIZE_CUSTOM_ONLY: "Randomize (custom only)",
            configDict.RANDOMIZE_ALL: "Randomize (in-game + custom)",
        }

    def randomize_room_transitions(self) -> list[ModAsset]:
        if self.transition_choice == configDict.VANILLA:
            return []
        assets: list[ModAsset] = []
        # assets.extend(self._randomize_ps2())
        assets.extend(self._randomize_pc())
        return assets

    def _randomize_pc(self) -> list[ModAsset]:
        transition_replacements = self._compute_transition_replacements()
        regions = ["us", "fr", "gr", "it", "sp"]
        assets: list[ModAsset] = []
        for old_image, replacement_source in transition_replacements.items():
            # These images aren't any different between the regions, so save some mod space by using a multi
            game_files = [
                self._remastered_transition_image_path(region=region, world_code=old_image) for region in regions
            ]
            assets.append(ModAsset.make_asset(
                game_files=game_files,
                platform=AssetPlatform.PC,
                method=AssetMethod.COPY,
                sources=[replacement_source],
            ))

        return assets

    @staticmethod
    def _supported_transitions() -> list[str]:
        return [
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

    def _compute_transition_replacements(self) -> dict[str, ModSourceFile]:
        supported_transitions = RoomTransitionImageRandomizer._supported_transitions()

        def game_transition_sources() -> Iterator[ModSourceFile]:
            for world_code in supported_transitions:
                yield ModSourceFile.make_source_file(
                    source_file=self._remastered_transition_image_path(region="us", world_code=world_code),
                    internal=True,
                )

        def custom_transition_sources() -> Iterator[ModSourceFile]:
            for custom_transition in self.custom_room_transition_images().values():
                yield ModSourceFile.make_source_file(custom_transition)

        transition_choice = self.transition_choice

        source_list: list[ModSourceFile] = []
        if transition_choice == configDict.RANDOMIZE_IN_GAME_ONLY:
            source_list.extend(game_transition_sources())
        elif transition_choice == configDict.RANDOMIZE_CUSTOM_ONLY:
            source_list.extend(custom_transition_sources())
        elif transition_choice == configDict.RANDOMIZE_ALL:
            source_list.extend(game_transition_sources())
            source_list.extend(custom_transition_sources())

        transition_replacements: dict[str, ModSourceFile] = {}
        if len(source_list) == 0:
            return transition_replacements

        candidates: list[ModSourceFile] = []
        for index, old_transition in enumerate(supported_transitions):
            if len(candidates) == 0:
                candidates = source_list.copy()
                random.shuffle(candidates)
            transition_replacements[old_transition] = candidates.pop()

        return transition_replacements

    @staticmethod
    def custom_room_transition_images() -> dict[str, Path]:
        result: dict[str, Path] = {}

        custom_visuals_path = appconfig.read_custom_visuals_path()
        if custom_visuals_path is None:
            return result

        room_transition_images_path = custom_visuals_path / RoomTransitionImageRandomizer.directory_name()
        if not room_transition_images_path.is_dir():
            return result

        for file in walk_files_with_extension(room_transition_images_path, ".png"):
            result[file.name] = file

        return result

    @staticmethod
    def collect_vanilla_images() -> list[Path]:
        result: list[Path] = []

        extracted_data_path = appconfig.extracted_game_path("kh2")
        if extracted_data_path is None:
            return result

        for code in RoomTransitionImageRandomizer._supported_transitions():
            image_path = RoomTransitionImageRandomizer._vanilla_transition_image_for_preview(extracted_data_path, code)
            if image_path is not None:
                result.append(image_path)

        return result

    @staticmethod
    def _vanilla_transition_image_for_preview(extracted_game_path: Path, code: str) -> Optional[Path]:
        for region in ["us", "fr", "gr", "it", "sp"]:
            subpath = RoomTransitionImageRandomizer._remastered_transition_image_path(region=region, world_code=code)
            path = extracted_game_path / subpath
            if path.is_file():
                return path
        return None

    @staticmethod
    def _remastered_transition_image_path(region: str, world_code: str) -> PurePath:
        return PurePath(
            "remastered",
            "field2d",
            region,
            f"{world_code}field.2dd",
            f"{region.upper()}_{world_code}field_2dd2.png"
        )

import re
from copy import deepcopy
from enum import Enum
from pathlib import PurePath, Path
from typing import Any, Optional, Iterator, Union
from zipfile import ZipFile

import yaml

from Module.resources import resource_path

ModPath = Union[str, PurePath]
StrDict = dict[str, Any]

_ASSETS = "assets"
_DESCRIPTION = "description"
_INTERNAL = "internal"
_METHOD = "method"
_MULTI = "multi"
_NAME = "name"
_ORIGINAL_AUTHOR = "originalAuthor"
_PLATFORM = "platform"
_SOURCE = "source"
_TITLE = "title"
_TYPE = "type"


def write_yaml_to_zip_file(zip_file: ZipFile, name: str, data, sort_keys: bool):
    zip_file.writestr(name, yaml.dump(data, line_break="\r\n", sort_keys=sort_keys))


def write_unicode_yaml_to_zip_file(zip_file: ZipFile, name: str, data, sort_keys: bool):
    yaml_string = yaml.dump(data, line_break="\r\n", sort_keys=sort_keys)
    yaml_string = re.sub(
        r"en: ([a-zA-Z0-9\\]+)", r'en: "\1"', yaml_string
    )  # surround text of the journal with double quotes to allow for automatic unicode conversion
    yaml_string = yaml_string.replace("NEWLINE", "\\n")
    zip_file.writestr(name, yaml_string)


def _as_path(mod_path: ModPath) -> PurePath:
    if isinstance(mod_path, PurePath):
        return mod_path
    else:
        return PurePath(mod_path)


class ModYmlException(Exception):
    pass


class ModYmlSyntaxException(ModYmlException):
    pass


class AssetMethod(str, Enum):
    # https://github.com/OpenKH/OpenKh/blob/8f967bd412a9e7104a5124ae2688815307ba2472/OpenKh.Patcher/Metadata.cs#L96-L107
    AREADATASCRIPT = "areadatascript"
    BDSCRIPT = "bdscript"
    BINARC = "binarc"
    COPY = "copy"
    IMGD = "imgd"
    IMGZ = "imgz"
    KH2MSG = "kh2msg"
    LISTPATCH = "listpatch"
    SPAWNPOINT = "spawnpoint"
    SYNTHPATCH = "synthpatch"


class AssetPlatform(str, Enum):
    PC = "pc"
    PS2 = "ps2"


class BinarcMethod(str, Enum):
    # Taken from OpenKH docs originally, but found others in use in practice.
    # It's not entirely clear whether these are even meant to be a separate entity from the AssetMethod.
    AREADATASCRIPT = "areadatascript"
    AREADATASPAWN = "areadataspawn"
    COPY = "copy"
    INDEX = "index"
    IMGD = "imgd"
    IMGZ = "imgz"
    LISTPATCH = "listpatch"
    KH2MSG = "kh2msg"
    SPAWNPOINT = "spawnpoint"


class ModSourceFile:
    """
    Representation of a file that serves as a source in a mod.

    Must have a `name` property that is the relative or absolute path of the source file. Optionally contains other
    properties as well, depending on the context in which the source file is being used.

    Not meant to be a fully type-safe implementation, as the underlying data model is still exposed.

    Some examples:

    - name: C:\\kh2\\keyblades\\Jungle King\\base\\remastered-effects\\-1.dds

    - name: randoseed-mod-files/ItemList.yml
      type: item

    - name: randoseed-mod-files/sys.yml
      language: en

    - name: title/title1.png
      highdef: title/title1_hd.png
      index: 1

    - name: obj/F_EX040_EH.a.us
      type: internal
    """

    def __init__(self, source: Optional[StrDict] = None):
        super().__init__()
        self.data: StrDict = {}
        if source is not None:
            # Normalize the source file name if present
            raw_name = source.get(_NAME, "")
            if raw_name:
                source[_NAME] = ModYml.source_file_name(raw_name)

            self.data = source

    def file_path(self) -> Path:
        """Returns the path represented by this source file, or raises ModYmlSyntaxException if missing."""
        name = self.data.get(_NAME, "")
        if not name:
            raise ModYmlSyntaxException(f"Source files must have a {_NAME}")
        return Path(name)

    def type(self) -> str:
        """
        Returns the value of the `type` property of this object, or an empty string if not defined. (Not all mod
        operations require an explicit type.)
        """
        return self.data.get(_TYPE, "")

    def __getitem__(self, key: str):
        """Returns the value of this object's property with the specified key, or None if not defined."""
        return self.data.get(key, None)

    def __repr__(self) -> str:
        return repr(self.data)

    @staticmethod
    def make_source_file(source_file: ModPath, internal: bool = False, **source_data: Any) -> "ModSourceFile":
        data: StrDict = {_NAME: ModYml.source_file_name(source_file)}
        if internal:
            data[_TYPE] = _INTERNAL
        data.update(source_data)
        return ModSourceFile(data)


class ModBinarcSource:
    """
    Representation of a source of a mod asset that uses the `binarc` method.

    Must have a `name`, `type`, and `method`, as well as at least one `source` (see `ModSourceFile`). The valid
    `method`s are enumerated in `BinarcMethod`.

    Not meant to be a fully type-safe implementation, as the underlying data model is still exposed.

    Some examples:

    - name: sys
      type: list
      method: kh2msg
      source:
        - name: sys.yml
          language: en

    - name: bons
      type: list
      method: listpatch
      source:
      - name: 00battle.bin/BonsList.yml
        type: bons
    """

    def __init__(self, source: Optional[StrDict] = None):
        super().__init__()
        self.data: StrDict = {}
        if source is not None:
            self.data = source

    def name(self) -> str:
        """Returns the name of the subfile being modified, or raises ModYmlSyntaxException if missing or invalid."""
        name = self.data.get(_NAME, "")
        if not name:
            raise ModYmlSyntaxException(f"binarc sources must have a {_NAME}")
        return name

    def type(self) -> str:
        """Returns the type of the subfile being modified, or raises ModYmlSyntaxException if missing or invalid."""
        name = self.data.get(_TYPE, "")
        if not name:
            raise ModYmlSyntaxException(f"binarc sources must have a {_TYPE}")
        return name

    def method(self) -> BinarcMethod:
        """Returns this source's method, or raises ModYmlSyntaxException if missing or invalid."""
        raw = self.data.get(_METHOD, "")
        if not raw:
            raise ModYmlSyntaxException(f"binarc sources must have a {_METHOD}")
        try:
            return BinarcMethod(raw)
        except ValueError as e:
            raise ModYmlSyntaxException from e

    def source_files(self) -> list[ModSourceFile]:
        """Returns this source's inner source files, or raises ModYmlSyntaxException if missing."""
        sources: list[StrDict] = self.data.get(_SOURCE, [])
        if not sources:
            raise ModYmlSyntaxException(f"Binarc sources must have at least one inner {_SOURCE}")
        return [ModSourceFile(source) for source in sources]

    @staticmethod
    def make_source(name: str, type_: str, method: BinarcMethod, sources: list[ModSourceFile]) -> "ModBinarcSource":
        data: StrDict = {
            _NAME: name,
            _TYPE: type_,
            _METHOD: method.value,
            _SOURCE: [source.data for source in sources]
        }
        return ModBinarcSource(data)


class ModAsset:
    """
    Representation of an OpenKH Mods Manager mod asset.

    Not meant to be a fully type-safe implementation, as the underlying data model is still exposed.

    Must have a `name` that represents the relative path to the target game file. May contain additional target game
    files as part of a `multi`.

    Must have a `method` that, should be one of the `AssetMethod` values.

    Must contain at least one `source`, which should either be a `ModSourceFile` or a `ModBinarcSource`, depending on
    the `method`.

    May contain a `platform` property that indicates that the asset is only needed for that particular platform (see
    `AssetPlatform`.

    Some examples:

    - name: scripts/F266B00B GoA ROM.lua
      method: copy
      source:
      - name: F266B00B GoA ROM.lua

    - method: copy
      name: msn/jp/BB03_MS103.bar
      source:
      - name: files/modified_msn.bar

    - name: obj/W_EX010_U0_NM.a.us
      multi:
      - name: obj/W_EX010_U0_TR.a.us
      - name: obj/W_EX010_U0_WI.a.us
      platform: pc
      method: copy
      source:
      - name: obj/W_EX010_U0.a.us
        type: internal

    - method: binarc
      name: ard/wi03.ard
      source:
      - method: spawnpoint
        name: b_40
        source:
        - name: files/b_40.yml
        type: AreaDataSpawn

    - name: 00common.bdx
      method: bdscript
      source:
      - name: 00common.bdscript

    - name: 00objentry.bin
      method: listpatch
      type: List
      source:
      - name: ObjList.yml
        type: objentry
    """

    def __init__(self, asset: Optional[StrDict] = None):
        super().__init__()
        self.data: StrDict = {}
        if asset is not None:
            self.data = asset

    def primary_game_file(self) -> PurePath:
        """Returns the primary game file for this asset, or raises ModYmlSyntaxException if missing or invalid."""
        return self._game_file(self.data)

    def game_files(self) -> list[PurePath]:
        """
        Returns all game files for this asset (both the primary and any additional from a `multi` declaration), or
        raises ModYmlSyntaxException if missing or invalid.
        """
        game_files = [self.primary_game_file()]
        game_files.extend(self._game_file(multi_data) for multi_data in self.data.get(_MULTI, []))
        return game_files

    def method(self) -> AssetMethod:
        """Returns this asset's method, or raises ModYmlSyntaxException if missing or invalid."""
        raw = self.data.get(_METHOD, "")
        if not raw:
            raise ModYmlSyntaxException(f"Assets must have a {_METHOD}")
        try:
            return AssetMethod(raw)
        except ValueError as e:
            raise ModYmlSyntaxException from e

    def sources(self) -> list[StrDict]:
        """Returns this asset's sources, or raises ModYmlSyntaxException if missing."""
        sources = self.data.get(_SOURCE, [])
        if not sources:
            raise ModYmlSyntaxException(f"Assets must have at least one {_SOURCE}")
        return sources

    def copy_sources(self) -> list[ModSourceFile]:
        """Returns the source files for this asset, or an empty list if this asset's method is not `copy`."""
        if self.method() == AssetMethod.COPY:
            return [ModSourceFile(source) for source in self.sources()]
        else:
            return []

    def binarc_sources(self) -> list[ModBinarcSource]:
        """Returns the binarc sources for this asset, or an empty list if this asset's method is not `binarc`."""
        if self.method() == AssetMethod.BINARC:
            return [ModBinarcSource(source) for source in self.sources()]
        else:
            return []

    @staticmethod
    def make_copy_asset(
            game_files: list[ModPath],
            source_file: ModPath,
            platform: Optional[AssetPlatform] = None,
            internal: bool = False,
    ) -> "ModAsset":
        """
        Creates a ModAsset for a simple file copy.

        Use make_asset if anything more complex is required.
        """
        source: StrDict = {_NAME: ModYml.source_file_name(source_file)}
        if internal:
            source[_TYPE] = _INTERNAL
        return ModAsset._make_asset(
            game_files=game_files,
            method=AssetMethod.COPY,
            sources=[source],
            platform=platform,
        )

    @staticmethod
    def make_binarc_asset(
            game_files: list[ModPath],
            sources: list[ModBinarcSource],
            platform: Optional[AssetPlatform] = None,
    ) -> "ModAsset":
        """
        Creates a ModAsset for a simple binarc modification.

        Use make_asset if anything more complex is required.
        """
        return ModAsset._make_asset(
            game_files=game_files,
            method=AssetMethod.BINARC,
            sources=[source.data for source in sources],
            platform=platform,
        )

    @staticmethod
    def make_asset(
            game_files: list[ModPath],
            method: AssetMethod,
            sources: list[ModSourceFile],
            platform: Optional[AssetPlatform] = None,
            type_: str = "",
    ) -> "ModAsset":
        asset_data: StrDict = {}
        if type_:
            asset_data[_TYPE] = type_
        asset = ModAsset._make_asset(
            game_files=game_files,
            method=method,
            sources=[source.data for source in sources],
            platform=platform,
            asset_data=asset_data,
        )
        return asset

    @staticmethod
    def _game_file(data: StrDict) -> PurePath:
        """
        Returns the value in the `name` property of the given dictionary as a relative PurePath, or raises
        ModYmlSyntaxException if missing or an absolute path.
        """
        name = data.get(_NAME, "")
        if not name:
            raise ModYmlSyntaxException(f"Assets must have a {_NAME}")
        path = PurePath(name)
        if path.is_absolute():
            raise ModYmlSyntaxException(f"{name} - Asset names must be relative paths")
        return path

    @staticmethod
    def _make_asset(
            game_files: list[ModPath],
            method: AssetMethod,
            sources: list[StrDict],
            platform: Optional[AssetPlatform],
            asset_data: Optional[StrDict] = None,
    ) -> "ModAsset":
        game_file_count = len(game_files)
        if game_file_count == 0:
            raise ValueError("Assets require at least one game file")

        def game_file_name(game_file: ModPath) -> str:
            game_file = _as_path(game_file)
            if game_file.is_absolute():
                raise ValueError(f"{str(game_file)}: Game files must be relative paths")
            else:
                return game_file.as_posix()

        data: StrDict = {_NAME: game_file_name(game_files[0])}

        if game_file_count > 1:
            data[_MULTI] = [{_NAME: game_file_name(game_file)} for game_file in game_files[1:]]

        if platform is not None:
            data[_PLATFORM] = platform.value

        data[_METHOD] = method.value

        if sources:
            data[_SOURCE] = sources
        else:
            raise ValueError("Assets require at least one source")

        if asset_data is not None:
            data.update(asset_data)

        return ModAsset(data)


class ModYml:
    """
    Representation of an OpenKH Mods Manager mod.

    Not meant to be a fully type-safe implementation, as the underlying data model is still exposed.
    """

    def __init__(self, title: str, description: Optional[str]):
        self.data: StrDict = {_TITLE: title}
        if description is not None:
            self.data[_DESCRIPTION] = description
        self.data[_ASSETS] = []

    @staticmethod
    def from_file(mod_yml_file: Path) -> "ModYml":
        """
        Returns a ModYml object from the contents of the specified file. Performs only basic syntax checking up front.
        """
        if not mod_yml_file.is_file():
            raise ModYmlException(f"{str(mod_yml_file)} - File does not exist")
        with open(mod_yml_file, "r", encoding="utf-8") as opened_file:
            yaml_data: StrDict = yaml.safe_load(opened_file)
            if not isinstance(yaml_data, dict):
                raise ModYmlSyntaxException(f"{str(mod_yml_file)} - Expected mod file to parse as a dict")
            if _ASSETS not in yaml_data:
                raise ModYmlSyntaxException(f"{str(mod_yml_file)} - Expected mod file to contain assets")

            # Create it with a title, but then swap out the data dict completely. Feels a little weird, but keeps the
            # constructor the way we want it.
            mod_yml = ModYml(title="", description=None)
            mod_yml.data = yaml_data
            return mod_yml

    def original_author(self) -> str:
        return self.data.get(_ORIGINAL_AUTHOR, "")

    def assets(self) -> list[StrDict]:
        return self.data[_ASSETS]

    def add_assets(self, assets: list[StrDict]):
        existing = self.data[_ASSETS]
        # Using deepcopy to avoid YAML anchors and aliases being used
        for asset in assets:
            existing.append(deepcopy(asset))

    def add_asset(self, asset: StrDict):
        self.add_assets([asset])

    def add_mod_assets(self, assets: list[ModAsset]):
        self.add_assets([asset.data for asset in assets])

    def add_mod_asset(self, asset: ModAsset):
        self.add_asset(asset.data)

    def find_assets(self, asset_name: str) -> Iterator[StrDict]:
        return (asset for asset in self.data[_ASSETS] if asset[_NAME] == asset_name)

    def find_asset(self, asset_name: str) -> Optional[StrDict]:
        return next(self.find_assets(asset_name), None)

    def add_asset_source(self, asset_name: str, source: StrDict):
        asset = self.find_asset(asset_name)
        if asset is None:
            raise Exception(f"Unable to find {asset_name} in the mod being built")
        else:
            # Using deepcopy to avoid YAML anchors and aliases being used
            asset[_SOURCE].append(deepcopy(source))

    def write_to_zip_file(self, zip_file: ZipFile):
        write_yaml_to_zip_file(zip_file, "mod.yml", self.data, sort_keys=False)

    @staticmethod
    def source_file_name(source_file: ModPath) -> str:
        """Returns an appropriately formatted string to use as a source name in a mod."""
        source_file = _as_path(source_file)
        if source_file.is_absolute():
            return str(source_file)
        else:
            return source_file.as_posix()


class Bonuses:
    """YAML builder for listpatch for bonuses. See https://openkh.dev/kh2/file/type/00battle.html#bons."""

    def __init__(self, source_name: str):
        self.data: dict[int, dict[str, dict[str, int]]] = {}
        self.source_name = source_name

    def add_bonus(
        self,
        reward_id: int,
        character_name: str,
        character_id: int,
        hp_increase: int,
        mp_increase: int,
        drive_gauge_increase: int,
        item_slot_upgrade: int,
        accessory_slot_upgrade: int,
        armor_slot_upgrade: int,
        bonus_item_1: int,
        bonus_item_2: int,
        padding: int,
    ):
        if reward_id not in self.data:
            self.data[reward_id] = {}
        self.data[reward_id][character_name] = {
            "RewardId": reward_id,
            "CharacterId": character_id,
            "HpIncrease": hp_increase,
            "MpIncrease": mp_increase,
            "DriveGaugeUpgrade": drive_gauge_increase,
            "ItemSlotUpgrade": item_slot_upgrade,
            "AccessorySlotUpgrade": accessory_slot_upgrade,
            "ArmorSlotUpgrade": armor_slot_upgrade,
            "BonusItem1": bonus_item_1,
            "BonusItem2": bonus_item_2,
            "Padding": padding,
            # "Description": ?,
            # "Unknown0c": ?,
        }

    def write_to_zip_file(self, zip_file: ZipFile):
        write_yaml_to_zip_file(zip_file, self.source_name, self.data, sort_keys=True)


class FormLevels:
    """YAML builder for listpatch for form levels. See https://openkh.dev/kh2/file/type/00battle.html#fmlv."""

    def __init__(self, source_name: str):
        self.data: dict[str, list[dict[str, int]]] = {}
        self.source_name = source_name

    def add_form_level(
        self,
        form_name: str,
        form_id: int,
        form_level: int,
        ability: int,
        experience: int,
        growth_ability_level: int,
    ):
        if form_name not in self.data:
            self.data[form_name] = []
        self.data[form_name].append(
            {
                "FormId": form_id,
                "FormLevel": form_level,
                "Experience": experience,
                "Ability": ability,
                "GrowthAbilityLevel": growth_ability_level,
            }
        )

    def turn_off_anti(self):
        self.data["Antiform"] = []
        self.data["Antiform"].append(
            {
                "FormId": 6,
                "FormLevel": 1,
                "Experience": 0,
                "Ability": 0,
                "GrowthAbilityLevel": 0,
            }
        )
        self.data["Antiform"].append(
            {
                "FormId": 6,
                "FormLevel": 2,
                "Experience": 0,
                "Ability": 0,
                "GrowthAbilityLevel": 0,
            }
        )
        self.data["Antiform"].append(
            {
                "FormId": 6,
                "FormLevel": 3,
                "Experience": 0,
                "Ability": 0,
                "GrowthAbilityLevel": 0,
            }
        )

    def write_to_zip_file(self, zip_file: ZipFile):
        write_yaml_to_zip_file(zip_file, self.source_name, self.data, sort_keys=False)


class Items:
    """YAML builder for listpatch for items. See https://openkh.dev/kh2/file/type/03system.html#item."""

    def __init__(self, source_name: str):
        self.data: dict[str, list[dict[str, int]]] = {
            "Stats": [],
            "Items": [],
        }
        self.source_name = source_name

    def add_stats(
        self,
        location_id: int,
        attack: int,
        magic: int,
        defense: int,
        ability: int,
        ability_points: int,
        unknown_08: int,
        fire_resistance: int,
        ice_resistance: int,
        lightning_resistance: int,
        dark_resistance: int,
        unknown_0d: int,
        general_resistance: int,
        unknown: int,
    ):
        self.data["Stats"].append(
            {
                "Id": location_id,
                "Attack": attack,
                "Magic": magic,
                "Defense": defense,
                "Ability": ability,
                "AbilityPoints": ability_points,
                "Unknown08": unknown_08,
                "FireResistance": fire_resistance,
                "IceResistance": ice_resistance,
                "LightningResistance": lightning_resistance,
                "DarkResistance": dark_resistance,
                "Unknown0d": unknown_0d,
                "GeneralResistance": general_resistance,
                "Unknown": unknown,
            }
        )

    def add_item(
        self,
        item_id: int,
        item_type: str,
        flag_0: int,
        flag_1: int,
        rank: str,
        stat_entry: int,
        name: int,
        description: int,
        shop_buy: int,
        shop_sell: int,
        command: int,
        slot: int,
        picture: int,
        icon_1: int,
        icon_2: int,
    ):
        self.data["Items"].append(
            {
                "Id": item_id,
                "Type": item_type,
                "Flag0": flag_0,
                "Flag1": flag_1,
                "Rank": rank,
                "StatEntry": stat_entry,
                "Name": name,
                "Description": description,
                "ShopBuy": shop_buy,
                "ShopSell": shop_sell,
                "Command": command,
                "Slot": slot,
                "Picture": picture,
                "Icon1": icon_1,
                "Icon2": icon_2,
            }
        )

    def write_to_zip_file(self, zip_file: ZipFile):
        write_yaml_to_zip_file(zip_file, self.source_name, self.data, sort_keys=False)


class LevelUps:
    """YAML builder for listpatch for level ups. See https://openkh.dev/kh2/file/type/00battle.html#lvup."""

    def __init__(self, source_name: str):
        self.data: dict[str, dict[int, dict[str, Any]]] = {"Sora": {}, "Donald": {}, "Goofy": {}, "PingMulan": {}, "Beast": {}, "Sparrow": {}, "Aladdin": {}, "Jack": {}, "Auron": {}, "Simba": {}, "Tron": {}, "Riku": {},}
        self.source_name = source_name
        with open(resource_path("static/LvupList.yml"), "r") as file:
            list_data = yaml.safe_load(file)
        self.yaml_list_data = list_data

    def add_sora_level(
        self,
        level: int,
        experience: int,
        strength: int,
        magic: int,
        defense: int,
        ap: int,
        sword_ability: int,
        shield_ability: int,
        staff_ability: int,
        padding: int,
    ):
        self.data["Sora"][level] = {
            "Character": "Sora",
            "Level": level,
            "Exp": experience,
            "Strength": strength,
            "Magic": magic,
            "Defense": defense,
            "Ap": ap,
            "SwordAbility": sword_ability,
            "ShieldAbility": shield_ability,
            "StaffAbility": staff_ability,
            "Padding": padding,
        }

    def add_companion_level(
        self,
        level: int,
        experience: int,
        strength: int,
        magic: int,
        defense: int,
        ap: int,
        companion_name: str,
        padding: int,
    ):
        self.data[companion_name][level] = {
            "Character": companion_name,
            "Level": level,
            "Exp": experience,
            "Strength": strength,
            "Magic": magic,
            "Defense": defense,
            "Ap": ap,
            "SwordAbility": 0,
            "ShieldAbility": 0,
            "StaffAbility": 0,
            "Padding": padding,
        }

    def get_companion_levels(self, companion_name: str):
        for entry in self.yaml_list_data:
            if entry == companion_name:
                return self.yaml_list_data[entry]

    def write_to_zip_file(self, zip_file: ZipFile):
        write_yaml_to_zip_file(zip_file, self.source_name, self.data, sort_keys=True)


class Messages:
    """YAML builder for listpatch for items. See the kh2msg section at https://openkh.dev/tool/GUI.ModsManager."""

    def __init__(self, source_name: str, unicode_output: bool = False):
        self.data: list[StrDict] = []
        self.source_name = source_name
        self.unicode_output = unicode_output

    def add_message(self, message_id: int, en: Optional[str] = None, jp: Optional[str] = None):
        entry: StrDict = {"id": message_id}
        if en is not None:
            entry["en"] = en
        if jp is not None:
            entry["jp"] = jp
        self.data.append(entry)

    def write_to_zip_file(self, zip_file: ZipFile):
        if not self.unicode_output:
            write_yaml_to_zip_file(
                zip_file, self.source_name, self.data, sort_keys=False
            )
        else:
            write_unicode_yaml_to_zip_file(
                zip_file, self.source_name, self.data, sort_keys=False
            )


class PlayerParams:
    """YAML builder for listpatch for player params. See https://openkh.dev/kh2/file/type/00battle.html#plrp."""

    def __init__(self, source_name: str):
        self.data: list[dict] = []
        self.source_name = source_name

    def add_player(
        self,
        character_id: int,
        identifier: int,
        hp: int,
        mp: int,
        ap: int,
        armor_slot_max: int,
        accessory_slot_max: int,
        item_slot_max: int,
        items: list[int],
        padding: list[int],
    ):
        self.data.append(
            {
                "Character": character_id,
                "Id": identifier,
                "Hp": hp,
                "Mp": mp,
                "Ap": ap,
                "ArmorSlotMax": armor_slot_max,
                "AccessorySlotMax": accessory_slot_max,
                "ItemSlotMax": item_slot_max,
                "Items": items,
                "Padding": padding,
            }
        )

    def write_to_zip_file(self, zip_file: ZipFile):
        write_yaml_to_zip_file(zip_file, self.source_name, self.data, sort_keys=False)


class ObjectEntries:
    """YAML builder for listpatch for object entries. See https://openkh.dev/kh2/file/type/00objentry.html."""

    def __init__(self, source_name: str):
        self.data: dict[int, StrDict] = {}
        self.source_name = source_name

    def add_object(
            self,
            object_id: int,
            object_type: str,
            subtype: int,
            draw_priority: int,
            weapon_joint: int,
            model_name: str,
            animation_name: str,
            flags: int,
            object_target_type: str,
            padding: int,
            neo_status: int,
            neo_moveset: int,
            weight: float,
            spawn_limiter: int,
            page: int,
            object_shadow_size: str,
            object_form: str,
            spawn_object_1: int,
            spawn_object_2: int,
            spawn_object_3: int,
            spawn_object_4: int,
            no_apdx: bool,
            before: bool,
            fix_color: bool,
            fly: bool,
            scissoring: bool,
            is_pirate: bool,
            wall_occlusion: bool,
            hift: bool,
    ):
        self.data[object_id] = {
            "ObjectId": object_id,
            "ObjectType": object_type,
            "SubType": subtype,
            "DrawPriority": draw_priority,
            "WeaponJoint": weapon_joint,
            "ModelName": model_name,
            "AnimationName": animation_name,
            "Flags": flags,
            "ObjectTargetType": object_target_type,
            "Padding": padding,
            "NeoStatus": neo_status,
            "NeoMoveset": neo_moveset,
            "Weight": weight,
            "SpawnLimiter": spawn_limiter,
            "Page": page,
            "ObjectShadowSize": object_shadow_size,
            "ObjectForm": object_form,
            "SpawnObject1": spawn_object_1,
            "SpawnObject2": spawn_object_2,
            "SpawnObject3": spawn_object_3,
            "SpawnObject4": spawn_object_4,
            "NoApdx": no_apdx,
            "Before": before,
            "FixColor": fix_color,
            "Fly": fly,
            "Scissoring": scissoring,
            "IsPirate": is_pirate,
            "WallOcclusion": wall_occlusion,
            "Hift": hift,
        }

    def write_to_zip_file(self, zip_file: ZipFile):
        write_yaml_to_zip_file(zip_file, self.source_name, self.data, sort_keys=False)


class PrizeTable:
    """YAML builder for listpatch for prize table. See https://openkh.dev/kh2/file/type/00battle.html#przt."""

    def __init__(self, source_name: str):
        self.data: list[dict[str, int]] = []
        self.source_name = source_name

    def has_entries(self):
        return len(self.data) > 0

    def add_prize(
        self,
        identifier: int,
        small_hp_orbs: int,
        big_hp_orbs: int,
        big_money_orbs: int,
        medium_money_orbs: int,
        small_money_orbs: int,
        small_mp_orbs: int,
        big_mp_orbs: int,
        small_drive_orbs: int,
        big_drive_orbs: int,
        item_1: int,
        item_1_percentage: int,
        item_2: int,
        item_2_percentage: int,
        item_3: int,
        item_3_percentage: int,
    ):
        self.data.append(
            {
                "Id": identifier,
                "SmallHpOrbs": small_hp_orbs,
                "BigHpOrbs": big_hp_orbs,
                "BigMoneyOrbs": big_money_orbs,
                "MediumMoneyOrbs": medium_money_orbs,
                "SmallMoneyOrbs": small_money_orbs,
                "SmallMpOrbs": small_mp_orbs,
                "BigMpOrbs": big_mp_orbs,
                "SmallDriveOrbs": small_drive_orbs,
                "BigDriveOrbs": big_drive_orbs,
                "Item1": item_1,
                "Item1Percentage": item_1_percentage,
                "Item2": item_2,
                "Item2Percentage": item_2_percentage,
                "Item3": item_3,
                "Item3Percentage": item_3_percentage,
            }
        )

    def write_to_zip_file(self, zip_file: ZipFile):
        write_yaml_to_zip_file(zip_file, self.source_name, self.data, sort_keys=False)


class Treasures:
    """YAML builder for listpatch for treasures. See https://openkh.dev/kh2/file/type/03system.html#trsr."""

    def __init__(self, source_name: str):
        self.data: dict[int, dict[str, int]] = {}
        self.source_name = source_name

    def add_treasure(self, location_id: int, item_id: int):
        self.data[location_id] = {"ItemId": item_id}

    def write_to_zip_file(self, zip_file: ZipFile):
        write_yaml_to_zip_file(zip_file, self.source_name, self.data, sort_keys=True)


class ATKPObject:
    def __init__(
        self,
        SubId: int,
        Id: int,
        Type: str,
        CriticalAdjust: int,
        Power: int,
        Team: int,
        Element: int,
        EnemyReaction: int,
        EffectOnHit: int,
        KnockbackStrength1: int,
        KnockbackStrength2: int,
        Unknown: int,
        Flags,
        RefactSelf: str,
        RefactOther: str,
        ReflectedMotion: int,
        ReflectedHitBack: int,
        ReflectAction: int,
        ReflectHitSound: int,
        ReflectRC: int,
        ReflectRange: int,
        ReflectAngle: int,
        DamageEffect: int,
        Switch: int,
        Interval: int,
        FloorCheck: int,
        DriveDrain: int,
        RevengeDamage: int,
        AttackTrReaction: str,
        ComboGroup: int,
        RandomEffect: int,
        Kind,
        HPDrain: int,
    ):
        self.SubId = SubId
        self.Id = Id
        self.Type = Type
        self.CriticalAdjust = CriticalAdjust
        self.Power = Power
        self.Team = Team
        self.Element = Element
        self.EnemyReaction = EnemyReaction
        self.EffectOnHit = EffectOnHit
        self.KnockbackStrength1 = KnockbackStrength1
        self.KnockbackStrength2 = KnockbackStrength2
        self.Unknown = Unknown
        self.Flags = Flags
        self.RefactSelf = RefactSelf
        self.RefactOther = RefactOther
        self.ReflectedMotion = ReflectedMotion
        self.ReflectedHitBack = ReflectedHitBack
        self.ReflectAction = ReflectAction
        self.ReflectHitSound = ReflectHitSound
        self.ReflectRC = ReflectRC
        self.ReflectRange = ReflectRange
        self.ReflectAngle = ReflectAngle
        self.DamageEffect = DamageEffect
        self.Switch = Switch
        self.Interval = Interval
        self.FloorCheck = FloorCheck
        self.DriveDrain = DriveDrain
        self.RevengeDamage = RevengeDamage
        self.AttackTrReaction = AttackTrReaction
        self.ComboGroup = ComboGroup
        self.RandomEffect = RandomEffect
        self.Kind = Kind
        self.HPDrain = HPDrain


class AttackEntriesOrganizer:
    def __init__(self, source_name: str):
        self.data: list[dict] = []
        self.source_name = source_name
        with open(resource_path("static/AtkpList.yml"), "r") as file:
            list_data = yaml.safe_load(file)
        self.yaml_list_data = list_data

    def convert_atkp_object_to_dict_and_add_to_data(self, atkp_object: ATKPObject):
        self.data.append(
            {
                "SubId": atkp_object.SubId,
                "Id": atkp_object.Id,
                "Type": atkp_object.Type,
                "CriticalAdjust": atkp_object.CriticalAdjust,
                "Power": atkp_object.Power,
                "Team": atkp_object.Team,
                "Element": atkp_object.Element,
                "EnemyReaction": atkp_object.EnemyReaction,
                "EffectOnHit": atkp_object.EffectOnHit,
                "KnockbackStrength1": atkp_object.KnockbackStrength1,
                "KnockbackStrength2": atkp_object.KnockbackStrength2,
                "Unknown": atkp_object.Unknown,
                "Flags": atkp_object.Flags,
                "RefactSelf": atkp_object.RefactSelf,
                "RefactOther": atkp_object.RefactOther,
                "ReflectedMotion": atkp_object.ReflectedMotion,
                "ReflectedHitBack": atkp_object.ReflectedHitBack,
                "ReflectAction": atkp_object.ReflectAction,
                "ReflectHitSound": atkp_object.ReflectHitSound,
                "ReflectRC": atkp_object.ReflectRC,
                "ReflectRange": atkp_object.ReflectRange,
                "ReflectAngle": atkp_object.ReflectAngle,
                "DamageEffect": atkp_object.DamageEffect,
                "Switch": atkp_object.Switch,
                "Interval": atkp_object.Interval,
                "FloorCheck": atkp_object.FloorCheck,
                "DriveDrain": atkp_object.DriveDrain,
                "RevengeDamage": atkp_object.RevengeDamage,
                "AttackTrReaction": atkp_object.AttackTrReaction,
                "ComboGroup": atkp_object.ComboGroup,
                "RandomEffect": atkp_object.RandomEffect,
                "Kind": atkp_object.Kind,
                "HPDrain": atkp_object.HPDrain,
            }
        )

    def write_to_zip_file(self, zip_file: ZipFile):
        write_yaml_to_zip_file(zip_file, self.source_name, self.data, sort_keys=False)

    def has_entries(self):
        return len(self.data) > 0

    def attack_entry_constructor(self, values):
        return ATKPObject(
            values["SubId"],
            values["Id"],
            values["Type"],
            values["CriticalAdjust"],
            values["Power"],
            values["Team"],
            values["Element"],
            values["EnemyReaction"],
            values["EffectOnHit"],
            values["KnockbackStrength1"],
            values["KnockbackStrength2"],
            values["Unknown"],
            values["Flags"],
            values["RefactSelf"],
            values["RefactOther"],
            values["ReflectedMotion"],
            values["ReflectedHitBack"],
            values["ReflectAction"],
            values["ReflectHitSound"],
            values["ReflectRC"],
            values["ReflectRange"],
            values["ReflectAngle"],
            values["DamageEffect"],
            values["Switch"],
            values["Interval"],
            values["FloorCheck"],
            values["DriveDrain"],
            values["RevengeDamage"],
            values["AttackTrReaction"],
            values["ComboGroup"],
            values["RandomEffect"],
            values["Kind"],
            values["HPDrain"],
        )

    def get_attack_using_ids(self, SubId, Id):
        for attack_entry in self.yaml_list_data:
            if attack_entry["SubId"] == SubId and attack_entry["Id"] == Id:
                return self.attack_entry_constructor(attack_entry)

    # Used specifically for entries that have the same Id and SubId
    def get_attack_using_ids_plus_switch(self, SubId, Id, Switch):
        for attack_entry in self.yaml_list_data:
            if (
                attack_entry["SubId"] == SubId
                and attack_entry["Id"] == Id
                and attack_entry["Switch"] == Switch
            ):
                return self.attack_entry_constructor(attack_entry)

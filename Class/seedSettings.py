import copy
import json
import random
import string
import textwrap
from dataclasses import dataclass
from enum import Enum

from bitstring import BitArray
from khbr.randomizer import Randomizer as khbr

from Class import settingkey
from Class.exceptions import SettingsException
from List.ItemList import Items
from List.configDict import (
    HintType,
    expCurve,
    itemBias,
    itemRarity,
    itemDifficulty,
    locationType,
    locationDepth,
    BattleLevelOption,
    StartingMovementOption,
    SoraLevelOption,
    location_depth_choices,
    ItemAccessibilityOption,
    SoftlockPreventionOption,
    AbilityPoolOption,
    StartingVisitMode,
)
from List.inventory import ability, misc, proof, storyunlock
from Module import encoding, field2d
from Module import knockbackTypes
from Module.knockbackTypes import KnockbackTypes
from Module.field2d import CommandMenuRandomizer, RoomTransitionImageRandomizer
from Module.progressionPoints import ProgressionPoints

# Characters available to be used for short encoding of certain settings
single_select_chars = string.digits + string.ascii_letters
SHORT_SELECT_LIMIT = len(single_select_chars)


def _format_list_for_spoiler(values: list[str]) -> str:
    if len(values) > 0:
        return ", ".join(values)
    else:
        return "(none)"


class SettingGroup(str, Enum):
    """
    Serves to provide a rough grouping of settings. Not necessarily meant to designate where things should live in the
    seed generator UI; rather, meant to give a way for settings to be grouped for things like the spoiler log.
    """

    LOCATIONS = "Locations"
    EXP_STATS = "EXP/Stats"
    STARTING_INVENTORY = "Starting Inventory"
    HINTS = "Hints"
    KEYBLADES = "Keyblades"
    ITEM_POOL = "Item Pool"
    ITEM_PLACEMENT = "Item Placement"
    SEED_MODIFIERS = "Seed Modifiers"
    COMPANIONS = "Companions"
    BOSS_RANDO = "Randomized Bosses"
    ENEMY_RANDO = "Randomized Enemies"
    COSMETICS = "Cosmetics"


class Setting:
    def __init__(
        self,
        name: str,
        setting_type: type,
        group: SettingGroup,
        ui_label: str,
        shared: bool,
        default,
        tooltip: str,
        standalone_label: str,
        randomizable,
    ):
        self.name = name
        self.group = group
        self.type = setting_type
        self.ui_label = ui_label
        self.shared = shared
        self.default = default
        self.tooltip = textwrap.dedent(tooltip).strip()
        if standalone_label == "":
            self.standalone_label = ui_label
        else:
            self.standalone_label = standalone_label
        self.randomizable = randomizable

    def settings_string(self, value) -> str:
        raise NotImplementedError

    def parse_settings_string(self, settings_string: str):
        raise NotImplementedError

    def spoiler_log_entries(self, value) -> dict[str, str]:
        return {self.standalone_label: f"{value}"}


class Toggle(Setting):
    def __init__(
        self,
        name: str,
        group: SettingGroup,
        ui_label: str,
        shared: bool,
        default: bool,
        tooltip: str = "",
        standalone_label: str = "",
        randomizable=None,
    ):
        super().__init__(
            name,
            bool,
            group,
            ui_label,
            shared,
            default,
            tooltip,
            standalone_label,
            randomizable,
        )

    def settings_string(self, value) -> str:
        return "1" if value else "0"

    def parse_settings_string(self, settings_string: str):
        return True if settings_string == "1" else False


class IntSpinner(Setting):
    def __init__(
        self,
        name: str,
        group: SettingGroup,
        ui_label: str,
        minimum: int,
        maximum: int,
        step: int,
        shared: bool,
        default: int,
        tooltip: str = "",
        standalone_label: str = "",
        randomizable=None,
    ):
        super().__init__(
            name,
            int,
            group,
            ui_label,
            shared,
            default,
            tooltip,
            standalone_label,
            randomizable,
        )
        self.min = minimum
        self.max = maximum
        self.step = step

        self.selectable_values = [
            value for value in range(minimum, maximum + step, step)
        ]

    def settings_string(self, value) -> str:
        index = self.selectable_values.index(value)
        return encoding.v2r(index)

    def parse_settings_string(self, settings_string: str):
        index = encoding.r2v(settings_string)
        return self.selectable_values[index]


class FloatSpinner(Setting):
    def __init__(
        self,
        name: str,
        group: SettingGroup,
        ui_label: str,
        minimum: float,
        maximum: float,
        step: float,
        shared: bool,
        default: float,
        tooltip: str = "",
        standalone_label: str = "",
        randomizable=None,
    ):
        super().__init__(
            name,
            float,
            group,
            ui_label,
            shared,
            default,
            tooltip,
            standalone_label,
            randomizable,
        )
        self.min = minimum
        self.max = maximum
        self.step = step

        selectable_values = []
        value = minimum
        while value <= maximum:
            selectable_values.append(value)
            value = value + step
        self.selectable_values = selectable_values

    def settings_string(self, value) -> str:
        index = self.selectable_values.index(value)
        return encoding.v2r(index)

    def parse_settings_string(self, settings_string: str):
        index = encoding.r2v(settings_string)
        return self.selectable_values[index]


class SingleSelect(Setting):
    def __init__(
        self,
        name: str,
        group: SettingGroup,
        ui_label: str,
        choices: dict[str, str],
        shared: bool,
        default: str,
        tooltip: str = "",
        standalone_label: str = "",
        randomizable=None,
    ):
        super().__init__(
            name,
            str,
            group,
            ui_label,
            shared,
            default,
            tooltip,
            standalone_label,
            randomizable,
        )
        self.choices = choices
        self.choice_keys = list(choices.keys())
        self.choice_values = list(choices.values())

    def settings_string(self, value) -> str:
        index = self.choice_keys.index(value)
        return encoding.v2r(index)

    def parse_settings_string(self, settings_string: str):
        index = encoding.r2v(settings_string)
        return self.choice_keys[index]

    def spoiler_log_entries(self, value) -> dict[str, str]:
        index = self.choice_keys.index(value)
        return {self.standalone_label: self.choice_values[index]}


class ProgressionChainSelect(Setting):
    def __init__(
        self,
        name: str,
        group: SettingGroup,
        ui_label: str,
        shared: bool,
        tooltip: str = "",
        standalone_label: str = "",
        randomizable=None,
    ):
        self.progression = ProgressionPoints()
        default = self.progression.get_compressed()
        super().__init__(
            name,
            str,
            group,
            ui_label,
            shared,
            default,
            tooltip,
            standalone_label,
            randomizable,
        )

    def settings_string(self, value) -> str:
        self.progression.set_uncompressed(value)
        return self.progression.get_compressed()

    def parse_settings_string(self, settings_string: str):
        self.progression.set_uncompressed(settings_string)
        return self.progression.get_compressed()

    def spoiler_log_entries(self, value) -> dict[str, str]:
        return {self.standalone_label: f"{self.progression.settings_spoiler_json()}"}


class MultiSelect(Setting):
    def __init__(
        self,
        name: str,
        group: SettingGroup,
        ui_label: str,
        choices: dict[str, str],
        shared: bool,
        default: list[str],
        choice_icons: dict[str, str] = None,
        tooltip: str = "",
        standalone_label: str = "",
        randomizable=None,
    ):
        super().__init__(
            name,
            str,
            group,
            ui_label,
            shared,
            default,
            tooltip,
            standalone_label,
            randomizable,
        )
        self.choices = choices
        self.choice_keys = list(choices.keys())
        self.choice_values = list(choices.values())
        self.choice_icons = choice_icons

    def settings_string(self, value) -> str:
        choice_keys = self.choice_keys

        bit_array = BitArray(len(choice_keys))
        for index, choice_key in enumerate(choice_keys):
            if choice_key in value:
                bit_array[index] = True
            else:
                bit_array[index] = False

        encoded = encoding.v2r(bit_array.uint)
        return encoded

    def parse_settings_string(self, settings_string: str):
        choice_keys = self.choice_keys

        decoded = encoding.r2v(settings_string)
        bit_array = BitArray(uint=decoded, length=len(choice_keys))

        selected_values = []
        for index, choice_key in enumerate(choice_keys):
            if bit_array[index]:
                selected_values.append(choice_key)

        return selected_values

    def spoiler_log_entries(self, value) -> dict[str, str]:
        selected_values = []
        for choice_key, choice_value in self.choices.items():
            if choice_key in value:
                selected_values.append(choice_value)
        return {self.standalone_label: _format_list_for_spoiler(selected_values)}


class WorldRandomizationTristate(Setting):
    def __init__(
        self,
        name: str,
        group: SettingGroup,
        ui_label: str,
        choices: dict[str, str],
        shared: bool,
        default: list[list[str], list[str]],
        choice_icons: dict[str, str] = None,
        tooltip: str = "",
        standalone_label: str = "",
        randomizable=None,
    ):
        super().__init__(
            name,
            str,
            group,
            ui_label,
            shared,
            default,
            tooltip,
            standalone_label,
            randomizable,
        )
        self.choices = choices
        self.choice_keys = list(choices.keys())
        self.choice_values = list(choices.values())
        self.choice_icons = choice_icons

    def settings_string(self, value) -> str:
        choice_keys = self.choice_keys

        bit_array = BitArray(len(choice_keys))
        bit_array_partial = BitArray(len(choice_keys))
        for index, choice_key in enumerate(choice_keys):
            if isinstance(value[0], list):
                if choice_key in value[0]:
                    bit_array[index] = True
                else:
                    bit_array[index] = False
                if choice_key in value[1]:
                    bit_array_partial[index] = True
                else:
                    bit_array_partial[index] = False
            else:
                if choice_key in value:
                    bit_array[index] = True
                else:
                    bit_array[index] = False
        return encoding.v2r(bit_array.uint) + "+" + encoding.v2r(bit_array_partial.uint)

    def parse_settings_string(self, settings_string: str):
        choice_keys = self.choice_keys
        split_settings = settings_string.split("+")

        bit_array = BitArray(
            uint=encoding.r2v(split_settings[0]), length=len(choice_keys)
        )
        bit_array_partial = BitArray(
            uint=encoding.r2v(split_settings[1]), length=len(choice_keys)
        )

        selected_values = []
        partial_values = []
        for index, choice_key in enumerate(choice_keys):
            if bit_array[index]:
                selected_values.append(choice_key)
        for index, choice_key in enumerate(choice_keys):
            if bit_array_partial[index]:
                partial_values.append(choice_key)

        return [selected_values, partial_values]

    def spoiler_log_entries(self, value) -> dict[str, str]:
        # Expects a list of 2 other lists, one for randomized world keys and one for vanilla world keys.
        # Anything not in those lists is assumed junk.
        if not isinstance(value, list):
            return {}
        if len(value) != 2:
            return {}
        randomized_keys: list[str] = value[0]
        vanilla_keys: list[str] = value[1]
        randomized_worlds: list[str] = []
        vanilla_worlds: list[str] = []
        junk_worlds: list[str] = []
        for choice_key, choice_value in self.choices.items():
            if choice_key in randomized_keys:
                randomized_worlds.append(choice_value)
            elif choice_key in vanilla_keys:
                vanilla_worlds.append(choice_value)
            else:
                junk_worlds.append(choice_value)
        return {
            "Randomized Worlds": _format_list_for_spoiler(randomized_worlds),
            "Vanilla Worlds": _format_list_for_spoiler(vanilla_worlds),
            "Junk Worlds": _format_list_for_spoiler(junk_worlds),
        }


class TextureRecolorsSetting(Setting):
    def __init__(
        self,
        name: str,
        group: SettingGroup,
        ui_label: str,
        shared: bool,
        default: dict[str, dict[str, str]],
        tooltip: str = "",
        standalone_label: str = "",
        randomizable=None,
    ):
        super().__init__(
            name,
            dict,
            group,
            ui_label,
            shared,
            default,
            tooltip,
            standalone_label,
            randomizable,
        )

    def settings_string(self, value) -> str:
        return json.dumps(value)

    def parse_settings_string(self, settings_string: str):
        return json.loads(settings_string)


_drive_exp_curve_tooltip_text = textwrap.dedent(
    """
        Experience curve options, inspired by KH1's experience curves. Midday and Dusk reduce the total experience
        needed to get to Level 7, but levels 2-4 require more experience to compensate.
        
        Dawn - The default experience rate.
        
        Midday - Early levels (2-4) require more experience, but later levels (5-7) require less.
        
        Dusk - Early levels (2-4) require even more experience, but later levels (5-7) require even less.
"""
)

_drive_exp_multiplier_tooltip_text = textwrap.dedent(
    """
        Adjusts the amount of experience needed to reach each drive form level.
        For example, setting the multiplier to 2.0 cuts the required experience to reach each level in half.
"""
)

_depth_options_text = textwrap.dedent(
    """

        Anywhere - No restriction.

        Non-Superboss - Cannot be on a superboss (Data Organization/Absent Silhouette/Sephiroth/Terra).
        All other locations are possible.
        
        First Visit - Force into a first visit (only for the 13 main hub worlds with portals).
        
        First Visit Boss - Force onto the first visit boss of a world (only for the 13 main hub worlds with portals).
        
        Second Visit - Force into a second visit (only for the 13 main hub worlds with portals).
        
        Last Story Boss - Force onto the last boss of a world (only for the 13 main hub worlds with portals).
        
        Superbosses - Force onto superbosses only (Data Organization/Absent Silhouette/Sephiroth/Terra).
        
        Non First Visits - Opposite of the first visit depth. Anywhere but the first visit of the 13 portal worlds (can include drives/levels/100 acre).
"""
)


def _location_unlock_setting(key: str, location: locationType) -> IntSpinner:
    unlock = storyunlock.story_unlock_for_location(location)
    return IntSpinner(
        name=key,
        group=SettingGroup.LOCATIONS,
        ui_label=f"{location}",
        standalone_label=f"{location} Unlocks",
        shared=True,
        minimum=0,
        maximum=storyunlock.story_unlock_for_location(location).visit_count,
        step=1,
        default=0,
        tooltip=f"Number of visits to unlock in {location}. Visits are unlocked with {unlock.name}.",
    )


def _weighted_item_setting(key: str, item_type: str):
    return SingleSelect(
        name=key,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label=item_type,
        standalone_label=f"{item_type} Placement Bias",
        choices={
            itemBias.VERY_EARLY: "Very Early (Scaled)",
            itemBias.EARLY: "Earlier (Scaled)",
            itemBias.SLIGHTLY_EARLY: "Early (Twice as Likely)",
            itemBias.NOBIAS: "None (Normal)",
            itemBias.SLIGHTLY_LATE: "Late (Twice as Likely)",
            itemBias.LATE: "Later (Scaled)",
            itemBias.VERY_LATE: "Very Late (Scaled)",
            itemBias.SUPER_LATE: "Extremely Late (Scaled)",
            itemBias.NIGHTMARE: "Latest (Scaled)",
        },
        shared=True,
        default=itemBias.NOBIAS,
        randomizable=[
            itemBias.EARLY,
            itemBias.SLIGHTLY_EARLY,
            itemBias.NOBIAS,
            itemBias.SLIGHTLY_LATE,
            itemBias.LATE,
        ],
        tooltip=f"""
        Bias the placement of {item_type} based on how difficult/easy you'd like accessing these items to be.
        
        Very Early (Scaled) - Equivalent to Earlier (Scaled) with more bias to the early locations.
        
        Earlier (Scaled) - Items in the category are more likely to be placed in the earliest locations, with the
        likelihood decreasing as locations get later.
        
        Early (Twice as Likely) - Items in the category are (equally) twice as likely to be placed in the first half of
        locations.
        
        None (Normal) - Items in the category are equally likely to be placed anywhere.
        
        Late (Twice as Likely) - Items in the category are (equally) twice as likely to be placed in the second half of
        locations.
        
        Later (Scaled) - Items in the category are less likely to be placed in the earliest locations, with the
        likelihood increasing as locations get later.
        
        Very Late (Scaled) - Equivalent to Later (Scaled) with more bias to the late locations.
        
        Extremely Late (Scaled) - Equivalent to Very Late (Scaled) with even more bias to the late locations.
        
        Latest (Scaled) - Items are _drastically_ biased towards the latest locations.
        """,
    )


_all_settings = [
    SingleSelect(
        name=settingkey.SORA_LEVELS,
        group=SettingGroup.LOCATIONS,
        ui_label="Max Level Reward",
        choices={
            SoraLevelOption.LEVEL_1: "Level 1",
            SoraLevelOption.LEVEL_50: "Level 50",
            SoraLevelOption.LEVEL_99: "Level 99",
        },
        shared=True,
        default=SoraLevelOption.LEVEL_50,
        randomizable=True,
        tooltip="Maximum Level for randomized rewards.",
    ),
    Toggle(
        name=settingkey.SPLIT_LEVELS,
        group=SettingGroup.LOCATIONS,
        ui_label="Dream Weapon Matters",
        shared=True,
        default=False,
        tooltip="""
        Makes the dream weapon choice at the beginning of the game change when you get items/abilities on levels
        (either with the same offsets as the vanilla game, or the adjusted values for max level 50).
        """,
        randomizable=True,
    ),
    Toggle(
        name=settingkey.STATSANITY,
        group=SettingGroup.ITEM_POOL,
        ui_label="Bonus Rewards as Items (Statsanity)",
        shared=True,
        default=True,
        randomizable=True,
        tooltip="""
        Takes HP, MP, Drive, Accessory Slot, Armor Slot, and Item Slot upgrades from their normal bonus locations and
        lets them appear in chests or other locations. Those bonus locations can now have other items in them.
        """,
    ),
    FloatSpinner(
        name=settingkey.SORA_EXP_MULTIPLIER,
        group=SettingGroup.EXP_STATS,
        ui_label="Sora",
        standalone_label="Sora EXP Multiplier",
        minimum=0.5,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=2.0,
        randomizable=True,
        tooltip="""
        Adjusts the amount of experience needed to reach each level.
        For example, setting the multiplier to 2.0 cuts the required experience to reach each level in half.
        """,
    ),
    FloatSpinner(
        name=settingkey.VALOR_EXP_MULTIPLIER,
        group=SettingGroup.EXP_STATS,
        ui_label="Valor",
        standalone_label="Valor EXP Multiplier",
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=7.0,
        randomizable=True,
        tooltip=_drive_exp_multiplier_tooltip_text,
    ),
    FloatSpinner(
        name=settingkey.WISDOM_EXP_MULTIPLIER,
        group=SettingGroup.EXP_STATS,
        ui_label="Wisdom",
        standalone_label="Wisdom EXP Multiplier",
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=3.0,
        randomizable=True,
        tooltip=_drive_exp_multiplier_tooltip_text,
    ),
    FloatSpinner(
        name=settingkey.LIMIT_EXP_MULTIPLIER,
        group=SettingGroup.EXP_STATS,
        ui_label="Limit",
        standalone_label="Limit EXP Multiplier",
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=4.0,
        randomizable=True,
        tooltip=_drive_exp_multiplier_tooltip_text,
    ),
    FloatSpinner(
        name=settingkey.MASTER_EXP_MULTIPLIER,
        group=SettingGroup.EXP_STATS,
        ui_label="Master",
        standalone_label="Master EXP Multiplier",
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=3.0,
        randomizable=True,
        tooltip=_drive_exp_multiplier_tooltip_text,
    ),
    FloatSpinner(
        name=settingkey.FINAL_EXP_MULTIPLIER,
        group=SettingGroup.EXP_STATS,
        ui_label="Final",
        standalone_label="Final EXP Multiplier",
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=3.5,
        randomizable=True,
        tooltip=_drive_exp_multiplier_tooltip_text,
    ),
    FloatSpinner(
        name=settingkey.SUMMON_EXP_MULTIPLIER,
        group=SettingGroup.EXP_STATS,
        ui_label="Summon",
        standalone_label="Summon EXP Multiplier",
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=2.0,
        randomizable=True,
        tooltip="""
        Adjusts the amount of experience needed to reach each summon level.
        For example, setting the multiplier to 2.0 cuts the required experience to reach each level in half.
        """,
    ),
    SingleSelect(
        name=settingkey.SORA_EXP_CURVE,
        group=SettingGroup.EXP_STATS,
        ui_label="Sora",
        standalone_label="Sora EXP Curve",
        choices={
            expCurve.DAWN.name: "Dawn (Normal)",
            expCurve.MIDDAY.name: "Midday",
            expCurve.DUSK.name: "Dusk",
        },
        shared=True,
        default=expCurve.DAWN.name,
        tooltip="""
        Experience curve options, inspired by KH1's experience curves. Midday and Dusk reduce the total experience
        needed to get to level 99, but levels up to 50 require more experience to compensate.
        
        Dawn - The default experience rate.
        
        Midday - Early levels (up to 50) require more experience, but levels 51-99 require less.
        
        Dusk - Early levels (up to 50) require even more experience, but levels 51-99 require even less.
        """,
        randomizable=True,
    ),
    SingleSelect(
        name=settingkey.VALOR_EXP_CURVE,
        group=SettingGroup.EXP_STATS,
        ui_label="Valor",
        standalone_label="Valor EXP Curve",
        choices={
            expCurve.DAWN.name: "Dawn (Normal)",
            expCurve.MIDDAY.name: "Midday",
            expCurve.DUSK.name: "Dusk",
        },
        shared=True,
        default=expCurve.MIDDAY.name,
        tooltip=_drive_exp_curve_tooltip_text,
        randomizable=True,
    ),
    SingleSelect(
        name=settingkey.WISDOM_EXP_CURVE,
        group=SettingGroup.EXP_STATS,
        ui_label="Wisdom",
        standalone_label="Wisdom EXP Curve",
        choices={
            expCurve.DAWN.name: "Dawn (Normal)",
            expCurve.MIDDAY.name: "Midday",
            expCurve.DUSK.name: "Dusk",
        },
        shared=True,
        default=expCurve.DAWN.name,
        tooltip=_drive_exp_curve_tooltip_text,
        randomizable=True,
    ),
    SingleSelect(
        name=settingkey.LIMIT_EXP_CURVE,
        group=SettingGroup.EXP_STATS,
        ui_label="Limit",
        standalone_label="Limit EXP Curve",
        choices={
            expCurve.DAWN.name: "Dawn (Normal)",
            expCurve.MIDDAY.name: "Midday",
            expCurve.DUSK.name: "Dusk",
        },
        shared=True,
        default=expCurve.MIDDAY.name,
        tooltip=_drive_exp_curve_tooltip_text,
        randomizable=True,
    ),
    SingleSelect(
        name=settingkey.MASTER_EXP_CURVE,
        group=SettingGroup.EXP_STATS,
        ui_label="Master",
        standalone_label="Master EXP Curve",
        choices={
            expCurve.DAWN.name: "Dawn (Normal)",
            expCurve.MIDDAY.name: "Midday",
            expCurve.DUSK.name: "Dusk",
        },
        shared=True,
        default=expCurve.MIDDAY.name,
        tooltip=_drive_exp_curve_tooltip_text,
        randomizable=True,
    ),
    SingleSelect(
        name=settingkey.FINAL_EXP_CURVE,
        group=SettingGroup.EXP_STATS,
        ui_label="Final",
        standalone_label="Final EXP Curve",
        choices={
            expCurve.DAWN.name: "Dawn (Normal)",
            expCurve.MIDDAY.name: "Midday",
            expCurve.DUSK.name: "Dusk",
        },
        shared=True,
        default=expCurve.DAWN.name,
        tooltip=_drive_exp_curve_tooltip_text,
        randomizable=True,
    ),
    SingleSelect(
        name=settingkey.SUMMON_EXP_CURVE,
        group=SettingGroup.EXP_STATS,
        ui_label="Summon",
        standalone_label="Summon EXP Curve",
        choices={
            expCurve.DAWN.name: "Dawn (Normal)",
            expCurve.MIDDAY.name: "Midday",
            expCurve.DUSK.name: "Dusk",
        },
        shared=True,
        default=expCurve.DAWN.name,
        tooltip=_drive_exp_curve_tooltip_text,
        randomizable=True,
    ),
    Toggle(
        name=settingkey.CRITICAL_BONUS_REWARDS,
        group=SettingGroup.LOCATIONS,
        ui_label="Critical Bonuses",
        standalone_label="Critical Bonuses in Pool",
        shared=True,
        default=True,
        randomizable=True,
        tooltip="Critical Mode Only! When enabled, non-junk items can be in the 7 starting items on critical mode.",
    ),
    Toggle(
        name=settingkey.GARDEN_OF_ASSEMBLAGE_REWARDS,
        group=SettingGroup.LOCATIONS,
        ui_label="Garden of Assemblage",
        standalone_label="Garden of Assemblage in Pool",
        shared=True,
        default=True,
        randomizable=True,
        tooltip="Randomizes the items in the treasure chests in the Garden of Assemblage.",
    ),
    Toggle(
        name=settingkey.AUTO_EQUIP_START_ABILITIES,
        group=SettingGroup.STARTING_INVENTORY,
        ui_label="Starting Abilities Equipped",
        shared=True,
        default=False,
        tooltip="Start with abilities auto-equipped (except ones from critical bonuses).",
    ),
    SingleSelect(
        name=settingkey.STARTING_MOVEMENT,
        group=SettingGroup.STARTING_INVENTORY,
        ui_label="Growth Ability Starting Level",
        choices={
            StartingMovementOption.DISABLED: "None",
            StartingMovementOption.RANDOM_3: "3 Random",
            StartingMovementOption.RANDOM_5: "5 Random",
            StartingMovementOption.LEVEL_1: "Level 1",
            StartingMovementOption.LEVEL_2: "Level 2",
            StartingMovementOption.LEVEL_3: "Level 3",
            StartingMovementOption.LEVEL_4: "Max",
        },
        shared=True,
        default="Level_1",
        tooltip="""
        None - No guaranteed starting growth.
        
        3 Random - Start with 3 individual growths at random.
        
        5 Random - Start with 5 individual growths at random.
        
        Level 1 - Start with level 1 of all growth abilities.
        
        Level 2 - Start with level 2 of all growth abilities.
        
        Level 3 - Start with level 3 of all growth abilities.
        
        Max - Start with the maximum level of all growth abilities.
        """,
        randomizable=[
            StartingMovementOption.DISABLED,
            StartingMovementOption.RANDOM_3,
            StartingMovementOption.RANDOM_5,
            StartingMovementOption.LEVEL_1,
            StartingMovementOption.LEVEL_2,
            StartingMovementOption.LEVEL_3,
            StartingMovementOption.LEVEL_4,
        ],
    ),
    IntSpinner(
        name=settingkey.STARTING_REPORTS,
        group=SettingGroup.STARTING_INVENTORY,
        ui_label="Starting Ansem Reports",
        standalone_label="# Starting Ansem Reports",
        minimum=0,
        maximum=13,
        step=1,
        shared=True,
        default=0,
        randomizable=[0, 1, 2, 3],
        tooltip="Start with this number of Ansem Reports already obtained.",
    ),
    MultiSelect(
        name=settingkey.STARTING_INVENTORY,
        group=SettingGroup.STARTING_INVENTORY,
        ui_label="Starting Inventory",
        choices={
            str(ability.Scan.id): ability.Scan.name,
            str(ability.NoExperience.id): ability.NoExperience.name,
            str(ability.AerialRecovery.id): ability.AerialRecovery.name,
            str(ability.Guard.id): ability.Guard.name,
            str(ability.FinishingPlus.id): ability.FinishingPlus.name,
            str(misc.HadesCupTrophy.id): misc.HadesCupTrophy.name,
            str(misc.OlympusStone.id): misc.OlympusStone.name,
            str(misc.UnknownDisk.id): misc.UnknownDisk.name,
            str(proof.ProofOfConnection.id): proof.ProofOfConnection.name,
            str(proof.ProofOfNonexistence.id): proof.ProofOfNonexistence.name,
            str(proof.ProofOfPeace.id): proof.ProofOfPeace.name,
            # TODO: misc.PromiseCharm.name is "PromiseCharm", need to see if that matters before committing to change
            str(misc.PromiseCharm.id): "Promise Charm",
        },
        shared=True,
        default=[],
        tooltip="Start with the selected items/abilities already obtained.",
    ),
    SingleSelect(
        name=settingkey.HINT_SYSTEM,
        group=SettingGroup.HINTS,
        ui_label="Hint System",
        choices={
            HintType.DISABLED: "Disabled",
            HintType.SHANANAS: "Shananas",
            HintType.JSMARTEE: "JSmartee",
            HintType.POINTS: "Points",
            HintType.PATH: "Path",
            HintType.SPOILER: "Spoiler",
        },
        shared=True,
        default=HintType.SHANANAS,
        tooltip="""
        Which hint system to use. More detailed explanations the hint systems can be found on the website.
    
        Disabled - Use no hint system.
        
        JSmartee - Ansem Reports reveal how many "important checks" are in a world.
        
        Shananas - Each world informs you once the world has no more "important checks".
        
        Points - Each "important check" is assigned a point value, and you are told the number of points in each
        world. Ansem Reports reveal where items are.
        
        Path - Ansem Reports will tell you if a world contains "breadcrumbs" left by a world that has a proof.
        "Breadcrumbs" being vanilla important checks from a world.
        
        Spoiler - Reveal "Important Check" locations in a world at the start of a seed.
        """,
        randomizable=[
            HintType.SHANANAS,
            HintType.JSMARTEE,
            HintType.POINTS,
            HintType.PATH,
            HintType.SPOILER,
        ],
    ),
    Toggle(
        name=settingkey.PROGRESSION_HINTS,
        group=SettingGroup.HINTS,
        ui_label="Progression Hint Mode",
        shared=True,
        default=False,
        tooltip="""
        Instead of Ansem Reports providing the source of hints, world progress unlocks more hints in your tracker.
        """,
        randomizable=True,
    ),
    Toggle(
        name=settingkey.PROGRESSION_HINTS_REVEAL_END,
        group=SettingGroup.HINTS,
        ui_label="Reveal All Hints When Done",
        shared=True,
        default=False,
        tooltip="""
        Make all hints reveal themselves when you beat Final Xemnas.
        """,
        randomizable=False,
    ),
    IntSpinner(
        name=settingkey.PROGRESSION_HINTS_REPORT_BONUS,
        group=SettingGroup.HINTS,
        ui_label="Progression Report Reward",
        minimum=0,
        maximum=5,
        step=1,
        shared=True,
        default=0,
        tooltip="""
        When you find an Ansem Report, how many points toward your hints you get.
        """,
        randomizable=False,
    ),
    IntSpinner(
        name=settingkey.PROGRESSION_HINTS_COMPLETE_BONUS,
        group=SettingGroup.HINTS,
        ui_label="Progression World Complete Reward",
        minimum=0,
        maximum=5,
        step=1,
        shared=True,
        default=0,
        tooltip="""
        When a world is finished, how many additional points you receive for progressing.
        """,
        randomizable=False,
    ),
    ProgressionChainSelect(
        name=settingkey.PROGRESSION_POINT_SELECT,
        group=SettingGroup.HINTS,
        ui_label="",
        standalone_label="Progression Point Values",
        shared=True,
        tooltip="""
        Point values for different checkpoints in worlds.
        """,
        randomizable=False,
    ),
    IntSpinner(
        name=settingkey.POINTS_PROOF,
        group=SettingGroup.HINTS,
        ui_label="Proof",
        standalone_label="Proof Point Value",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=5,
        tooltip="Point value for each Proof.",
    ),
    IntSpinner(
        name=settingkey.POINTS_FORM,
        group=SettingGroup.HINTS,
        ui_label="Drive Form",
        standalone_label="Drive Form Point Value",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=9,
        tooltip="Point value for each Drive Form.",
    ),
    IntSpinner(
        name=settingkey.POINTS_MAGIC,
        group=SettingGroup.HINTS,
        ui_label="Magic",
        standalone_label="Magic Point Value",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=7,
        tooltip="Point value for each Magic.",
    ),
    IntSpinner(
        name=settingkey.POINTS_SUMMON,
        group=SettingGroup.HINTS,
        ui_label="Summon",
        standalone_label="Summon Point Value",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=5,
        tooltip="Point value for each Summon.",
    ),
    IntSpinner(
        name=settingkey.POINTS_ABILITY,
        group=SettingGroup.HINTS,
        ui_label="Second Chance/Once More",
        standalone_label="Second Chance/Once More Point Value",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=5,
        tooltip="Point value for each of the Second Chance and Once More abilities.",
    ),
    IntSpinner(
        name=settingkey.POINTS_PAGE,
        group=SettingGroup.HINTS,
        ui_label="Torn Page",
        standalone_label="Torn Page Point Value",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=5,
        tooltip="Point value for each Torn Page.",
    ),
    IntSpinner(
        name=settingkey.POINTS_VISIT,
        group=SettingGroup.HINTS,
        ui_label="Visit Unlock",
        standalone_label="Visit Unlock Point Value",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=5,
        tooltip="Point value for each Visit Unlock.",
    ),
    IntSpinner(
        name=settingkey.POINTS_REPORT,
        group=SettingGroup.HINTS,
        ui_label="Ansem Report",
        standalone_label="Ansem Report Point Value",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=3,
        tooltip="Point value for each Ansem Report.",
    ),
    IntSpinner(
        name=settingkey.POINTS_KEYBLADES,
        group=SettingGroup.HINTS,
        ui_label="Locking Keyblades",
        standalone_label="Locking Keyblades Point Value",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=9,
        tooltip="Point value for each keyblade that locks chests.",
    ),
    IntSpinner(
        name=settingkey.POINTS_AUX,
        group=SettingGroup.HINTS,
        ui_label="Aux. Unlock",
        standalone_label="Aux. Unlock Point Value",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=1,
        tooltip="Point value for each Aux. Unlock.",
    ),
    IntSpinner(
        name=settingkey.POINTS_MAGIC_COLLECT,
        group=SettingGroup.HINTS,
        ui_label="Magic Set",
        standalone_label="Magic Set Bonus Points",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=0,
        tooltip="Bonus points for collecting all Magic.",
    ),
    IntSpinner(
        name=settingkey.POINTS_PAGE_COLLECT,
        group=SettingGroup.HINTS,
        ui_label="Torn Page Set",
        standalone_label="Torn Page Set Bonus Points",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=0,
        tooltip="Bonus points for collecting all Torn Pages.",
    ),
    IntSpinner(
        name=settingkey.POINTS_POUCHES_COLLECT,
        group=SettingGroup.HINTS,
        ui_label="Munny Pouch Set",
        standalone_label="Munny Pouch Set Bonus Points",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=0,
        tooltip="Bonus points for collecting all Munny Pouches.",
    ),
    IntSpinner(
        name=settingkey.POINTS_PROOF_COLLECT,
        group=SettingGroup.HINTS,
        ui_label="Proof Set",
        standalone_label="Proof Set Bonus Points",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=0,
        tooltip="Bonus points for collecting all Proofs.",
    ),
    IntSpinner(
        name=settingkey.POINTS_FORM_COLLECT,
        group=SettingGroup.HINTS,
        ui_label="Drive Form Set",
        standalone_label="Drive Form Set Bonus Points",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=0,
        tooltip="Bonus points for collecting all Drive Forms.",
    ),
    IntSpinner(
        name=settingkey.POINTS_SUMMON_COLLECT,
        group=SettingGroup.HINTS,
        ui_label="Summon Set",
        standalone_label="Summon Set Bonus Points",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=0,
        tooltip="Bonus points for collecting all Summons.",
    ),
    IntSpinner(
        name=settingkey.POINTS_ABILITY_COLLECT,
        group=SettingGroup.HINTS,
        ui_label="Ability Set",
        standalone_label="Ability Set Bonus Points",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=0,
    ),
    IntSpinner(
        name=settingkey.POINTS_REPORT_COLLECT,
        group=SettingGroup.HINTS,
        ui_label="Ansem Report Set",
        standalone_label="Ansem Report Set Bonus Points",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=0,
        tooltip="Bonus points for collecting all Ansem Reports.",
    ),
    IntSpinner(
        name=settingkey.POINTS_VISIT_COLLECT,
        group=SettingGroup.HINTS,
        ui_label="Visit Unlock Set",
        standalone_label="Visit Unlock Set Bonus Points",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=0,
        tooltip="Bonus points for collecting all Visit Unlocks.",
    ),
    IntSpinner(
        name=settingkey.POINTS_BONUS,
        group=SettingGroup.HINTS,
        ui_label="Bonus Level",
        standalone_label="Bonus Level Point Value",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=10,
    ),
    IntSpinner(
        name=settingkey.POINTS_COMPLETE,
        group=SettingGroup.HINTS,
        ui_label="World Completion",
        standalone_label="World Completion Point Value",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=10,
    ),
    IntSpinner(
        name=settingkey.POINTS_FORMLV,
        group=SettingGroup.HINTS,
        ui_label="Form Level",
        standalone_label="Form Level Point Value",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=3,
    ),
    IntSpinner(
        name=settingkey.POINTS_DEATH,
        group=SettingGroup.HINTS,
        ui_label="Death Penalty",
        standalone_label="Death Penalty Point Value",
        minimum=-1000,
        maximum=1000,
        step=1,
        shared=True,
        default=-10,
    ),
    IntSpinner(
        name=settingkey.POINTS_BOSS_NORMAL,
        group=SettingGroup.HINTS,
        ui_label="Normal Boss Defeated",
        standalone_label="Normal Boss Defeated Point Value",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=10,
    ),
    IntSpinner(
        name=settingkey.POINTS_BOSS_AS,
        group=SettingGroup.HINTS,
        ui_label="Absent Silhouette Defeated",
        standalone_label="Absent Silhouette Defeated Point Value",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=20,
    ),
    IntSpinner(
        name=settingkey.POINTS_BOSS_DATA,
        group=SettingGroup.HINTS,
        ui_label="Data Boss Defeated",
        standalone_label="Data Boss Defeated Point Value",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=30,
    ),
    IntSpinner(
        name=settingkey.POINTS_BOSS_SEPHIROTH,
        group=SettingGroup.HINTS,
        ui_label="Sephiroth Defeated",
        standalone_label="Sephiroth Defeated Point Value",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=40,
    ),
    IntSpinner(
        name=settingkey.POINTS_BOSS_TERRA,
        group=SettingGroup.HINTS,
        ui_label="Lingering Will Defeated",
        standalone_label="Lingering Will Defeated Point Value",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=50,
    ),
    IntSpinner(
        name=settingkey.POINTS_BOSS_FINAL,
        group=SettingGroup.HINTS,
        ui_label="Final Xemnas Defeated",
        standalone_label="Final Xemnas Defeated Point Value",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=100,
    ),
    SingleSelect(
        name=settingkey.REPORT_DEPTH,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Ansem Report Depth",
        choices=location_depth_choices(),
        shared=True,
        default=locationDepth.NonSuperboss,
        tooltip="The set of locations in which Ansem Reports are allowed to be placed."
        + _depth_options_text,
        randomizable=[
            locationDepth.SecondVisitOnly,
            locationDepth.NonSuperboss,
            locationDepth.FirstBoss,
            locationDepth.Anywhere,
        ],
    ),
    SingleSelect(
        name=settingkey.PROOF_DEPTH,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Proof Depth",
        choices=location_depth_choices(),
        shared=True,
        default=locationDepth.Anywhere,
        tooltip="The set of locations in which Proofs are allowed to be placed."
        + _depth_options_text,
        randomizable=[
            locationDepth.SecondVisitOnly,
            locationDepth.NonSuperboss,
            locationDepth.LastStoryBoss,
            locationDepth.Anywhere,
        ],
    ),
    SingleSelect(
        name=settingkey.PROMISE_CHARM_DEPTH,
        group=SettingGroup.ITEM_POOL,
        ui_label="Promise Charm Depth",
        choices=location_depth_choices(),
        shared=True,
        default=locationDepth.Anywhere,
        tooltip="The set of locations in which the Promise Charm is allowed to be placed (if enabled)."
        + _depth_options_text,
        randomizable=[
            locationDepth.SecondVisitOnly,
            locationDepth.NonSuperboss,
            locationDepth.LastStoryBoss,
            locationDepth.Anywhere,
        ],
    ),
    SingleSelect(
        name=settingkey.STORY_UNLOCK_DEPTH,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Visit Unlock Depth",
        choices=location_depth_choices(),
        shared=True,
        default=locationDepth.Anywhere,
        tooltip="The set of locations in which Visit Unlocks are allowed to be placed."
        + _depth_options_text,
        randomizable=[
            locationDepth.FirstVisit,
            locationDepth.NonSuperboss,
            locationDepth.FirstBoss,
            locationDepth.LastStoryBoss,
            locationDepth.Anywhere,
        ],
    ),
    SingleSelect(
        name=settingkey.BATTLE_LEVEL_RANDO,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Battle Level Choice",
        choices={option.name: option.value for option in list(BattleLevelOption)},
        shared=True,
        default=BattleLevelOption.NORMAL.name,
        tooltip="""
        Changes the battle levels of worlds.
        
        Normal - Battle levels are unchanged.
        
        Shuffle - Shuffle the normal battle levels among all visits of all worlds.
        
        Offset - Increase/Decrease all battle levels by a given amount.
        
        Within Range of Normal - Vary battle levels of all visits within a set number above or below normal.
        
        Random (Max 50) - All battle levels are random, with a maximum level of 50.
        
        Scale to 50 - All last visits are level 50, with previous visits scaled proportionally.
        """,
        standalone_label="Battle Level Randomization",
        randomizable=True,
    ),
    IntSpinner(
        name=settingkey.BATTLE_LEVEL_OFFSET,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Level Offset",
        minimum=-50,
        maximum=100,
        step=5,
        shared=True,
        default=0,
        standalone_label="Battle Level Offset (if chosen)",
        tooltip="How many battle levels to change the worlds by.",
        randomizable=[-20, -15, -10, 0, 10, 15, 20],
    ),
    IntSpinner(
        name=settingkey.BATTLE_LEVEL_RANGE,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Level Range",
        minimum=0,
        maximum=50,
        step=5,
        shared=True,
        default=0,
        standalone_label="Battle Level Range (if chosen)",
        tooltip="How far above or below normal battle levels to choose.",
        randomizable=[0, 20],
    ),
    Toggle(
        name=settingkey.YEET_THE_BEAR,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Yeet The Bear Required",
        shared=True,
        default=False,
        tooltip="Forces the Proof of Nonexistence onto the Starry Hill popup in 100 Acre Wood",
    ),
    Toggle(
        name=settingkey.CHAIN_LOGIC,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Chain Logic Enabled",
        shared=True,
        default=False,
        tooltip="Places all the locking items in a chain with one another, making the seed very linear.",
    ),
    Toggle(
        name=settingkey.CHAIN_LOGIC_TERRA,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Include Lingering Will in Chain",
        shared=True,
        default=False,
        tooltip="Puts the Proof of Connection into the logic chain, effectively requiring beating Lingering Will.",
    ),
    Toggle(
        name=settingkey.CHAIN_LOGIC_MIN_TERRA,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Force Late Depth for Proof of Connection",
        standalone_label="Force Late Depth for Proof of Connection (Chain Logic)",
        shared=True,
        default=False,
        tooltip="Forces the Proof of Connection to be in the last 5 steps of the chain, to give more chances for finding combat tools.",
    ),
    IntSpinner(
        name=settingkey.CHAIN_LOGIC_LENGTH,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Maximum Logic Length",
        standalone_label="Maximum Logic Chain Length",
        minimum=10,
        maximum=26,  # theoretical max
        step=1,
        shared=True,
        default=26,
        tooltip="How many steps in the logic chain you'd like to do at most.",
    ),
    Toggle(
        name=settingkey.PREVENT_SELF_HINTING,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Remove Self-Hinting Reports",
        shared=True,
        default=False,
        tooltip="Each Ansem Report must hint a world that is different from where that report was found.",
    ),
    Toggle(
        name=settingkey.ALLOW_PROOF_HINTING,
        group=SettingGroup.HINTS,
        ui_label="Reports can Reveal Proofs",
        shared=True,
        default=False,
        tooltip="If enabled, proofs can be directly revealed by Ansem Reports.",
    ),
    Toggle(
        name=settingkey.ALLOW_REPORT_HINTING,
        group=SettingGroup.HINTS,
        ui_label="Reports can Reveal other Reports",
        shared=True,
        default=True,
        tooltip="If enabled, Ansem Reports can reveal other Ansem Reports.",
    ),
    Toggle(
        name=settingkey.SCORE_MODE,
        group=SettingGroup.HINTS,
        ui_label="Hi-Score Mode",
        shared=True,
        default=False,
        tooltip="If enabled, gain points for collecting Important Checks, completing worlds, beating bosses, etc.",
    ),
    MultiSelect(
        name=settingkey.HINTABLE_CHECKS,
        group=SettingGroup.HINTS,
        ui_label="Hintable Items",
        choices={
            "magic": "Magic",
            "form": "Drive Forms",
            "summon": "Summon Charms",
            "page": "Torn Pages",
            "ability": "Second Chance/Once More",
            "report": "Ansem Reports",
            "visit": "Visit Unlocks",
            "proof": "Proofs",
            "keyblade": "Chest Locking Keyblades",
            "other": "Aux. Unlocks",
        },
        shared=True,
        default=[
            "magic",
            "form",
            "summon",
            "page",
            "ability",
            "report",
            "visit",
            "proof",
        ],
    ),
    MultiSelect(
        name=settingkey.SPOILER_REVEAL_TYPES,
        group=SettingGroup.HINTS,
        ui_label="Spoiled Items",
        choices={
            "magic": "Magic",
            "form": "Drive Forms",
            "summon": "Summon Charms",
            "page": "Torn Pages",
            "ability": "Second Chance/Once More",
            "report": "Ansem Reports",
            "visit": "Visit Unlocks",
            "proof": "Proofs",
            "keyblade": "Chest Locking Keyblades",
            "other": "Aux. Unlocks",
        },
        shared=True,
        default=[
            "magic",
            "form",
            "summon",
            "page",
            "ability",
            "report",
            "visit",
            "proof",
        ],
    ),
    Toggle(
        name=settingkey.REVEAL_COMPLETE,
        group=SettingGroup.HINTS,
        ui_label="Reveal World Completion",
        shared=True,
        default=True,
        tooltip="If enabled, the tracker will reveal when all Important Checks in a world are found.",
    ),
    SingleSelect(
        name=settingkey.REPORTS_REVEAL,
        group=SettingGroup.HINTS,
        ui_label="Report Reveal Mode",
        choices={
            "Disabled": "Disabled",
            "reportmode": "Worlds",
            "bossreports": "Randomized Bosses",
        },
        shared=True,
        default="reportmode",
        tooltip="""
        Configures how Ansem Reports reveal information.
    
        Disabled - All worlds will be revealed at the start.
        
        Worlds - Ansem Reports reveal the Important Checks in a world.
        
        Randomized Bosses - Ansem Reports reveal what a boss has randomized into (Requires Boss randomizer).
        """,
        randomizable=None,
    ),
    SingleSelect(
        name=settingkey.JOURNAL_HINTS_ABILITIES,
        group=SettingGroup.HINTS,
        ui_label="Abilities in Journal Reports",
        choices={
            "Off": "Off",
            "world": "World of Ability",
            "exact": "Exact Location",
        },
        shared=True,
        default="Off",
        tooltip="""
        If enabled, Ansem Reports in Jiminy's Journal reveal the locations of many useful abilities.

        Off - No ability locations are revealed.
        
        World of Ability - Ansem Reports in the Journal reveal which world contains each hinted ability. For example,
        "Berserk Charge is in Olympus Coliseum."

        Exact Location - Ansem Reports in the Journal reveal the exact location of each hinted ability. For example,
        "Berserk Charge is at Olympus Coliseum - Urns."
        """,
        randomizable=None,
    ),
    IntSpinner(
        name=settingkey.KEYBLADE_MIN_STAT,
        group=SettingGroup.KEYBLADES,
        ui_label="Keyblade Min Stat",
        minimum=0,
        maximum=20,
        step=1,
        shared=True,
        default=0,
        randomizable=True,
        tooltip="The minimum strength and magic stat that each keyblade must have.",
    ),
    IntSpinner(
        name=settingkey.KEYBLADE_MAX_STAT,
        group=SettingGroup.KEYBLADES,
        ui_label="Keyblade Max Stat",
        minimum=0,
        maximum=20,
        step=1,
        shared=True,
        default=7,
        randomizable=True,
        tooltip="The maximum strength and magic stat that each keyblade must have.",
    ),
    MultiSelect(
        name=settingkey.KEYBLADE_SUPPORT_ABILITIES,
        group=SettingGroup.KEYBLADES,
        ui_label="Support Keyblade-Eligible Abilities",
        choices={
            str(item.Id): item.Name
            for item in Items.getSupportAbilityList() + Items.getLevelAbilityList()
        },
        shared=True,
        default=list(
            set(
                [
                    str(item.Id)
                    for item in Items.getSupportAbilityList()
                    + Items.getLevelAbilityList()
                ]
            )
        ),
        tooltip="Selected abilities may randomize onto keyblades. Unselected abilities will not be on keyblades.",
    ),
    MultiSelect(
        name=settingkey.KEYBLADE_ACTION_ABILITIES,
        group=SettingGroup.KEYBLADES,
        ui_label="Action Keyblade-Eligible Abilities",
        choices={str(item.Id): item.Name for item in Items.getActionAbilityList()},
        shared=True,
        default=[],
        tooltip="Selected abilities may randomize onto keyblades. Unselected abilities will not be on keyblades.",
    ),
    WorldRandomizationTristate(
        name=settingkey.WORLDS_WITH_REWARDS,
        group=SettingGroup.LOCATIONS,
        ui_label="Worlds with Rewards",
        choices={
            location.name: location.value
            for location in [
                locationType.Level,
                locationType.FormLevel,
                locationType.STT,
                locationType.TT,
                locationType.HB,
                locationType.BC,
                locationType.OC,
                locationType.Agrabah,
                locationType.LoD,
                locationType.HUNDREDAW,
                locationType.PL,
                locationType.DC,
                locationType.HT,
                locationType.PR,
                locationType.SP,
                locationType.TWTNW,
                locationType.Atlantica,
            ]
        },
        shared=True,
        default=[
            [
                locationType.Level.name,
                locationType.FormLevel.name,
                locationType.STT.name,
                locationType.HB.name,
                locationType.OC.name,
                locationType.LoD.name,
                locationType.PL.name,
                locationType.HT.name,
                locationType.SP.name,
                locationType.TT.name,
                locationType.BC.name,
                locationType.Agrabah.name,
                locationType.HUNDREDAW.name,
                locationType.DC.name,
                locationType.PR.name,
                locationType.TWTNW.name,
            ],
            [],
        ],
        choice_icons={
            locationType.Level.name: "static/icons/worlds/sora.png",
            locationType.FormLevel.name: "static/icons/worlds/drives.png",
            locationType.STT.name: "static/icons/worlds/simulated_twilight_town.png",
            locationType.HB.name: "static/icons/worlds/hollow_bastion.png",
            locationType.OC.name: "static/icons/worlds/olympus_coliseum.png",
            locationType.LoD.name: "static/icons/worlds/land_of_dragons.png",
            locationType.PL.name: "static/icons/worlds/pride_lands.png",
            locationType.HT.name: "static/icons/worlds/halloween_town.png",
            locationType.SP.name: "static/icons/worlds/space_paranoids.png",
            locationType.TT.name: "static/icons/worlds/twilight_town.png",
            locationType.BC.name: "static/icons/worlds/beast's_castle.png",
            locationType.Agrabah.name: "static/icons/worlds/agrabah.png",
            locationType.HUNDREDAW.name: "static/icons/worlds/100_acre_wood.png",
            locationType.DC.name: "static/icons/worlds/disney_castle.png",
            locationType.PR.name: "static/icons/worlds/port_royal.png",
            locationType.TWTNW.name: "static/icons/worlds/the_world_that_never_was.png",
            locationType.Atlantica.name: "static/icons/worlds/atlantica.png",
        },
        randomizable=True,
        tooltip="""
        Configures the reward placement for a world.
    
        Rando - Fully randomized locations, can have junk or unique items.
        
        Vanilla - Notable unique items are placed in their original locations for KH2FM.
        All other locations will get junk items.
        
        Junk - All locations use items from the junk item pool.
        """,
    ),
    MultiSelect(
        name=settingkey.SUPERBOSSES_WITH_REWARDS,
        group=SettingGroup.LOCATIONS,
        ui_label="Superbosses with Rewards",
        choices={
            location.name: location.value
            for location in [
                locationType.AS,
                locationType.DataOrg,
                locationType.Sephi,
                locationType.LW,
            ]
        },
        shared=True,
        default=[locationType.AS.name, locationType.Sephi.name],
        choice_icons={
            locationType.AS.name: "static/icons/bosses/as.png",
            locationType.DataOrg.name: "static/icons/bosses/datas.png",
            locationType.Sephi.name: "static/icons/bosses/sephiroth.png",
            locationType.LW.name: "static/icons/bosses/lingering_will.png",
        },
        randomizable=True,
    ),
    MultiSelect(
        name=settingkey.MISC_LOCATIONS_WITH_REWARDS,
        group=SettingGroup.LOCATIONS,
        ui_label="Misc Locations with Rewards",
        choices={
            location.name: location.value
            for location in [
                locationType.OCCups,
                locationType.OCParadoxCup,
                locationType.Puzzle,
                locationType.CoR,
                locationType.TTR,
                locationType.SYNTH,
            ]
        },
        shared=True,
        default=[locationType.CoR.name],
        choice_icons={
            locationType.OCCups.name: "static/icons/misc/cups.png",
            locationType.OCParadoxCup.name: "static/icons/misc/paradox_cup.png",
            locationType.Puzzle.name: "static/icons/misc/puzzle.png",
            locationType.CoR.name: "static/icons/worlds/cavern_of_remembrance.png",
            locationType.TTR.name: "static/icons/misc/transport.png",
            locationType.SYNTH.name: "static/icons/misc/moogle.png",
        },
        randomizable=True,
    ),
    IntSpinner(
        name=settingkey.SORA_STR_RATE,
        group=SettingGroup.EXP_STATS,
        ui_label="Sora Strength Rate",
        minimum=0,
        maximum=100,
        step=1,
        shared=True,
        default=25,
        randomizable=True,
        tooltip="How likely to get STR upgrades on level up (relative to the other stats)",
    ),
    IntSpinner(
        name=settingkey.SORA_MAG_RATE,
        group=SettingGroup.EXP_STATS,
        ui_label="Sora Magic Rate",
        minimum=0,
        maximum=100,
        step=1,
        shared=True,
        default=25,
        randomizable=True,
        tooltip="How likely to get MAG upgrades on level up (relative to the other stats)",
    ),
    IntSpinner(
        name=settingkey.SORA_DEF_RATE,
        group=SettingGroup.EXP_STATS,
        ui_label="Sora Defense Rate",
        minimum=0,
        maximum=100,
        step=1,
        shared=True,
        default=25,
        randomizable=True,
        tooltip="How likely to get DEF upgrades on level up (relative to the other stats)",
    ),
    IntSpinner(
        name=settingkey.SORA_AP_RATE,
        group=SettingGroup.EXP_STATS,
        ui_label="Sora AP Rate",
        minimum=0,
        maximum=100,
        step=1,
        shared=True,
        default=25,
        randomizable=True,
        tooltip="How likely to get AP upgrades on level up (relative to the other stats)",
    ),
    MultiSelect(
        name=settingkey.JUNK_ITEMS,
        group=SettingGroup.ITEM_POOL,
        ui_label="Junk Items",
        choices={str(item.Id): item.Name for item in Items.getJunkList(False)},
        shared=True,
        default=list(set([str(item.Id) for item in Items.getJunkList(False)])),
        tooltip="""
        Once all of the required items are placed, items from this list are used to fill the rest.
        This item pool is also used for locations that are set to contain only junk or are disabled.
        """,
    ),
    IntSpinner(
        name=settingkey.SORA_AP,
        group=SettingGroup.EXP_STATS,
        ui_label="Sora Starting AP",
        minimum=0,
        maximum=150,
        step=25,
        shared=True,
        default=50,
        randomizable=True,
        tooltip="Sora starts with this much AP.",
    ),
    IntSpinner(
        name=settingkey.DONALD_AP,
        group=SettingGroup.COMPANIONS,
        ui_label="Donald Starting AP",
        minimum=5,
        maximum=55,
        step=5,
        shared=True,
        default=55,
        randomizable=True,
        tooltip="Donald starts with this much AP.",
    ),
    IntSpinner(
        name=settingkey.GOOFY_AP,
        group=SettingGroup.COMPANIONS,
        ui_label="Goofy Starting AP",
        minimum=4,
        maximum=54,
        step=5,
        shared=True,
        default=54,
        randomizable=True,
        tooltip="Goofy starts with this much AP.",
    ),
    Toggle(
        name=settingkey.ANTIFORM,
        group=SettingGroup.ITEM_POOL,
        ui_label="Antiform",
        standalone_label="Obtainable Antiform",
        shared=True,
        default=False,
        tooltip="Adds Antiform as an obtainable form.",
    ),
    Toggle(
        name=settingkey.FIFTY_AP_BOOSTS,
        group=SettingGroup.ITEM_POOL,
        ui_label="50 AP Boosts",
        shared=True,
        default=True,
        tooltip="Adds 50 guaranteed AP boosts into the item pool.",
    ),
    Toggle(
        name=settingkey.REMOVE_DAMAGE_CAP,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Remove Damage Cap",
        shared=True,
        default=False,
        tooltip="Removes the damage cap for every enemy/boss in the game.",
    ),
    Toggle(
        name=settingkey.CUPS_GIVE_XP,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Cups Give Experience",
        shared=True,
        default=False,
        tooltip="Defeating enemies while in an Olympus Coliseum Cup will give you experience and Form experience.",
    ),
    SingleSelect(
        name=settingkey.REVENGE_LIMIT_RANDO,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Randomize Revenge Limit Maximum (Beta)",
        shared=True,
        choices={
            "Vanilla": "Vanilla",
            "Set 0": "Set 0",
            "Set Infinity": "Set Infinity",
            "Random Swap": "Random Swap",
            "Random Values": "Random Values",
        },
        default="Vanilla",
        tooltip="Randomizes the revenge value limit of each enemy/boss in the game. Can be either set to 0, set to basically infinity, randomly swapped, or set to a random value between 0 and 200",
    ),
    Toggle(
        name=settingkey.CHESTS_MATCH_ITEM,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Chest Visuals Match Contents",
        shared=True,
        default=False,
        tooltip="Chests are given unique visuals based on the type of item they contain.",
    ),
    Toggle(
        name=settingkey.PARTY_MEMBER_RANDO,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Randomize World Party Members (Beta)",
        shared=True,
        default=False,
        tooltip="Randomizes the World Character party member in each world.",
    ),
    Toggle(
        name=settingkey.AS_DATA_SPLIT,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Split AS/Data Rewards",
        shared=True,
        default=False,
        tooltip="""
        When enabled, Absent Silhouette rewards will NOT give the reward from their Data Organization versions.
        You must beat the Data Organization version to get its reward.
        """,
    ),
    Toggle(
        name=settingkey.RETRY_DFX,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Retry Data Final Xemnas",
        shared=True,
        default=False,
        tooltip="""
        If you die to Data Final Xemnas, Continue will put you right back into the fight, instead of having to fight
        Data Xemnas I again.
         
        WARNING: This will be an effective softlock if you are unable to beat Data Final Xemnas.
        """,
    ),
    Toggle(
        name=settingkey.RETRY_DARK_THORN,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Retry Dark Thorn",
        shared=True,
        default=False,
        tooltip="""
        If you die to Dark Thorn, Continue will put you right back into the fight, instead of having to fight
        Shadow Stalker again.
         
        WARNING: This will be an effective softlock if you are unable to beat Dark Thorn.
        """,
    ),
    Toggle(
        name=settingkey.SKIP_CARPET_ESCAPE,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Skip Magic Carpet Escape",
        shared=True,
        default=False,
        tooltip="After reaching Ruined Chamber in Agrabah, the magic carpet escape sequence will be skipped.",
    ),
    Toggle(
        name=settingkey.PR_MAP_SKIP,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Remove Port Royal Map Select",
        shared=True,
        default=True,
        tooltip="Changes Port Royal map screen with text options, useful for avoiding crashes in PC.",
    ),
    Toggle(
        name=settingkey.ATLANTICA_TUTORIAL_SKIP,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Skip Atlantica Minigame Tutorial",
        shared=True,
        default=False,
        tooltip="Skips the Atlantica Music Tutorial (not the swimming tutorial).",
    ),
    Toggle(
        name=settingkey.REMOVE_WARDROBE_ANIMATION,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Remove Wardrobe Wakeup Animation",
        shared=True,
        default=False,
        tooltip="The wardrobe in Beast's Castle will not wake up when pushing it.",
    ),
    Toggle(
        name=settingkey.REMOVE_CUTSCENES,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Remove Cutscenes",
        shared=True,
        default=False,
        tooltip="Removes all cutscenes from the game. As a consequence there are occassionally strange flashes/backgrounds when in a spot a cutscene would normally occur.",
    ),
    Toggle(
        name=settingkey.COSTUME_RANDO,
        group=SettingGroup.COSMETICS,
        ui_label="Randomize Character Costumes (Beta)",
        shared=False,
        default=False,
        tooltip="Randomizes the different costumes that Sora/Donald/Goofy switch between in the different worlds (IE Space Paranoids could now be default sora, while anywhere default sora is used could be Christmas Town Sora.",
    ),
    Toggle(
        name=settingkey.FAST_URNS,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Fast Olympus Coliseum Urns",
        shared=True,
        default=False,
        tooltip="The urns in the minigame in Olympus Coliseum drop more orbs, making the minigame much faster.",
        randomizable=False,
    ),
    Toggle(
        name=settingkey.RICH_ENEMIES,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="All Enemies Drop Munny",
        shared=True,
        default=False,
        tooltip="Enemies will all drop munny.",
        randomizable=True,
    ),
    Toggle(
        name=settingkey.UNLIMITED_MP,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="All Enemies Drop MP Orbs",
        shared=True,
        default=False,
        tooltip="Enemies will all drop MP orbs.",
        randomizable=True,
    ),
    IntSpinner(
        name=settingkey.GLOBAL_JACKPOT,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Global Jackpots",
        standalone_label="# of Global Jackpots",
        minimum=0,
        maximum=3,
        step=1,
        shared=True,
        default=0,
        tooltip="""
        Increases orb/munny drops as if you had this many Jackpots equipped.
        Each Jackpot adds 50 percent of the original amount.
        """,
        randomizable=True,
    ),
    IntSpinner(
        name=settingkey.GLOBAL_LUCKY,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Global Lucky Lucky",
        standalone_label="# of Global Lucky Lucky",
        minimum=0,
        maximum=3,
        step=1,
        shared=True,
        default=0,
        tooltip="""
        Increases item drops as if you had this many Lucky Lucky abilities equipped.
        Each Lucky Lucky adds 50 percent of the chance to drop the item.
        """,
        randomizable=True,
    ),
    Toggle(
        name=settingkey.SHOP_KEYBLADES,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Keyblades",
        standalone_label="Keyblades in Shop",
        shared=True,
        default=False,
        tooltip="Adds duplicates of keyblades into the moogle shop.",
        randomizable=True,
    ),
    Toggle(
        name=settingkey.SHOP_ELIXIRS,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Elixirs",
        standalone_label="Elixirs in Shop",
        shared=True,
        default=False,
        tooltip="Adds Elixirs/Megalixirs into the moogle shop.",
        randomizable=True,
    ),
    Toggle(
        name=settingkey.SHOP_RECOVERIES,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Drive Recoveries",
        standalone_label="Drive Recoveries in Shop",
        shared=True,
        default=False,
        tooltip="Adds Drive Recovery/High Drive Recovery into the moogle shop.",
        randomizable=True,
    ),
    Toggle(
        name=settingkey.SHOP_BOOSTS,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Stat Boosts",
        standalone_label="Stat Boosts in Shop",
        shared=True,
        default=False,
        tooltip="Adds Power/Magic/AP/Defense Boosts into the moogle shop.",
        randomizable=True,
    ),
    IntSpinner(
        name=settingkey.SHOP_REPORTS,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Add Ansem Reports To Shop",
        standalone_label="# Ansem Reports in Shop",
        shared=True,
        minimum=0,
        maximum=13,
        step=1,
        default=0,
        tooltip="Adds a number of Ansem Reports into the moogle shop.",
        randomizable=[0, 1, 2, 3],
    ),
    IntSpinner(
        name=settingkey.SHOP_UNLOCKS,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Add Visit Unlocks To Shop",
        standalone_label="# Visit Unlocks in Shop",
        shared=True,
        minimum=0,
        maximum=len(storyunlock.all_individual_story_unlocks()),
        step=1,
        default=0,
        tooltip="Adds a number of visit unlocks into the moogle shop.",
        randomizable=[0, 1, 2, 3],
    ),
    Toggle(
        name=settingkey.ROXAS_ABILITIES_ENABLED,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Roxas Magic/Movement/Trinity",
        shared=True,
        default=False,
        tooltip="Allows Roxas to use magic, Sora's movement abilities, and Trinity Limit in Simulated Twilight Town.",
    ),
    Toggle(
        name=settingkey.DISABLE_FINAL_FORM,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Disable Final Form",
        shared=True,
        default=False,
        tooltip="""
        Disables going into Final Form in any way.
        Final Form can still be found to let other forms level up and for Final Genie.
        All items from Final Form are replaced with junk.
        """,
    ),
    Toggle(
        name=settingkey.BLOCK_COR_SKIP,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Block Skipping CoR",
        shared=True,
        default=False,
        tooltip="Disables skipping into the Cavern of Remembrance, requiring completion of the fights to progress.",
    ),
    Toggle(
        name=settingkey.BLOCK_SHAN_YU_SKIP,
        group=SettingGroup.SEED_MODIFIERS,
        ui_label="Block Skipping Shan-Yu",
        shared=True,
        default=False,
        tooltip="Disables skipping into the throne room of Land of Dragons, requiring beating Shan-Yu to progress.",
    ),
    Toggle(
        name=settingkey.ENABLE_PROMISE_CHARM,
        group=SettingGroup.ITEM_POOL,
        ui_label="Promise Charm",
        shared=True,
        default=False,
        tooltip="""
        If enabled, the Promise Charm will be added to the item pool.
        This allows skipping TWTNW by talking to the computer in the Garden of Assemblage when you have all 3 Proofs.
        """,
        randomizable=True,
    ),
    Toggle(
        name=settingkey.KEYBLADES_LOCK_CHESTS,
        group=SettingGroup.LOCATIONS,
        ui_label="Keyblades Unlock Chests",
        shared=True,
        default=False,
        tooltip="""
        When enabled, Sora must have certain keyblades to open chests in the different worlds.
        STT     | Bond of Flame
        TT      | Oathkeeper
        HB      | Sleeping Lion
        CoR     | Winner's Proof
        LoD     | Hidden Dragon
        BC      | Rumbling Rose
        OC      | Hero's Crest
        DC      | Monochrome
        PR      | Follow The Wind
        AG      | Wishing Lamp
        HT      | Decisive Pumpkin
        PL      | Circle of Life
        SP      | Photon Debugger
        TWTNW   | Two Become One
        HAW     | Sweet Memories
        """,
        randomizable=True,
    ),
    SingleSelect(
        name=settingkey.STARTING_VISIT_MODE,
        group=SettingGroup.LOCATIONS,
        ui_label="Mode",
        standalone_label="Visit Availability",
        choices={option.name: option.value for option in list(StartingVisitMode)},
        shared=True,
        default=StartingVisitMode.ALL.name,
        tooltip="""
        How "visits" for worlds that have them (the 13 portal worlds) should be initially available.
        
        All Visits - All visits of all worlds are available from the beginning of the seed.

        First Visits - All first visits are immediately available, but you must find visit unlock items to
        access subsequent visits in each visit-capable world.

        No Visits - No world visits are immediately available, outside of the ones that are always present. You
        must find a visit unlock item in the immediately available areas to proceed. 

        Random Visits - Unlock a random set of visits by starting with random visit unlock items.

        Specific Visits - Unlock a specific set of visits by starting with specific visit unlock items.
        """,
    ),
    IntSpinner(
        name=settingkey.STARTING_VISIT_RANDOM_MIN,
        group=SettingGroup.LOCATIONS,
        ui_label="Minimum Visits Available",
        standalone_label="Min Random Visits Available",
        shared=True,
        minimum=0,
        maximum=len(storyunlock.all_individual_story_unlocks()),
        step=1,
        default=3,
        tooltip="Minimum number of random visits to unlock at the start.",
    ),
    IntSpinner(
        name=settingkey.STARTING_VISIT_RANDOM_MAX,
        group=SettingGroup.LOCATIONS,
        ui_label="Maximum Visits Available",
        standalone_label="Max Random Visits Available",
        shared=True,
        minimum=0,
        maximum=len(storyunlock.all_individual_story_unlocks()),
        step=1,
        default=3,
        tooltip="Maximum number of random visits to unlock at the start.",
    ),
    _location_unlock_setting(key=settingkey.STARTING_UNLOCKS_SP, location=locationType.SP),
    _location_unlock_setting(key=settingkey.STARTING_UNLOCKS_PR, location=locationType.PR),
    _location_unlock_setting(key=settingkey.STARTING_UNLOCKS_TT, location=locationType.TT),
    _location_unlock_setting(key=settingkey.STARTING_UNLOCKS_OC, location=locationType.OC),
    _location_unlock_setting(key=settingkey.STARTING_UNLOCKS_HT, location=locationType.HT),
    _location_unlock_setting(key=settingkey.STARTING_UNLOCKS_LOD, location=locationType.LoD),
    _location_unlock_setting(key=settingkey.STARTING_UNLOCKS_TWTNW, location=locationType.TWTNW),
    _location_unlock_setting(key=settingkey.STARTING_UNLOCKS_BC, location=locationType.BC),
    _location_unlock_setting(key=settingkey.STARTING_UNLOCKS_AG, location=locationType.Agrabah),
    _location_unlock_setting(key=settingkey.STARTING_UNLOCKS_PL, location=locationType.PL),
    _location_unlock_setting(key=settingkey.STARTING_UNLOCKS_HB, location=locationType.HB),
    _location_unlock_setting(key=settingkey.STARTING_UNLOCKS_DC, location=locationType.DC),
    _location_unlock_setting(key=settingkey.STARTING_UNLOCKS_STT, location=locationType.STT),
    Toggle(
        name=settingkey.MAPS_IN_ITEM_POOL,
        group=SettingGroup.ITEM_POOL,
        ui_label="Maps",
        standalone_label="Maps in Item Pool",
        shared=True,
        default=True,
        tooltip="If enabled, maps are included in the required item pool. Disabling frees up more slots for the other 'junk' items.",
    ),
    Toggle(
        name=settingkey.RECIPES_IN_ITEM_POOL,
        group=SettingGroup.ITEM_POOL,
        ui_label="Synthesis Recipes",
        standalone_label="Synthesis Recipes in Item Pool",
        shared=True,
        default=True,
        tooltip="If enabled, recipes are included in the required item pool. Disabling frees up more slots for the other 'junk' items.",
    ),
    Toggle(
        name=settingkey.ACCESSORIES_IN_ITEM_POOL,
        group=SettingGroup.ITEM_POOL,
        ui_label="Accessories",
        standalone_label="Accessories in Item Pool",
        shared=True,
        default=True,
        tooltip="If enabled, all accessories are included in the required item pool.",
    ),
    Toggle(
        name=settingkey.ARMOR_IN_ITEM_POOL,
        group=SettingGroup.ITEM_POOL,
        ui_label="Armor",
        standalone_label="Armor in Item Pool",
        shared=True,
        default=True,
        tooltip="If enabled, all armor items are included in the required item pool.",
    ),
    Toggle(
        name=settingkey.MUNNY_IN_ITEM_POOL,
        group=SettingGroup.ITEM_POOL,
        ui_label="Munny Pouches",
        standalone_label="Munny Pouches in Item Pool",
        shared=True,
        default=True,
        tooltip="If enabled, all munny pouches are included in the required item pool.",
    ),
    Toggle(
        name=settingkey.REMOVE_POPUPS,
        group=SettingGroup.LOCATIONS,
        ui_label="Remove Non-Superboss Popups",
        shared=True,
        default=False,
        tooltip="Removes story popup and bonus rewards from eligble location pool for non-junk items. Used for door-rando primarily.",
        randomizable=False,
    ),
    SingleSelect(
        name=settingkey.STORY_UNLOCK_CATEGORY,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Visit Unlock Category",
        choices={
            itemRarity.COMMON: itemRarity.COMMON,
            itemRarity.UNCOMMON: itemRarity.UNCOMMON,
            itemRarity.RARE: itemRarity.RARE,
            itemRarity.MYTHIC: itemRarity.MYTHIC,
        },
        shared=True,
        default=itemRarity.UNCOMMON,
        randomizable=False,
        tooltip="""
        Change visit unlocks to have one of the 4 categories (Common,Uncommon,Rare,Mythic) that influence what bias
        each item gets when randomizing.
         
        Setting to Rare or Mythic will make these unlocking items more likely to be locked behind other key items
        in the harder item placement difficulties.
        """,
    ),
    SingleSelect(
        name=settingkey.ITEM_PLACEMENT_DIFFICULTY,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Item Placement Difficulty",
        choices={
            itemDifficulty.SUPEREASY: "Super Easy",
            itemDifficulty.EASY: "Easy",
            itemDifficulty.SLIGHTLY_EASY: "Slightly Easy",
            itemDifficulty.NORMAL: "Normal",
            itemDifficulty.SLIGHTLY_HARD: "Slightly Hard",
            itemDifficulty.HARD: "Hard",
            itemDifficulty.VERYHARD: "Very Hard",
            itemDifficulty.INSANE: "Insane",
            itemDifficulty.NIGHTMARE: "Nightmare",
        },
        shared=True,
        default=itemDifficulty.NORMAL,
        randomizable=[
            itemDifficulty.EASY,
            itemDifficulty.SLIGHTLY_EASY,
            itemDifficulty.NORMAL,
            itemDifficulty.SLIGHTLY_HARD,
            itemDifficulty.HARD,
        ],
        tooltip="""
        Bias the placement of items based on how difficult/easy you would like the seed to be. 
        Items have 4 categories (Common, Uncommon, Rare, Mythic) that influence what bias each item gets when placing those items. 
        Super Easy and Easy will bias Rare and Mythic items early, while the Hard settings will bias those later.
        """,
    ),
    _weighted_item_setting(key=settingkey.WEIGHTED_FORMS, item_type="Drive Forms"),
    _weighted_item_setting(key=settingkey.WEIGHTED_UNLOCKS, item_type="Visit Unlocks"),
    _weighted_item_setting(key=settingkey.WEIGHTED_MAGIC, item_type="Magics"),
    _weighted_item_setting(key=settingkey.WEIGHTED_PAGES, item_type="Torn Pages"),
    _weighted_item_setting(key=settingkey.WEIGHTED_SUMMONS, item_type="Summons"),
    _weighted_item_setting(key=settingkey.WEIGHTED_REPORTS, item_type="Ansem Reports"),
    _weighted_item_setting(key=settingkey.WEIGHTED_PROOFS, item_type="Proofs"),
    _weighted_item_setting(key=settingkey.WEIGHTED_PROMISE_CHARM, item_type="Promise Charm"),
    Toggle(
        name=settingkey.NIGHTMARE_LOGIC,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Extended Item Placement Logic",
        shared=True,
        default=False,
        tooltip="Enables weighting for keyblades with good abilities, and puts auto forms and final forcing `in-logic` meaning they may be required to complete the seed.",
        randomizable=True,
    ),
    SingleSelect(
        name=settingkey.SOFTLOCK_CHECKING,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Softlock Prevention",
        choices={
            SoftlockPreventionOption.DEFAULT: "Regular Rando",
            SoftlockPreventionOption.REVERSE: "Reverse Rando",
            SoftlockPreventionOption.BOTH: "Satisfy Regular & Reverse",
        },
        shared=True,
        default=SoftlockPreventionOption.DEFAULT,
        tooltip="""
        What type of rando are you playing?
        
        Regular Rando - The default setting.
        
        Reverse Rando - Playing with visits reversed.
        
        Satisfy Regular & Reverse - Playing cooperatively with both regular and reverse.
        """,
    ),
    SingleSelect(
        name=settingkey.ACCESSIBILITY,
        group=SettingGroup.ITEM_PLACEMENT,
        ui_label="Accessibility",
        standalone_label="Item Accessibility",
        choices={
            ItemAccessibilityOption.ALL: "100% Locations",
            ItemAccessibilityOption.BEATABLE: "Beatable",
        },
        shared=True,
        default=ItemAccessibilityOption.ALL,
        tooltip="""
        How accessible locations need to be for the seed to be "completable".
        
        100% Locations - All locations must be reachable, and nothing will be permanently locked.
        
        Beatable - The 3 Proofs must be reachable, but nothing else is guaranteed. 
        """,
    ),
    SingleSelect(
        name=settingkey.ABILITY_POOL,
        group=SettingGroup.ITEM_POOL,
        ui_label="Ability Pool",
        choices={
            AbilityPoolOption.DEFAULT: "Default Abilities",
            AbilityPoolOption.RANDOMIZE: "Randomize Ability Pool",
            AbilityPoolOption.RANDOMIZE_SUPPORT: "Randomize Support Ability Pool",
            AbilityPoolOption.RANDOMIZE_STACKABLE: "Randomize Stackable Abilities",
        },
        shared=True,
        default=AbilityPoolOption.DEFAULT,
        tooltip="""
        Configures the ability pool randomization.
    
        Randomize Ability Pool - Picks Sora\'s action/support abilities at random
        (guaranteed to have 1 Second Chance and 1 Once More).
         
        Randomize Support Ability Pool - Leaves action abilities alone, but will randomize the support abilities
        (still guaranteed to have 1 Second Chance and 1 Once More).
        
        Randomize Stackable Abilities - Gives 1 of each ability that works on its own, but randomizes how many of
        the stackable abilities you can get (guaranteeing at least 1 of each).
        """,
        randomizable=["default", "randomize support", "randomize stackable"],
    ),
    SingleSelect(
        name=settingkey.COMMAND_MENU,
        group=SettingGroup.COSMETICS,
        ui_label="Command Menu",
        choices=CommandMenuRandomizer.command_menu_options(),
        shared=False,
        default=field2d.VANILLA,
        tooltip="""
        Controls the appearance of the command menu on-screen.
        
        Vanilla - Command menus will have their normal appearance.
        
        Randomize (one) - Chooses a single random command menu to use for the entire game.
        
        Randomize (all) - Chooses random command menus for each world/location that has a unique command menu.
        
        individual command menu options - Forces all command menus to have the chosen appearance.
        """,
    ),
    Toggle(
        name=settingkey.RANDO_THEMED_TEXTURES,
        group=SettingGroup.COSMETICS,
        ui_label="Add Randomizer-Themed Textures",
        shared=False,
        default=False,
        tooltip="""
        If enabled, adds a few KH2 Randomizer-themed textures to the game.
        """,
    ),
    SingleSelect(
        name=settingkey.ROOM_TRANSITION_IMAGES,
        group=SettingGroup.COSMETICS,
        ui_label="Room Transition Images",
        choices=RoomTransitionImageRandomizer.room_transition_options(),
        shared=False,
        default=field2d.VANILLA,
        tooltip="""
        Controls the appearance of the room transition images.
        
        Vanilla - Room transitions will have their normal appearance.
        
        Randomize (in-game only) - Chooses a random transition for each world from existing in-game room transition
        images.
        
        Randomize (custom only) - Chooses a random transition for each world from the room-transition-images folder
        contained within your configured Custom Visuals Folder.
        
        Randomize (in-game + custom) - Chooses a random transition for each world from both existing in-game transition
        images and the room-transition-images folder contained within your configured Custom Visuals Folder.
        """,
    ),
    Toggle(
        name=settingkey.RECOLOR_TEXTURES,
        group=SettingGroup.COSMETICS,
        ui_label="Recolor Some Textures",
        standalone_label="Recolor Some Textures",
        shared=False,
        default=False,
        tooltip="""
        If enabled, allows for basic recoloring of some of the in-game textures.

        Requires the OpenKH folder to be set up in the Configure menu, and for KH2 to have been extracted using the
        OpenKH Mods Manager setup wizard.
        
        This will cause seeds to take longer to generate (relative to the number of recolored textures), especially at
        first, since all of the replacement textures need to be generated.
        """,
    ),
    Toggle(
        name=settingkey.RECOLOR_TEXTURES_KEEP_CACHE,
        group=SettingGroup.COSMETICS,
        ui_label="Keep Previously Generated Textures",
        shared=False,
        default=True,
        tooltip="""
        If enabled, previously generated textures will be kept around to speed up future recolors. This will potentially
        use large amounts of disk space, but improves performance. Disable this option to minimize disk space usage, but
        recoloring will take longer.
        """,
    ),
    TextureRecolorsSetting(
        name=settingkey.TEXTURE_RECOLOR_SETTINGS,
        group=SettingGroup.COSMETICS,
        ui_label="Texture Recolor Settings",
        shared=False,
        default={},
    ),
    Toggle(
        name=settingkey.MUSIC_RANDO_ENABLED_PC,
        group=SettingGroup.COSMETICS,
        ui_label="Randomize Music",
        shared=False,
        default=False,
        tooltip="""
        If enabled, randomizes in-game music.

        See the Randomized Music page on the website for more detailed instructions.
        """,
    ),
    Toggle(
        name=settingkey.MUSIC_RANDO_PC_USE_CATEGORIES,
        group=SettingGroup.COSMETICS,
        ui_label="Categorize Songs",
        shared=False,
        default=True,
        tooltip="""
        If enabled, randomizes music separately by category ("boss" songs are only replaced with other "boss" songs,
        "cutscene" songs are only replaced with other "cutscene" songs, etc.).
        
        If disabled, any song in the list can replace any other song.
        """,
    ),
    Toggle(
        name=settingkey.MUSIC_RANDO_PC_ALLOW_DUPLICATES,
        group=SettingGroup.COSMETICS,
        ui_label="Allow Duplicate Replacements",
        shared=False,
        default=False,
        tooltip="""
        If enabled, song replacements are used multiple times if there aren't enough replacements for every song.

        If disabled, replacement songs are only used once, and some songs will stay un-randomized if there aren't
        enough replacements.
        """,
    ),
    Toggle(
        name=settingkey.MUSIC_RANDO_PC_DMCA_SAFE,
        group=SettingGroup.COSMETICS,
        ui_label="DMCA Safe",
        shared=False,
        default=False,
        tooltip="""
        If enabled, excludes songs from the song list that are known to have some copyright concerns.
        """,
    ),
    Toggle(
        name=settingkey.MUSIC_RANDO_PC_INCLUDE_KH1,
        group=SettingGroup.COSMETICS,
        ui_label="Include KH1 Songs",
        shared=False,
        default=False,
        tooltip="""
        If enabled, includes all the base KH1 songs in the song list for music rando.

        Requires the OpenKH folder to be set up in the Configure menu, and for KH1 to have been extracted using the
        OpenKH Mods Manager setup wizard.
        """,
    ),
    Toggle(
        name=settingkey.MUSIC_RANDO_PC_INCLUDE_KH2,
        group=SettingGroup.COSMETICS,
        ui_label="Include KH2 Songs",
        shared=False,
        default=False,
        tooltip="""
        If enabled, includes all the base KH2 songs in the song list for music rando.

        Requires the OpenKH folder to be set up in the Configure menu.
        """,
    ),
    Toggle(
        name=settingkey.MUSIC_RANDO_PC_INCLUDE_RECOM,
        group=SettingGroup.COSMETICS,
        ui_label="Include Re:Chain of Memories Songs",
        shared=False,
        default=False,
        tooltip="""
        If enabled, includes all the base Re:Chain of Memories songs in the song list for music rando.

        Requires the OpenKH folder to be set up in the Configure menu, and for Re:Chain of Memories to have been
        extracted using the OpenKH Mods Manager setup wizard.
        """,
    ),
    Toggle(
        name=settingkey.MUSIC_RANDO_PC_INCLUDE_BBS,
        group=SettingGroup.COSMETICS,
        ui_label="Include Birth by Sleep Songs",
        shared=False,
        default=False,
        tooltip="""
        If enabled, includes all the base Birth by Sleep songs in the song list for music rando.

        Requires the OpenKH folder to be set up in the Configure menu, and for BBS to have been extracted using the
        OpenKH Mods Manager setup wizard.
        """,
    ),
    Toggle(
        name=settingkey.MUSIC_RANDO_PC_INCLUDE_DDD,
        group=SettingGroup.COSMETICS,
        ui_label="Include Dream Drop Distance Songs",
        shared=False,
        default=False,
        tooltip="""
        If enabled, includes all the base Dream Drop Distance songs in the song list for music rando.

        Requires the OpenKH folder to be set up in the Configure menu, and for DDD to have been extracted using the
        OpenKH Mods Manager setup wizard.
        """,
    ),
    Toggle(
        name=settingkey.MUSIC_RANDO_PC_INCLUDE_CUSTOM,
        group=SettingGroup.COSMETICS,
        ui_label="Include Custom Songs",
        shared=False,
        default=False,
        tooltip="""
        If enabled, includes any added custom music in the song list for music rando.

        Requires the custom music folder to be set up in the Configure menu.
        """,
    ),
    Toggle(
        name=settingkey.DONALD_DAMAGE_TOGGLE,
        group=SettingGroup.COMPANIONS,
        ui_label="Damage to All Enemies and Bosses",
        standalone_label="Donald Damages All Enemies and Bosses",
        shared=True,
        default=False,
        tooltip="""
        If enabled, Donald will deal normal damage to all enemies and bosses instead
        of just one damage. However, the default is for him to have no knockback, so
        if you want him to stun/knockback, change this setting.
        """,
        randomizable=False,
    ),
    SingleSelect(
        name=settingkey.DONALD_MELEE_ATTACKS_KNOCKBACK_TYPE,
        group=SettingGroup.COMPANIONS,
        ui_label="Melee Attack Damage Mode",
        standalone_label="Damage Mode for Donald's Melee Attacks",
        choices=KnockbackTypes.knockback_options(),
        shared=True,
        default=knockbackTypes.JUST_DAMAGE,
        tooltip=KnockbackTypes.damage_type_tooltip(),
    ),
    SingleSelect(
        name=settingkey.DONALD_FIRE_KNOCKBACK_TYPE,
        group=SettingGroup.COMPANIONS,
        ui_label="Donald Fire Damage Mode",
        standalone_label="Damage Mode for Donald Fire",
        choices=KnockbackTypes.knockback_options(),
        shared=True,
        default=knockbackTypes.JUST_DAMAGE,
        tooltip=KnockbackTypes.damage_type_tooltip(),
    ),
    SingleSelect(
        name=settingkey.DONALD_BLIZZARD_KNOCKBACK_TYPE,
        group=SettingGroup.COMPANIONS,
        ui_label="Donald Blizzard Damage Mode",
        standalone_label="Damage Mode for Donald Blizzard",
        choices=KnockbackTypes.knockback_options(),
        shared=True,
        default=knockbackTypes.JUST_DAMAGE,
        tooltip=KnockbackTypes.damage_type_tooltip(),
    ),
    SingleSelect(
        name=settingkey.DONALD_THUNDER_KNOCKBACK_TYPE,
        group=SettingGroup.COMPANIONS,
        ui_label="Donald Thunder Damage Mode",
        standalone_label="Damage Mode for Donald Thunder",
        choices=KnockbackTypes.knockback_options(),
        shared=True,
        default=knockbackTypes.JUST_DAMAGE,
        tooltip=KnockbackTypes.damage_type_tooltip(),
    ),
    Toggle(
        name=settingkey.GOOFY_DAMAGE_TOGGLE,
        group=SettingGroup.COMPANIONS,
        ui_label="Damage to All Enemies and Bosses",
        standalone_label="Goofy Damages all Enemies and Bosses",
        shared=True,
        default=False,
        tooltip="""
        If enabled, Goofy will deal normal damage to all enemies and bosses instead
        of just one damage. However, the default is for him to have no knockback, so
        if you want him to stun/knockback, change this setting.
        """,
        randomizable=False,
    ),
    SingleSelect(
        name=settingkey.GOOFY_MELEE_ATTACKS_KNOCKBACK_TYPE,
        group=SettingGroup.COMPANIONS,
        ui_label="Melee Attack Damage Mode",
        standalone_label="Damage Mode for Goofy's Melee Attacks",
        choices=KnockbackTypes.knockback_options(),
        shared=True,
        default=knockbackTypes.JUST_DAMAGE,
        tooltip=KnockbackTypes.damage_type_tooltip(),
    ),
    SingleSelect(
        name=settingkey.GOOFY_BASH_KNOCKBACK_TYPE,
        group=SettingGroup.COMPANIONS,
        ui_label="Goofy Bash Damage Mode",
        choices=KnockbackTypes.knockback_options(),
        shared=True,
        default=knockbackTypes.JUST_DAMAGE,
        tooltip=KnockbackTypes.damage_type_tooltip(),
    ),
    SingleSelect(
        name=settingkey.GOOFY_TURBO_KNOCKBACK_TYPE,
        group=SettingGroup.COMPANIONS,
        ui_label="Goofy Turbo Damage Mode",
        choices=KnockbackTypes.knockback_options(),
        shared=True,
        default=knockbackTypes.JUST_DAMAGE,
        tooltip=KnockbackTypes.damage_type_tooltip(),
    ),
    SingleSelect(
        name=settingkey.GOOFY_TORNADO_KNOCKBACK_TYPE,
        group=SettingGroup.COMPANIONS,
        ui_label="Goofy Tornado Damage Mode",
        choices=KnockbackTypes.knockback_options(),
        shared=True,
        default=knockbackTypes.JUST_DAMAGE,
        tooltip=KnockbackTypes.damage_type_tooltip(),
    ),
    Toggle(
        name=settingkey.DONALD_KILL_BOSS,
        group=SettingGroup.COMPANIONS,
        ui_label="Donald Can Kill Bosses",
        shared=True,
        default=False,
        tooltip="If enabled, attacks will be able to kill bosses.",
        randomizable=False,
    ),
    Toggle(
        name=settingkey.GOOFY_KILL_BOSS,
        group=SettingGroup.COMPANIONS,
        ui_label="Goofy Can Kill Bosses",
        shared=True,
        default=False,
        tooltip="If enabled, attacks will be able to kill bosses.",
        randomizable=False,
    ),
]


def _get_boss_enemy_settings():
    boss_settings = []
    enemy_settings = []
    boss_enemy_config = khbr()._get_game("kh2").get_options()
    for key in boss_enemy_config.keys():
        if key == "memory_expansion":
            continue
        config = boss_enemy_config[key]

        enemy_type = config.get("type") == "enemy"
        group = SettingGroup.ENEMY_RANDO if enemy_type else SettingGroup.BOSS_RANDO

        possible_values = config["possible_values"]
        if True in possible_values:
            # needs to be a toggle
            ui_widget = Toggle(
                name=key,
                group=group,
                ui_label=config["display_name"],
                shared=True,
                default=False,
                tooltip=config["description"],
            )
        else:
            # single select
            choices = {choice: choice for choice in possible_values}
            ui_widget = SingleSelect(
                name=key,
                group=group,
                ui_label=config["display_name"],
                choices=choices,
                shared=True,
                default=possible_values[0],
                tooltip=config["description"],
            )
        if enemy_type:
            enemy_settings.append(ui_widget)
        else:
            boss_settings.append(ui_widget)
    return boss_settings, enemy_settings


boss_settings, enemy_settings = _get_boss_enemy_settings()
for boss_enemy_setting in boss_settings + enemy_settings:
    _all_settings.append(boss_enemy_setting)

settings_by_name = {setting.name: setting for setting in _all_settings}

DELIMITER = "-"


class SeedSettings:
    def __init__(self):
        self._values = {setting.name: setting.default for setting in _all_settings}
        self._randomizable = [
            setting for setting in _all_settings if setting.randomizable
        ]
        self._observers = {}

    def get(self, name: str):
        return self._values[name]

    def set(self, name: str, value):
        self._values[name] = copy.deepcopy(value)
        if name in self._observers:
            for observer in self._observers[name]:
                observer()

    def observe(self, name: str, observer):
        """Calls the provided observer whenever the setting with the given name is changed."""
        if name in self._observers:
            observers = self._observers[name]
        else:
            observers = []
            self._observers[name] = observers
        observers.append(observer)

        # Trigger an initial observation
        observer()

    def _filtered_settings(self, include_private: bool) -> dict:
        return {
            name: setting
            for (name, setting) in settings_by_name.items()
            if setting.shared or include_private
        }

    def settings_string(self, include_private: bool = False):
        flags: list[bool] = []
        short_select_values = ""
        values: list[str] = []
        for name in sorted(self._filtered_settings(include_private)):
            setting = settings_by_name[name]
            value = self._values[name]
            if isinstance(setting, Toggle):
                flags.append(value)
            elif (
                isinstance(setting, SingleSelect)
                and len(setting.choice_keys) <= SHORT_SELECT_LIMIT
            ):
                index = setting.choice_keys.index(value)
                short_select_values += single_select_chars[index]
            elif (
                isinstance(setting, IntSpinner)
                and len(setting.selectable_values) <= SHORT_SELECT_LIMIT
            ):
                index = setting.selectable_values.index(value)
                short_select_values += single_select_chars[index]
            elif (
                isinstance(setting, FloatSpinner)
                and len(setting.selectable_values) <= SHORT_SELECT_LIMIT
            ):
                index = setting.selectable_values.index(value)
                short_select_values += single_select_chars[index]
            else:
                values.append(setting.settings_string(value))

        # Group up all the single select settings that are small enough and make one group for them to save some space
        values.insert(0, short_select_values)

        # Group up all the toggle/flag settings to save some space
        flags_bit_array = BitArray(len(flags))
        for index, flag in enumerate(flags):
            flags_bit_array[index] = flag
        values.insert(0, encoding.v2r(flags_bit_array.uint))

        return DELIMITER.join(values)

    def apply_settings_string(
        self, settings_string: str, include_private: bool = False
    ):
        parts = settings_string.split(DELIMITER)

        # The first part is an encoded representation of all the toggle/flag settings
        flags_value = encoding.r2v(parts.pop(0))
        # The second part is an encoded representation of other settings that can be represented as single chars
        short_select_string = parts.pop(0)

        toggle_settings = []
        short_select_settings = []

        used_index = 0
        for name in sorted(self._filtered_settings(include_private)):
            setting = settings_by_name[name]
            if isinstance(setting, Toggle):
                toggle_settings.append(setting)
            elif (
                isinstance(setting, SingleSelect)
                and len(setting.choice_keys) <= SHORT_SELECT_LIMIT
            ):
                short_select_settings.append(setting)
            elif (
                isinstance(setting, IntSpinner)
                and len(setting.selectable_values) <= SHORT_SELECT_LIMIT
            ):
                short_select_settings.append(setting)
            elif (
                isinstance(setting, FloatSpinner)
                and len(setting.selectable_values) <= SHORT_SELECT_LIMIT
            ):
                short_select_settings.append(setting)
            else:
                self.set(name, setting.parse_settings_string(parts[used_index]))
                used_index = used_index + 1

        flags_bit_array = BitArray(uint=flags_value, length=len(toggle_settings))
        for index, setting in enumerate(toggle_settings):
            self.set(setting.name, flags_bit_array[index])

        for index, setting in enumerate(short_select_settings):
            selected_index = single_select_chars.index(short_select_string[index])
            if isinstance(setting, SingleSelect):
                self.set(setting.name, setting.choice_keys[selected_index])
            elif isinstance(setting, IntSpinner):
                self.set(setting.name, setting.selectable_values[selected_index])
            elif isinstance(setting, FloatSpinner):
                self.set(setting.name, setting.selectable_values[selected_index])

    def settings_json(self, include_private: bool = False):
        filtered_settings = {
            key: self.get(key)
            for key in self._filtered_settings(include_private).keys()
        }
        return filtered_settings

    def settings_spoiler_json(self) -> dict[SettingGroup, dict[str, str]]:
        result: dict[SettingGroup, dict[str, str]] = {
            group: {} for group in SettingGroup
        }
        for key, setting in self._filtered_settings(include_private=True).items():
            for label, value in setting.spoiler_log_entries(self.get(key)).items():
                result[setting.group][label] = value
        return result

    def apply_settings_json(self, settings_json, include_private: bool = False):
        for key, setting in self._filtered_settings(include_private).items():
            # If there's a setting in the JSON for the key, use its value; otherwise, use the default.
            # This should in theory allow the generator to be (mostly) backward-compatible with older shared presets,
            # at least when it's a simple case like a new setting added.
            if key in settings_json:
                self.set(key, settings_json[key])
            else:
                self.set(key, setting.default)


def getRandoRandoTooltip():
    randomizable_settings = [
        setting for setting in _all_settings if setting.randomizable
    ]
    text = "Randomized settings will randomize the following options: ["
    for r in randomizable_settings:
        text += r.ui_label + ", "
    text += "] \n Worlds/Bosses/Misc Locations will only be turned off randomly, so anything that is set to off before generating a seed will stay off (e.g. if Datas are off, they will stay off)"
    return text


def randomize_settings(real_settings_object: SeedSettings, randomizable_settings_names):
    randomizable_settings = [
        setting
        for setting in _all_settings
        if setting.name in randomizable_settings_names
    ]
    setting_choices = {}
    multi_selects = []
    trimulti_selects = []
    for r in randomizable_settings:
        if isinstance(r, SingleSelect):
            if r.randomizable is True:  # randomize all choices
                setting_choices[r.name] = [c for c in r.choices]
            elif isinstance(r.randomizable, list):
                setting_choices[r.name] = [c for c in r.randomizable]
        elif isinstance(r, Toggle):
            setting_choices[r.name] = [True, False]
        elif isinstance(r, IntSpinner):
            setting_choices[r.name] = [c for c in r.selectable_values]
        elif isinstance(r, FloatSpinner):
            setting_choices[r.name] = [c for c in r.selectable_values]
        elif isinstance(r, MultiSelect):
            # get the current set of values, will allow for some to be removed
            setting_choices[r.name] = [c for c in real_settings_object.get(r.name)]
            multi_selects.append(r.name)
        elif isinstance(r, WorldRandomizationTristate):  # TODO make this work
            # get the current set of values, will allow for some to be removed
            setting_choices[r.name] = real_settings_object.get(r.name)
            trimulti_selects.append(r.name)

    for r in randomizable_settings:
        if r.name not in setting_choices:
            raise SettingsException(
                f"Improper configuration of rando rando settings object. Missing configuration for {r.name}"
            )

    random_choices = {}
    for r in randomizable_settings:
        if r.name in multi_selects:  # TODO make this work
            random_choices[r.name] = [c for c in setting_choices[r.name]]
            # pick a fraction of the multi's to keep
            num_to_remove = random.randint(0, len(setting_choices[r.name]))
            for iter in range(num_to_remove):
                choice = random.choice(random_choices[r.name])
                random_choices[r.name].remove(choice)
        elif r.name in trimulti_selects:
            random_choices[r.name] = [[], []]
            for r_world in setting_choices[r.name][0]:
                prob = random.random()
                if prob < (2.0 / 3.0):
                    random_choices[r.name][0].append(r_world)
                elif prob < (2.5 / 3.0):
                    random_choices[r.name][1].append(r_world)
            for r_world in setting_choices[r.name][1]:
                prob = random.random()
                if prob < (1.0 / 2.0):
                    random_choices[r.name][1].append(r_world)
        else:
            random_choices[r.name] = random.choice(setting_choices[r.name])

    if (
        settingkey.KEYBLADE_MIN_STAT in random_choices
        and settingkey.KEYBLADE_MAX_STAT in random_choices
    ):
        if (
            random_choices[settingkey.KEYBLADE_MIN_STAT]
            > random_choices[settingkey.KEYBLADE_MAX_STAT]
        ):
            random_choices[settingkey.KEYBLADE_MAX_STAT] = random_choices[
                settingkey.KEYBLADE_MIN_STAT
            ]

    for r in randomizable_settings:
        real_settings_object.set(r.name, random_choices[r.name])


def makeKHBRSettings(seed_name: str, ui_settings: SeedSettings):
    enemy_options = {
        "seed_name": seed_name,
        "remove_damage_cap": ui_settings.get(settingkey.REMOVE_DAMAGE_CAP),
        "cups_give_xp": ui_settings.get(settingkey.CUPS_GIVE_XP),
        "retry_data_final_xemnas": ui_settings.get(settingkey.RETRY_DFX),
        "retry_dark_thorn": ui_settings.get(settingkey.RETRY_DARK_THORN),
        "remove_cutscenes": ui_settings.get(settingkey.REMOVE_CUTSCENES),
        "party_member_rando": ui_settings.get(settingkey.PARTY_MEMBER_RANDO),
        "costume_rando": ui_settings.get(settingkey.COSTUME_RANDO),
        "revenge_limit_rando": ui_settings.get(settingkey.REVENGE_LIMIT_RANDO),
    }
    for setting in boss_settings + enemy_settings:
        value = ui_settings.get(setting.name)
        if value is not None:
            enemy_options[setting.name] = value

    return enemy_options


@dataclass(frozen=True)
class ExtraConfigurationData:
    platform: str
    command_menu_choice: str
    room_transition_choice: str
    tourney: bool
    custom_cosmetics_executables: list[str]

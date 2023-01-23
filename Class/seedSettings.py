import copy
import random
import string
import textwrap

from bitstring import BitArray
from khbr.randomizer import Randomizer as khbr

from Class import settingkey
from Class.exceptions import SettingsException
from List.ItemList import Items, itemRarity
from List.configDict import expCurve, locationType, locationDepth, BattleLevelOption
from Module import encoding
from Module.progressionPoints import ProgressionPoints
from Module.randomCmdMenu import RandomCmdMenu


# Characters available to be used for short encoding of certain settings
single_select_chars = string.digits + string.ascii_letters
SHORT_SELECT_LIMIT = len(single_select_chars)


class Setting:

    def __init__(
            self,
            name: str,
            setting_type: type,
            ui_label: str,
            shared: bool,
            default,
            tooltip: str,
            standalone_label: str,
            randomizable=None
    ):
        self.name = name
        self.type = setting_type
        self.ui_label = ui_label
        self.shared = shared
        self.default = default
        self.tooltip = textwrap.dedent(tooltip).strip()
        if standalone_label == '':
            self.standalone_label = ui_label
        else:
            self.standalone_label = standalone_label
        self.randomizable = randomizable

    def settings_string(self, value) -> str:
        raise NotImplementedError

    def parse_settings_string(self, settings_string: str):
        raise NotImplementedError


class Toggle(Setting):

    def __init__(
            self,
            name: str,
            ui_label: str,
            shared: bool,
            default: bool,
            tooltip: str = '',
            standalone_label: str = '',
            randomizable=None
    ):
        super().__init__(name, bool, ui_label, shared, default, tooltip, standalone_label, randomizable)

    def settings_string(self, value) -> str:
        return '1' if value else '0'

    def parse_settings_string(self, settings_string: str):
        return True if settings_string == '1' else False


class IntSpinner(Setting):

    def __init__(
            self,
            name: str,
            ui_label: str,
            minimum: int,
            maximum: int,
            step: int,
            shared: bool,
            default: int,
            tooltip: str = '',
            standalone_label: str = '',
            randomizable=None
    ):
        super().__init__(name, int, ui_label, shared, default, tooltip, standalone_label, randomizable)
        self.min = minimum
        self.max = maximum
        self.step = step

        self.selectable_values = [value for value in range(minimum, maximum + step, step)]

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
            ui_label: str,
            minimum: float,
            maximum: float,
            step: float,
            shared: bool,
            default: float,
            tooltip: str = '',
            standalone_label: str = '',
            randomizable=None
    ):
        super().__init__(name, float, ui_label, shared, default, tooltip, standalone_label, randomizable)
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
            ui_label: str,
            choices: dict[str, str],
            shared: bool,
            default: str,
            tooltip: str = '',
            standalone_label: str = '',
            randomizable = None
    ):
        super().__init__(name, str, ui_label, shared, default, tooltip, standalone_label, randomizable)
        self.choices = choices
        self.choice_keys = list(choices.keys())
        self.choice_values = list(choices.values())

    def settings_string(self, value) -> str:
        index = self.choice_keys.index(value)
        return encoding.v2r(index)

    def parse_settings_string(self, settings_string: str):
        index = encoding.r2v(settings_string)
        return self.choice_keys[index]


class ProgressionChainSelect(Setting):
    def __init__(
            self,
            name: str,
            ui_label: str,
            shared: bool,
            tooltip: str = '',
            standalone_label: str = '',
            randomizable=None
    ):
        self.progression = ProgressionPoints()
        super().__init__(
            name,
            str,
            ui_label,
            shared,
            self.progression.get_compressed(),
            tooltip,
            standalone_label,
            randomizable
        )

    def settings_string(self, value) -> str:
        self.progression.set_uncompressed(value)
        return self.progression.get_compressed()

    def parse_settings_string(self, settings_string: str):
        self.progression.set_uncompressed(settings_string)
        return self.progression.get_compressed()


class MultiSelect(Setting):

    def __init__(
            self,
            name: str,
            ui_label: str,
            choices: dict[str, str],
            shared: bool,
            default: list[str],
            choice_icons: dict[str, str] = None,
            tooltip: str = '',
            standalone_label: str = '',
            randomizable=None
    ):
        super().__init__(name, str, ui_label, shared, default, tooltip, standalone_label, randomizable)
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


class MultiSelectTristate(Setting):
    def __init__(
            self,
            name: str,
            ui_label: str,
            choices: dict[str, str],
            shared: bool,
            default: list[list[str],list[str]],
            choice_icons: dict[str, str] = None,
            tooltip: str = '',
            standalone_label: str = '',
            randomizable=None
    ):
        super().__init__(name, str, ui_label, shared, default, tooltip, standalone_label, randomizable)
        self.choices = choices
        self.choice_keys = list(choices.keys())
        self.partial_choice_keys = list()
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
        split_settings = settings_string.split('+')

        bit_array = BitArray(uint=encoding.r2v(split_settings[0]), length=len(choice_keys))
        bit_array_partial = BitArray(uint=encoding.r2v(split_settings[1]), length=len(choice_keys))

        selected_values = []
        partial_values = []
        for index, choice_key in enumerate(choice_keys):
            if bit_array[index]:
                selected_values.append(choice_key)
        for index, choice_key in enumerate(choice_keys):
            if bit_array_partial[index]:
                partial_values.append(choice_key)

        return [selected_values,partial_values]
        

_drive_exp_curve_tooltip_text = textwrap.dedent('''
        Experience curve options, inspired by KH1's experience curves. Midday and Dusk reduce the total experience
        needed to get to Level 7, but levels 2-4 require more experience to compensate.
        
        Dawn - The default experience rate.
        
        Midday - Early levels (2-4) require more experience, but later levels (5-7) require less.
        
        Dusk - Early levels (2-4) require even more experience, but later levels (5-7) require even less.
''')

_drive_exp_multiplier_tooltip_text = textwrap.dedent('''
        Adjusts the amount of experience needed to reach each drive form level.
        For example, setting the multiplier to 2.0 cuts the required experience to reach each level in half.
''')

_depth_options_text = textwrap.dedent('''

        Superbosses - Force onto superbosses only (Data Organization/Absent Silhouette/Sephiroth/Terra).
        
        First Visit - Force into a first visit (only for the 13 main hub worlds with portals).
        
        Second Visit - Force into a second visit (only for the 13 main hub worlds with portals).
        
        Non-Superboss - Cannot be on a superboss (Data Organization/Absent Silhouette/Sephiroth/Terra).
        All other locations are possible.
        
        First Visit Boss - Force onto the first visit boss of a world (only for the 13 main hub worlds with portals).
        
        Second Visit Boss - Force onto the last boss of a world (only for the 13 main hub worlds with portals).
        
        Anywhere - No restriction.
''')

_all_settings = [
    SingleSelect(
        name=settingkey.SORA_LEVELS,
        ui_label='Max Level Reward',
        choices={
            'Level': 'Level 1',
            'ExcludeFrom50': 'Level 50',
            'ExcludeFrom99': 'Level 99'
        },
        shared=True,
        default='ExcludeFrom50',
        randomizable=True,
        tooltip="Maximum Level for randomized rewards."
    ),

    Toggle(
        name=settingkey.LEVEL_ONE,
        ui_label='Level 1 Mode',
        shared=True,
        default=False,
        tooltip='Give no stats or items on level ups, removes abilities that would be on levels in vanilla from the item pool.'
    ),

    Toggle(
        name=settingkey.SPLIT_LEVELS,
        ui_label='Dream Weapon Matters',
        shared=True,
        default=False,
        tooltip='''
        Makes the dream weapon choice at the beginning of the game change when you get items/abilities on levels
        (either with the same offsets as the vanilla game, or the adjusted values for max level 50).
        ''',
        randomizable=True
    ),

    Toggle(
        name=settingkey.STATSANITY,
        ui_label='Bonus Rewards as Items (Statsanity)',
        shared=True,
        default=True,
        randomizable=True,
        tooltip='''
        Takes HP, MP, Drive, Accessory Slot, Armor Slot, and Item Slot upgrades from their normal bonus locations and
        lets them appear in chests or other locations. Those bonus locations can now have other items in them.
        ''',
    ),

    FloatSpinner(
        name=settingkey.SORA_EXP_MULTIPLIER,
        ui_label='Sora',
        standalone_label='Sora EXP Multiplier',
        minimum=0.5,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=2.0,
        randomizable=True,
        tooltip='''
        Adjusts the amount of experience needed to reach each level.
        For example, setting the multiplier to 2.0 cuts the required experience to reach each level in half.
        '''
    ),

    FloatSpinner(
        name=settingkey.VALOR_EXP_MULTIPLIER,
        ui_label='Valor',
        standalone_label='Valor EXP Multiplier',
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=7.0,
        randomizable=True,
        tooltip=_drive_exp_multiplier_tooltip_text
    ),

    FloatSpinner(
        name=settingkey.WISDOM_EXP_MULTIPLIER,
        ui_label='Wisdom',
        standalone_label='Wisdom EXP Multiplier',
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=3.0,
        randomizable=True,
        tooltip=_drive_exp_multiplier_tooltip_text
    ),

    FloatSpinner(
        name=settingkey.LIMIT_EXP_MULTIPLIER,
        ui_label='Limit',
        standalone_label='Limit EXP Multiplier',
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=4.0,
        randomizable=True,
        tooltip=_drive_exp_multiplier_tooltip_text
    ),

    FloatSpinner(
        name=settingkey.MASTER_EXP_MULTIPLIER,
        ui_label='Master',
        standalone_label='Master EXP Multiplier',
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=3.0,
        randomizable=True,
        tooltip=_drive_exp_multiplier_tooltip_text
    ),

    FloatSpinner(
        name=settingkey.FINAL_EXP_MULTIPLIER,
        ui_label='Final',
        standalone_label='Final EXP Multiplier',
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=3.5,
        randomizable=True,
        tooltip=_drive_exp_multiplier_tooltip_text
    ),

    FloatSpinner(
        name=settingkey.SUMMON_EXP_MULTIPLIER,
        ui_label='Summon',
        standalone_label='Summon EXP Multiplier',
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=2.0,
        randomizable=True,
        tooltip='''
        Adjusts the amount of experience needed to reach each summon level.
        For example, setting the multiplier to 2.0 cuts the required experience to reach each level in half.
        '''
    ),

    SingleSelect(
        name=settingkey.SORA_EXP_CURVE,
        ui_label='Sora',
        standalone_label='Sora EXP Curve',
        choices={
            expCurve.DAWN.name: "Dawn (Normal)",
            expCurve.MIDDAY.name: "Midday",
            expCurve.DUSK.name: "Dusk"
        },
        shared=True,
        default=expCurve.DAWN.name,
        tooltip='''
        Experience curve options, inspired by KH1's experience curves. Midday and Dusk reduce the total experience
        needed to get to level 99, but levels up to 50 require more experience to compensate.
        
        Dawn - The default experience rate.
        
        Midday - Early levels (up to 50) require more experience, but levels 51-99 require less.
        
        Dusk - Early levels (up to 50) require even more experience, but levels 51-99 require even less.
        ''',
        randomizable=True
    ),
    
    SingleSelect(
        name=settingkey.VALOR_EXP_CURVE,
        ui_label='Valor',
        standalone_label='Valor EXP Curve',
        choices={
            expCurve.DAWN.name: "Dawn (Normal)",
            expCurve.MIDDAY.name: "Midday",
            expCurve.DUSK.name: "Dusk"
        },
        shared=True,
        default=expCurve.MIDDAY.name,
        tooltip=_drive_exp_curve_tooltip_text,
        randomizable=True
    ),
    
    SingleSelect(
        name=settingkey.WISDOM_EXP_CURVE,
        ui_label='Wisdom',
        standalone_label='Wisdom EXP Curve',
        choices={
            expCurve.DAWN.name: "Dawn (Normal)",
            expCurve.MIDDAY.name: "Midday",
            expCurve.DUSK.name: "Dusk"
        },
        shared=True,
        default=expCurve.DAWN.name,
        tooltip=_drive_exp_curve_tooltip_text,
        randomizable=True
    ),
    
    SingleSelect(
        name=settingkey.LIMIT_EXP_CURVE,
        ui_label='Limit',
        standalone_label='Limit EXP Curve',
        choices={
            expCurve.DAWN.name: "Dawn (Normal)",
            expCurve.MIDDAY.name: "Midday",
            expCurve.DUSK.name: "Dusk"
        },
        shared=True,
        default=expCurve.MIDDAY.name,
        tooltip=_drive_exp_curve_tooltip_text,
        randomizable=True
    ),
    
    SingleSelect(
        name=settingkey.MASTER_EXP_CURVE,
        ui_label='Master',
        standalone_label='Master EXP Curve',
        choices={
            expCurve.DAWN.name: "Dawn (Normal)",
            expCurve.MIDDAY.name: "Midday",
            expCurve.DUSK.name: "Dusk"
        },
        shared=True,
        default=expCurve.MIDDAY.name,
        tooltip=_drive_exp_curve_tooltip_text,
        randomizable=True
    ),
    
    SingleSelect(
        name=settingkey.FINAL_EXP_CURVE,
        ui_label='Final',
        standalone_label='Final EXP Curve',
        choices={
            expCurve.DAWN.name: "Dawn (Normal)",
            expCurve.MIDDAY.name: "Midday",
            expCurve.DUSK.name: "Dusk"
        },
        shared=True,
        default=expCurve.DAWN.name,
        tooltip=_drive_exp_curve_tooltip_text,
        randomizable=True
    ),
    
    SingleSelect(
        name=settingkey.SUMMON_EXP_CURVE,
        ui_label='Summon',
        standalone_label='Summon EXP Curve',
        choices={
            expCurve.DAWN.name: "Dawn (Normal)",
            expCurve.MIDDAY.name: "Midday",
            expCurve.DUSK.name: "Dusk"
        },
        shared=True,
        default=expCurve.DAWN.name,
        tooltip=_drive_exp_curve_tooltip_text,
        randomizable=True
    ),

    Toggle(
        name=settingkey.CRITICAL_BONUS_REWARDS,
        ui_label='Critical Bonuses',
        standalone_label='Critical Bonuses in Pool',
        shared=True,
        default=True,
        randomizable=True,
        tooltip="Critical Mode Only! When enabled, non-junk items can be in the 7 starting items on critical mode."
    ),

    Toggle(
        name=settingkey.GARDEN_OF_ASSEMBLAGE_REWARDS,
        ui_label='Garden of Assemblage',
        standalone_label='Garden of Assemblage in Pool',
        shared=True,
        default=True,
        randomizable=True,
        tooltip='Randomizes the items in the treasure chests in the Garden of Assemblage.'
    ),

    Toggle(
       name=settingkey.AUTO_EQUIP_START_ABILITIES,
       ui_label='Starting Abilities Equipped',
       shared=True,
       default=False,
       tooltip='Start with abilities auto-equipped (except ones from critical bonuses).'
    ),

    SingleSelect(
        name=settingkey.STARTING_MOVEMENT,
        ui_label="Growth Ability Starting Level",
        choices={
            'Disabled': 'None',
            '3Random': '3 Random',
            'Random': '5 Random',
            'Level_1': 'Level 1',
            'Level_2': 'Level 2',
            'Level_3': 'Level 3',
            'Level_4': 'Max'
        },
        shared=True,
        default='Level_1',
        tooltip='''
        None - No guaranteed starting growth.
        
        3 Random - Start with 3 individual growths at random.
        
        5 Random - Start with 5 individual growths at random.
        
        Level 1 - Start with level 1 of all growth abilities.
        
        Level 2 - Start with level 2 of all growth abilities.
        
        Level 3 - Start with level 3 of all growth abilities.
        
        Max - Start with the maximum level of all growth abilities.
        ''',
        randomizable=["Disabled","3Random","Random","Level_1","Level_2","Level_3","Level_4"]
    ),

    IntSpinner(
        name=settingkey.STARTING_REPORTS,
        ui_label="Starting Ansem Reports",
        standalone_label='# Starting Ansem Reports',
        minimum=0,
        maximum=13,
        step=1,
        shared=True,
        default=0,
        randomizable=[0,1,2,3],
        tooltip='Start with this number of Ansem Reports already obtained.'
    ),

    MultiSelect(
        name=settingkey.STARTING_INVENTORY,
        ui_label='Starting Inventory',
        choices={
            '138': 'Scan',
            '404': 'No Experience',
            '158': 'Aerial Recovery',
            '82': 'Guard',
            '393': 'Finishing Plus',
            '537': 'Hades Cup Trophy',
            '370': 'Olympus Stone',
            '462': 'Unknown Disk',
            '593': 'Proof of Connection',
            '594': 'Proof of Nonexistence',
            '595': 'Proof of Peace',
            '524': 'Promise Charm',
        },
        shared=True,
        default=[],
        tooltip='Start with the selected items/abilities already obtained.'
    ),

    SingleSelect(
        name=settingkey.HINT_SYSTEM,
        ui_label="Hint System",
        choices={
            'Disabled': 'Disabled',
            'Shananas': 'Shananas',
            'JSmartee': 'JSmartee',
            'Points': 'Points',
            'Path': 'Path',
            'Spoiler': 'Spoiler'
        },
        shared=True,
        default='Shananas',
        tooltip='''
        Which hint system to use. More detailed explanations the hint systems can be found on the website.
    
        Disabled - Use no hint system.
        
        JSmartee - Ansem Reports reveal how many "important checks" are in a world.
        
        Shananas - Each world informs you once the world has no more "important checks".
        
        Points - Each "important check" is assigned a point value, and you are told the number of points in each
        world. Ansem Reports reveal where items are.
        
        Path - Ansem Reports will tell you if a world contains "breadcrumbs" left by a world that has a proof.
        "Breadcrumbs" being vanilla important checks from a world.
        
        Spoiler - Reveal "Important Check" locations in a world at the start of a seed.
        ''',
        randomizable=["Shananas","JSmartee","Points","Path","Spoiler"]
    ),

    Toggle(
        name=settingkey.PROGRESSION_HINTS,
        ui_label='Progression Hint Mode',
        shared=True,
        default=False,
        tooltip='''
        Instead of Ansem Reports providing the source of hints, world progress unlocks more hints in your tracker.
        ''',
        randomizable=True
    ),

    Toggle(
        name=settingkey.PROGRESSION_HINTS_REVEAL_END,
        ui_label='Reveal All Hints When Done',
        shared=True,
        default=False,
        tooltip='''
        Make all hints reveal themselves when you beat Final Xemnas.
        ''',
        randomizable=False
    ),

    IntSpinner(
        name=settingkey.PROGRESSION_HINTS_REPORT_BONUS,
        ui_label="Progression Report Reward",
        minimum=0,
        maximum=5,
        step=1,
        shared=True,
        default=0,
        tooltip='''
        When you find an Ansem Report, how many points toward your hints you get.
        ''',
        randomizable=False
    ),

    IntSpinner(
        name=settingkey.PROGRESSION_HINTS_COMPLETE_BONUS,
        ui_label="Progression World Complete Reward",
        minimum=0,
        maximum=5,
        step=1,
        shared=True,
        default=0,
        tooltip='''
        When a world is finished, how many additional points you receive for progressing.
        ''',
        randomizable=False
    ),

    ProgressionChainSelect(
        name=settingkey.PROGRESSION_POINT_SELECT,
        ui_label='',
        shared=True,
        tooltip='''
        Point values for different checkpoints in worlds.
        ''',
        randomizable=False
    ),

    IntSpinner(
        name=settingkey.POINTS_PROOF,
        ui_label="Proof",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=5,
        tooltip='Point value for each Proof.'
    ),

    IntSpinner(
        name=settingkey.POINTS_FORM,
        ui_label="Drive Form",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=9,
        tooltip='Point value for each Drive Form.'
    ),

    IntSpinner(
        name=settingkey.POINTS_MAGIC,
        ui_label="Magic",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=7,
        tooltip='Point value for each Magic.'
    ),

    IntSpinner(
        name=settingkey.POINTS_SUMMON,
        ui_label="Summon",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=5,
        tooltip='Point value for each Summon.'
    ),

    IntSpinner(
        name=settingkey.POINTS_ABILITY,
        ui_label="Second Chance/Once More",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=5,
        tooltip='Point value for each of the Second Chance and Once More abilities.'
    ),

    IntSpinner(
        name=settingkey.POINTS_PAGE,
        ui_label="Torn Page",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=5,
        tooltip='Point value for each Torn Page.'
    ),

    IntSpinner(
        name=settingkey.POINTS_VISIT,
        ui_label="Visit Unlock",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=5,
        tooltip='Point value for each Visit Unlock.'
    ),
    
    IntSpinner(
        name=settingkey.POINTS_REPORT,
        ui_label="Ansem Report",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=3,
        tooltip='Point value for each Ansem Report.'
    ),
    
    IntSpinner(
        name=settingkey.POINTS_AUX,
        ui_label="Aux. Unlock",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=1,
        tooltip='Point value for each Aux. Unlock.'
    ),

    IntSpinner(
        name=settingkey.POINTS_MAGIC_COLLECT,
        ui_label="Magic Set",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=0,
        tooltip='Bonus points for collecting all Magic.'
    ),

    IntSpinner(
        name=settingkey.POINTS_PAGE_COLLECT,
        ui_label="Torn Page Set",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=0,
        tooltip='Bonus points for collecting all Torn Pages.'
    ),

    IntSpinner(
        name=settingkey.POINTS_POUCHES_COLLECT,
        ui_label="Munny Pouch Set",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=0,
        tooltip='Bonus points for collecting all Munny Pouches.'
    ),

    IntSpinner(
        name=settingkey.POINTS_PROOF_COLLECT,
        ui_label="Proof Set",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=0,
        tooltip='Bonus points for collecting all Proofs.'
    ),

    IntSpinner(
        name=settingkey.POINTS_FORM_COLLECT,
        ui_label="Drive Form Set",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=0,
        tooltip='Bonus points for collecting all Drive Forms.'
    ),

    IntSpinner(
        name=settingkey.POINTS_SUMMON_COLLECT,
        ui_label="Summon Set",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=0,
        tooltip='Bonus points for collecting all Summons.'
    ),

    IntSpinner(
        name=settingkey.POINTS_ABILITY_COLLECT,
        ui_label="Ability Set",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=0
    ),

    IntSpinner(
        name=settingkey.POINTS_REPORT_COLLECT,
        ui_label="Ansem Report Set",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=0,
        tooltip='Bonus points for collecting all Ansem Reports.'
    ),

    IntSpinner(
        name=settingkey.POINTS_VISIT_COLLECT,
        ui_label="Visit Unlock Set",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=0,
        tooltip='Bonus points for collecting all Visit Unlocks.'
    ),

    IntSpinner(
        name=settingkey.POINTS_BONUS,
        ui_label="Bonus Level",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=10
    ),

    IntSpinner(
        name=settingkey.POINTS_COMPLETE,
        ui_label="World Completion",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=10
    ),

    IntSpinner(
        name=settingkey.POINTS_FORMLV,
        ui_label="Form Level",
        minimum=-10,
        maximum=1000,
        step=1,
        shared=True,
        default=3
    ),

    IntSpinner(
        name=settingkey.POINTS_DEATH,
        ui_label="Death Penalty",
        minimum=-1000,
        maximum=1000,
        step=1,
        shared=True,
        default=-10
    ),

    IntSpinner(
        name=settingkey.POINTS_BOSS_NORMAL,
        ui_label="Normal Boss Defeated",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=10
    ),
    
    IntSpinner(
        name=settingkey.POINTS_BOSS_AS,
        ui_label="Absent Silhouette Defeated",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=20
    ),
    
    IntSpinner(
        name=settingkey.POINTS_BOSS_DATA,
        ui_label="Data Boss Defeated",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=30
    ),
    
    IntSpinner(
        name=settingkey.POINTS_BOSS_SEPHIROTH,
        ui_label="Sephiroth Defeated",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=40
    ),
    
    IntSpinner(
        name=settingkey.POINTS_BOSS_TERRA,
        ui_label="Lingering Will Defeated",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=50
    ),
    
    IntSpinner(
        name=settingkey.POINTS_BOSS_FINAL,
        ui_label="Final Xemnas Defeated",
        minimum=0,
        maximum=1000,
        step=1,
        shared=True,
        default=100
    ),

    SingleSelect(
        name=settingkey.REPORT_DEPTH,
        ui_label='Ansem Report Depth',
        choices={
            locationDepth.DataFight.name: 'Superbosses',
            locationDepth.FirstVisit.name: 'First Visit',
            locationDepth.SecondVisitOnly.name: 'Second Visit',
            locationDepth.SecondVisit.name: 'Non-Superboss',
            locationDepth.FirstBoss.name: 'First Visit Boss',
            locationDepth.SecondBoss.name: 'Second Visit Boss',
            locationDepth.Anywhere.name: "Anywhere"
        },
        shared=True,
        default=locationDepth.SecondVisit.name,
        tooltip='The set of locations in which Ansem Reports are allowed to be placed.' + _depth_options_text,
        randomizable=[locationDepth.SecondVisitOnly.name, locationDepth.SecondVisit.name, locationDepth.FirstBoss.name, locationDepth.Anywhere.name]
    ),

    SingleSelect(
        name=settingkey.PROOF_DEPTH,
        ui_label='Proof Depth',
        choices={
            locationDepth.DataFight.name: 'Superbosses',
            locationDepth.FirstVisit.name: 'First Visit',
            locationDepth.SecondVisitOnly.name: 'Second Visit',
            locationDepth.SecondVisit.name: 'Non-Superboss',
            locationDepth.FirstBoss.name: 'First Visit Boss',
            locationDepth.SecondBoss.name: 'Second Visit Boss',
            locationDepth.Anywhere.name: "Anywhere"
        },
        shared=True,
        default=locationDepth.Anywhere.name,
        tooltip='The set of locations in which Proofs are allowed to be placed.' + _depth_options_text,
        randomizable=[locationDepth.SecondVisitOnly.name, locationDepth.SecondVisit.name, locationDepth.SecondBoss.name, locationDepth.Anywhere.name]
    ),

    SingleSelect(
        name=settingkey.STORY_UNLOCK_DEPTH,
        ui_label='Visit Unlock Depth',
        choices={
            locationDepth.DataFight.name: 'Superbosses',
            locationDepth.FirstVisit.name: 'First Visit',
            locationDepth.SecondVisitOnly.name: 'Second Visit',
            locationDepth.SecondVisit.name: 'Non-Superboss',
            locationDepth.FirstBoss.name: 'First Visit Boss',
            locationDepth.SecondBoss.name: 'Second Visit Boss',
            locationDepth.Anywhere.name: "Anywhere"
        },
        shared=True,
        default=locationDepth.Anywhere.name,
        tooltip='The set of locations in which Visit Unlocks are allowed to be placed.' + _depth_options_text,
        randomizable=[locationDepth.FirstVisit.name, locationDepth.SecondVisit.name, locationDepth.FirstBoss.name, locationDepth.SecondBoss.name, locationDepth.Anywhere.name]
    ),

    SingleSelect(
        name=settingkey.BATTLE_LEVEL_RANDO,
        ui_label='Battle Level Choice',
        choices={option.name: option.value for option in list(BattleLevelOption)},
        shared=True,
        default=BattleLevelOption.NORMAL.name,
        tooltip='''
        Changes the battle levels of worlds.
        
        Normal - Battle levels are unchanged.
        
        Shuffle - Shuffle the normal battle levels among all visits of all worlds.
        
        Offset - Increase/Decrease all battle levels by a given amount.
        
        Within Range of Normal - Vary battle levels of all visits within a set number above or below normal.
        
        Random (Max 50) - All battle levels are random, with a maximum level of 50.
        
        Scale to 50 - All last visits are level 50, with previous visits scaled proportionally.
        ''',
        standalone_label="Battle Level Randomization",
        randomizable=True
    ),

    IntSpinner(
        name=settingkey.BATTLE_LEVEL_OFFSET,
        ui_label="Level Offset",
        minimum=-50,
        maximum=100,
        step=5,
        shared=True,
        default=0,
        standalone_label="Battle Level Offset (if chosen)",
        tooltip="How many battle levels to change the worlds by.",
        randomizable=[-20,-15,-10,0,10,15,20]
    ),

    IntSpinner(
        name=settingkey.BATTLE_LEVEL_RANGE,
        ui_label="Level Range",
        minimum=0,
        maximum=50,
        step=5,
        shared=True,
        default=0,
        standalone_label="Battle Level Range (if chosen)",
        tooltip="How far above or below normal battle levels to choose.",
        randomizable=[0,20]
    ),

    Toggle(
        name=settingkey.YEET_THE_BEAR,
        ui_label='Yeet The Bear Required',
        shared=True,
        default=False,
        tooltip="Forces the Proof of Nonexistence onto the Starry Hill popup in 100 Acre Wood"
    ),

    Toggle(
        name=settingkey.CHAIN_LOGIC,
        ui_label='Turn On Chain Logic',
        shared=True,
        default=False,
        tooltip="Places all the locking items in a chain with one another, making the seed very linear."
    ),

    Toggle(
        name=settingkey.CHAIN_LOGIC_TERRA,
        ui_label='Include Lingering Will in Chain',
        shared=True,
        default=False,
        tooltip="Puts the Proof of Connection into the logic chain, effectively requiring beating Lingering Will."
    ),

    Toggle(
        name=settingkey.CHAIN_LOGIC_MIN_TERRA,
        ui_label='Force Late Depth for Proof of Connection',
        shared=True,
        default=False,
        tooltip="Forces the Proof of Connection to be in the last 5 steps of the chain, to give more chances for finding combat tools."
    ),

    IntSpinner(
        name=settingkey.CHAIN_LOGIC_LENGTH,
        ui_label="Maximum Logic Length",
        minimum=10,
        maximum=26, # theoretical max
        step=1,
        shared=True,
        default=26,
        tooltip="How many steps in the logic chain you'd like to do at most."
    ),

    Toggle(
        name=settingkey.PREVENT_SELF_HINTING,
        ui_label='Remove Self-Hinting Reports',
        shared=True,
        default=False,
        tooltip="Each Ansem Report must hint a world that is different from where that report was found."
    ),

    Toggle(
        name=settingkey.ALLOW_PROOF_HINTING,
        ui_label='Reports can Reveal Proofs',
        shared=True,
        default=False,
        tooltip="If enabled, proofs can be directly revealed by Ansem Reports."
    ),

    Toggle(
        name=settingkey.ALLOW_REPORT_HINTING,
        ui_label='Reports can Reveal other Reports',
        shared=True,
        default=True,
        tooltip="If enabled, Ansem Reports can reveal other Ansem Reports."
    ),
    
    Toggle(
        name=settingkey.SCORE_MODE,
        ui_label='Hi-Score Mode',
        shared=True,
        default=False,
        tooltip="If enabled, gain points for collecting Important Checks, completing worlds, beating bosses, etc."
    ),

    MultiSelect(
        name=settingkey.HINTABLE_CHECKS,
        ui_label='Hintable Items',
        choices={
            'magic': 'Magic',
            'form': 'Drive Forms',
            'summon': 'Summon Charms',
            'page': 'Torn Pages',
            'ability': 'Second Chance/Once More',
            'report': 'Ansem Reports',
            'visit': 'Visit Unlocks',
            'proof': 'Proofs',
            'other': 'Aux. Unlocks'
        },
        shared=True,
        default=["magic", "form", "summon", "page", "ability", "report", "visit", "proof"]
    ),
    MultiSelect(
        name=settingkey.SPOILER_REVEAL_TYPES,
        ui_label='Spoiled Items',
        choices={
            'magic': 'Magic',
            'form': 'Drive Forms',
            'summon': 'Summon Charms',
            'page': 'Torn Pages',
            'ability': 'Second Chance/Once More',
            'report': 'Ansem Reports',
            'visit': 'Visit Unlocks',
            'proof': 'Proofs',
            'other': 'Aux. Unlocks'
        },
        shared=True,
        default=["magic", "form", "summon", "page", "ability", "report", "visit", "proof"]
    ),

    Toggle(
        name=settingkey.REVEAL_COMPLETE,
        ui_label='Reveal World Completion',
        shared=True,
        default=True,
        tooltip="If enabled, the tracker will reveal when all Important Checks in a world are found."
    ),
    
    SingleSelect(
        name=settingkey.REPORTS_REVEAL,
        ui_label='Report Reveal Mode',
        choices={
            'Disabled': 'Disabled',
            'reportmode': 'Worlds',
            'bossreports': 'Randomized Bosses'
        },
        shared=True,
        default='reportmode',
        tooltip='''
        Configures how Ansem Reports reveal information.
    
        Disabled - All worlds will be revealed at the start.
        
        Worlds - Ansem Reports reveal the Important Checks in a world.
        
        Randomized Bosses - Ansem Reports reveal what a boss has randomized into (Requires Boss randomizer).
        ''',
        randomizable=None
    ),
    
    IntSpinner(
        name=settingkey.KEYBLADE_MIN_STAT,
        ui_label="Keyblade Min Stat",
        minimum=0,
        maximum=20,
        step=1,
        shared=True,
        default=0,
        randomizable=True,
        tooltip='The minimum strength and magic stat that each keyblade must have.'
    ),

    IntSpinner(
        name=settingkey.KEYBLADE_MAX_STAT,
        ui_label="Keyblade Max Stat",
        minimum=0,
        maximum=20,
        step=1,
        shared=True,
        default=7,
        randomizable=True,
        tooltip='The maximum strength and magic stat that each keyblade must have.'
    ),

    MultiSelect(
        name=settingkey.KEYBLADE_SUPPORT_ABILITIES,
        ui_label='Support Keyblade-Eligible Abilities',
        choices={str(item.Id): item.Name for item in Items.getSupportAbilityList() + Items.getLevelAbilityList()},
        shared=True,
        default=list(set([str(item.Id) for item in Items.getSupportAbilityList() + Items.getLevelAbilityList()])),
        tooltip='Selected abilities may randomize onto keyblades. Unselected abilities will not be on keyblades.'
    ),

    MultiSelect(
        name=settingkey.KEYBLADE_ACTION_ABILITIES,
        ui_label='Action Keyblade-Eligible Abilities',
        choices={str(item.Id): item.Name for item in Items.getActionAbilityList()},
        shared=True,
        default=[],
        tooltip='Selected abilities may randomize onto keyblades. Unselected abilities will not be on keyblades.'
    ),

    MultiSelectTristate(
        name=settingkey.WORLDS_WITH_REWARDS,
        ui_label='Worlds with Rewards',
        choices={location.name: location.value for location in [
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
            locationType.Atlantica
        ]},
        shared=True,
        default=[[
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
            locationType.TWTNW.name
        ],[]],
        choice_icons={
            locationType.Level.name: "icons/worlds/sora.png",
            locationType.FormLevel.name: "icons/worlds/drives.png",
            locationType.STT.name: "icons/worlds/simulated_twilight_town.png",
            locationType.HB.name: "icons/worlds/hollow_bastion.png",
            locationType.OC.name: "icons/worlds/olympus_coliseum.png",
            locationType.LoD.name: "icons/worlds/land_of_dragons.png",
            locationType.PL.name: "icons/worlds/pride_lands.png",
            locationType.HT.name: "icons/worlds/halloween_town.png",
            locationType.SP.name: "icons/worlds/space_paranoids.png",
            locationType.TT.name: "icons/worlds/twilight_town.png",
            locationType.BC.name: "icons/worlds/beast's_castle.png",
            locationType.Agrabah.name: "icons/worlds/agrabah.png",
            locationType.HUNDREDAW.name: "icons/worlds/100_acre_wood.png",
            locationType.DC.name: "icons/worlds/disney_castle.png",
            locationType.PR.name: "icons/worlds/port_royal.png",
            locationType.TWTNW.name: "icons/worlds/the_world_that_never_was.png",
            locationType.Atlantica.name: "icons/worlds/atlantica.png"
        },
        randomizable=True,
        tooltip='''
        Configures the reward placement for a world.
    
        Rando - Fully randomized locations, can have junk or unique items.
        
        Vanilla - Notable unique items are placed in their original locations for KH2FM.
        All other locations will get junk items.
        
        Junk - All locations use items from the junk item pool.
        '''
    ),

    MultiSelect(
        name=settingkey.SUPERBOSSES_WITH_REWARDS,
        ui_label='Superbosses with Rewards',
        choices={location.name: location.value for location in [
            locationType.AS,
            locationType.DataOrg,
            locationType.Sephi,
            locationType.LW
        ]},
        shared=True,
        default=[locationType.AS.name, locationType.Sephi.name],
        choice_icons={
            locationType.AS.name: 'icons/bosses/as.png',
            locationType.DataOrg.name: 'icons/bosses/datas.png',
            locationType.Sephi.name: 'icons/bosses/sephiroth.png',
            locationType.LW.name: 'icons/bosses/lingering_will.png'
        },
        randomizable=True
    ),

    MultiSelect(
        name=settingkey.MISC_LOCATIONS_WITH_REWARDS,
        ui_label='Misc Locations with Rewards',
        choices={location.name: location.value for location in [
            locationType.OCCups,
            locationType.OCParadoxCup,
            locationType.Puzzle,
            locationType.CoR,
            locationType.TTR,
            locationType.SYNTH
        ]},
        shared=True,
        default=[
            locationType.CoR.name,],
        choice_icons={
            locationType.OCCups.name: 'icons/misc/cups.png',
            locationType.OCParadoxCup.name: 'icons/misc/paradox_cup.png',
            locationType.Puzzle.name: 'icons/misc/puzzle.png',
            locationType.CoR.name: "icons/worlds/cavern_of_remembrance.png",
            locationType.TTR.name: 'icons/misc/transport.png',
            locationType.SYNTH.name: 'icons/misc/moogle.png'
        },
        randomizable=True
    ),

    Toggle(
        name=settingkey.GLASS_CANNON,
        ui_label='Glass Cannon',
        shared=True,
        default=False,
        tooltip='Removes Defense Ups from the level up statistics pool.'
    ),

    MultiSelect(
        name=settingkey.JUNK_ITEMS,
        ui_label='Junk Items',
        choices={str(item.Id): item.Name for item in Items.getJunkList(False)},
        shared=True,
        default=list(set([str(item.Id) for item in Items.getJunkList(False)])),
        tooltip='''
        Once all of the required items are placed, items from this list are used to fill the rest.
        This item pool is also used for locations that are set to contain only junk or are disabled.
        '''
    ),
    
    IntSpinner(
        name=settingkey.SORA_AP,
        ui_label="Sora Starting AP",
        minimum=0,
        maximum=150,
        step=25,
        shared=True,
        default=50,
        randomizable=True,
        tooltip='Sora starts with this much AP.'
    ),

    IntSpinner(
        name=settingkey.DONALD_AP,
        ui_label="Donald Starting AP",
        minimum=5,
        maximum=55,
        step=5,
        shared=True,
        default=55,
        randomizable=True,
        tooltip='Donald starts with this much AP.'
    ),

    IntSpinner(
        name=settingkey.GOOFY_AP,
        ui_label="Goofy Starting AP",
        minimum=4,
        maximum=54,
        step=5,
        shared=True,
        default=54,
        randomizable=True,
        tooltip='Goofy starts with this much AP.'
    ),

    Toggle(
        name=settingkey.PUREBLOOD,
        ui_label='Pureblood Keyblade',
        shared=True,
        default=True,
        tooltip='Adds the Pureblood Keyblade into the item pool (may be disabled for older versions of GoA).'
    ),

    Toggle(
        name=settingkey.ANTIFORM,
        ui_label='Antiform',
        standalone_label='Obtainable Antiform',
        shared=True,
        default=False,
        tooltip='Adds Antiform as an obtainable form.'
    ),

    Toggle(
        name=settingkey.FIFTY_AP_BOOSTS,
        ui_label='50 AP Boosts',
        shared=True,
        default=True,
        tooltip='Adds 50 guaranteed AP boosts into the item pool.'
    ),

    Toggle(
        name=settingkey.REMOVE_DAMAGE_CAP,
        ui_label='Remove Damage Cap',
        shared=True,
        default=False,
        tooltip='Removes the damage cap for every enemy/boss in the game.'
    ),

    Toggle(
        name=settingkey.CUPS_GIVE_XP,
        ui_label='Cups Give Experience',
        shared=True,
        default=False,
        tooltip='Defeating enemies while in an Olympus Coliseum Cup will give you experience and Form experience.'
    ),

    SingleSelect(
        name=settingkey.REVENGE_LIMIT_RANDO,
        ui_label='Randomize Revenge Limit Maximum (Beta)',
        shared=True,
        choices={
            'Vanilla': 'Vanilla',
            'Set 0': 'Set 0',
            'Set Infinity': 'Set Infinity',
            'Maximum': 'Random Values'
        },
        default='Vanilla',
        tooltip='Randomizes the revenge value limit of each enemy/boss in the game. Can be either set to 0, set to basically infinity, randomly swapped, or set to a random value between 0 and 200'
    ),

    Toggle(
        name=settingkey.PARTY_MEMBER_RANDO,
        ui_label='Randomize World Party Members (Beta)',
        shared=True,
        default=False,
        tooltip='Randomizes the World Character party member in each world.'
    ),

    Toggle(
        name=settingkey.AS_DATA_SPLIT,
        ui_label='Split AS/Data Rewards',
        shared=True,
        default=False,
        tooltip='''
        When enabled, Absent Silhouette rewards will NOT give the reward from their Data Organization versions.
        You must beat the Data Organization version to get its reward.
        '''
    ),

    Toggle(
        name=settingkey.RETRY_DFX,
        ui_label='Retry Data Final Xemnas',
        shared=True,
        default=False,
        tooltip='''
        If you die to Data Final Xemnas, Continue will put you right back into the fight, instead of having to fight
        Data Xemnas I again.
         
        WARNING: This will be an effective softlock if you are unable to beat Data Final Xemnas.
        '''
    ),

    Toggle(
        name=settingkey.RETRY_DARK_THORN,
        ui_label='Retry Dark Thorn',
        shared=True,
        default=False,
        tooltip='''
        If you die to Dark Thorn, Continue will put you right back into the fight, instead of having to fight
        Shadow Stalker again.
         
        WARNING: This will be an effective softlock if you are unable to beat Dark Thorn.
        '''
    ),

    Toggle(
        name=settingkey.SKIP_CARPET_ESCAPE,
        ui_label='Skip Magic Carpet Escape',
        shared=True,
        default=False,
        tooltip='After reaching Ruined Chamber in Agrabah, the magic carpet escape sequence will be skipped.'
    ),

    Toggle(
        name=settingkey.PR_MAP_SKIP,
        ui_label='Remove Port Royal Map Select',
        shared=True,
        default=True,
        tooltip='Changes Port Royal map screen with text options, useful for avoiding crashes in PC.'
    ),

    Toggle(
        name=settingkey.ATLANTICA_TUTORIAL_SKIP,
        ui_label='Skip Atlantica Minigame Tutorial',
        shared=True,
        default=False,
        tooltip='Skips the Atlantica Music Tutorial (not the swimming tutorial).'
    ),

    Toggle(
        name=settingkey.REMOVE_WARDROBE_ANIMATION,
        ui_label='Remove Wardrobe Wakeup Animation',
        shared=True,
        default=False,
        tooltip='The wardrobe in Beast\'s Castle will not wake up when pushing it.'
    ),

    SingleSelect(
        name=settingkey.REMOVE_CUTSCENES,
        ui_label='Remove Most Cutscenes (Beta)',
        shared=True,
        choices={
            'Disabled': 'Disabled',
            'Minimal': 'Minimal',
            'Non-Reward': 'Non-Reward',
            'Maximum': 'Maximum'
        },
        default='Disabled',
        tooltip='''
        Removes as many cutscenes from the game as possible.
        
        Minimal - Remove as many cutscenes as possible without causing side effects.

        Non-Reward - Also remove cutscenes prior to forced fights, which causes the Continue on game over to force you
        back into the fight. This can be worked around using the auto-save mod.
        
        Maximum: Also remove cutscenes prior to receiving popup rewards, which causes the popups to not appear.
        You still get the reward, and it still shows up on the tracker.
        '''
    ),

    Toggle(
        name=settingkey.COSTUME_RANDO,
        ui_label='Randomize Character Costumes (Beta)',
        shared=False,
        default=False,
        tooltip='Randomizes the different costumes that Sora/Donald/Goofy switch between in the different worlds (IE Space Paranoids could now be default sora, while anywhere default sora is used could be Christmas Town Sora.'
    ),

    Toggle(
        name=settingkey.FAST_URNS,
        ui_label='Fast Olympus Coliseum Urns',
        shared=True,
        default=False,
        tooltip="The urns in the minigame in Olympus Coliseum drop more orbs, making the minigame much faster.",
        randomizable=False
    ),

    Toggle(
        name=settingkey.RICH_ENEMIES,
        ui_label='All Enemies Drop Munny',
        shared=True,
        default=False,
        tooltip="Enemies will all drop munny.",
        randomizable=True
    ),

    Toggle(
        name=settingkey.UNLIMITED_MP,
        ui_label='All Enemies Drop MP Orbs',
        shared=True,
        default=False,
        tooltip="Enemies will all drop MP orbs.",
        randomizable=True
    ),

    IntSpinner(
        name=settingkey.GLOBAL_JACKPOT,
        ui_label="Global Jackpots",
        standalone_label='# of Global Jackpots',
        minimum=0,
        maximum=3,
        step=1,
        shared=True,
        default=0,
        tooltip='''
        Increases orb/munny drops as if you had this many Jackpots equipped.
        Each Jackpot adds 50 percent of the original amount.
        ''',
        randomizable=True
    ),

    IntSpinner(
        name=settingkey.GLOBAL_LUCKY,
        ui_label="Global Lucky Lucky",
        standalone_label='# of Global Lucky Lucky',
        minimum=0,
        maximum=3,
        step=1,
        shared=True,
        default=0,
        tooltip='''
        Increases item drops as if you had this many Lucky Lucky abilities equipped.
        Each Lucky Lucky adds 50 percent of the chance to drop the item.
        ''',
        randomizable=True
    ),

    Toggle(
        name=settingkey.SHOP_KEYBLADES,
        ui_label='Keyblades',
        standalone_label='Keyblades in Shop',
        shared=True,
        default=False,
        tooltip="Adds duplicates of keyblades into the moogle shop.",
        randomizable=True
    ),

    Toggle(
        name=settingkey.SHOP_ELIXIRS,
        ui_label='Elixirs',
        standalone_label='Elixirs in Shop',
        shared=True,
        default=False,
        tooltip="Adds Elixirs/Megalixirs into the moogle shop.",
        randomizable=True
    ),

    Toggle(
        name=settingkey.SHOP_RECOVERIES,
        ui_label='Drive Recoveries',
        standalone_label='Drive Recoveries in Shop',
        shared=True,
        default=False,
        tooltip="Adds Drive Recovery/High Drive Recovery into the moogle shop.",
        randomizable=True
    ),

    Toggle(
        name=settingkey.SHOP_BOOSTS,
        ui_label='Stat Boosts',
        standalone_label='Stat Boosts in Shop',
        shared=True,
        default=False,
        tooltip="Adds Power/Magic/AP/Defense Boosts into the moogle shop.",
        randomizable=True
    ),

    IntSpinner(
        name=settingkey.SHOP_REPORTS,
        ui_label='Add Ansem Reports To Shop',
        standalone_label='# Ansem Reports in Shop',
        shared=True,
        minimum=0,
        maximum=13,
        step=1,
        default=0,
        tooltip="Adds a number of Ansem Reports into the moogle shop.",
        randomizable=[0,1,2,3]
    ),

    IntSpinner(
        name=settingkey.SHOP_UNLOCKS,
        ui_label='Add Visit Unlocks To Shop',
        standalone_label='# Visit Unlocks in Shop',
        shared=True,
        minimum=0,
        maximum=11,
        step=1,
        default=0,
        tooltip="Adds a number of visit unlocks into the moogle shop.",
        randomizable=[0,1,2,3]
    ),

    Toggle(
        name=settingkey.TT1_JAILBREAK,
        ui_label='Early Twilight Town 1 Exit',
        shared=True,
        default=False,
        tooltip='Allows the use of save points to leave Twilight Town 1 anytime.'
    ),

    Toggle(
        name=settingkey.ROXAS_ABILITIES_ENABLED,
        ui_label='Roxas Magic/Movement/Trinity',
        shared=True,
        default=False,
        tooltip='Allows Roxas to use magic, Sora\'s movement abilities, and Trinity Limit in Simulated Twilight Town.'
    ),

    Toggle(
        name=settingkey.DISABLE_FINAL_FORM,
        ui_label='Disable Final Form',
        shared=True,
        default=False,
        tooltip='''
        Disables going into Final Form in any way.
        Final Form can still be found to let other forms level up and for Final Genie.
        All items from Final Form are replaced with junk.
        '''
    ),

    Toggle(
        name=settingkey.BLOCK_COR_SKIP,
        ui_label='Block Skipping CoR',
        shared=True,
        default=False,
        tooltip='Disables skipping into the Cavern of Remembrance, requiring completion of the fights to progress.'
    ),

    Toggle(
        name=settingkey.BLOCK_SHAN_YU_SKIP,
        ui_label='Block Skipping Shan-Yu',
        shared=True,
        default=False,
        tooltip='Disables skipping into the throne room of Land of Dragons, requiring beating Shan-Yu to progress.'
    ),

    Toggle(
        name=settingkey.ENABLE_PROMISE_CHARM,
        ui_label='Promise Charm',
        shared=True,
        default=False,
        tooltip='''
        If enabled, the Promise Charm will be added to the item pool.
        This allows skipping TWTNW by talking to the computer in the Garden of Assemblage when you have all 3 Proofs.
        ''',
        randomizable=True
    ),

    MultiSelect(
        name=settingkey.STARTING_STORY_UNLOCKS,
        ui_label='Starting Visit Unlocks',
        choices={
            '74': 'Identity Disk',
            '62': 'Skill and Crossbones',
            '376': 'Picture',
            '375': 'Ice Cream',
            '54': 'Battlefields of War',
            '60': 'Bone Fist',
            '55': 'Sword of the Ancestor',
            '59': "Beast's Claw",
            '72': 'Scimitar',
            '61': 'Proud Fang',
            '369': 'Membership Card',
        },
        shared=True,
        default=['74','62','376','375','54','60','55','59','72','61','369'],
        tooltip='''
        Start with the selected visit unlocks already obtained.
        Each of these items unlocks a second (or third) visit of a particular world.
        See the website for more details.
        ''',
    ),

    Toggle(
        name=settingkey.MAPS_IN_ITEM_POOL,
        ui_label='Maps',
        standalone_label='Maps in Item Pool',
        shared=True,
        default=True,
        tooltip="If enabled, maps are included in the required item pool. Disabling frees up more slots for the other 'junk' items.",
    ),

    Toggle(
        name=settingkey.RECIPES_IN_ITEM_POOL,
        ui_label='Synthesis Recipes',
        standalone_label='Synthesis Recipes in Item Pool',
        shared=True,
        default=True,
        tooltip="If enabled, recipes are included in the required item pool. Disabling frees up more slots for the other 'junk' items.",
    ),

    Toggle(
        name=settingkey.ACCESSORIES_IN_ITEM_POOL,
        ui_label='Accessories',
        standalone_label='Accessories in Item Pool',
        shared=True,
        default=True,
        tooltip="If enabled, all accessories are included in the required item pool.",
    ),
    Toggle(
        name=settingkey.ARMOR_IN_ITEM_POOL,
        ui_label='Armor',
        standalone_label='Armor in Item Pool',
        shared=True,
        default=True,
        tooltip="If enabled, all armor items are included in the required item pool.",
    ),

    Toggle(
        name=settingkey.REMOVE_POPUPS,
        ui_label='Remove Non-Superboss Popups',
        shared=True,
        default=False,
        tooltip="Removes story popup and bonus rewards from eligble location pool for non-junk items. Used for door-rando primarily.",
        randomizable=False
    ),

    SingleSelect(
        name=settingkey.STORY_UNLOCK_CATEGORY,
        ui_label='Visit Unlock Category',
        choices={
            itemRarity.COMMON : itemRarity.COMMON,
            itemRarity.UNCOMMON : itemRarity.UNCOMMON,
            itemRarity.RARE : itemRarity.RARE,
            itemRarity.MYTHIC : itemRarity.MYTHIC,
        },
        shared=True,
        default=itemRarity.UNCOMMON,
        randomizable=False,
        tooltip='''
        Change visit unlocks to have one of the 4 categories (Common,Uncommon,Rare,Mythic) that influence what bias
        each item gets when randomizing.
         
        Setting to Rare or Mythic will make these unlocking items more likely to be locked behind other key items
        in the harder item placement difficulties.
        ''',
    ),

    SingleSelect(
        name=settingkey.ITEM_PLACEMENT_DIFFICULTY,
        ui_label='Item Placement Difficulty',
        choices={
            'Super Easy': 'Super Easy',
            'Easy': 'Easy',
            'Slightly Easy': 'Slightly Easy',
            'Normal': 'Normal',
            'Slightly Hard': 'Slightly Hard',
            'Hard': 'Hard',
            'Very Hard': 'Very Hard',
            'Insane': 'Insane',
            'Nightmare': 'Nightmare'
        },
        shared=True,
        default='Normal',
        randomizable=["Easy","Slightly Easy","Normal","Slightly Hard","Hard"],
        tooltip='''
        Bias the placement of items based on how difficult/easy you would like the seed to be. 
        Items have 4 categories (Common, Uncommon, Rare, Mythic) that influence what bias each item gets when placing those items. 
        Super Easy and Easy will bias Rare and Mythic items early, while the Hard settings will bias those later.
        ''',
    ),

    Toggle(
        name=settingkey.NIGHTMARE_LOGIC,
        ui_label='Extended Item Placement Logic',
        shared=True,
        default=False,
        tooltip="Enables weighting for keyblades with good abilities, and puts auto forms and final forcing `in-logic` meaning they may be required to complete the seed.",
        randomizable=True
    ),

    SingleSelect(
        name=settingkey.SOFTLOCK_CHECKING,
        ui_label='Softlock Prevention',
        choices={
            'default': 'Regular Rando',
            'reverse': 'Reverse Rando',
            'both': 'Satisfy Regular & Reverse'
        },
        shared=True,
        default="default",
        tooltip='''
        What type of rando are you playing?
        
        Regular Rando - The default setting.
        
        Reverse Rando - Playing with visits reversed.
        
        Satisfy Regular & Reverse - Playing cooperatively with both regular and reverse.
        '''
    ),

    SingleSelect(
        name=settingkey.ACCESSIBILITY,
        ui_label='Accessibility',
        standalone_label='Item Accessibility',
        choices={
            'all': '100% Locations',
            'beatable': 'Beatable',
        },
        shared=True,
        default="all",
        tooltip='''
        How accessible locations need to be for the seed to be "completable".
        
        100% Locations - All locations must be reachable, and nothing will be permanently locked.
        
        Beatable - The 3 Proofs must be reachable, but nothing else is guaranteed. 
        '''
    ),

    SingleSelect(
        name=settingkey.ABILITY_POOL,
        ui_label='Ability Pool',
        choices={
            'default': 'Default Abilities',
            'randomize': 'Randomize Ability Pool',
            'randomize support': 'Randomize Support Ability Pool',
            'randomize stackable': 'Randomize Stackable Abilities'
        },
        shared=True,
        default='default',
        tooltip='''
        Configures the ability pool randomization.
    
        Randomize Ability Pool - Picks Sora\'s action/support abilities at random
        (guaranteed to have 1 Second Chance and 1 Once More).
         
        Randomize Support Ability Pool - Leaves action abilities alone, but will randomize the support abilities
        (still guaranteed to have 1 Second Chance and 1 Once More).
        
        Randomize Stackable Abilities - Gives 1 of each ability that works on its own, but randomizes how many of
        the stackable abilities you can get (guaranteeing at least 1 of each).
        ''',
        randomizable=["default","randomize support","randomize stackable"]
    ),

    SingleSelect(
        name=settingkey.COMMAND_MENU,
        ui_label='Command Menu',
        choices=RandomCmdMenu.getOptions(),
        shared=False,
        default='vanilla',
        tooltip='''
        Controls the appearance of the command menu on-screen.
        
        Vanilla - Command menus will have their normal appearance.
        
        Randomize (one) - Chooses a single random command menu to use for the entire game.
        
        Randomize (all) - Chooses random command menus for each world/location that has a unique command menu.
        
        individual command menu options - Forces all command menus to have the chosen appearance.
        '''
    ),

    Toggle(
        name=settingkey.MUSIC_RANDO_ENABLED_PC,
        ui_label='Randomize Music',
        shared=False,
        default=False,
        tooltip='''
        If enabled, randomizes in-game music.

        See the Randomized Music page on the website for more detailed instructions.
        '''
    ),

    Toggle(
        name=settingkey.MUSIC_RANDO_PC_ALLOW_DUPLICATES,
        ui_label='Allow Duplicate Replacements',
        shared=False,
        default=False,
        tooltip='''
        If enabled, song replacements are used multiple times if there aren't enough replacements for every song.

        If disabled, replacement songs are only used once, and some songs will stay un-randomized if there aren't
        enough replacements.
        '''
    ),

    Toggle(
        name=settingkey.MUSIC_RANDO_PC_INCLUDE_ALL_KH2,
        ui_label='Include All KH2 Music',
        shared=False,
        default=False,
        tooltip='''
        If enabled, includes all the base KH2 songs in the song list for music rando.

        Requires the OpenKH folder to be set up in the Configure menu.
        '''
    ),
]


def _get_boss_enemy_settings():
    boss_settings = []
    enemy_settings = []
    boss_enemy_config = khbr()._get_game('kh2').get_options()
    for key in boss_enemy_config.keys():
        if key == 'memory_expansion':
            continue
        config = boss_enemy_config[key]
        possible_values = config['possible_values']
        if True in possible_values:
            # needs to be a toggle
            ui_widget = Toggle(
                name=key,
                ui_label=config['display_name'],
                shared=True,
                default=False,
                tooltip=config['description']
            )
        else:
            # single select
            choices = {choice: choice for choice in possible_values}
            ui_widget = SingleSelect(
                name=key,
                ui_label=config['display_name'],
                choices=choices,
                shared=True,
                default=possible_values[0],
                tooltip=config['description']
            )
        if config.get("type") == "enemy":
            enemy_settings.append(ui_widget)
        else:
            boss_settings.append(ui_widget)
    return boss_settings, enemy_settings


boss_settings, enemy_settings = _get_boss_enemy_settings()
for boss_enemy_setting in boss_settings+enemy_settings:
    _all_settings.append(boss_enemy_setting)

settings_by_name = {setting.name: setting for setting in _all_settings}

DELIMITER = "-"


class SeedSettings:

    def __init__(self):
        self._values = {setting.name: setting.default for setting in _all_settings}
        self._randomizable = [setting for setting in _all_settings if setting.randomizable]
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
        return {name: setting for (name, setting) in settings_by_name.items() if setting.shared or include_private}

    def settings_string(self, include_private: bool = False):
        flags: [bool] = []
        short_select_values = ''
        values: [str] = []
        for name in sorted(self._filtered_settings(include_private)):
            setting = settings_by_name[name]
            value = self._values[name]
            if isinstance(setting, Toggle):
                flags.append(value)
            elif isinstance(setting, SingleSelect) and len(setting.choice_keys) <= SHORT_SELECT_LIMIT:
                index = setting.choice_keys.index(value)
                short_select_values += single_select_chars[index]
            elif isinstance(setting, IntSpinner) and len(setting.selectable_values) <= SHORT_SELECT_LIMIT:
                index = setting.selectable_values.index(value)
                short_select_values += single_select_chars[index]
            elif isinstance(setting, FloatSpinner) and len(setting.selectable_values) <= SHORT_SELECT_LIMIT:
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

    def apply_settings_string(self, settings_string: str, include_private: bool = False):
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
            elif isinstance(setting, SingleSelect) and len(setting.choice_keys) <= SHORT_SELECT_LIMIT:
                short_select_settings.append(setting)
            elif isinstance(setting, IntSpinner) and len(setting.selectable_values) <= SHORT_SELECT_LIMIT:
                short_select_settings.append(setting)
            elif isinstance(setting, FloatSpinner) and len(setting.selectable_values) <= SHORT_SELECT_LIMIT:
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
        filtered_settings = {key: self.get(key) for key in self._filtered_settings(include_private).keys()}
        return filtered_settings

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
    randomizable_settings = [setting for setting in _all_settings if setting.randomizable]
    text = "Randomized settings will randomize the following options: ["
    for r in randomizable_settings:
        text+=r.ui_label+", "
    text+="] \n Worlds/Bosses/Misc Locations will only be turned off randomly, so anything that is set to off before generating a seed will stay off (e.g. if Datas are off, they will stay off)"
    return text
    

def randomize_settings(real_settings_object: SeedSettings, randomizable_settings_names):
    randomizable_settings = [setting for setting in _all_settings if setting.name in randomizable_settings_names]
    setting_choices = {}
    multi_selects = []
    trimulti_selects = []
    for r in randomizable_settings:
        if isinstance(r,SingleSelect):
            if r.randomizable is True: # randomize all choices
                setting_choices[r.name] = [c for c in r.choices]
            elif isinstance(r.randomizable, list):
                setting_choices[r.name] = [c for c in r.randomizable]
        elif isinstance(r,Toggle):
            setting_choices[r.name] = [True,False]
        elif isinstance(r,IntSpinner):
            setting_choices[r.name] = [c for c in r.selectable_values ]
        elif isinstance(r,FloatSpinner):
            setting_choices[r.name] = [c for c in r.selectable_values ]
        elif isinstance(r,MultiSelect):
            # get the current set of values, will allow for some to be removed
            setting_choices[r.name] = [c for c in real_settings_object.get(r.name)]
            multi_selects.append(r.name)
        elif isinstance(r,MultiSelectTristate): # TODO make this work
            # get the current set of values, will allow for some to be removed
            setting_choices[r.name] = real_settings_object.get(r.name)
            trimulti_selects.append(r.name)

    
    for r in randomizable_settings:
        if r.name not in setting_choices:
            raise SettingsException(f"Improper configuration of rando rando settings object. Missing configuration for {r.name}")

    random_choices = {}
    for r in randomizable_settings:
        if r.name in multi_selects: # TODO make this work
            random_choices[r.name] = [c for c in setting_choices[r.name]]
            # pick a fraction of the multi's to keep
            num_to_remove = random.randint(0,len(setting_choices[r.name]))
            for iter in range(num_to_remove):
                choice = random.choice(random_choices[r.name])
                random_choices[r.name].remove(choice)
        elif r.name in trimulti_selects:
            random_choices[r.name] = [[],[]]
            for r_world in setting_choices[r.name][0]:
                prob = random.random()
                if prob < (2.0/3.0):
                    random_choices[r.name][0].append(r_world)
                elif prob < (2.5/3.0):
                    random_choices[r.name][1].append(r_world)
            for r_world in setting_choices[r.name][1]:
                prob = random.random()
                if prob < (1.0/2.0):
                    random_choices[r.name][1].append(r_world)
        else:
            random_choices[r.name] = random.choice(setting_choices[r.name])

    if settingkey.KEYBLADE_MIN_STAT in random_choices and settingkey.KEYBLADE_MAX_STAT in random_choices:
        if random_choices[settingkey.KEYBLADE_MIN_STAT] > random_choices[settingkey.KEYBLADE_MAX_STAT]:
            random_choices[settingkey.KEYBLADE_MAX_STAT] = random_choices[settingkey.KEYBLADE_MIN_STAT]

    for r in randomizable_settings:
        real_settings_object.set(r.name,random_choices[r.name])


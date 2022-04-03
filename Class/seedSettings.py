import math
import random
import textwrap

from bitstring import BitArray
from khbr.randomizer import Randomizer as khbr

from Class import settingkey
from Class.exceptions import SettingsException
from List.ItemList import Items
from List.configDict import expCurve, locationType, locationDepth
from Module.randomBGM import RandomBGM
from Module.randomCmdMenu import RandomCmdMenu


class Setting:

    def __init__(self, name: str, setting_type: type, ui_label: str, shared: bool, default, tooltip: str, randomizable = None):
        self.name = name
        self.type = setting_type
        self.ui_label = ui_label
        self.shared = shared
        self.default = default
        self.tooltip = tooltip
        self.randomizable = randomizable

    def settings_string(self, value) -> str:
        raise NotImplementedError

    def parse_settings_string(self, settings_string: str):
        raise NotImplementedError


class Toggle(Setting):

    def __init__(self, name: str, ui_label: str, shared: bool, default: bool, tooltip: str = '',randomizable = None):
        super().__init__(name, bool, ui_label, shared, default, tooltip, randomizable)

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
            randomizable = None
    ):
        super().__init__(name, int, ui_label, shared, default, tooltip, randomizable)
        self.min = minimum
        self.max = maximum
        self.step = step

        self.selectable_values = [value for value in range(minimum, maximum + step, step)]

    def settings_string(self, value) -> str:
        index = self.selectable_values.index(value)
        return str(index)

    def parse_settings_string(self, settings_string: str):
        index = int(settings_string)
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
            randomizable = None
    ):
        super().__init__(name, float, ui_label, shared, default, tooltip, randomizable)
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
        return str(index)

    def parse_settings_string(self, settings_string: str):
        index = int(settings_string)
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
            randomizable = None
    ):
        super().__init__(name, str, ui_label, shared, default, tooltip, randomizable)
        self.choices = choices
        self.choice_keys = list(choices.keys())
        self.choice_values = list(choices.values())

    def settings_string(self, value) -> str:
        index = self.choice_keys.index(value)
        return str(index)

    def parse_settings_string(self, settings_string: str):
        index = int(settings_string)
        return self.choice_keys[index]
        

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
            randomizable = None):
        super().__init__(name, str, ui_label, shared, default, tooltip, randomizable)
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

        return str(bit_array.uint)

    def parse_settings_string(self, settings_string: str):
        choice_keys = self.choice_keys

        bit_array = BitArray(uint=int(settings_string), length=len(choice_keys))

        selected_values = []
        for index, choice_key in enumerate(choice_keys):
            if bit_array[index]:
                selected_values.append(choice_key)

        return selected_values

_drive_exp_curve_tooltip_text = textwrap.dedent('''
        Experience curve options, inspired by KH1's experience curves. Midday and dusk will reduce the total 
                EXP needed to get to Level 7, but levels 2,3, and 4 will need more EXP to compensate.
        Dawn: This is the default exp rate from the game, adjusted as well from the multipiers.
        Midday: Early levels (2,3,4) have their required exp increased, later levels (5,6,7) have been lowered.
        Dusk: Early levels (2,3,4) have their required exp further increased, and later levels (5,6,7) are lowered more. 
    ''')

_all_settings = [
    SingleSelect(
        name=settingkey.SORA_LEVELS,
        ui_label='Sora Levels',
        choices={
            'Level': 'Level 1',
            'ExcludeFrom50': 'Level 50',
            'ExcludeFrom99': 'Level 99'
        },
        shared=True,
        default='ExcludeFrom50',
        randomizable=True,
        tooltip="Maximum Level for Randomized Rewards that aren't `junk`"
    ),

    Toggle(
        name=settingkey.LEVEL_ONE,
        ui_label='Level 1 Mode',
        shared=True,
        default=False,
        tooltip='Give no stats or items on level ups, removes abilities that would be on levels in vanilla from the item pool.'
    ),

    Toggle(
        name=settingkey.FORM_LEVEL_REWARDS,
        ui_label='Form Level Rewards',
        shared=True,
        default=True,
        randomizable=True,
        tooltip="Enable non-junk items onto form levels"
    ),

    Toggle(
        name=settingkey.STATSANITY,
        ui_label='Bonus Rewards as Items (Statsanity)',
        shared=True,
        default=False,
        randomizable=True,
        tooltip=textwrap.dedent('''Takes HP, MP, Drive, Accessory Slot, Armor Slot, and Item Slot upgrades from the normal bonus 
popup locations and lets them appear in chests. Those bonus locations can now have other items in them.'''),
    ),

    FloatSpinner(
        name=settingkey.SORA_EXP_MULTIPLIER,
        ui_label='Sora',
        minimum=0.5,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=1.5,
        randomizable=True
    ),

    FloatSpinner(
        name=settingkey.VALOR_EXP_MULTIPLIER,
        ui_label='Valor',
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=7.0,
        randomizable=True
    ),

    FloatSpinner(
        name=settingkey.WISDOM_EXP_MULTIPLIER,
        ui_label='Wisdom',
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=3.0,
        randomizable=True
    ),

    FloatSpinner(
        name=settingkey.LIMIT_EXP_MULTIPLIER,
        ui_label='Limit',
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=3.0,
        randomizable=True
    ),

    FloatSpinner(
        name=settingkey.MASTER_EXP_MULTIPLIER,
        ui_label='Master',
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=3.0,
        randomizable=True
    ),

    FloatSpinner(
        name=settingkey.FINAL_EXP_MULTIPLIER,
        ui_label='Final',
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=3.0,
        randomizable=True
    ),

    FloatSpinner(
        name=settingkey.SUMMON_EXP_MULTIPLIER,
        ui_label='Summon',
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=2.0,
        randomizable=True
    ),
    
    SingleSelect(
        name=settingkey.SORA_EXP_CURVE,
        ui_label='Sora',
        choices={
            expCurve.DAWN.name: "Dawn (Normal)",
            expCurve.MIDDAY.name: "Midday",
            expCurve.DUSK.name: "Dusk"
        },
        shared=True,
        default=expCurve.DAWN.name,
        tooltip=textwrap.dedent('''
            Experience curve options, inspired by KH1's experience curves. Midday and dusk will reduce the total 
                EXP needed to get to 99, but levels before 50 will take more EXP to compensate
            Dawn: This is the default exp rate from the game, adjusted as well from the multipiers.
            Midday: Early levels (up to 50) have their required exp increased, and 50 and later have been lowered.
            Dusk: Early levels (up to 50) have their required exp further increased, and 50 and higher are lowered more. 
        '''),
        randomizable=True
    ),
    
    SingleSelect(
        name=settingkey.VALOR_EXP_CURVE,
        ui_label='Valor',
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
        name=settingkey.WISDOM_EXP_CURVE,
        ui_label='Wisdom',
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
        name=settingkey.MASTER_EXP_CURVE,
        ui_label='Master',
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
        name=settingkey.FINAL_EXP_CURVE,
        ui_label='Final',
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
        shared=True,
        default=True,
        randomizable=True,
        tooltip="Critical Mode Only! When enabled, non-junk items can be in the 7 starting items on critical mode."
    ),

    Toggle(
        name=settingkey.GARDEN_OF_ASSEMBLAGE_REWARDS,
        ui_label='Garden of Assemblage',
        shared=True,
        default=True,
        randomizable=True
    ),

    Toggle(
        name=settingkey.SCHMOVEMENT,
        ui_label='Schmovement',
        shared=True,
        default=False,
        tooltip='Start with level 1 of all growth abilities'
    ),

    Toggle(
        name=settingkey.LIBRARY_OF_ASSEMBLAGE,
        ui_label='Library of Assemblage',
        shared=True,
        default=False,
        tooltip='Start with all the Ansem Reports, which act as hints for JSmartee and Point hints'
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
            '369': 'Membership Card',
            '593': 'Proof of Connection',
            '594': 'Proof of Nonexistence',
            '595': 'Proof of Peace',
            '524': 'Promise Charm',
        },
        shared=True,
        default=[]
    ),

    SingleSelect(
        name=settingkey.HINT_SYSTEM,
        ui_label="Hint System",
        choices={
            'Disabled': 'Disabled',
            'Shananas': 'Shananas',
            'JSmartee': 'JSmartee',
            'Points': 'Points'
        },
        shared=True,
        default='JSmartee',
        tooltip=textwrap.dedent('''
            Disabled - Use no hint system
            JSmartee - Secret Ansem Reports provide information for how many "important checks" are in a world
            Shananas - Each world informs you once the world has no more "important checks"
            Points - Each "important check" is assigned a point value, and you are told the number of points in each world. Secret Ansem Reports tell you where items are.
        '''),
        randomizable=["Shananas","JSmartee","Points"]
    ),

    IntSpinner(
        name=settingkey.POINTS_PROOF,
        ui_label="Proof Point Value",
        minimum=0,
        maximum=20,
        step=1,
        shared=True,
        default=12,
        randomizable=True
    ),

    IntSpinner(
        name=settingkey.POINTS_FORM,
        ui_label="Forms Point Value",
        minimum=0,
        maximum=20,
        step=1,
        shared=True,
        default=10,
        randomizable=True
    ),

    IntSpinner(
        name=settingkey.POINTS_MAGIC,
        ui_label="Magic Point Value",
        minimum=0,
        maximum=20,
        step=1,
        shared=True,
        default=8,
        randomizable=True
    ),

    IntSpinner(
        name=settingkey.POINTS_SUMMON,
        ui_label="Summon Point Value",
        minimum=0,
        maximum=20,
        step=1,
        shared=True,
        default=6,
        randomizable=True
    ),

    IntSpinner(
        name=settingkey.POINTS_ABILITY,
        ui_label="Ability Point Value",
        minimum=0,
        maximum=20,
        step=1,
        shared=True,
        default=4,
        randomizable=True
    ),

    IntSpinner(
        name=settingkey.POINTS_PAGE,
        ui_label="Page Point Value",
        minimum=0,
        maximum=20,
        step=1,
        shared=True,
        default=2,
        randomizable=True
    ),
    
    IntSpinner(
        name=settingkey.POINTS_REPORT,
        ui_label="Report Point Value",
        minimum=0,
        maximum=20,
        step=1,
        shared=True,
        default=2,
        randomizable=True
    ),

    IntSpinner(
        name=settingkey.POINTS_BONUS,
        ui_label="Bonus Level Points",
        minimum=-10,
        maximum=20,
        step=1,
        shared=True,
        default=10,
        randomizable=True
    ),

    IntSpinner(
        name=settingkey.POINTS_COMPLETE,
        ui_label="World Completion Points",
        minimum=-10,
        maximum=20,
        step=1,
        shared=True,
        default=10,
        randomizable=True
    ),

    IntSpinner(
        name=settingkey.POINTS_FORMLV,
        ui_label="Form level Points",
        minimum=-10,
        maximum=20,
        step=1,
        shared=True,
        default=3,
        randomizable=True
    ),


    SingleSelect(
        name=settingkey.REPORT_DEPTH,
        ui_label='Report Depth',
        choices={
            locationDepth.DataFight.name: 'Data Fights',
            locationDepth.FirstVisit.name: 'First Visit',
            locationDepth.SecondVisit.name: 'First/Second Visit',
            locationDepth.FirstBoss.name: 'First Boss',
            locationDepth.SecondBoss.name: 'Second Boss',
            locationDepth.Anywhere.name: "Anywhere"
        },
        shared=True,
        default=locationDepth.SecondVisit.name,
        tooltip=textwrap.dedent('''
            Data Fights - Force the item onto datas
            First Visit - Force the item into a first visit (only the 13 main hub worlds with portals)
            First/Second Visit - Force the item to not be on a data (all other locations possible)
            First Boss - Force the item onto the first visit boss of a world (only the 13 main hub worlds with portals)
            Second Boss - Force the item onto the last boss of a world (only the 13 main hub worlds with portals)
            Anywhere - No restriction
        '''),
        randomizable=[locationDepth.FirstVisit.name, locationDepth.SecondVisit.name, locationDepth.FirstBoss.name, locationDepth.SecondBoss.name, locationDepth.Anywhere.name]
    ),
    SingleSelect(
        name=settingkey.PROOF_DEPTH,
        ui_label='Proof Depth',
        choices={
            locationDepth.DataFight.name: 'Data Fights',
            locationDepth.FirstVisit.name: 'First Visit',
            locationDepth.SecondVisit.name: 'First/Second Visit',
            locationDepth.FirstBoss.name: 'First Boss',
            locationDepth.SecondBoss.name: 'Second Boss',
            locationDepth.Anywhere.name: "Anywhere"
        },
        shared=True,
        default=locationDepth.Anywhere.name,
        tooltip=textwrap.dedent('''
            Data Fights - Force the item onto datas
            First Visit - Force the item into a first visit (only the 13 main hub worlds with portals)
            First/Second Visit - Force the item to not be on a data (all other locations possible)
            First Boss - Force the item onto the first visit boss of a world (only the 13 main hub worlds with portals)
            Second Boss - Force the item onto the last boss of a world (only the 13 main hub worlds with portals)
            Anywhere - No restriction
        '''),
        randomizable=[locationDepth.FirstVisit.name, locationDepth.SecondVisit.name, locationDepth.FirstBoss.name, locationDepth.SecondBoss.name, locationDepth.Anywhere.name]
    ),
    Toggle(
        name=settingkey.YEET_THE_BEAR,
        ui_label='Yeet The Bear Required',
        shared=True,
        default=False,
        tooltip="Force the Proof of Nonexistence onto Starry Hill popup in 100 acre",
        randomizable=True
    ),

    Toggle(
        name=settingkey.PREVENT_SELF_HINTING,
        ui_label='Remove Self-Hinting Reports',
        shared=True,
        default=False,
        tooltip="Reports must hint a world that is different from where that report was found.",
        randomizable=True
    ),

    Toggle(
        name=settingkey.ALLOW_PROOF_HINTING,
        ui_label='Reports can Hint Proofs',
        shared=True,
        default=False,
        tooltip="Points Mode only: If enabled, proofs can be directly hinted by reports.",
        randomizable=True
    ),

    Toggle(
        name=settingkey.ALLOW_REPORT_HINTING,
        ui_label='Reports can Hint other Reports',
        shared=True,
        default=True,
        tooltip="Points Mode only: If enabled, reports can hint other reports.",
        randomizable=True
    ),
    
    IntSpinner(
        name=settingkey.KEYBLADE_MIN_STAT,
        ui_label="Keyblade Min Stat",
        minimum=0,
        maximum=20,
        step=1,
        shared=True,
        default=0,
        randomizable=True
    ),

    IntSpinner(
        name=settingkey.KEYBLADE_MAX_STAT,
        ui_label="Keyblade Max Stat",
        minimum=0,
        maximum=20,
        step=1,
        shared=True,
        default=7,
        randomizable=True
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

    MultiSelect(
        name=settingkey.WORLDS_WITH_REWARDS,
        ui_label='Worlds with Rewards',
        choices={location.name: location.value for location in [
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
            locationType.CoR,
            locationType.Atlantica
        ]},
        shared=True,
        default=[
            locationType.STT.name,
            locationType.HB.name,
            locationType.OC.name,
            locationType.LoD.name,
            locationType.PL.name,
            locationType.HT.name,
            locationType.SP.name,
            locationType.CoR.name,
            locationType.TT.name,
            locationType.BC.name,
            locationType.Agrabah.name,
            locationType.HUNDREDAW.name,
            locationType.DC.name,
            locationType.PR.name,
            locationType.TWTNW.name
        ],
        choice_icons={
            locationType.STT.name: "icons/worlds/simulated_twilight_town.png",
            locationType.HB.name: "icons/worlds/hollow_bastion.png",
            locationType.OC.name: "icons/worlds/olympus_coliseum.png",
            locationType.LoD.name: "icons/worlds/land_of_dragons.png",
            locationType.PL.name: "icons/worlds/pride_lands.png",
            locationType.HT.name: "icons/worlds/halloween_town.png",
            locationType.SP.name: "icons/worlds/space_paranoids.png",
            locationType.CoR.name: "icons/worlds/cavern_of_remembrance.png",
            locationType.TT.name: "icons/worlds/twilight_town.png",
            locationType.BC.name: "icons/worlds/beast's_castle.png",
            locationType.Agrabah.name: "icons/worlds/agrabah.png",
            locationType.HUNDREDAW.name: "icons/worlds/100_acre_wood.png",
            locationType.DC.name: "icons/worlds/disney_castle.png",
            locationType.PR.name: "icons/worlds/port_royal.png",
            locationType.TWTNW.name: "icons/worlds/the_world_that_never_was.png",
            locationType.Atlantica.name: "icons/worlds/atlantica.png"
        },
        randomizable=True
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
            locationType.TTR
        ]},
        shared=True,
        default=[],
        choice_icons={
            locationType.OCCups.name: 'icons/misc/cups.png',
            locationType.OCParadoxCup.name: 'icons/misc/paradox_cup.png',
            locationType.Puzzle.name: 'icons/misc/puzzle.png',
            locationType.TTR.name: 'icons/misc/transport.png'
        },
        randomizable=True
    ),

    Toggle(
        name=settingkey.GLASS_CANNON,
        ui_label='Glass Cannon',
        shared=True,
        default=False,
        tooltip='No more pesky Defense Ups in the level up stats pool'
    ),

    Toggle(
        name=settingkey.BETTER_JUNK,
        ui_label='Better Junk',
        shared=True,
        default=False,
        tooltip='No more synthesis materials in the junk item pool'
    ),
    MultiSelect(
        name=settingkey.JUNK_ITEMS,
        ui_label='Junk Items',
        choices={str(item.Id): item.Name for item in Items.getJunkList(False)},
        shared=True,
        default=list(set([str(item.Id) for item in Items.getJunkList(False)])),
        tooltip='Once all of the required items are placed, items from this list are used to fill the rest. This item pool is also used for worlds that are disabled'
    ),

    Toggle(
        name=settingkey.START_NO_AP,
        ui_label='Start with No AP',
        shared=True,
        default=False,
        tooltip='Sora/Donald/Goofy start the game with 0 AP'
    ),

    
    IntSpinner(
        name=settingkey.SORA_AP,
        ui_label="Sora Starting AP",
        minimum=0,
        maximum=150,
        step=25,
        shared=True,
        default=50,
        randomizable=True
    ),
    IntSpinner(
        name=settingkey.DONALD_AP,
        ui_label="Donald Starting AP",
        minimum=5,
        maximum=55,
        step=5,
        shared=True,
        default=55,
        randomizable=True
    ),
    IntSpinner(
        name=settingkey.GOOFY_AP,
        ui_label="Goofy Starting AP",
        minimum=4,
        maximum=54,
        step=5,
        shared=True,
        default=54,
        randomizable=True
    ),

    Toggle(
        name=settingkey.REMOVE_DAMAGE_CAP,
        ui_label='Remove Damage Cap',
        shared=True,
        default=False,
        tooltip='Removes the damage cap for every enemy/boss in the game'
    ),

    Toggle(
        name=settingkey.CUPS_GIVE_XP,
        ui_label='Cups Give XP',
        shared=True,
        default=False,
        tooltip='Defeating enemies while in an OC Cup will give you XP and Form XP'
    ),

    Toggle(
        name=settingkey.AS_DATA_SPLIT,
        ui_label='Split AS/Data Rewards',
        shared=True,
        default=False,
        tooltip="When enabled, Absent Silhouette rewards will NOT give the reward from their Data Org versions. You must beat the Data Org version to get its reward"
    ),

    Toggle(
        name=settingkey.RETRY_DFX,
        ui_label='Retry Data Final Xemnas',
        shared=True,
        default=False,
        tooltip='If you die to Data Final Xemnas, continue will put you right back into the fight, instead of having to fight Data Xemnas I again (warning will be a softlock if you are unable to beat Final Xemnas)'
    ),

    Toggle(
        name=settingkey.ENABLE_PROMISE_CHARM,
        ui_label='Enable Promise Charm',
        shared=True,
        default=False,
        tooltip="If enabled, the promise charm will be added to the item pool, which can allow skipping TWTNW by talking to the computer in the GoA when you have all 3 proofs",
        randomizable=True
    ),

    SingleSelect(
        name=settingkey.ITEM_PLACEMENT_DIFFICULTY,
        ui_label='Item Placement Difficulty',
        choices={
            'Super Easy': 'Super Easy',
            'Easy': 'Easy',
            'Normal': 'Normal',
            'Hard': 'Hard',
            'Very Hard': 'Very Hard',
            'Insane': 'Insane',
            'Nightmare': 'Nightmare'
        },
        shared=True,
        default='Normal',
        randomizable=["Easy","Normal","Hard","Very Hard"],
        tooltip=textwrap.dedent('''
            Bias the placement of items based on how difficult/easy you would like the seed to be. 
            Items have 4 categories (Common,Uncommon,Rare,Mythic) that influence what bias each item gets when placing those items. 
            Super Easy and Easy will bias Rare and Mythic items early, while the Hard settings will bias those later.
        '''),
    ),
    Toggle(
        name=settingkey.REVERSE_RANDO,
        ui_label='Reverse Rando',
        shared=True,
        default=False,
        tooltip='Use when generating a Reverse Rando seed to ensure softlock prevention'
    ),

    SingleSelect(
        name=settingkey.ABILITY_POOL,
        ui_label='Ability Pool',
        choices={
            'default': 'Default Abilities',
            'randomize': 'Randomize Ability Pool',
            'randomize support': 'Randomize Support Ability Pool'
        },
        shared=True,
        default='default',
        tooltip='If "Randomize Ability Pool", picks Sora\'s action/support abilities at random (guaranteed to have 1 SC & 1 OM). \nRandomized Support Ability Pool will leave action abilities alone, but will randomize the support abilities (still guaranteed to have SC/OM)'
    ),

    SingleSelect(
        name=settingkey.COMMAND_MENU,
        ui_label='Command Menu',
        choices=RandomCmdMenu.getOptions(),
        shared=False,
        default='vanilla'
    ),

    MultiSelect(
        name=settingkey.BGM_OPTIONS,
        ui_label='Music Options (PC Only)',
        choices={option: option for option in RandomBGM.getOptions()},
        shared=False,
        default=[]
    ),

    MultiSelect(
        name=settingkey.BGM_GAMES,
        ui_label='Music Games To Include',
        choices={option: option for option in RandomBGM.getGames()},
        shared=False,
        default=[]
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
        self._observers = {}

    def get(self, name: str):
        return self._values[name]

    def set(self, name: str, value):
        self._values[name] = value
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
        values = []
        for name in sorted(self._filtered_settings(include_private)):
            setting = settings_by_name[name]
            values.append(setting.settings_string(self._values[name]))
        return DELIMITER.join(values)

    def apply_settings_string(self, settings_string: str, include_private: bool = False):
        parts = settings_string.split(DELIMITER)
        for index, name in enumerate(sorted(self._filtered_settings(include_private))):
            setting = settings_by_name[name]
            self.set(name, setting.parse_settings_string(parts[index]))

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
    

class RandoRandoSettings:
    def __init__(self, real_settings_object: SeedSettings):
        self.randomizable_settings = [setting for setting in _all_settings if setting.randomizable]
        self.static_settings = [setting for setting in _all_settings if setting.randomizable is None]
        self.setting_choices = {}
        self.multi_selects = []
        for r in self.randomizable_settings:
            if isinstance(r,SingleSelect):
                if r.randomizable is True: # randomize all choices
                    self.setting_choices[r.name] = [c for c in r.choices]
                elif isinstance(r.randomizable, list):
                    self.setting_choices[r.name] = [c for c in r.randomizable]
            if isinstance(r,Toggle):
                self.setting_choices[r.name] = [True,False]
            if isinstance(r,IntSpinner):
                self.setting_choices[r.name] = [c for c in r.selectable_values if c != 0]
            if isinstance(r,FloatSpinner):
                # get set value from settings, and then allow all values larger than that
                self.setting_choices[r.name] = [c for c in r.selectable_values if c >= real_settings_object.get(r.name)]
            if isinstance(r,MultiSelect):
                # get the current set of values, will allow for some to be removed
                self.setting_choices[r.name] = [c for c in real_settings_object.get(r.name)]
                self.multi_selects.append(r.name)

        
        for r in self.randomizable_settings:
            if r.name not in self.setting_choices:
                raise SettingsException(f"Improper configuration of rando rando settings object. Missing configuration for {r.name}")

        self.random_choices = {}
        for r in self.randomizable_settings:
            if r.name in self.multi_selects:
                self.random_choices[r.name] = [c for c in self.setting_choices[r.name]]
                # pick a fraction of the multi's to keep
                num_to_remove = random.randint(0,math.ceil(.2*len(self.setting_choices[r.name])))
                for iter in range(num_to_remove):
                    choice = random.choice(self.random_choices[r.name])
                    self.random_choices[r.name].remove(choice)
            else:
                self.random_choices[r.name] = random.choice(self.setting_choices[r.name])

        while self.random_choices[settingkey.REPORT_DEPTH]==self.random_choices[settingkey.PROOF_DEPTH] and self.random_choices[settingkey.PROOF_DEPTH] in [locationDepth.DataFight.name,locationDepth.FirstBoss.name,locationDepth.SecondBoss.name]:
            # can't make these depths the same very restricted location
            self.random_choices[settingkey.REPORT_DEPTH] = random.choice(self.setting_choices[settingkey.REPORT_DEPTH])
            self.random_choices[settingkey.PROOF_DEPTH] = random.choice(self.setting_choices[settingkey.PROOF_DEPTH])
        
        if locationType.TTR.name in self.random_choices[settingkey.MISC_LOCATIONS_WITH_REWARDS] and self.random_choices[settingkey.STATSANITY] is False:
            # can't enable TTR and not be in statsanity
            self.random_choices[settingkey.STATSANITY] = True

        if self.random_choices[settingkey.KEYBLADE_MIN_STAT] > self.random_choices[settingkey.KEYBLADE_MAX_STAT]:
            self.random_choices[settingkey.KEYBLADE_MAX_STAT] = self.random_choices[settingkey.KEYBLADE_MIN_STAT]

        for r in self.randomizable_settings:
            real_settings_object.set(r.name,self.random_choices[r.name])


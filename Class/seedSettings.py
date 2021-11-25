import string
import textwrap

from khbr.randomizer import Randomizer as khbr

from Class import settingkey
from List.ItemList import Items
from List.configDict import locationType, locationDepth
from Module.randomBGM import RandomBGM
from Module.randomCmdMenu import RandomCmdMenu

# Characters safe to use in settings strings
_available_chars = string.digits + string.ascii_uppercase + string.ascii_lowercase


class Setting:

    def __init__(self, name: str, setting_type: type, ui_label: str, shared: bool, default, tooltip: str):
        self.name = name
        self.type = setting_type
        self.ui_label = ui_label
        self.shared = shared
        self.default = default
        self.tooltip = tooltip

    def settings_string(self, value) -> str:
        raise NotImplementedError

    def parse_settings_string(self, settings_string: str):
        raise NotImplementedError


class Toggle(Setting):

    def __init__(self, name: str, ui_label: str, shared: bool, default: bool, tooltip: str = ''):
        super().__init__(name, bool, ui_label, shared, default, tooltip)

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
            tooltip: str = ''
    ):
        super().__init__(name, int, ui_label, shared, default, tooltip)
        self.min = minimum
        self.max = maximum
        self.step = step

        self.selectable_values = [value for value in range(minimum, maximum + step, step)]

    def settings_string(self, value) -> str:
        index = self.selectable_values.index(value)
        return _available_chars[index]

    def parse_settings_string(self, settings_string: str):
        index = _available_chars.index(settings_string)
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
            tooltip: str = ''
    ):
        super().__init__(name, float, ui_label, shared, default, tooltip)
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
        return _available_chars[index]

    def parse_settings_string(self, settings_string: str):
        index = _available_chars.index(settings_string)
        return self.selectable_values[index]


class SingleSelect(Setting):

    def __init__(
            self,
            name: str,
            ui_label: str,
            choices: dict[str, str],
            shared: bool,
            default: str,
            tooltip: str = ''
    ):
        super().__init__(name, str, ui_label, shared, default, tooltip)
        self.choices = choices
        self.choice_keys = list(choices.keys())
        self.choice_values = list(choices.values())

    def settings_string(self, value) -> str:
        index = self.choice_keys.index(value)
        return _available_chars[index]

    def parse_settings_string(self, settings_string: str):
        index = _available_chars.index(settings_string)
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
            tooltip: str = ''):
        super().__init__(name, str, ui_label, shared, default, tooltip)
        self.choices = choices
        self.choice_keys = list(choices.keys())
        self.choice_values = list(choices.values())
        self.choice_icons = choice_icons

    def settings_string(self, value) -> str:
        selected_indexes = ''
        for selected in value:
            index = self.choice_keys.index(selected)
            selected_indexes += _available_chars[index]
        return selected_indexes

    def parse_settings_string(self, settings_string: str):
        selected_values = []
        for character in settings_string:
            index = _available_chars.index(character)
            selected_values.append(self.choice_keys[index])
        return selected_values


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
        default='ExcludeFrom50'
    ),

    Toggle(
        name=settingkey.FORM_LEVEL_REWARDS,
        ui_label='Form Level Rewards',
        shared=True,
        default=True
    ),

    Toggle(
        name=settingkey.STATSANITY,
        ui_label='Statsanity',
        shared=True,
        default=False
    ),

    FloatSpinner(
        name=settingkey.SORA_EXP_MULTIPLIER,
        ui_label='Sora',
        minimum=0.5,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=1.5
    ),

    FloatSpinner(
        name=settingkey.VALOR_EXP_MULTIPLIER,
        ui_label='Valor',
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=7.0
    ),

    FloatSpinner(
        name=settingkey.WISDOM_EXP_MULTIPLIER,
        ui_label='Wisdom',
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=3.0
    ),

    FloatSpinner(
        name=settingkey.LIMIT_EXP_MULTIPLIER,
        ui_label='Limit',
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=3.0
    ),

    FloatSpinner(
        name=settingkey.MASTER_EXP_MULTIPLIER,
        ui_label='Master',
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=3.0
    ),

    FloatSpinner(
        name=settingkey.FINAL_EXP_MULTIPLIER,
        ui_label='Final',
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=3.0
    ),

    FloatSpinner(
        name=settingkey.SUMMON_EXP_MULTIPLIER,
        ui_label='Summon',
        minimum=1.0,
        maximum=10.0,
        step=0.5,
        shared=True,
        default=2.0
    ),

    Toggle(
        name=settingkey.CRITICAL_BONUS_REWARDS,
        ui_label='Critical Bonuses',
        shared=True,
        default=True
    ),

    Toggle(
        name=settingkey.GARDEN_OF_ASSEMBLAGE_REWARDS,
        ui_label='Garden of Assemblage',
        shared=True,
        default=True
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
        tooltip='Start with all the hints'
    ),

    MultiSelect(
        name=settingkey.STARTING_INVENTORY,
        ui_label='Starting Inventory',
        choices={
            '138': 'Scan',
            '404': 'No Experience',
            '158': 'Aerial Recovery',
            '82': 'Guard',
            '537': 'Hades Cup Trophy',
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
        ''')
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
        default=locationDepth.SecondVisit.name
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
        default=locationDepth.Anywhere.name
    ),

    Toggle(
        name=settingkey.PREVENT_SELF_HINTING,
        ui_label='Remove Self-Hinting Reports',
        shared=True,
        default=False
    ),

    Toggle(
        name=settingkey.ALLOW_PROOF_HINTING,
        ui_label='Reports can Hint Proofs',
        shared=True,
        default=False
    ),

    IntSpinner(
        name=settingkey.KEYBLADE_MIN_STAT,
        ui_label="Keyblade Min Stat",
        minimum=0,
        maximum=20,
        step=1,
        shared=True,
        default=0
    ),

    IntSpinner(
        name=settingkey.KEYBLADE_MAX_STAT,
        ui_label="Keyblade Max Stat",
        minimum=0,
        maximum=20,
        step=1,
        shared=True,
        default=7
    ),

    MultiSelect(
        name=settingkey.KEYBLADE_SUPPORT_ABILITIES,
        ui_label='Support Keyblade-Eligible Abilities',
        choices={str(item.Id): item.Name for item in Items.getSupportAbilityList()},
        shared=True,
        default=list(set([str(item.Id) for item in Items.getSupportAbilityList()])),
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
        }
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
        }
    ),

    MultiSelect(
        name=settingkey.MISC_LOCATIONS_WITH_REWARDS,
        ui_label='Misc Locations with Rewards',
        choices={location.name: location.value for location in [
            locationType.OCCups,
            locationType.OCParadoxCup,
            locationType.Puzzle
        ]},
        shared=True,
        default=[],
        choice_icons={
            locationType.OCCups.name: 'icons/misc/cups.png',
            locationType.OCParadoxCup.name: 'icons/misc/paradox_cup.png',
            locationType.Puzzle.name: 'icons/misc/puzzle.png'
        }
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

    Toggle(
        name=settingkey.START_NO_AP,
        ui_label='Start with No AP',
        shared=True,
        default=False,
        tooltip='Sora/Donald/Goofy start the game with 0 AP'
    ),

    Toggle(
        name=settingkey.REMOVE_DAMAGE_CAP,
        ui_label='Remove Damage Cap',
        shared=True,
        default=False,
        tooltip='Removes the damage cap for every enemy/boss in the game'
    ),

    Toggle(
        name=settingkey.ENABLE_PROMISE_CHARM,
        ui_label='Enable Promise Charm',
        shared=True,
        default=False
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
        default='Normal'
    ),

    Toggle(
        name=settingkey.MAX_LOGIC_ITEM_PLACEMENT,
        ui_label='Max Logic Item Placement',
        shared=True,
        default=False,
        tooltip='Less restricted item placement (all checks still obtainable)'
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
            'randomize': 'Randomize Ability Pool'
        },
        shared=True,
        default='default',
        tooltip='If "Randomize Ability Pool", picks Sora\'s action/support abilities at random (guaranteed to have 1 SC & 1 OM)'
    ),

    SingleSelect(
        name=settingkey.COMMAND_MENU,
        ui_label='Command Menu (PS2 Only)',
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
    settings = []
    boss_enemy_config = khbr()._get_game('kh2').get_options()
    for key in boss_enemy_config.keys():
        if key == 'memory_expansion':
            continue
        config = boss_enemy_config[key]
        possible_values = config['possible_values']
        if True in possible_values:
            # needs to be a toggle
            toggle = Toggle(
                name=key,
                ui_label=config['display_name'],
                shared=True,
                default=False,
                tooltip=config['description']
            )
            settings.append(toggle)
        else:
            # single select
            choices = {choice: choice for choice in possible_values}
            select = SingleSelect(
                name=key,
                ui_label=config['display_name'],
                choices=choices,
                shared=True,
                default=possible_values[0],
                tooltip=config['description']
            )
            settings.append(select)

    return settings


boss_enemy_settings = _get_boss_enemy_settings()
for boss_enemy_setting in boss_enemy_settings:
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
        filtered_keys = self._filtered_settings(include_private).keys()
        for key, value in settings_json.items():
            if key in filtered_keys:
                self.set(key, value)


from Module.modifier import SeedModifier
from List.experienceValues import soraExp, formExp
from List.hashTextEntries import generateHashIcons
from List.configDict import locationCategory, locationType, itemType, locationDepth
from itertools import chain
import math,random,json
from Class import seedSettings, settingkey
from Class.seedSettings import SeedSettings

class RandomizerSettings():
    excludeFrom50 = list(chain([1,3,5,6,8,11,13,16,18,19,21,22,24,26,27,29,31,33,35,37,38,40,42,43,45,47,49],range(51,100)))
    excludeFrom99 = [1,2,3,4,5,6,8,10,11,13,14,16,18,19,21,22,24,26,27,29,30,32,34,35,37,38,40,42,43,45,46,48,50,51,52,54,55,56,57,58,60,61,62,63,64,66,67,68,69,70,71,72,74,75,76,77,78,79,80,81,82,83,84,86,87,88,89,90,91,92,93,94,95,96,97,98]
    
    def __init__(self, seed_name: str, spoiler_log: bool, ui_version: str, ui_settings: SeedSettings):

        include_list = []
        include_list_keys = [
            (settingkey.FORM_LEVEL_REWARDS, 'Form Levels'),
            (settingkey.CRITICAL_BONUS_REWARDS, 'Critical Bonuses'),
            (settingkey.GARDEN_OF_ASSEMBLAGE_REWARDS, 'Garden of Assemblage'),
        ]
        for key in include_list_keys:
            if ui_settings.get(key[0]):
                include_list.append(key[1])
        for location in ui_settings.get(settingkey.WORLDS_WITH_REWARDS):
            include_list.append(locationType[location].value)
        for location in ui_settings.get(settingkey.SUPERBOSSES_WITH_REWARDS):
            include_list.append(locationType[location].value)
        for location in ui_settings.get(settingkey.MISC_LOCATIONS_WITH_REWARDS):
            include_list.append(locationType[location].value)
        self.enabledLocations = [l for l in locationType if l in include_list]
        self.disabledLocations = [l for l in locationType if l not in include_list and l not in [locationType.Mush13,locationType.WeaponSlot,locationType.Level]]
       
        level_setting = ui_settings.get(settingkey.SORA_LEVELS)
        if level_setting=="Level":
            self.setLevelChecks(1)
        elif level_setting=="ExcludeFrom50":
            self.setLevelChecks(50)
        elif level_setting=="ExcludeFrom99":
            self.setLevelChecks(99)
        else:
            raise RuntimeError("Invalid Level choice")
        self.startingItems = [int(value) for value in ui_settings.get(settingkey.STARTING_INVENTORY)] + SeedModifier.schmovement(ui_settings.get(settingkey.SCHMOVEMENT)) + SeedModifier.library(ui_settings.get(settingkey.LIBRARY_OF_ASSEMBLAGE))
        self.itemPlacementDifficulty = ui_settings.get(settingkey.ITEM_PLACEMENT_DIFFICULTY)
        self.reverse_rando = ui_settings.get(settingkey.REVERSE_RANDO)
        self.level_stat_pool = SeedModifier.glassCannon if ui_settings.get(settingkey.GLASS_CANNON) else SeedModifier.regularStats
        self.betterJunk = ui_settings.get(settingkey.BETTER_JUNK)
        self.no_ap = ui_settings.get(settingkey.START_NO_AP)

        ui_ability_pool = ui_settings.get(settingkey.ABILITY_POOL)
        if ui_ability_pool == "default":
            self.abilityListModifier = SeedModifier.defaultAbilityPool
        elif ui_ability_pool == "randomize":
            self.abilityListModifier = SeedModifier.randomAbilityPool
        else:
            raise RuntimeError("Invalid ability pool option")

        self.promiseCharm = ui_settings.get(settingkey.ENABLE_PROMISE_CHARM)
        self.hintsType = ui_settings.get(settingkey.HINT_SYSTEM)
        self.reportDepth = [l for l in locationDepth if l==ui_settings.get(settingkey.REPORT_DEPTH)][0]
        self.prevent_self_hinting = ui_settings.get(settingkey.PREVENT_SELF_HINTING)
        self.allow_proof_hinting = ui_settings.get(settingkey.ALLOW_PROOF_HINTING)
        self.keybladeAbilities = []
        if ui_settings.get(settingkey.SUPPORT_KEYBLADE_ABILITIES):
             self.keybladeAbilities.append(itemType.SUPPORT_ABILITY)
        if ui_settings.get(settingkey.ACTION_KEYBLADE_ABILITIES):
             self.keybladeAbilities.append(itemType.ACTION_ABILITY)
        self.keyblade_min_stat = ui_settings.get(settingkey.KEYBLADE_MIN_STAT)
        self.keyblade_max_stat = ui_settings.get(settingkey.KEYBLADE_MAX_STAT)
        self.setSoraExp(ui_settings.get(settingkey.SORA_EXP_MULTIPLIER))
        self.setValorExp(ui_settings.get(settingkey.VALOR_EXP_MULTIPLIER))
        self.setWisdomExp(ui_settings.get(settingkey.WISDOM_EXP_MULTIPLIER))
        self.setLimitExp(ui_settings.get(settingkey.LIMIT_EXP_MULTIPLIER))
        self.setMasterExp(ui_settings.get(settingkey.MASTER_EXP_MULTIPLIER))
        self.setFinalExp(ui_settings.get(settingkey.FINAL_EXP_MULTIPLIER))
        self.setSummonExp(ui_settings.get(settingkey.SUMMON_EXP_MULTIPLIER))

        self.enemy_options = {'remove_damage_cap': ui_settings.get(settingkey.REMOVE_DAMAGE_CAP)}
        for setting in seedSettings.boss_enemy_settings:
            value = ui_settings.get(setting.name)
            if value is not None:
                self.enemy_options[setting.name] = value


        self.random_seed = seed_name
        self.spoiler_log = spoiler_log
        self.ui_version = ui_version
        random.seed(self.random_seed + str(spoiler_log) + ui_version + str(ui_settings.settings_json()))
        self.seedHashIcons = generateHashIcons()

        self.statSanity = False

    def setLevelChecks(self,maxLevel):
        self.level_checks = maxLevel
        if self.level_checks==99:
            self.enabledLocations.append(locationType.Level)
            levels_to_exclude = self.excludeFrom99
        elif self.level_checks==50:
            self.enabledLocations.append(locationType.Level)
            levels_to_exclude = self.excludeFrom50
        elif self.level_checks==1:
            self.disabledLocations.append(locationType.Level)
            levels_to_exclude = range(1,100)
        else:
            raise RuntimeError(f"Incorrect level choice {maxLevel}")
        self.excludedLevels = [f"Level {i}" for i in range(1,100) if i in levels_to_exclude]


    def setSoraExp(self,rate):
        self.sora_exp_multiplier = rate
        self.sora_exp = [math.ceil(a/b) for a,b in zip(soraExp,[self.sora_exp_multiplier]*100)]
    
    def setValorExp(self, rate):
        self.valor_exp_multiplier = rate
        self.valor_exp = [math.ceil(a/b) for a,b in zip([0]+[formExp[1][i] for i in range(1,8)],[self.valor_exp_multiplier]*8)]
    
    def setWisdomExp(self,rate):
        self.wisdom_exp_multiplier = rate
        self.wisdom_exp = [math.ceil(a/b) for a,b in zip([0]+[formExp[2][i] for i in range(1,8)],[self.wisdom_exp_multiplier]*8)]

    def setLimitExp(self,rate):
        self.limit_exp_multiplier = rate
        self.limit_exp = [math.ceil(a/b) for a,b in zip([0]+[formExp[3][i] for i in range(1,8)],[self.limit_exp_multiplier]*8)]

    def setMasterExp(self,rate):
        self.master_exp_multiplier = rate
        self.master_exp = [math.ceil(a/b) for a,b in zip([0]+[formExp[4][i] for i in range(1,8)],[self.master_exp_multiplier]*8)]

    def setFinalExp(self,rate):
        self.final_exp_multiplier = rate
        self.final_exp = [math.ceil(a/b) for a,b in zip([0]+[formExp[5][i] for i in range(1,8)],[self.final_exp_multiplier]*8)]

    def setSummonExp(self,rate):
        self.summon_exp_multiplier = rate
        self.summon_exp = [math.ceil(a/b) for a,b in zip([0]+[formExp[0][i] for i in range(1,8)],[self.summon_exp_multiplier]*8)]
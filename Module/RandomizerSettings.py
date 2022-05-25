
from Class.exceptions import SettingsException
from List.ItemList import Items
from Module.modifier import SeedModifier
from List.experienceValues import duskExp, duskFormExp, middayFormExp, vanillaExp, middayExp, vanillaFormExp
from List.hashTextEntries import generateHashIcons
from List.configDict import expCurve, locationType, itemType, locationDepth
from itertools import chain
import math,random
from Class import modYml, seedSettings, settingkey
from Class.seedSettings import SeedSettings, Setting

class RandomizerSettings():
    excludeFrom50 = list(chain([1,3,5,6,8,11,13,16,18,19,21,22,24,26,27,29,31,33,35,37,38,40,42,43,45,47,49],range(51,100)))
    excludeFrom99 = [1,2,3,4,5,6,8,10,11,13,14,16,18,19,21,22,24,26,27,29,30,32,34,35,37,38,40,42,43,45,46,48,50,51,52,54,55,56,57,58,60,61,62,63,64,66,67,68,69,70,71,72,74,75,76,77,78,79,80,81,82,83,84,86,87,88,89,90,91,92,93,94,95,96,97,98]
    
    def __init__(self, seed_name: str, spoiler_log: bool, ui_version: str, ui_settings: SeedSettings, full_ui_settings):

        self.full_ui_settings = full_ui_settings
        self.ui_settings = ui_settings
        self.crit_mode = ui_settings.get(settingkey.CRITICAL_BONUS_REWARDS)

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
        self.level_one = False 
        if level_setting=="Level":
            self.setLevelChecks(1)
            self.level_one = ui_settings.get(settingkey.LEVEL_ONE)
        elif level_setting=="ExcludeFrom50":
            self.setLevelChecks(50)
        elif level_setting=="ExcludeFrom99":
            self.setLevelChecks(99)
        else:
            raise SettingsException("Invalid Level choice")

        self.split_levels = ui_settings.get(settingkey.SPLIT_LEVELS)
        self.startingItems = [int(value) for value in ui_settings.get(settingkey.STARTING_INVENTORY)] + SeedModifier.schmovement(ui_settings.get(settingkey.SCHMOVEMENT)) + SeedModifier.library(ui_settings.get(settingkey.LIBRARY_OF_ASSEMBLAGE)) + SeedModifier.world_unlocks(ui_settings.get(settingkey.STORY_UNLOCKS)) + ([Items.getTT1Jailbreak().Id] if ui_settings.get(settingkey.TT1_JAILBREAK) else [])
        self.itemPlacementDifficulty = ui_settings.get(settingkey.ITEM_PLACEMENT_DIFFICULTY)
        self.nightmare = ui_settings.get(settingkey.NIGHTMARE_LOGIC)
        self.regular_rando = ui_settings.get(settingkey.SOFTLOCK_CHECKING) in ["default","both"]
        self.reverse_rando = ui_settings.get(settingkey.SOFTLOCK_CHECKING) in ["reverse","both"]
        self.level_stat_pool = SeedModifier.glassCannon if ui_settings.get(settingkey.GLASS_CANNON) else SeedModifier.regularStats
        # self.betterJunk = ui_settings.get(settingkey.BETTER_JUNK)
        self.junk_pool = [
            int(item_id) for item_id in ui_settings.get(settingkey.JUNK_ITEMS)
        ]

        if len(self.junk_pool) == 0:
            raise SettingsException("Need at least one junk item in the pool")

        # self.no_ap = ui_settings.get(settingkey.START_NO_AP)
        self.sora_ap = ui_settings.get(settingkey.SORA_AP)
        self.donald_ap = ui_settings.get(settingkey.DONALD_AP)
        self.goofy_ap = ui_settings.get(settingkey.GOOFY_AP)

        ui_ability_pool = ui_settings.get(settingkey.ABILITY_POOL)
        if ui_ability_pool == "default":
            self.abilityListModifier = SeedModifier.defaultAbilityPool
        elif ui_ability_pool == "randomize":
            self.abilityListModifier = SeedModifier.randomAbilityPool
        elif ui_ability_pool == "randomize support":
            self.abilityListModifier = SeedModifier.randomSupportAbilityPool
        else:
            raise SettingsException("Invalid ability pool option")

        self.promiseCharm = ui_settings.get(settingkey.ENABLE_PROMISE_CHARM)
        self.tt1_jailbreak = ui_settings.get(settingkey.TT1_JAILBREAK)
        self.pureblood = ui_settings.get(settingkey.PUREBLOOD)
        self.hintsType = ui_settings.get(settingkey.HINT_SYSTEM)
        if self.hintsType in ["JSmartee","Points"]:
            self.reportDepth = [l for l in locationDepth if l==ui_settings.get(settingkey.REPORT_DEPTH)][0]
        else:
            self.reportDepth = locationDepth.Anywhere
        self.proofDepth = [l for l in locationDepth if l==ui_settings.get(settingkey.PROOF_DEPTH)][0]

        if ui_settings.get(settingkey.SOFTLOCK_CHECKING) == "both":
            if self.proofDepth in [locationDepth.FirstBoss,locationDepth.SecondBoss,locationDepth.FirstVisit]:
                raise SettingsException(f"Setting proof depth to {self.proofDepth} will contradict either regular or reverse rando. Please use another setting")
            if self.reportDepth in [locationDepth.FirstBoss,locationDepth.SecondBoss,locationDepth.FirstVisit]:
                raise SettingsException(f"Setting report depth to {self.reportDepth} will contradict either regular or reverse rando. Please use another setting")


        self.prevent_self_hinting = ui_settings.get(settingkey.PREVENT_SELF_HINTING)
        self.allow_proof_hinting = ui_settings.get(settingkey.ALLOW_PROOF_HINTING)
        self.allow_report_hinting = ui_settings.get(settingkey.ALLOW_REPORT_HINTING)
        self.keyblade_support_abilities = [
            int(ability_id) for ability_id in ui_settings.get(settingkey.KEYBLADE_SUPPORT_ABILITIES)
        ]
        self.keyblade_action_abilities = [
            int(ability_id) for ability_id in ui_settings.get(settingkey.KEYBLADE_ACTION_ABILITIES)
        ]
        self.keyblade_min_stat = ui_settings.get(settingkey.KEYBLADE_MIN_STAT)
        self.keyblade_max_stat = ui_settings.get(settingkey.KEYBLADE_MAX_STAT)
        self.setSoraExp(ui_settings.get(settingkey.SORA_EXP_MULTIPLIER),ui_settings.get(settingkey.SORA_EXP_CURVE))
        self.setValorExp(ui_settings.get(settingkey.VALOR_EXP_MULTIPLIER),ui_settings.get(settingkey.VALOR_EXP_CURVE))
        self.setWisdomExp(ui_settings.get(settingkey.WISDOM_EXP_MULTIPLIER),ui_settings.get(settingkey.WISDOM_EXP_CURVE))
        self.setLimitExp(ui_settings.get(settingkey.LIMIT_EXP_MULTIPLIER),ui_settings.get(settingkey.LIMIT_EXP_CURVE))
        self.setMasterExp(ui_settings.get(settingkey.MASTER_EXP_MULTIPLIER),ui_settings.get(settingkey.MASTER_EXP_CURVE))
        self.setFinalExp(ui_settings.get(settingkey.FINAL_EXP_MULTIPLIER),ui_settings.get(settingkey.FINAL_EXP_CURVE))
        self.setSummonExp(ui_settings.get(settingkey.SUMMON_EXP_MULTIPLIER),ui_settings.get(settingkey.SUMMON_EXP_CURVE))

        self.as_data_split = ui_settings.get(settingkey.AS_DATA_SPLIT)

        self.retries = ([modYml.modYml.retryDataXemnas] if ui_settings.get(settingkey.RETRY_DFX) else []) + ([modYml.modYml.retryDarkThorn] if ui_settings.get(settingkey.RETRY_DARK_THORN) else [])

        self.skip_carpet_escape = ui_settings.get(settingkey.SKIP_CARPET_ESCAPE)

        if self.reverse_rando and not self.as_data_split:
            raise SettingsException("Can't run reverse rando without the as/data split code")

        self.enemy_options = {'remove_damage_cap': ui_settings.get(settingkey.REMOVE_DAMAGE_CAP),
                              'cups_give_xp': ui_settings.get(settingkey.CUPS_GIVE_XP)}
        for setting in seedSettings.boss_settings + seedSettings.enemy_settings:
            value = ui_settings.get(setting.name)
            if value is not None:
                self.enemy_options[setting.name] = value

        self.random_seed = seed_name
        self.spoiler_log = spoiler_log
        self.ui_version = ui_version
        self.create_full_seed_string()
        self.seedHashIcons = generateHashIcons()

        self.statSanity = ui_settings.get(settingkey.STATSANITY)
        self.yeetTheBear = ui_settings.get(settingkey.YEET_THE_BEAR)
        self.roxas_abilities_enabled = ui_settings.get(settingkey.ROXAS_ABILITIES_ENABLED)
        self.remove_maps = ui_settings.get(settingkey.REMOVE_MAPS)
        self.remove_recipes = ui_settings.get(settingkey.REMOVE_RECIPES)
        self.remove_popups = ui_settings.get(settingkey.REMOVE_POPUPS)

        self.point_hint_values = {"proof":ui_settings.get(settingkey.POINTS_PROOF),
                                    "form":ui_settings.get(settingkey.POINTS_FORM),
                                    "magic":ui_settings.get(settingkey.POINTS_MAGIC), 
                                    "summon":ui_settings.get(settingkey.POINTS_SUMMON), 
                                    "ability":ui_settings.get(settingkey.POINTS_ABILITY), 
                                    "page":ui_settings.get(settingkey.POINTS_PAGE), 
                                    "report":ui_settings.get(settingkey.POINTS_REPORT),
                                    "visit":ui_settings.get(settingkey.POINTS_VISIT),
                                    "bonus":ui_settings.get(settingkey.POINTS_BONUS), 
                                    "complete":ui_settings.get(settingkey.POINTS_COMPLETE), 
                                    "formlv":ui_settings.get(settingkey.POINTS_FORMLV)}

        self.tracker_includes = []
        if self.promiseCharm:
            self.tracker_includes.append("PromiseCharm")
        self.tracker_includes.append(level_setting)
        if self.roxas_abilities_enabled:
            self.tracker_includes.append("better_stt")
        if ui_settings.get(settingkey.STORY_UNLOCKS):
            self.tracker_includes.append("visit_locking")
        if ui_settings.get(settingkey.LIBRARY_OF_ASSEMBLAGE):
            self.tracker_includes.append("library")

        # making tracker includes use all worlds and 
        for l in locationType:
            if l.value in self.enabledLocations:
                if l.value!="Level": # don't duplicate the level info
                    self.tracker_includes.append(l.value)

        self.validateSettings()

    def create_full_seed_string(self):
        seed_string_from_all_inputs = self.random_seed + str(self.spoiler_log) + self.ui_version + str(self.ui_settings.settings_string())
        self.full_rando_seed = seed_string_from_all_inputs
        random.seed(seed_string_from_all_inputs)

    def validateSettings(self):
        if self.reportDepth == self.proofDepth and self.reportDepth in [locationDepth.DataFight,locationDepth.FirstBoss,locationDepth.SecondBoss]:
            raise SettingsException("Proof depth and report depth can't be the same")
        
        if locationType.TTR in self.enabledLocations and not self.statSanity:
            raise SettingsException("Enabling Transport to Remembrance when not in Statsanity is incorrect. Enable Statsanity or disable TTR.")

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
            raise SettingsException(f"Incorrect level choice {maxLevel}")
        self.excludedLevels = levels_to_exclude


    def setSoraExp(self,rate,curve):
        # with open("exp_values.csv","w") as output_file:
        #     vanilla = vanillaExp()
        #     middayExp99 = middayExp(False)
        #     duskExp99 = duskExp(False)
        #     middayExp50 = middayExp(True)
        #     duskExp50 = duskExp(True)
        #     for i in range(100):
        #         output_file.write(f"{vanilla[i]},{middayExp99[i]},{duskExp99[i]},{middayExp50[i]},{duskExp50[i]}\n")

        adjust_exp_curves = self.level_checks == 50
        if curve == expCurve.DAWN.name:
            exp_list = vanillaExp()
        elif curve == expCurve.MIDDAY.name:
            exp_list = middayExp(adjust_exp_curves)
        elif curve == expCurve.DUSK.name:
            exp_list = duskExp(adjust_exp_curves)
        else:
            raise SettingsException(f"Incorrect exp curve value {curve}")

        self.sora_exp_multiplier = rate
        self.sora_exp = [math.ceil(a/b) for a,b in zip(exp_list,[self.sora_exp_multiplier]*100)]
    
    def setValorExp(self, rate, curve):
        if curve == expCurve.DAWN.name:
            exp_list = vanillaFormExp()
        elif curve == expCurve.MIDDAY.name:
            exp_list = middayFormExp()
        elif curve == expCurve.DUSK.name:
            exp_list = duskFormExp()
        else:
            raise SettingsException(f"Incorrect exp curve value {curve}")
        self.valor_exp_multiplier = rate
        self.valor_exp = [math.ceil(a/b) for a,b in zip([exp_list[1][i] for i in range(1,8)],[self.valor_exp_multiplier]*7)]
    
    def setWisdomExp(self,rate,curve):
        if curve == expCurve.DAWN.name:
            exp_list = vanillaFormExp()
        elif curve == expCurve.MIDDAY.name:
            exp_list = middayFormExp()
        elif curve == expCurve.DUSK.name:
            exp_list = duskFormExp()
        else:
            raise SettingsException(f"Incorrect exp curve value {curve}")
        self.wisdom_exp_multiplier = rate
        self.wisdom_exp = [math.ceil(a/b) for a,b in zip([exp_list[2][i] for i in range(1,8)],[self.wisdom_exp_multiplier]*7)]

    def setLimitExp(self,rate,curve):
        if curve == expCurve.DAWN.name:
            exp_list = vanillaFormExp()
        elif curve == expCurve.MIDDAY.name:
            exp_list = middayFormExp()
        elif curve == expCurve.DUSK.name:
            exp_list = duskFormExp()
        else:
            raise SettingsException(f"Incorrect exp curve value {curve}")
        self.limit_exp_multiplier = rate
        self.limit_exp = [math.ceil(a/b) for a,b in zip([exp_list[3][i] for i in range(1,8)],[self.limit_exp_multiplier]*7)]

    def setMasterExp(self,rate,curve):
        if curve == expCurve.DAWN.name:
            exp_list = vanillaFormExp()
        elif curve == expCurve.MIDDAY.name:
            exp_list = middayFormExp()
        elif curve == expCurve.DUSK.name:
            exp_list = duskFormExp()
        else:
            raise SettingsException(f"Incorrect exp curve value {curve}")
        self.master_exp_multiplier = rate
        self.master_exp = [math.ceil(a/b) for a,b in zip([exp_list[4][i] for i in range(1,8)],[self.master_exp_multiplier]*7)]

    def setFinalExp(self,rate,curve):
        if curve == expCurve.DAWN.name:
            exp_list = vanillaFormExp()
        elif curve == expCurve.MIDDAY.name:
            exp_list = middayFormExp()
        elif curve == expCurve.DUSK.name:
            exp_list = duskFormExp()
        else:
            raise SettingsException(f"Incorrect exp curve value {curve}")
        self.final_exp_multiplier = rate
        self.final_exp = [math.ceil(a/b) for a,b in zip([exp_list[5][i] for i in range(1,8)],[self.final_exp_multiplier]*7)]

    def setSummonExp(self,rate,curve):
        if curve == expCurve.DAWN.name:
            exp_list = vanillaFormExp()
        elif curve == expCurve.MIDDAY.name:
            exp_list = middayFormExp()
        elif curve == expCurve.DUSK.name:
            exp_list = duskFormExp()
        else:
            raise SettingsException(f"Incorrect exp curve value {curve}")
        self.summon_exp_multiplier = rate
        self.summon_exp = [math.ceil(a/b) for a,b in zip([exp_list[0][i] for i in range(1,8)],[self.summon_exp_multiplier]*7)]

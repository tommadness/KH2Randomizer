
import math
import random
from itertools import chain

from Class import seedSettings, settingkey
from Class.exceptions import SettingsException
from Class.seedSettings import SeedSettings, makeKHBRSettings
from List.ItemList import Items
from List.configDict import expCurve, locationType, itemType, locationDepth
from List.experienceValues import duskExp, duskFormExp, middayFormExp, vanillaExp, middayExp, vanillaFormExp
from List.hashTextEntries import generateHashIcons
from Module.modifier import SeedModifier
from Module.progressionPoints import ProgressionPoints


class RandomizerSettings():
    excludeFrom50 = list(chain([1,3,5,6,8,11,13,16,18,19,21,22,24,26,27,29,31,33,35,37,38,40,42,43,45,47,49],range(51,100)))
    excludeFrom99 = [1,2,3,4,5,6,8,10,11,13,14,16,18,19,21,22,24,26,27,29,30,32,34,35,37,38,40,42,43,45,46,48,50,51,52,54,55,56,57,58,60,61,62,63,64,66,67,68,69,70,71,72,74,75,76,77,78,79,80,81,82,83,84,86,87,88,89,90,91,92,93,94,95,96,97,98]
    
    def __init__(
            self,
            seed_name: str,
            spoiler_log: bool,
            ui_version: str,
            ui_settings: SeedSettings,
            seed_string: str
    ):
        self.ui_settings = ui_settings
        self.seed_string = seed_string
        self.crit_mode = ui_settings.get(settingkey.CRITICAL_BONUS_REWARDS)
        self.item_accessibility = ui_settings.get(settingkey.ACCESSIBILITY)

        include_list = []
        vanilla_list = []
        include_list_keys = [
            (settingkey.CRITICAL_BONUS_REWARDS, 'Critical Bonuses'),
            (settingkey.GARDEN_OF_ASSEMBLAGE_REWARDS, 'Garden of Assemblage'),
        ]
        for key in include_list_keys:
            if ui_settings.get(key[0]):
                include_list.append(key[1])
        worlds_with_rewards =  ui_settings.get(settingkey.WORLDS_WITH_REWARDS)
        vanilla_worlds = []
        if isinstance(worlds_with_rewards[0],list):
            vanilla_worlds = worlds_with_rewards[1]
            worlds_with_rewards = worlds_with_rewards[0]
        for location in worlds_with_rewards:
            include_list.append(locationType[location].value)
        for location in vanilla_worlds:
            vanilla_list.append(locationType[location].value)
        for location in ui_settings.get(settingkey.SUPERBOSSES_WITH_REWARDS):
            include_list.append(locationType[location].value)
        for location in ui_settings.get(settingkey.MISC_LOCATIONS_WITH_REWARDS):
            include_list.append(locationType[location].value)
        self.enabledLocations = [l for l in locationType if l in include_list]
        self.vanillaLocations = [l for l in locationType if l in vanilla_list]
        self.disabledLocations = [l for l in locationType if l not in include_list and l not in [locationType.Mush13,locationType.WeaponSlot]]
       
        level_setting = ui_settings.get(settingkey.SORA_LEVELS)
        self.level_one = False 
        if level_setting=="Level":
            self.setLevelChecks(1)
            if locationType.Level in self.enabledLocations:
                raise SettingsException("Please choose between Junk or Vanilla Checks when doing Level 1")
            elif locationType.Level in self.vanillaLocations:
                self.level_one = True
        elif level_setting=="ExcludeFrom50":
            self.setLevelChecks(50)
        elif level_setting=="ExcludeFrom99":
            self.setLevelChecks(99)
        else:
            raise SettingsException("Invalid Level choice")

        self.split_levels = ui_settings.get(settingkey.SPLIT_LEVELS)
        self.battle_level_rando = ui_settings.get(settingkey.BATTLE_LEVEL_RANDO)
        self.battle_level_offset = ui_settings.get(settingkey.BATTLE_LEVEL_OFFSET)
        self.battle_level_range = ui_settings.get(settingkey.BATTLE_LEVEL_RANGE)

        self.starting_growth = ui_settings.get(settingkey.STARTING_MOVEMENT)
        self.num_random_growths = 0
        if self.starting_growth == "Random":
            self.num_random_growths = 5
        elif self.starting_growth == "3Random":
            self.num_random_growths = 3
        self.chosen_random_growths = []

        self.startingItems = [int(value) for value in ui_settings.get(settingkey.STARTING_INVENTORY)] + [int(value) for value in ui_settings.get(settingkey.STARTING_STORY_UNLOCKS)] + [starting_level for starting_level in SeedModifier.schmovement(ui_settings.get(settingkey.STARTING_MOVEMENT))] + SeedModifier.library(ui_settings.get(settingkey.STARTING_REPORTS)) + [Items.getTT1Jailbreak().Id]
        self.itemPlacementDifficulty = ui_settings.get(settingkey.ITEM_PLACEMENT_DIFFICULTY)
        self.nightmare = ui_settings.get(settingkey.NIGHTMARE_LOGIC)
        self.story_unlock_rarity = ui_settings.get(settingkey.STORY_UNLOCK_CATEGORY)
        self.regular_rando = ui_settings.get(settingkey.SOFTLOCK_CHECKING) in ["default","both"]
        self.reverse_rando = ui_settings.get(settingkey.SOFTLOCK_CHECKING) in ["reverse","both"]
        self.level_stat_pool = SeedModifier.glassCannon if ui_settings.get(settingkey.GLASS_CANNON) else SeedModifier.regularStats
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
        self.abilityListModifierString = ui_ability_pool
        if ui_ability_pool == "default":
            self.abilityListModifier = SeedModifier.defaultAbilityPool
        elif ui_ability_pool == "randomize":
            self.abilityListModifier = SeedModifier.randomAbilityPool
        elif ui_ability_pool == "randomize support":
            self.abilityListModifier = SeedModifier.randomSupportAbilityPool
        elif ui_ability_pool == "randomize stackable":
            self.abilityListModifier = SeedModifier.randomStackableAbilityPool
        else:
            raise SettingsException("Invalid ability pool option")

        self.promiseCharm = ui_settings.get(settingkey.ENABLE_PROMISE_CHARM)
        self.auto_equip_abilities = ui_settings.get(settingkey.AUTO_EQUIP_START_ABILITIES)
        self.tt1_jailbreak = True # ui_settings.get(settingkey.TT1_JAILBREAK)
        self.pureblood = True # ui_settings.get(settingkey.PUREBLOOD)
        self.antiform = ui_settings.get(settingkey.ANTIFORM)
        self.fifty_ap = ui_settings.get(settingkey.FIFTY_AP_BOOSTS)
        self.hintsType = ui_settings.get(settingkey.HINT_SYSTEM)
        # if self.hintsType in ["JSmartee","Points","Path"]:
        self.reportDepth = [l for l in locationDepth if l==ui_settings.get(settingkey.REPORT_DEPTH)][0]
        # else:
        #     self.reportDepth = locationDepth.Anywhere
        self.proofDepth = [l for l in locationDepth if l==ui_settings.get(settingkey.PROOF_DEPTH)][0]
        self.storyDepth = [l for l in locationDepth if l==ui_settings.get(settingkey.STORY_UNLOCK_DEPTH)][0]

        if ui_settings.get(settingkey.SOFTLOCK_CHECKING) == "both":
            if self.proofDepth in [locationDepth.FirstBoss,locationDepth.SecondBoss,locationDepth.FirstVisit]:
                raise SettingsException(f"Setting proof depth to {self.proofDepth} will contradict either regular or reverse rando. Please use another setting")
            if self.reportDepth in [locationDepth.FirstBoss,locationDepth.SecondBoss,locationDepth.FirstVisit]:
                raise SettingsException(f"Setting report depth to {self.reportDepth} will contradict either regular or reverse rando. Please use another setting")
            if self.storyDepth in [locationDepth.FirstBoss,locationDepth.SecondBoss,locationDepth.FirstVisit]:
                raise SettingsException(f"Setting visit unlock depth to {self.storyDepth} will contradict either regular or reverse rando. Please use another setting")


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

        self.chests_match_item = ui_settings.get(settingkey.CHESTS_MATCH_ITEM)

        self.skip_carpet_escape = ui_settings.get(settingkey.SKIP_CARPET_ESCAPE)

        if self.reverse_rando and not self.as_data_split:
            raise SettingsException("Can't run reverse rando without the as/data split code")

        self.enemy_options = makeKHBRSettings(ui_settings)

        self.random_seed = seed_name
        self.spoiler_log = spoiler_log
        self.ui_version = ui_version
        self.create_full_seed_string()
        self.seedHashIcons = generateHashIcons()

        self.statSanity = ui_settings.get(settingkey.STATSANITY)
        self.yeetTheBear = ui_settings.get(settingkey.YEET_THE_BEAR)
        self.chainLogic = ui_settings.get(settingkey.CHAIN_LOGIC)
        self.chainLogicIncludeTerra = ui_settings.get(settingkey.CHAIN_LOGIC_TERRA)
        self.chainLogicTerraLate = ui_settings.get(settingkey.CHAIN_LOGIC_MIN_TERRA)
        self.chainLogicMinLength = ui_settings.get(settingkey.CHAIN_LOGIC_LENGTH)

        if self.proofDepth in [locationDepth.FirstVisit,locationDepth.FirstBoss] and self.chainLogic:
            raise SettingsException("Chain logic is not compatible with first visit proofs")
        if self.storyDepth not in [locationDepth.Anywhere, locationDepth.SecondVisit] and self.chainLogic:
            raise SettingsException("Chain logic is only compatible with visit unlock depth non-data and anywhere")
        if self.chainLogic and self.regular_rando and self.reverse_rando:
            raise SettingsException("Can't do chain logic with both regular and reverse rando")


        self.roxas_abilities_enabled = ui_settings.get(settingkey.ROXAS_ABILITIES_ENABLED)
        self.disable_final_form = ui_settings.get(settingkey.DISABLE_FINAL_FORM)
        self.block_cor_skip = ui_settings.get(settingkey.BLOCK_COR_SKIP)
        self.block_shan_yu_skip = ui_settings.get(settingkey.BLOCK_SHAN_YU_SKIP)
        self.pr_map_skip = ui_settings.get(settingkey.PR_MAP_SKIP)
        self.atlantica_skip = ui_settings.get(settingkey.ATLANTICA_TUTORIAL_SKIP)
        self.wardrobe_skip = ui_settings.get(settingkey.REMOVE_WARDROBE_ANIMATION)
        self.include_maps = ui_settings.get(settingkey.MAPS_IN_ITEM_POOL)
        self.include_recipes = ui_settings.get(settingkey.RECIPES_IN_ITEM_POOL)
        self.include_accessories = ui_settings.get(settingkey.ACCESSORIES_IN_ITEM_POOL)
        self.include_armor = ui_settings.get(settingkey.ARMOR_IN_ITEM_POOL)
        self.remove_popups = ui_settings.get(settingkey.REMOVE_POPUPS)

        self.global_jackpot = ui_settings.get(settingkey.GLOBAL_JACKPOT)
        self.global_lucky = ui_settings.get(settingkey.GLOBAL_LUCKY)
        self.rich_enemies = ui_settings.get(settingkey.RICH_ENEMIES)
        self.unlimited_mp = ui_settings.get(settingkey.UNLIMITED_MP)
        self.fast_urns = ui_settings.get(settingkey.FAST_URNS)
        
        self.shop_elixirs = ui_settings.get(settingkey.SHOP_ELIXIRS)
        self.shop_recoveries = ui_settings.get(settingkey.SHOP_RECOVERIES)
        self.shop_boosts = ui_settings.get(settingkey.SHOP_BOOSTS)
        self.shop_keyblades = ui_settings.get(settingkey.SHOP_KEYBLADES)
        self.shop_unlocks = ui_settings.get(settingkey.SHOP_UNLOCKS)
        self.shop_reports = ui_settings.get(settingkey.SHOP_REPORTS)

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
                                    "formlv":ui_settings.get(settingkey.POINTS_FORMLV),
                                    "other":ui_settings.get(settingkey.POINTS_AUX),
                                    "boss_as":ui_settings.get(settingkey.POINTS_BOSS_AS),
                                    "boss_datas":ui_settings.get(settingkey.POINTS_BOSS_DATA),
                                    "boss_sephi":ui_settings.get(settingkey.POINTS_BOSS_SEPHIROTH),
                                    "boss_terra":ui_settings.get(settingkey.POINTS_BOSS_TERRA),
                                    "boss_final":ui_settings.get(settingkey.POINTS_BOSS_FINAL),
                                    "boss_other":ui_settings.get(settingkey.POINTS_BOSS_NORMAL),
                                    "deaths":ui_settings.get(settingkey.POINTS_DEATH),
                                    "collection_magic":ui_settings.get(settingkey.POINTS_MAGIC_COLLECT),
                                    "collection_page":ui_settings.get(settingkey.POINTS_PAGE_COLLECT),
                                    "collection_pouches":ui_settings.get(settingkey.POINTS_POUCHES_COLLECT),
                                    "collection_proof":ui_settings.get(settingkey.POINTS_PROOF_COLLECT),
                                    "collection_form":ui_settings.get(settingkey.POINTS_FORM_COLLECT),
                                    "collection_summon":ui_settings.get(settingkey.POINTS_SUMMON_COLLECT),
                                    "collection_ability":ui_settings.get(settingkey.POINTS_ABILITY_COLLECT),
                                    "collection_report":ui_settings.get(settingkey.POINTS_REPORT_COLLECT),
                                    "collection_visit":ui_settings.get(settingkey.POINTS_VISIT_COLLECT),
                                    }

        self.progression_hints = ui_settings.get(settingkey.PROGRESSION_HINTS)
        self.progression_world_complete_bonus = ui_settings.get(settingkey.PROGRESSION_HINTS_COMPLETE_BONUS)
        self.progression_report_bonus = ui_settings.get(settingkey.PROGRESSION_HINTS_REPORT_BONUS)
        self.progression_reveal_all = ui_settings.get(settingkey.PROGRESSION_HINTS_REVEAL_END)

        self.shop_hintable = self.shop_unlocks or self.shop_reports or locationType.Puzzle in include_list or locationType.SYNTH in include_list
        prog_points = ProgressionPoints()
        prog_points.set_uncompressed(ui_settings.get(settingkey.PROGRESSION_POINT_SELECT))
        self.progression_hint_settings = prog_points.get_points_json()
        num_worlds = len(vanilla_worlds) + len(worlds_with_rewards) + (1 if self.shop_hintable else 0)
        self.progression_hint_settings["HintCosts"] = prog_points.get_hint_thresholds(num_worlds)
        self.progression_hint_settings["WorldCompleteBonus"] = [self.progression_world_complete_bonus]
        self.progression_hint_settings["ReportBonus"] = [self.progression_report_bonus]
        self.progression_hint_settings["FinalXemnasReveal"] = [1 if self.progression_reveal_all else 0]


        self.revealComplete = ui_settings.get(settingkey.REVEAL_COMPLETE)
        self.revealMode = ui_settings.get(settingkey.REPORTS_REVEAL)

        self.hintable_check_types = [
            item_type for item_type in ui_settings.get(settingkey.HINTABLE_CHECKS)
        ]
        self.spoiler_hint_values = [
            item_type for item_type in ui_settings.get(settingkey.SPOILER_REVEAL_TYPES)
        ]
        if self.revealComplete:
            self.spoiler_hint_values.append("complete")
        if self.revealMode != 'Disabled':
            self.spoiler_hint_values.append(self.revealMode)
            if self.revealMode == "bossreports" and ui_settings.get("boss")=="Disabled":
                raise SettingsException("Can't use report hint bosses option without boss randomization.")
        if self.hintsType=="Spoiler" and self.revealMode == 'Disabled' and self.progression_hints:
            raise SettingsException("Can't use progression hints with full spoiler hints")

        self.hiscore_mode = ui_settings.get(settingkey.SCORE_MODE)

        self.tracker_includes = []
        if self.progression_hints:
            self.tracker_includes.append("ProgressionHints")
        if self.level_one:
            self.tracker_includes.append("Level1Mode")
        self.tracker_includes.append(level_setting)
        if self.roxas_abilities_enabled:
            self.tracker_includes.append("better_stt")
        if self.as_data_split:
            self.tracker_includes.append("Data Split")
        if len(ui_settings.get(settingkey.STARTING_STORY_UNLOCKS)) < 11:
            self.tracker_includes.append("visit_locking")
        if ui_settings.get(settingkey.STARTING_REPORTS)==13:
            self.tracker_includes.append("library")
        if self.hiscore_mode:
            self.tracker_includes.append("ScoreMode")

        hintable_checks_list = ui_settings.get(settingkey.HINTABLE_CHECKS)
        
        if self.hintsType in ["JSmartee","Path"] and "proof" not in hintable_checks_list:
            raise SettingsException("Jsmartee and Path hints really need proofs hintable.")
        self.important_checks = []

        if "magic" in hintable_checks_list:
            self.important_checks+=[itemType.FIRE, itemType.BLIZZARD, itemType.THUNDER, 
                        itemType.CURE, itemType.REFLECT, itemType.MAGNET]
        if "proof" in hintable_checks_list:
            self.important_checks+=[itemType.PROOF,itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE,itemType.PROMISE_CHARM]
        if "form" in hintable_checks_list:
            self.important_checks+=[itemType.FORM,"Anti-Form"]
        if "page" in hintable_checks_list:
            self.important_checks+=[itemType.TORN_PAGE]
        if "report" in hintable_checks_list:
            self.important_checks+=[itemType.REPORT]
        if "summon" in hintable_checks_list:
            self.important_checks+=[itemType.SUMMON]
        if "visit" in hintable_checks_list:
            self.important_checks+=[itemType.STORYUNLOCK]
        if "ability" in hintable_checks_list:
            self.important_checks+=["Second Chance", "Once More"]
        if "other" in hintable_checks_list:
            self.important_checks+=[itemType.TROPHY, itemType.MANUFACTORYUNLOCK, itemType.OCSTONE,itemType.MUNNY_POUCH]

        for check_type in ["magic","proof","form","page","summon","visit","ability","other","report"]:
            if check_type not in hintable_checks_list:
                self.point_hint_values[check_type] = 0

        # making tracker includes use all worlds and 
        for l in locationType:
            if l.value in self.enabledLocations:
                if l.value!="Level": # don't duplicate the level info
                    self.tracker_includes.append(l.value)
            if l.value in self.vanillaLocations:
                if l.value!="Level": # don't duplicate the level info
                    self.tracker_includes.append(l.value)

        # putting this in the settings object to allow us to turn it off as a safety valve
        self.dummy_forms = True

        self.validateSettings()

    def create_full_seed_string(self):
        seed_string_from_all_inputs = self.random_seed + str(self.spoiler_log) + self.ui_version + str(self.ui_settings.settings_string())
        self.full_rando_seed = seed_string_from_all_inputs
        random.seed(seed_string_from_all_inputs)

    def validateSettings(self):
        if self.reportDepth == self.proofDepth and self.reportDepth in [locationDepth.DataFight,locationDepth.FirstBoss,locationDepth.SecondBoss]:
            raise SettingsException("Proof depth and report depth can't be set to the same boss category")
        if self.storyDepth == self.proofDepth and self.proofDepth in [locationDepth.DataFight,locationDepth.FirstBoss,locationDepth.SecondBoss]:
            raise SettingsException("Proof depth and visit unlock depth can't be set to the same boss category")
        if self.reportDepth == self.storyDepth and self.reportDepth in [locationDepth.DataFight,locationDepth.FirstBoss,locationDepth.SecondBoss]:
            raise SettingsException("Visit unlock depth and report depth can't be set to the same boss category")
        
        if locationType.TTR in self.enabledLocations and not self.statSanity:
            raise SettingsException("Enabling Transport to Remembrance when not in Statsanity is incorrect. Enable Statsanity or disable TTR.")

        if self.chainLogic and len(self.vanillaLocations)>0:
            raise SettingsException("Currently can't do chain logic and vanilla worlds. Sorry about that. ")
        if self.abilityListModifierString!="default" and len(self.vanillaLocations)>0:
            pass
            # raise SettingsException("Currently can't do randomized ability pools and vanilla worlds. Sorry about that. ")

    def setLevelChecks(self,maxLevel):
        self.level_checks = maxLevel
        if self.level_checks==99:
            levels_to_exclude = self.excludeFrom99
        elif self.level_checks==50:
            levels_to_exclude = self.excludeFrom50
        elif self.level_checks==1:
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

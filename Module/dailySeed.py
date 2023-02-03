import random
from collections import namedtuple

from Class import settingkey
from Class.itemClass import itemRarity
from Class.seedSettings import SeedSettings
from List.ItemList import Items
from List.configDict import BattleLevelOption, expCurve, locationDepth, locationType

DailyModifier = namedtuple('DailyModifier', ['local_modifier', 'initMod', 'name', 'description', 'categories'])

def levelItUpLocal(seed_settings: SeedSettings):
    seed_settings.set(settingkey.SORA_LEVELS, 'ExcludeFrom99')
    seed_settings.set(settingkey.SORA_EXP_MULTIPLIER, 10.0)

def vanillaGrowth(seed_settings: SeedSettings):
    seed_settings.set(settingkey.VALOR_EXP_MULTIPLIER, 1.0)
    seed_settings.set(settingkey.WISDOM_EXP_MULTIPLIER, 1.0)
    seed_settings.set(settingkey.LIMIT_EXP_MULTIPLIER, 1.0)
    seed_settings.set(settingkey.MASTER_EXP_MULTIPLIER, 1.0)
    seed_settings.set(settingkey.FINAL_EXP_MULTIPLIER, 1.0)
    seed_settings.set(settingkey.VALOR_EXP_CURVE, expCurve.DAWN.name)
    seed_settings.set(settingkey.WISDOM_EXP_CURVE, expCurve.DAWN.name)
    seed_settings.set(settingkey.LIMIT_EXP_CURVE, expCurve.DAWN.name)
    seed_settings.set(settingkey.MASTER_EXP_CURVE, expCurve.DAWN.name)
    seed_settings.set(settingkey.FINAL_EXP_CURVE, expCurve.DAWN.name)

def addShops(seed_settings: SeedSettings):
    seed_settings.set(settingkey.SHOP_ELIXIRS,True)
    seed_settings.set(settingkey.SHOP_BOOSTS,True)
    seed_settings.set(settingkey.SHOP_RECOVERIES,True)

def shuffleBattleLevel(seed_settings: SeedSettings):
    seed_settings.set(settingkey.BATTLE_LEVEL_RANDO,BattleLevelOption.SHUFFLE.name)

def chaosBattleLevel(seed_settings: SeedSettings):
    seed_settings.set(settingkey.BATTLE_LEVEL_RANDO,BattleLevelOption.RANDOM_WITHIN_RANGE.name)
    seed_settings.set(settingkey.BATTLE_LEVEL_RANGE,50)

def fixedBattleLevel(seed_settings: SeedSettings):
    seed_settings.set(settingkey.BATTLE_LEVEL_RANDO,BattleLevelOption.SCALE_TO_50.name)

def cupsOn(seed_settings: SeedSettings):
    seed_settings.set(settingkey.CUPS_GIVE_XP,True)
    seed_settings.set(settingkey.MISC_LOCATIONS_WITH_REWARDS,seed_settings.get(settingkey.MISC_LOCATIONS_WITH_REWARDS)+[locationType.OCCups.name])
    seed_settings.set(settingkey.STARTING_INVENTORY,seed_settings.get(settingkey.STARTING_INVENTORY)+[537])

def corOn(seed_settings: SeedSettings):
    seed_settings.set(settingkey.MISC_LOCATIONS_WITH_REWARDS,seed_settings.get(settingkey.MISC_LOCATIONS_WITH_REWARDS)+[locationType.CoR.name])

def lockedVisitsHard(seed_settings: SeedSettings):
    seed_settings.set(settingkey.STARTING_STORY_UNLOCKS,[])
    seed_settings.set(settingkey.STORY_UNLOCK_CATEGORY,itemRarity.MYTHIC)

def blockSkips(seed_settings: SeedSettings):
    seed_settings.set(settingkey.BLOCK_COR_SKIP,True)
    seed_settings.set(settingkey.BLOCK_SHAN_YU_SKIP,True)


def turnOffWorldsLocal(worlds: list):
    def _turnOffLocal(settings: SeedSettings):
        worlds_with_rewards = settings.get(settingkey.WORLDS_WITH_REWARDS)
        for world in worlds:
            if world.name in worlds_with_rewards[0]:
                worlds_with_rewards[0].remove(world.name)
    return _turnOffLocal

def enableBossEnemy(settings: SeedSettings):
    settings.set("boss","One to One")
    settings.set("enemy","One to One")

def modifyShutOut(daily: DailyModifier):
    X = 3
    choices = [
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
            locationType.TWTNW
        ]
    random.shuffle(choices)
    shut_out_worlds = choices[:X]
    shut_out_world_names = [l.name for l in shut_out_worlds]
    daily = daily._replace(description = daily.description.format(', '.join(shut_out_world_names)),
                   local_modifier = daily.local_modifier(shut_out_worlds))
    return daily

dailyModifiers = [
    DailyModifier(name="Level Up!",
                initMod=None,
                description="Level checks up to 99 but Sora XP multiplier set to 10x",
                categories={"xp"},
                local_modifier=levelItUpLocal
                ),
    DailyModifier(name="Shut Out of Worlds",
                description="The following worlds have no unique checks and are filled with junk: {}",
                initMod=modifyShutOut,
                categories={'worlds'},
                local_modifier=lambda worlds: turnOffWorldsLocal(worlds)
    ),
    DailyModifier(name="Path Hints",
                initMod=None,
                description="Path Hints will guide you to the proofs",
                categories={'hints'},
                local_modifier=lambda settings: settings.set(settingkey.HINT_SYSTEM,"Path")
                ),
    DailyModifier(name="Spoiler Hints",
                initMod=None,
                description="Spoiler Hints will guide you to the proofs",
                categories={'hints'},
                local_modifier=lambda settings: settings.set(settingkey.HINT_SYSTEM,"Spoiler")
                ),
    DailyModifier(name="Locked Second Visits",
                initMod=None,
                description="Visit unlocks are dispersed in the seed, requiring you to find them to get to second visits",
                categories={'progression'},
                local_modifier=lambda settings: settings.set(settingkey.STARTING_STORY_UNLOCKS,[])
                ),
    DailyModifier(name="Glass Cannon",
                initMod=None,
                description="Level up stats will not include Defense Ups, all stats are Strength, Magic, and Max AP",
                categories={'stats'},
                local_modifier=lambda settings: settings.set(settingkey.GLASS_CANNON,True)
                ),
    DailyModifier(name="Moving Quick",
                initMod=None,
                description="All Growth Abilities start at level 3",
                categories={'qol'},
                local_modifier=lambda settings: settings.set(settingkey.STARTING_MOVEMENT,"Level_3")
                ),
    DailyModifier(name="Weapons In Stock",
                initMod=None,
                description="Adds all obtainable Keyblades into the Moogle shops",
                categories={'qol'},
                local_modifier=lambda settings: settings.set(settingkey.SHOP_KEYBLADES,True)
                ),
    DailyModifier(name="Deal More Damage",
                initMod=None,
                description="Removes the damage cap, making all stat increases matter",
                categories={'qol'},
                local_modifier=lambda settings: settings.set(settingkey.REMOVE_DAMAGE_CAP,True)
                ),
    DailyModifier(name="Beatable Seed",
                initMod=None,
                description="Seed is guaranteed to give you the three proofs, but some locations may be impossible to reach",
                categories={'access'},
                local_modifier=lambda settings: settings.set(settingkey.ACCESSIBILITY,"beatable")
                ),
    DailyModifier(name="Mini Super Bosses",
                initMod=None,
                description="Adds Absent Silhouettes and Sephiroth as possible locations",
                categories={'bosses'},
                local_modifier=lambda settings: settings.set(settingkey.SUPERBOSSES_WITH_REWARDS,[locationType.AS.name, locationType.Sephi.name])
                ),
    DailyModifier(name="Enter the Tournament",
                initMod=None,
                description="Cups are enabled, they give experience, and you start with full access to every cup (after beating Hydra)",
                categories={'misc'},
                local_modifier=cupsOn
                ),
    DailyModifier(name="What's in this Cavern?",
                initMod=None,
                description="Cavern of Remembrance is enabled",
                categories={'misc'},
                local_modifier=corOn
                ),
    DailyModifier(name="Yeet the Bear",
                initMod=None,
                description="Proof of Nonexistence will be on starry hill in 100 Acre Wood",
                categories={'proof','worlds'},
                local_modifier=lambda settings: settings.set(settingkey.YEET_THE_BEAR,True)
                ),
    DailyModifier(name="Proofs on Bosses",
                initMod=None,
                description="Proofs will be on the last non-data boss of a world.",
                categories={'proof'},
                local_modifier=lambda settings: settings.set(settingkey.PROOF_DEPTH,locationDepth.SecondBoss.name)
                ),
    DailyModifier(name="Biased Checks Early",
                initMod=None,
                description="Using the Slightly Easy item placement, good stuff is twice as likely to be in first half of worlds",
                categories={'placement'},
                local_modifier=lambda settings: settings.set(settingkey.ITEM_PLACEMENT_DIFFICULTY,'Slightly Easy')
                ),
    DailyModifier(name="Biased Checks Late",
                initMod=None,
                description="Using the Slightly Hard item placement, good stuff is twice as likely to be in second half of worlds",
                categories={'placement'},
                local_modifier=lambda settings: settings.set(settingkey.ITEM_PLACEMENT_DIFFICULTY,'Slightly Hard')
                ),
    DailyModifier(name="You can have 3 of those?",
                initMod=None,
                description="Randomized Stacked Abilities is turned on, changing the pool of potential abilities you can find",
                categories={'abilities'},
                local_modifier=lambda settings: settings.set(settingkey.ABILITY_POOL,'randomize stackable')
                ),
    DailyModifier(name="Where did you find these?",
                initMod=None,
                description="Moogle shops contain useful consumable items, such as drive recoveries and elixirs",
                categories={'qol'},
                local_modifier=addShops
                ),
    DailyModifier(name="What if you went to Twilight Town Last?",
                initMod=None,
                description="Shuffle the battle level of worlds.",
                categories={'btlv'},
                local_modifier=shuffleBattleLevel
                ),
    DailyModifier(name="All Worlds are the Same",
                initMod=None,
                description="All max battle levels are 50, and visits are scaled.",
                categories={'btlv'},
                local_modifier=fixedBattleLevel
                ),

]

dailyHardModifiers = [
    DailyModifier(name="Biased Checks Even Later",
                initMod=None,
                description="Using the Hard item placement, good stuff is likely to be pushed even later.",
                categories={'placement'},
                local_modifier=lambda settings: settings.set(settingkey.ITEM_PLACEMENT_DIFFICULTY,'Hard')
                ),
    DailyModifier(name="Biased Checks Way Later",
                initMod=None,
                description="Using the Very Hard item placement, good stuff is likely to be pushed way later.",
                categories={'placement'},
                local_modifier=lambda settings: settings.set(settingkey.ITEM_PLACEMENT_DIFFICULTY,'Very Hard')
                ),
    DailyModifier(name="All Super Bosses",
                initMod=None,
                description="Adds Absent Silhouettes, Sephiroth, Lingering Will, and Data Org as possible locations",
                categories={'bosses'},
                local_modifier=lambda settings: settings.set(settingkey.SUPERBOSSES_WITH_REWARDS,[locationType.AS.name, locationType.Sephi.name, locationType.DataOrg.name, locationType.LW.name])
                ),
    DailyModifier(name="Locked Second Visits (Mythic Version)",
                initMod=None,
                description="Visit unlocks are dispersed in the seed, requiring you to find them to get to second visits, and those items are Mythic rarity",
                categories={'progression'},
                local_modifier=lockedVisitsHard
                ),
    DailyModifier(name="No Final Form",
                initMod=None,
                description="You are unable to use final form. You can find it for more drive levels and Genie, but you can't go into the form",
                categories={'dol'},
                local_modifier=lambda settings: settings.set(settingkey.DISABLE_FINAL_FORM,True)
                ),
    DailyModifier(name="No Skipping :)",
                initMod=None,
                description="You can't skip into CoR or Throne Room. Get there normally :)",
                categories={'dol'},
                local_modifier=blockSkips
                ),
    DailyModifier(name="Vanilla Drive Leveling",
                initMod=None,
                description="Remember leveling drives in vanilla? You will now.",
                categories={'dol'},
                local_modifier=vanillaGrowth
                ),
    DailyModifier(name="Battle levels make no sense.",
                initMod=None,
                description="Battle levels are with 50 levels of original. 1-99 possible",
                categories={'btlv'},
                local_modifier=chaosBattleLevel
                ),
]

dailyBossEnemyModifiers = [
    DailyModifier(name="Final Fantasy Friends",
                initMod=None,
                description="Adds Cup Bosses to the Boss Pool",
                categories={'boss_pool'},
                local_modifier=lambda settings: settings.set("cups_bosses",True)
                ),
    DailyModifier(name="Enemies Change Per Room",
                initMod=None,
                description="Enemies are randomized 1-1 per room",
                categories={'enemy_pool'},
                local_modifier=lambda settings: settings.set("enemy","One to One Per Room")
                ),]

dailyHardBossEnemyModifiers = [
    DailyModifier(name="Superbosses",
                initMod=None,
                description="Adds Superbosses to the Boss Pool",
                categories={'hard_boss_pool'},
                local_modifier=lambda settings: settings.set("data_bosses",True)
                ),]


crit_modifier = [DailyModifier(name="Critical Mode",
                initMod=None,
                description="Enables the Randomized critical Bonuses, which you must play on critical to get.",
                categories={'hard_mode_setting'},
                local_modifier=lambda settings: settings.set(settingkey.CRITICAL_BONUS_REWARDS,True)
                ),
]

boss_enemy_modifier = [DailyModifier(name="Boss/Enemy",
                initMod=None,
                description="Enables boss and enemy randomization",
                categories={'boss_enemy_setting'},
                local_modifier=enableBossEnemy
                ),
]

def allDailyModifiers():
    return dailyModifiers + dailyHardModifiers + dailyBossEnemyModifiers + dailyHardBossEnemyModifiers


def getDailyModifiers(date, hard_mode = False, boss_enemy = False):
    random.seed(date.strftime('%d_%m_%Y'))
    # Weekends have more modifiers
    numMods = 3 if date.isoweekday() < 5 else 5
    chosenMods = []
    usedCategories = set()
    for _ in range(numMods):
        availableMods = []
        modifiers = dailyModifiers + ([] if not hard_mode else dailyHardModifiers)
        for m in modifiers:
            # Don't have more than one modifier from the same category
            if m.categories:
                if len(m.categories.intersection(usedCategories)) > 0:
                    continue
            # Don't have the same modifier twice
            if m.name in [m.name for m in chosenMods]:
                continue
            availableMods.append(m)
        chosen = random.choice(availableMods)
        if chosen.initMod:
            chosen = chosen.initMod(chosen) # A little strange, but the description and modifier needs to be randomly changed
        chosenMods.append(chosen)
        for c in chosen.categories:
            usedCategories.add(c)
    
    if hard_mode:
        chosenMods = crit_modifier + chosenMods
    
    if boss_enemy:
        chosenMods = boss_enemy_modifier + chosenMods

    return chosenMods

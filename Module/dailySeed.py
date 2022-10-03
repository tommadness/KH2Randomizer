import random
from collections import namedtuple

from Class import settingkey
from Class.seedSettings import SeedSettings
from List.ItemList import Items
from List.configDict import locationType

DailyModifier = namedtuple('DailyModifier', ['local_modifier', 'initMod', 'name', 'description', 'categories'])

def levelItUpLocal(seed_settings: SeedSettings):
    seed_settings.set(settingkey.SORA_LEVELS, 'ExcludeFrom99')
    seed_settings.set(settingkey.SORA_EXP_MULTIPLIER, 10.0)

def turnOffWorldsLocal(worlds: list):
    def _turnOffLocal(settings: SeedSettings):
        worlds_with_rewards = settings.get(settingkey.WORLDS_WITH_REWARDS)
        for world in worlds:
            if world.name in worlds_with_rewards:
                worlds_with_rewards.remove(world.name)
    return _turnOffLocal

def modifyShutOut(daily: DailyModifier):
    X = 3
    choices = [
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
    daily = daily._replace(description = daily.description.format(','.join(shut_out_world_names)),
                   local_modifier = daily.local_modifier(shut_out_worlds))
    return daily

dailyModifiers = [
    DailyModifier(name="Level it up",
                initMod=None,
                description="Level 99 but Sora XP multiplier set to 10x",
                categories={"xp"},
                local_modifier=levelItUpLocal
                ),
    DailyModifier(name="Shut Out of Worlds",
                description="The following worlds have closed their doors and hold no good checks: {}",
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
    DailyModifier(name="Locked Second Visits",
                initMod=None,
                description="Visit locks are dispersed in the seed, requiring you to find to get to second visits.",
                categories={'progression'},
                local_modifier=lambda settings: settings.set(settingkey.STARTING_STORY_UNLOCKS,[])
                )
]

# glass cannon
# schmovement
# AS/Sephi on
# synth + synth junk
# cups, with trophy, and exp
# cor
# randomized ability pool
# yeet the bear
# proofs on second visit bosses
# slightly hard
# slightly easy
# any%
# remove damage cap


# ------------------hard mode
# always 
#        turn crit bonuses on
#        exp down a bit
#        
# all bosses on
# extended logic
# key item weighting mythic
# disable final form
# block skips
# hard, very hard


def allDailyModifiers():
    return dailyModifiers


def getDailyModifiers(date):
    random.seed(date.strftime('%d_%m_%Y'))
    # Weekends have more modifiers
    numMods = 1#3 if date.isoweekday() < 5 else 5
    chosenMods = []
    usedCategories = set()
    for _ in range(numMods):
        availableMods = []
        for m in dailyModifiers:
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
    return chosenMods

import random, datetime
from collections import namedtuple

DailyModifier = namedtuple('DailyModifier', ['modifier', 'name', 'description', 'categories'])

# Default Settings are League + Enemy One-to-One + Boss One-to-One
def get_default_settings():
    return {
    "keybladeAbilities": ["Support"],
    "formExpMult":  {0: 1.0, 1: 5.0, 2: 3.0, 3: 3.0, 4: 2.0, 5: 3.0},
    "soraExpMult": 1.5,
    "levelChoice": "ExcludeFrom50",
    "spoilerLog": False,
    "keybladeMaxStat": 7,
    "keybladeMinStat": 0,
    "promiseCharm": False,
    "bossEnemy": False,
    "enemyOptions": {"boss": "One to One", "enemy": "One to One", "scale_boss_stats": True, "cups_bosses": True},
    "hintsType": "JSmartee",
    "startingInventory": [],
    "seedModifiers": [],
    "locations": ["Land of Dragons", "Beast's Castle", "Hollow Bastion", "Cavern of Remembrance", "Twilight Town", "The World That Never Was", "Space Paranoids", "Port Royal", "Olympus Coliseum", "Agrabah", "Halloween Town", "Pride Lands", "Disney Castle / Timeless River", "Hundred Acre Wood", "Simulated Twilight Town", "Absent Silhouettes", "Sephiroth", "Form Levels", "Garden of Assemblage", "Critical Bonuses"]
    }

def levelItUp(s):
    s["levelChoice"] = "ExcludeFrom99"
    s["soraExpMult"] = 10.0

def noLevels(s):
    s["levelChoice"] = "Level"
    s["startingInventory"].append("404")

def goMode(s):
    s["startingInventory"].append("593")
    s["startingInventory"].append("594")
    s["startingInventory"].append("595")

def enableSuperbosses(s):
    s["enemyOptions"]["data_bosses"] = True
    s["locations"] += ["Sephiroth", "Lingering Will (Terra)", "Data Organization XIII"]

dailyModifiers = [
    DailyModifier(name="Level it up",
                description="Level 99 but Sora XP multiplier set to 10x",
                categories={"xp"},
                modifier=levelItUp
                ),
    DailyModifier(name="No Levels",
                description="No checks on Levels and you start with No Experience",
                categories={"levels", "xp"},
                modifier=noLevels
                ),
    DailyModifier(name="Promise Charm",
                description="Start the game with the Promise Charm",
                categories={'progression'},
                modifier=lambda s: exec('s["promiseCharm"] = True')
                ),
    DailyModifier(name="Go Mode",
                description="Start the game with all 3 proofs",
                categories={'progression'},
                modifier=goMode
                ),
    DailyModifier(name="Action Keyblades",
                description="Keyblades can have action or support abilities",
                categories={'keyblades'},
                modifier=lambda s: s["keybladeAbilities"].append("Action")
                ),
    DailyModifier(name="Wild Bosses",
                description="Bosses are randomized using the Wild setting",
                categories={'bosses'},
                modifier=lambda s: exec('s["enemyOptions"]["boss"] = "Wild"')
                ),
    DailyModifier(name="Superbosses",
                description="All superbosses will be included in the randomization pool, and their reward locations are added to the item pool",
                categories={'bosses', 'worlds'},
                modifier=enableSuperbosses
                ),
    DailyModifier(name="Enemies Changed Every Room",
                description="The randomization mapping used for enemies is different every room",
                categories={'enemies'},
                modifier=lambda s: exec('s["enemyOptions"]["enemy"] = "One to One Per Room"')
                ),
    DailyModifier(name="X-Ray Vision",
                description="Sora starts the game with Scan",
                categories={},
                modifier=lambda s: s["startingInventory"].append("138")
                ),
    DailyModifier(name="Shananas Hints",
                description="Use Shananas hints",
                categories={'hints'},
                modifier=lambda s: exec('s["hintsType"] = "Shananas"')
                ),
    DailyModifier(name="Glass Cannon",
                description="Replaces all defense ups found during level ups",
                categories={'levels'},
                modifier=lambda s: s["seedModifiers"].append("Glass Cannon")
                ),
    DailyModifier(name="Library of Assemblage",
                description="Start the game with every Ansem Report",
                categories={'hints'},
                modifier=lambda s: s["seedModifiers"].append("Library of Assemblage")
                ),
    DailyModifier(name="Schmovement",
                description="Start the game with level 1 of each movement type",
                categories={},
                modifier=lambda s: s["seedModifiers"].append("Schmovement")
                ),
    DailyModifier(name="Better Junk",
                description="Replaces all synthesis materials with better items",
                categories={},
                modifier=lambda s: s["seedModifiers"].append("Better Junk")
                ),
    DailyModifier(name="Randomize Ability Pool",
                description="Pick Sora's Action/Support abilities at random (Guaranteed 1 SC & 1 OM)",
                categories={},
                modifier=lambda s: s["seedModifiers"].append("Randomize Ability Pool")
                ),
    DailyModifier(name="Have Some Finny Fun",
                description="Atlantica is turned on.",
                categories={'worlds'},
                modifier=lambda s: s["locations"].append("Atlantica")
    )
]

def getDailyModifiers(date):
    random.seed(date.strftime('%D'))
    # Weekends have more modifiers
    numMods = 3 if date.isoweekday() < 5 else 5
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
        chosenMods.append(chosen)
        for c in chosen.categories:
            usedCategories.add(c)
    return chosenMods

# I think I want to make it less side effecty, where this just returns an object
# And app can take responsibility for messing with the session
#    and regenerating the location types
def generateDailySeed():
    session = dict(get_default_settings())
    session["dailyModifiers"] = []
    currentDate = datetime.date.today()
    modifiers = getDailyModifiers(currentDate)
    for mod in modifiers:
        mod.modifier(session)
        session["dailyModifiers"].append(mod.name)
    session["seed"] = "Daily Seed " + currentDate.strftime('%D')
    return session

if __name__ == '__main__':
    seed = generateDailySeed()
    for k,v in seed.items():
        print("{}:{}".format(k, v))
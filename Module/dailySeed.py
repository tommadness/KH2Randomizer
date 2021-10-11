import random, datetime
from collections import namedtuple
from List.hashTextEntries import generateHashIcons

DailyModifier = namedtuple('DailyModifier', ['local_modifier','modifier', 'name', 'description', 'categories'])

# Default Settings are League + Enemy One-to-One + Boss One-to-One
def get_default_settings():
    return {
    "keybladeAbilities": ["Support"],
    "formExpMult":  {0: 1.0, 1: 5.0, 2: 3.0, 3: 3.0, 4: 2.0, 5: 3.0},
    "soraExpMult": 3,
    "levelChoice": "ExcludeFrom50",
    "spoilerLog": False,
    "keybladeMaxStat": 7,
    "keybladeMinStat": 0,
    "promiseCharm": False,
    "bossEnemy": False,
    "enemyOptions": {"boss": "One to One", "enemy": "One to One", "scale_boss_stats": True, "cups_bosses": True},
    "hintsType": "JSmartee",
    "startingInventory": [],
    "seedModifiers": ["Max Logic Item Placement"],
    "locations": ["Land of Dragons", "Beast's Castle", "Hollow Bastion", "Cavern of Remembrance", "Twilight Town", "The World That Never Was", "Space Paranoids", "Port Royal", "Olympus Coliseum", "Agrabah", "Halloween Town", "Pride Lands", "Disney Castle / Timeless River", "Hundred Acre Wood", "Simulated Twilight Town", "Absent Silhouettes", "Sephiroth", "Form Levels", "Garden of Assemblage", "Critical Bonuses"],
    "itemPlacementDifficulty": "Normal"
    }

def powerfulKeyblades(s):
    s["keybladeMaxStat"] = 20

def levelItUp(s):
    s["levelChoice"] = "ExcludeFrom99"
    s["soraExpMult"] = 10.0

def levelItUpLocal(s):
    s["Sora"]["levelChoice"] = "Level 99"
    s["Sora"]["soraExpMult"] = 10.0

def noLevels(s):
    s["levelChoice"] = "Level"
    s["startingInventory"].append("404")

def noLevelsLocal(s):
    s["Sora"]["levelChoice"] = "Level 1"
    s["Starting Items"]["startingInventory"].append(404)

def goMode(s):
    s["startingInventory"].append("593")
    s["startingInventory"].append("594")
    s["startingInventory"].append("595")

def goModeLocal(s):
    s["Starting Items"]["startingInventory"].append(593)
    s["Starting Items"]["startingInventory"].append(594)
    s["Starting Items"]["startingInventory"].append(595)

def enableSuperbosses(s):
    s["soraExpMult"] = max(s["soraExpMult"], 5)
    s["enemyOptions"]["data_bosses"] = True
    s["locations"] += ["Sephiroth", "Lingering Will (Terra)", "Data Organization XIII"]


def enableSuperbossesLocal(s):
    s["Sora"]["soraExpMult"] = max(s["Sora"]["soraExpMult"], 5)
    s["Boss/Enemy"]["data_bosses"] = True
    s["Superbosses with Rewards"]["Sephiroth"] = True
    s["Superbosses with Rewards"]["Lingering Will (Terra)"] = True
    s["Superbosses with Rewards"]["Data Organization XIII"] = True

dailyModifiers = [
    DailyModifier(name="Level it up",
                description="Level 99 but Sora XP multiplier set to 10x",
                categories={"xp"},
                modifier=levelItUp,
                local_modifier=levelItUpLocal
                ),
    DailyModifier(name="No Levels",
                description="No checks on Levels and you start with No Experience",
                categories={"levels", "xp"},
                modifier=noLevels,
                local_modifier=noLevelsLocal
                ),
    DailyModifier(name="Promise Charm",
                description="Promise Charm is added to the item pool",
                categories={'progression'},
                modifier=lambda s: exec('s["promiseCharm"] = True'),
                local_modifier=lambda s: exec('s["Item Placement Options"]["PromiseCharm"]=True')
                ),
    DailyModifier(name="Go Mode",
                description="Start the game with all 3 proofs",
                categories={'progression'},
                modifier=goMode,
                local_modifier=goModeLocal
                ),
    DailyModifier(name="Action Keyblades",
                description="Keyblades can have action or support abilities",
                categories={'keyblades'},
                modifier=lambda s: s["keybladeAbilities"].append("Action"),
                local_modifier=lambda s: exec('s["Keyblades"]["keybladeAction"]=True')
                ),
    DailyModifier(name="Wild Bosses",
                description="Bosses are randomized using the Wild setting",
                categories={'bosses'},
                modifier=lambda s: exec('s["enemyOptions"]["boss"] = "Wild"'),
                local_modifier=lambda s: exec('s["Boss/Enemy"]["boss"]="Wild"')
                ),
    DailyModifier(name="Superbosses",
                description="All superbosses will be included in the randomization pool, and their reward locations are added to the item pool, but your XP is at leat times 5",
                categories={'bosses', 'worlds'},
                modifier=enableSuperbosses,
                local_modifier=enableSuperbossesLocal
                ),
    DailyModifier(name="X-Ray Vision",
                description="Sora starts the game with Scan",
                categories={},
                modifier=lambda s: s["startingInventory"].append("138"),
                local_modifier=lambda s: s["Starting Items"]["startingInventory"].append(138),
                ),
    DailyModifier(name="Shananas Hints",
                description="Use Shananas hints",
                categories={'hints'},
                modifier=lambda s: exec('s["hintsType"] = "Shananas"'),
                local_modifier=lambda s: exec('s["Hint Systems"]["hintsType"] = "Shananas"')
                ),
    DailyModifier(name="Glass Cannon",
                description="Replaces all defense ups found during level ups",
                categories={'levels'},
                modifier=lambda s: s["seedModifiers"].append("Glass Cannon"),
                local_modifier=lambda s: exec('s["Seed Modifiers"]["Glass Cannon"] = True')
                ),
    DailyModifier(name="Library of Assemblage",
                description="Start the game with every Ansem Report",
                categories={'hints'},
                modifier=lambda s: s["seedModifiers"].append("Library of Assemblage"),
                local_modifier=lambda s: exec('s["Starting Items"]["Library of Assemblage"] = True')
                ),
    DailyModifier(name="Schmovement",
                description="Start the game with level 1 of each movement type",
                categories={},
                modifier=lambda s: s["seedModifiers"].append("Schmovement"),
                local_modifier=lambda s: exec('s["Starting Items"]["Schmovement"] = True')
                ),
    DailyModifier(name="Better Junk",
                description="Replaces all synthesis materials with better items",
                categories={},
                modifier=lambda s: s["seedModifiers"].append("Better Junk"),
                local_modifier=lambda s: exec('s["Seed Modifiers"]["Better Junk"] = True')
                ),
    DailyModifier(name="Randomize Ability Pool",
                description="Pick Sora's Action/Support abilities at random (Guaranteed 1 SC & 1 OM)",
                categories={},
                modifier=lambda s: s["seedModifiers"].append("Randomize Ability Pool"),
                local_modifier=lambda s: exec('s["Item Placement Options"]["Randomize Ability Pool"] = True')
                ),
    DailyModifier(name="Have Some Finny Fun",
                description="Atlantica is turned on.",
                categories={'worlds'},
                modifier=lambda s: s["locations"].append("Atlantica"),
                local_modifier=lambda s: exec('s["Worlds with Rewards"]["Atlantica"] = True')
                ),
    DailyModifier(name="Remove Damage Cap",
                description="Remove Damage Cap for Sora dealing damage to enemies",
                categories={},
                modifier=lambda s: s["seedModifiers"].append("Remove Damage Cap"),
                local_modifier=lambda s: exec('s["Seed Modifiers"]["Remove Damage Cap"] = True')
                ),
    DailyModifier(name="More Powerful keyblades",
                description="Keyblades can have maximum stats of up to 20",
                categories={'keyblades'},
                modifier=powerfulKeyblades,
                local_modifier=lambda s: exec('s["Keyblades"]["keybladeMaxStat"]=20')
                ),
    DailyModifier(name="Early Checks",
                description="Worlds are more likely to have better checks early, than late",
                categories={'itemdifficulty'},
                modifier=lambda s: exec('s["itemPlacementDifficulty"] = "Easy"'),
                local_modifier=lambda s: exec('s["Item Placement Options"]["itemPlacementDifficulty"] = "Easy"')
                ),
    DailyModifier(name="Late Checks",
                description="Worlds are more likely to have better checks early, than late",
                categories={'itemdifficulty'},
                modifier=lambda s: exec('s["itemPlacementDifficulty"] = "Hard"'),
                local_modifier=lambda s: exec('s["Item Placement Options"]["itemPlacementDifficulty"] = "Hard"')
                ),
    DailyModifier(name="No Starting AP",
                description="Sora/Donald/Goofy start the game with 0 AP",
                categories= {"abilities"},
                modifier=lambda s: s["seedModifiers"].append("Start with No AP"),
                local_modifier=lambda s: exec('s["Seed Modifiers"]["Start with No AP"] = True')
                )
]

def getDailyModifiers(date):
    random.seed(date.strftime('%d_%m_%Y'))
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
    session['seedHashIcons'] = generateHashIcons()
    return session

if __name__ == '__main__':
    seed = generateDailySeed()
    for k,v in seed.items():
        print("{}:{}".format(k, v))
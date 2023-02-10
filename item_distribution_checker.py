import random
import string
from Class import settingkey
from Class.exceptions import RandomizerExceptions
from Class.itemClass import KH2Item, itemRarity
from Class.newLocationClass import KH2Location
from Class.seedSettings import SeedSettings
from List.configDict import itemDifficulty, locationCategory
from Module.newRandomize import RandomizerSettings,Randomizer
from Module.seedEvaluation import LocationInformedSeedValidator

def make_rando_seed(difficulty,seed_name):
    seed_settings = SeedSettings()
    seed_settings.set(settingkey.ITEM_PLACEMENT_DIFFICULTY,difficulty)
    seed_settings.set(settingkey.SORA_LEVELS,"ExcludeFrom99")
    seed_settings.set(settingkey.SUPERBOSSES_WITH_REWARDS,["AS","Sephi"])#"DataOrg",
    seed_settings.set(settingkey.STORY_UNLOCK_CATEGORY,itemRarity.RARE)
    settings = RandomizerSettings(seed_name,True,"version",seed_settings, "")
    newSeedValidation = LocationInformedSeedValidator()
    randomizer = None
    while True:
        try:
            randomizer = Randomizer(settings)
            result = newSeedValidation.validateSeed(settings,randomizer)
            break
        except RandomizerExceptions as e:
            characters = string.ascii_letters + string.digits
            settings.random_seed = (''.join(random.choice(characters) for i in range(30)))
            settings.create_full_seed_string()
            last_error = e
            continue

    item_depths = {}
    item_depths[itemRarity.COMMON] = []
    item_depths[itemRarity.UNCOMMON] = []
    item_depths[itemRarity.RARE] = []
    item_depths[itemRarity.MYTHIC] = []

    for assignment in randomizer.assignedItems:
        loc: KH2Location = assignment.location
        item : KH2Item = assignment.item
        item2 : KH2Item = assignment.item2

        if loc.LocationCategory is locationCategory.WEAPONSLOT:
            continue

        if item:
            item_depths[item.Rarity].append(randomizer.location_weights.location_depths[loc])
        if item2:
            item_depths[item2.Rarity].append(randomizer.location_weights.location_depths[loc])
    
    return item_depths
        
        
if __name__ == '__main__':
    for difficulty in itemDifficulty:
        counts = {}
        counts[itemRarity.COMMON] = {}
        counts[itemRarity.UNCOMMON] = {}
        counts[itemRarity.RARE] = {}
        counts[itemRarity.MYTHIC] = {}
        max_r = 0

        for i in range(21):
            counts[itemRarity.COMMON][i] = 0
            counts[itemRarity.UNCOMMON][i] = 0
            counts[itemRarity.RARE][i] = 0
            counts[itemRarity.MYTHIC][i] = 0

        print(difficulty)
        num_attempts = 100
        for attempt in range(num_attempts):
            item_results = make_rando_seed(difficulty,difficulty+str(attempt))
            for rarity in itemRarity:
                results = item_results[rarity]
                rarity_count = counts[rarity]
                for r in results:
                    max_r = max(max_r,r)
                    rarity_count[r]+=1

        line_string = "\t\t"
        for i in range(max_r+1):
            line_string+=f"{i}\t"
        print(line_string)
        for rarity in itemRarity:
            rarity_count = counts[rarity]
            line_string = rarity+"\t"
            if rarity != itemRarity.UNCOMMON:
                line_string+="\t"
            for i in range(max_r+1):
                line_string+=f"{rarity_count[i]*1.0/num_attempts}\t"
            print(line_string)

        

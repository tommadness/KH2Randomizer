
import sys
sys.path.append("..")
from Class.locationClass import KH2FormLevel,KH2Treasure
from List.configDict import itemType,locationDepth,locationType
from Module.randomize import KH2Randomizer
import unittest


class Tests(unittest.TestCase):
    def test_determinism(self):
        previous_locations = None
        for i in range(100):
            seed = self.createSeed(f"testing_determinism",[],[],[],[])
            current_locations = seed._locationItems
            if previous_locations is not None:
                for i in range(len(previous_locations)):
                    assert previous_locations[i]==current_locations[i]
                previous_locations = current_locations


    @staticmethod
    def createSeed(seedName,treasure_items,treasure_locations,form_items,form_locations):
        randomizer = KH2Randomizer(seedName = seedName)
        randomizer.populateLocations([])
        randomizer.populateItems(promiseCharm = True, startingInventory = [], abilityListModifier=None)

        treasures = [location for location in randomizer._validLocationList if isinstance(location,KH2Treasure)]
        formLevels = [location for location in randomizer._validLocationList if isinstance(location,KH2FormLevel)]

        for index, t_loc_id in enumerate(treasure_locations):
            t_location = [loc for loc in treasures if loc.Id==t_loc_id][0]
            t_location.setReward(treasure_items[index])
            item_obj = [obj for obj in randomizer._validItemList if obj.Id==treasure_items[index]][0]
            randomizer._validLocationList.remove(t_location)
            t_location.InvalidChecks.append(itemType.JUNK)
            randomizer._validItemList.remove(item_obj)
            randomizer._locationItems.append((t_location, item_obj))

        for index, f_loc_id in enumerate(form_locations):
            f_location = [loc for loc in formLevels if loc.getFormName()==f_loc_id[0] and loc.FormLevel==f_loc_id[1]][0]
            f_location.setReward(form_items[index])
            item_obj = [obj for obj in randomizer._validItemList if obj.Id==form_items[index]][0]
            randomizer._validLocationList.remove(f_location)
            f_location.InvalidChecks.append(itemType.JUNK)
            randomizer._validItemList.remove(item_obj)
            randomizer._locationItems.append((f_location, item_obj))

        randomizer.setKeybladeAbilities()
        randomizer.setRewards()
        randomizer.setLevels(5,{'0':3, '1':3, '2':3, '3':3, '4':3, '5':3})
        randomizer.setBonusStats()
        return randomizer

ut = Tests()

unittest.main()

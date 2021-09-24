
from Class.locationClass import KH2Location, KH2ItemStat, KH2LevelUp, KH2FormLevel, KH2Bonus, KH2Treasure, KH2StartingItem, KH2ItemStat, KH2Puzzle

from List.configDict import itemType, locationType

from Module.importantItems import getImportantChecks,getUsefulItems
from Module.itemPlacementRestriction import ItemPlacementRestriction
from Module.startingInventory import StartingInventory


class SeedValidator:
    def __init__(self,sessionDict):
        nightmare = "Nightmare"==sessionDict["itemPlacementDifficulty"]
        if "Reverse Rando" in sessionDict["seedModifiers"]:
            self.itemRestrictions = ItemPlacementRestriction("Reverse",nightmare)
        else:
            self.itemRestrictions = ItemPlacementRestriction("Regular",nightmare)

    def validateSeed(self, sessionDict, randomizer):
        startingInventory = sessionDict["startingInventory"]

        trsrList = [location for location in randomizer._allLocationList if isinstance(location, KH2Treasure)]
        lvupList = [location for location in randomizer._allLocationList if isinstance(location, KH2LevelUp)]
        bonsList = [location for location in randomizer._allLocationList if isinstance(location, KH2Bonus)]
        fmlvList = [location for location in randomizer._allLocationList if isinstance(location, KH2FormLevel)]
        puzzleList = [location for location in randomizer._allLocationList if isinstance(location, KH2Puzzle)]
        plrpList = []
        [plrpList.append(location) for location in randomizer._allLocationList if isinstance(location, KH2StartingItem) and not location in plrpList]
        StartingInventory.generateStartingInventory(plrpList[0], startingInventory)
        inventory = []


        # grab everything that can't possibly be locked by items
        for i in plrpList:
            inventory += i.Items
            # remove the starting inventory to prevent duplication
            for j in startingInventory:
                i.Items.remove(int(j))
        for i in lvupList:
            inventory.append(i.getReward())

        treasure_restriction,bonus_restriction,form_restriction,puzzle_restriction = self.itemRestrictions.get_restriction_functions()

        changed = True
        depth = 0
        while changed:
            depth+=1
            if len(trsrList)==0 and len(bonsList)==0 and len(fmlvList)==0:
                print(f"Logic depth {depth}")
                return True
            changed = False
            treasures_to_remove = []
            bonuses_to_remove = []
            forms_to_remove = []
            puzzles_to_remove = []
            # pass through remaining treasures and find unlockable things
            for i in trsrList:
                location_id = i.Id
                reward_id = i.ItemId
                if treasure_restriction(location_id)(inventory):
                    treasures_to_remove.append(i)
                    inventory.append(reward_id)
                    changed = True
            for i in bonsList:
                location_id = i.RewardId
                reward_id = i.getReward()
                if bonus_restriction(location_id)(inventory):
                    bonuses_to_remove.append(i)
                    inventory.append(reward_id)
                    changed = True
            for i in fmlvList:
                reward_id = i.Ability
                if form_restriction(i.FormId,i.FormLevel)(inventory):
                    forms_to_remove.append(i)
                    inventory.append(reward_id)
                    changed = True
            for i in puzzleList:
                reward_id = i.ItemId
                if puzzle_restriction(i.Id)(inventory):
                    puzzles_to_remove.append(i)
                    inventory.append(reward_id)
                    changed = True
            for i in treasures_to_remove:
                trsrList.remove(i)
            for i in bonuses_to_remove:
                bonsList.remove(i)
            for i in forms_to_remove:
                fmlvList.remove(i)
            for i in puzzles_to_remove:
                puzzleList.remove(i)

        return False

class SeedMetricsNumDatas:
    def metrics(self, randomizer):

        trsrList = [location for location in randomizer._allLocationList if isinstance(location, KH2Treasure)]
        useful_items = getImportantChecks()+getUsefulItems()

        num_data_checks = 0
        for i in trsrList:
            reward_id = i.ItemId
            if locationType.DataOrg in i.LocationTypes and reward_id in useful_items:
                num_data_checks+=1

        return num_data_checks


class SeedMetricsNumCritExtra:
    def metrics(self, randomizer):

        trsrList = [location for location in randomizer._allLocationList if isinstance(location, KH2StartingItem)]
        useful_items = getImportantChecks()+getUsefulItems()

        num_starting_checks = 0
        for i in trsrList:
            rewards = i.Items
            for reward_id in rewards:
                if reward_id in useful_items:
                    num_starting_checks+=1

        return num_starting_checks

class SeedMetricsGenDataFrame:
    def metrics(self, randomizer):
        useful_items = getImportantChecks()+getUsefulItems()
        item_dict = {}
        crit_duplicates = 0
        for loc,item in randomizer._locationItems:
            if item.Id in useful_items:
                desc = loc.getDescription()
                if desc in item_dict:
                    crit_duplicates+=1
                    desc +=str(crit_duplicates)
                item_dict[desc] = item.Id
        return item_dict
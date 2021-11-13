
from List.configDict import isFormCheck, locationCategory, locationType
from Module.RandomizerSettings import RandomizerSettings

from Module.itemPlacementRestriction import ItemPlacementRestriction
from Module.newRandomize import Randomizer


class SeedValidator:
    def __init__(self,settings: RandomizerSettings):
        nightmare = "Nightmare"==settings.itemPlacementDifficulty
        if settings.reverse_rando:
            self.itemRestrictions = ItemPlacementRestriction("Reverse",nightmare)
        else:
            self.itemRestrictions = ItemPlacementRestriction("Regular",nightmare)

    def validateSeed(self, settings: RandomizerSettings, randomizer: Randomizer):
        startingInventory = settings.startingItems

        trsrList = [assignment for assignment in randomizer.assignedItems if assignment.location.LocationCategory in [locationCategory.CHEST,locationCategory.POPUP] and locationType.Puzzle not in assignment.location.LocationTypes]
        lvupList =  [assignment for assignment in randomizer.assignedItems if assignment.location.LocationCategory in [locationCategory.LEVEL]]
        bonsList = [assignment for assignment in randomizer.assignedItems if assignment.location.LocationCategory in [locationCategory.DOUBLEBONUS,locationCategory.HYBRIDBONUS,locationCategory.ITEMBONUS,locationCategory.STATBONUS]]
        fmlvList = [assignment for assignment in randomizer.assignedItems if isFormCheck(assignment.location.LocationCategory)]
        puzzleList =  [assignment for assignment in randomizer.assignedItems if locationType.Puzzle in assignment.location.LocationTypes]

        inventory = []


        # grab everything that can't possibly be locked by items
        inventory += startingInventory
        for i in lvupList:
            inventory.append(i.item.Id)
            if i.item2 is not None: 
                inventory.append(i.item2.Id)

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
                location_id = i.location
                if treasure_restriction(location_id)(inventory):
                    treasures_to_remove.append(i)
                    inventory.append(i.item.Id)
                    if i.item2 is not None:
                        inventory.append(i.item2.Id)
                    changed = True
            for i in bonsList:
                location_id = i.location
                if bonus_restriction(location_id)(inventory):
                    bonuses_to_remove.append(i)
                    inventory.append(i.item.Id)
                    if i.item2 is not None:
                        inventory.append(i.item2.Id)
                    changed = True
            for i in fmlvList:
                location_id = i.location
                if form_restriction(location_id)(inventory):
                    forms_to_remove.append(i)
                    inventory.append(i.item.Id)
                    if i.item2 is not None:
                        inventory.append(i.item2.Id)
                    changed = True
            for i in puzzleList:
                location_id = i.location
                if puzzle_restriction(location_id)(inventory):
                    puzzles_to_remove.append(i)
                    inventory.append(i.item.Id)
                    if i.item2 is not None:
                        inventory.append(i.item2.Id)
                    changed = True
            for i in treasures_to_remove:
                trsrList.remove(i)
            for i in bonuses_to_remove:
                bonsList.remove(i)
            for i in forms_to_remove:
                fmlvList.remove(i)
            for i in puzzles_to_remove:
                puzzleList.remove(i)

        print("Failed seed, trying again")
        raise RuntimeError(f"We couldn't access trsr {trsrList} bons {bonsList} form {fmlvList} puzz {puzzleList}")
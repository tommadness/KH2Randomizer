
from typing import List
from Class.newLocationClass import KH2Location
from Class.itemClass import KH2Item
# from List.configDict import locationCategory, locationDepth, locationType
from List.configDict import itemType
from Module.newRandomize import Randomizer, ItemAssignment
from Module.RandomizerSettings import RandomizerSettings

class MultiWorldConfig():
    def __init__(self,settings: RandomizerSettings):
        self.mixed_item_count = 20
        self.num_players = 2
        self.item_swaps = [itemType.FIRE,itemType.BLIZZARD,itemType.THUNDER,itemType.CURE,itemType.MAGNET,itemType.REFLECT,itemType.PROMISE_CHARM,itemType.PROOF,itemType.PROOF_OF_PEACE,itemType.PROOF_OF_CONNECTION, itemType.STORYUNLOCK]

class MultiWorldEntry():
    def __init__(self, finder, owner, where_found: KH2Location, what_found: KH2Item):
        self.finder = finder
        self.owner = owner
        self.where_found = where_found
        self.what_found = what_found

class MultiWorldOutput():
    def __init__(self, config: MultiWorldConfig):
        self.new_assignments = []
        for x in range(config.num_players):
            self.new_assignments.append({})


class MultiWorld():
    def __init__(self, seeds: List[Randomizer], config: MultiWorldConfig):
        all_candidate_swaps: List[List[ItemAssignment]] = []

        for seed in seeds:
            all_candidate_swaps.append([])
            for assignment in seed.assignedItems:
                if assignment.item is not None and assignment.item.ItemType in config.item_swaps:
                    all_candidate_swaps[-1].append(assignment)
                elif assignment.item2 is not None and assignment.item2.ItemType in config.item_swaps:
                    all_candidate_swaps[-1].append(assignment)


        for player in range(len(all_candidate_swaps)):
            candiate_swaps = all_candidate_swaps[player]
            print(f"Player {player}")
            for assignment in candiate_swaps:
                print(f"--- ({assignment.item},{assignment.item2}) in {assignment.location.Description}")
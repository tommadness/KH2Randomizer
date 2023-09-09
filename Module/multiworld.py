
import random
from typing import List

from Class.itemClass import KH2Item
from Class.newLocationClass import KH2Location
from List.ItemList import Items
from List.configDict import itemType, locationCategory
from Module.RandomizerSettings import RandomizerSettings
from Module.newRandomize import Randomizer, ItemAssignment


class MultiWorldConfig():
    def __init__(self,settings: RandomizerSettings):
        self.mixed_item_count = 20
        self.num_players = 2
        self.item_swaps = [itemType.FIRE, itemType.BLIZZARD, itemType.THUNDER, itemType.CURE, itemType.MAGNET, itemType.REFLECT, itemType.PROMISE_CHARM, itemType.PROOF_OF_NONEXISTENCE, itemType.PROOF_OF_PEACE, itemType.PROOF_OF_CONNECTION, itemType.STORYUNLOCK]
        self.location_swaps = [locationCategory.CHEST]

class MultiWorldEntry():
    def __init__(self, finder, owner, where_found: KH2Location, what_found: KH2Item):
        self.finder = finder
        self.owner = owner
        self.where_found : KH2Location = where_found
        self.what_found : KH2Item = what_found

    def __call__(self):
        location_category = ""
        if self.where_found.LocationCategory in [locationCategory.ITEMBONUS,locationCategory.HYBRIDBONUS,locationCategory.STATBONUS,locationCategory.DOUBLEBONUS]:
            location_category = "BONUS"
        else:
            location_category = self.where_found.LocationCategory.name
        return {"name":self.what_found.Id,"location":location_category+"-"+str(self.where_found.LocationId),"to":self.owner,"from":self.finder}

class MultiWorldOutput():
    def __init__(self):
        self.new_assignments = []

    def add_item(self,item,location,from_player,to_player):
        self.new_assignments.append(MultiWorldEntry(from_player,to_player,location,item))


    def __call__(self):
        output = {"items":[]}
        for a in self.new_assignments:
            output["items"].append(a())
        return output

class MultiWorld():
    def __init__(self, seeds: List[Randomizer], config: MultiWorldConfig):
        self.all_candidate_swaps: List[List[ItemAssignment]] = []

        for seed in seeds:
            self.all_candidate_swaps.append([])
            for assignment in seed.assignments:
                if assignment.location.LocationCategory in config.location_swaps:
                    if assignment.item is not None and assignment.item.ItemType in config.item_swaps:
                        self.all_candidate_swaps[-1].append(assignment)
                    # elif assignment.item2 is not None and assignment.item2.ItemType in config.item_swaps:
                    #     self.all_candidate_swaps[-1].append(assignment)

        for player in range(len(self.all_candidate_swaps)):
            candiate_swaps = self.all_candidate_swaps[player]
            print(f"Player {player}")
            for assignment in candiate_swaps:
                print(f"--- ({assignment.item},{assignment.item2}) in {assignment.location.Description}({assignment.location.LocationId})")

        self.mix(config)

        print("------------------")

        for player in range(len(self.all_candidate_swaps)):
            candiate_swaps = self.all_candidate_swaps[player]
            print(f"Player {player}")
            for assignment in candiate_swaps:
                print(f"--- ({assignment.item},{assignment.item2}) in {assignment.location.Description}({assignment.location.LocationId})")

    

    def mix(self,config: MultiWorldConfig):
        full_swaps = []
        max_item_swap = 999999
        for i,player in enumerate(self.all_candidate_swaps):
            max_item_swap = min(len(player),max_item_swap)
            for j in range(len(player)):
                full_swaps.append((i,j))

        max_item_swap=min(config.mixed_item_count,max_item_swap*config.num_players)
        

        swap_chain = []
        swap_chain.append(random.choice(full_swaps))
        full_swaps.remove(swap_chain[-1])

        for _ in range(max_item_swap-1):
            filtered_list = [it for it in full_swaps if it[0]!=swap_chain[-1][0]]
            swap_chain.append(random.choice(filtered_list))
            full_swaps.remove(swap_chain[-1])

        self.multi_output = MultiWorldOutput()

        prev_owner = swap_chain[-1][0]
        temp_item = swap_chain[-1][1]

        for ch in swap_chain:
            item = self.all_candidate_swaps[prev_owner][temp_item].item
            location = self.all_candidate_swaps[ch[0]][ch[1]].location

            self.multi_output.add_item(item,location,ch[0],prev_owner)
            prev_owner = ch[0]
            temp_item = ch[1]
    
        print(self.multi_output())


        for s in self.multi_output.new_assignments:
            # print(s())
            for ass in self.all_candidate_swaps[s.finder]:
                # print(f"{ass.location == s.where_found} {ass.location}")
                if ass.location == s.where_found:
                    ass.item = Items.sharedMultiItem()
                    break



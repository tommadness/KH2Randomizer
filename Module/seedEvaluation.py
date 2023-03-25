
import copy
from typing import Any
from Class.exceptions import ValidationException
from Class.newLocationClass import KH2Location
from List.ItemList import Items
from List.configDict import locationType
from Module.RandomizerSettings import RandomizerSettings
from List.NewLocationList import get_all_parent_edge_reqs
from List.configDict import locationCategory

from Module.newRandomize import Randomizer

class ValidationResult:
    def __init__(self,any_per=False,clear=False):
        self.any_percent = any_per
        self.full_clear = clear


class LocationInformedSeedValidator:
    def __init__(self):
        pass

    def evaluate(self,inventory: list[int],reqs_list : list[Any]):
        result = True
        for r in reqs_list:
            result = result and r(inventory)
        return result

    def is_location_available(self,inventory: list[int], loc : KH2Location):
        return self.evaluate(inventory,self.location_requirements[loc])

    def prep_req_list(self, settings: RandomizerSettings, randomizer: Randomizer):
        self.location_graphs = []
        if settings.regular_rando:
            self.location_graphs.append(randomizer.regular_locations.location_graph)
        if settings.reverse_rando:
            self.location_graphs.append(randomizer.reverse_locations.location_graph)

        self.location_requirements = {}
        for graph in self.location_graphs:
            for node in graph.node_list():
                reqs = get_all_parent_edge_reqs(node,graph)
                for loc in graph.node_data(node).locations:
                    if loc in self.location_requirements:
                        self.location_requirements[loc] += reqs
                    else:
                        self.location_requirements[loc] = reqs

        # def get_recipe(loc):
        #     for r in randomizer.synthesis_recipes:
        #         if r.location == loc:
        #             return r
        #     return None

        # for loc in self.location_requirements:
        #     if locationType.SYNTH in loc.LocationTypes:
        #         # this is a synth location, we need to get its recipe to know what locks it logically
        #         recipe = get_recipe(loc)
        #         for req in recipe.requirements:
        #             synth_item_id = req.item_id
        #             # now that we know what synth item is in the recipe, we can determine what to add to the logic
        #             # TODO FINISH


    def validateSeed(self, settings: RandomizerSettings, randomizer: Randomizer, verbose=True):

        self.prep_req_list(settings,randomizer)

        startingInventory = settings.startingItems
        location_requirements = copy.deepcopy(self.location_requirements)

        results = ValidationResult()
        inventory = []
        inventory += startingInventory
        if len(randomizer.shop_items)>0:
            for i in randomizer.shop_items:
                inventory.append(i.Id)

        changed = True
        depth = 0
        while changed:
            depth+=1
            if all([x in inventory for x in [593,594,595]]):
                results.any_percent = True

            if len(location_requirements)==0:
                if verbose:
                    print(f"Logic Depth {depth}")
                results.full_clear = True
                break
            changed = False
            locations_to_remove = []
            for loc_req in location_requirements.items():
                loc,req = loc_req
                if self.evaluate(inventory,req):
                    #find assigned item to location
                    for assignment in randomizer.assignedItems:
                        # if assignment is one of the struggle win/lose items, only count one, and not count the second.
                        if assignment.location.LocationCategory is locationCategory.POPUP and assignment.location.LocationId == 389:
                            continue
                        if loc == assignment.location:
                            inventory.append(assignment.item.Id)
                            if assignment.item2 is not None:
                                inventory.append(assignment.item2.Id)
                            break
                    locations_to_remove.append(loc)
                    changed = True
            for i in locations_to_remove:
                location_requirements.pop(i)

        if (settings.item_accessibility=="all" and results.full_clear) or (settings.item_accessibility=="beatable" and results.any_percent):
            #we all good
            print(f"Unreachable locations {len(location_requirements)}")
            return [i for i in location_requirements.keys()]
        else:
            if verbose:
                print("Failed seed, trying again")
            
            # print(inventory)
            # for loc in location_requirements:
            #     print(loc[0].Description)
            #     for assignment in randomizer.assignedItems:
            #         if loc[0] == assignment.location:
            #             print(f"---{assignment.item.Name}")
            raise ValidationException(f"Completion checking failed to collect {len(location_requirements)} items")

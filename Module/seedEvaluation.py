
from Class.exceptions import ValidationException
from List.ItemList import Items
from Module.RandomizerSettings import RandomizerSettings
from List.NewLocationList import get_all_parent_edge_reqs

from Module.newRandomize import Randomizer

class ValidationResult:
    def __init__(self,any_per=False,clear=False):
        self.any_percent = any_per
        self.full_clear = clear


class LocationInformedSeedValidator:
    def __init__(self):
        pass

    def evaluate(self,inventory,reqs_list):
        result = True
        for r in reqs_list:
            result = result and r(inventory)
        return result

    def validateSeed(self, settings: RandomizerSettings, randomizer: Randomizer, verbose=True):
        startingInventory = settings.startingItems

        location_graphs = []
        if settings.regular_rando:
            location_graphs.append(randomizer.regular_locations.location_graph)
        if settings.reverse_rando:
            location_graphs.append(randomizer.reverse_locations.location_graph)

        results = ValidationResult(True,True)

        for graph in location_graphs:
            result = ValidationResult()
            inventory = []
            inventory += startingInventory

            location_requirements = []
            for node in graph.node_list():
                reqs = get_all_parent_edge_reqs(node,graph)
                for loc in graph.node_data(node).locations:
                    location_requirements.append((loc,reqs))

            changed = True
            depth = 0
            while changed:
                depth+=1
                if all([x in inventory for x in [593,594,595]]):
                    result.any_percent = True

                if len(location_requirements)==0:
                    if verbose:
                        print(f"Logic Depth {depth}")
                    result.full_clear = True
                    break
                changed = False
                locations_to_remove = []
                for loc_req in location_requirements:
                    loc,req = loc_req
                    if self.evaluate(inventory,req):
                        #find assigned item to location
                        for assignment in randomizer.assignedItems:
                            if loc == assignment.location:
                                inventory.append(assignment.item.Id)
                                if assignment.item2 is not None:
                                    inventory.append(assignment.item2.Id)
                                break
                        locations_to_remove.append(loc_req)
                        changed = True
                for i in locations_to_remove:
                    location_requirements.remove(i)

            results.any_percent &= result.any_percent
            results.full_clear &= result.full_clear

        if (settings.item_accessibility=="all" and results.full_clear) or (settings.item_accessibility=="beatable" and results.any_percent):
            #we all good
            print(f"Unreachable locations {len(location_requirements)}")
            return [i[0] for i in location_requirements]
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

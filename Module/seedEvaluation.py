
from Class.exceptions import ValidationException
from List.ItemList import Items
from Module.RandomizerSettings import RandomizerSettings

from Module.newRandomize import Randomizer

class LocationInformedSeedValidator:
    def __init__(self):
        pass

    def evaluate(self,inventory,reqs_list):
        result = True
        for r in reqs_list:
            result = result and r(inventory)
        return result

    def validateSeed(self, settings: RandomizerSettings, randomizer: Randomizer):
        startingInventory = settings.startingItems
        inventory = []
        if not settings.world_unlocks:
            inventory += [i.Id for i in Items.getStoryKeyItems()]
        inventory += startingInventory

        graph = randomizer.master_locations.location_graph

        location_requirements = []
        for loc in graph.node_data("Starting").locations:
            location_requirements.append((loc,[]))


        def dfs_search(node_name,reqs):
            out_edges = graph.out_edges(node_name)
            for e in out_edges:
                data = graph.edge_data(e)
                _,target = graph.edge_by_id(e)
                req_for_target = data.requirement
                new_reqs = reqs + [req_for_target]
                for loc in graph.node_data(target).locations:
                    location_requirements.append((loc,new_reqs))
                dfs_search(target,new_reqs)

        dfs_search("Starting",[])

        changed = True
        depth = 0
        while changed:
            depth+=1
            if len(location_requirements)==0:
                print(f"Logic Depth {depth}")
                return True
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
        
        print("Failed seed, trying again")
        raise ValidationException(f"Completion checking failed to collect {len(location_requirements)} items")

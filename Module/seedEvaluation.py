
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

    def validateSeed(self, settings: RandomizerSettings, randomizer: Randomizer, verbose=True):
        startingInventory = settings.startingItems

        location_graphs = []
        if settings.regular_rando:
            location_graphs.append(randomizer.regular_locations.location_graph)
        if settings.reverse_rando:
            location_graphs.append(randomizer.reverse_locations.location_graph)

        for graph in location_graphs:
            inventory = []
            inventory += startingInventory

            # graph = randomizer.master_locations.location_graph

            location_requirements = []
            for loc in graph.node_data("Starting").locations:
                location_requirements.append((loc,[]))


            # updated function to allow for multiple incoming connections to enforce multiple constraints
            def get_all_parent_edge_reqs(n,reqs = None):
                if reqs is None:
                    reqs = []
                all_edges = graph.inc_edges(n)
                for e in all_edges:
                    data = graph.edge_data(e)
                    source,_ = graph.edge_by_id(e)
                    reqs += [data.requirement]
                    get_all_parent_edge_reqs(source,reqs)
                return reqs

            for node in graph.node_list():
                reqs = get_all_parent_edge_reqs(node)
                for loc in graph.node_data(node).locations:
                    location_requirements.append((loc,reqs))



            # def dfs_search(node_name,reqs):
            #     out_edges = graph.out_edges(node_name)
            #     for e in out_edges:
            #         data = graph.edge_data(e)
            #         _,target = graph.edge_by_id(e)
            #         req_for_target = data.requirement
            #         new_reqs = reqs + [req_for_target]
            #         for loc in graph.node_data(target).locations:
            #             location_requirements.append((loc,new_reqs))
            #         dfs_search(target,new_reqs)

            # dfs_search("Starting",[])

            changed = True
            depth = 0
            while changed:
                depth+=1
                if len(location_requirements)==0:
                    if verbose:
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
            
            if verbose:
                print("Failed seed, trying again")
            # for loc in location_requirements:
            #     print(loc[0].Description)
            #     for assignment in randomizer.assignedItems:
            #         if loc[0] == assignment.location:
            #             print(f"---{assignment.item.Name}")
            raise ValidationException(f"Completion checking failed to collect {len(location_requirements)} items")

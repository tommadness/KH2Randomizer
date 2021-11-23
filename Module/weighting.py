

from math import ceil
from Class.itemClass import KH2Item, itemRarity
from Class.newLocationClass import KH2Location
from List.NewLocationList import Locations
from Module.RandomizerSettings import RandomizerSettings


class WeightDistributions():
    def __init__(self,max_depth):
        self.weighting_function = {}
        self.weighting_function["Normal"] = {}
        for rarity in itemRarity:
            self.weighting_function["Normal"][rarity] = [1]*(max_depth+1)

        for diff_index,difficulty in enumerate(["Super Easy","Easy"]):
            self.weighting_function[difficulty] = {}
            self.weighting_function[difficulty][itemRarity.COMMON] = [1]*(max_depth+1)
            self.weighting_function[difficulty][itemRarity.UNCOMMON] = [ceil(3.0/pow(x/(max_depth/5.0),2.0-diff_index)) for x in range(1,max_depth+2)]
            self.weighting_function[difficulty][itemRarity.RARE] = [ceil(10.0/pow(x/(max_depth/5.0),2.0-diff_index)) for x in range(1,max_depth+2)]
            self.weighting_function[difficulty][itemRarity.MYTHIC] = [ceil(30.0/pow(x/(max_depth/5.0),2.0-diff_index)) for x in range(1,max_depth+2)]

        for diff_index,difficulty in enumerate(["Hard","Very Hard","Insane","Nightmare"]):
            self.weighting_function[difficulty] = {}
            self.weighting_function[difficulty][itemRarity.COMMON] =  [ceil(10.0/pow(x/(max_depth/3.0),diff_index*.5+1)) for x in range(1,max_depth+2)]
            self.weighting_function[difficulty][itemRarity.UNCOMMON] = [ceil(3.0/pow(x/(max_depth/3.0),diff_index*.5+1)) for x in range(1,max_depth+2)]
            self.weighting_function[difficulty][itemRarity.RARE] = [ceil(3.0/pow((max_depth+2-x)/(max_depth/3.0),diff_index*.5+1)) for x in range(1,max_depth+2)]
            self.weighting_function[difficulty][itemRarity.MYTHIC] = [ceil(15.0/pow((max_depth+2-x)/(max_depth/3.0),diff_index*.5+1)) for x in range(1,max_depth+2)]

    def getRarityWeighting(self,difficulty):
        if difficulty not in self.weighting_function:
            raise ValueError(f"Unknown item placement difficulty {difficulty}")
        return self.weighting_function[difficulty]


class LocationWeights():
    def __init__(self,settings:RandomizerSettings,locations : Locations):
        location_graph = locations.location_graph
        hops = location_graph.get_hops("Starting")
        self.location_depths = {}
        max_hops = 0

        for hop in hops:
            max_hops = max(max_hops,hop[1])
            for loc in location_graph.node_data(hop[0]).locations:
                self.location_depths[loc] = hop[1]
        
        self.weights = WeightDistributions(max_hops).getRarityWeighting(settings.itemPlacementDifficulty)

    def getWeight(self,item: KH2Item, loc: KH2Location):
        return self.weights[item.Rarity][self.location_depths[loc]]

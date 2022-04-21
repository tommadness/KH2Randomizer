from math import ceil,floor,fmod
from Class.itemClass import KH2Item, itemRarity
from Class.newLocationClass import KH2Location
from List.LvupStats import DreamWeaponOffsets
from List.NewLocationList import Locations
from List.configDict import locationCategory
from Module.RandomizerSettings import RandomizerSettings


class WeightDistributions():
    def __init__(self,max_depth):
        self.weighting_function = {}
        self.weighting_function["Normal"] = {}
        for rarity in itemRarity:
            self.weighting_function["Normal"][rarity] = [1]*(max_depth+1)

        for diff_index,difficulty in enumerate(["Super Easy","Easy"]):
            diff_index_modded = (1-diff_index)-0.25
            self.weighting_function[difficulty] = {}
            self.weighting_function[difficulty][itemRarity.COMMON] = [max(1,floor(10.0/pow(x/(max_depth/3.0),diff_index_modded*.5+1))) for x in range(max_depth+1,0,-1)]
            self.weighting_function[difficulty][itemRarity.UNCOMMON] = [max(1,floor(3.0/pow(x/(max_depth/3.0),diff_index_modded*.5+1))) for x in range(max_depth+1,0,-1)]
            self.weighting_function[difficulty][itemRarity.RARE] = [max(1,floor(3.0/pow((max_depth+2-x)/(max_depth/3.0),diff_index_modded*.5+1))) for x in range(max_depth+1,0,-1)]
            self.weighting_function[difficulty][itemRarity.MYTHIC] = [max(1,floor(10.0/pow((max_depth+2-x)/(max_depth/3.0),diff_index_modded*.5+1))) for x in range(max_depth+1,0,-1)]

        for diff_index,difficulty in enumerate(["Hard","Very Hard","Insane","Nightmare"]):
            diff_index_modded = diff_index-0.25
            self.weighting_function[difficulty] = {}
            self.weighting_function[difficulty][itemRarity.COMMON] =  [max(1,floor(10.0/pow(x/(max_depth/3.0),diff_index_modded*.5+1))) for x in range(1,max_depth+2)]
            self.weighting_function[difficulty][itemRarity.UNCOMMON] = [max(1,floor(3.0/pow(x/(max_depth/3.0),diff_index_modded*.5+1))) for x in range(1,max_depth+2)]
            self.weighting_function[difficulty][itemRarity.RARE] = [max(1,floor(3.0/pow((max_depth+2-x)/(max_depth/3.0),diff_index_modded*.5+1))) for x in range(1,max_depth+2)]
            self.weighting_function[difficulty][itemRarity.MYTHIC] = [max(1,floor(10.0/pow((max_depth+2-x)/(max_depth/3.0),diff_index_modded*.5+1))) for x in range(1,max_depth+2)]

        # for diff_index,difficulty in enumerate(["Super Easy","Easy","Hard","Very Hard","Insane","Nightmare"]):
        #     print(self.weighting_function[difficulty][itemRarity.COMMON])
        #     print(self.weighting_function[difficulty][itemRarity.UNCOMMON])
        #     print(self.weighting_function[difficulty][itemRarity.RARE])
        #     print(self.weighting_function[difficulty][itemRarity.MYTHIC])
        #     print("--------------------")

    def getRarityWeighting(self,difficulty):
        if difficulty not in self.weighting_function:
            raise ValueError(f"Unknown item placement difficulty {difficulty}")
        return self.weighting_function[difficulty]


class LocationWeights():
    def __init__(self,settings:RandomizerSettings,locations : Locations, reverse_locations : Locations):
        self.regular_rando = settings.regular_rando
        self.reverse_rando = settings.reverse_rando
        
        location_graph = locations.location_graph
        reverse_location_graph = reverse_locations.location_graph


        self.split_levels = settings.split_levels
        self.level_offsets = DreamWeaponOffsets()
        self.max_level = settings.level_checks
        self.level_depths = {}


        # Regular
        # -------------------------------
        hops = location_graph.get_hops("Starting")
        self.location_depths = {}
        self.location_type_maxes = {}
        max_hops = 17 # hard coding max hops to unify depths between reverse and regular rando
        # for hop in hops:
        #     max_hops = max(max_hops,hop[1])
        for hop in hops:
            for loc in location_graph.node_data(hop[0]).locations:
                if loc.LocationTypes[0] not in self.location_type_maxes:
                    self.location_type_maxes[loc.LocationTypes[0]] = hop[1]
                else:
                    self.location_type_maxes[loc.LocationTypes[0]] = max(hop[1],self.location_type_maxes[loc.LocationTypes[0]])


        for hop in hops:
            for loc in location_graph.node_data(hop[0]).locations:
                if self.location_type_maxes[loc.LocationTypes[0]] != 0:
                    scaled_depth = floor((hop[1]*1.0/self.location_type_maxes[loc.LocationTypes[0]])*max_hops)
                else:
                    scaled_depth = hop[1]
                self.location_depths[loc] = scaled_depth
                if loc.LocationCategory is locationCategory.LEVEL:
                    self.level_depths[loc.LocationId] = scaled_depth
        
        self.weights = WeightDistributions(max_hops).getRarityWeighting(settings.itemPlacementDifficulty)

        # Reverse
        # -------------------------------
        hops = reverse_location_graph.get_hops("Starting")
        self.reverse_location_depths = {}
        self.reverse_location_type_maxes = {}
        # max_hops = 0
        # for hop in hops:
        #     max_hops = max(max_hops,hop[1])
        for hop in hops:
            for loc in reverse_location_graph.node_data(hop[0]).locations:
                if loc.LocationTypes[0] not in self.reverse_location_type_maxes:
                    self.reverse_location_type_maxes[loc.LocationTypes[0]] = hop[1]
                else:
                    self.reverse_location_type_maxes[loc.LocationTypes[0]] = max(hop[1],self.reverse_location_type_maxes[loc.LocationTypes[0]])


        for hop in hops:
            for loc in reverse_location_graph.node_data(hop[0]).locations:
                if self.reverse_location_type_maxes[loc.LocationTypes[0]] != 0:
                    scaled_depth = floor((hop[1]*1.0/self.reverse_location_type_maxes[loc.LocationTypes[0]])*max_hops)
                else:
                    scaled_depth = hop[1]
                self.reverse_location_depths[loc] = scaled_depth
        
        self.reverse_weights = WeightDistributions(max_hops).getRarityWeighting(settings.itemPlacementDifficulty)


    def getWeight(self,rarity: itemRarity, depth: int):
        return self.weights[rarity][depth]

    def getDepth(self,loc: KH2Location):
        if loc.LocationCategory is not locationCategory.LEVEL or not self.split_levels:
            if self.regular_rando and self.reverse_rando:
                return (self.location_depths[loc], self.reverse_location_depths[loc])
            elif self.regular_rando:
                return self.location_depths[loc]
            else:
                return self.location_depths[loc]
        else:
            assert self.location_depths[loc] == self.level_depths[loc.LocationId]
            sword_depth = self.level_depths[loc.LocationId]
            shield_depth = self.level_depths[self.level_offsets.get_shield_level(self.max_level,loc.LocationId)]
            staff_depth = self.level_depths[self.level_offsets.get_staff_level(self.max_level,loc.LocationId)]
            return (sword_depth+shield_depth+staff_depth)//3


    def getWeight(self,item: KH2Item, loc: KH2Location):
        if loc.LocationCategory is not locationCategory.LEVEL or not self.split_levels:
            if self.regular_rando and self.reverse_rando:
                return (self.weights[item.Rarity][self.location_depths[loc]] + self.reverse_weights[item.Rarity][self.reverse_location_depths[loc]])//2
            elif self.regular_rando:
                return self.weights[item.Rarity][self.reverse_location_depths[loc]]
            else:
                return self.reverse_weights[item.Rarity][self.location_depths[loc]]
        else:
            assert self.location_depths[loc] == self.level_depths[loc.LocationId]
            sword_depth = self.level_depths[loc.LocationId]
            shield_depth = self.level_depths[self.level_offsets.get_shield_level(self.max_level,loc.LocationId)]
            staff_depth = self.level_depths[self.level_offsets.get_staff_level(self.max_level,loc.LocationId)]
            return self.weights[item.Rarity][(sword_depth+shield_depth+staff_depth)//3]

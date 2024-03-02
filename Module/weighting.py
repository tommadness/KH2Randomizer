from math import ceil, floor
from typing import Union

from Class.newLocationClass import KH2Location
from List.LvupStats import DreamWeaponOffsets
from List.NewLocationList import Locations
from List.configDict import itemType, locationCategory, itemRarity, locationDepth, locationType, itemBias, itemDifficulty
from List.location.graph import START_NODE
from Module.RandomizerSettings import RandomizerSettings




class SimplifiedWeightDistributions:
    def __init__(self, max_depth: int):
        self.weighting_function: dict[itemBias, list[int]] = {}

        weight_list_maker = lambda function_index : [
                    max(1, floor(10.0 / pow((max_depth + 2 - x) / (max_depth / 3.0), function_index * .5 + 1)))
                    for x in range(1, max_depth + 2)
                ]

        self.weighting_function[itemBias.VERY_EARLY]  = weight_list_maker(1)[::-1]
        self.weighting_function[itemBias.EARLY]  = weight_list_maker(0)[::-1]
        self.weighting_function[itemBias.SLIGHTLY_EARLY] = [2] * floor((max_depth + 1) / 2) + [1] * ceil((max_depth + 1) / 2)
        self.weighting_function[itemBias.NOBIAS] = [1] * (max_depth + 1)
        self.weighting_function[itemBias.SLIGHTLY_LATE] = [1] * floor((max_depth + 1) / 2) + [2] * ceil((max_depth + 1) / 2)
        self.weighting_function[itemBias.LATE]  = weight_list_maker(0)
        self.weighting_function[itemBias.VERY_LATE]  = weight_list_maker(1)
        self.weighting_function[itemBias.SUPER_LATE]  = weight_list_maker(2)
        self.weighting_function[itemBias.NIGHTMARE]  = weight_list_maker(3)

    
    def get_rarity_weightings(self):
        return self.weighting_function

class WeightDistributions:

    def __init__(self, max_depth: int):
        self.weighting_function: dict[itemDifficulty, dict[itemRarity, list[int]]] = {
            itemDifficulty.NORMAL: {}
        }
        for rarity in itemRarity:
            self.weighting_function[itemDifficulty.NORMAL][itemRarity(rarity)] = [1] * (max_depth + 1)

        self.weighting_function[itemDifficulty.SLIGHTLY_HARD] = {
            itemRarity.COMMON: [1] * (max_depth + 1),
            itemRarity.UNCOMMON: [1] * (max_depth + 1),
            itemRarity.RARE: [1] * floor((max_depth + 1) / 2) + [2] * ceil((max_depth + 1) / 2),
            itemRarity.MYTHIC: [1] * floor((max_depth + 1) / 2) + [2] * ceil((max_depth + 1) / 2)
        }
        self.weighting_function[itemDifficulty.SLIGHTLY_EASY] = {
            itemRarity.COMMON: [1] * (max_depth + 1),
            itemRarity.UNCOMMON: [1] * (max_depth + 1),
            itemRarity.RARE: [2] * floor((max_depth + 1) / 2) + [1] * ceil((max_depth + 1) / 2),
            itemRarity.MYTHIC: [2] * floor((max_depth + 1) / 2) + [1] * ceil((max_depth + 1) / 2)
        }

        easier_difficulties = [
            itemDifficulty.SUPEREASY,
            itemDifficulty.EASY
        ]
        for diff_index, difficulty in enumerate(easier_difficulties):
            diff_index_modded = (1 - diff_index) - 0.25
            self.weighting_function[difficulty] = {
                itemRarity.COMMON: [
                    max(1, floor(10.0 / pow(x / (max_depth / 3.0), diff_index_modded * .5 + 1)))
                    for x in range(max_depth + 1, 0, -1)
                ],
                itemRarity.UNCOMMON: [
                    max(1, floor(3.0 / pow(x / (max_depth / 3.0), diff_index_modded * .5 + 1)))
                    for x in range(max_depth + 1, 0, -1)
                ],
                itemRarity.RARE: [
                    max(1, floor(3.0 / pow((max_depth + 2 - x) / (max_depth / 3.0), diff_index_modded * .5 + 1)))
                    for x in range(max_depth + 1, 0, -1)],
                itemRarity.MYTHIC: [
                    max(1, floor(10.0 / pow((max_depth + 2 - x) / (max_depth / 3.0), diff_index_modded * .5 + 1)))
                    for x in range(max_depth + 1, 0, -1)
                ]
            }

        harder_difficulties = [
            itemDifficulty.HARD,
            itemDifficulty.VERYHARD,
            itemDifficulty.INSANE,
            itemDifficulty.NIGHTMARE
        ]
        for diff_index, difficulty in enumerate(harder_difficulties):
            diff_index_modded = diff_index - 0.25
            self.weighting_function[difficulty] = {
                itemRarity.COMMON: [
                    max(1, floor(10.0 / pow(x / (max_depth / 3.0), diff_index_modded * .5 + 1)))
                    for x in range(1, max_depth + 2)
                ],
                itemRarity.UNCOMMON: [
                    max(1, floor(3.0 / pow(x / (max_depth / 3.0), diff_index_modded * .5 + 1)))
                    for x in range(1, max_depth + 2)
                ],
                itemRarity.RARE: [
                    max(1, floor(3.0 / pow((max_depth + 2 - x) / (max_depth / 3.0), diff_index_modded * .5 + 1)))
                    for x in range(1, max_depth + 2)],
                itemRarity.MYTHIC: [
                    max(1, floor(10.0 / pow((max_depth + 2 - x) / (max_depth / 3.0), diff_index_modded * .5 + 1)))
                    for x in range(1, max_depth + 2)
                ]
            }

        # for diff_index,difficulty in enumerate(["Super Easy","Easy","Hard","Very Hard","Insane","Nightmare"]):
        #     print(self.weighting_function[difficulty][itemRarity.COMMON])
        #     print(self.weighting_function[difficulty][itemRarity.UNCOMMON])
        #     print(self.weighting_function[difficulty][itemRarity.RARE])
        #     print(self.weighting_function[difficulty][itemRarity.MYTHIC])
        #     print("--------------------")

    def get_rarity_weighting(self, difficulty: itemDifficulty):
        if difficulty not in self.weighting_function:
            raise ValueError(f"Unknown item placement difficulty {difficulty}")
        return self.weighting_function[difficulty]


class LocationWeights:

    def __init__(self, settings: RandomizerSettings, locations: Locations, reverse_locations: Locations):
        self.regular_rando = settings.regular_rando
        self.reverse_rando = settings.reverse_rando
        self.split_levels = settings.split_levels
        self.level_offsets = DreamWeaponOffsets()
        self.max_level = settings.max_level_checks
        self.level_depths: dict[int, int] = {}

        # Regular
        # -------------------------------
        self.location_depths: dict[KH2Location, int] = {}
        hops = locations.location_graph.get_hops(START_NODE)
        location_type_maxes: dict[locationType, int] = {}
        max_hops = 17  # hard coding max hops to unify depths between reverse and regular rando
        # for hop in hops:
        #     max_hops = max(max_hops,hop[1])
        for node, distance in hops:
            for loc in locations.locations_for_node(node):
                primary_type = loc.LocationTypes[0]
                if primary_type not in location_type_maxes:
                    location_type_maxes[primary_type] = distance
                else:
                    location_type_maxes[primary_type] = max(distance, location_type_maxes[primary_type])

        for node, distance in hops:
            for loc in locations.locations_for_node(node):
                primary_type = loc.LocationTypes[0]
                if location_type_maxes[primary_type] != 0:
                    scaled_depth = floor((distance * 1.0 / location_type_maxes[primary_type]) * max_hops)
                else:
                    scaled_depth = distance
                self.location_depths[loc] = scaled_depth
                if loc.LocationCategory is locationCategory.LEVEL:
                    self.level_depths[loc.LocationId] = scaled_depth

        # Reverse
        # -------------------------------
        self.reverse_location_depths: dict[KH2Location, int] = {}
        hops = reverse_locations.location_graph.get_hops(START_NODE)
        reverse_location_type_maxes: dict[locationType, int] = {}
        # max_hops = 0
        # for hop in hops:
        #     max_hops = max(max_hops,hop[1])
        for node, distance in hops:
            for loc in reverse_locations.locations_for_node(node):
                primary_type = loc.LocationTypes[0]
                if primary_type not in reverse_location_type_maxes:
                    reverse_location_type_maxes[primary_type] = distance
                else:
                    reverse_location_type_maxes[primary_type] = max(distance, reverse_location_type_maxes[primary_type])

        for node, distance in hops:
            for loc in reverse_locations.locations_for_node(node):
                primary_type = loc.LocationTypes[0]
                if reverse_location_type_maxes[primary_type] != 0:
                    scaled_depth = floor((distance * 1.0 / reverse_location_type_maxes[primary_type]) * max_hops)
                else:
                    scaled_depth = distance
                self.reverse_location_depths[loc] = scaled_depth

                
        self.base_weights = SimplifiedWeightDistributions(max_hops).get_rarity_weightings()
        self.weights = {}
        # default to normal weighting
        for item_type in itemType:
            self.weights[item_type] = self.base_weights[itemBias.NOBIAS]

        self.weights[itemType.FORM] = self.base_weights[settings.form_weights]
        self.weights[itemType.STORYUNLOCK] = self.base_weights[settings.unlock_weights]

        self.weights[itemType.FIRE] = self.base_weights[settings.magic_weights]
        self.weights[itemType.BLIZZARD] = self.base_weights[settings.magic_weights]
        self.weights[itemType.THUNDER] = self.base_weights[settings.magic_weights]
        self.weights[itemType.CURE] = self.base_weights[settings.magic_weights]
        self.weights[itemType.MAGNET] = self.base_weights[settings.magic_weights]
        self.weights[itemType.REFLECT] = self.base_weights[settings.magic_weights]

        self.weights[itemType.TORN_PAGE] = self.base_weights[settings.page_weights]

        self.weights[itemType.SUMMON] = self.base_weights[settings.summon_weights]

        self.weights[itemType.PROOF_OF_PEACE] = self.base_weights[settings.proof_weights]
        self.weights[itemType.PROOF_OF_CONNECTION] = self.base_weights[settings.proof_weights]
        self.weights[itemType.PROOF_OF_NONEXISTENCE] = self.base_weights[settings.proof_weights]

        self.weights[itemType.PROMISE_CHARM] = self.base_weights[settings.promise_charm_weights]

    def get_depth(self, location: KH2Location) -> Union[int, tuple[int, int]]:
        """
        Returns either a single depth (for levels or regular or reverse rando) or a tuple of
        (regular depth, reverse depth) if both regular and reverse rando.
        """
        if location.LocationCategory is locationCategory.LEVEL:
            loc_id = location.LocationId
            if self.split_levels:
                sword_depth = self.level_depths[loc_id]
                shield_depth = self.level_depths[self.level_offsets.get_shield_level(self.max_level, loc_id)]
                staff_depth = self.level_depths[self.level_offsets.get_staff_level(self.max_level, loc_id)]
                return (sword_depth + shield_depth + staff_depth) // 3
            else:
                return self.level_depths[loc_id]
        else:
            if self.regular_rando and self.reverse_rando:
                return self.location_depths[location], self.reverse_location_depths[location]
            elif self.regular_rando:
                return self.location_depths[location]
            else:
                return self.reverse_location_depths[location]

    def get_weight(self, rarity: itemRarity, location: KH2Location) -> int:
        raise AssertionError("Deprecated weighting function")
        """ Returns the weight that should be used for an item of the given rarity at the given location. """
        depth_or_depths = self.get_depth(location)
        rarity_weights = self.weights[rarity]
        if isinstance(depth_or_depths, int):
            return rarity_weights[depth_or_depths]
        elif isinstance(depth_or_depths, tuple):
            regular_weight = rarity_weights[depth_or_depths[0]]
            reverse_weight = rarity_weights[depth_or_depths[1]]
            return (regular_weight + reverse_weight) // 2
        

    def get_weight(self, item_type: itemType, location: KH2Location) -> int:
        """ Returns the weight that should be used for an item of the given type at the given location. """
        depth_or_depths = self.get_depth(location)
        rarity_weights = self.weights[item_type]
        if isinstance(depth_or_depths, int):
            return rarity_weights[depth_or_depths]
        elif isinstance(depth_or_depths, tuple):
            regular_weight = rarity_weights[depth_or_depths[0]]
            reverse_weight = rarity_weights[depth_or_depths[1]]
            return (regular_weight + reverse_weight) // 2

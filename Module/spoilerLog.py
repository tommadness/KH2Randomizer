from typing import Optional

from Class.itemClass import KH2Item
from List.configDict import locationType
from Module.newRandomize import ItemAssignment, SynthesisRecipe, WeaponStats
from Module.weighting import LocationWeights



def itemSpoilerDictionary(locationItems, shop_items: Optional[list[KH2Item]] = None, weights: LocationWeights = None, unreachable_locations = None):
    outDict = {}

    if shop_items is not None:
        shop_spoiler = []
        for shop_item in shop_items:
            shop_spoiler.append(("Moogle Shop", shop_item))
        if len(shop_spoiler) > 0:
            outDict[locationType.SHOP] = shop_spoiler

    for assignment in locationItems:
        location = assignment.location
        if weights and location in weights.location_depths:
            added_string = f" <{weights.getDepth(location)}>"
        else:
            added_string = ""

        if unreachable_locations and location in unreachable_locations:
            prepend_string = "Unreachable "
        else:
            prepend_string = ""


        item = assignment.item
        item2 = assignment.item2
        if not location.LocationTypes == []:
            if not location.LocationTypes[0] in outDict.keys():
                outDict[location.LocationTypes[0]] = []
            outDict[location.LocationTypes[0]].append((prepend_string+location.Description+added_string,item))
            if item2 is not None:
                outDict[location.LocationTypes[0]].append((prepend_string+location.Description+added_string,item2))
    return outDict

def levelStatsDictionary(level_stats):
    outDict = {}
    for lvl in level_stats:
        desc = lvl.location.Description
        split_desc=desc.split(' ')
        if len(split_desc) > 2:
            desc = split_desc[0] + " " +split_desc[2]
        outDict[desc] = {"experience":lvl.experience,"strength":lvl.strength, "magic": lvl.magic, "defense": lvl.defense, "ap":lvl.ap }
    return outDict


def synth_recipe_dictionary(assignments: list[ItemAssignment], recipes: list[SynthesisRecipe]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []

    sorted_recipes = [r for r in recipes]
    sorted_recipes.sort(key=lambda r: r.location.LocationId)

    for recipe in sorted_recipes:
        location = recipe.location
        synth_assignment = next(a for a in assignments if a.location == location)
        requirement_strings = []
        for requirement in recipe.requirements:
            requirement_strings.append(" x".join([requirement.synth_item.Name, f"{requirement.amount}"]))
        result.append({
            "location": location.Description,
            "item": synth_assignment.item.Name,
            "requirements": ", ".join(requirement_strings)
        })

    return result


def weapon_stats_dictionary(
        sora_assignments: list[ItemAssignment],
        donald_assignments: list[ItemAssignment],
        goofy_assignments: list[ItemAssignment],
        weapons: list[WeaponStats]
) -> list[dict[str, str]]:
    all_assignments = sora_assignments + donald_assignments + goofy_assignments

    result: list[dict[str, str]] = []
    for weapon in weapons:
        location = weapon.location
        assignment = next(a for a in all_assignments if a.location == location)
        result.append({
            "name": location.Description.partition(" (Slot)")[0],
            "strength": weapon.strength,
            "magic": weapon.magic,
            "item": assignment.item.Name
        })
    return result

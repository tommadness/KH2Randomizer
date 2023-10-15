from typing import Optional

from Class.itemClass import KH2Item
from List.ItemList import Items
from List.configDict import locationType
from List.inventory import misc
from Module.newRandomize import ItemAssignment, SynthesisRecipe, WeaponStats
from Module.weighting import LocationWeights


def item_spoiler_dictionary(
        item_assignments: list[ItemAssignment],
        starting_inventory_ids: Optional[list[int]] = None,
        shop_items: Optional[list[KH2Item]] = None,
        weights: LocationWeights = None,
        unreachable_locations=None
) -> dict[locationType, list[tuple[str, KH2Item]]]:
    # (depth for sort purposes, location id for sort purposes, spoiler log string, item)
    out_dict: dict[locationType, list[tuple[int, int, str, KH2Item]]] = {}

    item_lookup = Items.sora_lookup_table()
    if starting_inventory_ids is not None:
        item_spoiler = []
        for index, starting_item_id in enumerate(starting_inventory_ids):
            item = item_lookup.get(starting_item_id)
            if item is not None:
                item_spoiler.append((0, index, "Sora Starting Item", item))
            else:
                print(f"Could not find item with id {starting_item_id} to add to the spoiler log")
        if len(item_spoiler) > 0:
            out_dict[locationType.Free] = item_spoiler

    if shop_items is not None:
        shop_spoiler = []
        for shop_item in shop_items:
            shop_spoiler.append((0, 0, "Moogle Shop", shop_item))
        if len(shop_spoiler) > 0:
            out_dict[locationType.SHOP] = shop_spoiler

    for assignment in item_assignments:
        location = assignment.location
        loc_id = location.LocationId

        sort_depth = 0
        if weights and location in weights.location_depths:
            depth = weights.get_depth(location)
            added_string = f" <{depth}>"
            if isinstance(depth, int):
                sort_depth = depth
            elif isinstance(depth, tuple):
                sort_depth = depth[0]
        else:
            added_string = ""

        if unreachable_locations and location in unreachable_locations:
            prepend_string = "Unreachable "
        else:
            prepend_string = ""

        spoiler_string = prepend_string + location.Description + added_string

        if len(location.LocationTypes) > 0:
            location_type = location.LocationTypes[0]
            if location_type not in out_dict:
                out_dict[location_type] = []
            if assignment.item.item != misc.NullItem:
                out_dict[location_type].append((sort_depth, loc_id, spoiler_string, assignment.item))
            if assignment.item2 is not None:
                out_dict[location_type].append((sort_depth, loc_id, spoiler_string, assignment.item2))

    result_dict: dict[locationType, list[tuple[str, KH2Item]]] = {}
    for location_type, entries in out_dict.items():
        # Sort first by the location ID (this will be the tiebreaker)
        entries.sort(key=lambda entry: entry[1])
        # Now sort by the depth
        entries.sort(key=lambda entry: entry[0])
        result_dict[location_type] = [(entry[2], entry[3]) for entry in entries]

    return result_dict


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

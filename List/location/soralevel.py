from typing import Optional

from Class.newLocationClass import KH2Location
from List.LvupStats import DreamWeaponOffsets
from List.configDict import locationCategory, locationType
from List.inventory import ability
from List.inventory.item import InventoryItem
from List.location.graph import LocationGraphBuilder, START_NODE


def level_reward(level: int, description: str, vanilla: Optional[InventoryItem]) -> KH2Location:
    vanilla_items: list[int] = []
    if vanilla is not None:
        vanilla_items.append(vanilla.id)
    return KH2Location(level, description, locationCategory.LEVEL, [locationType.Level], VanillaItems=vanilla_items)


def make_graph(graph: LocationGraphBuilder):
    settings = graph.settings
    max_level = settings.max_level_checks

    vanilla_levels: dict[int, dict[int, InventoryItem]] = {
        50: {
            2: ability.ComboBoost,
            4: ability.ExperienceBoost,
            7: ability.MagicLockOn,
            9: ability.ReactionBoost,
            10: ability.ItemBoost,
            12: ability.LeafBracer,
            14: ability.FireBoost,
            15: ability.DriveBoost,
            17: ability.Draw,
            20: ability.CombinationBoost,
            23: ability.DamageDrive,
            25: ability.AirComboBoost,
            28: ability.BlizzardBoost,
            30: ability.DriveConverter,
            32: ability.NegativeCombo,
            34: ability.OnceMore,
            36: ability.FinishingPlus,
            39: ability.ThunderBoost,
            41: ability.Defender,
            44: ability.BerserkCharge,
            46: ability.Jackpot,
            48: ability.SecondChance,
            50: ability.DamageControl
        },
        99: {
            7: ability.ComboBoost,
            9: ability.ExperienceBoost,
            12: ability.MagicLockOn,
            15: ability.ReactionBoost,
            17: ability.ItemBoost,
            20: ability.LeafBracer,
            23: ability.FireBoost,
            25: ability.DriveBoost,
            28: ability.Draw,
            31: ability.CombinationBoost,
            33: ability.DamageDrive,
            36: ability.AirComboBoost,
            39: ability.BlizzardBoost,
            41: ability.DriveConverter,
            44: ability.NegativeCombo,
            47: ability.OnceMore,
            49: ability.FinishingPlus,
            53: ability.ThunderBoost,
            59: ability.Defender,
            65: ability.BerserkCharge,
            73: ability.Jackpot,
            85: ability.SecondChance,
            99: ability.DamageControl
        }
    }

    node_index = 0
    locations: list[str] = []
    current_location_list: list[KH2Location] = []

    double_level_reward = False
    level_offsets = DreamWeaponOffsets()
    excluded_levels = settings.excluded_levels()
    for level in range(1, 100):
        level_description = f"Level {level}"

        if settings.split_levels:
            shield = level_offsets.get_shield_level(max_level, level)
            staff = level_offsets.get_staff_level(max_level, level)
            if shield and staff:
                level_description = f"Level Sw: {level} Sh: {shield} St: {staff}"

        vanilla_item: Optional[InventoryItem] = None
        if max_level in vanilla_levels and level in vanilla_levels[max_level]:
            vanilla_item = vanilla_levels[max_level][level]
        elif level in vanilla_levels[99]:
            vanilla_item = vanilla_levels[99][level]

        current_location_list.append(level_reward(level, level_description, vanilla_item))

        if level not in excluded_levels:
            if double_level_reward:
                locations.append(graph.add_location(f"LevelGroup-{node_index}", current_location_list))
                current_location_list = []
                node_index += 1
                double_level_reward = False
            else:
                double_level_reward = True

    # Add in the last group if there are any stragglers
    if len(current_location_list) > 0:
        locations.append(graph.add_location(f"LevelGroup-{node_index}", current_location_list))

    for index, location in enumerate(locations):
        if index == 0:
            graph.add_edge(START_NODE, location)
        else:
            graph.add_edge(locations[index - 1], location)

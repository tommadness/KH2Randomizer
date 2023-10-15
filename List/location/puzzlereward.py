from enum import Enum

from Class.newLocationClass import KH2Location
from List.configDict import locationType, locationCategory, itemType
from List.location.graph import RequirementEdge, LocationGraphBuilder, START_NODE
from Module.itemPlacementRestriction import ItemPlacementHelpers


class NodeId(str, Enum):
    AwakeningPuzzle = "Awakening Puzzle"
    HeartPuzzle = "Heart Puzzle"
    DualityPuzzle = "Duality Puzzle"
    FrontierPuzzle = "Frontier Puzzle"
    DaylightPuzzle = "Daylight Puzzle"
    SunsetPuzzle = "Sunset Puzzle"


class CheckLocation(str, Enum):
    AwakeningApBoost = "Awakening (AP Boost)"
    HeartSerenityCrystal = "Heart (Serenity Crystal)"
    DualityRareDocument = "Duality (Rare Document)"
    FrontierManifestIllusion = "Frontier (Manifest Illusion)"
    DaylightExecutivesRing = "Daylight (Executive's Ring)"
    SunsetGrandRibbon = "Sunset (Grand Ribbon)"


def puzzle_reward(loc_id: int, description: str, invalid_checks: list[itemType]) -> KH2Location:
    return KH2Location(
        LocationId=loc_id,
        Description=description,
        LocationCategory=locationCategory.CREATION,
        LocationTypes=[locationType.Puzzle],
        InvalidChecks=invalid_checks
    )


def make_graph(graph: LocationGraphBuilder):
    awakening = graph.add_location(NodeId.AwakeningPuzzle, [
        puzzle_reward(0, CheckLocation.AwakeningApBoost, invalid_checks=[itemType.REPORT]),
    ])
    heart = graph.add_location(NodeId.HeartPuzzle, [
        puzzle_reward(1, CheckLocation.HeartSerenityCrystal, invalid_checks=[itemType.REPORT]),
    ])
    duality = graph.add_location(NodeId.DualityPuzzle, [
        puzzle_reward(2, CheckLocation.DualityRareDocument, invalid_checks=[itemType.REPORT]),
    ])
    frontier = graph.add_location(NodeId.FrontierPuzzle, [
        puzzle_reward(3, CheckLocation.FrontierManifestIllusion, invalid_checks=[itemType.REPORT]),
    ])
    daylight = graph.add_location(NodeId.DaylightPuzzle, [
        puzzle_reward(4, CheckLocation.DaylightExecutivesRing, invalid_checks=[itemType.TORN_PAGE, itemType.REPORT]),
    ])
    sunset = graph.add_location(NodeId.SunsetPuzzle, [
        puzzle_reward(5, CheckLocation.SunsetGrandRibbon, invalid_checks=[itemType.REPORT]),
    ])

    if not graph.reverse_rando:
        graph.add_edge(START_NODE, awakening, RequirementEdge(req=ItemPlacementHelpers.need_growths))
        graph.add_edge(START_NODE, heart, RequirementEdge(req=ItemPlacementHelpers.need_growths))
        graph.add_edge(START_NODE, duality, RequirementEdge(req=ItemPlacementHelpers.need_growths))
        graph.add_edge(START_NODE, frontier, RequirementEdge(
            req=lambda inv: ItemPlacementHelpers.need_growths(inv) and ItemPlacementHelpers.tt2_check(
                inv) and ItemPlacementHelpers.hb_check(inv)))

        def daylight_checker(inv: list[int]) -> bool:
            return ItemPlacementHelpers.need_growths(inv) and \
                ItemPlacementHelpers.need_torn_pages(5)(inv) and \
                ItemPlacementHelpers.hb_check(inv) and \
                ItemPlacementHelpers.mulan_check(inv) and \
                ItemPlacementHelpers.tt3_check(inv) and \
                ItemPlacementHelpers.jack_pr_check(inv) and \
                ItemPlacementHelpers.aladdin_check(inv)

        def sunset_checker(inv: list[int]) -> bool:
            return ItemPlacementHelpers.need_growths(inv) and \
                ItemPlacementHelpers.hb_check(inv) and \
                ItemPlacementHelpers.tt3_check(inv) and \
                ItemPlacementHelpers.tron_check(inv) and \
                ItemPlacementHelpers.jack_pr_check(inv) and \
                ItemPlacementHelpers.aladdin_check(inv) and \
                ItemPlacementHelpers.beast_check(inv)

        graph.add_edge(START_NODE, daylight, RequirementEdge(req=daylight_checker))
        graph.add_edge(START_NODE, sunset, RequirementEdge(req=sunset_checker))
    else:
        def awakening_checker(inv: list[int]) -> bool:
            return ItemPlacementHelpers.need_growths(inv) and \
                ItemPlacementHelpers.beast_check(inv) and \
                ItemPlacementHelpers.tt3_check(inv)

        def heart_checker(inv: list[int]) -> bool:
            return ItemPlacementHelpers.need_growths(inv) and \
                ItemPlacementHelpers.auron_check(inv) and \
                ItemPlacementHelpers.jack_pr_check(inv)

        def duality_checker(inv: list[int]) -> bool:
            return ItemPlacementHelpers.need_growths(inv) and \
                ItemPlacementHelpers.jack_pr_check(inv) and \
                ItemPlacementHelpers.auron_check(inv)

        def frontier_checker(inv: list[int]) -> bool:
            return ItemPlacementHelpers.need_growths(inv) and \
                ItemPlacementHelpers.jack_pr_check(inv) and \
                ItemPlacementHelpers.aladdin_check(inv) and \
                ItemPlacementHelpers.need_fire_blizzard_thunder(inv)

        def daylight_checker(inv: list[int]) -> bool:
            return ItemPlacementHelpers.need_growths(inv) and \
                ItemPlacementHelpers.need_torn_pages(5)(inv) and \
                ItemPlacementHelpers.simba_check(inv) and \
                ItemPlacementHelpers.aladdin_check(inv) and \
                ItemPlacementHelpers.need_fire_blizzard_thunder(inv) and \
                ItemPlacementHelpers.hb_check(inv)

        def sunset_checker(inv: list[int]) -> bool:
            return ItemPlacementHelpers.need_growths(inv) and \
                ItemPlacementHelpers.hb_check(inv) and \
                ItemPlacementHelpers.tt3_check(inv) and \
                ItemPlacementHelpers.aladdin_check(inv) and \
                ItemPlacementHelpers.need_fire_blizzard_thunder(inv)

        graph.add_edge(START_NODE, awakening, RequirementEdge(req=awakening_checker))
        graph.add_edge(START_NODE, heart, RequirementEdge(req=heart_checker))
        graph.add_edge(START_NODE, duality, RequirementEdge(req=duality_checker))
        graph.add_edge(START_NODE, frontier, RequirementEdge(req=frontier_checker))
        graph.add_edge(START_NODE, daylight, RequirementEdge(req=daylight_checker))
        graph.add_edge(START_NODE, sunset, RequirementEdge(req=sunset_checker))

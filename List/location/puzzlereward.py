from enum import Enum

from Class.newLocationClass import KH2Location
from List.configDict import locationType, locationCategory, itemType
from List.location.graph import DefaultLogicGraph, RequirementEdge, LocationGraphBuilder, START_NODE
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

class PuzzleLogicGraph(DefaultLogicGraph):
    def __init__(self,reverse_rando,first_visit_locks):
        DefaultLogicGraph.__init__(self,NodeId)

        if not reverse_rando:
            def daylight_checker(inv: list[int]) -> bool:
                return (
                    ItemPlacementHelpers.need_growths(inv)
                    and ItemPlacementHelpers.need_torn_pages(5)(inv)
                    and ItemPlacementHelpers.hb2_check(inv)
                    and ItemPlacementHelpers.lod2_check(inv)
                    and ItemPlacementHelpers.tt3_check(inv)
                    and ItemPlacementHelpers.pr2_check(inv)
                    and ItemPlacementHelpers.ag2_check(inv)
                )

            def sunset_checker(inv: list[int]) -> bool:
                return (
                    ItemPlacementHelpers.need_growths(inv)
                    and ItemPlacementHelpers.hb2_check(inv)
                    and ItemPlacementHelpers.tt3_check(inv)
                    and ItemPlacementHelpers.sp2_check(inv)
                    and ItemPlacementHelpers.pr2_check(inv)
                    and ItemPlacementHelpers.ag2_check(inv)
                    and ItemPlacementHelpers.bc2_check(inv)
                )
            self.logic[START_NODE][NodeId.AwakeningPuzzle] = ItemPlacementHelpers.need_growths
            self.logic[START_NODE][NodeId.HeartPuzzle] = ItemPlacementHelpers.need_growths
            self.logic[START_NODE][NodeId.DualityPuzzle] = ItemPlacementHelpers.need_growths
            self.logic[START_NODE][NodeId.FrontierPuzzle] = lambda inv: ItemPlacementHelpers.need_growths(inv) and ItemPlacementHelpers.tt2_check(inv) and ItemPlacementHelpers.hb2_check(inv)
            self.logic[START_NODE][NodeId.DaylightPuzzle] = daylight_checker
            self.logic[START_NODE][NodeId.SunsetPuzzle] = sunset_checker
        else:
            def awakening_checker(inv: list[int]) -> bool:
                return (
                    ItemPlacementHelpers.need_growths(inv)
                    and ItemPlacementHelpers.bc2_check(inv)
                    and ItemPlacementHelpers.tt3_check(inv)
                )

            def heart_checker(inv: list[int]) -> bool:
                return (
                    ItemPlacementHelpers.need_growths(inv)
                    and ItemPlacementHelpers.oc2_check(inv)
                    and ItemPlacementHelpers.pr2_check(inv)
                )

            def duality_checker(inv: list[int]) -> bool:
                return (
                    ItemPlacementHelpers.need_growths(inv)
                    and ItemPlacementHelpers.pr2_check(inv)
                    and ItemPlacementHelpers.oc2_check(inv)
                )

            def frontier_checker(inv: list[int]) -> bool:
                return (
                    ItemPlacementHelpers.need_growths(inv)
                    and ItemPlacementHelpers.pr2_check(inv)
                    and ItemPlacementHelpers.ag2_check(inv)
                    and ItemPlacementHelpers.need_fire_blizzard_thunder(inv)
                )

            def daylight_checker(inv: list[int]) -> bool:
                return (
                    ItemPlacementHelpers.need_growths(inv)
                    and ItemPlacementHelpers.need_torn_pages(5)(inv)
                    and ItemPlacementHelpers.pl2_check(inv)
                    and ItemPlacementHelpers.ag2_check(inv)
                    and ItemPlacementHelpers.need_fire_blizzard_thunder(inv)
                    and ItemPlacementHelpers.hb2_check(inv)
                )

            def sunset_checker(inv: list[int]) -> bool:
                return (
                    ItemPlacementHelpers.need_growths(inv)
                    and ItemPlacementHelpers.hb2_check(inv)
                    and ItemPlacementHelpers.tt3_check(inv)
                    and ItemPlacementHelpers.ag2_check(inv)
                    and ItemPlacementHelpers.need_fire_blizzard_thunder(inv)
                )
            self.logic[START_NODE][NodeId.AwakeningPuzzle] = awakening_checker
            self.logic[START_NODE][NodeId.HeartPuzzle] = heart_checker
            self.logic[START_NODE][NodeId.DualityPuzzle] = duality_checker
            self.logic[START_NODE][NodeId.FrontierPuzzle] = frontier_checker
            self.logic[START_NODE][NodeId.DaylightPuzzle] = daylight_checker
            self.logic[START_NODE][NodeId.SunsetPuzzle] = sunset_checker

def puzzle_reward(
    loc_id: int, description: str, invalid_checks: list[itemType]
) -> KH2Location:
    return KH2Location(
        LocationId=loc_id,
        Description=description,
        LocationCategory=locationCategory.CREATION,
        LocationTypes=[locationType.Puzzle, locationType.Creations],
        InvalidChecks=invalid_checks,
    )


def make_graph(graph: LocationGraphBuilder):
    puzzle_logic = PuzzleLogicGraph(graph.reverse_rando,graph.first_visit_locks)
    graph.add_logic(puzzle_logic)
    awakening = graph.add_location(
        NodeId.AwakeningPuzzle,
        [
            puzzle_reward(
                0, CheckLocation.AwakeningApBoost, invalid_checks=[itemType.REPORT]
            ),
        ],
    )
    heart = graph.add_location(
        NodeId.HeartPuzzle,
        [
            puzzle_reward(
                1, CheckLocation.HeartSerenityCrystal, invalid_checks=[itemType.REPORT]
            ),
        ],
    )
    duality = graph.add_location(
        NodeId.DualityPuzzle,
        [
            puzzle_reward(
                2, CheckLocation.DualityRareDocument, invalid_checks=[itemType.REPORT]
            ),
        ],
    )
    frontier = graph.add_location(
        NodeId.FrontierPuzzle,
        [
            puzzle_reward(
                3,
                CheckLocation.FrontierManifestIllusion,
                invalid_checks=[itemType.REPORT],
            ),
        ],
    )
    daylight = graph.add_location(
        NodeId.DaylightPuzzle,
        [
            puzzle_reward(
                4,
                CheckLocation.DaylightExecutivesRing,
                invalid_checks=[itemType.TORN_PAGE, itemType.REPORT],
            ),
        ],
    )
    sunset = graph.add_location(
        NodeId.SunsetPuzzle,
        [
            puzzle_reward(
                5, CheckLocation.SunsetGrandRibbon, invalid_checks=[itemType.REPORT]
            ),
        ],
    )
    graph.add_edge(START_NODE, awakening)
    graph.add_edge(START_NODE, heart)
    graph.add_edge(START_NODE, duality)
    graph.add_edge(START_NODE, frontier)
    graph.add_edge(START_NODE, daylight)
    graph.add_edge(START_NODE, sunset)
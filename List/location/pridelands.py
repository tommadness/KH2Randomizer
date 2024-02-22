from enum import Enum

from List.configDict import locationType
from List.inventory import magic, keyblade, misc
from List.location.graph import DefaultLogicGraph, RequirementEdge, chest, popup, hybrid_bonus, stat_bonus, LocationGraphBuilder, \
    START_NODE
from Module.itemPlacementRestriction import ItemPlacementHelpers


class NodeId(str, Enum):
    Gorge = "Gorge"
    ElephantGraveyard = "Elephant Graveyard"
    PrideRock = "Pride Rock"
    WildebeestValley = "Wildebeest Valley"
    Wastelands = "Wastelands"
    Jungle = "Jungle"
    Oasis = "Oasis"
    CircleOfLife = "Circle of Life"
    Hyenas1Bonus = "Hyenas 1 Bonus"
    Scar = "Scar"
    Hyenas2Bonus = "Hyenas 2 Bonus"
    Groundshaker = "Groundshaker"
    DataSaix = "Data Saix"


class CheckLocation(str, Enum):
    GorgeSavannahMap = "Gorge Savannah Map"
    GorgeDarkGem = "Gorge Dark Gem"
    GorgeMyhtrilStone = "Gorge Mythril Stone"
    ElephantGraveyardFrostGem = "Elephant Graveyard Frost Gem"
    ElephantGraveyardMythrilStone = "Elephant Graveyard Mythril Stone"
    ElephantGraveyardBrightStone = "Elephant Graveyard Bright Stone"
    ElephantGraveyardApBoost = "Elephant Graveyard AP Boost"
    ElephantGraveyardMythrilShard = "Elephant Graveyard Mythril Shard"
    PrideRockMap = "Pride Rock Map"
    PrideRockMythrilStone = "Pride Rock Mythril Stone"
    PrideRockSerenityCrystal = "Pride Rock Serenity Crystal"
    WildebeestValleyEnergyStone = "Wildebeest Valley Energy Stone"
    WildebeestValleyApBoost = "Wildebeest Valley AP Boost"
    WildebeestValleyMythrilGem = "Wildebeest Valley Mythril Gem"
    WildebeestValleyMythrilStone = "Wildebeest Valley Mythril Stone"
    WildebeestValleyLucidGem = "Wildebeest Valley Lucid Gem"
    WastelandsMythrilShard = "Wastelands Mythril Shard"
    WastelandsSerenityGem = "Wastelands Serenity Gem"
    WastelandsMythrilStone = "Wastelands Mythril Stone"
    JungleSerenityGem = "Jungle Serenity Gem"
    JungleMythrilStone = "Jungle Mythril Stone"
    JungleSerenityCrystal = "Jungle Serenity Crystal"
    OasisMap = "Oasis Map"
    OasisTornPages = "Oasis Torn Pages"
    OasisApBoost = "Oasis AP Boost"
    CircleOfLife = "Circle of Life"
    Hyenas1 = "Hyenas 1"
    Scar = "Scar"
    ScarFireElement = "Scar Fire Element"
    Hyenas2 = "Hyenas 2"
    Groundshaker = "Groundshaker"
    DataSaix = "Saix (Data) Defense Boost"

class PLLogicGraph(DefaultLogicGraph):
    def __init__(self,reverse_rando,first_visit_locks):
        DefaultLogicGraph.__init__(self,NodeId)
        if not reverse_rando:
            self.logic[NodeId.Scar][NodeId.Hyenas2Bonus] = ItemPlacementHelpers.simba_check
        else:
            self.logic[NodeId.Groundshaker][NodeId.Gorge] = ItemPlacementHelpers.simba_check

def make_graph(graph: LocationGraphBuilder):
    pl = locationType.PL
    pl_logic = PLLogicGraph(graph.reverse_rando,graph.first_visit_locks)
    graph.add_logic(pl_logic)

    gorge = graph.add_location(NodeId.Gorge, [
        chest(492, CheckLocation.GorgeSavannahMap, pl),
        chest(404, CheckLocation.GorgeDarkGem, pl),
        chest(405, CheckLocation.GorgeMyhtrilStone, pl),
    ])
    elephant_graveyard = graph.add_location(NodeId.ElephantGraveyard, [
        chest(401, CheckLocation.ElephantGraveyardFrostGem, pl),
        chest(402, CheckLocation.ElephantGraveyardMythrilStone, pl),
        chest(403, CheckLocation.ElephantGraveyardBrightStone, pl),
        chest(508, CheckLocation.ElephantGraveyardApBoost, pl),
        chest(509, CheckLocation.ElephantGraveyardMythrilShard, pl),
    ])
    pride_rock = graph.add_location(NodeId.PrideRock, [
        chest(418, CheckLocation.PrideRockMap, pl),
        chest(392, CheckLocation.PrideRockMythrilStone, pl),
        chest(393, CheckLocation.PrideRockSerenityCrystal, pl),
    ])
    wildebeest_valley = graph.add_location(NodeId.WildebeestValley, [
        chest(396, CheckLocation.WildebeestValleyEnergyStone, pl),
        chest(397, CheckLocation.WildebeestValleyApBoost, pl),
        chest(398, CheckLocation.WildebeestValleyMythrilGem, pl),
        chest(399, CheckLocation.WildebeestValleyMythrilStone, pl),
        chest(400, CheckLocation.WildebeestValleyLucidGem, pl),
    ])
    wastelands = graph.add_location(NodeId.Wastelands, [
        chest(406, CheckLocation.WastelandsMythrilShard, pl),
        chest(407, CheckLocation.WastelandsSerenityGem, pl),
        chest(408, CheckLocation.WastelandsMythrilStone, pl),
    ])
    jungle = graph.add_location(NodeId.Jungle, [
        chest(409, CheckLocation.JungleSerenityGem, pl),
        chest(410, CheckLocation.JungleMythrilStone, pl),
        chest(411, CheckLocation.JungleSerenityCrystal, pl),
    ])
    oasis = graph.add_location(NodeId.Oasis, [
        chest(412, CheckLocation.OasisMap, pl),
        chest(493, CheckLocation.OasisTornPages, pl, vanilla=misc.TornPages),
        chest(413, CheckLocation.OasisApBoost, pl),
    ])
    circle_of_life = graph.add_location(NodeId.CircleOfLife, [
        popup(264, CheckLocation.CircleOfLife, pl, vanilla=keyblade.CircleOfLife),
    ])
    hyenas_1_bonus = graph.add_location(NodeId.Hyenas1Bonus, [
        stat_bonus(49, CheckLocation.Hyenas1, pl),
    ])
    scar = graph.add_location(NodeId.Scar, [
        stat_bonus(29, CheckLocation.Scar, pl),
        popup(302, CheckLocation.ScarFireElement, pl, vanilla=magic.Fire),
    ])
    hyenas_2_bonus = graph.add_location(NodeId.Hyenas2Bonus, [
        stat_bonus(50, CheckLocation.Hyenas2, pl),
    ])
    groundshaker = graph.add_location(NodeId.Groundshaker, [
        hybrid_bonus(30, CheckLocation.Groundshaker, pl, vanilla=magic.Thunder),
    ])
    data_saix = graph.add_location(NodeId.DataSaix, [
        popup(556, CheckLocation.DataSaix, [pl, locationType.DataOrg]),
    ])

    graph.register_superboss(data_saix)

    if not graph.reverse_rando:
        graph.add_edge(START_NODE, gorge)
        graph.add_edge(gorge, elephant_graveyard, RequirementEdge(battle=True))
        graph.add_edge(elephant_graveyard, pride_rock)
        graph.add_edge(pride_rock, wildebeest_valley)
        graph.add_edge(wildebeest_valley, wastelands)
        graph.add_edge(wastelands, jungle)
        graph.add_edge(jungle, oasis)
        graph.add_edge(oasis, circle_of_life)
        graph.add_edge(circle_of_life, hyenas_1_bonus, RequirementEdge(battle=True))
        graph.add_edge(hyenas_1_bonus, scar, RequirementEdge(battle=True))
        graph.add_edge(scar, hyenas_2_bonus, RequirementEdge(battle=True, req=ItemPlacementHelpers.simba_check))
        graph.add_edge(hyenas_2_bonus, groundshaker, RequirementEdge(battle=True))
        graph.add_edge(groundshaker, data_saix, RequirementEdge(battle=True))
        graph.register_first_boss(scar)
        graph.register_last_story_boss(groundshaker)
    else:
        graph.add_edge(START_NODE, pride_rock)
        graph.add_edge(pride_rock, elephant_graveyard)
        graph.add_edge(elephant_graveyard, hyenas_2_bonus, RequirementEdge(battle=True))
        graph.add_edge(hyenas_2_bonus, wildebeest_valley)
        graph.add_edge(wildebeest_valley, wastelands)
        graph.add_edge(wastelands, jungle)
        graph.add_edge(jungle, groundshaker, RequirementEdge(battle=True))
        graph.add_edge(groundshaker, gorge, RequirementEdge(req=ItemPlacementHelpers.simba_check))
        graph.add_edge(gorge, oasis, RequirementEdge(battle=True))
        graph.add_edge(oasis, circle_of_life)
        graph.add_edge(circle_of_life, hyenas_1_bonus, RequirementEdge(battle=True))
        graph.add_edge(hyenas_1_bonus, scar, RequirementEdge(battle=True))
        graph.add_edge(scar, data_saix, RequirementEdge(battle=True))
        graph.register_first_boss(groundshaker)
        graph.register_last_story_boss(scar)

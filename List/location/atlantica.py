from enum import Enum

from List.configDict import locationType
from List.inventory import keyblade, magic
from List.location.graph import RequirementEdge, popup, LocationGraphBuilder, START_NODE, DefaultLogicGraph
from Module.itemPlacementRestriction import ItemPlacementHelpers


class NodeId(str, Enum):
    AtlanticaTutorial = "Atlantica Tutorial"
    Ursula = "Ursula"
    NewDayIsDawning = "New Day is Dawning"


class CheckLocation(str, Enum):
    UnderseaKingdomMap = "Undersea Kingdom Map"
    MysteriousAbyss = "Mysterious Abyss"
    MusicalBlizzardElement = "Musical Blizzard Element"
    MusicalOrichalcumPlus = "Musical Orichalcum+"


class ATLogicGraph(DefaultLogicGraph):
    def __init__(self,reverse_rando):
        DefaultLogicGraph.__init__(self,NodeId)
        if not reverse_rando:
            self.logic[NodeId.AtlanticaTutorial][NodeId.Ursula] = ItemPlacementHelpers.need_2_magnet
            self.logic[NodeId.Ursula][NodeId.NewDayIsDawning] = ItemPlacementHelpers.need_3_thunders
        else:
            self.logic[NodeId.NewDayIsDawning][NodeId.Ursula] = ItemPlacementHelpers.need_1_magnet
            self.logic[NodeId.Ursula][NodeId.AtlanticaTutorial] = lambda inv: ItemPlacementHelpers.need_2_magnet(inv) and ItemPlacementHelpers.need_3_thunders(inv)


def make_graph(graph: LocationGraphBuilder):
    at = locationType.Atlantica
    at_logic = ATLogicGraph(graph.reverse_rando)
    graph.add_logic(at_logic)

    tutorial = graph.add_location(NodeId.AtlanticaTutorial, [
        popup(367, CheckLocation.UnderseaKingdomMap, at),
    ])
    ursula = graph.add_location(NodeId.Ursula, [
        popup(287, CheckLocation.MysteriousAbyss, at, vanilla=keyblade.MysteriousAbyss),
    ])
    new_day_is_dawning = graph.add_location(NodeId.NewDayIsDawning, [
        popup(279, CheckLocation.MusicalBlizzardElement, at, vanilla=magic.Blizzard),
        popup(538, CheckLocation.MusicalOrichalcumPlus, at),
    ])

    if not graph.reverse_rando:
        graph.add_edge(START_NODE, tutorial)
        graph.add_edge(tutorial, ursula, RequirementEdge())
        graph.add_edge(ursula, new_day_is_dawning, RequirementEdge())
    else:
        graph.add_edge(START_NODE, new_day_is_dawning)
        graph.add_edge(new_day_is_dawning, ursula, RequirementEdge())
        graph.add_edge(ursula, tutorial, RequirementEdge())

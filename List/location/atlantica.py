from enum import Enum

from List.configDict import locationType
from List.inventory import keyblade, magic
from List.location.graph import RequirementEdge, popup, LocationGraphBuilder, START_NODE
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


def make_graph(graph: LocationGraphBuilder):
    at = locationType.Atlantica

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
        graph.add_edge(tutorial, ursula, RequirementEdge(req=ItemPlacementHelpers.need_2_magnet))
        graph.add_edge(ursula, new_day_is_dawning, RequirementEdge(
            req=lambda inv: ItemPlacementHelpers.need_2_magnet(inv) and ItemPlacementHelpers.need_3_thunders(inv)))
    else:
        graph.add_edge(START_NODE, new_day_is_dawning)
        graph.add_edge(new_day_is_dawning, ursula, RequirementEdge(req=ItemPlacementHelpers.need_1_magnet))
        graph.add_edge(ursula, tutorial, RequirementEdge(
            req=lambda inv: ItemPlacementHelpers.need_2_magnet(inv) and ItemPlacementHelpers.need_3_thunders(inv)))

from enum import Enum

from List.configDict import locationType
from List.inventory import magic, keyblade
from List.location.graph import DefaultLogicGraph, RequirementEdge, chest, popup, LocationGraphBuilder, START_NODE
from Module.itemPlacementRestriction import ItemPlacementHelpers


class NodeId(str, Enum):
    PoohsHowse = "Pooh's Howse"
    PoohsHowseChests = "Pooh's Howse Chests"
    PigletsHowse = "Piglet's Howse"
    PigletsHowseChests = "Piglet's Howse Chests"
    RabbitsHowse = "Rabbit's Howse"
    RabbitsHowseChests = "Rabbit's Howse Chests"
    KangasHowse = "Kanga's Howse"
    KangasHowseChests = "Kanga's Howse Chests"
    SpookyCave = "Spooky Cave"
    SpookyCaveChests = "Spooky Cave Chests"
    StarryHill = "Starry Hill"
    StarryHillChests = "Starry Hill Chests"


class CheckLocation(str, Enum):
    PoohsHowseHundredAcreWoodMap = "Pooh's House 100 Acre Wood Map"
    PoohsHowseApBoost = "Pooh's House AP Boost"
    PoohsHowseMythrilStone = "Pooh's House Mythril Stone"
    PigletsHowseDefenseBoost = "Piglet's House Defense Boost"
    PigletsHowseApBoost = "Piglet's House AP Boost"
    PigletsHowseMythrilGem = "Piglet's House Mythril Gem"
    RabbitsHowseDrawRing = "Rabbit's House Draw Ring"
    RabbitsHowseMythrilCrystal = "Rabbit's House Mythril Crystal"
    RabbitsHowseApBoost = "Rabbit's House AP Boost"
    KangasHowseMagicBoost = "Kanga's House Magic Boost"
    KangasHowseApBoost = "Kanga's House AP Boost"
    KangasHowseOrichalcum = "Kanga's House Orichalcum"
    SpookyCaveMyhtrilGem = "Spooky Cave Mythril Gem"
    SpookyCaveApBoost = "Spooky Cave AP Boost"
    SpookyCaveOrichalcum = "Spooky Cave Orichalcum"
    SpookyCaveGuardRecipe = "Spooky Cave Guard Recipe"
    SpookyCaveMythrilCrystal = "Spooky Cave Mythril Crystal"
    SpookyCaveApBoost2 = "Spooky Cave AP Boost (2)"
    SweetMemories = "Sweet Memories"
    SpookyCaveMap = "Spooky Cave Map"
    StarryHillCosmicRing = "Starry Hill Cosmic Ring"
    StarryHillStyleRecipe = "Starry Hill Style Recipe"
    StarryHillCureElement = "Starry Hill Cure Element"
    StarryHillOrichalcumPlus = "Starry Hill Orichalcum+"

class HAWLogicGraph(DefaultLogicGraph):
    def __init__(self,reverse_rando, keyblade_unlocks):
        DefaultLogicGraph.__init__(self,NodeId)
        keyblade_lambda = lambda inv : not keyblade_unlocks or ItemPlacementHelpers.need_haw_keyblade(inv)
        self.logic[NodeId.PoohsHowse][NodeId.PoohsHowseChests] = keyblade_lambda
        self.logic[NodeId.PigletsHowse][NodeId.PigletsHowseChests] = keyblade_lambda
        self.logic[NodeId.RabbitsHowse][NodeId.RabbitsHowseChests] = keyblade_lambda
        self.logic[NodeId.KangasHowse][NodeId.KangasHowseChests] = keyblade_lambda
        self.logic[NodeId.SpookyCave][NodeId.SpookyCaveChests] = keyblade_lambda
        self.logic[NodeId.StarryHill][NodeId.StarryHillChests] = keyblade_lambda
        if not reverse_rando:
            self.logic[NodeId.PoohsHowse][NodeId.PigletsHowse] = ItemPlacementHelpers.need_torn_pages(1)
            self.logic[NodeId.PigletsHowse][NodeId.RabbitsHowse] = ItemPlacementHelpers.need_torn_pages(2)
            self.logic[NodeId.RabbitsHowse][NodeId.KangasHowse] = ItemPlacementHelpers.need_torn_pages(3)
            self.logic[NodeId.KangasHowse][NodeId.SpookyCave] = ItemPlacementHelpers.need_torn_pages(4)
            self.logic[NodeId.SpookyCave][NodeId.StarryHill] = ItemPlacementHelpers.need_torn_pages(5)
        else:
            self.logic[NodeId.StarryHill][NodeId.SpookyCave] = ItemPlacementHelpers.need_torn_pages(1)
            self.logic[NodeId.SpookyCave][NodeId.KangasHowse] = ItemPlacementHelpers.need_torn_pages(2)
            self.logic[NodeId.KangasHowse][NodeId.RabbitsHowse] = ItemPlacementHelpers.need_torn_pages(3)
            self.logic[NodeId.RabbitsHowse][NodeId.PigletsHowse] = ItemPlacementHelpers.need_torn_pages(4)
            self.logic[NodeId.PigletsHowse][NodeId.PoohsHowse] = ItemPlacementHelpers.need_torn_pages(5)
            

def make_graph(graph: LocationGraphBuilder):
    haw = locationType.HUNDREDAW
    haw_logic = HAWLogicGraph(graph.reverse_rando,graph.keyblades_unlock_chests)
    graph.add_logic(haw_logic)

    poohs_howse_chests = graph.add_location(NodeId.PoohsHowseChests, [
        chest(313, CheckLocation.PoohsHowseHundredAcreWoodMap, haw),
        chest(97, CheckLocation.PoohsHowseApBoost, haw),
        chest(98, CheckLocation.PoohsHowseMythrilStone, haw),
    ])
    poohs_howse = graph.add_location(NodeId.PoohsHowse, [])
    piglets_howse_chests = graph.add_location(NodeId.PigletsHowseChests, [
        chest(105, CheckLocation.PigletsHowseDefenseBoost, haw),
        chest(103, CheckLocation.PigletsHowseApBoost, haw),
        chest(104, CheckLocation.PigletsHowseMythrilGem, haw),
    ])
    piglets_howse = graph.add_location(NodeId.PigletsHowse, [])
    rabbits_howse_chests = graph.add_location(NodeId.RabbitsHowseChests, [
        chest(314, CheckLocation.RabbitsHowseDrawRing, haw),
        chest(100, CheckLocation.RabbitsHowseMythrilCrystal, haw),
        chest(101, CheckLocation.RabbitsHowseApBoost, haw),
    ])
    rabbits_howse = graph.add_location(NodeId.RabbitsHowse, [])
    kangas_howse_chests = graph.add_location(NodeId.KangasHowseChests, [
        chest(108, CheckLocation.KangasHowseMagicBoost, haw),
        chest(106, CheckLocation.KangasHowseApBoost, haw),
        chest(107, CheckLocation.KangasHowseOrichalcum, haw),
    ])
    kangas_howse = graph.add_location(NodeId.KangasHowse, [])
    spooky_cave_chests = graph.add_location(NodeId.SpookyCaveChests, [
        chest(110, CheckLocation.SpookyCaveMyhtrilGem, haw),
        chest(111, CheckLocation.SpookyCaveApBoost, haw),
        chest(112, CheckLocation.SpookyCaveOrichalcum, haw),
        chest(113, CheckLocation.SpookyCaveGuardRecipe, haw),
        chest(115, CheckLocation.SpookyCaveMythrilCrystal, haw),
        chest(116, CheckLocation.SpookyCaveApBoost2, haw),
    ])
    spooky_cave = graph.add_location(NodeId.SpookyCave, [
        popup(284, CheckLocation.SweetMemories, haw, vanilla=keyblade.SweetMemories),
        popup(485, CheckLocation.SpookyCaveMap, haw),
    ])
    starry_hill_chests = graph.add_location(NodeId.StarryHillChests, [
        chest(312, CheckLocation.StarryHillCosmicRing, haw),
        chest(94, CheckLocation.StarryHillStyleRecipe, haw),
    ])
    starry_hill = graph.add_location(NodeId.StarryHill, [
        popup(285, CheckLocation.StarryHillCureElement, haw, vanilla=magic.Cure),
        popup(539, CheckLocation.StarryHillOrichalcumPlus, haw),
    ])

    graph.add_edge(poohs_howse, poohs_howse_chests)
    graph.add_edge(piglets_howse, piglets_howse_chests)
    graph.add_edge(rabbits_howse, rabbits_howse_chests)
    graph.add_edge(kangas_howse, kangas_howse_chests)
    graph.add_edge(spooky_cave, spooky_cave_chests)
    graph.add_edge(starry_hill, starry_hill_chests)

    if not graph.reverse_rando:
        graph.add_edge(START_NODE, poohs_howse)
        graph.add_edge(poohs_howse, piglets_howse)
        graph.add_edge(piglets_howse, rabbits_howse)
        graph.add_edge(rabbits_howse, kangas_howse)
        graph.add_edge(kangas_howse, spooky_cave)
        graph.add_edge(spooky_cave, starry_hill)
    else:
        graph.add_edge(START_NODE, starry_hill)
        graph.add_edge(starry_hill, spooky_cave)
        graph.add_edge(spooky_cave, kangas_howse)
        graph.add_edge(kangas_howse, rabbits_howse)
        graph.add_edge(rabbits_howse, piglets_howse)
        graph.add_edge(piglets_howse, poohs_howse)


def yeet_the_bear_location_names() -> list[str]:
    """ The names of the "yeet the bear" popup locations. """
    return [CheckLocation.StarryHillCureElement, CheckLocation.StarryHillOrichalcumPlus]

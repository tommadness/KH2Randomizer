from enum import Enum

from List.configDict import locationType, itemType
from List.inventory import magic, keyblade, ability
from List.location.graph import RequirementEdge, chest, popup, hybrid_bonus, stat_bonus, LocationGraphBuilder, \
    START_NODE
from Module.itemPlacementRestriction import ItemPlacementHelpers


class NodeId(str, Enum):
    Graveyard = "Graveyard"
    FinklesteinsLab = "Finklestein's Lab"
    TownSquare = "Town Square"
    Hinterlands = "Hinterlands"
    CandyCaneLane = "Candy Cane Lane"
    SantasHouse = "Santa's House"
    PrisonKeeper = "Prison Keeper"
    OogieBoogie = "Oogie Boogie"
    LockShockBarrel = "Lock, Shock, and Barrel"
    Presents = "Presents"
    DecoyPresentMinigame = "Decoy Present Minigame"
    Experiment = "Experiment"
    Vexen = "AS Vexen"
    DataVexen = "Data Vexen"


class CheckLocation(str, Enum):
    GraveyardMythrilShard = "Graveyard Mythril Shard"
    GraveyardSerenityGem = "Graveyard Serenity Gem"
    FinklesteinsLabHalloweenTownMap = "Finklestein's Lab Halloween Town Map"
    TownSquareMythrilStone = "Town Square Mythril Stone"
    TownSquareEnergyShard = "Town Square Energy Shard"
    HinterlandsLightningShard = "Hinterlands Lightning Shard"
    HinterlandsMythrilStone = "Hinterlands Mythril Stone"
    HinterlandsApBoost = "Hinterlands AP Boost"
    CandyCaneLaneMegaPotion = "Candy Cane Lane Mega-Potion"
    CandyCaneLaneMythrilGem = "Candy Cane Lane Mythril Gem"
    CandyCaneLaneLightningStone = "Candy Cane Lane Lightning Stone"
    CandyCaneLaneMythrilStone = "Candy Cane Lane Mythril Stone"
    SantasHouseChristmasTownMap = "Santa's House Christmas Town Map"
    SantasHouseApBoost = "Santa's House AP Boost"
    PrisonKeeper = "Prison Keeper"
    OogieBoogie = "Oogie Boogie"
    OogieMagnetElement = "Oogie Boogie Magnet Element"
    LockShockBarrel = "Lock, Shock, and Barrel"
    Present = "Present"
    DecoyPresents = "Decoy Presents"
    Experiment = "Experiment"
    DecisivePumpkin = "Decisive Pumpkin"
    VexenBonus = "Vexen Bonus"
    VexenRoadToDiscovery = "Vexen (AS) Road to Discovery"
    DataVexen = "Vexen (Data) Lost Illusion"


def make_graph(graph: LocationGraphBuilder):
    ht = locationType.HT

    finklesteins_lab = graph.add_location(NodeId.FinklesteinsLab, [
        chest(211, CheckLocation.FinklesteinsLabHalloweenTownMap, ht),
    ])
    graveyard = graph.add_location(NodeId.Graveyard, [
        chest(53, CheckLocation.GraveyardMythrilShard, ht),
        chest(212, CheckLocation.GraveyardSerenityGem, ht),
    ])
    town_square = graph.add_location(NodeId.TownSquare, [
        chest(209, CheckLocation.TownSquareMythrilStone, ht),
        chest(210, CheckLocation.TownSquareEnergyShard, ht),
    ])
    hinterlands = graph.add_location(NodeId.Hinterlands, [
        chest(54, CheckLocation.HinterlandsLightningShard, ht),
        chest(213, CheckLocation.HinterlandsMythrilStone, ht),
        chest(214, CheckLocation.HinterlandsApBoost, ht),
    ])
    candy_cane_lane = graph.add_location(NodeId.CandyCaneLane, [
        chest(55, CheckLocation.CandyCaneLaneMegaPotion, ht),
        chest(56, CheckLocation.CandyCaneLaneMythrilGem, ht),
        chest(216, CheckLocation.CandyCaneLaneLightningStone, ht),
        chest(217, CheckLocation.CandyCaneLaneMythrilStone, ht),
    ])
    santas_house = graph.add_location(NodeId.SantasHouse, [
        chest(57, CheckLocation.SantasHouseChristmasTownMap, ht, invalid_checks=[itemType.GAUGE]),
        chest(58, CheckLocation.SantasHouseApBoost, ht, invalid_checks=[itemType.GAUGE]),
    ])
    prison_keeper = graph.add_location(NodeId.PrisonKeeper, [
        hybrid_bonus(18, CheckLocation.PrisonKeeper, ht, vanilla=ability.FlashStep),
    ])
    oogie_boogie = graph.add_location(NodeId.OogieBoogie, [
        stat_bonus(19, CheckLocation.OogieBoogie, ht),
        popup(301, CheckLocation.OogieMagnetElement, ht, vanilla=magic.Magnet),
    ])
    lock_shock_barrel = graph.add_location(NodeId.LockShockBarrel, [
        stat_bonus(40, CheckLocation.LockShockBarrel, ht),
    ])
    presents = graph.add_location(NodeId.Presents, [
        popup(297, CheckLocation.Present, ht),
    ])
    decoy_present_minigame = graph.add_location(NodeId.DecoyPresentMinigame, [
        popup(298, CheckLocation.DecoyPresents, ht),
    ])
    experiment = graph.add_location(NodeId.Experiment, [
        stat_bonus(20, CheckLocation.Experiment, ht),
        popup(275, CheckLocation.DecisivePumpkin, ht, vanilla=keyblade.DecisivePumpkin),
    ])
    vexen = graph.add_location(NodeId.Vexen, [
        stat_bonus(64, CheckLocation.VexenBonus, [ht, locationType.AS]),
        popup(544, CheckLocation.VexenRoadToDiscovery, [ht, locationType.AS]),
    ])
    data_vexen = graph.add_location(NodeId.DataVexen, [
        popup(549, CheckLocation.DataVexen, [ht, locationType.DataOrg]),
    ])

    graph.register_superboss(data_vexen)

    if not graph.reverse_rando:
        graph.add_edge(START_NODE, graveyard)
        graph.add_edge(graveyard, finklesteins_lab)
        graph.add_edge(finklesteins_lab, town_square)
        graph.add_edge(town_square, hinterlands)
        graph.add_edge(hinterlands, candy_cane_lane, RequirementEdge(battle=True))
        graph.add_edge(candy_cane_lane, santas_house)
        graph.add_edge(santas_house, prison_keeper, RequirementEdge(battle=True))
        graph.add_edge(prison_keeper, oogie_boogie, RequirementEdge(battle=True))
        graph.add_edge(oogie_boogie, lock_shock_barrel,
                       RequirementEdge(battle=True, req=ItemPlacementHelpers.jack_ht_check))
        graph.add_edge(lock_shock_barrel, presents, RequirementEdge(battle=True))
        graph.add_edge(presents, decoy_present_minigame)
        graph.add_edge(decoy_present_minigame, experiment, RequirementEdge(battle=True))
        graph.add_edge(experiment, vexen, RequirementEdge(battle=True))
        graph.add_edge(vexen, data_vexen)
        graph.register_first_boss(oogie_boogie)
        graph.register_last_story_boss(experiment)
        graph.register_superboss(vexen)
    else:
        graph.add_edge(START_NODE, santas_house)
        graph.add_edge(santas_house, candy_cane_lane)
        graph.add_edge(candy_cane_lane, hinterlands)
        graph.add_edge(hinterlands, graveyard)
        graph.add_edge(graveyard, town_square)
        graph.add_edge(santas_house, lock_shock_barrel, RequirementEdge(battle=True))
        graph.add_edge(lock_shock_barrel, presents, RequirementEdge(battle=True))
        graph.add_edge(presents, decoy_present_minigame)
        graph.add_edge(decoy_present_minigame, experiment, RequirementEdge(battle=True))
        graph.add_edge(experiment, vexen, RequirementEdge(battle=True))
        graph.add_edge(vexen, finklesteins_lab, RequirementEdge(req=ItemPlacementHelpers.jack_ht_check))
        graph.add_edge(finklesteins_lab, prison_keeper, RequirementEdge(battle=True))
        graph.add_edge(prison_keeper, oogie_boogie, RequirementEdge(battle=True))
        graph.add_edge(oogie_boogie, data_vexen, RequirementEdge(battle=True))
        graph.register_first_boss(experiment)
        graph.register_last_story_boss(oogie_boogie)

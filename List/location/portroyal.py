from enum import Enum

from List.configDict import locationType
from List.inventory import magic, keyblade, ability, summon, report
from List.location.graph import RequirementEdge, chest, popup, hybrid_bonus, stat_bonus, item_bonus, \
    LocationGraphBuilder, START_NODE
from Module.itemPlacementRestriction import ItemPlacementHelpers


class NodeId(str, Enum):
    Rampart = "Ramparts"
    PortRoyalTown = "PR Town"
    CaveMouth = "Cave Mouth"
    IslaDeMuertaPopup = "Isla de Meurta Popup"
    BoatFight = "Boat Fight"
    BarrelsMinigame = "Barrels Minigame"
    PowderStore = "Powder Store"
    MoonlightNook = "Moonlight Nook"
    Barbossa = "Barbossa"
    GrimReaper1 = "Grim Reaper 1"
    InterceptorsHold = "Interceptor's Hold"
    SeadriftKeep = "Seadrift Keep"
    SeadriftRow = "Seadrift Row"
    CursedMedallionPopup = "Cursed Medallion Popup"
    GrimReaper2 = "Grim Reaper 2"
    DataLuxord = "Data Luxord"


class CheckLocation(str, Enum):
    RampartNavalMap = "Rampart Naval Map"
    RampartMythrilStone = "Rampart Mythril Stone"
    RampartDarkShard = "Rampart Dark Shard"
    TownDarkStone = "Town Dark Stone"
    TownApBoost = "Town AP Boost"
    TownMythrilShard = "Town Mythril Shard"
    TownMythrilGem = "Town Mythril Gem"
    CaveMouthBrightShard = "Cave Mouth Bright Shard"
    CaveMouthMythrilShard = "Cave Mouth Mythril Shard"
    IslaDeMuertaMap = "Isla de Muerta Map"
    BoatFight = "Boat Fight"
    InterceptorBarrels = "Interceptor Barrels"
    PowderStoreApBoost1 = "Powder Store AP Boost (1)"
    PowderStoreApBoost2 = "Powder Store AP Boost (2)"
    MoonlightNookMythrilShard = "Moonlight Nook Mythril Shard"
    MoonlightNookSerenityGem = "Moonlight Nook Serenity Gem"
    MoonlightNookPowerStone = "Moonlight Nook Power Stone"
    Barbossa = "Barbossa"
    FollowTheWind = "Follow the Wind"
    GrimReaper1 = "Grim Reaper 1"
    InterceptorsHoldFeatherCharm = "Interceptor's Hold Feather Charm"
    SeadriftKeepApBoost = "Seadrift Keep AP Boost"
    SeadriftKeepOrichalcum = "Seadrift Keep Orichalcum"
    SeadriftKeepMeteorStaff = "Seadrift Keep Meteor Staff"
    SeadriftRowSerenityGem = "Seadrift Row Serenity Gem"
    SeadriftRowKingRecipe = "Seadrift Row King Recipe"
    SeadriftRowMythrilCrystal = "Seadrift Row Mythril Crystal"
    SeadriftRowCursedMedallion = "Seadrift Row Cursed Medallion"
    SeadriftRowShipGraveyardMap = "Seadrift Row Ship Graveyard Map"
    GrimReaper2 = "Grim Reaper 2"
    GrimReaper2SecretAnsemReport6 = "Secret Ansem Report 6"
    DataLuxordApBoost = "Luxord (Data) AP Boost"


def make_graph(graph: LocationGraphBuilder):
    pr = locationType.PR

    rampart = graph.add_location(NodeId.Rampart, [
        chest(70, CheckLocation.RampartNavalMap, pr),
        chest(219, CheckLocation.RampartMythrilStone, pr),
        chest(220, CheckLocation.RampartDarkShard, pr),
    ])
    town = graph.add_location(NodeId.PortRoyalTown, [
        chest(71, CheckLocation.TownDarkStone, pr),
        chest(72, CheckLocation.TownApBoost, pr),
        chest(73, CheckLocation.TownMythrilShard, pr),
        chest(221, CheckLocation.TownMythrilGem, pr),
    ])
    cave_mouth = graph.add_location(NodeId.CaveMouth, [
        chest(74, CheckLocation.CaveMouthBrightShard, pr),
        chest(223, CheckLocation.CaveMouthMythrilShard, pr),
    ])
    isla_de_muerta_popup = graph.add_location(NodeId.IslaDeMuertaPopup, [
        popup(329, CheckLocation.IslaDeMuertaMap, pr),
    ])
    boat_fight = graph.add_location(NodeId.BoatFight, [
        item_bonus(62, CheckLocation.BoatFight, pr, vanilla=ability.AerialSpiral),
    ])
    barrels_minigame = graph.add_location(NodeId.BarrelsMinigame, [
        stat_bonus(39, CheckLocation.InterceptorBarrels, pr),
    ])
    powder_store = graph.add_location(NodeId.PowderStore, [
        chest(369, CheckLocation.PowderStoreApBoost1, pr),
        chest(370, CheckLocation.PowderStoreApBoost2, pr),
    ])
    moonlight_nook = graph.add_location(NodeId.MoonlightNook, [
        chest(75, CheckLocation.MoonlightNookMythrilShard, pr),
        chest(224, CheckLocation.MoonlightNookSerenityGem, pr),
        chest(371, CheckLocation.MoonlightNookPowerStone, pr),
    ])
    barbossa = graph.add_location(NodeId.Barbossa, [
        hybrid_bonus(21, CheckLocation.Barbossa, pr, vanilla=ability.AerialFinish),
        popup(263, CheckLocation.FollowTheWind, pr, vanilla=keyblade.FollowTheWind),
    ])
    grim_reaper_1 = graph.add_location(NodeId.GrimReaper1, [
        item_bonus(59, CheckLocation.GrimReaper1, pr, vanilla=ability.HorizontalSlash),
    ])
    interceptors_hold = graph.add_location(NodeId.InterceptorsHold, [
        chest(252, CheckLocation.InterceptorsHoldFeatherCharm, pr, vanilla=summon.FeatherCharm),
    ])
    seadrift_keep = graph.add_location(NodeId.SeadriftKeep, [
        chest(76, CheckLocation.SeadriftKeepApBoost, pr),
        chest(225, CheckLocation.SeadriftKeepOrichalcum, pr),
        chest(372, CheckLocation.SeadriftKeepMeteorStaff, pr),
    ])
    seadrift_row = graph.add_location(NodeId.SeadriftRow, [
        chest(77, CheckLocation.SeadriftRowSerenityGem, pr),
        chest(78, CheckLocation.SeadriftRowKingRecipe, pr),
        chest(373, CheckLocation.SeadriftRowMythrilCrystal, pr),
    ])
    cursed_medallion_popup = graph.add_location(NodeId.CursedMedallionPopup, [
        popup(296, CheckLocation.SeadriftRowCursedMedallion, pr),
        popup(331, CheckLocation.SeadriftRowShipGraveyardMap, pr),
    ])
    grim_reaper_2 = graph.add_location(NodeId.GrimReaper2, [
        item_bonus(22, CheckLocation.GrimReaper2, pr, vanilla=magic.Magnet),
        popup(530, CheckLocation.GrimReaper2SecretAnsemReport6, pr, vanilla=report.AnsemReport6),
    ])
    data_luxord = graph.add_location(NodeId.DataLuxord, [
        popup(557, CheckLocation.DataLuxordApBoost, [pr, locationType.DataOrg]),
    ])

    graph.register_superboss(data_luxord)

    if not graph.reverse_rando:
        graph.add_edge(START_NODE, rampart)
        graph.add_edge(rampart, town, RequirementEdge(battle=True))
        graph.add_edge(town, cave_mouth)
        graph.add_edge(cave_mouth, isla_de_muerta_popup, RequirementEdge(battle=True))
        graph.add_edge(isla_de_muerta_popup, boat_fight, RequirementEdge(battle=True))
        graph.add_edge(boat_fight, barrels_minigame)
        graph.add_edge(barrels_minigame, powder_store)
        graph.add_edge(powder_store, moonlight_nook)
        graph.add_edge(moonlight_nook, barbossa, RequirementEdge(battle=True))
        graph.add_edge(barbossa, grim_reaper_1, RequirementEdge(battle=True, req=ItemPlacementHelpers.jack_pr_check))
        graph.add_edge(grim_reaper_1, interceptors_hold)
        graph.add_edge(interceptors_hold, seadrift_keep)
        graph.add_edge(seadrift_keep, seadrift_row)
        graph.add_edge(seadrift_row, cursed_medallion_popup, RequirementEdge(battle=True))
        graph.add_edge(cursed_medallion_popup, grim_reaper_2, RequirementEdge(battle=True))
        graph.add_edge(grim_reaper_2, data_luxord, RequirementEdge(battle=True))
        graph.register_first_boss(barbossa)
        graph.register_last_story_boss(grim_reaper_2)
    else:
        graph.add_edge(START_NODE, rampart)
        graph.add_edge(rampart, grim_reaper_1, RequirementEdge(battle=True))
        graph.add_edge(grim_reaper_1, interceptors_hold)
        graph.add_edge(interceptors_hold, seadrift_keep)
        graph.add_edge(seadrift_keep, seadrift_row)
        graph.add_edge(seadrift_row, cursed_medallion_popup, RequirementEdge(battle=True))
        graph.add_edge(cursed_medallion_popup, cave_mouth)
        graph.add_edge(cave_mouth, grim_reaper_2, RequirementEdge(battle=True))
        graph.add_edge(grim_reaper_2, town, RequirementEdge(battle=True, req=ItemPlacementHelpers.jack_pr_check))
        graph.add_edge(town, isla_de_muerta_popup, RequirementEdge(battle=True))
        graph.add_edge(isla_de_muerta_popup, boat_fight, RequirementEdge(battle=True))
        graph.add_edge(boat_fight, barrels_minigame)
        graph.add_edge(barrels_minigame, powder_store)
        graph.add_edge(powder_store, moonlight_nook)
        graph.add_edge(moonlight_nook, barbossa, RequirementEdge(battle=True))
        graph.add_edge(barbossa, data_luxord, RequirementEdge(battle=True))
        graph.register_first_boss(grim_reaper_2)
        graph.register_last_story_boss(barbossa)

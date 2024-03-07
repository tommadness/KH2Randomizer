from enum import Enum

from List.configDict import locationType
from List.inventory import magic, keyblade, ability, summon, report
from List.location.graph import DefaultLogicGraph, RequirementEdge, chest, popup, hybrid_bonus, stat_bonus, item_bonus, \
    LocationGraphBuilder, START_NODE
from Module.itemPlacementRestriction import ItemPlacementHelpers


class NodeId(str, Enum):
    Rampart = "Ramparts"
    RampartChests = "Ramparts Chests"
    PortRoyalTown = "PR Town"
    PortRoyalTownChests = "PR Town Chests"
    CaveMouth = "Cave Mouth"
    CaveMouthChests = "Cave Mouth Chests"
    IslaDeMuertaPopup = "Isla de Meurta Popup"
    BoatFight = "Boat Fight"
    BarrelsMinigame = "Barrels Minigame"
    PowderStore = "Powder Store"
    PowderStoreChests = "Powder Store Chests"
    MoonlightNook = "Moonlight Nook"
    MoonlightNookChests = "Moonlight Nook Chests"
    Barbossa = "Barbossa"
    GrimReaper1 = "Grim Reaper 1"
    InterceptorsHold = "Interceptor's Hold"
    InterceptorsHoldChests = "Interceptor's Hold Chests"
    SeadriftKeep = "Seadrift Keep"
    SeadriftKeepChests = "Seadrift Keep Chests"
    SeadriftRow = "Seadrift Row"
    SeadriftRowChests = "Seadrift Row Chests"
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

class PRLogicGraph(DefaultLogicGraph):
    def __init__(self,reverse_rando,first_visit_locks):
        DefaultLogicGraph.__init__(self,NodeId)
        if not reverse_rando:
            self.logic[NodeId.Rampart][NodeId.RampartChests] = ItemPlacementHelpers.need_pr_keyblade
            self.logic[NodeId.PortRoyalTown][NodeId.PortRoyalTownChests] = ItemPlacementHelpers.need_pr_keyblade
            self.logic[NodeId.CaveMouth][NodeId.CaveMouthChests] = ItemPlacementHelpers.need_pr_keyblade
            self.logic[NodeId.PowderStore][NodeId.PowderStoreChests] = ItemPlacementHelpers.need_pr_keyblade
            self.logic[NodeId.MoonlightNook][NodeId.MoonlightNookChests] = ItemPlacementHelpers.need_pr_keyblade
            self.logic[NodeId.InterceptorsHold][NodeId.InterceptorsHoldChests] = ItemPlacementHelpers.need_pr_keyblade
            self.logic[NodeId.SeadriftKeep][NodeId.SeadriftKeepChests] = ItemPlacementHelpers.need_pr_keyblade
            self.logic[NodeId.SeadriftRow][NodeId.SeadriftRowChests] = ItemPlacementHelpers.need_pr_keyblade
            self.logic[START_NODE][NodeId.Rampart] = ItemPlacementHelpers.pr1_check
            self.logic[NodeId.Barbossa][NodeId.GrimReaper1] = ItemPlacementHelpers.pr2_check
        else:
            self.logic[NodeId.GrimReaper2][NodeId.PortRoyalTown] = ItemPlacementHelpers.pr2_check
            

def make_graph(graph: LocationGraphBuilder):
    pr = locationType.PR
    pr_logic = PRLogicGraph(graph.reverse_rando,graph.first_visit_locks)
    graph.add_logic(pr_logic)

    rampart_chests = graph.add_location(NodeId.RampartChests, [
        chest(70, CheckLocation.RampartNavalMap, pr),
        chest(219, CheckLocation.RampartMythrilStone, pr),
        chest(220, CheckLocation.RampartDarkShard, pr),
    ])
    rampart = graph.add_location(NodeId.Rampart, [])
    town_chests = graph.add_location(NodeId.PortRoyalTownChests, [
        chest(71, CheckLocation.TownDarkStone, pr),
        chest(72, CheckLocation.TownApBoost, pr),
        chest(73, CheckLocation.TownMythrilShard, pr),
        chest(221, CheckLocation.TownMythrilGem, pr),
    ])
    town = graph.add_location(NodeId.PortRoyalTown, [])
    cave_mouth_chests = graph.add_location(NodeId.CaveMouthChests, [
        chest(74, CheckLocation.CaveMouthBrightShard, pr),
        chest(223, CheckLocation.CaveMouthMythrilShard, pr),
    ])
    cave_mouth = graph.add_location(NodeId.CaveMouth, [])
    isla_de_muerta_popup = graph.add_location(NodeId.IslaDeMuertaPopup, [
        popup(329, CheckLocation.IslaDeMuertaMap, pr),
    ])
    boat_fight = graph.add_location(NodeId.BoatFight, [
        item_bonus(62, CheckLocation.BoatFight, pr, vanilla=ability.AerialSpiral),
    ])
    barrels_minigame = graph.add_location(NodeId.BarrelsMinigame, [
        stat_bonus(39, CheckLocation.InterceptorBarrels, pr),
    ])
    powder_store_chests = graph.add_location(NodeId.PowderStoreChests, [
        chest(369, CheckLocation.PowderStoreApBoost1, pr),
        chest(370, CheckLocation.PowderStoreApBoost2, pr),
    ])
    powder_store = graph.add_location(NodeId.PowderStore, [])
    moonlight_nook_chests = graph.add_location(NodeId.MoonlightNookChests, [
        chest(75, CheckLocation.MoonlightNookMythrilShard, pr),
        chest(224, CheckLocation.MoonlightNookSerenityGem, pr),
        chest(371, CheckLocation.MoonlightNookPowerStone, pr),
    ])
    moonlight_nook = graph.add_location(NodeId.MoonlightNook, [])
    barbossa = graph.add_location(NodeId.Barbossa, [
        hybrid_bonus(21, CheckLocation.Barbossa, pr, vanilla=ability.AerialFinish),
        popup(263, CheckLocation.FollowTheWind, pr, vanilla=keyblade.FollowTheWind),
    ])
    grim_reaper_1 = graph.add_location(NodeId.GrimReaper1, [
        item_bonus(59, CheckLocation.GrimReaper1, pr, vanilla=ability.HorizontalSlash),
    ])
    interceptors_hold_chests = graph.add_location(NodeId.InterceptorsHoldChests, [
        chest(252, CheckLocation.InterceptorsHoldFeatherCharm, pr, vanilla=summon.FeatherCharm),
    ])
    interceptors_hold = graph.add_location(NodeId.InterceptorsHold, [])
    seadrift_keep_chests = graph.add_location(NodeId.SeadriftKeepChests, [
        chest(76, CheckLocation.SeadriftKeepApBoost, pr),
        chest(225, CheckLocation.SeadriftKeepOrichalcum, pr),
        chest(372, CheckLocation.SeadriftKeepMeteorStaff, pr),
    ])
    seadrift_keep = graph.add_location(NodeId.SeadriftKeep, [])
    seadrift_row_chests = graph.add_location(NodeId.SeadriftRowChests, [
        chest(77, CheckLocation.SeadriftRowSerenityGem, pr),
        chest(78, CheckLocation.SeadriftRowKingRecipe, pr),
        chest(373, CheckLocation.SeadriftRowMythrilCrystal, pr),
    ])
    seadrift_row = graph.add_location(NodeId.SeadriftRow, [])
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
    
    graph.add_edge(rampart, rampart_chests)
    graph.add_edge(town, town_chests)
    graph.add_edge(cave_mouth, cave_mouth_chests)
    graph.add_edge(powder_store, powder_store_chests)
    graph.add_edge(moonlight_nook, moonlight_nook_chests)
    graph.add_edge(interceptors_hold, interceptors_hold_chests)
    graph.add_edge(seadrift_keep, seadrift_keep_chests)
    graph.add_edge(seadrift_row, seadrift_row_chests)

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
        graph.add_edge(barbossa, grim_reaper_1, RequirementEdge(battle=True))
        graph.add_edge(grim_reaper_1, interceptors_hold)
        graph.add_edge(interceptors_hold, seadrift_row)
        graph.add_edge(seadrift_row, seadrift_keep)
        graph.add_edge(seadrift_keep, cursed_medallion_popup, RequirementEdge(battle=True))
        graph.add_edge(cursed_medallion_popup, grim_reaper_2, RequirementEdge(battle=True))
        graph.add_edge(grim_reaper_2, data_luxord, RequirementEdge(battle=True))
        graph.register_first_boss(barbossa)
        graph.register_last_story_boss(grim_reaper_2)
    else:
        graph.add_edge(START_NODE, rampart)
        graph.add_edge(rampart, grim_reaper_1, RequirementEdge(battle=True))
        graph.add_edge(grim_reaper_1, interceptors_hold)
        graph.add_edge(interceptors_hold, seadrift_row)
        graph.add_edge(seadrift_row, seadrift_keep)
        graph.add_edge(seadrift_keep, cursed_medallion_popup, RequirementEdge(battle=True))
        graph.add_edge(cursed_medallion_popup, cave_mouth)
        graph.add_edge(cave_mouth, grim_reaper_2, RequirementEdge(battle=True))
        graph.add_edge(grim_reaper_2, town, RequirementEdge(battle=True))
        graph.add_edge(town, isla_de_muerta_popup, RequirementEdge(battle=True))
        graph.add_edge(isla_de_muerta_popup, boat_fight, RequirementEdge(battle=True))
        graph.add_edge(boat_fight, barrels_minigame)
        graph.add_edge(barrels_minigame, powder_store)
        graph.add_edge(powder_store, moonlight_nook)
        graph.add_edge(moonlight_nook, barbossa, RequirementEdge(battle=True))
        graph.add_edge(barbossa, data_luxord, RequirementEdge(battle=True))
        graph.register_first_boss(grim_reaper_2)
        graph.register_last_story_boss(barbossa)

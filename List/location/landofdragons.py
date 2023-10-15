from enum import Enum

from List.configDict import locationType
from List.inventory import misc, magic, keyblade, ability
from List.location.graph import RequirementEdge, chest, popup, item_bonus, hybrid_bonus, \
    LocationGraphBuilder, START_NODE
from Module.itemPlacementRestriction import ItemPlacementHelpers


class NodeId(str, Enum):
    BambooGrove = "Bamboo Grove"
    EncampmentAreaMap = "Encampment Area Map"
    Mission3 = "Mission 3"
    Checkpoint = "Checkpoint"
    MountainTrail = "Mountain Trail"
    VillageCaveMapPopup = "Village Cave Map Popup"
    VillageCave = "Village Cave"
    VillageCaveBonus = "Village Cave Bonus"
    Ridge = "Ridge"
    ShanYu = "Shan-Yu"
    ThroneRoom = "Throne Room"
    StormRider = "Storm Rider"
    DataXigbar = "Data Xigbar"


class CheckLocation(str, Enum):
    BambooGroveDarkShard = "Bamboo Grove Dark Shard"
    BambooGroveEther = "Bamboo Grove Ether"
    BambooGroveMythrilShard = "Bamboo Grove Mythril Shard"
    EncampmentAreaMap = "Encampment Area Map"
    Mission3 = "Mission 3"
    CheckpointHiPotion = "Checkpoint Hi-Potion"
    CheckpointMythrilShard = "Checkpoint Mythril Shard"
    MountainTrailLightningShard = "Mountain Trail Lightning Shard"
    MountainTrailRecoveryRecipe = "Mountain Trail Recovery Recipe"
    MountainTrailEther = "Mountain Trail Ether"
    MountainTrailMythrilShard = "Mountain Trail Mythril Shard"
    VillageCaveAreaMap = "Village Cave Area Map"
    VillageCaveApBoost = "Village Cave AP Boost"
    VillageCaveDarkShard = "Village Cave Dark Shard"
    VillageCaveBonus = "Village Cave Bonus"
    RidgeFrostShard = "Ridge Frost Shard"
    RidgeApBoost = "Ridge AP Boost"
    ShanYuBonus = "Shan-Yu"
    HiddenDragon = "Hidden Dragon"
    ThroneRoomTornPages = "Throne Room Torn Pages"
    ThroneRoomPalaceMap = "Throne Room Palace Map"
    ThroneRoomApBoost = "Throne Room AP Boost"
    ThroneRoomQueenRecipe = "Throne Room Queen Recipe"
    ThroneRoomApBoost2 = "Throne Room AP Boost (2)"
    ThroneRoomOgreShield = "Throne Room Ogre Shield"
    ThroneRoomMythrilCrystal = "Throne Room Mythril Crystal"
    ThroneRoomOrichalcum = "Throne Room Orichalcum"
    StormRiderBonus = "Storm Rider"
    DataXigbarDefenseBoost = "Xigbar (Data) Defense Boost"


def make_graph(graph: LocationGraphBuilder):
    lod = locationType.LoD

    bamboo_grove = graph.add_location(NodeId.BambooGrove, [
        chest(245, CheckLocation.BambooGroveDarkShard, lod),
        chest(497, CheckLocation.BambooGroveEther, lod),
        chest(498, CheckLocation.BambooGroveMythrilShard, lod),
    ])
    encampment_area_map = graph.add_location(NodeId.EncampmentAreaMap, [
        popup(350, CheckLocation.EncampmentAreaMap, lod),
    ])
    mission3 = graph.add_location(NodeId.Mission3, [
        popup(417, CheckLocation.Mission3, lod),
    ])
    checkpoint = graph.add_location(NodeId.Checkpoint, [
        chest(21, CheckLocation.CheckpointHiPotion, lod),
        chest(121, CheckLocation.CheckpointMythrilShard, lod),
    ])
    mountain_trail = graph.add_location(NodeId.MountainTrail, [
        chest(22, CheckLocation.MountainTrailLightningShard, lod),
        chest(23, CheckLocation.MountainTrailRecoveryRecipe, lod),
        chest(122, CheckLocation.MountainTrailEther, lod),
        chest(123, CheckLocation.MountainTrailMythrilShard, lod),
    ])
    village_cave_map_popup = graph.add_location(NodeId.VillageCaveMapPopup, [
        popup(495, CheckLocation.VillageCaveAreaMap, lod),
    ])
    village_cave = graph.add_location(NodeId.VillageCave, [
        chest(124, CheckLocation.VillageCaveApBoost, lod),
        chest(125, CheckLocation.VillageCaveDarkShard, lod),
    ])
    village_cave_bonus = graph.add_location(NodeId.VillageCaveBonus, [
        item_bonus(43, CheckLocation.VillageCaveBonus, lod, vanilla=ability.SlideDash),
    ])
    ridge = graph.add_location(NodeId.Ridge, [
        chest(24, CheckLocation.RidgeFrostShard, lod),
        chest(126, CheckLocation.RidgeApBoost, lod),
    ])
    shan_yu = graph.add_location(NodeId.ShanYu, [
        hybrid_bonus(9, CheckLocation.ShanYuBonus, lod, vanilla=ability.AerialSweep),
        popup(257, CheckLocation.HiddenDragon, lod, vanilla=keyblade.HiddenDragon),
    ])
    throne_room = graph.add_location(NodeId.ThroneRoom, [
        chest(25, CheckLocation.ThroneRoomTornPages, lod, vanilla=misc.TornPages),
        chest(127, CheckLocation.ThroneRoomPalaceMap, lod),
        chest(26, CheckLocation.ThroneRoomApBoost, lod),
        chest(27, CheckLocation.ThroneRoomQueenRecipe, lod),
        chest(128, CheckLocation.ThroneRoomApBoost2, lod),
        chest(129, CheckLocation.ThroneRoomOgreShield, lod),
        chest(130, CheckLocation.ThroneRoomMythrilCrystal, lod),
        chest(131, CheckLocation.ThroneRoomOrichalcum, lod),
    ])
    storm_rider = graph.add_location(NodeId.StormRider, [
        item_bonus(10, CheckLocation.StormRiderBonus, lod, vanilla=magic.Thunder),
    ])
    data_xigbar = graph.add_location(NodeId.DataXigbar, [
        popup(555, CheckLocation.DataXigbarDefenseBoost, [lod, locationType.DataOrg]),
    ])

    graph.register_superboss(data_xigbar)

    if not graph.reverse_rando:
        graph.add_edge(START_NODE, bamboo_grove)
        graph.add_edge(bamboo_grove, encampment_area_map)
        graph.add_edge(encampment_area_map, mission3, RequirementEdge(battle=True))
        graph.add_edge(encampment_area_map, checkpoint)
        graph.add_edge(mission3, mountain_trail, RequirementEdge(battle=True))
        graph.add_edge(mountain_trail, village_cave_map_popup, RequirementEdge(battle=True))
        graph.add_edge(village_cave_map_popup, village_cave)
        graph.add_edge(village_cave, village_cave_bonus, RequirementEdge(battle=True))
        graph.add_edge(village_cave_bonus, ridge)
        graph.add_edge(ridge, shan_yu, RequirementEdge(battle=True))
        graph.add_edge(shan_yu, throne_room, RequirementEdge(battle=True, req=ItemPlacementHelpers.mulan_check))
        graph.add_edge(throne_room, storm_rider, RequirementEdge(battle=True))
        graph.add_edge(storm_rider, data_xigbar, RequirementEdge(battle=True))
        graph.register_first_boss(shan_yu)
        graph.register_last_story_boss(storm_rider)
    else:
        graph.add_edge(START_NODE, mountain_trail)
        graph.add_edge(mountain_trail, checkpoint)
        graph.add_edge(mountain_trail, ridge)
        graph.add_edge(ridge, throne_room, RequirementEdge(battle=True))
        graph.add_edge(throne_room, storm_rider, RequirementEdge(battle=True))
        graph.add_edge(storm_rider, bamboo_grove, RequirementEdge(req=ItemPlacementHelpers.mulan_check))
        graph.add_edge(bamboo_grove, encampment_area_map, RequirementEdge(battle=True))
        graph.add_edge(encampment_area_map, mission3)
        graph.add_edge(mission3, village_cave_map_popup, RequirementEdge(battle=True))
        graph.add_edge(village_cave_map_popup, village_cave)
        graph.add_edge(village_cave, village_cave_bonus, RequirementEdge(battle=True))
        graph.add_edge(village_cave_bonus, shan_yu, RequirementEdge(battle=True))
        graph.add_edge(shan_yu, data_xigbar, RequirementEdge(battle=True))
        graph.register_first_boss(storm_rider)
        graph.register_last_story_boss(shan_yu)

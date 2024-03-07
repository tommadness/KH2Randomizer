from enum import Enum

from List.configDict import locationType
from List.inventory import magic, keyblade, ability, report
from List.location.graph import DefaultLogicGraph, RequirementEdge, chest, popup, item_bonus, stat_bonus, hybrid_bonus, \
    LocationGraphBuilder, START_NODE
from Module.itemPlacementRestriction import ItemPlacementHelpers


class NodeId(str, Enum):
    BeastsCastleCourtyard = "BC Courtyard"
    BeastsCastleCourtyardChests = "BC Courtyard Chests"
    BellesRoom = "Belle's Room"
    BellesRoomChests = "Belle's Room Chests"
    EastWing = "East Wing"
    EastWingChests = "East Wing Chests"
    WestHall = "West Hall"
    WestHallChests = "West Hall Chests"
    Thresholder = "Thresholder"
    Dungeon = "Dungeon"
    DungeonChests = "Dungeon Chests"
    SecretPassage = "Secret Passage"
    SecretPassageChests = "Secret Passage Chests"
    WestHallPostDungeon = "West Hall Post Dungeon"
    WestHallPostDungeonChests = "West Hall Post Dungeon Chests"
    WestWing = "West Wing"
    WestWingChests = "West Wing Chests"
    BeastBonus = "Beast Bonus"
    BeastsRoom = "Beast's Room"
    BeastsRoomChests = "Beast's Room Chests"
    DarkThorn = "Dark Thorn"
    RumblingRose = "Rumbling Rose"
    Xaldin = "Xaldin"
    DataXaldin = "Data Xaldin"


class CheckLocation(str, Enum):
    CourtyardApBoost = "BC Courtyard AP Boost"
    CourtyardHiPotion = "BC Courtyard Hi-Potion"
    CourtyardMythrilShard = "BC Courtyard Mythril Shard"
    BellesRoomCastleMap = "Belle's Room Castle Map"
    BellesRoomMegaRecipe = "Belle's Room Mega-Recipe"
    EastWingMythrilShard = "The East Wing Mythril Shard"
    EastWingTent = "The East Wing Tent"
    WestHallHiPotion = "The West Hall Hi-Potion"
    WestHallPowerShard = "The West Hall Power Shard"
    WestHallMythrilShard2 = "The West Hall Mythril Shard (2)"
    WestHallBrightStone = "The West Hall Bright Stone"
    WestHallMythrilShard = "The West Hall Mythril Shard"
    Thresholder = "Thresholder"
    DungeonBasementMap = "Dungeon Basement Map"
    DungeonApBoost = "Dungeon AP Boost"
    SecretPassageMythrilShard = "Secret Passage Mythril Shard"
    SecretPassageHiPotion = "Secret Passage Hi-Potion"
    SecretPassageLucidShard = "Secret Passage Lucid Shard"
    WestHallPostDungeonApBoost = "The West Hall AP Boost (Post Dungeon)"
    WestWingMythrilShard = "The West Wing Mythril Shard"
    WestWingTent = "The West Wing Tent"
    Beast = "Beast"
    BeastsRoomBlazingShard = "The Beast's Room Blazing Shard"
    DarkThorn = "Dark Thorn Bonus"
    DarkThornCureElement = "Dark Thorn Cure Element"
    RumblingRose = "Rumbling Rose"
    CastleWallsMap = "Castle Walls Map"
    XaldinBonus = "Xaldin Bonus"
    XaldinSecretAnsemReport4 = "Secret Ansem Report 4"
    DataXaldin = "Xaldin (Data) Defense Boost"

class BCLogicGraph(DefaultLogicGraph):
    def __init__(self,reverse_rando,first_visit_locks):
        DefaultLogicGraph.__init__(self,NodeId)
        if not reverse_rando:
            self.logic[NodeId.BeastsCastleCourtyard][NodeId.BeastsCastleCourtyardChests] = ItemPlacementHelpers.need_bc_keyblade
            self.logic[NodeId.BellesRoom][NodeId.BellesRoomChests] = ItemPlacementHelpers.need_bc_keyblade
            self.logic[NodeId.EastWing][NodeId.EastWingChests] = ItemPlacementHelpers.need_bc_keyblade
            self.logic[NodeId.WestHall][NodeId.WestHallChests] = ItemPlacementHelpers.need_bc_keyblade
            self.logic[NodeId.Dungeon][NodeId.DungeonChests] = ItemPlacementHelpers.need_bc_keyblade
            self.logic[NodeId.SecretPassage][NodeId.SecretPassageChests] = ItemPlacementHelpers.need_bc_keyblade
            self.logic[NodeId.WestHallPostDungeon][NodeId.WestHallPostDungeonChests] = ItemPlacementHelpers.need_bc_keyblade
            self.logic[NodeId.WestWing][NodeId.WestWingChests] = ItemPlacementHelpers.need_bc_keyblade
            self.logic[NodeId.BeastsRoom][NodeId.BeastsRoomChests] = ItemPlacementHelpers.need_bc_keyblade
            self.logic[START_NODE][NodeId.BeastsCastleCourtyard] = ItemPlacementHelpers.bc1_check
            self.logic[NodeId.DarkThorn][NodeId.RumblingRose] = ItemPlacementHelpers.bc2_check
        else:
            self.logic[NodeId.Xaldin][NodeId.BeastsCastleCourtyard] = ItemPlacementHelpers.bc2_check

def make_graph(graph: LocationGraphBuilder):
    bc = locationType.BC
    bc_logic = BCLogicGraph(graph.reverse_rando,graph.first_visit_locks)
    graph.add_logic(bc_logic)

    courtyard_chests = graph.add_location(NodeId.BeastsCastleCourtyardChests, [
        chest(39, CheckLocation.CourtyardApBoost, bc),
        chest(40, CheckLocation.CourtyardHiPotion, bc),
        chest(505, CheckLocation.CourtyardMythrilShard, bc),
    ])
    courtyard = graph.add_location(NodeId.BeastsCastleCourtyard, [])
    belles_room_chests = graph.add_location(NodeId.BellesRoomChests, [
        chest(46, CheckLocation.BellesRoomCastleMap, bc),
        chest(240, CheckLocation.BellesRoomMegaRecipe, bc),
    ])
    belles_room = graph.add_location(NodeId.BellesRoom, [])
    east_wing_chests = graph.add_location(NodeId.EastWingChests, [
        chest(63, CheckLocation.EastWingMythrilShard, bc),
        chest(155, CheckLocation.EastWingTent, bc),
    ])
    east_wing = graph.add_location(NodeId.EastWing, [])
    west_hall_chests = graph.add_location(NodeId.WestHallChests, [
        chest(41, CheckLocation.WestHallHiPotion, bc),
        chest(207, CheckLocation.WestHallPowerShard, bc),
        chest(208, CheckLocation.WestHallMythrilShard2, bc),
        chest(159, CheckLocation.WestHallBrightStone, bc),
        chest(206, CheckLocation.WestHallMythrilShard, bc),
    ])
    west_hall = graph.add_location(NodeId.WestHall, [])
    thresholder = graph.add_location(NodeId.Thresholder, [
        item_bonus(2, CheckLocation.Thresholder, bc, vanilla=ability.UpperSlash),
    ])
    dungeon_chests = graph.add_location(NodeId.DungeonChests, [
        chest(239, CheckLocation.DungeonBasementMap, bc),
        chest(43, CheckLocation.DungeonApBoost, bc),
    ])
    dungeon = graph.add_location(NodeId.Dungeon, [])
    secret_passage_chests = graph.add_location(NodeId.SecretPassageChests, [
        chest(44, CheckLocation.SecretPassageMythrilShard, bc),
        chest(168, CheckLocation.SecretPassageHiPotion, bc),
        chest(45, CheckLocation.SecretPassageLucidShard, bc),
    ])
    secret_passage = graph.add_location(NodeId.SecretPassage, [])
    west_hall_post_dungeon_chests = graph.add_location(NodeId.WestHallPostDungeonChests, [
        chest(158, CheckLocation.WestHallPostDungeonApBoost, bc),
    ])
    west_hall_post_dungeon = graph.add_location(NodeId.WestHallPostDungeon, [])
    west_wing_chests = graph.add_location(NodeId.WestWingChests, [
        chest(42, CheckLocation.WestWingMythrilShard, bc),
        chest(164, CheckLocation.WestWingTent, bc),
    ])
    west_wing = graph.add_location(NodeId.WestWing, [])
    beast_bonus = graph.add_location(NodeId.BeastBonus, [
        stat_bonus(12, CheckLocation.Beast, bc),
    ])
    beasts_room_chests = graph.add_location(NodeId.BeastsRoomChests, [
        chest(241, CheckLocation.BeastsRoomBlazingShard, bc),
    ])
    beasts_room = graph.add_location(NodeId.BeastsRoom, [])
    dark_thorn = graph.add_location(NodeId.DarkThorn, [
        hybrid_bonus(3, CheckLocation.DarkThorn, bc, vanilla=ability.RetaliatingSlash),
        popup(299, CheckLocation.DarkThornCureElement, bc, vanilla=magic.Cure),
    ])
    rumbling_rose = graph.add_location(NodeId.RumblingRose, [
        popup(270, CheckLocation.RumblingRose, bc, vanilla=keyblade.RumblingRose),
        popup(325, CheckLocation.CastleWallsMap, bc),
    ])
    xaldin = graph.add_location(NodeId.Xaldin, [
        hybrid_bonus(4, CheckLocation.XaldinBonus, bc, vanilla=magic.Reflect),
        popup(528, CheckLocation.XaldinSecretAnsemReport4, bc, vanilla=report.AnsemReport4),
    ])
    data_xaldin = graph.add_location(NodeId.DataXaldin, [
        popup(559, CheckLocation.DataXaldin, [bc, locationType.DataOrg]),
    ])

    graph.register_superboss(data_xaldin)
    
    graph.add_edge(courtyard, courtyard_chests)
    graph.add_edge(belles_room, belles_room_chests)
    graph.add_edge(east_wing, east_wing_chests)
    graph.add_edge(west_hall, west_hall_chests)
    graph.add_edge(dungeon, dungeon_chests)
    graph.add_edge(secret_passage, secret_passage_chests)
    graph.add_edge(west_hall_post_dungeon, west_hall_post_dungeon_chests)
    graph.add_edge(west_wing, west_wing_chests)
    graph.add_edge(beasts_room, beasts_room_chests)

    if not graph.reverse_rando:
        graph.add_edge(START_NODE, courtyard)
        graph.add_edge(courtyard, belles_room)
        graph.add_edge(belles_room, east_wing)
        graph.add_edge(courtyard, west_hall)
        graph.add_edge(west_hall, thresholder, RequirementEdge(battle=True))
        graph.add_edge(thresholder, dungeon)
        graph.add_edge(dungeon, secret_passage)
        graph.add_edge(secret_passage, west_hall_post_dungeon)
        graph.add_edge(west_hall_post_dungeon, west_wing)
        graph.add_edge(west_wing, beast_bonus, RequirementEdge(battle=True))
        graph.add_edge(beast_bonus, beasts_room)
        graph.add_edge(beasts_room, dark_thorn, RequirementEdge(battle=True))
        graph.add_edge(dark_thorn, rumbling_rose, RequirementEdge(battle=True))
        graph.add_edge(rumbling_rose, xaldin, RequirementEdge(battle=True))
        graph.add_edge(xaldin, data_xaldin, RequirementEdge(battle=True))
        graph.register_first_boss(dark_thorn)
        graph.register_last_story_boss(xaldin)
    else:
        graph.add_edge(START_NODE, west_hall, RequirementEdge(battle=True))
        graph.add_edge(west_hall, west_hall_post_dungeon)
        graph.add_edge(west_hall, west_wing)
        graph.add_edge(west_wing, beasts_room)
        graph.add_edge(beasts_room, rumbling_rose)
        graph.add_edge(rumbling_rose, xaldin, RequirementEdge(battle=True))
        graph.add_edge(xaldin, courtyard)
        graph.add_edge(courtyard, belles_room)
        graph.add_edge(belles_room, east_wing)
        graph.add_edge(east_wing, thresholder, RequirementEdge(battle=True))
        graph.add_edge(thresholder, dungeon)
        graph.add_edge(dungeon, secret_passage)
        graph.add_edge(secret_passage, beast_bonus, RequirementEdge(battle=True))
        graph.add_edge(beast_bonus, dark_thorn, RequirementEdge(battle=True))
        graph.add_edge(dark_thorn, data_xaldin, RequirementEdge(battle=True))
        graph.register_first_boss(xaldin)
        graph.register_last_story_boss(dark_thorn)

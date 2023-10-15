from enum import Enum

from List.configDict import locationType
from List.inventory import misc, magic, keyblade, ability, summon
from List.location.graph import RequirementEdge, chest, popup, item_bonus, stat_bonus, \
    LocationGraphBuilder, START_NODE
from Module.itemPlacementRestriction import ItemPlacementHelpers


class NodeId(str, Enum):
    AgrabahMapPopup = "Agrabah Map Popup"
    Agrabah = "Agrabah"
    Bazaar = "Bazaar"
    PalaceWalls = "Palace Walls"
    CaveOfWondersEntrance = "Cave of Wonders Entrance"
    ValleyOfStone = "Valley of Stone"
    AbuEscort = "Abu Escort"
    ChasmOfChallenges = "Chasm of Challenges"
    TreasureRoomBonus = "Treasure Room Bonus"
    TreasureRoom = "Treasure Room"
    ElementalLords = "Elemental Lords"
    RuinedChamber = "Ruined Chamber"
    GenieJafar = "Genie Jafar"
    Lexaeus = "AS Lexaeus"
    DataLexaeus = "Data Lexaeus"


class CheckLocation(str, Enum):
    AgrabahMap = "Agrabah Map"
    AgrabahDarkShard = "Agrabah Dark Shard"
    AgrabahMythrilShard = "Agrabah Mythril Shard"
    AgrabahHiPotion = "Agrabah Hi-Potion"
    AgrabahApBoost = "Agrabah AP Boost"
    AgrabahMythrilStone = "Agrabah Mythril Stone"
    AgrabahMythrilShard2 = "Agrabah Mythril Shard (2)"
    AgrabahSerenityShard = "Agrabah Serenity Shard"
    BazaarMythrilGem = "Bazaar Mythril Gem"
    BazaarPowerShard = "Bazaar Power Shard"
    BazaarHiPotion = "Bazaar Hi-Potion"
    BazaarApBoost = "Bazaar AP Boost"
    BazaarMythrilShard = "Bazaar Mythril Shard"
    PalaceWallsSkillRing = "Palace Walls Skill Ring"
    PalaceWallsMythrilStone = "Palace Walls Mythril Stone"
    CaveEntrancePowerStone = "Cave Entrance Power Stone"
    CaveEntranceMythrilShard = "Cave Entrance Mythril Shard"
    ValleyOfStoneMythrilStone = "Valley of Stone Mythril Stone"
    ValleyOfStoneApBoost = "Valley of Stone AP Boost"
    ValleyOfStoneMythrilShard = "Valley of Stone Mythril Shard"
    ValleyOfStoneHiPotion = "Valley of Stone Hi-Potion"
    AbuEscort = "Abu Escort"
    ChasmOfChallengesCaveOfWondersMap = "Chasm of Challenges Cave of Wonders Map"
    ChasmOfChallengesApBoost = "Chasm of Challenges AP Boost"
    TreasureRoomBonus = "Treasure Room"
    TreasureRoomApBoost = "Treasure Room AP Boost"
    TreasureRoomSerenityGem = "Treasure Room Serenity Gem"
    ElementalLordsBonus = "Elemental Lords"
    LampCharm = "Lamp Charm"
    RuinedChamberTornPages = "Ruined Chamber Torn Pages"
    RuinedChamberRuinsMap = "Ruined Chamber Ruins Map"
    GenieJafarBonus = "Genie Jafar"
    WishingLamp = "Wishing Lamp"
    LexaeusBonus = "Lexaeus Bonus"
    LexaeusStrengthBeyondStrength = "Lexaeus (AS) Strength Beyond Strength"
    DataLexaeus = "Lexaeus (Data) Lost Illusion"


def make_graph(graph: LocationGraphBuilder):
    ag = locationType.Agrabah

    agrabah_map_popup = graph.add_location(NodeId.AgrabahMapPopup, [
        popup(353, CheckLocation.AgrabahMap, ag),
    ])
    agrabah = graph.add_location(NodeId.Agrabah, [
        chest(28, CheckLocation.AgrabahDarkShard, ag),
        chest(29, CheckLocation.AgrabahMythrilShard, ag),
        chest(30, CheckLocation.AgrabahHiPotion, ag),
        chest(132, CheckLocation.AgrabahApBoost, ag),
        chest(133, CheckLocation.AgrabahMythrilStone, ag),
        chest(249, CheckLocation.AgrabahMythrilShard2, ag),
        chest(501, CheckLocation.AgrabahSerenityShard, ag),
    ])
    bazaar = graph.add_location(NodeId.Bazaar, [
        chest(31, CheckLocation.BazaarMythrilGem, ag),
        chest(32, CheckLocation.BazaarPowerShard, ag),
        chest(33, CheckLocation.BazaarHiPotion, ag),
        chest(134, CheckLocation.BazaarApBoost, ag),
        chest(135, CheckLocation.BazaarMythrilShard, ag),
    ])
    palace_walls = graph.add_location(NodeId.PalaceWalls, [
        chest(136, CheckLocation.PalaceWallsSkillRing, ag),
        chest(520, CheckLocation.PalaceWallsMythrilStone, ag),
    ])
    cave_of_wonders_entrance = graph.add_location(NodeId.CaveOfWondersEntrance, [
        chest(250, CheckLocation.CaveEntrancePowerStone, ag),
        chest(251, CheckLocation.CaveEntranceMythrilShard, ag),
    ])
    valley_of_stone = graph.add_location(NodeId.ValleyOfStone, [
        chest(35, CheckLocation.ValleyOfStoneMythrilStone, ag),
        chest(36, CheckLocation.ValleyOfStoneApBoost, ag),
        chest(137, CheckLocation.ValleyOfStoneMythrilShard, ag),
        chest(138, CheckLocation.ValleyOfStoneHiPotion, ag),
    ])
    abu_escort = graph.add_location(NodeId.AbuEscort, [
        item_bonus(42, CheckLocation.AbuEscort, ag, vanilla=ability.SummonBoost),
    ])
    chasm_of_challenges = graph.add_location(NodeId.ChasmOfChallenges, [
        chest(487, CheckLocation.ChasmOfChallengesCaveOfWondersMap, ag),
        chest(37, CheckLocation.ChasmOfChallengesApBoost, ag),
    ])
    treasure_room_bonus = graph.add_location(NodeId.TreasureRoomBonus, [
        stat_bonus(46, CheckLocation.TreasureRoomBonus, ag),
    ])
    treasure_room = graph.add_location(NodeId.TreasureRoom, [
        chest(502, CheckLocation.TreasureRoomApBoost, ag),
        chest(503, CheckLocation.TreasureRoomSerenityGem, ag),
    ])
    elemental_lords = graph.add_location(NodeId.ElementalLords, [
        item_bonus(37, CheckLocation.ElementalLordsBonus, ag, vanilla=ability.FinishingLeap),
        popup(300, CheckLocation.LampCharm, ag, vanilla=summon.LampCharm),
    ])
    ruined_chamber = graph.add_location(NodeId.RuinedChamber, [
        chest(34, CheckLocation.RuinedChamberTornPages, ag, vanilla=misc.TornPages),
        chest(486, CheckLocation.RuinedChamberRuinsMap, ag),
    ])
    genie_jafar = graph.add_location(NodeId.GenieJafar, [
        item_bonus(15, CheckLocation.GenieJafarBonus, ag, vanilla=magic.Fire),
        popup(303, CheckLocation.WishingLamp, ag, vanilla=keyblade.WishingLamp),
    ])
    lexaeus = graph.add_location(NodeId.Lexaeus, [
        stat_bonus(65, CheckLocation.LexaeusBonus, [ag, locationType.AS]),
        popup(545, CheckLocation.LexaeusStrengthBeyondStrength, [ag, locationType.AS]),
    ])
    data_lexaeus = graph.add_location(NodeId.DataLexaeus, [
        popup(550, CheckLocation.DataLexaeus, [ag, locationType.DataOrg]),
    ])

    graph.register_superboss(data_lexaeus)

    if not graph.reverse_rando:
        graph.add_edge(START_NODE, agrabah_map_popup)
        graph.add_edge(agrabah_map_popup, agrabah)
        graph.add_edge(agrabah, bazaar)
        graph.add_edge(bazaar, palace_walls)
        graph.add_edge(palace_walls, cave_of_wonders_entrance)
        graph.add_edge(cave_of_wonders_entrance, valley_of_stone)
        graph.add_edge(valley_of_stone, abu_escort)
        graph.add_edge(abu_escort, chasm_of_challenges, RequirementEdge(battle=True))
        graph.add_edge(chasm_of_challenges, treasure_room_bonus, RequirementEdge(battle=True))
        graph.add_edge(treasure_room_bonus, treasure_room)
        graph.add_edge(treasure_room, elemental_lords, RequirementEdge(battle=True))
        graph.add_edge(elemental_lords, ruined_chamber, RequirementEdge(battle=True, req=lambda
            inv: ItemPlacementHelpers.need_fire_blizzard_thunder(inv) and ItemPlacementHelpers.aladdin_check(inv)))
        graph.add_edge(ruined_chamber, genie_jafar, RequirementEdge(battle=True))
        graph.add_edge(genie_jafar, lexaeus, RequirementEdge(battle=True))
        graph.add_edge(lexaeus, data_lexaeus)
        graph.register_superboss(lexaeus)
        graph.register_first_boss(elemental_lords)
        graph.register_last_story_boss(genie_jafar)
    else:
        graph.add_edge(START_NODE, agrabah)
        graph.add_edge(agrabah, bazaar)
        graph.add_edge(bazaar, palace_walls)
        graph.add_edge(palace_walls, ruined_chamber,
                       RequirementEdge(battle=True, req=ItemPlacementHelpers.need_fire_blizzard_thunder))
        graph.add_edge(ruined_chamber, genie_jafar, RequirementEdge(battle=True))
        graph.add_edge(genie_jafar, lexaeus, RequirementEdge(battle=True))
        graph.add_edge(lexaeus, agrabah_map_popup, RequirementEdge(req=ItemPlacementHelpers.aladdin_check))
        graph.add_edge(agrabah_map_popup, cave_of_wonders_entrance)
        graph.add_edge(cave_of_wonders_entrance, valley_of_stone)
        graph.add_edge(valley_of_stone, abu_escort)
        graph.add_edge(abu_escort, chasm_of_challenges, RequirementEdge(battle=True))
        graph.add_edge(chasm_of_challenges, treasure_room_bonus, RequirementEdge(battle=True))
        graph.add_edge(treasure_room_bonus, treasure_room)
        graph.add_edge(treasure_room, elemental_lords, RequirementEdge(battle=True))
        graph.add_edge(elemental_lords, data_lexaeus, RequirementEdge(battle=True))
        graph.register_first_boss(genie_jafar)
        graph.register_last_story_boss(elemental_lords)

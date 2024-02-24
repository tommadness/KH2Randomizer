from enum import Enum

from List.configDict import locationType
from List.inventory import keyblade, ability, report, form, misc
from List.location.graph import DefaultLogicGraph, RequirementEdge, chest, popup, stat_bonus, item_bonus, \
    LocationGraphBuilder, START_NODE
from Module.itemPlacementRestriction import ItemPlacementHelpers


class NodeId(str, Enum):
    OldMansion = "Old Mansion"
    Woods = "Woods"
    TramCommon = "Tram Common"
    StationFightPopup = "Station Fight Popup"
    CentralStation = "TT Central Station"
    YenSidTower = "Yensid Tower"
    YenSidTowerEntryway = "Yensid Tower Entryway"
    SorcerersLoft = "Sorcerer's Loft"
    TowerWardrobe = "Tower Wardrobe"
    ValorForm = "Valor Form"
    SeifersTrophy = "Seifer's Trophy"
    LimitForm = "Limit Form"
    UndergroundConcourse = "Underground Concourse"
    Tunnelway = "Tunnelway"
    SunsetTerrace = "TT Sunset Terrace"
    MansionBonus = "TT Mansion Bonus"
    MansionFoyer = "TT Mansion Foyer"
    MansionDiningRoom = "TT Mansion Dining Room"
    MansionLibrary = "TT Mansion Library"
    TwilightTownBeam = "TT Beam"
    MansionBasement = "TT Mansion Basement"
    BetwixtAndBetween = "Betwixt and Between"
    DataAxel = "Data Axel"


class CheckLocation(str, Enum):
    OldMansionPotion = "Old Mansion Potion"
    OldMansionMythrilShard = "Old Mansion Mythril Shard"
    WoodsPotion = "The Woods Potion"
    WoodsMythrilShard = "The Woods Mythril Shard"
    WoodsHiPotion = "The Woods Hi-Potion"
    TramCommonHiPotion = "Tram Common Hi-Potion"
    TramCommonApBoost = "Tram Common AP Boost"
    TramCommonTent = "Tram Common Tent"
    TramCommonMythrilShard1 = "Tram Common Mythril Shard (1)"
    TramCommonPotion1 = "Tram Common Potion (1)"
    TramCommonMythrilShard2 = "Tram Common Mythril Shard (2)"
    TramCommonPotion2 = "Tram Common Potion (2)"
    StationPlazaSecretAnsemReport2 = "Station Plaza Secret Ansem Report 2"
    MunnyPouchMickey = "Munny Pouch (Mickey)"
    CrystalOrb = "Crystal Orb"
    CentralStationTent = "Central Station Tent"
    CentralStationHiPotion = "TT Central Station Hi-Potion"
    CentralStationMythrilShard = "Central Station Mythril Shard"
    TowerPotion = "The Tower Potion"
    TowerHiPotion = "The Tower Hi-Potion"
    TowerEther = "The Tower Ether"
    TowerEntrywayEther = "Tower Entryway Ether"
    TowerEntrywayMythrilShard = "Tower Entryway Mythril Shard"
    SorcerersLoftTowerMap = "Sorcerer's Loft Tower Map"
    TowerWardrobeMythrilStone = "Tower Wardrobe Mythril Stone"
    StarSeeker = "Star Seeker"
    ValorForm = "Valor Form"
    SeifersTrophy = "Seifer´s Trophy"
    Oathkeeper = "Oathkeeper"
    LimitForm = "Limit Form"
    UndergroundConcourseMythrilGem = "Underground Concourse Mythril Gem"
    UndergroundConcourseOrichalcum = "Underground Concourse Orichalcum"
    UndergroundConcourseApBoost = "Underground Concourse AP Boost"
    UndergroundConcourseMythrilCrystal = "Underground Concourse Mythril Crystal"
    TunnelwayOrichalcum = "Tunnelway Orichalcum"
    TunnelwayMythrilCrystal = "Tunnelway Mythril Crystal"
    SunsetTerraceOrichalcumPlus = "Sunset Terrace Orichalcum+"
    SunsetTerraceMythrilShard = "Sunset Terrace Mythril Shard"
    SunsetTerraceMythrilCrystal = "Sunset Terrace Mythril Crystal"
    SunsetTerraceApBoost = "Sunset Terrace AP Boost"
    MansionNobodies = "Mansion Nobodies"
    MansionFoyerMythrilCrystal = "Mansion Foyer Mythril Crystal"
    MansionFoyerMythrilStone = "Mansion Foyer Mythril Stone"
    MansionFoyerSerenityCrystal = "Mansion Foyer Serenity Crystal"
    MansionDiningRoomMythrilCrystal = "Mansion Dining Room Mythril Crystal"
    MansionDiningRoomMythrilStone = "Mansion Dining Room Mythril Stone"
    MansionLibraryOrichalcum = "Mansion Library Orichalcum"
    BeamSecretAnsemReport10 = "Beam Secret Ansem Report 10"
    MansionBasementCorridorUltimateRecipe = "Mansion Basement Corridor Ultimate Recipe"
    BetwixtAndBetween = "Betwixt and Between"
    BetwixtAndBetweenBondOfFlame = "Betwixt and Between Bond of Flame"
    DataAxelMagicBoost = "Axel (Data) Magic Boost"

class TTLogicGraph(DefaultLogicGraph):
    def __init__(self,reverse_rando,first_visit_locks):
        DefaultLogicGraph.__init__(self,NodeId)
        if not reverse_rando:
            self.logic[START_NODE][NodeId.OldMansion] = ItemPlacementHelpers.tt1_check
            self.logic[NodeId.ValorForm][NodeId.SeifersTrophy] = ItemPlacementHelpers.tt2_check
            self.logic[NodeId.LimitForm][NodeId.UndergroundConcourse] = ItemPlacementHelpers.tt3_check
            self.logic[NodeId.LimitForm][NodeId.MansionBonus] = ItemPlacementHelpers.tt3_check
        else:
            self.logic[NodeId.BetwixtAndBetween][NodeId.SeifersTrophy] = ItemPlacementHelpers.tt2_check
            self.logic[NodeId.LimitForm][NodeId.StationFightPopup] = ItemPlacementHelpers.tt3_check

def make_graph(graph: LocationGraphBuilder):
    tt = locationType.TT
    tt_logic = TTLogicGraph(graph.reverse_rando,graph.first_visit_locks)
    graph.add_logic(tt_logic)

    old_mansion = graph.add_location(NodeId.OldMansion, [
        chest(447, CheckLocation.OldMansionPotion, tt),
        chest(448, CheckLocation.OldMansionMythrilShard, tt),
    ])
    woods = graph.add_location(NodeId.Woods, [
        chest(442, CheckLocation.WoodsPotion, tt),
        chest(443, CheckLocation.WoodsMythrilShard, tt),
        chest(444, CheckLocation.WoodsHiPotion, tt),
    ])
    tram_common = graph.add_location(NodeId.TramCommon, [
        chest(420, CheckLocation.TramCommonHiPotion, tt),
        chest(421, CheckLocation.TramCommonApBoost, tt),
        chest(422, CheckLocation.TramCommonTent, tt),
        chest(423, CheckLocation.TramCommonMythrilShard1, tt),
        chest(424, CheckLocation.TramCommonPotion1, tt),
        chest(425, CheckLocation.TramCommonMythrilShard2, tt),
        chest(484, CheckLocation.TramCommonPotion2, tt),
    ])
    station_fight_popup = graph.add_location(NodeId.StationFightPopup, [
        popup(526, CheckLocation.StationPlazaSecretAnsemReport2, tt, vanilla=report.AnsemReport2),
        popup(290, CheckLocation.MunnyPouchMickey, tt, vanilla=misc.MunnyPouchMickey),
        popup(291, CheckLocation.CrystalOrb, tt),
    ])
    central_station = graph.add_location(NodeId.CentralStation, [
        chest(431, CheckLocation.CentralStationTent, tt),
        chest(432, CheckLocation.CentralStationHiPotion, tt),
        chest(433, CheckLocation.CentralStationMythrilShard, tt),
    ])
    yen_sid_tower = graph.add_location(NodeId.YenSidTower, [
        chest(465, CheckLocation.TowerPotion, tt),
        chest(466, CheckLocation.TowerHiPotion, tt),
        chest(522, CheckLocation.TowerEther, tt),
    ])
    yen_sid_tower_entryway = graph.add_location(NodeId.YenSidTowerEntryway, [
        chest(467, CheckLocation.TowerEntrywayEther, tt),
        chest(468, CheckLocation.TowerEntrywayMythrilShard, tt),
    ])
    sorcerers_loft = graph.add_location(NodeId.SorcerersLoft, [
        chest(469, CheckLocation.SorcerersLoftTowerMap, tt),
    ])
    tower_wardrobe = graph.add_location(NodeId.TowerWardrobe, [
        chest(470, CheckLocation.TowerWardrobeMythrilStone, tt),
    ])
    valor_form = graph.add_location(NodeId.ValorForm, [
        popup(304, CheckLocation.StarSeeker, tt, vanilla=keyblade.StarSeeker),
        popup(286, CheckLocation.ValorForm, tt, vanilla=form.ValorForm),
    ])
    seifers_trophy = graph.add_location(NodeId.SeifersTrophy, [
        popup(294, CheckLocation.SeifersTrophy, tt),
    ])
    limit_form = graph.add_location(NodeId.LimitForm, [
        popup(265, CheckLocation.Oathkeeper, tt, vanilla=keyblade.Oathkeeper),
        popup(543, CheckLocation.LimitForm, tt, vanilla=form.LimitForm),
    ])
    underground_concourse = graph.add_location(NodeId.UndergroundConcourse, [
        chest(479, CheckLocation.UndergroundConcourseMythrilGem, tt),
        chest(480, CheckLocation.UndergroundConcourseOrichalcum, tt),
        chest(481, CheckLocation.UndergroundConcourseApBoost, tt),
        chest(482, CheckLocation.UndergroundConcourseMythrilCrystal, tt),
    ])
    tunnelway = graph.add_location(NodeId.Tunnelway, [
        chest(477, CheckLocation.TunnelwayOrichalcum, tt),
        chest(478, CheckLocation.TunnelwayMythrilCrystal, tt),
    ])
    sunset_terrace = graph.add_location(NodeId.SunsetTerrace, [
        chest(438, CheckLocation.SunsetTerraceOrichalcumPlus, tt),
        chest(439, CheckLocation.SunsetTerraceMythrilShard, tt),
        chest(440, CheckLocation.SunsetTerraceMythrilCrystal, tt),
        chest(441, CheckLocation.SunsetTerraceApBoost, tt),
    ])
    mansion_bonus = graph.add_location(NodeId.MansionBonus, [
        stat_bonus(56, CheckLocation.MansionNobodies, tt),
    ])
    mansion_foyer = graph.add_location(NodeId.MansionFoyer, [
        chest(452, CheckLocation.MansionFoyerMythrilCrystal, tt),
        chest(453, CheckLocation.MansionFoyerMythrilStone, tt),
        chest(454, CheckLocation.MansionFoyerSerenityCrystal, tt),
    ])
    mansion_dining_room = graph.add_location(NodeId.MansionDiningRoom, [
        chest(457, CheckLocation.MansionDiningRoomMythrilCrystal, tt),
        chest(458, CheckLocation.MansionDiningRoomMythrilStone, tt),
    ])
    mansion_library = graph.add_location(NodeId.MansionLibrary, [
        chest(460, CheckLocation.MansionLibraryOrichalcum, tt),
    ])
    beam = graph.add_location(NodeId.TwilightTownBeam, [
        popup(534, CheckLocation.BeamSecretAnsemReport10, tt, vanilla=report.AnsemReport10),
    ])
    mansion_basement = graph.add_location(NodeId.MansionBasement, [
        chest(464, CheckLocation.MansionBasementCorridorUltimateRecipe, tt),
    ])
    betwixt_and_between = graph.add_location(NodeId.BetwixtAndBetween, [
        item_bonus(63, CheckLocation.BetwixtAndBetween, tt, vanilla=ability.Slapshot),
        popup(317, CheckLocation.BetwixtAndBetweenBondOfFlame, tt, vanilla=keyblade.BondOfFlame),
    ])
    data_axel = graph.add_location(NodeId.DataAxel, [
        popup(561, CheckLocation.DataAxelMagicBoost, [tt, locationType.DataOrg]),
    ])

    graph.register_superboss(data_axel)

    if not graph.reverse_rando:
        graph.add_edge(START_NODE, old_mansion)
        graph.add_edge(old_mansion, tram_common)
        graph.add_edge(tram_common, woods)
        graph.add_edge(tram_common, station_fight_popup, RequirementEdge(battle=True))
        graph.add_edge(station_fight_popup, central_station)
        graph.add_edge(central_station, yen_sid_tower)
        graph.add_edge(yen_sid_tower, yen_sid_tower_entryway)
        graph.add_edge(yen_sid_tower_entryway, sorcerers_loft, RequirementEdge(battle=True))
        graph.add_edge(sorcerers_loft, tower_wardrobe)
        graph.add_edge(tower_wardrobe, valor_form)
        graph.add_edge(valor_form, seifers_trophy, RequirementEdge(battle=True))
        graph.add_edge(seifers_trophy, limit_form)
        graph.add_edge(limit_form, underground_concourse)
        graph.add_edge(underground_concourse, tunnelway)
        graph.add_edge(tunnelway, sunset_terrace)
        graph.add_edge(limit_form, mansion_bonus, RequirementEdge(battle=True))
        graph.add_edge(mansion_bonus, mansion_foyer)
        graph.add_edge(mansion_foyer, mansion_dining_room)
        graph.add_edge(mansion_foyer, mansion_library)
        graph.add_edge(mansion_foyer, beam)
        graph.add_edge(mansion_foyer, mansion_basement)
        graph.add_edge(beam, betwixt_and_between, RequirementEdge(battle=True))
        graph.add_edge(betwixt_and_between, data_axel, RequirementEdge(battle=True))
        graph.register_first_boss(valor_form)
        graph.register_last_story_boss(betwixt_and_between)
    else:
        graph.add_edge(START_NODE, central_station)
        graph.add_edge(central_station, underground_concourse)
        graph.add_edge(central_station, tram_common)
        graph.add_edge(tram_common, woods)
        graph.add_edge(underground_concourse, tunnelway)
        graph.add_edge(tunnelway, sunset_terrace)
        graph.add_edge(woods, mansion_bonus, RequirementEdge(battle=True))
        graph.add_edge(mansion_bonus, old_mansion)
        graph.add_edge(mansion_bonus, mansion_foyer)
        graph.add_edge(mansion_foyer, mansion_dining_room)
        graph.add_edge(mansion_foyer, mansion_library)
        graph.add_edge(mansion_foyer, beam)
        graph.add_edge(mansion_foyer, mansion_basement)
        graph.add_edge(beam, betwixt_and_between, RequirementEdge(battle=True))
        graph.add_edge(betwixt_and_between, seifers_trophy,RequirementEdge(battle=True))
        graph.add_edge(seifers_trophy, limit_form)
        graph.add_edge(limit_form, station_fight_popup,RequirementEdge(battle=True))
        graph.add_edge(station_fight_popup, yen_sid_tower)
        graph.add_edge(yen_sid_tower, yen_sid_tower_entryway)
        graph.add_edge(yen_sid_tower_entryway, sorcerers_loft, RequirementEdge(battle=True))
        graph.add_edge(sorcerers_loft, tower_wardrobe)
        graph.add_edge(tower_wardrobe, valor_form)
        graph.add_edge(valor_form, data_axel, RequirementEdge(battle=True))
        graph.register_first_boss(betwixt_and_between)
        graph.register_last_story_boss(valor_form)

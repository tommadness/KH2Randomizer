from enum import Enum

from List.configDict import locationType
from List.inventory import ability, misc
from List.location.graph import DefaultLogicGraph, RequirementEdge, chest, popup, stat_bonus, item_bonus, \
    LocationGraphBuilder, START_NODE
from Module.itemPlacementRestriction import ItemPlacementHelpers


class NodeId(str, Enum):
    TwilightTownMapPopup = "Twilight Town Map Popup"
    MunnyPouchPopup = "Munny Pouch Popup"
    RoxasStation = "Roxas Station"
    RoxasStationChests = "Roxas Station Chests"
    TwilightThorn = "Twilight Thorn"
    Axel1 = "Axel 1"
    StruggleChampion = "Struggle Champion"
    SimulatedCentralStation = "STT Central Station"
    SimulatedCentralStationChests = "STT Central Station Chests"
    SimulatedSunsetTerrace = "STT Sunset Terrace"
    SimulatedSunsetTerraceChests = "STT Sunset Terrace Chests"
    SimulatedMansionFoyer = "STT Mansion Foyer"
    SimulatedMansionFoyerChests = "STT Mansion Foyer Chests"
    SimulatedMansionDiningRoom = "STT Mansion Dining Room"
    SimulatedMansionDiningRoomChests = "STT Mansion Dining Room Chests"
    NaminesRoom = "Namine's Room"
    SimulatedMansionLibrary = "STT Mansion Library"
    SimulatedMansionLibraryChests = "STT Mansion Library Chests"
    Axel2 = "Axel 2"
    SimulatedMansionBasement = "STT Mansion Basement"
    SimulatedMansionBasementChests = "STT Mansion Basement Chests"
    DataRoxas = "Data Roxas"


class CheckLocation(str, Enum):
    TwilightTownMap = "Twilight Town Map"
    MunnyPouchOlette = "Munny Pouch (Olette)"
    StationDusks = "Station Dusks"
    StationOfSerenityPotion = "Station of Serenity Potion"
    StationOfCallingPotion = "Station of Calling Potion"
    TwilightThorn = "Twilight Thorn"
    Axel1 = "Axel 1"
    StruggleWinnerChampionBelt = "(Struggle Winner) Champion Belt"
    StruggleLoserMedal = "(Struggle Loser) Medal"
    StruggleTrophy = "The Struggle Trophy"
    CentralStationPotion1 = "Central Station Potion (1)"
    CentralStationHiPotion = "STT Central Station Hi-Potion"
    CentralStationPotion2 = "Central Station Potion (2)"
    SunsetTerraceAbilityRing = "Sunset Terrace Ability Ring"
    SunsetTerraceHiPotion = "Sunset Terrace Hi-Potion"
    SunsetTerracePotion1 = "Sunset Terrace Potion (1)"
    SunsetTerracePotion2 = "Sunset Terrace Potion (2)"
    MansionFoyerHiPotion = "Mansion Foyer Hi-Potion"
    MansionFoyerPotion1 = "Mansion Foyer Potion (1)"
    MansionFoyerPotion2 = "Mansion Foyer Potion (2)"
    MansionDiningRoomElvenBandanna = "Mansion Dining Room Elven Bandanna"
    MansionDiningRoomPotion = "Mansion Dining Room Potion"
    NaminesSketches = "Naminé´s Sketches"
    MansionMap = "Mansion Map"
    MansionLibraryHiPotion = "Mansion Library Hi-Potion"
    Axel2 = "Axel 2"
    MansionBasementCorridorHiPotion = "Mansion Basement Corridor Hi-Potion"
    DataRoxasMagicBoost = "Roxas (Data) Magic Boost"


class STTLogicGraph(DefaultLogicGraph):
    def __init__(self,reverse_rando,first_visit_locks):
        DefaultLogicGraph.__init__(self,NodeId)
        if not reverse_rando:
            self.logic[NodeId.RoxasStation][NodeId.RoxasStationChests] = ItemPlacementHelpers.need_stt_keyblade
            self.logic[NodeId.SimulatedCentralStation][NodeId.SimulatedCentralStationChests] = ItemPlacementHelpers.need_stt_keyblade
            self.logic[NodeId.SimulatedSunsetTerrace][NodeId.SimulatedSunsetTerraceChests] = ItemPlacementHelpers.need_stt_keyblade
            self.logic[NodeId.SimulatedMansionFoyer][NodeId.SimulatedMansionFoyerChests] = ItemPlacementHelpers.need_stt_keyblade
            self.logic[NodeId.SimulatedMansionDiningRoom][NodeId.SimulatedMansionDiningRoomChests] = ItemPlacementHelpers.need_stt_keyblade
            self.logic[NodeId.SimulatedMansionLibrary][NodeId.SimulatedMansionLibraryChests] = ItemPlacementHelpers.need_stt_keyblade
            self.logic[NodeId.SimulatedMansionBasement][NodeId.SimulatedMansionBasementChests] = ItemPlacementHelpers.need_stt_keyblade
        
            self.logic[START_NODE][NodeId.TwilightTownMapPopup] = ItemPlacementHelpers.stt_check
        else:
            pass

def make_graph(graph: LocationGraphBuilder):
    stt = locationType.STT
    stt_logic = STTLogicGraph(graph.reverse_rando,graph.first_visit_locks)
    graph.add_logic(stt_logic)

    twilight_town_map_popup = graph.add_location(NodeId.TwilightTownMapPopup, [
        popup(319, CheckLocation.TwilightTownMap, stt),
    ])
    munny_pouch_popup = graph.add_location(NodeId.MunnyPouchPopup, [
        popup(288, CheckLocation.MunnyPouchOlette, stt, vanilla=misc.MunnyPouchOlette),
    ])
    roxas_station_chests = graph.add_location(NodeId.RoxasStationChests, [
        chest(315, CheckLocation.StationOfSerenityPotion, stt),
        chest(472, CheckLocation.StationOfCallingPotion, stt),
    ])
    roxas_station = graph.add_location(NodeId.RoxasStation, [
        item_bonus(54, CheckLocation.StationDusks, stt, vanilla=ability.AerialRecovery),
    ])
    twilight_thorn = graph.add_location(NodeId.TwilightThorn, [
        item_bonus(33, CheckLocation.TwilightThorn, stt, vanilla=ability.Guard),
    ])
    axel_1 = graph.add_location(NodeId.Axel1, [
        item_bonus(73, CheckLocation.Axel1, stt, vanilla=ability.Scan),
    ])
    struggle_champion = graph.add_location(NodeId.StruggleChampion, [
        popup(389, CheckLocation.StruggleWinnerChampionBelt, stt),
        popup(390, CheckLocation.StruggleLoserMedal, stt),
        popup(519, CheckLocation.StruggleTrophy, stt),
    ])
    central_station_chests = graph.add_location(NodeId.SimulatedCentralStationChests, [
        chest(428, CheckLocation.CentralStationPotion1, stt),
        chest(429, CheckLocation.CentralStationHiPotion, stt),
        chest(430, CheckLocation.CentralStationPotion2, stt),
    ])
    central_station = graph.add_location(NodeId.SimulatedCentralStation, [])
    sunset_terrace_chests = graph.add_location(NodeId.SimulatedSunsetTerraceChests, [
        chest(434, CheckLocation.SunsetTerraceAbilityRing, stt),
        chest(435, CheckLocation.SunsetTerraceHiPotion, stt),
        chest(436, CheckLocation.SunsetTerracePotion1, stt),
        chest(437, CheckLocation.SunsetTerracePotion2, stt),
    ])
    sunset_terrace = graph.add_location(NodeId.SimulatedSunsetTerrace, [])
    mansion_foyer_chests = graph.add_location(NodeId.SimulatedMansionFoyerChests, [
        chest(449, CheckLocation.MansionFoyerHiPotion, stt),
        chest(450, CheckLocation.MansionFoyerPotion1, stt),
        chest(451, CheckLocation.MansionFoyerPotion2, stt),
    ])
    mansion_foyer = graph.add_location(NodeId.SimulatedMansionFoyer, [])
    mansion_dining_room_chests = graph.add_location(NodeId.SimulatedMansionDiningRoomChests, [
        chest(455, CheckLocation.MansionDiningRoomElvenBandanna, stt),
        chest(456, CheckLocation.MansionDiningRoomPotion, stt),
    ])
    mansion_dining_room = graph.add_location(NodeId.SimulatedMansionDiningRoom, [])
    namines_room = graph.add_location(NodeId.NaminesRoom, [
        popup(289, CheckLocation.NaminesSketches, stt),
        popup(483, CheckLocation.MansionMap, stt),
    ])
    mansion_library_chests = graph.add_location(NodeId.SimulatedMansionLibraryChests, [
        chest(459, CheckLocation.MansionLibraryHiPotion, stt),
    ])
    mansion_library = graph.add_location(NodeId.SimulatedMansionLibrary, [])
    axel_2 = graph.add_location(NodeId.Axel2, [
        stat_bonus(34, CheckLocation.Axel2, stt),
    ])
    mansion_basement_chests = graph.add_location(NodeId.SimulatedMansionBasementChests, [
        chest(463, CheckLocation.MansionBasementCorridorHiPotion, stt),
    ])
    mansion_basement = graph.add_location(NodeId.SimulatedMansionBasement, [])

    data_roxas = graph.add_location(NodeId.DataRoxas, [
        popup(558, CheckLocation.DataRoxasMagicBoost, [stt, locationType.DataOrg]),
    ])

    graph.register_superboss(data_roxas)

    graph.add_edge(roxas_station, roxas_station_chests)
    graph.add_edge(central_station, central_station_chests)
    graph.add_edge(sunset_terrace, sunset_terrace_chests)
    graph.add_edge(mansion_foyer, mansion_foyer_chests)
    graph.add_edge(mansion_dining_room, mansion_dining_room_chests)
    graph.add_edge(mansion_library, mansion_library_chests)
    graph.add_edge(mansion_basement, mansion_basement_chests)

    if not graph.reverse_rando:
        graph.add_edge(START_NODE, twilight_town_map_popup)
        graph.add_edge(twilight_town_map_popup, munny_pouch_popup)
        graph.add_edge(munny_pouch_popup, roxas_station)
        graph.add_edge(roxas_station, twilight_thorn, RequirementEdge(battle=True))
        graph.add_edge(twilight_thorn, axel_1, RequirementEdge(battle=True))
        graph.add_edge(axel_1, struggle_champion, RequirementEdge(battle=True))
        graph.add_edge(struggle_champion, central_station)
        graph.add_edge(struggle_champion, sunset_terrace)
        graph.add_edge(sunset_terrace, mansion_foyer, RequirementEdge(battle=True))
        graph.add_edge(mansion_foyer, mansion_dining_room)
        graph.add_edge(mansion_foyer, namines_room)
        graph.add_edge(namines_room, mansion_library)
        graph.add_edge(namines_room, axel_2, RequirementEdge(battle=True))
        graph.add_edge(axel_2, mansion_basement)
        graph.add_edge(mansion_basement, data_roxas, RequirementEdge(battle=True))
        graph.register_first_boss(mansion_basement_chests)
        graph.register_last_story_boss(mansion_basement_chests)
    else:
        graph.add_edge(START_NODE, mansion_foyer)
        graph.add_edge(mansion_foyer, mansion_dining_room)
        graph.add_edge(mansion_foyer, namines_room)
        graph.add_edge(namines_room, mansion_library)
        graph.add_edge(namines_room, axel_2, RequirementEdge(battle=True))
        graph.add_edge(axel_2, mansion_basement)
        graph.add_edge(mansion_basement, central_station)
        graph.add_edge(mansion_basement, sunset_terrace)
        graph.add_edge(sunset_terrace, axel_1, RequirementEdge(battle=True))
        graph.add_edge(axel_1, struggle_champion, RequirementEdge(battle=True))
        graph.add_edge(struggle_champion, roxas_station)
        graph.add_edge(roxas_station, twilight_thorn, RequirementEdge(battle=True))
        graph.add_edge(twilight_thorn, twilight_town_map_popup, RequirementEdge(battle=True))
        graph.add_edge(twilight_town_map_popup, munny_pouch_popup)
        graph.add_edge(munny_pouch_popup, data_roxas, RequirementEdge(battle=True))
        graph.register_first_boss(munny_pouch_popup)
        graph.register_last_story_boss(munny_pouch_popup)

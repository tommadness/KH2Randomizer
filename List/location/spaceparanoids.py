from enum import Enum

from List.configDict import locationType
from List.inventory import ability, keyblade, magic
from List.location.graph import DefaultLogicGraph, RequirementEdge, chest, popup, hybrid_bonus, item_bonus, stat_bonus, \
    LocationGraphBuilder, START_NODE
from Module.itemPlacementRestriction import ItemPlacementHelpers


class NodeId(str, Enum):
    PitCell = "Pit Cell"
    PitCellChests = "Pit Cell Chests"
    Canyon = "Canyon"
    CanyonChests = "Canyon Chests"
    ScreensBonus = "Screens Bonus"
    Hallway = "Hallway"
    HallwayChests = "Hallway Chests"
    CommunicationsRoom = "Communications Room"
    CommunicationsRoomChests = "Communications Room Chests"
    HostileProgram = "Hostile Program"
    PhotonDebugger = "Photon Debugger"
    SolarSailerBonus = "Solar Sailer Bonus"
    CentralComputerCore = "Central Computer Core"
    CentralComputerCoreChests = "Central Computer Core Chests"
    MasterControlProgramBonus = "MCP Bonus"
    Larxene = "AS Larxene"
    DataLarxene = "Data Larxene"


class CheckLocation(str, Enum):
    PitCellAreaMap = "Pit Cell Area Map"
    PitCellMythrilCrystal = "Pit Cell Mythril Crystal"
    CanyonDarkCrystal = "Canyon Dark Crystal"
    CanyonMythrilStone = "Canyon Mythril Stone"
    CanyonMythrilGem = "Canyon Mythril Gem"
    CanyonFrostCrystal = "Canyon Frost Crystal"
    ScreensBonus = "Screens"
    HallwayPowerCrystal = "Hallway Power Crystal"
    HallwayApBoost = "Hallway AP Boost"
    CommunicationsRoomIoTowerMap = "Communications Room I/O Tower Map"
    CommunicationsRoomGaiaBelt = "Communications Room Gaia Belt"
    HostileProgramBonus = "Hostile Program"
    PhotonDebugger = "Photon Debugger"
    SolarSailerBonus = "Solar Sailer"
    CentralComputerCoreApBoost = "Central Computer Core AP Boost"
    CentralComputerCoreOrichalcumPlus = "Central Computer Core Orichalcum+"
    CentralComputerCoreCosmicArts = "Central Computer Core Cosmic Arts"
    CentralComputerCoreMap = "Central Computer Core Map"
    McpBonus = "MCP"
    LarxeneBonus = "Larxene Bonus"
    LarxeneCloakedThunder = "Larxene (AS) Cloaked Thunder"
    DataLarxeneLostIllusion = "Larxene (Data) Lost Illusion"
    
class SPLogicGraph(DefaultLogicGraph):
    def __init__(self,reverse_rando,keyblade_unlocks):
        DefaultLogicGraph.__init__(self,NodeId)
        keyblade_lambda = lambda inv : not keyblade_unlocks or ItemPlacementHelpers.need_sp_keyblade(inv)
        self.logic[NodeId.PitCell][NodeId.PitCellChests] = keyblade_lambda
        self.logic[NodeId.Canyon][NodeId.CanyonChests] = keyblade_lambda
        self.logic[NodeId.Hallway][NodeId.HallwayChests] = keyblade_lambda
        self.logic[NodeId.CommunicationsRoom][NodeId.CommunicationsRoomChests] = keyblade_lambda
        self.logic[NodeId.CentralComputerCore][NodeId.CentralComputerCoreChests] = keyblade_lambda
        if not reverse_rando:
            self.logic[START_NODE][NodeId.PitCell] = ItemPlacementHelpers.sp1_check
            self.logic[NodeId.PhotonDebugger][NodeId.SolarSailerBonus] = ItemPlacementHelpers.sp2_check
        else:
            self.logic[START_NODE][NodeId.PitCell] = ItemPlacementHelpers.sp1_check
            self.logic[NodeId.Larxene][NodeId.ScreensBonus] = ItemPlacementHelpers.sp2_check

def make_graph(graph: LocationGraphBuilder):
    sp = locationType.SP
    sp_logic = SPLogicGraph(graph.reverse_rando,graph.keyblades_unlock_chests)
    graph.add_logic(sp_logic)

    pit_cell_chests = graph.add_location(NodeId.PitCellChests, [
        chest(316, CheckLocation.PitCellAreaMap, sp),
        chest(64, CheckLocation.PitCellMythrilCrystal, sp),
    ])
    pit_cell = graph.add_location(NodeId.PitCell, [])
    canyon_chests = graph.add_location(NodeId.CanyonChests, [
        chest(65, CheckLocation.CanyonDarkCrystal, sp),
        chest(171, CheckLocation.CanyonMythrilStone, sp),
        chest(253, CheckLocation.CanyonMythrilGem, sp),
        chest(521, CheckLocation.CanyonFrostCrystal, sp),
    ])
    canyon = graph.add_location(NodeId.Canyon, [])
    screens_bonus = graph.add_location(NodeId.ScreensBonus, [
        stat_bonus(45, CheckLocation.ScreensBonus, sp),
    ])
    hallway_chests = graph.add_location(NodeId.HallwayChests, [
        chest(49, CheckLocation.HallwayPowerCrystal, sp),
        chest(50, CheckLocation.HallwayApBoost, sp),
    ])
    hallway = graph.add_location(NodeId.Hallway, [])
    communications_room_chests = graph.add_location(NodeId.CommunicationsRoomChests, [
        chest(255, CheckLocation.CommunicationsRoomIoTowerMap, sp),
        chest(499, CheckLocation.CommunicationsRoomGaiaBelt, sp),
    ])
    communications_room = graph.add_location(NodeId.CommunicationsRoom, [])
    hostile_program = graph.add_location(NodeId.HostileProgram, [
        hybrid_bonus(31, CheckLocation.HostileProgramBonus, sp, vanilla=ability.VicinityBreak),
    ])
    photon_debugger = graph.add_location(NodeId.PhotonDebugger, [
        popup(267, CheckLocation.PhotonDebugger, sp, vanilla=keyblade.PhotonDebugger),
    ])
    solar_sailer_bonus = graph.add_location(NodeId.SolarSailerBonus, [
        item_bonus(61, CheckLocation.SolarSailerBonus, sp, vanilla=ability.Explosion),
    ])
    central_computer_core_chests = graph.add_location(NodeId.CentralComputerCoreChests, [
        chest(177, CheckLocation.CentralComputerCoreApBoost, sp),
        chest(178, CheckLocation.CentralComputerCoreOrichalcumPlus, sp),
        chest(51, CheckLocation.CentralComputerCoreCosmicArts, sp),
        chest(488, CheckLocation.CentralComputerCoreMap, sp),
    ])
    central_computer_core = graph.add_location(NodeId.CentralComputerCore, [])
    mcp_bonus = graph.add_location(NodeId.MasterControlProgramBonus, [
        hybrid_bonus(32, CheckLocation.McpBonus, sp, vanilla=magic.Reflect),
    ])
    larxene = graph.add_location(NodeId.Larxene, [
        stat_bonus(68, CheckLocation.LarxeneBonus, [sp, locationType.AS]),
        popup(547, CheckLocation.LarxeneCloakedThunder, [sp, locationType.AS]),
    ])
    data_larxene = graph.add_location(NodeId.DataLarxene, [
        popup(552, CheckLocation.DataLarxeneLostIllusion, [sp, locationType.DataOrg]),
    ])

    graph.register_superboss(data_larxene)
    
    graph.add_edge(pit_cell, pit_cell_chests)
    graph.add_edge(canyon, canyon_chests)
    graph.add_edge(hallway, hallway_chests)
    graph.add_edge(communications_room, communications_room_chests)
    graph.add_edge(central_computer_core, central_computer_core_chests)

    if not graph.reverse_rando:
        graph.add_edge(START_NODE, pit_cell)
        graph.add_edge(pit_cell, canyon)
        graph.add_edge(canyon, screens_bonus, RequirementEdge(battle=True))
        graph.add_edge(screens_bonus, hallway)
        graph.add_edge(hallway, communications_room)
        graph.add_edge(communications_room, hostile_program, RequirementEdge(battle=True))
        graph.add_edge(hostile_program, photon_debugger)
        graph.add_edge(photon_debugger, solar_sailer_bonus)
        graph.add_edge(solar_sailer_bonus, central_computer_core)
        graph.add_edge(central_computer_core, mcp_bonus, RequirementEdge(battle=True))
        graph.add_edge(mcp_bonus, larxene, RequirementEdge(battle=True))
        graph.add_edge(larxene, data_larxene)
        graph.register_first_boss(photon_debugger)
        graph.register_last_story_boss(mcp_bonus)
        graph.register_superboss(larxene)
    else:
        graph.add_edge(START_NODE, pit_cell)
        graph.add_edge(pit_cell, canyon)
        graph.add_edge(canyon, communications_room, RequirementEdge(battle=True))
        graph.add_edge(communications_room, hallway)
        graph.add_edge(hallway, solar_sailer_bonus, RequirementEdge(battle=True))
        graph.add_edge(solar_sailer_bonus, central_computer_core)
        graph.add_edge(central_computer_core, mcp_bonus, RequirementEdge(battle=True))
        graph.add_edge(mcp_bonus, larxene, RequirementEdge(battle=True))
        graph.add_edge(larxene, screens_bonus, RequirementEdge(battle=True))
        graph.add_edge(screens_bonus, hostile_program, RequirementEdge(battle=True))
        graph.add_edge(hostile_program, photon_debugger)
        graph.add_edge(photon_debugger, data_larxene, RequirementEdge(battle=True))
        graph.register_first_boss(mcp_bonus)
        graph.register_last_story_boss(photon_debugger)

from enum import Enum

from List.configDict import locationType, itemType
from List.inventory import keyblade, ability, report
from List.location.graph import DefaultLogicGraph, RequirementEdge, chest, popup, hybrid_bonus, stat_bonus, double_bonus, \
    LocationGraphBuilder, START_NODE
from Module.itemPlacementRestriction import ItemPlacementHelpers


class NodeId(str, Enum):
    FragmentCrossing = "Fragment Crossing"
    FragmentCrossingChests = "Fragment Crossing Chests"
    Roxas = "Roxas"
    MemorysSkyscraper = "Memory's Skyscraper"
    MemorysSkyscraperChests = "Memory's Skyscraper Chests"
    BrinkOfDespair = "Brink of Despair"
    BrinkOfDespairChests = "Brink of Despair Chests"
    NothingsCall = "Nothing's Call"
    NothingsCallChests = "Nothing's Call Chests"
    TwilightsView = "Twilight's View"
    TwilightsViewChests = "Twilight's View Chests"
    Xigbar = "Xigbar"
    NaughtsSkyway = "Naught's Skyway"
    NaughtsSkywayChests = "Naught's Skyway Chests"
    Oblivion = "Oblivion"
    Luxord = "Luxord"
    Saix = "Saix"
    PreXemnas1Popup = "Pre-Xemnas 1 Popup"
    RuinAndCreationsPassage = "Ruin and Creation's Passage"
    RuinAndCreationsPassageChests = "Ruin and Creation's Passage Chests"
    Xemnas1 = "Xemnas 1"
    FinalXemnas = "Final Xemnas"
    DataXemnas = "Data Xemnas"


class CheckLocation(str, Enum):
    FragmentCrossingMythrilStone = "Fragment Crossing Mythril Stone"
    FragmentCrossingMythrilCrystal = "Fragment Crossing Mythril Crystal"
    FragmentCrossingApBoost = "Fragment Crossing AP Boost"
    FragmentCrossingOrichalcum = "Fragment Crossing Orichalcum"
    Roxas = "Roxas"
    RoxasSecretAnsemReport8 = "Roxas Secret Ansem Report 8"
    TwoBecomeOne = "Two Become One"
    MemorysSkyscraperMythrilCrystal = "Memory's Skyscaper Mythril Crystal"
    MemorysSkyscraperApBoost = "Memory's Skyscaper AP Boost"
    MemorysSkyscraperMythrilStone = "Memory's Skyscaper Mythril Stone"
    BrinkOfDespairDarkCityMap = "The Brink of Despair Dark City Map"
    BrinkOfDespairOrichalcumPlus = "The Brink of Despair Orichalcum+"
    NothingsCallMythrilGem = "Nothing's Call Mythril Gem"
    NothingsCallOrichalcum = "Nothing's Call Orichalcum"
    TwilightsViewCosmicBelt = "Twilight's View Cosmic Belt"
    XigbarBonus = "Xigbar Bonus"
    XigbarSecretAnsemReport3 = "Xigbar Secret Ansem Report 3"
    NaughtsSkywayMythrilGem = "Naught's Skyway Mythril Gem"
    NaughtsSkywayOrichalcum = "Naught's Skyway Orichalcum"
    NaughtsSkywayMythrilCrystal = "Naught's Skyway Mythril Crystal"
    Oblivion = "Oblivion"
    CastleThatNeverWasMap = "Castle That Never Was Map"
    LuxordBonus = "Luxord Bonus"
    LuxordSecretAnsemReport9 = "Luxord Secret Ansem Report 9"
    SaixBonus = "Saix Bonus"
    SaixSecretAnsemReport12 = "Saix Secret Ansem Report 12"
    PreXemnas1SecretAnsemReport11 = "(Pre-Xemnas 1) Secret Ansem Report 11"
    RuinCreationsPassageMythrilStone = "Ruin and Creation's Passage Mythril Stone"
    RuinCreationsPassageApBoost = "Ruin and Creation's Passage AP Boost"
    RuinCreationsPassageMythrilCrystal = "Ruin and Creation's Passage Mythril Crystal"
    RuinCreationsPassageOrichalcum = "Ruin and Creation's Passage Orichalcum"
    Xemnas1Bonus = "Xemnas 1 Bonus"
    Xemnas1SecretAnsemReport13 = "Xemnas 1 Secret Ansem Report 13"
    FinalXemnas = "Final Xemnas"
    DataXemnas = "Xemnas (Data) Power Boost"

class TWTNWLogicGraph(DefaultLogicGraph):
    def __init__(self,reverse_rando,keyblade_unlocks,objectives_needed):
        DefaultLogicGraph.__init__(self,NodeId)
        keyblade_lambda = lambda inv : not keyblade_unlocks or ItemPlacementHelpers.need_twtnw_keyblade(inv)
        self.logic[NodeId.FragmentCrossing][NodeId.FragmentCrossingChests] = keyblade_lambda
        self.logic[NodeId.MemorysSkyscraper][NodeId.MemorysSkyscraperChests] = keyblade_lambda
        self.logic[NodeId.BrinkOfDespair][NodeId.BrinkOfDespairChests] = keyblade_lambda
        self.logic[NodeId.NothingsCall][NodeId.NothingsCallChests] = keyblade_lambda
        self.logic[NodeId.TwilightsView][NodeId.TwilightsViewChests] = keyblade_lambda
        self.logic[NodeId.NaughtsSkyway][NodeId.NaughtsSkywayChests] = keyblade_lambda
        self.logic[NodeId.RuinAndCreationsPassage][NodeId.RuinAndCreationsPassageChests] = keyblade_lambda

        self.logic[START_NODE][NodeId.FinalXemnas] = lambda inv : ItemPlacementHelpers.need_promise_charm(inv) and (ItemPlacementHelpers.need_proofs(inv) or ItemPlacementHelpers.make_need_objectives_lambda(objectives_needed))
        if not reverse_rando:
            self.logic[NodeId.FragmentCrossing][NodeId.Roxas] = ItemPlacementHelpers.twtnw_roxas_check
            self.logic[NodeId.Saix][NodeId.PreXemnas1Popup] = ItemPlacementHelpers.twtnw_post_saix_check
            self.logic[NodeId.Xemnas1][NodeId.FinalXemnas] = lambda inv : ItemPlacementHelpers.need_proofs(inv) or ItemPlacementHelpers.make_need_objectives_lambda(objectives_needed)
        else:
            self.logic[NodeId.FragmentCrossing][NodeId.Xemnas1] = ItemPlacementHelpers.twtnw_roxas_check
            self.logic[NodeId.Xigbar][NodeId.PreXemnas1Popup] = ItemPlacementHelpers.twtnw_post_saix_check
            self.logic[NodeId.Roxas][NodeId.FinalXemnas] = lambda inv : ItemPlacementHelpers.need_proofs(inv) or ItemPlacementHelpers.make_need_objectives_lambda(objectives_needed)

def make_graph(graph: LocationGraphBuilder):
    twtnw = locationType.TWTNW
    twtnw_logic = TWTNWLogicGraph(graph.reverse_rando,graph.keyblades_unlock_chests,graph.settings.num_objectives_needed)
    graph.add_logic(twtnw_logic)

    fragment_crossing_chests = graph.add_location(NodeId.FragmentCrossingChests, [
        chest(374, CheckLocation.FragmentCrossingMythrilStone, twtnw),
        chest(375, CheckLocation.FragmentCrossingMythrilCrystal, twtnw),
        chest(376, CheckLocation.FragmentCrossingApBoost, twtnw),
        chest(377, CheckLocation.FragmentCrossingOrichalcum, twtnw),
    ])
    fragment_crossing = graph.add_location(NodeId.FragmentCrossing, [])
    roxas = graph.add_location(NodeId.Roxas, [
        hybrid_bonus(69, CheckLocation.Roxas, twtnw, vanilla=ability.ComboMaster),
        popup(532, CheckLocation.RoxasSecretAnsemReport8, twtnw, vanilla=report.AnsemReport8),
        popup(277, CheckLocation.TwoBecomeOne, twtnw, vanilla=keyblade.TwoBecomeOne),
    ])
    memorys_skyscraper_chests = graph.add_location(NodeId.MemorysSkyscraperChests, [
        chest(391, CheckLocation.MemorysSkyscraperMythrilCrystal, twtnw),
        chest(523, CheckLocation.MemorysSkyscraperApBoost, twtnw),
        chest(524, CheckLocation.MemorysSkyscraperMythrilStone, twtnw),
    ])
    memorys_skyscraper = graph.add_location(NodeId.MemorysSkyscraper, [])
    brink_of_despair_chests = graph.add_location(NodeId.BrinkOfDespairChests, [
        chest(335, CheckLocation.BrinkOfDespairDarkCityMap, twtnw),
        chest(500, CheckLocation.BrinkOfDespairOrichalcumPlus, twtnw),
    ])
    brink_of_despair = graph.add_location(NodeId.BrinkOfDespair, [])
    nothings_call_chests = graph.add_location(NodeId.NothingsCallChests, [
        chest(378, CheckLocation.NothingsCallMythrilGem, twtnw),
        chest(379, CheckLocation.NothingsCallOrichalcum, twtnw),
    ])
    nothings_call = graph.add_location(NodeId.NothingsCall, [])
    twilights_view_chests = graph.add_location(NodeId.TwilightsViewChests, [
        chest(336, CheckLocation.TwilightsViewCosmicBelt, twtnw),
    ])
    twilights_view = graph.add_location(NodeId.TwilightsView, [])
    xigbar = graph.add_location(NodeId.Xigbar, [
        stat_bonus(23, CheckLocation.XigbarBonus, twtnw),
        popup(527, CheckLocation.XigbarSecretAnsemReport3, twtnw, vanilla=report.AnsemReport3),
    ])
    naughts_skyway_chests = graph.add_location(NodeId.NaughtsSkywayChests, [
        chest(380, CheckLocation.NaughtsSkywayMythrilGem, twtnw),
        chest(381, CheckLocation.NaughtsSkywayOrichalcum, twtnw),
        chest(382, CheckLocation.NaughtsSkywayMythrilCrystal, twtnw),
    ])
    naughts_skyway = graph.add_location(NodeId.NaughtsSkyway, [])
    oblivion = graph.add_location(NodeId.Oblivion, [
        popup(278, CheckLocation.Oblivion, twtnw, vanilla=keyblade.Oblivion),
        popup(496, CheckLocation.CastleThatNeverWasMap, twtnw),
    ])
    luxord = graph.add_location(NodeId.Luxord, [
        hybrid_bonus(24, CheckLocation.LuxordBonus, twtnw),
        popup(533, CheckLocation.LuxordSecretAnsemReport9, twtnw, vanilla=report.AnsemReport9),
    ])
    saix = graph.add_location(NodeId.Saix, [
        stat_bonus(25, CheckLocation.SaixBonus, twtnw),
        popup(536, CheckLocation.SaixSecretAnsemReport12, twtnw, vanilla=report.AnsemReport12),
    ])
    pre_xemnas_1_popup = graph.add_location(NodeId.PreXemnas1Popup, [
        popup(535, CheckLocation.PreXemnas1SecretAnsemReport11, twtnw, vanilla=report.AnsemReport11),
    ])
    ruin_creations_passage_chests = graph.add_location(NodeId.RuinAndCreationsPassageChests, [
        chest(385, CheckLocation.RuinCreationsPassageMythrilStone, twtnw),
        chest(386, CheckLocation.RuinCreationsPassageApBoost, twtnw),
        chest(387, CheckLocation.RuinCreationsPassageMythrilCrystal, twtnw),
        chest(388, CheckLocation.RuinCreationsPassageOrichalcum, twtnw),
    ])
    ruin_creations_passage = graph.add_location(NodeId.RuinAndCreationsPassage, [])
    xemnas_1 = graph.add_location(NodeId.Xemnas1, [
        double_bonus(26, CheckLocation.Xemnas1Bonus, twtnw),
        popup(537, CheckLocation.Xemnas1SecretAnsemReport13, twtnw, vanilla=report.AnsemReport13),
    ])
    final_xemnas = graph.add_location(NodeId.FinalXemnas, [
        stat_bonus(71, CheckLocation.FinalXemnas, twtnw, invalid_checks=[e for e in itemType if
                                                                         e not in [itemType.GAUGE, itemType.SLOT,
                                                                                   itemType.SYNTH, itemType.ITEM]]),
    ])
    data_xemnas = graph.add_location(NodeId.DataXemnas, [
        popup(554, CheckLocation.DataXemnas, [twtnw, locationType.DataOrg]),
    ])

    graph.register_superboss(data_xemnas)

    
    graph.add_edge(START_NODE, final_xemnas, RequirementEdge(battle=True, strict=False))
    
    graph.add_edge(fragment_crossing, fragment_crossing_chests)
    graph.add_edge(memorys_skyscraper, memorys_skyscraper_chests)
    graph.add_edge(brink_of_despair, brink_of_despair_chests)
    graph.add_edge(nothings_call, nothings_call_chests)
    graph.add_edge(twilights_view, twilights_view_chests)
    graph.add_edge(naughts_skyway, naughts_skyway_chests)
    graph.add_edge(ruin_creations_passage, ruin_creations_passage_chests)

    if not graph.reverse_rando:
        graph.add_edge(START_NODE, fragment_crossing)
        graph.add_edge(fragment_crossing, roxas, RequirementEdge(battle=True))
        graph.add_edge(roxas, memorys_skyscraper)
        graph.add_edge(memorys_skyscraper, brink_of_despair)
        graph.add_edge(brink_of_despair, nothings_call)
        graph.add_edge(nothings_call, twilights_view)
        graph.add_edge(twilights_view, xigbar, RequirementEdge(battle=True))
        graph.add_edge(xigbar, naughts_skyway)
        graph.add_edge(naughts_skyway, oblivion)
        graph.add_edge(oblivion, luxord, RequirementEdge(battle=True))
        graph.add_edge(luxord, saix, RequirementEdge(battle=True))
        graph.add_edge(saix, pre_xemnas_1_popup)
        graph.add_edge(pre_xemnas_1_popup, ruin_creations_passage)
        graph.add_edge(ruin_creations_passage, xemnas_1, RequirementEdge(battle=True))
        graph.add_edge(xemnas_1, final_xemnas, RequirementEdge(battle=True, strict=False))
        graph.add_edge(xemnas_1, data_xemnas, RequirementEdge(battle=True))
        graph.register_first_boss(xemnas_1)
        graph.register_last_story_boss(xemnas_1)
    else:
        graph.add_edge(START_NODE, fragment_crossing)
        graph.add_edge(fragment_crossing, xemnas_1, RequirementEdge(battle=True))
        graph.add_edge(xemnas_1, memorys_skyscraper)
        graph.add_edge(memorys_skyscraper, brink_of_despair)
        graph.add_edge(brink_of_despair, nothings_call)
        graph.add_edge(nothings_call, twilights_view)
        graph.add_edge(twilights_view, saix, RequirementEdge(battle=True))
        graph.add_edge(saix, naughts_skyway)
        graph.add_edge(naughts_skyway, oblivion)
        graph.add_edge(oblivion, luxord, RequirementEdge(battle=True))
        graph.add_edge(luxord, xigbar, RequirementEdge(battle=True))
        graph.add_edge(xigbar, pre_xemnas_1_popup)
        graph.add_edge(pre_xemnas_1_popup, ruin_creations_passage)
        graph.add_edge(ruin_creations_passage, roxas, RequirementEdge(battle=True))
        graph.add_edge(roxas, final_xemnas, RequirementEdge(battle=True, strict=False))
        graph.add_edge(roxas, data_xemnas, RequirementEdge(battle=True))
        graph.register_first_boss(roxas)
        graph.register_last_story_boss(roxas)

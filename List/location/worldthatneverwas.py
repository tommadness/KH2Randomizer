from enum import Enum

from List.configDict import locationType, itemType
from List.inventory import keyblade, ability, report
from List.location.graph import RequirementEdge, chest, popup, hybrid_bonus, stat_bonus, double_bonus, \
    LocationGraphBuilder, START_NODE
from Module.itemPlacementRestriction import ItemPlacementHelpers


class NodeId(str, Enum):
    FragmentCrossing = "Fragment Crossing"
    Roxas = "Roxas"
    MemorysSkyscraper = "Memory's Skyscraper"
    BrinkOfDespair = "Brink of Despair"
    NothingsCall = "Nothing's Call"
    TwilightsView = "Twilight's View"
    Xigbar = "Xigbar"
    NaughtsSkyway = "Naught's Skyway"
    Oblivion = "Oblivion"
    Luxord = "Luxord"
    Saix = "Saix"
    PreXemnas1Popup = "Pre-Xemnas 1 Popup"
    RuinAndCreationsPassage = "Ruin and Creation's Passage"
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


def make_graph(graph: LocationGraphBuilder):
    twtnw = locationType.TWTNW

    fragment_crossing = graph.add_location(NodeId.FragmentCrossing, [
        chest(374, CheckLocation.FragmentCrossingMythrilStone, twtnw),
        chest(375, CheckLocation.FragmentCrossingMythrilCrystal, twtnw),
        chest(376, CheckLocation.FragmentCrossingApBoost, twtnw),
        chest(377, CheckLocation.FragmentCrossingOrichalcum, twtnw),
    ])
    roxas = graph.add_location(NodeId.Roxas, [
        hybrid_bonus(69, CheckLocation.Roxas, twtnw, vanilla=ability.ComboMaster),
        popup(532, CheckLocation.RoxasSecretAnsemReport8, twtnw, vanilla=report.AnsemReport8),
        popup(277, CheckLocation.TwoBecomeOne, twtnw, vanilla=keyblade.TwoBecomeOne),
    ])
    memorys_skyscraper = graph.add_location(NodeId.MemorysSkyscraper, [
        chest(391, CheckLocation.MemorysSkyscraperMythrilCrystal, twtnw),
        chest(523, CheckLocation.MemorysSkyscraperApBoost, twtnw),
        chest(524, CheckLocation.MemorysSkyscraperMythrilStone, twtnw),
    ])
    brink_of_despair = graph.add_location(NodeId.BrinkOfDespair, [
        chest(335, CheckLocation.BrinkOfDespairDarkCityMap, twtnw),
        chest(500, CheckLocation.BrinkOfDespairOrichalcumPlus, twtnw),
    ])
    nothings_call = graph.add_location(NodeId.NothingsCall, [
        chest(378, CheckLocation.NothingsCallMythrilGem, twtnw),
        chest(379, CheckLocation.NothingsCallOrichalcum, twtnw),
    ])
    twilights_view = graph.add_location(NodeId.TwilightsView, [
        chest(336, CheckLocation.TwilightsViewCosmicBelt, twtnw),
    ])
    xigbar = graph.add_location(NodeId.Xigbar, [
        stat_bonus(23, CheckLocation.XigbarBonus, twtnw),
        popup(527, CheckLocation.XigbarSecretAnsemReport3, twtnw, vanilla=report.AnsemReport3),
    ])
    naughts_skyway = graph.add_location(NodeId.NaughtsSkyway, [
        chest(380, CheckLocation.NaughtsSkywayMythrilGem, twtnw),
        chest(381, CheckLocation.NaughtsSkywayOrichalcum, twtnw),
        chest(382, CheckLocation.NaughtsSkywayMythrilCrystal, twtnw),
    ])
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
    ruin_creations_passage = graph.add_location(NodeId.RuinAndCreationsPassage, [
        chest(385, CheckLocation.RuinCreationsPassageMythrilStone, twtnw),
        chest(386, CheckLocation.RuinCreationsPassageApBoost, twtnw),
        chest(387, CheckLocation.RuinCreationsPassageMythrilCrystal, twtnw),
        chest(388, CheckLocation.RuinCreationsPassageOrichalcum, twtnw),
    ])
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
        graph.add_edge(xemnas_1, final_xemnas, RequirementEdge(battle=True, req=ItemPlacementHelpers.need_proofs))
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
        graph.add_edge(roxas, final_xemnas, RequirementEdge(battle=True, req=ItemPlacementHelpers.need_proofs))
        graph.add_edge(roxas, data_xemnas, RequirementEdge(battle=True))
        graph.register_first_boss(roxas)
        graph.register_last_story_boss(roxas)

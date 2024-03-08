from enum import Enum

from List.configDict import locationType, itemType
from List.inventory import magic, keyblade, ability, summon, report, storyunlock, form, misc
from List.location.graph import DefaultLogicGraph, RequirementEdge, chest, popup, hybrid_bonus, stat_bonus, item_bonus, \
    LocationGraphBuilder, START_NODE
from Module.itemPlacementRestriction import ItemPlacementHelpers


class NodeId(str, Enum):
    MarketplaceMapPopup = "Marketplace Map Popup"
    Borough = "Borough"
    BoroughChests = "Borough Chests"
    MerlinsHousePopup = "Merlin's House Popup"
    Bailey = "Bailey"
    BaseballCharmPopup = "Baseball Charm Popup"
    Postern = "Postern"
    PosternChests = "Postern Chests"
    Corridors = "Cooridors"
    CorridorsChests = "Cooridors Chests"
    DoorToDarknessPopup = "DTD Popup"
    AnsemsStudy = "Ansem's Study"
    AnsemsStudyChests = "Ansem's Study Chests"
    UkuleleCharm = "Ukulele Charm"
    UkuleleCharmChests = "Ukulele Charm Chests"
    RestorationSite = "Restoration Site"
    RestorationSiteChests = "Restoration Site Chests"
    DemyxHollowBastion = "Demyx (HB)"
    FinalFantasyFights = "Final Fantasy Fights"
    CrystalFissure = "Crystal Fissure"
    CrystalFissureChests = "Crystal Fissure Chests"
    ThousandHeartless = "1000 Heartless"
    GullWing = "Gull Wing"
    GullWingChests = "Gull Wing Chests"
    HeartlessManufactory = "Heartless Manufactory"
    HeartlessManufactoryChests = "Heartless Manufactory Chests"
    Sephiroth = "Sephiroth"
    Mushroom13 = "Mushroom 13"
    DataDemyx = "Data Demyx"
    CorDepths = "CoR Depths"
    CorDepthsChests = "CoR Depths Chests"
    CorMineshaftPreFigh1 = "CoR Mineshaft Pre-Fight 1"
    CorMineshaftPreFigh1Chests = "CoR Mineshaft Pre-Fight 1 Chests"
    CorDepthsPostFight1 = "CoR-Depths Post-Fight 1"
    CorDepthsPostFight1Chests = "CoR-Depths Post-Fight 1 Chests"
    CorMiningArea = "CoR Mining Area"
    CorMiningAreaChests = "CoR Mining Area Chests"
    CorMineshaftPreFight2 = "CoR Minshaft Pre-Fight 2"
    CorMineshaftPreFight2Chests = "CoR Minshaft Pre-Fight 2 Chests"
    CorEngineChamber = "CoR Engine Chamber"
    CorEngineChamberChests  = "CoR Engine Chamber Chests"
    CorMineshaftPostFight2 = "CoR Mineshaft Post Fight 2"
    CorMineshaftPostFight2Chests = "CoR Mineshaft Post Fight 2 Chests"
    CorMineshaftLastChest = "CoR Mineshaft Last Chest"
    CorMineshaftLastChestChests = "CoR Mineshaft Last Chest Chests"
    TransportToRemembrance = "Transport to Remembrance"


class CheckLocation(str, Enum):
    MarketplaceMap = "Marketplace Map"
    BoroughDriveRecovery = "Borough Drive Recovery"
    BoroughApBoost = "Borough AP Boost"
    BoroughHiPotion = "Borough Hi-Potion"
    BoroughMythrilShard = "Borough Mythril Shard"
    BoroughDarkShard = "Borough Dark Shard"
    MerlinsHouseMembershipCard = "Merlin's House Membership Card"
    MerlinsHouseBlizzardElement = "Merlin's House Blizzard Element"
    Bailey = "Bailey"
    BaileySecretAnsemReport7 = "Bailey Secret Ansem Report 7"
    BaseballCharm = "Baseball Charm"
    PosternCastlePerimeterMap = "Postern Castle Perimeter Map"
    PosternMythrilGem = "Postern Mythril Gem"
    PosternApBoost = "Postern AP Boost"
    CorridorsMythrilStone = "Corridors Mythril Stone"
    CorridorsMythrilCrystal = "Corridors Mythril Crystal"
    CorridorsDarkCrystal = "Corridors Dark Crystal"
    CorridorsApBoost = "Corridors AP Boost"
    AnsemsStudyMasterForm = "Ansem's Study Master Form"
    AnsemsStudySleepingLion = "Ansem's Study Sleeping Lion"
    AnsemsStudySkillRecipe = "Ansem's Study Skill Recipe"
    UkuleleCharm = "Ansem's Study Ukulele Charm"
    RestorationSiteMoonRecipe = "Restoration Site Moon Recipe"
    RestorationSiteApBoost = "Restoration Site AP Boost"
    DemyxHollowBastion = "Demyx (HB)"
    FinalFantasyFightsCureElement = "FF Fights Cure Element"
    CrystalFissureTornPages = "Crystal Fissure Torn Pages"
    CrystalFissureGreatMawMap = "Crystal Fissure The Great Maw Map"
    CrystalFissureEnergyCrystal = "Crystal Fissure Energy Crystal"
    CrystalFissureApBoost = "Crystal Fissure AP Boost"
    ThousandHeartless = "1000 Heartless"
    ThousandHeartlessSecretAnsemReport1 = "1000 Heartless Secret Ansem Report 1"
    ThousandHeartlessIceCream = "1000 Heartless Ice Cream"
    ThousandHeartlessPicture = "1000 Heartless Picture"
    PosternGullWing = "Postern Gull Wing"
    HeartlessManufactoryCosmicChain = "Heartless Manufactory Cosmic Chain"
    SephirothBonus = "Sephiroth Bonus"
    SephirothFenrir = "Sephiroth Fenrir"
    WinnersProof = "Winner's Proof"
    ProofOfPeace = "Proof of Peace"
    DataDemyxApBoost = "Demyx (Data) AP Boost"

    CorDepthsApBoost = "CoR Depths AP Boost"
    CorDepthsPowerCrystal = "CoR Depths Power Crystal"
    CorDepthsFrostCrystal = "CoR Depths Frost Crystal"
    CorDepthsManifestIllusion = "CoR Depths Manifest Illusion"
    CorDepthsApBoost2 = "CoR Depths AP Boost (2)"
    CorMineshaftLowerLevelDepthsOfRemembranceMap = "CoR Mineshaft Lower Level Depths of Remembrance Map"
    CorMineshaftLowerLevelApBoost = "CoR Mineshaft Lower Level AP Boost"
    CorDepthsUpperLevelRemembranceGem = "CoR Depths Upper Level Remembrance Gem"
    CorMiningAreaSerenityGem = "CoR Mining Area Serenity Gem"
    CorMiningAreaApBoost = "CoR Mining Area AP Boost"
    CorMiningAreaSerenityCrystal = "CoR Mining Area Serenity Crystal"
    CorMiningAreaManifestIllusion = "CoR Mining Area Manifest Illusion"
    CorMiningAreaSerenityGem2 = "CoR Mining Area Serenity Gem (2)"
    CorMiningAreaDarkRemembranceMap = "CoR Mining Area Dark Remembrance Map"
    CorMineshaftMidLevelPowerBoost = "CoR Mineshaft Mid Level Power Boost"
    CorEngineChamberSerenityCrystal = "CoR Engine Chamber Serenity Crystal"
    CorEngineChamberRemembranceCrystal = "CoR Engine Chamber Remembrance Crystal"
    CorEngineChamberApBoost = "CoR Engine Chamber AP Boost"
    CorEngineChamberManifestIllusion = "CoR Engine Chamber Manifest Illusion"
    CorMineshaftUpperLevelMagicBoost = "CoR Mineshaft Upper Level Magic Boost"
    CorMineshaftUpperLevelApBoost = "CoR Mineshaft Upper Level AP Boost"
    TransportToRemembrance = "Transport to Remembrance"

class HBLogicGraph(DefaultLogicGraph):
    def __init__(self,reverse_rando,keyblade_unlocks):
        DefaultLogicGraph.__init__(self,NodeId)
        hb_keyblade_lambda = lambda inv : not keyblade_unlocks or ItemPlacementHelpers.need_hb_keyblade(inv)
        cor_keyblade_lambda = lambda inv : not keyblade_unlocks or ItemPlacementHelpers.need_cor_keyblade(inv)
        self.logic[NodeId.Borough][NodeId.BoroughChests] = hb_keyblade_lambda
        self.logic[NodeId.Postern][NodeId.PosternChests] = hb_keyblade_lambda
        self.logic[NodeId.Corridors][NodeId.CorridorsChests] = hb_keyblade_lambda
        self.logic[NodeId.AnsemsStudy][NodeId.AnsemsStudyChests] = hb_keyblade_lambda
        self.logic[NodeId.UkuleleCharm][NodeId.UkuleleCharmChests] = hb_keyblade_lambda
        self.logic[NodeId.RestorationSite][NodeId.RestorationSiteChests] = hb_keyblade_lambda
        self.logic[NodeId.CrystalFissure][NodeId.CrystalFissureChests] = hb_keyblade_lambda
        self.logic[NodeId.GullWing][NodeId.GullWingChests] = hb_keyblade_lambda
        self.logic[NodeId.HeartlessManufactory][NodeId.HeartlessManufactoryChests] = hb_keyblade_lambda

        self.logic[NodeId.CorDepths][NodeId.CorDepthsChests] = cor_keyblade_lambda
        self.logic[NodeId.CorMineshaftPreFigh1][NodeId.CorMineshaftPreFigh1Chests] = cor_keyblade_lambda
        self.logic[NodeId.CorDepthsPostFight1][NodeId.CorDepthsPostFight1Chests] = cor_keyblade_lambda
        self.logic[NodeId.CorMiningArea][NodeId.CorMiningAreaChests] = cor_keyblade_lambda
        self.logic[NodeId.CorMineshaftPreFight2][NodeId.CorMineshaftPreFight2Chests] = cor_keyblade_lambda
        self.logic[NodeId.CorEngineChamber][NodeId.CorEngineChamberChests] = cor_keyblade_lambda
        self.logic[NodeId.CorMineshaftPostFight2][NodeId.CorMineshaftPostFight2Chests] = cor_keyblade_lambda
        self.logic[NodeId.CorMineshaftLastChest][NodeId.CorMineshaftLastChestChests] = cor_keyblade_lambda
        if not reverse_rando:
            self.logic[START_NODE][NodeId.MarketplaceMapPopup] = ItemPlacementHelpers.hb1_check
            self.logic[NodeId.BaseballCharmPopup][NodeId.Postern] = ItemPlacementHelpers.hb2_check
            self.logic[NodeId.DoorToDarknessPopup][NodeId.CorDepths] = ItemPlacementHelpers.need_growths
            self.logic[NodeId.ThousandHeartless][NodeId.Mushroom13] = ItemPlacementHelpers.need_proof_peace
            self.logic[NodeId.ThousandHeartless][NodeId.DataDemyx] = ItemPlacementHelpers.need_forms
        else:
            self.logic[START_NODE][NodeId.Borough] = ItemPlacementHelpers.hb1_check
            self.logic[NodeId.ThousandHeartless][NodeId.CorDepths] = lambda inv : ItemPlacementHelpers.hb2_check(inv) and ItemPlacementHelpers.need_growths(inv)
            self.logic[NodeId.BaseballCharmPopup][NodeId.DataDemyx] = ItemPlacementHelpers.need_forms
            

def make_graph(graph: LocationGraphBuilder):
    hb = locationType.HB
    cor = locationType.CoR
    hb_logic = HBLogicGraph(graph.reverse_rando,graph.keyblades_unlock_chests)
    graph.add_logic(hb_logic)

    marketplace_map_popup = graph.add_location(NodeId.MarketplaceMapPopup, [
        popup(362, CheckLocation.MarketplaceMap, hb),
    ])
    borough_chests = graph.add_location(NodeId.BoroughChests, [
        chest(194, CheckLocation.BoroughDriveRecovery, hb),
        chest(195, CheckLocation.BoroughApBoost, hb),
        chest(196, CheckLocation.BoroughHiPotion, hb),
        chest(305, CheckLocation.BoroughMythrilShard, hb),
        chest(506, CheckLocation.BoroughDarkShard, hb),
    ])
    borough = graph.add_location(NodeId.Borough, [])
    merlins_house_popup = graph.add_location(NodeId.MerlinsHousePopup, [
        popup(256, CheckLocation.MerlinsHouseMembershipCard, hb, vanilla=storyunlock.MembershipCard),
        popup(292, CheckLocation.MerlinsHouseBlizzardElement, hb, vanilla=magic.Blizzard),
    ])
    bailey = graph.add_location(NodeId.Bailey, [
        item_bonus(47, CheckLocation.Bailey, hb, vanilla=magic.Fire),
        popup(531, CheckLocation.BaileySecretAnsemReport7, hb, vanilla=report.AnsemReport7),
    ])
    baseball_charm_popup = graph.add_location(NodeId.BaseballCharmPopup, [
        popup(258, CheckLocation.BaseballCharm, hb, vanilla=summon.BaseballCharm),
    ])
    postern_chests = graph.add_location(NodeId.PosternChests, [
        chest(310, CheckLocation.PosternCastlePerimeterMap, hb),
        chest(189, CheckLocation.PosternMythrilGem, hb),
        chest(190, CheckLocation.PosternApBoost, hb),
    ])
    postern = graph.add_location(NodeId.Postern, [])
    corridors_chests = graph.add_location(NodeId.CorridorsChests, [
        chest(200, CheckLocation.CorridorsMythrilStone, hb),
        chest(201, CheckLocation.CorridorsMythrilCrystal, hb),
        chest(202, CheckLocation.CorridorsDarkCrystal, hb),
        chest(307, CheckLocation.CorridorsApBoost, hb),
    ])
    corridors = graph.add_location(NodeId.Corridors, [])
    dtd_popup = graph.add_location(NodeId.DoorToDarknessPopup, [
        popup(266, CheckLocation.AnsemsStudyMasterForm, hb, vanilla=form.MasterForm),
        popup(276, CheckLocation.AnsemsStudySleepingLion, hb, vanilla=keyblade.SleepingLion),
    ])
    ansems_study_chests = graph.add_location(NodeId.AnsemsStudyChests, [
        chest(184, CheckLocation.AnsemsStudySkillRecipe, hb),
    ])
    ansems_study = graph.add_location(NodeId.AnsemsStudy, [])
    ukulele_charm_chests = graph.add_location(NodeId.UkuleleCharmChests, [
        chest(183, CheckLocation.UkuleleCharm, hb, vanilla=summon.UkuleleCharm),
    ])
    ukulele_charm = graph.add_location(NodeId.UkuleleCharm, [])
    restoration_site_chests = graph.add_location(NodeId.RestorationSiteChests, [
        chest(309, CheckLocation.RestorationSiteMoonRecipe, hb),
        chest(507, CheckLocation.RestorationSiteApBoost, hb),
    ])
    restoration_site = graph.add_location(NodeId.RestorationSite, [])
    demyx = graph.add_location(NodeId.DemyxHollowBastion, [
        hybrid_bonus(28, CheckLocation.DemyxHollowBastion, hb, vanilla=magic.Blizzard),
    ])
    final_fantasy_fights = graph.add_location(NodeId.FinalFantasyFights, [
        popup(361, CheckLocation.FinalFantasyFightsCureElement, hb, vanilla=magic.Cure),
    ])
    crystal_fissure_chests = graph.add_location(NodeId.CrystalFissureChests, [
        chest(179, CheckLocation.CrystalFissureTornPages, hb, vanilla=misc.TornPages),
        chest(489, CheckLocation.CrystalFissureGreatMawMap, hb),
        chest(180, CheckLocation.CrystalFissureEnergyCrystal, hb),
        chest(181, CheckLocation.CrystalFissureApBoost, hb),
    ])
    crystal_fissure = graph.add_location(NodeId.CrystalFissure, [])
    thousand_heartless = graph.add_location(NodeId.ThousandHeartless, [
        item_bonus(60, CheckLocation.ThousandHeartless, hb, vanilla=ability.GuardBreak),
        popup(525, CheckLocation.ThousandHeartlessSecretAnsemReport1, hb, vanilla=report.AnsemReport1),
        popup(269, CheckLocation.ThousandHeartlessIceCream, hb, vanilla=storyunlock.IceCream),
        popup(511, CheckLocation.ThousandHeartlessPicture, hb),
    ])
    gull_wing_chests = graph.add_location(NodeId.GullWingChests, [
        chest(491, CheckLocation.PosternGullWing, hb, vanilla=keyblade.GullWing),
    ])
    gull_wing = graph.add_location(NodeId.GullWing, [])
    heartless_manufactory_chests = graph.add_location(NodeId.HeartlessManufactoryChests, [
        chest(311, CheckLocation.HeartlessManufactoryCosmicChain, hb, invalid_checks=[itemType.MANUFACTORYUNLOCK]),
    ])
    heartless_manufactory = graph.add_location(NodeId.HeartlessManufactory, [])
    sephiroth = graph.add_location(NodeId.Sephiroth, [
        stat_bonus(35, CheckLocation.SephirothBonus, [hb, locationType.Sephi]),
        popup(282, CheckLocation.SephirothFenrir, [hb, locationType.Sephi], vanilla=keyblade.Fenrir),
    ])
    mushroom_13 = graph.add_location(NodeId.Mushroom13, [
        popup(588, CheckLocation.WinnersProof, [hb, locationType.Mush13], invalid_checks=[itemType.PROOF_OF_PEACE],
              vanilla=keyblade.WinnersProof),
        popup(589, CheckLocation.ProofOfPeace, [hb, locationType.Mush13], invalid_checks=[itemType.PROOF_OF_PEACE]),
    ])
    data_demyx = graph.add_location(NodeId.DataDemyx, [
        popup(560, CheckLocation.DataDemyxApBoost, [hb, locationType.DataOrg], invalid_checks=[itemType.FORM]),
    ])

    cor_depths_chests = graph.add_location(NodeId.CorDepthsChests, [
        chest(562, CheckLocation.CorDepthsApBoost, [hb, cor]),
        chest(563, CheckLocation.CorDepthsPowerCrystal, [hb, cor]),
        chest(564, CheckLocation.CorDepthsFrostCrystal, [hb, cor]),
        chest(565, CheckLocation.CorDepthsManifestIllusion, [hb, cor]),
        chest(566, CheckLocation.CorDepthsApBoost2, [hb, cor]),
    ])
    cor_depths = graph.add_location(NodeId.CorDepths, [])
    cor_mineshaft_pre_fight_1_chests = graph.add_location(NodeId.CorMineshaftPreFigh1Chests, [
        chest(580, CheckLocation.CorMineshaftLowerLevelDepthsOfRemembranceMap, [hb, cor]),
        chest(578, CheckLocation.CorMineshaftLowerLevelApBoost, [hb, cor]),
    ])
    cor_mineshaft_pre_fight_1 = graph.add_location(NodeId.CorMineshaftPreFigh1, [])
    cor_depths_post_fight_1_chests = graph.add_location(NodeId.CorDepthsPostFight1Chests, [
        chest(567, CheckLocation.CorDepthsUpperLevelRemembranceGem, [hb, cor]),
    ])
    cor_depths_post_fight_1 = graph.add_location(NodeId.CorDepthsPostFight1, [])
    cor_mining_area_chests = graph.add_location(NodeId.CorMiningAreaChests, [
        chest(568, CheckLocation.CorMiningAreaSerenityGem, [hb, cor]),
        chest(569, CheckLocation.CorMiningAreaApBoost, [hb, cor]),
        chest(570, CheckLocation.CorMiningAreaSerenityCrystal, [hb, cor]),
        chest(571, CheckLocation.CorMiningAreaManifestIllusion, [hb, cor]),
        chest(572, CheckLocation.CorMiningAreaSerenityGem2, [hb, cor]),
        chest(573, CheckLocation.CorMiningAreaDarkRemembranceMap, [hb, cor]),
    ])
    cor_mining_area = graph.add_location(NodeId.CorMiningArea, [])
    cor_mineshaft_pre_fight_2_chests = graph.add_location(NodeId.CorMineshaftPreFight2Chests, [
        chest(581, CheckLocation.CorMineshaftMidLevelPowerBoost, [hb, cor]),
    ])
    cor_mineshaft_pre_fight_2 = graph.add_location(NodeId.CorMineshaftPreFight2, [])
    cor_engine_chamber_chests = graph.add_location(NodeId.CorEngineChamberChests, [
        chest(574, CheckLocation.CorEngineChamberSerenityCrystal, [hb, cor]),
        chest(575, CheckLocation.CorEngineChamberRemembranceCrystal, [hb, cor]),
        chest(576, CheckLocation.CorEngineChamberApBoost, [hb, cor]),
        chest(577, CheckLocation.CorEngineChamberManifestIllusion, [hb, cor]),
    ])
    cor_engine_chamber = graph.add_location(NodeId.CorEngineChamber, [])
    cor_mineshaft_post_fight_2_chests = graph.add_location(NodeId.CorMineshaftPostFight2Chests, [
        chest(582, CheckLocation.CorMineshaftUpperLevelMagicBoost, [hb, cor]),
    ])
    cor_mineshaft_post_fight_2 = graph.add_location(NodeId.CorMineshaftPostFight2, [])
    cor_mineshaft_last_chest_chests = graph.add_location(NodeId.CorMineshaftLastChestChests, [
        chest(579, CheckLocation.CorMineshaftUpperLevelApBoost, [hb, cor]),
    ])
    cor_mineshaft_last_chest = graph.add_location(NodeId.CorMineshaftLastChest, [])
    transport_to_remembrance = graph.add_location(NodeId.TransportToRemembrance, [
        stat_bonus(72, CheckLocation.TransportToRemembrance, [hb, locationType.TTR]),
    ])

    graph.register_superboss(data_demyx)
    
    graph.add_edge(borough, borough_chests)
    graph.add_edge(postern, postern_chests)
    graph.add_edge(corridors, corridors_chests)
    graph.add_edge(ansems_study, ansems_study_chests)
    graph.add_edge(ukulele_charm, ukulele_charm_chests)
    graph.add_edge(restoration_site, restoration_site_chests)
    graph.add_edge(crystal_fissure, crystal_fissure_chests)
    graph.add_edge(gull_wing, gull_wing_chests)
    graph.add_edge(heartless_manufactory, heartless_manufactory_chests)
    
    graph.add_edge(cor_depths, cor_depths_chests)
    graph.add_edge(cor_mineshaft_pre_fight_1, cor_mineshaft_pre_fight_1_chests)
    graph.add_edge(cor_depths_post_fight_1, cor_depths_post_fight_1_chests)
    graph.add_edge(cor_mining_area, cor_mining_area_chests)
    graph.add_edge(cor_mineshaft_pre_fight_2, cor_mineshaft_pre_fight_2_chests)
    graph.add_edge(cor_engine_chamber, cor_engine_chamber_chests)
    graph.add_edge(cor_mineshaft_post_fight_2, cor_mineshaft_post_fight_2_chests)
    graph.add_edge(cor_mineshaft_last_chest, cor_mineshaft_last_chest_chests)

    if not graph.reverse_rando:
        graph.add_edge(START_NODE, marketplace_map_popup)
        graph.add_edge(marketplace_map_popup, borough)
        graph.add_edge(borough, merlins_house_popup)
        graph.add_edge(merlins_house_popup, bailey, RequirementEdge(battle=True))
        graph.add_edge(bailey, baseball_charm_popup)
        graph.add_edge(baseball_charm_popup, postern)
        graph.add_edge(postern, corridors)
        graph.add_edge(corridors, dtd_popup)
        graph.add_edge(corridors, ansems_study)
        graph.add_edge(dtd_popup, ukulele_charm)

        graph.add_edge(dtd_popup, cor_depths)
        graph.add_edge(cor_depths, cor_mineshaft_pre_fight_1)
        graph.add_edge(cor_mineshaft_pre_fight_1, cor_depths_post_fight_1, RequirementEdge(battle=True))
        graph.add_edge(cor_depths_post_fight_1, cor_mining_area)
        graph.add_edge(cor_mining_area, cor_mineshaft_pre_fight_2)
        graph.add_edge(cor_mineshaft_pre_fight_2, cor_engine_chamber, RequirementEdge(battle=True))
        graph.add_edge(cor_engine_chamber, cor_mineshaft_post_fight_2)
        graph.add_edge(cor_mineshaft_post_fight_2, cor_mineshaft_last_chest)
        graph.add_edge(cor_mineshaft_last_chest, transport_to_remembrance, RequirementEdge(battle=True))

        graph.add_edge(dtd_popup, restoration_site, RequirementEdge(battle=True))
        graph.add_edge(restoration_site, demyx, RequirementEdge(battle=True))
        graph.add_edge(demyx, final_fantasy_fights, RequirementEdge(battle=True))
        graph.add_edge(final_fantasy_fights, crystal_fissure)
        graph.add_edge(crystal_fissure, thousand_heartless, RequirementEdge(battle=True))
        graph.add_edge(thousand_heartless, gull_wing)
        graph.add_edge(thousand_heartless, heartless_manufactory)
        graph.add_edge(thousand_heartless, sephiroth, RequirementEdge(battle=True))
        graph.add_edge(thousand_heartless, mushroom_13)
        graph.add_edge(thousand_heartless, data_demyx,
                       RequirementEdge(battle=True))
        graph.register_first_boss(baseball_charm_popup)
        graph.register_last_story_boss(thousand_heartless)
        graph.register_superboss(sephiroth)
    else:
        graph.add_edge(START_NODE, borough)
        graph.add_edge(borough, postern)
        graph.add_edge(postern, corridors)
        graph.add_edge(corridors, dtd_popup)
        graph.add_edge(corridors, ansems_study)
        graph.add_edge(dtd_popup, ukulele_charm)
        graph.add_edge(dtd_popup, restoration_site, RequirementEdge(battle=True))
        graph.add_edge(restoration_site, demyx, RequirementEdge(battle=True))
        graph.add_edge(demyx, final_fantasy_fights, RequirementEdge(battle=True))
        graph.add_edge(final_fantasy_fights, crystal_fissure)
        graph.add_edge(crystal_fissure, thousand_heartless, RequirementEdge(battle=True))
        graph.add_edge(thousand_heartless, gull_wing)
        graph.add_edge(thousand_heartless, heartless_manufactory)
        graph.add_edge(thousand_heartless, cor_depths)
        graph.add_edge(cor_depths, cor_mineshaft_pre_fight_1)
        graph.add_edge(cor_mineshaft_pre_fight_1, cor_depths_post_fight_1, RequirementEdge(battle=True))
        graph.add_edge(cor_depths_post_fight_1, cor_mining_area)
        graph.add_edge(cor_mining_area, cor_mineshaft_pre_fight_2)
        graph.add_edge(cor_mineshaft_pre_fight_2, cor_engine_chamber, RequirementEdge(battle=True))
        graph.add_edge(cor_engine_chamber, cor_mineshaft_post_fight_2)
        graph.add_edge(cor_mineshaft_post_fight_2, cor_mineshaft_last_chest)
        graph.add_edge(cor_mineshaft_last_chest, transport_to_remembrance, RequirementEdge(battle=True))
        graph.add_edge(transport_to_remembrance, mushroom_13)
        graph.add_edge(transport_to_remembrance, sephiroth)
        graph.add_edge(sephiroth, marketplace_map_popup)
        graph.add_edge(marketplace_map_popup, merlins_house_popup)
        graph.add_edge(merlins_house_popup, bailey, RequirementEdge(battle=True))
        graph.add_edge(bailey, baseball_charm_popup)
        graph.add_edge(baseball_charm_popup, data_demyx,
                       RequirementEdge(battle=True))
        graph.register_first_boss(thousand_heartless)
        graph.register_last_story_boss(bailey)

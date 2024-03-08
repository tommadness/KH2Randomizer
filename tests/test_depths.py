import unittest
from typing import Iterable

from Class.newLocationClass import KH2Location
from Class.seedSettings import SeedSettings
from List.NewLocationList import Locations
from List.configDict import locationDepth, locationType
from List.location import hollowbastion, hundredacrewood, atlantica, simulatedtwilighttown, twilighttown,\
    landofdragons, beastscastle, olympuscoliseum, disneycastle, portroyal, agrabah, halloweentown, pridelands,\
    spaceparanoids, worldthatneverwas
from List.location.graph import START_NODE
from Module.RandomizerSettings import RandomizerSettings
from Module.depths import ItemDepths


class Tests(unittest.TestCase):

    def setUp(self):
        seed_settings = SeedSettings()
        settings = RandomizerSettings("test_name", True, "version", seed_settings, "")
        self.locations = Locations(settings, secondary_graph=False)

    def test_anywhere(self):
        locations = self.locations
        depths = ItemDepths(locationDepth.Anywhere, locations)

        # All locations should be valid
        for location in locations.all_locations():
            self._assert_location_valid(location, depths)

    def test_non_superboss(self):
        locations = self.locations
        depths = ItemDepths(locationDepth.NonSuperboss, locations)

        # Superbosses are invalid
        self._assert_validity(locations.superboss_nodes, depths, False)

        # Anything else should be valid
        self._assert_node_valid(START_NODE, depths)
        self._assert_validity(_sample_first_visit_nodes(), depths, True)
        self._assert_validity(locations.first_boss_nodes, depths, True)
        self._assert_validity(_sample_second_visit_nodes(), depths, True)
        self._assert_validity(locations.last_story_boss_nodes, depths, True)
        self._assert_validity(hundredacrewood.NodeId, depths, True)
        self._assert_validity(atlantica.NodeId, depths, True)
        self._assert_misc_locations_validity(depths, valid=True)

    def test_first_visit(self):
        locations = self.locations
        depths = ItemDepths(locationDepth.FirstVisit, locations)

        # First visits (including first bosses) are valid
        self._assert_validity(_sample_first_visit_nodes(), depths, True)
        self._assert_validity(locations.first_boss_nodes, depths, True)

        # Starting locations are not considered any visit
        self._assert_node_invalid(START_NODE, depths)

        self._assert_validity(_sample_second_visit_nodes(), depths, False)

        for last_story_boss_node in locations.last_story_boss_nodes:
            # Sometimes the last story boss is the same as the first boss.
            # In this case that node isn't actually invalid.
            if last_story_boss_node not in locations.first_boss_nodes:
                self._assert_node_invalid(last_story_boss_node, depths)

        # Hundred Acre Wood and Atlantica are not considered any visit
        self._assert_validity(hundredacrewood.NodeId, depths, False)
        self._assert_validity(atlantica.NodeId, depths, False)

        self._assert_misc_locations_validity(depths, valid=False)

    def test_first_boss(self):
        locations = self.locations
        depths = ItemDepths(locationDepth.FirstBoss, locations)

        expected_first_boss_nodes = _expected_first_boss_nodes()
        for first_boss_node in expected_first_boss_nodes:
            # Only one location per boss node is considered the "preferred" location.
            # This is by design to help keep things spread out.
            first_boss_locations = locations.locations_for_node(first_boss_node)
            preferred_location = ItemDepths.preferred_boss_location(first_boss_locations)
            self._assert_location_valid(preferred_location, depths)
            for invalid_location in (loc for loc in first_boss_locations if loc != preferred_location):
                self._assert_location_invalid(invalid_location, depths)

        # Anything else is invalid
        for node_id in locations.node_ids():
            if node_id not in expected_first_boss_nodes:
                self._assert_node_invalid(node_id, depths)

    def test_second_visit_only(self):
        locations = self.locations
        depths = ItemDepths(locationDepth.SecondVisitOnly, locations)

        # Second visits are valid, including last story bosses (as long as the last story boss isn't the same as the
        # first boss)
        self._assert_validity(_sample_second_visit_nodes(), depths, True)
        for last_story_boss_node in locations.last_story_boss_nodes:
            if last_story_boss_node not in locations.first_boss_nodes:
                self._assert_node_valid(last_story_boss_node, depths)

        # These worlds have no "second visit" so there shouldn't be any valid locations there
        self._assert_validity(disneycastle.NodeId, depths, valid=False)
        self._assert_validity(simulatedtwilighttown.NodeId, depths, valid=False)
        self._assert_validity(worldthatneverwas.NodeId, depths, valid=False)

        # Hundred Acre Wood and Atlantica are not considered any visit
        self._assert_validity(hundredacrewood.NodeId, depths, False)
        self._assert_validity(atlantica.NodeId, depths, False)

        # Anything else is invalid
        self._assert_node_invalid(START_NODE, depths)
        self._assert_validity(_sample_first_visit_nodes(), depths, False)
        self._assert_validity(locations.first_boss_nodes, depths, False)
        self._assert_validity(locations.superboss_nodes, depths, False)
        self._assert_misc_locations_validity(depths, valid=False)

    def test_last_story_boss(self):
        locations = self.locations
        depths = ItemDepths(locationDepth.LastStoryBoss, locations)

        expected_last_story_boss_nodes = _expected_last_story_boss_nodes()
        for last_story_boss_node in expected_last_story_boss_nodes:
            # Only one location per boss node is considered the "preferred" location.
            # This is by design to help keep things spread out.
            last_story_boss_locations = locations.locations_for_node(last_story_boss_node)
            preferred_location = ItemDepths.preferred_boss_location(last_story_boss_locations)
            self._assert_location_valid(preferred_location, depths)
            for invalid_location in (loc for loc in last_story_boss_locations if loc != preferred_location):
                self._assert_location_invalid(invalid_location, depths)

        # Anything else is invalid
        for node_id in locations.node_ids():
            if node_id not in expected_last_story_boss_nodes:
                self._assert_node_invalid(node_id, depths)

    def test_superbosses(self):
        locations = self.locations
        depths = ItemDepths(locationDepth.Superbosses, locations)

        expected_superboss_nodes = _expected_superboss_nodes()
        for superboss_node in expected_superboss_nodes:
            # Only one location per boss node is considered the "preferred" location.
            # This is by design to help keep things spread out.
            superboss_locations = locations.locations_for_node(superboss_node)
            preferred_location = ItemDepths.preferred_boss_location(superboss_locations)
            self._assert_location_valid(preferred_location, depths)
            for invalid_location in (loc for loc in superboss_locations if loc != preferred_location):
                self._assert_location_invalid(invalid_location, depths)

        # Anything else is invalid
        for node_id in locations.node_ids():
            if node_id not in expected_superboss_nodes:
                self._assert_node_invalid(node_id, depths)

    def test_no_first_visit(self):
        depths = ItemDepths(locationDepth.NoFirstVisit, self.locations)

        # First visits (including first bosses) are invalid
        self._assert_validity(_sample_first_visit_nodes(), depths, False)
        self._assert_validity(self.locations.first_boss_nodes, depths, False)

        # Starting locations are not considered any visit, so are technically valid here
        self._assert_node_valid(START_NODE, depths)

        # Hundred Acre Wood and Atlantica are not considered any visit, so are technically valid here
        self._assert_validity(hundredacrewood.NodeId, depths, True)
        self._assert_validity(atlantica.NodeId, depths, True)

        # Anything else should be valid
        self._assert_validity(_sample_second_visit_nodes(), depths, True)
        self._assert_misc_locations_validity(depths, valid=True)

    def _assert_location_valid(self, location: KH2Location, depths: ItemDepths):
        self.assertTrue(
            depths.is_valid(location),
            msg=f"Expected {location} to be valid for [{depths.location_depth}]"
        )

    def _assert_location_invalid(self, location: KH2Location, depths: ItemDepths):
        self.assertFalse(
            depths.is_valid(location),
            msg=f"Expected {location} to be invalid for [{depths.location_depth}]"
        )

    def _assert_node_valid(self, node_id: str, depths: ItemDepths):
        for location in self.locations.locations_for_node(node_id):
            self._assert_location_valid(location, depths)

    def _assert_node_invalid(self, node_id: str, depths: ItemDepths):
        for location in self.locations.locations_for_node(node_id):
            self._assert_location_invalid(location, depths)

    def _assert_validity(self, node_ids: Iterable[str], depths: ItemDepths, valid: bool):
        for node_id in node_ids:
            if valid:
                self._assert_node_valid(node_id, depths)
            else:
                self._assert_node_invalid(node_id, depths)

    def _assert_misc_locations_validity(self, depths: ItemDepths, valid: bool):
        def checker(loc: KH2Location):
            if valid:
                self._assert_location_valid(loc, depths)
            else:
                self._assert_location_invalid(loc, depths)

        for location in self.locations.all_locations():
            primary_type = location.LocationTypes[0]
            if primary_type in [locationType.Level, locationType.FormLevel, locationType.SYNTH, locationType.Puzzle]:
                checker(location)


def _sample_first_visit_nodes() -> list[str]:
    """
    A set of known first visit node IDs. Done this way to avoid tests being coupled to the same logic that's
    implementing the code being tested.
    """
    return [
        simulatedtwilighttown.NodeId.MunnyPouchPopup,
        simulatedtwilighttown.NodeId.Axel2,
        simulatedtwilighttown.NodeId.SimulatedMansionBasementChests,
        twilighttown.NodeId.OldMansion,
        twilighttown.NodeId.YenSidTowerEntryway,
        twilighttown.NodeId.TowerWardrobe,
        twilighttown.NodeId.ValorForm,
        hollowbastion.NodeId.Borough,
        hollowbastion.NodeId.Bailey,
        hollowbastion.NodeId.BaseballCharmPopup,
        landofdragons.NodeId.BambooGrove,
        landofdragons.NodeId.MountainTrail,
        landofdragons.NodeId.Ridge,
        landofdragons.NodeId.ShanYu,
        beastscastle.NodeId.BeastsCastleCourtyard,
        beastscastle.NodeId.WestHall,
        beastscastle.NodeId.BeastsRoom,
        beastscastle.NodeId.DarkThorn,
        olympuscoliseum.NodeId.Passage,
        olympuscoliseum.NodeId.UrnsBonus,
        olympuscoliseum.NodeId.PeteOlympusColiseum,
        olympuscoliseum.NodeId.Hydra,
        disneycastle.NodeId.DisneyCastleCourtyard,
        disneycastle.NodeId.CornerstoneHill,
        disneycastle.NodeId.BoatPete,
        disneycastle.NodeId.FuturePete,
        disneycastle.NodeId.WisdomPopup,
        portroyal.NodeId.Rampart,
        portroyal.NodeId.IslaDeMuertaPopup,
        portroyal.NodeId.MoonlightNook,
        portroyal.NodeId.Barbossa,
        agrabah.NodeId.AgrabahMapPopup,
        agrabah.NodeId.CaveOfWondersEntrance,
        agrabah.NodeId.TreasureRoom,
        agrabah.NodeId.ElementalLords,
        halloweentown.NodeId.Graveyard,
        halloweentown.NodeId.CandyCaneLane,
        halloweentown.NodeId.PrisonKeeper,
        halloweentown.NodeId.OogieBoogie,
        pridelands.NodeId.Gorge,
        pridelands.NodeId.WildebeestValley,
        pridelands.NodeId.Hyenas1Bonus,
        pridelands.NodeId.Scar,
        spaceparanoids.NodeId.PitCell,
        spaceparanoids.NodeId.ScreensBonus,
        spaceparanoids.NodeId.HostileProgram,
        spaceparanoids.NodeId.PhotonDebugger,
        worldthatneverwas.NodeId.FragmentCrossing,
        worldthatneverwas.NodeId.NothingsCall,
        worldthatneverwas.NodeId.Luxord,
        worldthatneverwas.NodeId.RuinAndCreationsPassage,
        worldthatneverwas.NodeId.Xemnas1,
    ]


def _sample_second_visit_nodes() -> list[str]:
    """
    A set of known second visit node IDs. Done this way to avoid tests being coupled to the same logic that's
    implementing the code being tested.
    """
    return [
        hollowbastion.NodeId.AnsemsStudy,
        hollowbastion.NodeId.CorMiningArea,
        hollowbastion.NodeId.ThousandHeartless,
        hollowbastion.NodeId.TransportToRemembrance,
        twilighttown.NodeId.LimitForm,
        twilighttown.NodeId.UndergroundConcourse,
        twilighttown.NodeId.MansionBasement,
        twilighttown.NodeId.BetwixtAndBetween,
        landofdragons.NodeId.ThroneRoom,
        landofdragons.NodeId.StormRider,
        beastscastle.NodeId.RumblingRose,
        beastscastle.NodeId.Xaldin,
        olympuscoliseum.NodeId.AuronsStatue,
        olympuscoliseum.NodeId.Hades,
        portroyal.NodeId.GrimReaper1,
        portroyal.NodeId.SeadriftKeep,
        portroyal.NodeId.CursedMedallionPopup,
        portroyal.NodeId.GrimReaper2,
        agrabah.NodeId.RuinedChamber,
        agrabah.NodeId.GenieJafar,
        halloweentown.NodeId.LockShockBarrel,
        halloweentown.NodeId.DecoyPresentMinigame,
        halloweentown.NodeId.Experiment,
        pridelands.NodeId.Hyenas2Bonus,
        pridelands.NodeId.Groundshaker,
        spaceparanoids.NodeId.SolarSailerBonus,
        spaceparanoids.NodeId.CentralComputerCore,
        spaceparanoids.NodeId.MasterControlProgramBonus,
    ]


def _expected_first_boss_nodes() -> list[str]:
    """
    A set of known superboss node IDs. Done this way to avoid tests being coupled to the same logic that's
    implementing the code being tested.
    """
    return [
        worldthatneverwas.NodeId.Xemnas1,
        landofdragons.NodeId.ShanYu,
        beastscastle.NodeId.DarkThorn,
        halloweentown.NodeId.OogieBoogie,
        agrabah.NodeId.ElementalLords,
        olympuscoliseum.NodeId.Hydra,
        pridelands.NodeId.Scar,
        twilighttown.NodeId.ValorForm,
        hollowbastion.NodeId.BaseballCharmPopup,
        portroyal.NodeId.Barbossa,
        disneycastle.NodeId.WisdomPopup,
        spaceparanoids.NodeId.PhotonDebugger,
        simulatedtwilighttown.NodeId.SimulatedMansionBasementChests,
    ]


def _expected_last_story_boss_nodes() -> list[str]:
    """
    A set of known last story boss node IDs. Done this way to avoid tests being coupled to the same logic that's
    implementing the code being tested.
    """
    return [
        worldthatneverwas.NodeId.Xemnas1,
        landofdragons.NodeId.StormRider,
        beastscastle.NodeId.Xaldin,
        halloweentown.NodeId.Experiment,
        agrabah.NodeId.GenieJafar,
        olympuscoliseum.NodeId.Hades,
        pridelands.NodeId.Groundshaker,
        twilighttown.NodeId.BetwixtAndBetween,
        hollowbastion.NodeId.ThousandHeartless,
        portroyal.NodeId.GrimReaper2,
        disneycastle.NodeId.WisdomPopup,
        spaceparanoids.NodeId.MasterControlProgramBonus,
        simulatedtwilighttown.NodeId.SimulatedMansionBasementChests,
    ]


def _expected_superboss_nodes() -> list[str]:
    """
    A set of known superboss node IDs. Done this way to avoid tests being coupled to the same logic that's
    implementing the code being tested.
    """
    return [
        worldthatneverwas.NodeId.DataXemnas,
        landofdragons.NodeId.DataXigbar,
        beastscastle.NodeId.DataXaldin,
        halloweentown.NodeId.Vexen,
        halloweentown.NodeId.DataVexen,
        agrabah.NodeId.Lexaeus,
        agrabah.NodeId.DataLexaeus,
        olympuscoliseum.NodeId.Zexion,
        olympuscoliseum.NodeId.DataZexion,
        pridelands.NodeId.DataSaix,
        twilighttown.NodeId.DataAxel,
        hollowbastion.NodeId.DataDemyx,
        portroyal.NodeId.DataLuxord,
        disneycastle.NodeId.Marluxia,
        disneycastle.NodeId.DataMarluxia,
        spaceparanoids.NodeId.Larxene,
        spaceparanoids.NodeId.DataLarxene,
        simulatedtwilighttown.NodeId.DataRoxas,
        hollowbastion.NodeId.Sephiroth,
        disneycastle.NodeId.LingeringWill,
    ]


if __name__ == '__main__':
    unittest.main()

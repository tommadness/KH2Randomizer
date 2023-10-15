import unittest
from datetime import datetime

from Class import settingkey
from Class.seedSettings import SeedSettings
from List.NewLocationList import Locations
from List.inventory import storyunlock, misc, proof, form, magic
from List.inventory.item import InventoryItem
from List.location import landofdragons as lod, twilighttown as tt, hundredacrewood as haw, worldthatneverwas, \
    hollowbastion, agrabah as ag, disneycastle
from Module.newRandomize import RandomizerSettings
from Module.seedEvaluation import LocationInformedSeedValidator


class Tests(unittest.TestCase):

    def setUp(self):
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.STARTING_INVENTORY, [])

        seed_name = f"{datetime.now()}"
        settings = RandomizerSettings(seed_name, True, "version", seed_settings, "")
        self.locations = Locations(settings, secondary_graph=False)

        validator = LocationInformedSeedValidator()
        # TODO: Are there tests we can add for synthesis recipes?
        validator.prepare_requirements_list([self.locations], synthesis_recipes=[])
        self.validator = validator

        self.inventory: list[int] = []

    def test_final_door(self):
        """ Verifies all 3 proofs are required to access Final Xemnas. """
        final_xemnas = [worldthatneverwas.NodeId.FinalXemnas]
        self._assert_unavailable(final_xemnas)
        self._collect(proof.ProofOfPeace)
        self._collect(proof.ProofOfConnection)
        self._assert_unavailable(final_xemnas)
        self._collect(proof.ProofOfNonexistence)
        self._assert_available(final_xemnas)

    def test_data_demyx(self):
        """ Verifies Membership Card and all 5 forms are required to access Data Demyx. """
        data_demyx = [hollowbastion.NodeId.DataDemyx]
        self._assert_unavailable(data_demyx)
        self._collect(storyunlock.MembershipCard)
        self._collect(form.ValorForm)
        self._collect(form.WisdomForm)
        self._collect(form.LimitForm)
        self._collect(form.MasterForm)
        self._assert_unavailable(data_demyx)
        self._collect(form.FinalForm)
        self._assert_available(data_demyx)

    def test_mushroom_13(self):
        """ Verifies both Membership Card and Proof of Peace are required to access the Mushroom 13 check. """
        mushroom_13 = [hollowbastion.NodeId.Mushroom13]
        self._assert_unavailable(mushroom_13)
        self._collect(storyunlock.MembershipCard)
        self._assert_unavailable(mushroom_13)
        self._uncollect(storyunlock.MembershipCard)
        self._collect(proof.ProofOfPeace)
        self._assert_unavailable(mushroom_13)
        self._collect(storyunlock.MembershipCard)
        self._assert_available(mushroom_13)

    def test_lingering_will(self):
        """ Verifies Proof of Connection is required to access Lingering Will. """
        lingering_will = [disneycastle.NodeId.LingeringWill]
        self._assert_unavailable(lingering_will)
        self._collect(proof.ProofOfNonexistence)
        self._assert_unavailable(lingering_will)
        self._collect(proof.ProofOfPeace)
        self._assert_unavailable(lingering_will)
        self._collect(proof.ProofOfConnection)
        self._assert_available(lingering_will)
        self._uncollect(proof.ProofOfNonexistence)
        self._uncollect(proof.ProofOfPeace)
        self._assert_available(lingering_will)

    def test_lod_unlock(self):
        """ Verifies Sword of the Ancestor is required to access Land of Dragons 2. """
        lod2_nodes = [lod.NodeId.ThroneRoom, lod.NodeId.StormRider, lod.NodeId.DataXigbar]
        self._assert_unavailable(lod2_nodes)
        self._collect(storyunlock.SwordOfTheAncestor)
        self._assert_available(lod2_nodes)

    def test_ag_unlock(self):
        """ Verifies Scimitar and one of each blizzard/fire/thunder is required to access Agrabah 2. """
        ag2_nodes = [ag.NodeId.RuinedChamber, ag.NodeId.GenieJafar, ag.NodeId.Lexaeus, ag.NodeId.DataLexaeus]
        self._assert_unavailable(ag2_nodes)
        self._collect(storyunlock.Scimitar)
        self._assert_unavailable(ag2_nodes)
        self._collect(magic.Fire)
        self._collect(magic.Fire)
        self._collect(magic.Fire)
        self._assert_unavailable(ag2_nodes)
        self._collect(magic.Thunder)
        self._assert_unavailable(ag2_nodes)
        self._collect(magic.Thunder)
        self._assert_unavailable(ag2_nodes)
        self._collect(magic.Blizzard)
        self._assert_available(ag2_nodes)

    def test_tt2_unlock(self):
        """ Verifies Picture is required to access Twilight Town 2. """
        tt2_nodes = [tt.NodeId.SeifersTrophy, tt.NodeId.LimitForm]
        self._assert_unavailable(tt2_nodes)
        self._collect(storyunlock.IceCream)
        self._assert_unavailable(tt2_nodes)
        self._uncollect(storyunlock.IceCream)
        self._collect(storyunlock.Picture)
        self._assert_available(tt2_nodes)
        self._collect(storyunlock.IceCream)
        self._assert_available(tt2_nodes)

    def test_tt3_unlock(self):
        """ Verifies Picture and Ice Cream are both required to access Twilight Town 3. """
        tt3_nodes = [
            tt.NodeId.UndergroundConcourse,
            tt.NodeId.Tunnelway,
            tt.NodeId.SunsetTerrace,
            tt.NodeId.MansionBonus,
            tt.NodeId.MansionFoyer,
            tt.NodeId.MansionDiningRoom,
            tt.NodeId.MansionLibrary,
            tt.NodeId.TwilightTownBeam,
            tt.NodeId.MansionBasement,
            tt.NodeId.BetwixtAndBetween,
            tt.NodeId.DataAxel,
        ]

        self._assert_unavailable(tt3_nodes)

        # Just Ice Cream isn't enough
        self._collect(storyunlock.IceCream)
        self._assert_unavailable(tt3_nodes)

        # Just Picture isn't enough
        self._uncollect(storyunlock.IceCream)
        self._collect(storyunlock.Picture)
        self._assert_unavailable(tt3_nodes)

        # Both Picture and Ice Cream
        self._collect(storyunlock.IceCream)
        self._assert_available(tt3_nodes)

    def test_hundred_acre_wood_unlocks(self):
        """ Verifies the appropriate number of Torn Pages are required to access each Hundred Acre Wood location. """
        self._assert_unavailable([
            haw.NodeId.PigletsHowse,
            haw.NodeId.RabbitsHowse,
            haw.NodeId.KangasHowse,
            haw.NodeId.SpookyCave,
            haw.NodeId.StarryHill
        ])

        self._collect(misc.TornPages)
        self._assert_available([haw.NodeId.PigletsHowse])
        self._assert_unavailable([
            haw.NodeId.RabbitsHowse,
            haw.NodeId.KangasHowse,
            haw.NodeId.SpookyCave,
            haw.NodeId.StarryHill
        ])

        self._collect(misc.TornPages)
        self._assert_available([haw.NodeId.PigletsHowse, haw.NodeId.RabbitsHowse])
        self._assert_unavailable([haw.NodeId.KangasHowse, haw.NodeId.SpookyCave, haw.NodeId.StarryHill])

        self._collect(misc.TornPages)
        self._assert_available([haw.NodeId.PigletsHowse, haw.NodeId.RabbitsHowse, haw.NodeId.KangasHowse])
        self._assert_unavailable([haw.NodeId.SpookyCave, haw.NodeId.StarryHill])

        self._collect(misc.TornPages)
        self._assert_available([
            haw.NodeId.PigletsHowse,
            haw.NodeId.RabbitsHowse,
            haw.NodeId.KangasHowse,
            haw.NodeId.SpookyCave
        ])
        self._assert_unavailable([haw.NodeId.StarryHill])

        self._collect(misc.TornPages)
        self._assert_available([
            haw.NodeId.PigletsHowse,
            haw.NodeId.RabbitsHowse,
            haw.NodeId.KangasHowse,
            haw.NodeId.SpookyCave,
            haw.NodeId.StarryHill
        ])

        # Sanity check, just in case synthesizing pages or something
        self._collect(misc.TornPages)
        self._assert_available([
            haw.NodeId.PigletsHowse,
            haw.NodeId.RabbitsHowse,
            haw.NodeId.KangasHowse,
            haw.NodeId.SpookyCave,
            haw.NodeId.StarryHill
        ])

    def _collect(self, item: InventoryItem):
        self.inventory.append(item.id)

    def _uncollect(self, item: InventoryItem):
        self.inventory.remove(item.id)

    def _assert_available(self, node_ids: list[str]):
        for node_id in node_ids:
            msg = f"Expected {node_id} to be available"
            for location in self.locations.locations_for_node(node_id):
                self.assertTrue(self.validator.is_location_available(self.inventory, location), msg=msg)

    def _assert_unavailable(self, node_ids: list[str]):
        for node_id in node_ids:
            msg = f"Expected {node_id} to be unavailable"
            for location in self.locations.locations_for_node(node_id):
                self.assertFalse(self.validator.is_location_available(self.inventory, location), msg=msg)


if __name__ == '__main__':
    unittest.main()

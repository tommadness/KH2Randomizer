import unittest

from Class import settingkey
from Class.exceptions import SettingsException
from Class.seedSettings import SeedSettings
from List.configDict import locationType, StartingVisitMode
from List.inventory import proof
from Module.newRandomize import RandomizerSettings, Randomizer
from seedtests import seedtest


class Tests(unittest.TestCase):

    def test_start_all_unlocks(self):
        """
        Verifies that you can start with all unlocks and chain logic still works.
        Should be fine since it has forms and pages to work with.
        """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.CHAIN_LOGIC, True)
        seed_settings.set(settingkey.STARTING_VISIT_MODE, StartingVisitMode.ALL.name)

        for randomizer in seedtest.test_seeds(seed_settings):
            proof_assignment = randomizer.assignment_for_item(proof.ProofOfNonexistence)
            self.assertIsNotNone(proof_assignment)

    def test_nothing_to_unlock(self):
        """
        Verifies a potential worst-case scenario for chain logic.
        Starts you with as many locking items as possible and sets forms and Hundred Acre Wood to junk.
        Chain logic just places Proof of Nonexistence randomly in this case. While not a particularly interesting seed
        from a chain logic perspective, not likely a player is going to do this combination.
        """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.CHAIN_LOGIC, True)
        seed_settings.set(settingkey.STARTING_VISIT_MODE, StartingVisitMode.ALL.name)
        seed_settings.set(settingkey.STARTING_INVENTORY, [proof.ProofOfPeace.id])
        randomized_worlds = [
            locationType.STT.name,
            locationType.HB.name,
            locationType.OC.name,
            locationType.LoD.name,
            locationType.PL.name,
            locationType.HT.name,
            locationType.SP.name,
            locationType.TT.name,
            locationType.BC.name,
            locationType.Agrabah.name,
            locationType.DC.name,
            locationType.PR.name,
            locationType.TWTNW.name
        ]
        vanilla_worlds = []
        seed_settings.set(settingkey.WORLDS_WITH_REWARDS, [randomized_worlds, vanilla_worlds])

        for randomizer in seedtest.test_seeds(seed_settings):
            proof_assignment = randomizer.assignment_for_item(proof.ProofOfNonexistence)
            self.assertIsNotNone(proof_assignment)

    def test_start_nonexistence(self):
        """
        Chain logic works by putting Proof of Nonexistence at the end of the chain.
        If Proof of Nonexistence is in the starting inventory, that won't be possible.
        """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.CHAIN_LOGIC, True)
        seed_settings.set(settingkey.STARTING_INVENTORY, [proof.ProofOfNonexistence.id])

        for seed_name in seedtest.test_seed_names():
            with self.assertRaises(SettingsException):
                settings = RandomizerSettings(seed_name, True, "version", seed_settings, "")
                Randomizer(settings)


if __name__ == '__main__':
    unittest.main()

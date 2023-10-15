import unittest

from Class import settingkey
from Class.exceptions import SettingsException
from Class.seedSettings import SeedSettings
from List.configDict import locationType
from List.inventory import proof
from List.location import hundredacrewood as haw
from Module.newRandomize import RandomizerSettings, Randomizer
from seedtests import seedtest


class Tests(unittest.TestCase):

    def test_start_with_nonexistence(self):
        """
        Verifies that an exception is raised if Yeet the Bear is on and Proof of Nonexistence is in starting inventory.
        """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.YEET_THE_BEAR, True)
        seed_settings.set(settingkey.STARTING_INVENTORY, [proof.ProofOfNonexistence.id])

        for seed_name in seedtest.test_seed_names():
            with self.assertRaises(SettingsException):
                settings = RandomizerSettings(seed_name, True, "version", seed_settings, "")
                Randomizer(settings)

    def test_hundred_acre_junked_basic(self):
        """
        Verifies that an exception is raised if Yeet the Bear is on and Hundred Acre Wood is set to junk.
        """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.YEET_THE_BEAR, True)

        randomized_worlds = [
            locationType.FormLevel.name,
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

        for seed_name in seedtest.test_seed_names():
            with self.assertRaises(SettingsException):
                settings = RandomizerSettings(seed_name, True, "version", seed_settings, "")
                Randomizer(settings)

    def test_hundred_acre_vanilla(self):
        """
        Verifies that an exception is raised if Yeet the Bear is on and Hundred Acre Wood is set to vanilla.
        """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.YEET_THE_BEAR, True)

        randomized_worlds = [
            locationType.FormLevel.name,
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
        vanilla_worlds = [locationType.HUNDREDAW.name]
        seed_settings.set(settingkey.WORLDS_WITH_REWARDS, [randomized_worlds, vanilla_worlds])

        for seed_name in seedtest.test_seed_names():
            with self.assertRaises(SettingsException):
                settings = RandomizerSettings(seed_name, True, "version", seed_settings, "")
                Randomizer(settings)

    def test_basic(self):
        """
        Verifies the Proof of Nonexistence was placed in an appropriate location for Yeet the Bear.
        """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.YEET_THE_BEAR, True)

        for randomizer in seedtest.test_seeds(seed_settings):
            self._validate_yeet(randomizer)

    def test_chain(self):
        """
        Verifies the Proof of Nonexistence was placed in an appropriate location for Yeet the Bear with chain logic.
        """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.YEET_THE_BEAR, True)
        seed_settings.set(settingkey.CHAIN_LOGIC, True)

        for randomizer in seedtest.test_seeds(seed_settings):
            self._validate_yeet(randomizer)

    def _validate_yeet(self, randomizer: Randomizer):
        proof_location = randomizer.assignment_for_item(proof.ProofOfNonexistence).location
        self.assertIn(proof_location.name(), haw.yeet_the_bear_location_names())


if __name__ == '__main__':
    unittest.main()

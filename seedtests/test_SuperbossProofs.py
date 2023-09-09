import unittest

from Class import settingkey
from Class.exceptions import SettingsException
from Class.seedSettings import SeedSettings
from List.configDict import locationDepth, locationType
from List.inventory import proof
from Module.newRandomize import RandomizerSettings, Randomizer
from seedtests import seedtest


class Tests(unittest.TestCase):

    def test_absent_silhouette_only_proofs(self):
        """
        Verifies proof placement when only Absent Silhouettes are on.
        """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.PROOF_DEPTH, locationDepth.Superbosses)
        seed_settings.set(settingkey.SUPERBOSSES_WITH_REWARDS, [
            locationType.AS.name,
        ])

        for randomizer in seedtest.test_seeds(seed_settings):
            for item in [proof.ProofOfConnection, proof.ProofOfNonexistence, proof.ProofOfPeace]:
                location = randomizer.assignment_for_item(item).location
                self.assertTrue(locationType.AS in location.LocationTypes)

    def test_data_only_proofs(self):
        """
        Verifies proof placement when only Data Organization is on.
        """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.PROOF_DEPTH, locationDepth.Superbosses)
        seed_settings.set(settingkey.SUPERBOSSES_WITH_REWARDS, [
            locationType.DataOrg.name,
        ])

        for randomizer in seedtest.test_seeds(seed_settings):
            for item in [proof.ProofOfConnection, proof.ProofOfNonexistence, proof.ProofOfPeace]:
                location = randomizer.assignment_for_item(item).location
                self.assertTrue(locationType.DataOrg in location.LocationTypes)

    def test_absent_silhouette_data_proofs(self):
        """
        Verifies that when proof depth is set to Superbosses, and both Absent Silhouettes and Data Organization are on,
        proofs are not on the Absent Silhouettes. This is done by design to prevent, for example, a proof being on
        Absent Silhouette Marluxia as well as one on Data Marluxia.
        """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.PROOF_DEPTH, locationDepth.Superbosses)
        seed_settings.set(settingkey.REPORT_DEPTH, locationDepth.NonSuperboss)
        seed_settings.set(settingkey.SUPERBOSSES_WITH_REWARDS, [
            locationType.AS.name,
            locationType.DataOrg.name,
            locationType.Sephi.name,
            locationType.LW.name
        ])

        for randomizer in seedtest.test_seeds(seed_settings):
            for item in [proof.ProofOfConnection, proof.ProofOfNonexistence, proof.ProofOfPeace]:
                location = randomizer.assignment_for_item(item).location
                self.assertFalse(locationType.AS in location.LocationTypes)

    def test_absent_silhouette_lingering_will_proofs(self):
        """
        Verifies that when proof depth is set to Superbosses, and both Absent Silhouettes and Lingering Will are on,
        proofs are on one of those.
        """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.PROOF_DEPTH, locationDepth.Superbosses)
        seed_settings.set(settingkey.REPORT_DEPTH, locationDepth.NonSuperboss)
        seed_settings.set(settingkey.SUPERBOSSES_WITH_REWARDS, [
            locationType.AS.name,
            locationType.LW.name
        ])

        for randomizer in seedtest.test_seeds(seed_settings):
            for item in [proof.ProofOfConnection, proof.ProofOfNonexistence, proof.ProofOfPeace]:
                location = randomizer.assignment_for_item(item).location
                types = location.LocationTypes
                self.assertTrue(locationType.AS in types or locationType.LW in types)

    def test_absent_silhouette_sephiroth_proofs(self):
        """
        Verifies that when proof depth is set to Superbosses, and both Absent Silhouettes and Sephiroth are on,
        proofs are on one of those.
        """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.PROOF_DEPTH, locationDepth.Superbosses)
        seed_settings.set(settingkey.REPORT_DEPTH, locationDepth.NonSuperboss)
        seed_settings.set(settingkey.SUPERBOSSES_WITH_REWARDS, [
            locationType.AS.name,
            locationType.Sephi.name
        ])

        for randomizer in seedtest.test_seeds(seed_settings):
            for item in [proof.ProofOfConnection, proof.ProofOfNonexistence, proof.ProofOfPeace]:
                location = randomizer.assignment_for_item(item).location
                types = location.LocationTypes
                self.assertTrue(locationType.AS in types or locationType.Sephi in types)

    def test_lingering_will_sephiroth_proofs(self):
        """
        Verifies that an exception is raised when proof depth is set to Superbosses and only Lingering Will and
        Sephiroth are on. In this case we don't have enough locations to place all 3 proofs since we only allow 1 per
        superboss.
        """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.PROOF_DEPTH, locationDepth.Superbosses)
        seed_settings.set(settingkey.REPORT_DEPTH, locationDepth.NonSuperboss)
        seed_settings.set(settingkey.SUPERBOSSES_WITH_REWARDS, [
            locationType.LW.name,
            locationType.Sephi.name
        ])

        for seed_name in seedtest.test_seed_names():
            with self.assertRaises(SettingsException):
                settings = RandomizerSettings(seed_name, True, "version", seed_settings, "")
                Randomizer(settings)


if __name__ == '__main__':
    unittest.main()

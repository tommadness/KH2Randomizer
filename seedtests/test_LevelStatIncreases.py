import unittest

from Class import settingkey
from Class.seedSettings import SeedSettings
from List.configDict import locationType, SoraLevelOption
from Module.newRandomize import Randomizer
from seedtests import seedtest


class Tests(unittest.TestCase):

    def test_level_stat_increases(self):
        """ Verifies at least one stat increase per level. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.SORA_LEVELS, SoraLevelOption.LEVEL_50)

        for randomizer in seedtest.test_seeds(seed_settings):
            self._validate_stats(randomizer, should_increase=True)

    # TODO: Verify for sure if this is how we want level 1 to behave when levels is set to junk.
    #       As it stands, your stats still increase from leveling in this mode.
    def test_level_one_junk_stat_increases(self):
        """ Verifies at least one stat increase per level when level 1 mode with levels set to junk. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.SORA_LEVELS, SoraLevelOption.LEVEL_1)

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
            locationType.HUNDREDAW.name,
            locationType.DC.name,
            locationType.PR.name,
            locationType.TWTNW.name
        ]
        vanilla_worlds = []
        seed_settings.set(settingkey.WORLDS_WITH_REWARDS, [randomized_worlds, vanilla_worlds])

        for randomizer in seedtest.test_seeds(seed_settings):
            self._validate_stats(randomizer, should_increase=True)

    def test_level_one_vanilla_no_stat_increases(self):
        """ Verifies no stats increase when level 1 mode with levels set to vanilla. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.SORA_LEVELS, SoraLevelOption.LEVEL_1)

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
            locationType.HUNDREDAW.name,
            locationType.DC.name,
            locationType.PR.name,
            locationType.TWTNW.name
        ]
        vanilla_worlds = [locationType.Level]
        seed_settings.set(settingkey.WORLDS_WITH_REWARDS, [randomized_worlds, vanilla_worlds])

        for randomizer in seedtest.test_seeds(seed_settings):
            self._validate_stats(randomizer, should_increase=False)

    def _validate_stats(self, randomizer: Randomizer, should_increase: bool):
        level_stats = randomizer.level_stats
        self.assertEqual(99, len(level_stats))

        for index, stats in enumerate(level_stats):
            if index > 0:
                previous_stats = level_stats[index - 1]
                str_increased = stats.strength > previous_stats.strength
                mag_increased = stats.magic > previous_stats.magic
                def_increased = stats.defense > previous_stats.defense
                ap_increased = stats.ap > previous_stats.ap
                if should_increase:
                    self.assertTrue(str_increased or mag_increased or def_increased or ap_increased)
                else:
                    self.assertFalse(str_increased or mag_increased or def_increased or ap_increased)


if __name__ == '__main__':
    unittest.main()

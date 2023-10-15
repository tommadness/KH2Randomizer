import unittest

from Class import settingkey
from Class.seedSettings import SeedSettings
from List.location import simulatedtwilighttown as stt
from Module.newRandomize import Randomizer
from seedtests import seedtest


class Tests(unittest.TestCase):

    def test_basic(self):
        """ Verifies that the struggle items are the same for a basic seed. """
        seed_settings = SeedSettings()

        for randomizer in seedtest.test_seeds(seed_settings):
            self._validate_struggles(randomizer)

    def test_chain(self):
        """ Verifies that the struggle items are the same for a chain logic seed. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.CHAIN_LOGIC, True)

        for randomizer in seedtest.test_seeds(seed_settings):
            self._validate_struggles(randomizer)

    def _validate_struggles(self, randomizer: Randomizer):
        winner = randomizer.assignment_for_location(stt.CheckLocation.StruggleWinnerChampionBelt)
        loser = randomizer.assignment_for_location(stt.CheckLocation.StruggleLoserMedal)
        self.assertEqual(winner.item, loser.item)


if __name__ == '__main__':
    unittest.main()

import unittest

from Class.seedSettings import SeedSettings
from Module.newRandomize import RandomizerSettings, Randomizer


class Tests(unittest.TestCase):

    def test_randomizer_quantities(self):
        seed_settings = SeedSettings()
        settings = RandomizerSettings("test_name", True, "version", seed_settings, "")
        randomizer = Randomizer(settings)

        self.assertEqual(702, len(randomizer.assignments))
        self.assertEqual(31, len(randomizer.donald_assignments))
        self.assertEqual(32, len(randomizer.goofy_assignments))
        self.assertEqual(61, len(randomizer.weapon_stats))
        self.assertEqual(99, len(randomizer.level_stats))
        self.assertEqual(20, randomizer.level_stats[0].experience)
        self.assertEqual(1437789, randomizer.level_stats[-1].experience)
        self.assertLessEqual(2, randomizer.level_stats[-1].strength)
        self.assertLessEqual(6, randomizer.level_stats[-1].magic)
        self.assertLessEqual(2, randomizer.level_stats[-1].defense)
        self.assertLessEqual(0, randomizer.level_stats[-1].ap)

        num_str_increase = (randomizer.level_stats[-1].strength - 2) // 2
        num_mag_increase = (randomizer.level_stats[-1].magic - 6) // 2
        num_def_increase = (randomizer.level_stats[-1].defense - 2)
        num_ap_increase = (randomizer.level_stats[-1].ap) // 2
        self.assertEqual(173, num_str_increase + num_mag_increase + num_def_increase + num_ap_increase)
        self.assertEqual(42, len(randomizer.form_level_exp))


if __name__ == '__main__':
    unittest.main()

import unittest

from khbr.randomizer import Randomizer as BossEnemyRandomizer

from Class.seedSettings import SeedSettings, makeKHBRSettings
from seedtests import seedtest


class Tests(unittest.TestCase):

    def test_one_to_one_boss_rando(self):
        """ Verifies that randomization succeeds using One to One boss randomization. """
        seed_settings = SeedSettings()
        seed_settings.set("boss", "One to One")

        for seed_name in seedtest.test_seed_names(count=20):
            enemy_options = makeKHBRSettings(seed_name, seed_settings)
            del enemy_options["seed_name"]
            enemy_options["memory_expansion"] = True
            BossEnemyRandomizer().generate_seed("kh2", enemy_options, seed_name, randomization_only=True)

    def test_wild_boss_rando(self):
        """ Verifies that randomization succeeds using Wild boss randomization. """
        seed_settings = SeedSettings()
        seed_settings.set("boss", "Wild")

        for seed_name in seedtest.test_seed_names(count=20):
            enemy_options = makeKHBRSettings(seed_name, seed_settings)
            del enemy_options["seed_name"]
            enemy_options["memory_expansion"] = True
            BossEnemyRandomizer().generate_seed("kh2", enemy_options, seed_name, randomization_only=True)

    def test_one_to_one_enemy_rando(self):
        """ Verifies that randomization succeeds using One to One enemy randomization. """
        seed_settings = SeedSettings()
        seed_settings.set("enemy", "One to One")

        for seed_name in seedtest.test_seed_names(count=20):
            enemy_options = makeKHBRSettings(seed_name, seed_settings)
            enemy_options["memory_expansion"] = True
            del enemy_options["seed_name"]
            BossEnemyRandomizer().generate_seed("kh2", enemy_options, seed_name, randomization_only=True)

    def test_one_to_one_per_room_enemy_rando(self):
        """ Verifies that randomization succeeds using One to One enemy randomization. """
        seed_settings = SeedSettings()
        seed_settings.set("enemy", "One to One Per Room")

        for seed_name in seedtest.test_seed_names(count=20):
            enemy_options = makeKHBRSettings(seed_name, seed_settings)
            enemy_options["memory_expansion"] = True
            del enemy_options["seed_name"]
            BossEnemyRandomizer().generate_seed("kh2", enemy_options, seed_name, randomization_only=True)

    def test_wild_enemy_rando(self):
        """ Verifies that randomization succeeds using Wild enemy randomization. """
        seed_settings = SeedSettings()
        seed_settings.set("enemy", "Wild")

        for seed_name in seedtest.test_seed_names(count=20):
            enemy_options = makeKHBRSettings(seed_name, seed_settings)
            enemy_options["memory_expansion"] = True
            del enemy_options["seed_name"]
            BossEnemyRandomizer().generate_seed("kh2", enemy_options, seed_name, randomization_only=True)


if __name__ == '__main__':
    unittest.main()

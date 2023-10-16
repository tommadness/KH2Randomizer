import unittest

from Class.seedSettings import SeedSettings
from Module.newRandomize import RandomizerSettings


class Tests(unittest.TestCase):

    def test_ui_to_randomizer_keeps_seed_name(self):
        settings = RandomizerSettings("test_name", True, "version", SeedSettings(), "")
        self.assertEqual("test_name", settings.random_seed)


if __name__ == '__main__':
    unittest.main()

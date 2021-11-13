from Class.seedSettings import SeedSettings
from Module.newRandomize import RandomizerSettings
import unittest


class Tests(unittest.TestCase):
    def test_constructingRandomizer(self):
        settings = RandomizerSettings("test_name",True,"version",SeedSettings())
        self.assertEqual(settings.random_seed,"test_name")
        
if __name__ == '__main__':
    unittest.main()
from Class.seedSettings import SeedSettings
from Module.newRandomize import RandomizerSettings,Randomizer
import unittest


class Tests(unittest.TestCase):
    def test_constructingRandomizer(self):
        settings = RandomizerSettings("test_name",True,"version",SeedSettings())
        randomizer = Randomizer(settings)
        self.assertEqual(len(randomizer.assignedItems),668)
        self.assertEqual(len(randomizer.assignedDonaldItems),31)
        self.assertEqual(len(randomizer.assignedGoofyItems),32)
        self.assertEqual(len(randomizer.weaponStats),57)
        self.assertEqual(len(randomizer.levelStats),99)
        self.assertEqual(randomizer.levelStats[0].experience,27)
        self.assertEqual(randomizer.levelStats[-1].experience,1917052)
        self.assertGreater(randomizer.levelStats[-1].strength,2)
        self.assertGreater(randomizer.levelStats[-1].magic,6)
        self.assertGreater(randomizer.levelStats[-1].defense,2)
        self.assertGreater(randomizer.levelStats[-1].ap,0)

        num_str_increase = (randomizer.levelStats[-1].strength-2)//2
        num_mag_increase = (randomizer.levelStats[-1].magic-6)//2
        num_def_increase = (randomizer.levelStats[-1].defense-2)
        num_ap_increase = (randomizer.levelStats[-1].ap)//2
        self.assertEqual(num_str_increase+num_mag_increase+num_def_increase+num_ap_increase,173)
        self.assertEqual(len(randomizer.formLevelExp),42)
        
if __name__ == '__main__':
    unittest.main()
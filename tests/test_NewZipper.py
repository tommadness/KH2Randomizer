
from Module.hints import Hints
from Module.newRandomize import RandomizerSettings,Randomizer
from Module.zipper import SeedZip
import unittest
import zipfile,os


class Tests(unittest.TestCase):
    def test_constructingSeedZip(self):
        settings = RandomizerSettings()
        randomizer = Randomizer(settings)
        hints = Hints.generateHints(randomizer.assignedItems,settings.hintsType,settings.random_seed,settings.disabledLocations)
        zipper = SeedZip(settings,randomizer,hints)
        zip = zipper.outputZip
        development_mode_path = os.environ.get("DEVELOPMENT_MODE_PATH")
        if os.path.exists(development_mode_path):
            # Ensure a clean environment
            import shutil
            shutil.rmtree(development_mode_path)
        zipfile.ZipFile(zip).extractall(development_mode_path)
        
if __name__ == '__main__':
    unittest.main()
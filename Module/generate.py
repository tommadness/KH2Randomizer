
from Module.hints import Hints
from Module.newRandomize import Randomizer
from Module.zipper import SeedZip

def generateSeed(settings,data):
    randomizer = Randomizer(settings)
    hints = Hints.generateHints(randomizer.assignedItems,settings.hintsType,settings.random_seed,settings.disabledLocations)
    zipper = SeedZip(settings,randomizer,hints,data)
    return zipper.outputZip

from Module.hints import Hints
from Module.newRandomize import RandomizerSettings,Randomizer
from Module.zipper import generateZip

def generateSeed():
    settings = RandomizerSettings()
    randomizer = Randomizer(settings)
    hints = Hints.generateHints(randomizer.assignedItems,settings.hintsType,settings.random_seed,settings.disabledLocations)
    # zip = generateZip(settings,randomizer,hints)
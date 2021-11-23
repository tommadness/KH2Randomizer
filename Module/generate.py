
from Class.exceptions import RandomizerExceptions
from Module.RandomizerSettings import RandomizerSettings
from Module.hints import Hints
from Module.newRandomize import Randomizer
from Module.seedEvaluation import SeedValidator
from Module.zipper import SeedZip
import string,random

def generateSeed(settings: RandomizerSettings,data):
    seedValidation = SeedValidator(settings)
    last_error = None
    for attempt in range(50):
        try:
            randomizer = Randomizer(settings)
            seedValidation.validateSeed(settings,randomizer)
            hints = Hints.generateHints(randomizer.assignedItems,settings.hintsType,settings.random_seed,settings.disabledLocations)
            zipper = SeedZip(settings,randomizer,hints,data)
            return zipper.outputZip
        except RandomizerExceptions as e:
            characters = string.ascii_letters + string.digits
            settings.random_seed = (''.join(random.choice(characters) for i in range(30)))
            last_error = e
            continue
    raise last_error

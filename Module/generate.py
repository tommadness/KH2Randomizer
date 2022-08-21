
import copy
from typing import List
from Class.exceptions import RandomizerExceptions
from Module.RandomizerSettings import RandomizerSettings
from Module.hints import Hints
from Module.multiworld import MultiWorld, MultiWorldConfig
from Module.newRandomize import Randomizer
from Module.seedEvaluation import LocationInformedSeedValidator
from Module.zipper import SeedZip
import string,random

def generateSeed(settings: RandomizerSettings,data):

    newSeedValidation = LocationInformedSeedValidator()
    last_error = None
    for attempt in range(50):
        try:
            randomizer = Randomizer(settings)
            newSeedValidation.validateSeed(settings,randomizer)
            hints = Hints.generateHints(randomizer.assignedItems,settings)
            zipper = SeedZip(settings,randomizer,hints,data)
            return zipper.outputZip, zipper.spoiler_log, zipper.enemy_log
        except RandomizerExceptions as e:
            characters = string.ascii_letters + string.digits
            settings.random_seed = (''.join(random.choice(characters) for i in range(30)))
            settings.create_full_seed_string()
            last_error = e
            continue
    raise last_error


def generateMultiWorldSeed(settingsSet: List[RandomizerSettings], data):
    newSeedValidation = LocationInformedSeedValidator()
    randomizers = []
    last_error = None

    for player_settings in settingsSet:
        for attempt in range(50):
            try:
                last_error = None
                randomizer = Randomizer(player_settings)
                newSeedValidation.validateSeed(player_settings,randomizer)
                randomizers.append(randomizer)
                break
            except RandomizerExceptions as e:
                characters = string.ascii_letters + string.digits
                player_settings.random_seed = (''.join(random.choice(characters) for i in range(30)))
                player_settings.create_full_seed_string()
                last_error = e
                continue
        if last_error is not None:
            raise last_error

    # each individual randomization is done and valid, now we can mix the item pools

    m = MultiWorld(randomizers,MultiWorldConfig(settingsSet[0]))


    return 1,2
        


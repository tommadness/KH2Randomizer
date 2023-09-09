from datetime import datetime
from typing import Iterable

from Class.seedSettings import SeedSettings
from Module.RandomizerSettings import RandomizerSettings
from Module.newRandomize import Randomizer

SEED_COUNT = 500


def test_seed_names(count: int = SEED_COUNT) -> Iterable[str]:
    """ Generates unique seed names that can be used for testing. The amount is based on the SEED_COUNT. """
    initial_name = f"{datetime.now()}"
    for i in range(count):
        yield f"{initial_name}-{i}"


def test_seeds(seed_settings: SeedSettings, count: int = SEED_COUNT) -> Iterable[Randomizer]:
    """ Generates unique seeds that can be used for testing. The amount is based on the SEED_COUNT. """
    for name in test_seed_names(count):
        settings = RandomizerSettings(name, True, "version", seed_settings, "")
        yield Randomizer(settings)

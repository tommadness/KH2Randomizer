import random
import string
from bisect import bisect_left
from itertools import accumulate
from typing import Optional

# An instance of a Random that deliberately _isn't_ tied to a specific seed.
unseeded_rng = random.Random()


def random_seed_name(rng: Optional[random.Random] = None) -> str:
    """
    Returns a randomly generated seed name.

    If a specific generator instance is passed, uses that; otherwise, uses the shared generator instance.
    """
    possible_characters = string.ascii_letters + string.digits
    if rng is None:
        chosen_characters = random.choices(possible_characters, k=30)
    else:
        chosen_characters = rng.choices(possible_characters, k=30)
    return "".join(chosen_characters)


def weighted_sample_without_replacement(population, weights, k):
    wts = list(weights)
    sampl = []
    rnums = [random.random() for _ in range(k)]
    for r in rnums:
        acm_wts = list(accumulate(wts))
        total = acm_wts[-1]
        i = bisect_left(acm_wts, total * r)
        p = population[i]
        wts[i] = 0
        sampl.append(p)
    return sampl

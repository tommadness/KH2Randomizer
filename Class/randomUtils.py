from bisect import bisect_left
from itertools import accumulate
from random import random, Random

# An instance of a Random that deliberately _isn't_ tied to a specific seed.
unseeded_rng = Random()


def weighted_sample_without_replacement(population, weights, k):
    wts = list(weights)
    sampl = []
    rnums = [random() for _ in range(k)]
    for r in rnums:
        acm_wts = list(accumulate(wts))
        total = acm_wts[-1]
        i = bisect_left(acm_wts, total * r)
        p = population[i]
        wts[i] = 0
        sampl.append(p)
    return sampl

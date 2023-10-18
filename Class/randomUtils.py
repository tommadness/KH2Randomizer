from random import random
from bisect import bisect_left
from itertools import accumulate


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

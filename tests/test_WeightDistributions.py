import unittest

from List.configDict import itemRarity, itemDifficulty
from Module.weighting import WeightDistributions


class Tests(unittest.TestCase):

    # TODO: Not 100% sure if we want to tie these tests to the exact values, but wanted to at least get some tests
    #       on the books for this.

    def test_super_easy(self):
        distributions = WeightDistributions(max_depth=17)
        weighting = distributions.get_rarity_weighting(itemDifficulty.SUPEREASY)
        self.assertEqual([2, 2, 2, 2, 2, 3, 3, 4, 4, 5, 6, 7, 9, 11, 16, 23, 41, 108], weighting[itemRarity.COMMON])
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 4, 7, 12, 32], weighting[itemRarity.UNCOMMON])
        self.assertEqual([32, 12, 7, 4, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], weighting[itemRarity.RARE])
        self.assertEqual([108, 41, 23, 16, 11, 9, 7, 6, 5, 4, 4, 3, 3, 2, 2, 2, 2, 2], weighting[itemRarity.MYTHIC])

    def test_easy(self):
        distributions = WeightDistributions(max_depth=17)
        weighting = distributions.get_rarity_weighting(itemDifficulty.EASY)
        self.assertEqual([3, 3, 4, 4, 4, 4, 5, 5, 6, 6, 7, 8, 9, 11, 13, 17, 24, 45], weighting[itemRarity.COMMON])
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 7, 13], weighting[itemRarity.UNCOMMON])
        self.assertEqual([13, 7, 5, 4, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1], weighting[itemRarity.RARE])
        self.assertEqual([45, 24, 17, 13, 11, 9, 8, 7, 6, 6, 5, 5, 4, 4, 4, 4, 3, 3], weighting[itemRarity.MYTHIC])

    def test_slightly_easy(self):
        distributions = WeightDistributions(max_depth=17)
        weighting = distributions.get_rarity_weighting(itemDifficulty.SLIGHTLY_EASY)
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], weighting[itemRarity.COMMON])
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], weighting[itemRarity.UNCOMMON])
        self.assertEqual([2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1], weighting[itemRarity.RARE])
        self.assertEqual([2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1], weighting[itemRarity.MYTHIC])

    def test_normal(self):
        distributions = WeightDistributions(max_depth=17)
        weighting = distributions.get_rarity_weighting(itemDifficulty.NORMAL)
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], weighting[itemRarity.COMMON])
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], weighting[itemRarity.UNCOMMON])
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], weighting[itemRarity.RARE])
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], weighting[itemRarity.MYTHIC])

    def test_slightly_hard(self):
        distributions = WeightDistributions(max_depth=17)
        weighting = distributions.get_rarity_weighting(itemDifficulty.SLIGHTLY_HARD)
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], weighting[itemRarity.COMMON])
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], weighting[itemRarity.UNCOMMON])
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2], weighting[itemRarity.RARE])
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2], weighting[itemRarity.MYTHIC])

    def test_hard(self):
        distributions = WeightDistributions(max_depth=17)
        weighting = distributions.get_rarity_weighting(itemDifficulty.HARD)
        self.assertEqual([45, 24, 17, 13, 11, 9, 8, 7, 6, 6, 5, 5, 4, 4, 4, 4, 3, 3], weighting[itemRarity.COMMON])
        self.assertEqual([13, 7, 5, 4, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1], weighting[itemRarity.UNCOMMON])
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 7, 13], weighting[itemRarity.RARE])
        self.assertEqual([3, 3, 4, 4, 4, 4, 5, 5, 6, 6, 7, 8, 9, 11, 13, 17, 24, 45], weighting[itemRarity.MYTHIC])

    def test_very_hard(self):
        distributions = WeightDistributions(max_depth=17)
        weighting = distributions.get_rarity_weighting(itemDifficulty.VERYHARD)
        self.assertEqual([108, 41, 23, 16, 11, 9, 7, 6, 5, 4, 4, 3, 3, 2, 2, 2, 2, 2], weighting[itemRarity.COMMON])
        self.assertEqual([32, 12, 7, 4, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], weighting[itemRarity.UNCOMMON])
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 4, 7, 12, 32], weighting[itemRarity.RARE])
        self.assertEqual([2, 2, 2, 2, 2, 3, 3, 4, 4, 5, 6, 7, 9, 11, 16, 23, 41, 108], weighting[itemRarity.MYTHIC])

    def test_insane(self):
        distributions = WeightDistributions(max_depth=17)
        weighting = distributions.get_rarity_weighting(itemDifficulty.INSANE)
        self.assertEqual([258, 70, 32, 19, 12, 8, 6, 5, 4, 3, 2, 2, 2, 1, 1, 1, 1, 1], weighting[itemRarity.COMMON])
        self.assertEqual([77, 21, 9, 5, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], weighting[itemRarity.UNCOMMON])
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 5, 9, 21, 77], weighting[itemRarity.RARE])
        self.assertEqual([1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 5, 6, 8, 12, 19, 32, 70, 258], weighting[itemRarity.MYTHIC])

    def test_nightmare(self):
        distributions = WeightDistributions(max_depth=17)
        weighting = distributions.get_rarity_weighting(itemDifficulty.NIGHTMARE)
        self.assertEqual([615, 118, 45, 22, 13, 8, 6, 4, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1], weighting[itemRarity.COMMON])
        self.assertEqual([184, 35, 13, 6, 4, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], weighting[itemRarity.UNCOMMON])
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 4, 6, 13, 35, 184], weighting[itemRarity.RARE])
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 4, 6, 8, 13, 22, 45, 118, 615], weighting[itemRarity.MYTHIC])


if __name__ == '__main__':
    unittest.main()

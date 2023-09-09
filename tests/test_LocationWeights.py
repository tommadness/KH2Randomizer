import unittest

from Class import settingkey
from Class.seedSettings import SeedSettings
from List.NewLocationList import Locations
from List.configDict import itemDifficulty, itemRarity
from List.location import hundredacrewood as haw, soralevel
from Module.RandomizerSettings import RandomizerSettings
from Module.weighting import LocationWeights


class Tests(unittest.TestCase):

    def test_normal(self):
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.ITEM_PLACEMENT_DIFFICULTY, itemDifficulty.NORMAL)
        seed_settings.set(settingkey.AS_DATA_SPLIT, True)
        seed_settings.set(settingkey.SOFTLOCK_CHECKING, 'default')

        reverse_seed_settings = SeedSettings()
        reverse_seed_settings.set(settingkey.ITEM_PLACEMENT_DIFFICULTY, itemDifficulty.NORMAL)
        reverse_seed_settings.set(settingkey.AS_DATA_SPLIT, True)
        reverse_seed_settings.set(settingkey.SOFTLOCK_CHECKING, 'reverse')

        both_seed_settings = SeedSettings()
        both_seed_settings.set(settingkey.ITEM_PLACEMENT_DIFFICULTY, itemDifficulty.NORMAL)
        both_seed_settings.set(settingkey.AS_DATA_SPLIT, True)
        both_seed_settings.set(settingkey.SOFTLOCK_CHECKING, 'both')

        settings = RandomizerSettings("test_name", True, "version", seed_settings, "")
        regular_locations = Locations(settings, secondary_graph=False)
        regular_weights = LocationWeights(
            settings,
            regular_locations,
            Locations(settings, secondary_graph=True)
        )

        reverse_settings = RandomizerSettings("test_name", True, "version", reverse_seed_settings, "")
        reverse_weights = LocationWeights(
            reverse_settings,
            Locations(reverse_settings, secondary_graph=False),
            Locations(reverse_settings, secondary_graph=True)
        )

        both_settings = RandomizerSettings("test_name", True, "version", both_seed_settings, "")
        both_weights = LocationWeights(
            both_settings,
            Locations(both_settings, secondary_graph=False),
            Locations(both_settings, secondary_graph=True)
        )

        # Earliest regular depth location
        haw_map = regular_locations.locations_by_name[haw.CheckLocation.PoohsHowseHundredAcreWoodMap]
        self.assertEqual(1, regular_weights.get_weight(itemRarity.MYTHIC, haw_map))
        self.assertEqual(1, reverse_weights.get_weight(itemRarity.MYTHIC, haw_map))
        self.assertEqual(1, both_weights.get_weight(itemRarity.MYTHIC, haw_map))

        # Medium depth location
        kangas_magic_boost = regular_locations.locations_by_name[haw.CheckLocation.KangasHowseMagicBoost]
        self.assertEqual(1, regular_weights.get_weight(itemRarity.MYTHIC, kangas_magic_boost))
        self.assertEqual(1, reverse_weights.get_weight(itemRarity.MYTHIC, kangas_magic_boost))
        self.assertEqual(1, both_weights.get_weight(itemRarity.MYTHIC, kangas_magic_boost))

        # Latest regular depth location
        starry_hill_cure = regular_locations.locations_by_name[haw.CheckLocation.StarryHillCureElement]
        self.assertEqual(1, regular_weights.get_weight(itemRarity.MYTHIC, starry_hill_cure))
        self.assertEqual(1, reverse_weights.get_weight(itemRarity.MYTHIC, starry_hill_cure))
        self.assertEqual(1, both_weights.get_weight(itemRarity.MYTHIC, starry_hill_cure))

        # Sample a few levels
        level_1 = soralevel.level_reward(1, "Level 1", None)
        self.assertEqual(1, regular_weights.get_weight(itemRarity.MYTHIC, level_1))
        self.assertEqual(1, reverse_weights.get_weight(itemRarity.MYTHIC, level_1))
        self.assertEqual(1, both_weights.get_weight(itemRarity.MYTHIC, level_1))

        level_25 = soralevel.level_reward(25, "Level 25", None)
        self.assertEqual(1, regular_weights.get_weight(itemRarity.MYTHIC, level_25))
        self.assertEqual(1, reverse_weights.get_weight(itemRarity.MYTHIC, level_25))
        self.assertEqual(1, both_weights.get_weight(itemRarity.MYTHIC, level_25))

        level_50 = soralevel.level_reward(50, "Level 50", None)
        self.assertEqual(1, regular_weights.get_weight(itemRarity.MYTHIC, level_50))
        self.assertEqual(1, reverse_weights.get_weight(itemRarity.MYTHIC, level_50))
        self.assertEqual(1, both_weights.get_weight(itemRarity.MYTHIC, level_50))

    def test_slightly_easy(self):
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.ITEM_PLACEMENT_DIFFICULTY, itemDifficulty.SLIGHTLY_EASY)
        seed_settings.set(settingkey.AS_DATA_SPLIT, True)
        seed_settings.set(settingkey.SOFTLOCK_CHECKING, 'default')

        reverse_seed_settings = SeedSettings()
        reverse_seed_settings.set(settingkey.ITEM_PLACEMENT_DIFFICULTY, itemDifficulty.SLIGHTLY_EASY)
        reverse_seed_settings.set(settingkey.AS_DATA_SPLIT, True)
        reverse_seed_settings.set(settingkey.SOFTLOCK_CHECKING, 'reverse')

        both_seed_settings = SeedSettings()
        both_seed_settings.set(settingkey.ITEM_PLACEMENT_DIFFICULTY, itemDifficulty.SLIGHTLY_EASY)
        both_seed_settings.set(settingkey.AS_DATA_SPLIT, True)
        both_seed_settings.set(settingkey.SOFTLOCK_CHECKING, 'both')

        settings = RandomizerSettings("test_name", True, "version", seed_settings, "")
        regular_locations = Locations(settings, secondary_graph=False)
        regular_weights = LocationWeights(
            settings,
            regular_locations,
            Locations(settings, secondary_graph=True)
        )

        reverse_settings = RandomizerSettings("test_name", True, "version", reverse_seed_settings, "")
        reverse_weights = LocationWeights(
            reverse_settings,
            Locations(reverse_settings, secondary_graph=False),
            Locations(reverse_settings, secondary_graph=True)
        )

        both_settings = RandomizerSettings("test_name", True, "version", both_seed_settings, "")
        both_weights = LocationWeights(
            both_settings,
            Locations(both_settings, secondary_graph=False),
            Locations(both_settings, secondary_graph=True)
        )

        # Earliest regular depth location
        haw_map = regular_locations.locations_by_name[haw.CheckLocation.PoohsHowseHundredAcreWoodMap]
        self.assertEqual(2, regular_weights.get_weight(itemRarity.MYTHIC, haw_map))
        self.assertEqual(1, reverse_weights.get_weight(itemRarity.MYTHIC, haw_map))
        self.assertEqual(1, both_weights.get_weight(itemRarity.MYTHIC, haw_map))

        # Medium depth location
        kangas_magic_boost = regular_locations.locations_by_name[haw.CheckLocation.KangasHowseMagicBoost]
        self.assertEqual(1, regular_weights.get_weight(itemRarity.MYTHIC, kangas_magic_boost))
        self.assertEqual(2, reverse_weights.get_weight(itemRarity.MYTHIC, kangas_magic_boost))
        self.assertEqual(1, both_weights.get_weight(itemRarity.MYTHIC, kangas_magic_boost))

        # Latest regular depth location
        starry_hill_cure = regular_locations.locations_by_name[haw.CheckLocation.StarryHillCureElement]
        self.assertEqual(1, regular_weights.get_weight(itemRarity.MYTHIC, starry_hill_cure))
        self.assertEqual(2, reverse_weights.get_weight(itemRarity.MYTHIC, starry_hill_cure))
        self.assertEqual(1, both_weights.get_weight(itemRarity.MYTHIC, starry_hill_cure))

        # Sample a few levels
        level_1 = soralevel.level_reward(1, "Level 1", None)
        self.assertEqual(2, regular_weights.get_weight(itemRarity.MYTHIC, level_1))
        self.assertEqual(2, reverse_weights.get_weight(itemRarity.MYTHIC, level_1))
        self.assertEqual(2, both_weights.get_weight(itemRarity.MYTHIC, level_1))

        level_25 = soralevel.level_reward(25, "Level 25", None)
        self.assertEqual(2, regular_weights.get_weight(itemRarity.MYTHIC, level_25))
        self.assertEqual(2, reverse_weights.get_weight(itemRarity.MYTHIC, level_25))
        self.assertEqual(2, both_weights.get_weight(itemRarity.MYTHIC, level_25))

        level_50 = soralevel.level_reward(50, "Level 50", None)
        self.assertEqual(1, regular_weights.get_weight(itemRarity.MYTHIC, level_50))
        self.assertEqual(1, reverse_weights.get_weight(itemRarity.MYTHIC, level_50))
        self.assertEqual(1, both_weights.get_weight(itemRarity.MYTHIC, level_50))

    def test_nightmare(self):
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.ITEM_PLACEMENT_DIFFICULTY, itemDifficulty.NIGHTMARE)
        seed_settings.set(settingkey.AS_DATA_SPLIT, True)
        seed_settings.set(settingkey.SOFTLOCK_CHECKING, 'default')

        reverse_seed_settings = SeedSettings()
        reverse_seed_settings.set(settingkey.ITEM_PLACEMENT_DIFFICULTY, itemDifficulty.NIGHTMARE)
        reverse_seed_settings.set(settingkey.AS_DATA_SPLIT, True)
        reverse_seed_settings.set(settingkey.SOFTLOCK_CHECKING, 'reverse')

        both_seed_settings = SeedSettings()
        both_seed_settings.set(settingkey.ITEM_PLACEMENT_DIFFICULTY, itemDifficulty.NIGHTMARE)
        both_seed_settings.set(settingkey.AS_DATA_SPLIT, True)
        both_seed_settings.set(settingkey.SOFTLOCK_CHECKING, 'both')

        settings = RandomizerSettings("test_name", True, "version", seed_settings, "")
        regular_locations = Locations(settings, secondary_graph=False)
        regular_weights = LocationWeights(
            settings,
            regular_locations,
            Locations(settings, secondary_graph=True)
        )

        reverse_settings = RandomizerSettings("test_name", True, "version", reverse_seed_settings, "")
        reverse_weights = LocationWeights(
            reverse_settings,
            Locations(reverse_settings, secondary_graph=False),
            Locations(reverse_settings, secondary_graph=True)
        )

        both_settings = RandomizerSettings("test_name", True, "version", both_seed_settings, "")
        both_weights = LocationWeights(
            both_settings,
            Locations(both_settings, secondary_graph=False),
            Locations(both_settings, secondary_graph=True)
        )

        # Determine the expected weights from the weight distribution, so we're not tying these to specific details
        weight_distribution = regular_weights.weights[itemRarity.MYTHIC]
        min_weight = weight_distribution[0]
        max_weight = weight_distribution[-1]

        # Earliest regular depth location
        haw_map = regular_locations.locations_by_name[haw.CheckLocation.PoohsHowseHundredAcreWoodMap]
        regular = regular_weights.get_weight(itemRarity.MYTHIC, haw_map)
        reverse = reverse_weights.get_weight(itemRarity.MYTHIC, haw_map)
        both = both_weights.get_weight(itemRarity.MYTHIC, haw_map)
        self.assertEqual(min_weight, regular)
        self.assertEqual(max_weight, reverse)
        self.assertTrue(both in range(regular + 1, reverse))

        # Medium depth location
        kangas_magic_boost = regular_locations.locations_by_name[haw.CheckLocation.KangasHowseMagicBoost]
        regular = regular_weights.get_weight(itemRarity.MYTHIC, kangas_magic_boost)
        reverse = reverse_weights.get_weight(itemRarity.MYTHIC, kangas_magic_boost)
        both = both_weights.get_weight(itemRarity.MYTHIC, kangas_magic_boost)
        self.assertGreater(regular, min_weight)
        self.assertGreater(reverse, min_weight)
        if reverse > regular:
            self.assertTrue(both in range(regular + 1, reverse))
        else:
            self.assertTrue(both in range(reverse + 1, regular))

        # Latest regular depth location
        starry_hill_cure = regular_locations.locations_by_name[haw.CheckLocation.StarryHillCureElement]
        regular = regular_weights.get_weight(itemRarity.MYTHIC, starry_hill_cure)
        reverse = reverse_weights.get_weight(itemRarity.MYTHIC, starry_hill_cure)
        both = both_weights.get_weight(itemRarity.MYTHIC, starry_hill_cure)
        self.assertEqual(max_weight, regular)
        self.assertEqual(min_weight, reverse)
        self.assertTrue(both in range(reverse + 1, regular))

        # Sample a few levels
        level_1 = soralevel.level_reward(1, "Level 1", None)
        self.assertEqual(min_weight, regular_weights.get_weight(itemRarity.MYTHIC, level_1))
        self.assertEqual(min_weight, reverse_weights.get_weight(itemRarity.MYTHIC, level_1))
        self.assertEqual(min_weight, both_weights.get_weight(itemRarity.MYTHIC, level_1))

        level_25 = soralevel.level_reward(25, "Level 25", None)
        self.assertTrue(regular_weights.get_weight(itemRarity.MYTHIC, level_25) in range(min_weight + 1, max_weight))
        self.assertTrue(reverse_weights.get_weight(itemRarity.MYTHIC, level_25) in range(min_weight + 1, max_weight))
        self.assertTrue(both_weights.get_weight(itemRarity.MYTHIC, level_25) in range(min_weight + 1, max_weight))

        level_50 = soralevel.level_reward(50, "Level 50", None)
        self.assertEqual(max_weight, regular_weights.get_weight(itemRarity.MYTHIC, level_50))
        self.assertEqual(max_weight, reverse_weights.get_weight(itemRarity.MYTHIC, level_50))
        self.assertEqual(max_weight, both_weights.get_weight(itemRarity.MYTHIC, level_50))


if __name__ == '__main__':
    unittest.main()

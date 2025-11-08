import unittest

from List.ItemList import Items
from List.configDict import LevelUpStatBonus
from List.inventory import ability
from List.inventory.growth import (
    HighJump1,
    HighJump2,
    HighJump3,
    HighJumpMax,
    QuickRun1,
    QuickRun2,
    QuickRun3,
    QuickRunMax,
    AerialDodge1,
    AerialDodge2,
    AerialDodge3,
    AerialDodgeMax,
    Glide1,
    Glide2,
    Glide3,
    GlideMax,
    DodgeRoll1,
    DodgeRoll2,
    DodgeRoll3,
    DodgeRollMax,
    GrowthType,
)
from Module.modifier import SeedModifier


class Tests(unittest.TestCase):
    def test_default_ability_pool(self):
        all_action = Items.getActionAbilityList()
        all_support = Items.getSupportAbilityList() + Items.getKeybladeAbilityList() + Items.getLevelAbilityList()
        pool = SeedModifier.default_ability_pool(action=all_action, support=all_support)
        self.assertCountEqual(all_action + all_support, pool)

    def test_random_ability_pool(self):
        all_action = Items.getActionAbilityList()
        all_support = Items.getSupportAbilityList() + Items.getKeybladeAbilityList() + Items.getLevelAbilityList()
        for _ in range(1000):
            pool = SeedModifier.random_ability_pool(
                action=all_action, support=all_support
            )
            self.assertEqual(len(pool), len(all_action) + len(all_support))
            second_chance = next(
                (a for a in pool if a.item == ability.SecondChance), None
            )
            self.assertIsNotNone(second_chance)
            once_more = next((a for a in pool if a.item == ability.OnceMore), None)
            self.assertIsNotNone(once_more)

    def test_random_support_ability_pool(self):
        all_action = Items.getActionAbilityList()
        all_support = Items.getSupportAbilityList() + Items.getKeybladeAbilityList() + Items.getLevelAbilityList()
        for _ in range(1000):
            pool = SeedModifier.random_support_ability_pool(
                action=all_action, support=all_support
            )
            self.assertEqual(len(pool), len(all_action) + len(all_support))
            second_chance = next(
                (a for a in pool if a.item == ability.SecondChance), None
            )
            self.assertIsNotNone(second_chance)
            once_more = next((a for a in pool if a.item == ability.OnceMore), None)
            self.assertIsNotNone(once_more)
            for action_ability in all_action:
                self.assertIn(action_ability, pool)

    def test_random_stackable_ability_pool(self):
        all_action = Items.getActionAbilityList()
        all_support = Items.getSupportAbilityList() + Items.getKeybladeAbilityList() + Items.getLevelAbilityList()
        for _ in range(1000):
            pool = SeedModifier.random_stackable_ability_pool(
                action=all_action, support=all_support
            )
            self.assertEqual(len(pool), len(all_action) + len(all_support))
            second_chance = next(
                (a for a in pool if a.item == ability.SecondChance), None
            )
            self.assertIsNotNone(second_chance)
            once_more = next((a for a in pool if a.item == ability.OnceMore), None)
            self.assertIsNotNone(once_more)

    def test_level_up_stat_pool_normal(self):
        pool = SeedModifier.level_up_stat_pool(glass_cannon=False)
        bonuses = [bonus for bonus, _ in pool]
        expected = [
            LevelUpStatBonus.STRENGTH,
            LevelUpStatBonus.MAGIC,
            LevelUpStatBonus.DEFENSE,
            LevelUpStatBonus.AP,
        ]
        self.assertCountEqual(expected, bonuses)

    def test_level_up_stat_pool_glass_cannon(self):
        pool = SeedModifier.level_up_stat_pool(glass_cannon=True)
        bonuses = [bonus for bonus, _ in pool]
        expected = [
            LevelUpStatBonus.STRENGTH,
            LevelUpStatBonus.MAGIC,
            LevelUpStatBonus.AP,
        ]
        self.assertCountEqual(expected, bonuses)

    def test_level_up_stat_pool_weighted_default(self):
        pool = SeedModifier.level_up_stat_pool_weighted()
        bonuses = [bonus for bonus, _, _ in pool]
        weights = [weight for _, _, weight in pool]
        expected_bonuses = [
            LevelUpStatBonus.STRENGTH,
            LevelUpStatBonus.MAGIC,
            LevelUpStatBonus.DEFENSE,
            LevelUpStatBonus.AP,
        ]
        expected_weights = [
            25,
            25,
            25,
            25,
        ]
        self.assertCountEqual(expected_bonuses, bonuses)
        self.assertCountEqual(expected_weights, weights)

    def test_level_up_stat_pool_weighted_glass_cannon(self):
        pool = SeedModifier.level_up_stat_pool_weighted(def_rate=0)
        bonuses = [bonus for bonus, _, _ in pool]
        weights = [weight for _, _, weight in pool]
        expected_bonuses = [
            LevelUpStatBonus.STRENGTH,
            LevelUpStatBonus.MAGIC,
            LevelUpStatBonus.AP,
        ]
        expected_weights = [
            34,
            33,
            33,
        ]
        self.assertCountEqual(expected_bonuses, bonuses)
        self.assertCountEqual(expected_weights, weights)

    def test_level_up_stat_pool_weighted_str_bias(self):
        pool = SeedModifier.level_up_stat_pool_weighted(str_rate=50)
        bonuses = [bonus for bonus, _, _ in pool]
        weights = [weight for _, _, weight in pool]
        expected_bonuses = [
            LevelUpStatBonus.STRENGTH,
            LevelUpStatBonus.MAGIC,
            LevelUpStatBonus.DEFENSE,
            LevelUpStatBonus.AP,
        ]
        expected_weights = [
            40,
            20,
            20,
            20,
        ]
        self.assertCountEqual(expected_bonuses, bonuses)
        self.assertCountEqual(expected_weights, weights)

    def test_movement_disabled(self):
        specific_growth = {
            GrowthType.HIGH_JUMP: 0,
            GrowthType.QUICK_RUN: 0,
            GrowthType.DODGE_ROLL: 0,
            GrowthType.AERIAL_DODGE: 0,
            GrowthType.GLIDE: 0,
        }
        growths = SeedModifier.starting_growth(specific_growth, random_range=(0, 0))
        self.assertEqual(0, len(growths))

    def test_movement_level_1(self):
        specific_growth = {
            GrowthType.HIGH_JUMP: 1,
            GrowthType.QUICK_RUN: 1,
            GrowthType.DODGE_ROLL: 1,
            GrowthType.AERIAL_DODGE: 1,
            GrowthType.GLIDE: 1,
        }
        expected = [
            HighJump1,
            QuickRun1,
            AerialDodge1,
            Glide1,
            DodgeRoll1,
        ]
        growths = SeedModifier.starting_growth(specific_growth, random_range=(0, 0))
        self.assertCountEqual(expected, growths)

    def test_movement_level_2(self):
        specific_growth = {
            GrowthType.HIGH_JUMP: 2,
            GrowthType.QUICK_RUN: 2,
            GrowthType.DODGE_ROLL: 2,
            GrowthType.AERIAL_DODGE: 2,
            GrowthType.GLIDE: 2,
        }
        expected = [
            HighJump1,
            HighJump2,
            QuickRun1,
            QuickRun2,
            AerialDodge1,
            AerialDodge2,
            Glide1,
            Glide2,
            DodgeRoll1,
            DodgeRoll2,
        ]
        growths = SeedModifier.starting_growth(specific_growth, random_range=(0, 0))
        self.assertCountEqual(expected, growths)

    def test_movement_level_3(self):
        specific_growth = {
            GrowthType.HIGH_JUMP: 3,
            GrowthType.QUICK_RUN: 3,
            GrowthType.DODGE_ROLL: 3,
            GrowthType.AERIAL_DODGE: 3,
            GrowthType.GLIDE: 3,
        }
        expected = [
            HighJump1,
            HighJump2,
            HighJump3,
            QuickRun1,
            QuickRun2,
            QuickRun3,
            AerialDodge1,
            AerialDodge2,
            AerialDodge3,
            Glide1,
            Glide2,
            Glide3,
            DodgeRoll1,
            DodgeRoll2,
            DodgeRoll3,
        ]
        growths = SeedModifier.starting_growth(specific_growth, random_range=(0, 0))
        self.assertCountEqual(expected, growths)

    def test_movement_level_4(self):
        specific_growth = {
            GrowthType.HIGH_JUMP: 4,
            GrowthType.QUICK_RUN: 4,
            GrowthType.DODGE_ROLL: 4,
            GrowthType.AERIAL_DODGE: 4,
            GrowthType.GLIDE: 4,
        }
        expected = [
            HighJump1,
            HighJump2,
            HighJump3,
            HighJumpMax,
            QuickRun1,
            QuickRun2,
            QuickRun3,
            QuickRunMax,
            AerialDodge1,
            AerialDodge2,
            AerialDodge3,
            AerialDodgeMax,
            Glide1,
            Glide2,
            Glide3,
            GlideMax,
            DodgeRoll1,
            DodgeRoll2,
            DodgeRoll3,
            DodgeRollMax,
        ]
        growths = SeedModifier.starting_growth(specific_growth, random_range=(0, 0))
        self.assertCountEqual(expected, growths)

    def test_random_3(self):
        specific_growth = {
            GrowthType.HIGH_JUMP: 0,
            GrowthType.QUICK_RUN: 0,
            GrowthType.DODGE_ROLL: 0,
            GrowthType.AERIAL_DODGE: 0,
            GrowthType.GLIDE: 0,
        }
        for _ in range(1000):
            growths = SeedModifier.starting_growth(specific_growth, random_range=(3, 3))
            self.assertEqual(3, len(growths))

    def test_random_5(self):
        specific_growth = {
            GrowthType.HIGH_JUMP: 0,
            GrowthType.QUICK_RUN: 0,
            GrowthType.DODGE_ROLL: 0,
            GrowthType.AERIAL_DODGE: 0,
            GrowthType.GLIDE: 0,
        }
        for _ in range(1000):
            growths = SeedModifier.starting_growth(specific_growth, random_range=(5, 5))
            self.assertEqual(5, len(growths))


if __name__ == "__main__":
    unittest.main()

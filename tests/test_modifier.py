import unittest

from List.ItemList import Items
from List.configDict import StartingMovementOption, LevelUpStatBonus
from List.inventory import ability
from List.inventory.growth import HighJump1, HighJump2, HighJump3, HighJumpMax, QuickRun1, QuickRun2, \
    QuickRun3, QuickRunMax, AerialDodge1, AerialDodge2, AerialDodge3, AerialDodgeMax, Glide1, Glide2, Glide3, \
    GlideMax, DodgeRoll1, DodgeRoll2, DodgeRoll3, DodgeRollMax
from Module.modifier import SeedModifier


class Tests(unittest.TestCase):

    def test_default_ability_pool(self):
        all_action = Items.getActionAbilityList()
        all_support = Items.getSupportAbilityList() + Items.getLevelAbilityList()
        pool = SeedModifier.default_ability_pool(action=all_action, support=all_support)
        self.assertCountEqual(all_action + all_support, pool)

    def test_random_ability_pool(self):
        all_action = Items.getActionAbilityList()
        all_support = Items.getSupportAbilityList() + Items.getLevelAbilityList()
        for _ in range(1000):
            pool = SeedModifier.random_ability_pool(action=all_action, support=all_support)
            self.assertEqual(len(pool), len(all_action) + len(all_support))
            second_chance = next((a for a in pool if a.item == ability.SecondChance), None)
            self.assertIsNotNone(second_chance)
            once_more = next((a for a in pool if a.item == ability.OnceMore), None)
            self.assertIsNotNone(once_more)

    def test_random_support_ability_pool(self):
        all_action = Items.getActionAbilityList()
        all_support = Items.getSupportAbilityList() + Items.getLevelAbilityList()
        for _ in range(1000):
            pool = SeedModifier.random_support_ability_pool(action=all_action, support=all_support)
            self.assertEqual(len(pool), len(all_action) + len(all_support))
            second_chance = next((a for a in pool if a.item == ability.SecondChance), None)
            self.assertIsNotNone(second_chance)
            once_more = next((a for a in pool if a.item == ability.OnceMore), None)
            self.assertIsNotNone(once_more)
            for action_ability in all_action:
                self.assertIn(action_ability, pool)

    def test_random_stackable_ability_pool(self):
        all_action = Items.getActionAbilityList()
        all_support = Items.getSupportAbilityList() + Items.getLevelAbilityList()
        for _ in range(1000):
            pool = SeedModifier.random_stackable_ability_pool(action=all_action, support=all_support)
            self.assertEqual(len(pool), len(all_action) + len(all_support))
            second_chance = next((a for a in pool if a.item == ability.SecondChance), None)
            self.assertIsNotNone(second_chance)
            once_more = next((a for a in pool if a.item == ability.OnceMore), None)
            self.assertIsNotNone(once_more)

    def test_level_up_stat_pool_normal(self):
        pool = SeedModifier.level_up_stat_pool(glass_cannon=False)
        bonuses = [bonus for bonus, _ in pool]
        expected = [LevelUpStatBonus.STRENGTH, LevelUpStatBonus.MAGIC, LevelUpStatBonus.DEFENSE, LevelUpStatBonus.AP]
        self.assertCountEqual(expected, bonuses)

    def test_level_up_stat_pool_glass_cannon(self):
        pool = SeedModifier.level_up_stat_pool(glass_cannon=True)
        bonuses = [bonus for bonus, _ in pool]
        expected = [LevelUpStatBonus.STRENGTH, LevelUpStatBonus.MAGIC, LevelUpStatBonus.AP]
        self.assertCountEqual(expected, bonuses)

    def test_movement_disabled(self):
        growths = SeedModifier.starting_growth(StartingMovementOption.DISABLED)
        self.assertEqual(0, len(growths))

    def test_movement_level_1(self):
        expected = [
            HighJump1,
            QuickRun1,
            AerialDodge1,
            Glide1,
            DodgeRoll1,
        ]
        growths = SeedModifier.starting_growth(StartingMovementOption.LEVEL_1)
        self.assertCountEqual(expected, growths)

    def test_movement_level_2(self):
        expected = [
            HighJump1, HighJump2,
            QuickRun1, QuickRun2,
            AerialDodge1, AerialDodge2,
            Glide1, Glide2,
            DodgeRoll1, DodgeRoll2,
        ]
        growths = SeedModifier.starting_growth(StartingMovementOption.LEVEL_2)
        self.assertCountEqual(expected, growths)

    def test_movement_level_3(self):
        expected = [
            HighJump1, HighJump2, HighJump3,
            QuickRun1, QuickRun2, QuickRun3,
            AerialDodge1, AerialDodge2, AerialDodge3,
            Glide1, Glide2, Glide3,
            DodgeRoll1, DodgeRoll2, DodgeRoll3,
        ]
        growths = SeedModifier.starting_growth(StartingMovementOption.LEVEL_3)
        self.assertCountEqual(expected, growths)

    def test_movement_level_4(self):
        expected = [
            HighJump1, HighJump2, HighJump3, HighJumpMax,
            QuickRun1, QuickRun2, QuickRun3, QuickRunMax,
            AerialDodge1, AerialDodge2, AerialDodge3, AerialDodgeMax,
            Glide1, Glide2, Glide3, GlideMax,
            DodgeRoll1, DodgeRoll2, DodgeRoll3, DodgeRollMax,
        ]
        growths = SeedModifier.starting_growth(StartingMovementOption.LEVEL_4)
        self.assertCountEqual(expected, growths)

    def test_random_3(self):
        for _ in range(1000):
            growths = SeedModifier.starting_growth(StartingMovementOption.RANDOM_3)
            self.assertEqual(3, len(growths))

    def test_random_5(self):
        for _ in range(1000):
            growths = SeedModifier.starting_growth(StartingMovementOption.RANDOM_5)
            self.assertEqual(5, len(growths))


if __name__ == '__main__':
    unittest.main()

import unittest

from Class import settingkey
from Class.newLocationClass import KH2Location
from Class.seedSettings import SeedSettings
from List.configDict import itemType
from List.inventory import keyblade, ability
from List.location import weaponslot
from Module.newRandomize import Randomizer
from seedtests import seedtest


class Tests(unittest.TestCase):

    def test_vanilla_stats(self):
        """ Verifies that keyblades have their vanilla stats if configured as such. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.KEYBLADE_STATS_RANDOMIZED, False)

        for randomizer in seedtest.test_seeds(seed_settings):
            self._validate_vanilla_stats(randomizer)

    def test_random_stats(self):
        """ Verifies that keyblades have their randomized stats in the configured range. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.KEYBLADE_STATS_RANDOMIZED, True)
        seed_settings.set(settingkey.KEYBLADE_MIN_STAT, 4)
        seed_settings.set(settingkey.KEYBLADE_MAX_STAT, 8)

        for randomizer in seedtest.test_seeds(seed_settings):
            self._validate_random_stats(randomizer, minimum_expected=4, maximum_expected=8, struggle_expected=6)

    def test_vanilla_abilities(self):
        """ Verifies that keyblades have their vanilla abilities if configured as such. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.KEYBLADE_ABILITIES_RANDOMIZED, False)

        for randomizer in seedtest.test_seeds(seed_settings):
            self._validate_vanilla_abilities(randomizer)

    def test_random_abilities(self):
        """ Verifies that randomized keyblade abilities only come from the configured pool. """

        # Effectively an arbitrary list of allowed abilities for testing
        ability_list = {
            ability.Draw, ability.NegativeCombo, ability.BerserkCharge, ability.DamageDrive, ability.DriveBoost,
            ability.FormBoost, ability.SummonBoost, ability.CombinationBoost, ability.ExperienceBoost,
            ability.LeafBracer, ability.MagicLockOn, ability.NoExperience, ability.Draw, ability.Jackpot,
            ability.LuckyLucky, ability.FireBoost, ability.SlideDash, ability.GuardBreak, ability.Explosion,
            ability.FinishingLeap, ability.Counterguard, ability.AerialSweep, ability.AerialSpiral,
            ability.HorizontalSlash, ability.AerialFinish, ability.RetaliatingSlash, ability.AutoValor,
        }

        seed_settings = SeedSettings()
        seed_settings.set(settingkey.KEYBLADE_ABILITIES_RANDOMIZED, True)
        seed_settings.set(
            settingkey.KEYBLADE_SUPPORT_ABILITIES,
            [a.id for a in ability_list if a.type == itemType.SUPPORT_ABILITY]
        )
        seed_settings.set(
            settingkey.KEYBLADE_ACTION_ABILITIES,
            [a.id for a in ability_list if a.type == itemType.ACTION_ABILITY]
        )

        for randomizer in seedtest.test_seeds(seed_settings):
            self._validate_random_abilities(randomizer, ability_list)

    def _validate_vanilla_stats(self, randomizer: Randomizer):
        for location in weaponslot.keyblade_slots():
            assigned_stats = randomizer.weapon_stats_for_location(location.name())
            key = self._keyblade_for_location(location)
            self.assertEqual(key.strength, assigned_stats.strength, f"{key.name} should have its vanilla strength")
            self.assertEqual(key.magic, assigned_stats.magic, f"{key.name} should have its vanilla magic")

    def _validate_random_stats(
            self,
            randomizer: Randomizer,
            minimum_expected: int,
            maximum_expected: int,
            struggle_expected: int
    ):
        for location in weaponslot.keyblade_slots():
            assigned_stats = randomizer.weapon_stats_for_location(location.name())
            assigned_strength = assigned_stats.strength
            assigned_magic = assigned_stats.magic
            key = self._keyblade_for_location(location)
            if key.struggle_weapon:
                self.assertEqual(struggle_expected, assigned_strength)
                self.assertEqual(struggle_expected, assigned_magic)
            else:
                self.assertGreaterEqual(assigned_strength, minimum_expected)
                self.assertLessEqual(assigned_strength, maximum_expected)
                self.assertGreaterEqual(assigned_magic, minimum_expected)
                self.assertLessEqual(assigned_magic, maximum_expected)

    def _validate_vanilla_abilities(self, randomizer: Randomizer):
        for location in weaponslot.keyblade_slots():
            assigned_item = randomizer.assignment_for_location(location.name()).item.item
            key = self._keyblade_for_location(location)
            if key.struggle_weapon:
                self.assertEqual(ability.Draw, assigned_item, f"{key.name} should have Draw")
            else:
                self.assertEqual(key.ability, assigned_item, f"{key.name} should have its vanilla ability")

    def _validate_random_abilities(self, randomizer: Randomizer, ability_list: set[ability.Ability]):
        for location in weaponslot.keyblade_slots():
            assigned_item = randomizer.assignment_for_location(location.name()).item.item
            key = self._keyblade_for_location(location)
            if key.struggle_weapon:
                self.assertEqual(ability.Draw, assigned_item, f"{key.name} should have Draw")
            else:
                self.assertTrue(assigned_item in ability_list, f"{key.name} has an ability it should not: {assigned_item}")

    @staticmethod
    def _keyblade_for_location(location: KH2Location) -> keyblade.Keyblade:
        location_id = location.LocationId
        return next(key for key in keyblade.get_all_keyblades() if key.weaponslot_id == location_id)


if __name__ == '__main__':
    unittest.main()

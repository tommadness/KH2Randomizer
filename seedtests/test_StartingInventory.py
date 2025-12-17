import unittest

from Class import settingkey
from Class.seedSettings import SeedSettings
from List.inventory import ability, misc, proof, report, storyunlock, magic
from List.inventory.item import InventoryItem
from List.location import simulatedtwilighttown as stt
from Module.newRandomize import Randomizer
from seedtests import seedtest


class Tests(unittest.TestCase):

    def test_no_starting_abilities(self):
        """ Verifies that potential starting abilities have the appropriate counts when starting with none. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.STARTING_ABILITIES, [])

        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(0, self._starting_count(randomizer, [ability.Scan]))
            self.assertEqual(0, self._starting_count(randomizer, [ability.NoExperience]))
            self.assertEqual(0, self._starting_count(randomizer, [ability.Guard]))
            self.assertEqual(0, self._starting_count(randomizer, [ability.FinishingPlus]))

            self.assertEqual(2, self._assignment_count(randomizer, [ability.Scan]))
            self.assertEqual(2, self._assignment_count(randomizer, [ability.NoExperience]))
            self.assertEqual(1, self._assignment_count(randomizer, [ability.Guard]))
            self.assertEqual(3, self._assignment_count(randomizer, [ability.FinishingPlus]))

    def test_starting_abilities_removed_from_pool(self):
        """ Verifies that potential starting abilities have the appropriate counts when starting with some. """
        seed_settings = SeedSettings()
        seed_settings.set(
            settingkey.STARTING_ABILITIES,
            [ability.Scan.id, ability.NoExperience.id, ability.Guard.id, ability.FinishingPlus.id]
        )

        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(1, self._starting_count(randomizer, [ability.Scan]))
            self.assertEqual(1, self._starting_count(randomizer, [ability.NoExperience]))
            self.assertEqual(1, self._starting_count(randomizer, [ability.Guard]))
            self.assertEqual(1, self._starting_count(randomizer, [ability.FinishingPlus]))

            self.assertEqual(1, self._assignment_count(randomizer, [ability.Scan]))
            self.assertEqual(1, self._assignment_count(randomizer, [ability.NoExperience]))
            self.assertEqual(0, self._assignment_count(randomizer, [ability.Guard]))
            self.assertEqual(2, self._assignment_count(randomizer, [ability.FinishingPlus]))

    def test_no_starting_items(self):
        """ Verifies that potential starting items have the appropriate counts when starting with none. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.STARTING_ITEMS, [])
        seed_settings.set(settingkey.ENABLE_PROMISE_CHARM, True)

        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(0, self._starting_count(randomizer, [misc.HadesCupTrophy]))
            self.assertEqual(0, self._starting_count(randomizer, [misc.OlympusStone]))
            self.assertEqual(0, self._starting_count(randomizer, [misc.UnknownDisk]))
            self.assertEqual(0, self._starting_count(randomizer, [proof.ProofOfConnection]))
            self.assertEqual(0, self._starting_count(randomizer, [proof.ProofOfNonexistence]))
            self.assertEqual(0, self._starting_count(randomizer, [proof.ProofOfPeace]))
            self.assertEqual(0, self._starting_count(randomizer, [misc.PromiseCharm]))

            self.assertEqual(1, self._assignment_count(randomizer, [misc.HadesCupTrophy]))
            self.assertEqual(1, self._assignment_count(randomizer, [misc.OlympusStone]))
            self.assertEqual(1, self._assignment_count(randomizer, [misc.UnknownDisk]))
            self.assertEqual(1, self._assignment_count(randomizer, [proof.ProofOfConnection]))
            self.assertEqual(1, self._assignment_count(randomizer, [proof.ProofOfNonexistence]))
            self.assertEqual(1, self._assignment_count(randomizer, [proof.ProofOfPeace]))
            self.assertEqual(1, self._assignment_count(randomizer, [misc.PromiseCharm]))

    def test_starting_items_removed_from_pool(self):
        """ Verifies that potential starting items have the appropriate counts when starting with some. """
        seed_settings = SeedSettings()
        seed_settings.set(
            settingkey.STARTING_ITEMS,
            [misc.UnknownDisk.id, proof.ProofOfPeace.id, misc.PromiseCharm.id]
        )
        seed_settings.set(settingkey.ENABLE_PROMISE_CHARM, True)

        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(0, self._starting_count(randomizer, [misc.HadesCupTrophy]))
            self.assertEqual(0, self._starting_count(randomizer, [misc.OlympusStone]))
            self.assertEqual(1, self._starting_count(randomizer, [misc.UnknownDisk]))
            self.assertEqual(0, self._starting_count(randomizer, [proof.ProofOfConnection]))
            self.assertEqual(0, self._starting_count(randomizer, [proof.ProofOfNonexistence]))
            self.assertEqual(1, self._starting_count(randomizer, [proof.ProofOfPeace]))
            self.assertEqual(1, self._starting_count(randomizer, [misc.PromiseCharm]))

            self.assertEqual(1, self._assignment_count(randomizer, [misc.HadesCupTrophy]))
            self.assertEqual(1, self._assignment_count(randomizer, [misc.OlympusStone]))
            self.assertEqual(0, self._assignment_count(randomizer, [misc.UnknownDisk]))
            self.assertEqual(1, self._assignment_count(randomizer, [proof.ProofOfConnection]))
            self.assertEqual(1, self._assignment_count(randomizer, [proof.ProofOfNonexistence]))
            self.assertEqual(0, self._assignment_count(randomizer, [proof.ProofOfPeace]))
            self.assertEqual(0, self._assignment_count(randomizer, [misc.PromiseCharm]))

    def test_no_starting_reports(self):
        """ Verifies that reports have the appropriate counts when starting with none and none in the shop. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.STARTING_REPORTS, 0)
        seed_settings.set(settingkey.SHOP_REPORTS, 0)

        all_reports = report.all_reports()
        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(0, self._starting_count(randomizer, all_reports))
            self.assertEqual(0, self._shop_count(randomizer, all_reports))
            self.assertEqual(13, self._assignment_count(randomizer, all_reports))

    def test_starting_reports(self):
        """ Verifies that starting reports have the appropriate counts when starting with some and none in the shop. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.STARTING_REPORTS, 4)
        seed_settings.set(settingkey.SHOP_REPORTS, 0)

        all_reports = report.all_reports()
        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(4, self._starting_count(randomizer, all_reports))
            self.assertEqual(0, self._shop_count(randomizer, all_reports))
            self.assertEqual(9, self._assignment_count(randomizer, all_reports))

    def test_shop_reports(self):
        """ Verifies that starting reports have the appropriate counts when starting with none and some in the shop. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.STARTING_REPORTS, 0)
        seed_settings.set(settingkey.SHOP_REPORTS, 7)

        all_reports = report.all_reports()
        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(0, self._starting_count(randomizer, all_reports))
            self.assertEqual(7, self._shop_count(randomizer, all_reports))
            self.assertEqual(6, self._assignment_count(randomizer, all_reports))

    def test_start_and_shop_reports(self):
        """ Verifies that starting reports have the appropriate counts when starting with some and some in the shop. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.STARTING_REPORTS, 4)
        seed_settings.set(settingkey.SHOP_REPORTS, 5)

        all_reports = report.all_reports()
        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(4, self._starting_count(randomizer, all_reports))
            self.assertEqual(5, self._shop_count(randomizer, all_reports))
            self.assertEqual(4, self._assignment_count(randomizer, all_reports))

    def test_no_starting_unlocks(self):
        """ Verifies that starting unlocks have the appropriate counts when starting with none and none in the shop. """
        seed_settings = SeedSettings()
        self._clear_unlock_settings(seed_settings)
        seed_settings.set(settingkey.SHOP_UNLOCKS, 0)

        for randomizer in seedtest.test_seeds(seed_settings):
            for unlock in storyunlock.all_story_unlocks():
                self.assertEqual(0, self._starting_count(randomizer, [unlock]))
                self.assertEqual(0, self._shop_count(randomizer, [unlock]))
                self.assertEqual(unlock.visit_count, self._assignment_count(randomizer, [unlock]))

    def test_first_visit_starting_unlocks(self):
        """ Verifies that starting unlocks have the appropriate counts when starting with all first visits unlocked. """
        seed_settings = SeedSettings()
        self._clear_unlock_settings(seed_settings)
        seed_settings.set(settingkey.STARTING_UNLOCKS_SP, 1)
        seed_settings.set(settingkey.STARTING_UNLOCKS_PR, 1)
        seed_settings.set(settingkey.STARTING_UNLOCKS_TT, 1)
        seed_settings.set(settingkey.STARTING_UNLOCKS_OC, 1)
        seed_settings.set(settingkey.STARTING_UNLOCKS_HT, 1)
        seed_settings.set(settingkey.STARTING_UNLOCKS_LOD, 1)
        seed_settings.set(settingkey.STARTING_UNLOCKS_TWTNW, 1)
        seed_settings.set(settingkey.STARTING_UNLOCKS_BC, 1)
        seed_settings.set(settingkey.STARTING_UNLOCKS_AG, 1)
        seed_settings.set(settingkey.STARTING_UNLOCKS_PL, 1)
        seed_settings.set(settingkey.STARTING_UNLOCKS_HB, 1)
        seed_settings.set(settingkey.STARTING_UNLOCKS_DC, 1)
        seed_settings.set(settingkey.STARTING_UNLOCKS_STT, 1)
        seed_settings.set(settingkey.SHOP_UNLOCKS, 0)

        all_unlocks = storyunlock.all_story_unlocks()
        first_visit_unlock_count = len(all_unlocks)
        remainder = len(storyunlock.all_individual_story_unlocks()) - first_visit_unlock_count
        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(first_visit_unlock_count, self._starting_count(randomizer, all_unlocks))
            self.assertEqual(0, self._shop_count(randomizer, all_unlocks))
            self.assertEqual(remainder, self._assignment_count(randomizer, all_unlocks))

    def test_all_starting_unlocks(self):
        """ Verifies that starting unlocks have the appropriate counts when starting with all visits unlocked. """
        seed_settings = SeedSettings()
        self._start_with_all_unlocks(seed_settings)
        seed_settings.set(settingkey.SHOP_UNLOCKS, 0)

        all_unlocks = storyunlock.all_story_unlocks()
        individual_unlocks_count = len(storyunlock.all_individual_story_unlocks())
        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(individual_unlocks_count, self._starting_count(randomizer, all_unlocks))
            self.assertEqual(0, self._shop_count(randomizer, all_unlocks))
            self.assertEqual(0, self._assignment_count(randomizer, all_unlocks))

    def test_specific_starting_unlocks(self):
        """ Verifies that starting unlocks have the appropriate counts when starting with some and none in the shop. """
        seed_settings = SeedSettings()
        self._clear_unlock_settings(seed_settings)
        seed_settings.set(settingkey.STARTING_UNLOCKS_TT, 2)
        seed_settings.set(settingkey.STARTING_UNLOCKS_AG, 1)
        seed_settings.set(settingkey.STARTING_UNLOCKS_DC, 2)
        seed_settings.set(settingkey.SHOP_UNLOCKS, 0)

        for randomizer in seedtest.test_seeds(seed_settings):
            for unlock in storyunlock.all_story_unlocks():
                if unlock == storyunlock.IceCream:
                    self.assertEqual(2, self._starting_count(randomizer, [unlock]))
                    self.assertEqual(0, self._shop_count(randomizer, [unlock]))
                    self.assertEqual(1, self._assignment_count(randomizer, [unlock]))
                elif unlock == storyunlock.Scimitar:
                    self.assertEqual(1, self._starting_count(randomizer, [unlock]))
                    self.assertEqual(0, self._shop_count(randomizer, [unlock]))
                    self.assertEqual(1, self._assignment_count(randomizer, [unlock]))
                elif unlock == storyunlock.RoyalSummons:
                    self.assertEqual(2, self._starting_count(randomizer, [unlock]))
                    self.assertEqual(0, self._shop_count(randomizer, [unlock]))
                    self.assertEqual(0, self._assignment_count(randomizer, [unlock]))
                else:
                    self.assertEqual(0, self._starting_count(randomizer, [unlock]))
                    self.assertEqual(0, self._shop_count(randomizer, [unlock]))
                    self.assertEqual(unlock.visit_count, self._assignment_count(randomizer, [unlock]))

    def test_random_starting_unlocks(self):
        """ Verifies that starting unlocks have the appropriate counts when starting with a fixed random number. """
        seed_settings = SeedSettings()
        self._clear_unlock_settings(seed_settings)
        seed_settings.set(settingkey.STARTING_VISIT_RANDOM_MIN, 6)
        seed_settings.set(settingkey.STARTING_VISIT_RANDOM_MAX, 6)

        all_unlocks = storyunlock.all_story_unlocks()
        remainder = len(storyunlock.all_individual_story_unlocks()) - 6
        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(6, self._starting_count(randomizer, all_unlocks))
            self.assertEqual(0, self._shop_count(randomizer, all_unlocks))
            self.assertEqual(remainder, self._assignment_count(randomizer, all_unlocks))

    def test_shop_unlocks(self):
        """ Verifies that starting unlocks have the appropriate counts when starting with none and some in the shop. """
        seed_settings = SeedSettings()
        self._clear_unlock_settings(seed_settings)
        seed_settings.set(settingkey.SHOP_UNLOCKS, 8)

        all_unlocks = storyunlock.all_story_unlocks()
        remainder = len(storyunlock.all_individual_story_unlocks()) - 8
        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(0, self._starting_count(randomizer, all_unlocks))
            self.assertEqual(8, self._shop_count(randomizer, all_unlocks))
            self.assertEqual(remainder, self._assignment_count(randomizer, all_unlocks))

    def test_start_and_shop_unlocks(self):
        """ Verifies that starting unlocks have the appropriate counts when starting with some and some in the shop. """
        seed_settings = SeedSettings()
        self._clear_unlock_settings(seed_settings)
        seed_settings.set(settingkey.STARTING_UNLOCKS_HT, 1)
        seed_settings.set(settingkey.STARTING_UNLOCKS_PR, 1)
        seed_settings.set(settingkey.STARTING_UNLOCKS_TWTNW, 2)
        seed_settings.set(settingkey.SHOP_UNLOCKS, 9)

        all_unlocks = storyunlock.all_story_unlocks()
        for randomizer in seedtest.test_seeds(seed_settings):
            starting_count = self._starting_count(randomizer, all_unlocks)
            shop_count = self._shop_count(randomizer, all_unlocks)
            self.assertEqual(4, starting_count)
            self.assertEqual(9, shop_count)

            remainder = len(storyunlock.all_individual_story_unlocks()) - starting_count - shop_count
            self.assertEqual(remainder, self._assignment_count(randomizer, all_unlocks))

    def test_starting_magic_none(self):
        """ Verifies no starting magic is given if not configured to do so. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.STARTING_MAGIC_FIRE, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_BLIZZARD, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_THUNDER, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_CURE, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_MAGNET, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_REFLECT, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_RANDOM_MIN, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_RANDOM_MAX, 0)

        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(0, self._starting_count(randomizer, [magic.Fire]))
            self.assertEqual(3, self._assignment_count(randomizer, [magic.Fire]))

            self.assertEqual(0, self._starting_count(randomizer, [magic.Blizzard]))
            self.assertEqual(3, self._assignment_count(randomizer, [magic.Blizzard]))

            self.assertEqual(0, self._starting_count(randomizer, [magic.Thunder]))
            self.assertEqual(3, self._assignment_count(randomizer, [magic.Thunder]))

            self.assertEqual(0, self._starting_count(randomizer, [magic.Cure]))
            self.assertEqual(3, self._assignment_count(randomizer, [magic.Cure]))

            self.assertEqual(0, self._starting_count(randomizer, [magic.Magnet]))
            self.assertEqual(3, self._assignment_count(randomizer, [magic.Magnet]))

            self.assertEqual(0, self._starting_count(randomizer, [magic.Reflect]))
            self.assertEqual(3, self._assignment_count(randomizer, [magic.Reflect]))

    def test_starting_magic_specific_only(self):
        """ Verifies magic is given based on the specific specs. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.STARTING_MAGIC_FIRE, 1)
        seed_settings.set(settingkey.STARTING_MAGIC_BLIZZARD, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_THUNDER, 2)
        seed_settings.set(settingkey.STARTING_MAGIC_CURE, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_MAGNET, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_REFLECT, 3)
        seed_settings.set(settingkey.STARTING_MAGIC_RANDOM_MIN, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_RANDOM_MAX, 0)

        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(1, self._starting_count(randomizer, [magic.Fire]))
            self.assertEqual(2, self._assignment_count(randomizer, [magic.Fire]))

            self.assertEqual(0, self._starting_count(randomizer, [magic.Blizzard]))
            self.assertEqual(3, self._assignment_count(randomizer, [magic.Blizzard]))

            self.assertEqual(2, self._starting_count(randomizer, [magic.Thunder]))
            self.assertEqual(1, self._assignment_count(randomizer, [magic.Thunder]))

            self.assertEqual(0, self._starting_count(randomizer, [magic.Cure]))
            self.assertEqual(3, self._assignment_count(randomizer, [magic.Cure]))

            self.assertEqual(0, self._starting_count(randomizer, [magic.Magnet]))
            self.assertEqual(3, self._assignment_count(randomizer, [magic.Magnet]))

            self.assertEqual(3, self._starting_count(randomizer, [magic.Reflect]))
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Reflect]))

    def test_starting_magic_random_only(self):
        """ Verifies magic is given based on the random specs. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.STARTING_MAGIC_FIRE, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_BLIZZARD, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_THUNDER, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_CURE, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_MAGNET, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_REFLECT, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_RANDOM_MIN, 3)
        seed_settings.set(settingkey.STARTING_MAGIC_RANDOM_MAX, 6)

        for randomizer in seedtest.test_seeds(seed_settings):
            fires = self._starting_count(randomizer, [magic.Fire])
            self.assertIn(fires, range(0, 4))
            self.assertEqual(3 - fires, self._assignment_count(randomizer, [magic.Fire]))

            blizzards = self._starting_count(randomizer, [magic.Blizzard])
            self.assertIn(blizzards, range(0, 4))
            self.assertEqual(3 - blizzards, self._assignment_count(randomizer, [magic.Blizzard]))

            thunders = self._starting_count(randomizer, [magic.Thunder])
            self.assertIn(thunders, range(0, 4))
            self.assertEqual(3 - thunders, self._assignment_count(randomizer, [magic.Thunder]))

            cures = self._starting_count(randomizer, [magic.Cure])
            self.assertIn(cures, range(0, 4))
            self.assertEqual(3 - cures, self._assignment_count(randomizer, [magic.Cure]))

            magnets = self._starting_count(randomizer, [magic.Magnet])
            self.assertIn(magnets, range(0, 4))
            self.assertEqual(3 - magnets, self._assignment_count(randomizer, [magic.Magnet]))

            reflects = self._starting_count(randomizer, [magic.Reflect])
            self.assertIn(reflects, range(0, 4))
            self.assertEqual(3 - reflects, self._assignment_count(randomizer, [magic.Reflect]))

            total_assigned = fires + blizzards + thunders + cures + magnets + reflects
            self.assertIn(total_assigned, range(3, 7))

    def test_starting_magic_combination(self):
        """
        Verifies that starting magics have the appropriate counts when starting with some and adding some randomly.
        """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.STARTING_MAGIC_FIRE, 2)
        seed_settings.set(settingkey.STARTING_MAGIC_BLIZZARD, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_THUNDER, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_CURE, 1)
        seed_settings.set(settingkey.STARTING_MAGIC_MAGNET, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_REFLECT, 3)
        seed_settings.set(settingkey.STARTING_MAGIC_RANDOM_MIN, 3)
        seed_settings.set(settingkey.STARTING_MAGIC_RANDOM_MAX, 5)

        for randomizer in seedtest.test_seeds(seed_settings):
            fires = self._starting_count(randomizer, [magic.Fire])
            self.assertIn(fires, range(2, 4))
            self.assertEqual(3 - fires, self._assignment_count(randomizer, [magic.Fire]))

            blizzards = self._starting_count(randomizer, [magic.Blizzard])
            self.assertIn(blizzards, range(0, 4))
            self.assertEqual(3 - blizzards, self._assignment_count(randomizer, [magic.Blizzard]))

            thunders = self._starting_count(randomizer, [magic.Thunder])
            self.assertIn(thunders, range(0, 4))
            self.assertEqual(3 - thunders, self._assignment_count(randomizer, [magic.Thunder]))

            cures = self._starting_count(randomizer, [magic.Cure])
            self.assertIn(cures, range(1, 4))
            self.assertEqual(3 - cures, self._assignment_count(randomizer, [magic.Cure]))

            magnets = self._starting_count(randomizer, [magic.Magnet])
            self.assertIn(magnets, range(0, 4))
            self.assertEqual(3 - magnets, self._assignment_count(randomizer, [magic.Magnet]))

            reflects = self._starting_count(randomizer, [magic.Reflect])
            self.assertEqual(3, reflects)
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Reflect]))

            total_assigned = fires + blizzards + thunders + cures + magnets + reflects
            self.assertIn(total_assigned, range(9, 12))

    def test_starting_magic_overflow_protection(self):
        """ Verifies that bounds checking is handling too much starting magic by just giving all. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.STARTING_MAGIC_FIRE, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_BLIZZARD, 3)
        seed_settings.set(settingkey.STARTING_MAGIC_THUNDER, 1)
        seed_settings.set(settingkey.STARTING_MAGIC_CURE, 3)
        seed_settings.set(settingkey.STARTING_MAGIC_MAGNET, 3)
        seed_settings.set(settingkey.STARTING_MAGIC_REFLECT, 2)
        seed_settings.set(settingkey.STARTING_MAGIC_RANDOM_MIN, 18)
        seed_settings.set(settingkey.STARTING_MAGIC_RANDOM_MAX, 18)

        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(3, self._starting_count(randomizer, [magic.Fire]))
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Fire]))

            self.assertEqual(3, self._starting_count(randomizer, [magic.Blizzard]))
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Blizzard]))

            self.assertEqual(3, self._starting_count(randomizer, [magic.Thunder]))
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Thunder]))

            self.assertEqual(3, self._starting_count(randomizer, [magic.Cure]))
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Cure]))

            self.assertEqual(3, self._starting_count(randomizer, [magic.Magnet]))
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Magnet]))

            self.assertEqual(3, self._starting_count(randomizer, [magic.Reflect]))
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Reflect]))

    def test_starting_magic_specific_all(self):
        """ Verifies that all magic is given if all is chosen for each specifically. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.STARTING_MAGIC_FIRE, 3)
        seed_settings.set(settingkey.STARTING_MAGIC_BLIZZARD, 3)
        seed_settings.set(settingkey.STARTING_MAGIC_THUNDER, 3)
        seed_settings.set(settingkey.STARTING_MAGIC_CURE, 3)
        seed_settings.set(settingkey.STARTING_MAGIC_MAGNET, 3)
        seed_settings.set(settingkey.STARTING_MAGIC_REFLECT, 3)
        seed_settings.set(settingkey.STARTING_MAGIC_RANDOM_MIN, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_RANDOM_MAX, 0)

        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(3, self._starting_count(randomizer, [magic.Fire]))
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Fire]))

            self.assertEqual(3, self._starting_count(randomizer, [magic.Blizzard]))
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Blizzard]))

            self.assertEqual(3, self._starting_count(randomizer, [magic.Thunder]))
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Thunder]))

            self.assertEqual(3, self._starting_count(randomizer, [magic.Cure]))
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Cure]))

            self.assertEqual(3, self._starting_count(randomizer, [magic.Magnet]))
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Magnet]))

            self.assertEqual(3, self._starting_count(randomizer, [magic.Reflect]))
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Reflect]))

    def test_starting_magic_random_all(self):
        """ Verifies that all magic is given if the min random is equal to the number of magics. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.STARTING_MAGIC_FIRE, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_BLIZZARD, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_THUNDER, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_CURE, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_MAGNET, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_REFLECT, 0)
        seed_settings.set(settingkey.STARTING_MAGIC_RANDOM_MIN, 18)
        seed_settings.set(settingkey.STARTING_MAGIC_RANDOM_MAX, 18)

        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(3, self._starting_count(randomizer, [magic.Fire]))
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Fire]))

            self.assertEqual(3, self._starting_count(randomizer, [magic.Blizzard]))
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Blizzard]))

            self.assertEqual(3, self._starting_count(randomizer, [magic.Thunder]))
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Thunder]))

            self.assertEqual(3, self._starting_count(randomizer, [magic.Cure]))
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Cure]))

            self.assertEqual(3, self._starting_count(randomizer, [magic.Magnet]))
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Magnet]))

            self.assertEqual(3, self._starting_count(randomizer, [magic.Reflect]))
            self.assertEqual(0, self._assignment_count(randomizer, [magic.Reflect]))

    @staticmethod
    def _assignment_count(randomizer: Randomizer, items: list[InventoryItem]) -> int:
        count = 0
        for item in items:
            for assignment in randomizer.assignments:
                if assignment.location.name() == stt.CheckLocation.StruggleLoserMedal:
                    # The winner and loser should have the same item, but only count it once
                    continue
                if assignment.item.item == item:
                    count = count + 1
                if assignment.item2 is not None and assignment.item2.item == item:
                    count = count + 1
        return count

    @staticmethod
    def _starting_count(randomizer: Randomizer, items: list[InventoryItem]) -> int:
        count = 0
        for item in items:
            for starting_item_id in randomizer.starting_item_ids:
                if starting_item_id == item.id:
                    count = count + 1
        return count

    @staticmethod
    def _shop_count(randomizer: Randomizer, items: list[InventoryItem]) -> int:
        count = 0
        for item in items:
            for shop_item in randomizer.shop_items:
                if shop_item.item == item:
                    count = count + 1
        return count

    @staticmethod
    def _clear_unlock_settings(settings: SeedSettings):
        settings.set(settingkey.STARTING_UNLOCKS_SP, 0)
        settings.set(settingkey.STARTING_UNLOCKS_PR, 0)
        settings.set(settingkey.STARTING_UNLOCKS_TT, 0)
        settings.set(settingkey.STARTING_UNLOCKS_OC, 0)
        settings.set(settingkey.STARTING_UNLOCKS_HT, 0)
        settings.set(settingkey.STARTING_UNLOCKS_LOD, 0)
        settings.set(settingkey.STARTING_UNLOCKS_TWTNW, 0)
        settings.set(settingkey.STARTING_UNLOCKS_BC, 0)
        settings.set(settingkey.STARTING_UNLOCKS_AG, 0)
        settings.set(settingkey.STARTING_UNLOCKS_PL, 0)
        settings.set(settingkey.STARTING_UNLOCKS_HB, 0)
        settings.set(settingkey.STARTING_UNLOCKS_DC, 0)
        settings.set(settingkey.STARTING_UNLOCKS_STT, 0)
        settings.set(settingkey.STARTING_VISIT_RANDOM_MIN, 0)
        settings.set(settingkey.STARTING_VISIT_RANDOM_MAX, 0)

    @staticmethod
    def _start_with_all_unlocks(settings: SeedSettings):
        settings.set(settingkey.STARTING_UNLOCKS_SP, storyunlock.IdentityDisk.visit_count)
        settings.set(settingkey.STARTING_UNLOCKS_PR, storyunlock.SkillAndCrossbones.visit_count)
        settings.set(settingkey.STARTING_UNLOCKS_TT, storyunlock.IceCream.visit_count)
        settings.set(settingkey.STARTING_UNLOCKS_OC, storyunlock.BattlefieldsOfWar.visit_count)
        settings.set(settingkey.STARTING_UNLOCKS_HT, storyunlock.BoneFist.visit_count)
        settings.set(settingkey.STARTING_UNLOCKS_LOD, storyunlock.SwordOfTheAncestor.visit_count)
        settings.set(settingkey.STARTING_UNLOCKS_TWTNW, storyunlock.WayToTheDawn.visit_count)
        settings.set(settingkey.STARTING_UNLOCKS_BC, storyunlock.BeastsClaw.visit_count)
        settings.set(settingkey.STARTING_UNLOCKS_AG, storyunlock.Scimitar.visit_count)
        settings.set(settingkey.STARTING_UNLOCKS_PL, storyunlock.ProudFang.visit_count)
        settings.set(settingkey.STARTING_UNLOCKS_HB, storyunlock.MembershipCard.visit_count)
        settings.set(settingkey.STARTING_UNLOCKS_DC, storyunlock.RoyalSummons.visit_count)
        settings.set(settingkey.STARTING_UNLOCKS_STT, storyunlock.NaminesSketches.visit_count)
        settings.set(settingkey.STARTING_VISIT_RANDOM_MIN, 0)
        settings.set(settingkey.STARTING_VISIT_RANDOM_MAX, 0)


if __name__ == '__main__':
    unittest.main()

import unittest

from Class import settingkey
from Class.seedSettings import SeedSettings
from List.inventory import ability, misc, proof, report, storyunlock
from List.inventory.item import InventoryItem
from List.location import simulatedtwilighttown as stt
from Module.newRandomize import Randomizer
from seedtests import seedtest


class Tests(unittest.TestCase):

    def test_no_starting_abilities(self):
        """ Verifies that potential starting abilities have the appropriate counts when starting with none. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.STARTING_INVENTORY, [])

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
            settingkey.STARTING_INVENTORY,
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
        seed_settings.set(settingkey.STARTING_INVENTORY, [])
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
            settingkey.STARTING_INVENTORY,
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
        seed_settings.set(settingkey.STARTING_STORY_UNLOCKS, [])
        seed_settings.set(settingkey.SHOP_UNLOCKS, 0)

        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.BattlefieldsOfWar]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.BattlefieldsOfWar]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.BattlefieldsOfWar]))

            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.SwordOfTheAncestor]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.SwordOfTheAncestor]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.SwordOfTheAncestor]))

            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.BeastsClaw]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.BeastsClaw]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.BeastsClaw]))

            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.BoneFist]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.BoneFist]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.BoneFist]))

            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.ProudFang]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.ProudFang]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.ProudFang]))

            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.SkillAndCrossbones]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.SkillAndCrossbones]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.SkillAndCrossbones]))

            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.Scimitar]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.Scimitar]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.Scimitar]))

            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.IdentityDisk]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.IdentityDisk]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.IdentityDisk]))

            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.MembershipCard]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.MembershipCard]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.MembershipCard]))

            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.IceCream]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.IceCream]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.IceCream]))

            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.Picture]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.Picture]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.Picture]))

    def test_starting_unlocks(self):
        """ Verifies that starting unlocks have the appropriate counts when starting with some and none in the shop. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.STARTING_STORY_UNLOCKS, [storyunlock.Picture.id, storyunlock.IceCream.id])
        seed_settings.set(settingkey.SHOP_UNLOCKS, 0)

        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.BattlefieldsOfWar]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.BattlefieldsOfWar]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.BattlefieldsOfWar]))

            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.SwordOfTheAncestor]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.SwordOfTheAncestor]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.SwordOfTheAncestor]))

            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.BeastsClaw]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.BeastsClaw]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.BeastsClaw]))

            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.BoneFist]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.BoneFist]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.BoneFist]))

            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.ProudFang]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.ProudFang]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.ProudFang]))

            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.SkillAndCrossbones]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.SkillAndCrossbones]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.SkillAndCrossbones]))

            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.Scimitar]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.Scimitar]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.Scimitar]))

            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.IdentityDisk]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.IdentityDisk]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.IdentityDisk]))

            self.assertEqual(0, self._starting_count(randomizer, [storyunlock.MembershipCard]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.MembershipCard]))
            self.assertEqual(1, self._assignment_count(randomizer, [storyunlock.MembershipCard]))

            self.assertEqual(1, self._starting_count(randomizer, [storyunlock.IceCream]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.IceCream]))
            self.assertEqual(0, self._assignment_count(randomizer, [storyunlock.IceCream]))

            self.assertEqual(1, self._starting_count(randomizer, [storyunlock.Picture]))
            self.assertEqual(0, self._shop_count(randomizer, [storyunlock.Picture]))
            self.assertEqual(0, self._assignment_count(randomizer, [storyunlock.Picture]))

    def test_shop_unlocks(self):
        """ Verifies that starting unlocks have the appropriate counts when starting with none and some in the shop. """
        seed_settings = SeedSettings()
        seed_settings.set(settingkey.STARTING_STORY_UNLOCKS, [])
        seed_settings.set(settingkey.SHOP_UNLOCKS, 3)

        all_unlocks = storyunlock.all_story_unlocks()
        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(0, self._starting_count(randomizer, all_unlocks))
            self.assertEqual(3, self._shop_count(randomizer, all_unlocks))
            self.assertEqual(8, self._assignment_count(randomizer, all_unlocks))

    def test_start_and_shop_unlocks(self):
        """ Verifies that starting unlocks have the appropriate counts when starting with some and some in the shop. """
        seed_settings = SeedSettings()
        seed_settings.set(
            settingkey.STARTING_STORY_UNLOCKS,
            [storyunlock.BoneFist.id, storyunlock.SkillAndCrossbones.id]
        )
        seed_settings.set(settingkey.SHOP_UNLOCKS, 3)

        all_unlocks = storyunlock.all_story_unlocks()
        for randomizer in seedtest.test_seeds(seed_settings):
            self.assertEqual(2, self._starting_count(randomizer, all_unlocks))
            self.assertEqual(3, self._shop_count(randomizer, all_unlocks))
            self.assertEqual(6, self._assignment_count(randomizer, all_unlocks))

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


if __name__ == '__main__':
    unittest.main()

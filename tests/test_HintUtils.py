import unittest

from List.configDict import locationType
from List.inventory import magic, misc, form, ability, summon, storyunlock
from Module.Hints.HintUtils import HintUtils


class Tests(unittest.TestCase):

    def test_item_to_vanilla_world(self):
        """
        Verifies that item_to_vanilla_world is behaving as expected.
        """
        lookup = HintUtils.item_to_vanilla_world()

        self.assertEqual(
            {locationType.HB, locationType.Agrabah, locationType.PL},
            set(lookup[magic.Fire])
        )
        self.assertEqual(
            {locationType.HB, locationType.Atlantica},
            set(lookup[magic.Blizzard])
        )
        self.assertEqual(
            {locationType.OC, locationType.LoD, locationType.PL},
            set(lookup[magic.Thunder])
        )
        self.assertEqual(
            {locationType.HUNDREDAW, locationType.BC, locationType.HB},
            set(lookup[magic.Cure])
        )
        self.assertEqual(
            {locationType.TWTNW, locationType.PR, locationType.HT},
            set(lookup[magic.Magnet])
        )
        self.assertEqual(
            {locationType.DC, locationType.SP, locationType.BC},
            set(lookup[magic.Reflect])
        )
        self.assertEqual(
            {
                locationType.HB, locationType.Agrabah, locationType.PL,
                locationType.DC, locationType.LoD, locationType.HUNDREDAW
            },
            set(lookup[misc.TornPages])
        )
        self.assertEqual(
            {locationType.TT, locationType.STT, locationType.FormLevel},
            set(lookup[form.ValorForm])
        )
        self.assertEqual(
            {locationType.DC, locationType.FormLevel},
            set(lookup[form.WisdomForm])
        )
        self.assertEqual(
            {locationType.TT, locationType.STT, locationType.FormLevel},
            set(lookup[form.LimitForm])
        )
        self.assertEqual(
            {locationType.HB, locationType.FormLevel},
            set(lookup[form.MasterForm])
        )
        self.assertEqual({locationType.FormLevel}, set(lookup[form.FinalForm]))
        self.assertEqual({locationType.Level}, set(lookup[ability.OnceMore]))
        self.assertEqual({locationType.Level}, set(lookup[ability.SecondChance]))
        self.assertEqual({locationType.HB}, set(lookup[summon.BaseballCharm]))
        self.assertEqual({locationType.HB}, set(lookup[summon.UkuleleCharm]))
        self.assertEqual({locationType.Agrabah}, set(lookup[summon.LampCharm]))
        self.assertEqual({locationType.PR}, set(lookup[summon.FeatherCharm]))
        self.assertEqual({locationType.BC}, set(lookup[storyunlock.BeastsClaw]))
        self.assertEqual({locationType.HT}, set(lookup[storyunlock.BoneFist]))
        self.assertEqual({locationType.PL}, set(lookup[storyunlock.ProudFang]))
        self.assertEqual({locationType.OC}, set(lookup[storyunlock.BattlefieldsOfWar]))
        self.assertEqual({locationType.LoD}, set(lookup[storyunlock.SwordOfTheAncestor]))
        self.assertEqual({locationType.PR}, set(lookup[storyunlock.SkillAndCrossbones]))
        self.assertEqual({locationType.Agrabah}, set(lookup[storyunlock.Scimitar]))
        self.assertEqual({locationType.SP}, set(lookup[storyunlock.IdentityDisk]))
        self.assertEqual({locationType.HB}, set(lookup[storyunlock.MembershipCard]))
        self.assertEqual({locationType.TT}, set(lookup[storyunlock.Picture]))
        self.assertEqual({locationType.TT}, set(lookup[storyunlock.IceCream]))


if __name__ == '__main__':
    unittest.main()

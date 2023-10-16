import unittest

from List.ChestList import chest_visual_id
from List.configDict import locationType, itemType


class ChestVisualTests(unittest.TestCase):
    item_types = [itemType.SYNTH, itemType.GROWTH_ABILITY, itemType.ACTION_ABILITY, itemType.SUPPORT_ABILITY, itemType.FORM, itemType.FIRE, itemType.BLIZZARD, itemType.THUNDER, itemType.CURE, itemType.MAGNET, itemType.REFLECT, itemType.TORN_PAGE, itemType.REPORT, itemType.GAUGE, itemType.SLOT, itemType.MUNNY_POUCH,
                  itemType.SUMMON, itemType.STORYUNLOCK, itemType.MANUFACTORYUNLOCK, itemType.TROPHY, itemType.OCSTONE, itemType.KEYBLADE, itemType.SHIELD, itemType.STAFF, itemType.ACCESSORY, itemType.ARMOR, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE, itemType.PROOF_OF_NONEXISTENCE, itemType.PROMISE_CHARM]

    default_chest_ids = [4000, 4001, 4001, 4001, 4002, 4003, 4003, 4003, 4003, 4003, 4003, 4004, 4005,
                         4006, 4006, 4006, 4007, 4008, 4008, 4008, 4008, 4009, 4009, 4009, 4009, 4009, 4010, 4010, 4010, 4010]
    twilight_town_chest_ids = [4020, 4021, 4021, 4021, 4022, 4023, 4023, 4023, 4023, 4023, 4023, 4024, 4025,
                               4026, 4026, 4026, 4027, 4028, 4028, 4028, 4028, 4029, 4029, 4029, 4029, 4029, 4030, 4030, 4030, 4030]
    pride_lands_chest_ids = [4040, 4041, 4041, 4041, 4042, 4043, 4043, 4043, 4043, 4043, 4043, 4044, 4045,
                             4046, 4046, 4046, 4047, 4048, 4048, 4048, 4048, 4049, 4049, 4049, 4049, 4049, 4050, 4050, 4050, 4050]

    def test_default_world_chest_visuals(self):
        for index, i_type in enumerate(ChestVisualTests.item_types):
            self.assertEqual(ChestVisualTests.default_chest_ids[index], chest_visual_id(
                [locationType.BC], i_type))
            self.assertEqual(ChestVisualTests.default_chest_ids[index], chest_visual_id(
                [locationType.Agrabah], i_type))

    def test_pl_world_chest_visuals(self):
        for index, i_type in enumerate(ChestVisualTests.item_types):
            self.assertEqual(ChestVisualTests.pride_lands_chest_ids[index], chest_visual_id(
                [locationType.PL], i_type))

    def test_default_world_chest_visuals(self):
        for index, i_type in enumerate(ChestVisualTests.item_types):
            self.assertEqual(ChestVisualTests.twilight_town_chest_ids[index], chest_visual_id(
                [locationType.TT], i_type))
        for index, i_type in enumerate(ChestVisualTests.item_types):
            self.assertEqual(ChestVisualTests.twilight_town_chest_ids[index], chest_visual_id(
                [locationType.STT], i_type))


if __name__ == '__main__':
    unittest.main()

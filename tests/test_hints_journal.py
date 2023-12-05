import unittest

from Class.itemClass import KH2Item
from Class.newLocationClass import KH2Location
from List.configDict import locationCategory, locationType
from List.inventory import ability, keyblade, form
from List.location import weaponslot
from Module.hints import Hints

keyblade_locations_by_id = {location.LocationId: location for location in weaponslot.keyblade_slots()}


class Tests(unittest.TestCase):

    def test_kingdom_key_specific(self):
        """
        Kingdom Key should always be skipped for journal hints.
        """
        location = keyblade_locations_by_id[weaponslot.LocationId.KingdomKey]
        item = KH2Item(ability.Explosion)
        location_item_data: list[tuple[KH2Location, KH2Item]] = [(location, item)]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=True)
        self.assertIsNone(hint)

    def test_kingdom_key_world(self):
        """
        Kingdom Key should always be skipped for journal hints.
        """
        location = keyblade_locations_by_id[weaponslot.LocationId.KingdomKey]
        item = KH2Item(ability.Explosion)
        location_item_data: list[tuple[KH2Location, KH2Item]] = [(location, item)]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=False)
        self.assertIsNone(hint)

    def test_form_key_specific(self):
        """
        Journal hints will only say what form keyblade has the ability. It's not going to inform you where that form is,
        by design.
        """
        location = keyblade_locations_by_id[weaponslot.LocationId.AlphaWeapon]
        item = KH2Item(ability.AerialSpiral)
        master_location = KH2Location(10001, "Test Location", locationCategory.CHEST, [locationType.BC])
        location_item_data: list[tuple[KH2Location, KH2Item]] = [
            (location, item),
            (master_location, KH2Item(form.MasterForm)),
        ]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=True)
        self.assertEqual("Aerial Spiral is on Master Form's Keyblade.", hint)

    def test_form_key_world(self):
        """
        Journal hints will only say what form keyblade has the ability. It's not going to inform you where that form is,
        by design.
        """
        location = keyblade_locations_by_id[weaponslot.LocationId.AlphaWeapon]
        item = KH2Item(ability.AerialSpiral)
        master_location = KH2Location(10001, "Test Location", locationCategory.CHEST, [locationType.BC])
        location_item_data: list[tuple[KH2Location, KH2Item]] = [
            (location, item),
            (master_location, KH2Item(form.MasterForm)),
        ]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=False)
        self.assertEqual("Aerial Spiral is on Master Form's Keyblade.", hint)

    def test_other_key_specific(self):
        """
        Reveal the specific location of the keyblade with the ability.
        """
        location = keyblade_locations_by_id[weaponslot.LocationId.BondOfFlame]
        item = KH2Item(ability.AerialDive)
        key_location = KH2Location(10001, "Test Location", locationCategory.CHEST, [locationType.TWTNW])
        location_item_data: list[tuple[KH2Location, KH2Item]] = [
            (location, item),
            (key_location, KH2Item(keyblade.BondOfFlame)),
        ]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=True)
        self.assertEqual("Aerial Dive is at TWTNW - Test Location (on Bond of Flame).", hint)

    def test_other_key_world(self):
        """
        Reveal the world containing the keyblade with the ability.
        """
        location = keyblade_locations_by_id[weaponslot.LocationId.BondOfFlame]
        item = KH2Item(ability.AerialDive)
        key_location = KH2Location(10001, "Test Location", locationCategory.CHEST, [locationType.TWTNW])
        location_item_data: list[tuple[KH2Location, KH2Item]] = [
            (location, item),
            (key_location, KH2Item(keyblade.BondOfFlame)),
        ]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=False)
        self.assertEqual("Aerial Dive is in TWTNW (on Bond of Flame).", hint)

    def test_other_key_level_specific(self):
        """
        Reveal the specific location of the keyblade with the ability.
        """
        location = keyblade_locations_by_id[weaponslot.LocationId.Oblivion]
        item = KH2Item(ability.SlideDash)
        key_location = KH2Location(10001, "Level 44", locationCategory.LEVEL, [locationType.Level])
        location_item_data: list[tuple[KH2Location, KH2Item]] = [
            (location, item),
            (key_location, KH2Item(keyblade.Oblivion)),
        ]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=True)
        self.assertEqual("Slide Dash is at Sora's Heart - Level 44 (on Oblivion).", hint)

    def test_other_key_level_world(self):
        """
        Reveal the world containing the keyblade with the ability.
        """
        location = keyblade_locations_by_id[weaponslot.LocationId.Oblivion]
        item = KH2Item(ability.SlideDash)
        key_location = KH2Location(10001, "Level 44", locationCategory.LEVEL, [locationType.Level])
        location_item_data: list[tuple[KH2Location, KH2Item]] = [
            (location, item),
            (key_location, KH2Item(keyblade.Oblivion)),
        ]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=False)
        self.assertEqual("Slide Dash is in Sora's Heart (on Oblivion).", hint)

    def test_other_key_form_level_specific(self):
        """
        Reveal the specific location of the keyblade with the ability.
        """
        location = keyblade_locations_by_id[weaponslot.LocationId.Oathkeeper]
        item = KH2Item(ability.ExperienceBoost)
        key_location = KH2Location(10001, "Master Level 5", locationCategory.MASTERLEVEL, [locationType.FormLevel])
        location_item_data: list[tuple[KH2Location, KH2Item]] = [
            (location, item),
            (key_location, KH2Item(keyblade.Oathkeeper)),
        ]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=True)
        self.assertEqual("Experience Boost is at Form Levels - Master Level 5 (on Oathkeeper).", hint)

    def test_other_key_form_level_world(self):
        """
        Reveal the world containing the keyblade with the ability.
        """
        location = keyblade_locations_by_id[weaponslot.LocationId.Oathkeeper]
        item = KH2Item(ability.ExperienceBoost)
        key_location = KH2Location(10001, "Master Level 5", locationCategory.MASTERLEVEL, [locationType.FormLevel])
        location_item_data: list[tuple[KH2Location, KH2Item]] = [
            (location, item),
            (key_location, KH2Item(keyblade.Oathkeeper)),
        ]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=False)
        self.assertEqual("Experience Boost is in Form Levels (on Oathkeeper).", hint)

    def test_other_key_specific_unhintable(self):
        """
        No hint if the location is not in the hintable worlds list.
        """
        location = keyblade_locations_by_id[weaponslot.LocationId.StarSeeker]
        item = KH2Item(ability.AerialRecovery)
        key_location = KH2Location(10001, "Test Location", locationCategory.CREATION, [locationType.Puzzle])
        location_item_data: list[tuple[KH2Location, KH2Item]] = [
            (location, item),
            (key_location, KH2Item(keyblade.StarSeeker)),
        ]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=True)
        self.assertIsNone(hint)

    def test_other_key_world_unhintable(self):
        """
        No hint if the location is not in the hintable worlds list.
        """
        location = keyblade_locations_by_id[weaponslot.LocationId.StarSeeker]
        item = KH2Item(ability.AerialRecovery)
        key_location = KH2Location(10001, "Test Location", locationCategory.CREATION, [locationType.Puzzle])
        location_item_data: list[tuple[KH2Location, KH2Item]] = [
            (location, item),
            (key_location, KH2Item(keyblade.StarSeeker)),
        ]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=False)
        self.assertIsNone(hint)

    def test_misc_location_specific(self):
        location = KH2Location(10001, "Test Location", locationCategory.CHEST, [locationType.LoD])
        item = KH2Item(ability.GuardBreak)
        location_item_data: list[tuple[KH2Location, KH2Item]] = [(location, item)]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=True)
        self.assertEqual("Guard Break is at Land of Dragons - Test Location.", hint)

    def test_misc_location_world(self):
        location = KH2Location(10001, "Test Location", locationCategory.CHEST, [locationType.LoD])
        item = KH2Item(ability.GuardBreak)
        location_item_data: list[tuple[KH2Location, KH2Item]] = [(location, item)]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=False)
        self.assertEqual("Guard Break is in Land of Dragons.", hint)

    def test_misc_location_specific_unhintable(self):
        location = KH2Location(10001, "Test Location", locationCategory.CREATION, [locationType.Puzzle])
        item = KH2Item(ability.FlashStep)
        location_item_data: list[tuple[KH2Location, KH2Item]] = [(location, item)]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=True)
        self.assertIsNone(hint)

    def test_misc_location_world_unhintable(self):
        location = KH2Location(10001, "Test Location", locationCategory.CREATION, [locationType.Puzzle])
        item = KH2Item(ability.FlashStep)
        location_item_data: list[tuple[KH2Location, KH2Item]] = [(location, item)]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=False)
        self.assertIsNone(hint)

    def test_levels_specific(self):
        location = KH2Location(10001, "Level 50", locationCategory.LEVEL, [locationType.Level])
        item = KH2Item(ability.MagnetBurst)
        location_item_data: list[tuple[KH2Location, KH2Item]] = [(location, item)]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=True)
        self.assertEqual("Magnet Burst is at Sora's Heart - Level 50.", hint)

    def test_levels_world(self):
        location = KH2Location(10001, "Level 50", locationCategory.LEVEL, [locationType.Level])
        item = KH2Item(ability.MagnetBurst)
        location_item_data: list[tuple[KH2Location, KH2Item]] = [(location, item)]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=False)
        self.assertEqual("Magnet Burst is in Sora's Heart.", hint)

    def test_form_levels_specific(self):
        location = KH2Location(10001, "Valor Level 7", locationCategory.VALORLEVEL, [locationType.FormLevel])
        item = KH2Item(ability.Guard)
        location_item_data: list[tuple[KH2Location, KH2Item]] = [(location, item)]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=True)
        self.assertEqual("Guard is at Form Levels - Valor Level 7.", hint)

    def test_form_levels_world(self):
        location = KH2Location(10001, "Valor Level 7", locationCategory.VALORLEVEL, [locationType.FormLevel])
        item = KH2Item(ability.Guard)
        location_item_data: list[tuple[KH2Location, KH2Item]] = [(location, item)]
        hint = Hints.get_journal_hint(location, item, location_item_data, independent_hint_specific=False)
        self.assertEqual("Guard is in Form Levels.", hint)


if __name__ == '__main__':
    unittest.main()

import unittest

from Class.seedSettings import SeedSettings
from List.configDict import locationType, locationCategory, itemType
from seedtests import seedtest

_ability_types = [itemType.ACTION_ABILITY, itemType.SUPPORT_ABILITY, itemType.GROWTH_ABILITY]
_gauge_types = [itemType.GAUGE]


class Tests(unittest.TestCase):

    def test_no_abilities_on_popups(self):
        """ Verifies that no abilities are given on popup locations. """
        seed_settings = SeedSettings()
        for randomizer in seedtest.test_seeds(seed_settings):
            for assignment in randomizer.assignments:
                if assignment.location.LocationCategory == locationCategory.POPUP:
                    for item in assignment.items():
                        self.assertNotIn(item.ItemType, _ability_types)

    def test_no_gauges_on_popups(self):
        """ Verifies that no gauge increases are given on popup locations. """
        seed_settings = SeedSettings()
        for randomizer in seedtest.test_seeds(seed_settings):
            for assignment in randomizer.assignments:
                if assignment.location.LocationCategory == locationCategory.POPUP:
                    for item in assignment.items():
                        self.assertNotIn(item.ItemType, _gauge_types)

    def test_no_abilities_on_creations(self):
        """ Verifies that no abilities are given on creation locations. """
        seed_settings = SeedSettings()
        for randomizer in seedtest.test_seeds(seed_settings):
            for assignment in randomizer.assignments:
                if assignment.location.LocationCategory == locationCategory.CREATION:
                    for item in assignment.items():
                        self.assertNotIn(item.ItemType, _ability_types)

    def test_no_gauges_on_creations(self):
        """ Verifies that no gauge increases are given on creation locations. """
        seed_settings = SeedSettings()
        for randomizer in seedtest.test_seeds(seed_settings):
            for assignment in randomizer.assignments:
                location = assignment.location
                if location.LocationCategory == locationCategory.CREATION:
                    for item in assignment.items():
                        self.assertNotIn(item.ItemType, _gauge_types)

    def test_no_gauges_on_critical_bonuses(self):
        """ Verifies that no gauge increases are given on critical bonus locations. """
        seed_settings = SeedSettings()
        for randomizer in seedtest.test_seeds(seed_settings):
            for assignment in randomizer.assignments:
                location = assignment.location
                if locationType.Critical in location.LocationTypes:
                    for item in assignment.items():
                        self.assertNotIn(item.ItemType, _gauge_types)

    def test_gauges_in_stt(self):
        """ Verifies that gauge increases are not given in STT unless in a stat bonus location. """
        seed_settings = SeedSettings()
        for randomizer in seedtest.test_seeds(seed_settings):
            for assignment in randomizer.assignments:
                loc = assignment.location
                if locationType.STT in loc.LocationTypes and loc.LocationCategory != locationCategory.STATBONUS:
                    for item in assignment.items():
                        self.assertNotIn(item.ItemType, _gauge_types)


if __name__ == '__main__':
    unittest.main()

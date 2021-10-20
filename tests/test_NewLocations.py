
import sys
sys.path.append("..")
from List.NewLocationList import Locations
import unittest


class Tests(unittest.TestCase):
    def test_Locations(self):
        print(len(Locations.getAllSoraLocations()))

ut = Tests()

unittest.main()

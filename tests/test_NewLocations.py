
from Class.seedSettings import SeedSettings
from List.NewLocationList import Locations
from Module.RandomizerSettings import RandomizerSettings

import unittest



class Tests(unittest.TestCase):
    def test_allLocations(self):
        l = Locations(RandomizerSettings("test_name",True,"version",SeedSettings()))
        graph = l.location_graph
        locations = Tests.create_list_from_nodes(graph)
        self.assertEqual(len(locations),len(l.getAllSoraLocations()))
        self.assertEqual(len(l.getAllSoraLocations()),641)

    @staticmethod
    def create_list_from_nodes(graph):
        nodes = graph.node_list()
        locations = []
        for n in nodes:
            locations+=graph.node_data(n).locations
        return locations

if __name__ == '__main__':
    unittest.main()

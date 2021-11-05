
from List.NewLocationList import Locations
import unittest


class Tests(unittest.TestCase):
    def test_LocationsLoD(self):
        l = Locations()
        graph = l.getLoDGraph()
        locations = Tests.create_list_from_nodes(graph)
        self.assertEqual(len(l.LoD()),len(locations))

    def test_LocationsAG(self):
        l = Locations()
        graph = l.getAGGraph()
        locations = Tests.create_list_from_nodes(graph)
        self.assertEqual(len(l.AG()),len(locations))

    def test_LocationsDC(self):
        l = Locations()
        graph = l.getDCGraph()
        locations = Tests.create_list_from_nodes(graph)
        self.assertEqual(len(l.DC()),len(locations))

    def test_Locations100Acre(self):
        l = Locations()
        graph = l.get100AcreGraph()
        locations = Tests.create_list_from_nodes(graph)
        self.assertEqual(len(l.HundredAcre()),len(locations))

    def test_LocationsOC(self):
        l = Locations()
        graph = l.getOCGraph()
        locations = Tests.create_list_from_nodes(graph)
        self.assertEqual(len(l.OC()),len(locations))

    def test_LocationsBC(self):
        l = Locations()
        graph = l.getBCGraph()
        locations = Tests.create_list_from_nodes(graph)
        self.assertEqual(len(l.BC()),len(locations))

    def test_LocationsSP(self):
        l = Locations()
        graph = l.getSPGraph()
        locations = Tests.create_list_from_nodes(graph)
        self.assertEqual(len(l.SP()),len(locations))

    def test_LocationsHT(self):
        l = Locations()
        graph = l.getHTGraph()
        locations = Tests.create_list_from_nodes(graph)
        self.assertEqual(len(l.HT()),len(locations))

    def test_LocationsPR(self):
        l = Locations()
        graph = l.getPRGraph()
        locations = Tests.create_list_from_nodes(graph)
        self.assertEqual(len(l.PR()),len(locations))

    def test_LocationsHB(self):
        l = Locations()
        graph = l.getHBGraph()
        locations = Tests.create_list_from_nodes(graph)
        self.assertEqual(len(l.HB()),len(locations))

    def test_LocationsCoR(self):
        l = Locations()
        graph = l.getCoRGraph()
        locations = Tests.create_list_from_nodes(graph)
        self.assertEqual(len(l.CoR()),len(locations))

    def test_LocationsPL(self):
        l = Locations()
        graph = l.getPLGraph()
        locations = Tests.create_list_from_nodes(graph)
        self.assertEqual(len(l.PL()),len(locations))

    def test_LocationsSTT(self):
        l = Locations()
        graph = l.getSTTGraph()
        locations = Tests.create_list_from_nodes(graph)
        self.assertEqual(len(l.STT()),len(locations))

    def test_LocationsTT(self):
        l = Locations()
        graph = l.getTTGraph()
        locations = Tests.create_list_from_nodes(graph)
        self.assertEqual(len(l.TT()),len(locations))

    def test_LocationsTWTNW(self):
        l = Locations()
        graph = l.getTWTNWGraph()
        locations = Tests.create_list_from_nodes(graph)
        self.assertEqual(len(l.TWTNW()),len(locations))


    @staticmethod
    def create_list_from_nodes(graph):
        nodes = graph.node_list()
        locations = []
        for n in nodes:
            locations+=graph.node_data(n).locations
        return locations

if __name__ == '__main__':
    unittest.main()

from enum import Enum

from Class.newLocationClass import KH2Location
from List.configDict import locationType
from List.inventory import proof
from List.location.graph import chest, LocationGraphBuilder, START_NODE


class CheckLocation(str, Enum):
    GardenOfAssemblageMap = "Garden of Assemblage Map"
    GoaLostIllusion = "GoA Lost Illusion"
    ProofOfNonexistence = "Proof of Nonexistence"


def make_graph(graph: LocationGraphBuilder):
    locations = [chest(i, f"Starting Item {i}", locationType.Critical) for i in range(1, 8)]
    locations.append(chest(585, CheckLocation.GardenOfAssemblageMap, locationType.Free))
    locations.append(chest(586, CheckLocation.GoaLostIllusion, locationType.Free))
    locations.append(
        chest(590, CheckLocation.ProofOfNonexistence, locationType.Free, vanilla=proof.ProofOfNonexistence))

    graph.add_location(START_NODE, locations)


def donald_starting_items() -> list[KH2Location]:
    return [chest(i, f"Donald Starting Item {i}", locationType.Free) for i in range(1, 3)]


def goofy_starting_items() -> list[KH2Location]:
    return [chest(i, f"Goofy Starting Item {i}", locationType.Free) for i in range(1, 3)]

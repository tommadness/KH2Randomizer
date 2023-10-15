from Class.newLocationClass import KH2Location
from List.configDict import locationCategory, locationType
from List.location.graph import LocationGraphBuilder, START_NODE


def summon_level(level: int) -> KH2Location:
    return KH2Location(level, f"Summon Level {level}", locationCategory.SUMMONLEVEL, [locationType.SummonLevel])


def make_graph(graph: LocationGraphBuilder):
    locations: dict[int, str] = {}
    for level in range(1, 8):
        locations[level] = graph.add_location(f"Summon-{level}", [
            summon_level(level)
        ])

    graph.add_edge(START_NODE, locations[1])
    for level in range(2, 8):
        graph.add_edge(locations[level - 1], locations[level])

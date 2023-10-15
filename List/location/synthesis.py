from enum import Enum

from Class.newLocationClass import KH2Location
from List.configDict import locationType, itemType, locationCategory
from List.location.graph import LocationGraphBuilder, START_NODE


class NodeId(str, Enum):
    FreeDev1 = "Synthesis Free Dev 1"
    FreeDev1Part2 = "Synthesis Free Dev 1 Part 2"
    FreeDev1Part3 = "Synthesis Free Dev 1 Part 3"
    FreeDev2 = "Synthesis Free Dev 2"
    FreeDev2Part2 = "Synthesis Free Dev 2 Part 2"
    FreeDev2Part3 = "Synthesis Free Dev 2 Part 3"


def synth_recipe(recipe: int) -> KH2Location:
    return KH2Location(
        LocationId=recipe - 1,
        Description=f"Synth Recipe {recipe}",
        LocationCategory=locationCategory.CREATION,
        LocationTypes=[locationType.SYNTH],
        InvalidChecks=[itemType.RECIPE, itemType.REPORT]
    )


def make_graph(graph: LocationGraphBuilder):
    free_dev_1 = graph.add_location(NodeId.FreeDev1, [
        synth_recipe(recipe) for recipe in range(1, 6)
    ])
    free_dev_1_part_2 = graph.add_location(NodeId.FreeDev1Part2, [
        synth_recipe(recipe) for recipe in range(6, 11)
    ])
    free_dev_1_part_3 = graph.add_location(NodeId.FreeDev1Part3, [
        synth_recipe(recipe) for recipe in range(11, 16)
    ])
    free_dev_2 = graph.add_location(NodeId.FreeDev2, [
        synth_recipe(recipe) for recipe in range(16, 21)
    ])
    free_dev_2_part_2 = graph.add_location(NodeId.FreeDev2Part2, [
        synth_recipe(recipe) for recipe in range(21, 26)
    ])
    free_dev_2_part_3 = graph.add_location(NodeId.FreeDev2Part3, [
        synth_recipe(recipe) for recipe in range(26, 31)
    ])

    graph.add_edge(START_NODE, free_dev_1)
    graph.add_edge(free_dev_1, free_dev_1_part_2)
    graph.add_edge(free_dev_1_part_2, free_dev_1_part_3)
    graph.add_edge(free_dev_1_part_3, free_dev_2)
    graph.add_edge(free_dev_2, free_dev_2_part_2)
    graph.add_edge(free_dev_2_part_2, free_dev_2_part_3)

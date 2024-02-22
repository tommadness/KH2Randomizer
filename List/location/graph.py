from enum import Enum
from typing import Optional, Union, Callable

from altgraph.Graph import Graph

from Class.exceptions import GeneratorException
from Class.newLocationClass import KH2Location
from List.configDict import locationType, itemType, locationCategory
from List.inventory.item import InventoryItem
from Module.RandomizerSettings import RandomizerSettings

RequirementFunction = Callable[[list[int]], bool]


START_NODE = "Starting"


class DefaultLogicGraph:
    def __init__(self, node_ids : Enum = None):
        # makes a dictionary of all unique ordered pairs
        self.logic = {}
        self.logic[START_NODE] = {}
        if node_ids is not None:
            for i in list(node_ids):
                self.logic[START_NODE][i] = lambda inv : True
                self.logic[i] = {}
                for j in list(node_ids):
                    if i!=j:
                        self.logic[i][j] = lambda inv : True
        
    def has_rule(self,node1,node2):
        if node1 in self.logic and node2 in self.logic[node1]:
            return True
        return False

    def merge(self, other: 'DefaultLogicGraph'):
        for start_node, out_edges in other.logic.items():
            if start_node not in self.logic:
                self.logic[start_node] = {}
            for end_node, rule in out_edges.items():
                self.logic[start_node][end_node] = rule

class LocationNode:

    def __init__(self, in_loc: Optional[list[KH2Location]] = None):
        if in_loc is None:
            self.locations = []
        else:
            self.locations = in_loc


class RequirementEdge:

    def __init__(self, req: Optional[RequirementFunction] = None, strict=True, battle=False):
        self.requirement = req
        self.strict = strict
        self.battle = battle


class LocationGraphBuilder:

    def __init__(self, graph: Graph, reverse_rando: bool, settings: RandomizerSettings):
        self.graph = graph
        self.first_visit_locks = False
        self.reverse_rando = reverse_rando
        self.settings = settings
        self.logic_graph = DefaultLogicGraph()
        self.pending_locations_by_name: dict[str, KH2Location] = {}
        self.pending_first_boss_nodes: list[str] = []
        self.pending_last_story_boss_nodes: list[str] = []
        self.pending_superboss_nodes: list[str] = []
    
    def add_logic(self,added_logic_graph : DefaultLogicGraph):
        self.logic_graph.merge(added_logic_graph)

    def add_location(self, name: str, locations: list[KH2Location]) -> str:
        self.graph.add_node(name, LocationNode(locations))
        for location in locations:
            location_name = location.name()
            if location_name in self.pending_locations_by_name:
                raise GeneratorException(f"Location {location_name} is already in the graph")
            else:
                self.pending_locations_by_name[location_name] = location
        return name

    def add_edge(self, node1: str, node2: str, requirement: Optional[RequirementEdge] = None):
        if requirement is None:
            requirement = RequirementEdge()
        if self.logic_graph.has_rule(node1,node2) and requirement.requirement is None:
            requirement.requirement = self.logic_graph.logic[node1][node2]
        self.graph.add_edge(node1, node2, requirement)

    def register_first_boss(self, node: str):
        self.pending_first_boss_nodes.append(node)

    def register_last_story_boss(self, node: str):
        self.pending_last_story_boss_nodes.append(node)

    def register_superboss(self, node: str):
        self.pending_superboss_nodes.append(node)


def _make_location(
        loc_id: int,
        description: str,
        category: locationCategory,
        loc_types: Union[locationType, list[locationType]],
        invalid_checks: Optional[list[itemType]] = None,
        vanilla: Optional[Union[InventoryItem, list[InventoryItem]]] = None
) -> KH2Location:
    if isinstance(loc_types, locationType):
        loc_types = [loc_types]
    if invalid_checks is None:
        invalid_checks = []
    vanilla_items: list[int] = []
    if vanilla is not None:
        if isinstance(vanilla, InventoryItem):
            vanilla_items.append(vanilla.id)
        else:
            for item in vanilla:
                vanilla_items.append(item.id)
    return KH2Location(loc_id, description, category, loc_types, invalid_checks, vanilla_items)


def chest(
        loc_id: int,
        description: str,
        loc_types: Union[locationType, list[locationType]],
        invalid_checks: Optional[list[itemType]] = None,
        vanilla: Optional[Union[InventoryItem, list[InventoryItem]]] = None
) -> KH2Location:
    return _make_location(loc_id, description, locationCategory.CHEST, loc_types, invalid_checks, vanilla)


def popup(
        loc_id: int,
        description: str,
        loc_types: Union[locationType, list[locationType]],
        invalid_checks: Optional[list[itemType]] = None,
        vanilla: Optional[Union[InventoryItem, list[InventoryItem]]] = None
) -> KH2Location:
    return _make_location(loc_id, description, locationCategory.POPUP, loc_types, invalid_checks, vanilla)


def item_bonus(
        loc_id: int,
        description: str,
        loc_types: Union[locationType, list[locationType]],
        invalid_checks: Optional[list[itemType]] = None,
        vanilla: Optional[Union[InventoryItem, list[InventoryItem]]] = None
) -> KH2Location:
    return _make_location(loc_id, description, locationCategory.ITEMBONUS, loc_types, invalid_checks, vanilla)


def stat_bonus(
        loc_id: int,
        description: str,
        loc_types: Union[locationType, list[locationType]],
        invalid_checks: Optional[list[itemType]] = None,
        vanilla: Optional[Union[InventoryItem, list[InventoryItem]]] = None
) -> KH2Location:
    return _make_location(loc_id, description, locationCategory.STATBONUS, loc_types, invalid_checks, vanilla)


def hybrid_bonus(
        loc_id: int,
        description: str,
        loc_types: Union[locationType, list[locationType]],
        invalid_checks: Optional[list[itemType]] = None,
        vanilla: Optional[Union[InventoryItem, list[InventoryItem]]] = None
) -> KH2Location:
    return _make_location(loc_id, description, locationCategory.HYBRIDBONUS, loc_types, invalid_checks, vanilla)


def double_bonus(
        loc_id: int,
        description: str,
        loc_types: Union[locationType, list[locationType]],
        invalid_checks: Optional[list[itemType]] = None,
        vanilla: Optional[Union[InventoryItem, list[InventoryItem]]] = None
) -> KH2Location:
    return _make_location(loc_id, description, locationCategory.DOUBLEBONUS, loc_types, invalid_checks, vanilla)

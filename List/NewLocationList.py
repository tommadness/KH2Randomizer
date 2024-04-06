from typing import Iterator, List, Optional

from altgraph.Graph import Graph

from Class.newLocationClass import KH2Location
from List.configDict import locationCategory
from List.location import landofdragons, spaceparanoids, weaponslot, donaldbonus, goofybonus, starting, formlevel, \
    summonlevel, agrabah, disneycastle, hundredacrewood, olympuscoliseum, beastscastle, halloweentown, portroyal, \
    hollowbastion, pridelands, simulatedtwilighttown, twilighttown, worldthatneverwas, atlantica, synthesis, \
    puzzlereward, soralevel
from List.location.graph import LocationGraphBuilder, START_NODE, RequirementEdge, RequirementFunction
from Module.RandomizerSettings import RandomizerSettings


# updated function to allow for multiple incoming connections to enforce multiple constraints
def get_all_parent_edge_requirements(
        node_id: str,
        graph: Graph
) -> RequirementFunction:
    # base_requirement = lambda inv : True
    non_strict_requirements = []
    strict_requirements = []

    for edge in graph.inc_edges(node_id):
        # we want to collate the parent requirements in the proper arrangement. 
        #   If we have non-strict edges, only one of the parent edges is needed to enter this node.
        source, _ = graph.edge_by_id(edge)
        parent_requirements = get_all_parent_edge_requirements(source, graph)
        # if debug_mode:
        #     parent_requirements([])
        data: RequirementEdge = graph.edge_data(edge)
        # condition to get to here through this parent
        if data.requirement is not None:
            requirement = lambda inv, this_req=data.requirement, par_req=parent_requirements : this_req(inv) and par_req(inv)
        else:
            requirement = lambda inv, par_req=parent_requirements: par_req(inv)
        if data.strict:
            strict_requirements.append(requirement)
        else:
            non_strict_requirements.append(requirement)
    if len(non_strict_requirements) > 0:
        #convert the non-strict requirements into a strict with with an or condition
        new_strict_func = lambda inv, non_s_req=non_strict_requirements: any([r(inv) for r in non_s_req])
        strict_requirements.append(new_strict_func)
    this_requirement = lambda inv, s_req=strict_requirements : all([r(inv) for r in s_req])
    return this_requirement


class Locations:

    def __init__(self, settings: RandomizerSettings, secondary_graph: bool = False):
        self.location_graph = Graph()
        self.reverse_rando = secondary_graph
        self.locations_by_name: dict[str, KH2Location] = {}
        self.first_boss_nodes: list[str] = []
        self.last_story_boss_nodes: list[str] = []
        self.superboss_nodes: list[str] = []
        self.make_location_graph(settings)

    def _all_locations_iter(self) -> Iterator[KH2Location]:
        graph = self.location_graph
        for node_id in graph.nodes.keys():
            node_data = graph.node_data(node_id)
            for location in node_data.locations:
                yield location

    def _common_ancestor(self, node_id) -> List[KH2Location]:
        result = [node_id]
        current_node = node_id
        graph = self.location_graph

        while True:
            in_nbrs = graph.inc_nbrs(current_node)
            assert len(in_nbrs)==1
            current_node = in_nbrs[0]
            result.append(current_node)
            if current_node==START_NODE:
                break
            # check all out edges
            bfs_search = [current_node]
            while len(bfs_search):
                bfs_node = bfs_search.pop(0)
                out_nbrs = graph.out_nbrs(bfs_node)
                for o in out_nbrs:
                    if o not in result:
                        bfs_search.append(o)
                        result.append(o)

        return result

    def node_ids(self) -> list[str]:
        """ Returns a list of all the node IDs in the graph. """
        return self.location_graph.node_list()

    def node_ids_before(self, node_id: str, include_self: bool = False, include_starting: bool = False) -> list[str]:
        """
        Returns a list of all node IDs that come before the given node_id. Additional argument(s) can be given to
        control whether the given node_id itself is included in the returned list, as well as the starting node.
        """
        result = []
        ancestors = self._common_ancestor(node_id)
        for before_node_id in ancestors:
            if node_id == before_node_id and not include_self:
                continue
            if before_node_id == START_NODE and not include_starting:
                continue
            result.append(before_node_id)
        return result

    def node_ids_after(self, node_id: str, include_self: bool = False) -> list[str]:
        """
        Returns a list of all node IDs that come after the given node_id. An additional argument can be given to
        control whether the given node_id itself is included in the returned list.
        """
        result = []
        for after_node_id in self.location_graph.forw_bfs(node_id):
            if node_id == after_node_id and not include_self:
                continue
            result.append(after_node_id)
        return result

    def locations_for_node(self, node_id: str) -> list[KH2Location]:
        """ Returns a list of the locations for the given node ID. """
        return self.location_graph.node_data(node_id).locations

    def locations_for_category(self, category: locationCategory) -> list[KH2Location]:
        """ Returns all locations whose category matches the input category. """
        return [location for location in self._all_locations_iter() if category == location.LocationCategory]

    def all_locations(self) -> list[KH2Location]:
        """ Returns a list of all the locations in the graph. """
        result = []
        for node_id in self.node_ids():
            result.extend(self.locations_for_node(node_id))
        return result

    def locations_before(
            self,
            node_id: str,
            include_self: bool = False,
            include_starting_node: bool = False
    ) -> list[KH2Location]:
        """
        Returns a list of all locations that come before the given node_id. Additional argument(s) can be given to
        control whether locations for the given node_id itself are included in the returned list, as well as the
        starting node.
        """
        result = []
        for before_node_id in self.node_ids_before(node_id, include_self, include_starting_node):
            result.extend(self.locations_for_node(before_node_id))
        return result

    def locations_after(self, node_id: str, include_self: bool = False) -> list[KH2Location]:
        """
        Returns a list of all locations that come after the given node_id. An additional argument can be given to
        control whether locations for the given node_id itself are included in the returned list.
        """
        result = []
        for after_node_id in self.node_ids_after(node_id, include_self):
            result.extend(self.locations_for_node(after_node_id))
        return result

    @staticmethod
    def all_donald_locations() -> list[KH2Location]:
        return donaldbonus.donald_bonuses() + weaponslot.donald_staff_slots() + starting.donald_starting_items()

    @staticmethod
    def all_goofy_locations() -> list[KH2Location]:
        return goofybonus.goofy_bonuses() + weaponslot.goofy_shield_slots() + starting.goofy_starting_items()

    def make_location_graph(self, settings: RandomizerSettings):
        builder = LocationGraphBuilder(self.location_graph, self.reverse_rando, settings)

        starting.make_graph(builder)
        simulatedtwilighttown.make_graph(builder)
        twilighttown.make_graph(builder)
        hollowbastion.make_graph(builder)
        landofdragons.make_graph(builder)
        beastscastle.make_graph(builder)
        olympuscoliseum.make_graph(builder)
        disneycastle.make_graph(builder)
        portroyal.make_graph(builder)
        agrabah.make_graph(builder)
        halloweentown.make_graph(builder)
        pridelands.make_graph(builder)
        spaceparanoids.make_graph(builder)
        worldthatneverwas.make_graph(builder)
        hundredacrewood.make_graph(builder)
        atlantica.make_graph(builder)
        soralevel.make_graph(builder)
        formlevel.make_graph(builder)
        summonlevel.make_graph(builder)
        synthesis.make_graph(builder)
        puzzlereward.make_graph(builder)

        for name, location in builder.pending_locations_by_name.items():
            self.locations_by_name[name] = location
        self.first_boss_nodes.extend(builder.pending_first_boss_nodes)
        self.last_story_boss_nodes.extend(builder.pending_last_story_boss_nodes)
        self.superboss_nodes.extend(builder.pending_superboss_nodes)

        # from altgraph.Dot import Dot
        # dot = Dot(self.location_graph)
        # dot.style(rankdir="LR")
        # if self.reverse_rando:
        #     dot.save_img(file_name='reverse_graph',file_type="gif")
        # else:
        #     dot.save_img(file_name='graph',file_type="gif")

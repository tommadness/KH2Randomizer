from Class.exceptions import SettingsException
from Class.newLocationClass import KH2Location
from List.NewLocationList import Locations
from List.configDict import locationCategory, locationDepth


class ItemDepths:

    def __init__(self, location_depth: locationDepth, locations: Locations):
        self.location_depth = location_depth
        self.depth_classification: dict[KH2Location, bool] = {}
        self.very_restricted_locations = location_depth in [
            locationDepth.FirstBoss,
            locationDepth.LastStoryBoss,
            locationDepth.Superbosses
        ]

        if location_depth is locationDepth.Anywhere:
            self._set_all_initial_values(locations, True)
        elif location_depth is locationDepth.FirstVisit:
            self._apply_first_visit(locations)
        elif location_depth is locationDepth.NonSuperboss:
            self._apply_non_superboss(locations)
        elif location_depth is locationDepth.FirstBoss:
            self._apply_boss_depth(locations, locations.first_boss_nodes)
        elif location_depth is locationDepth.SecondVisitOnly:
            self._apply_second_visit_only(locations)
        elif location_depth is locationDepth.LastStoryBoss:
            self._apply_boss_depth(locations, locations.last_story_boss_nodes)
        elif location_depth is locationDepth.Superbosses:
            self._apply_boss_depth(locations, locations.superboss_nodes)
        elif location_depth is locationDepth.NoFirstVisit:
            self._apply_non_first_visit(locations)
        else:
            raise SettingsException(f"Invalid location depth {location_depth}")

    def is_valid(self, location: KH2Location):
        return self.depth_classification[location]

    def _set_all_initial_values(self, locations: Locations, classification: bool):
        """ Marks all locations with the given classification initially. """
        for location in locations.all_locations():
            self.depth_classification[location] = classification

    def _apply_boss_depth(self, locations: Locations, boss_node_ids: list[str]):
        """
        Marks all nodes invalid, then marks _exactly one_ location valid in each of the given boss nodes.
        This by design in any of the boss depth modes to try to spread the items out more evenly among the bosses.
        """
        self._set_all_initial_values(locations, False)
        for node_id in boss_node_ids:
            preferred_location = self.preferred_boss_location(locations.locations_for_node(node_id))
            self.depth_classification[preferred_location] = True

    def _apply_first_visit(self, locations: Locations):
        # Default to no, enable before and including first boss
        self._set_all_initial_values(locations, False)
        for first_boss_node in locations.first_boss_nodes:
            for location in locations.locations_before(first_boss_node, include_self=True):
                self.depth_classification[location] = True

    def _apply_non_superboss(self, locations: Locations):
        # Default to yes, disable superbosses
        self._set_all_initial_values(locations, True)
        for superboss_node in locations.superboss_nodes:
            for location in locations.locations_for_node(superboss_node):
                self.depth_classification[location] = False

    def _apply_second_visit_only(self, locations: Locations):
        # Default to no, enable all after first boss (excluding superbosses)
        self._set_all_initial_values(locations, False)
        for first_boss_node in locations.first_boss_nodes:
            # In worlds where the first boss is the same as the last story boss, there is effectively no "second visit"
            if first_boss_node in locations.last_story_boss_nodes:
                continue
            for after_node in locations.node_ids_after(first_boss_node, include_self=False):
                if after_node not in locations.superboss_nodes:
                    for location in locations.locations_for_node(after_node):
                        self.depth_classification[location] = True

    def _apply_non_first_visit(self, locations: Locations):
        # Default to yes, disable before and including first boss
        self._set_all_initial_values(locations, True)
        for first_boss_node in locations.first_boss_nodes:
            for location in locations.locations_before(first_boss_node, include_self=True):
                self.depth_classification[location] = False

    @staticmethod
    def preferred_boss_location(locations: list[KH2Location]) -> KH2Location:
        # Try to find a popup location. If no popups, just prefer the first location.
        popup = next((loc for loc in locations if loc.LocationCategory is locationCategory.POPUP), None)
        return popup if popup is not None else locations[0]

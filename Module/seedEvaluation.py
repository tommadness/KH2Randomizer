
import copy

from Class.exceptions import ValidationException
from Class.newLocationClass import KH2Location
from List.NewLocationList import get_all_parent_edge_requirements, Locations
from List.configDict import ItemAccessibilityOption, locationType
from List.inventory import proof
from List.location import simulatedtwilighttown as stt
from List.location import worldthatneverwas as twtnw
from List.location.graph import RequirementFunction
from Module.RandomizerSettings import RandomizerSettings
from Module.itemPlacementRestriction import ItemPlacementHelpers
from Module.newRandomize import Randomizer, SynthesisRecipe


class ValidationResult:

    def __init__(self):
        self.any_percent = False
        self.full_clear = False


class LocationInformedSeedValidator:

    def __init__(self):
        self.location_requirements: dict[KH2Location, list[RequirementFunction]] = {}

    @staticmethod
    def evaluate(inventory: list[int], reqs_list: list[RequirementFunction]) -> bool:
        return all([r(inventory) for r in reqs_list])

    def is_location_available(self, inventory: list[int], location: KH2Location) -> bool:
        return self.evaluate(inventory, self.location_requirements[location])

    def prepare_requirements_list(self, location_lists: list[Locations], synthesis_recipes: list[SynthesisRecipe]):
        self.location_requirements.clear()
        for locations in location_lists:
            for node_id in locations.node_ids():
                parent_requirement_function = get_all_parent_edge_requirements(node_id, locations.location_graph)
                for location in locations.locations_for_node(node_id):
                    if location not in self.location_requirements:
                        self.location_requirements[location] = []
                    self.location_requirements[location].append(parent_requirement_function)

        for loc, requirements in self.location_requirements.items():
            if locationType.SYNTH in loc.LocationTypes:
                # this is a synth location, we need to get its recipe to know what locks it logically
                recipe = next((r for r in synthesis_recipes if r.location == loc), None)
                # if we don't have recipes yet, we can't validate that yet
                if recipe:
                    for recipe_requirement in recipe.requirements:
                        synth_item = recipe_requirement.synth_item
                        # now that we know what synth item is in the recipe, we can determine what to add to the logic
                        requirements.append(ItemPlacementHelpers.make_synth_requirement(synth_item))

    def prep_requirements_list(self, settings: RandomizerSettings, randomizer: Randomizer):
        location_lists = []
        if settings.regular_rando:
            location_lists.append(randomizer.regular_locations)
        if settings.reverse_rando:
            location_lists.append(randomizer.reverse_locations)
        self.prepare_requirements_list(location_lists, randomizer.synthesis_recipes)

    def validate_seed(
            self,
            settings: RandomizerSettings,
            randomizer: Randomizer,
            verbose: bool = True
    ) -> list[KH2Location]:
        self.prep_requirements_list(settings, randomizer)

        location_requirements = copy.deepcopy(self.location_requirements)

        results = ValidationResult()
        inventory = [item_id for item_id in randomizer.starting_item_ids]
        if len(randomizer.shop_items) > 0:
            for shop_item in randomizer.shop_items:
                inventory.append(shop_item.Id)

        changed = True
        depth = 0
        while changed:
            depth += 1
            final_xem_in_list = False
            if not results.any_percent:
                for location, requirements in location_requirements.items():
                    if location.name() == twtnw.CheckLocation.FinalXemnas:
                        final_xem_in_list = True
                        break
                if not final_xem_in_list:
                    results.any_percent = True

            if len(location_requirements) == 0:
                if verbose:
                    print(f"Logic Depth {depth}")
                results.full_clear = True
                break

            changed = False
            locations_to_remove = []
            for location, requirements in location_requirements.items():
                if self.evaluate(inventory, requirements):
                    # find assigned item to location
                    for assignment in randomizer.assignments:
                        # if assignment is one of the struggle win/lose items, only count one, and not count the second.
                        if assignment.location.name() == stt.CheckLocation.StruggleWinnerChampionBelt:
                            continue
                        if location == assignment.location:
                            inventory.append(assignment.item.Id)
                            if assignment.item2 is not None:
                                inventory.append(assignment.item2.Id)
                            break
                    locations_to_remove.append(location)
                    changed = True
            for shop_item in locations_to_remove:
                location_requirements.pop(shop_item)

        if (settings.item_accessibility == ItemAccessibilityOption.ALL and results.full_clear) \
                or (settings.item_accessibility == ItemAccessibilityOption.BEATABLE and results.any_percent):
            # we all good
            print(f"Unreachable locations {len(location_requirements)}")
            return [i for i in location_requirements.keys()]
        else:
            if verbose:
                print("Failed seed, trying again")
            
            # print(inventory)
            # for loc_req in location_requirements.items():
            #     print(loc_req[0].Description)
            #     for assignment in randomizer.assignments:
            #         if loc_req[0] == assignment.location:
            #             print(f"---{assignment.item.Name}")
            raise ValidationException(f"Completion checking failed to collect {len(location_requirements)} items")

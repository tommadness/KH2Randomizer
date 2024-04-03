

import random
from altgraph.Graph import Graph
import copy
import itertools

from Class.exceptions import ValidationException
from Class.itemClass import KH2Item
from Class.newLocationClass import KH2Location
from List.NewLocationList import get_all_parent_edge_requirements, Locations
from List.configDict import ItemAccessibilityOption, locationType
from List.inventory import storyunlock, keyblade, proof, form, magic, misc
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
        self.human_readable_lock_list: dict[locationType,Graph] = {}

    def populate_possible_locking_item_list(self, regular_rando: bool):
        # STT
        stt_graph = Graph()
        stt_graph.add_node("STT",[storyunlock.NaminesSketches])
        stt_graph.add_node("STTChests",[keyblade.BondOfFlame])
        stt_graph.add_edge("STT","STTChests")
        self.human_readable_lock_list[locationType.STT] = stt_graph
        # HB
        hb_graph = Graph()
        hb_graph.add_node("HB1",[storyunlock.MembershipCard])
        hb_graph.add_node("HBChests",[keyblade.SleepingLion])
        hb_graph.add_node("HB2",[storyunlock.MembershipCard,storyunlock.MembershipCard])
        hb_graph.add_node("CoR",[keyblade.WinnersProof])
        hb_graph.add_node("PoP",[proof.ProofOfPeace])
        hb_graph.add_edge("HB1","HBChests")
        hb_graph.add_edge("HB1","HB2")
        hb_graph.add_edge("HB2","HBChests")
        hb_graph.add_edge("HBChests","HB2")
        hb_graph.add_edge("HB2","CoR")
        hb_graph.add_edge("HB2","PoP")
        hb_graph.add_edge("CoR","PoP")
        hb_graph.add_edge("PoP","CoR")
        self.human_readable_lock_list[locationType.HB] = hb_graph
        # OC
        oc_graph = Graph()
        oc_graph.add_node("OC1",[storyunlock.BattlefieldsOfWar])
        oc_graph.add_node("OCChests",[keyblade.HerosCrest])
        oc_graph.add_node("OC2",[storyunlock.BattlefieldsOfWar,storyunlock.BattlefieldsOfWar])
        oc_graph.add_edge("OC1","OCChests")
        oc_graph.add_edge("OC1","OC2")
        oc_graph.add_edge("OC2","OCChests")
        oc_graph.add_edge("OCChests","OC2")
        self.human_readable_lock_list[locationType.OC] = oc_graph
        # LoD
        lod_graph = Graph()
        lod_graph.add_node("LoD1",[storyunlock.SwordOfTheAncestor])
        lod_graph.add_node("LoDChests",[keyblade.HiddenDragon])
        lod_graph.add_node("LoD2",[storyunlock.SwordOfTheAncestor,storyunlock.SwordOfTheAncestor])
        lod_graph.add_edge("LoD1","LoDChests")
        lod_graph.add_edge("LoD1","LoD2")
        lod_graph.add_edge("LoD2","LoDChests")
        lod_graph.add_edge("LoDChests","LoD2")
        self.human_readable_lock_list[locationType.LoD] = lod_graph
        # PL
        pl_graph = Graph()
        pl_graph.add_node("PL1",[storyunlock.ProudFang])
        pl_graph.add_node("PLChests",[keyblade.CircleOfLife])
        pl_graph.add_node("PL2",[storyunlock.ProudFang,storyunlock.ProudFang])
        pl_graph.add_edge("PL1","PLChests")
        pl_graph.add_edge("PL1","PL2")
        pl_graph.add_edge("PL2","PLChests")
        pl_graph.add_edge("PLChests","PL2")
        self.human_readable_lock_list[locationType.PL] = pl_graph
        # HT
        ht_graph = Graph()
        ht_graph.add_node("HT1",[storyunlock.BoneFist])
        ht_graph.add_node("HTChests",[keyblade.DecisivePumpkin])
        ht_graph.add_node("HT2",[storyunlock.BoneFist,storyunlock.BoneFist])
        ht_graph.add_edge("HT1","HTChests")
        ht_graph.add_edge("HT1","HT2")
        ht_graph.add_edge("HT2","HTChests")
        ht_graph.add_edge("HTChests","HT2")
        self.human_readable_lock_list[locationType.HT] = ht_graph
        # SP
        sp_graph = Graph()
        sp_graph.add_node("SP1",[storyunlock.IdentityDisk])
        sp_graph.add_node("SPChests",[keyblade.PhotonDebugger])
        sp_graph.add_node("SP2",[storyunlock.IdentityDisk,storyunlock.IdentityDisk])
        sp_graph.add_edge("SP1","SPChests")
        sp_graph.add_edge("SP1","SP2")
        sp_graph.add_edge("SP2","SPChests")
        sp_graph.add_edge("SPChests","SP2")
        self.human_readable_lock_list[locationType.HT] = sp_graph
        # Drives
        drive_graph = Graph()
        drive_graph.add_node("Valor",[form.ValorForm])
        drive_graph.add_node("Wisdom",[form.WisdomForm])
        drive_graph.add_node("Limit",[form.LimitForm])
        drive_graph.add_node("Master",[form.MasterForm])
        drive_graph.add_node("Final",[form.FinalForm])
        for n in drive_graph.node_list():
            for m in drive_graph.node_list():
                if n is not m:
                    drive_graph.add_edge(n,m)
        self.human_readable_lock_list[locationType.FormLevel] = drive_graph
        # TT
        tt_graph = Graph()
        tt_graph.add_node("TT1",[storyunlock.IceCream])
        tt_graph.add_node("TT2",[storyunlock.IceCream,storyunlock.IceCream])
        tt_graph.add_node("TT3",[storyunlock.IceCream,storyunlock.IceCream,storyunlock.IceCream])
        tt_graph.add_node("TTChests",[keyblade.Oathkeeper])
        tt_graph.add_edge("TT1","TT2")
        tt_graph.add_edge("TT2","TT3")
        tt_graph.add_edge("TT1","TTChests")
        tt_graph.add_edge("TT2","TTChests")
        tt_graph.add_edge("TT3","TTChests")
        tt_graph.add_edge("TTChests","TT2")
        tt_graph.add_edge("TTChests","TT3")
        self.human_readable_lock_list[locationType.TT] = tt_graph
        # BC
        bc_graph = Graph()
        bc_graph.add_node("BC1",[storyunlock.BeastsClaw])
        bc_graph.add_node("BCChests",[keyblade.RumblingRose])
        bc_graph.add_node("BC2",[storyunlock.BeastsClaw,storyunlock.BeastsClaw])
        bc_graph.add_edge("BC1","BCChests")
        bc_graph.add_edge("BC1","BC2")
        bc_graph.add_edge("BC2","BCChests")
        bc_graph.add_edge("BCChests","BC2")
        self.human_readable_lock_list[locationType.BC] = bc_graph
        # HAW
        haw_graph = Graph()
        haw_graph.add_node("Page1",[misc.TornPages])
        haw_graph.add_node("Page2",[misc.TornPages,misc.TornPages])
        haw_graph.add_node("Page3",[misc.TornPages,misc.TornPages,misc.TornPages])
        haw_graph.add_node("Page4",[misc.TornPages,misc.TornPages,misc.TornPages,misc.TornPages])
        haw_graph.add_node("Page5",[misc.TornPages,misc.TornPages,misc.TornPages,misc.TornPages,misc.TornPages])
        haw_graph.add_node("PoohChests",[keyblade.SweetMemories])
        haw_graph.add_edge("PoohChests","Page1")
        haw_graph.add_edge("Page1","Page2")
        haw_graph.add_edge("Page2","Page3")
        haw_graph.add_edge("Page3","Page4")
        haw_graph.add_edge("Page4","Page5")
        self.human_readable_lock_list[locationType.HUNDREDAW] = haw_graph
        # DC
        dc_graph = Graph()
        dc_graph.add_node("DC1",[storyunlock.DisneyCastleKey])
        dc_graph.add_node("DCChests",[keyblade.Monochrome])
        dc_graph.add_node("DC2",[storyunlock.DisneyCastleKey,storyunlock.DisneyCastleKey])
        dc_graph.add_node("PoC",[proof.ProofOfConnection])
        dc_graph.add_edge("DC1","DCChests")
        dc_graph.add_edge("DC1","DC2")
        dc_graph.add_edge("DC2","DCChests")
        dc_graph.add_edge("DC2","PoC")
        dc_graph.add_edge("DCChests","DC2")
        dc_graph.add_edge("DCChests","PoC")
        self.human_readable_lock_list[locationType.DC] = dc_graph
        # PR
        pr_graph = Graph()
        pr_graph.add_node("PR1",[storyunlock.SkillAndCrossbones])
        pr_graph.add_node("PRChests",[keyblade.FollowTheWind])
        pr_graph.add_node("PR2",[storyunlock.SkillAndCrossbones,storyunlock.SkillAndCrossbones])
        pr_graph.add_edge("PR1","PRChests")
        pr_graph.add_edge("PR1","PR2")
        pr_graph.add_edge("PR2","PRChests")
        pr_graph.add_edge("PRChests","PR2")
        self.human_readable_lock_list[locationType.PR] = pr_graph
        # TWTNW
        twtnw_graph = Graph()
        twtnw_graph.add_node("TWTNW1",[storyunlock.WayToTheDawn])
        twtnw_graph.add_node("TWTNWChests",[keyblade.TwoBecomeOne])
        twtnw_graph.add_node("TWTNW2",[storyunlock.WayToTheDawn,storyunlock.WayToTheDawn])
        twtnw_graph.add_edge("TWTNW1","TWTNWChests")
        twtnw_graph.add_edge("TWTNW1","TWTNW2")
        twtnw_graph.add_edge("TWTNW2","TWTNWChests")
        twtnw_graph.add_edge("TWTNWChests","TWTNW2")
        self.human_readable_lock_list[locationType.TWTNW] = twtnw_graph
        # Atlantica
        atlantica_graph = Graph()
        atlantica_graph.add_node("Song2",[magic.Magnet])
        atlantica_graph.add_node("Song4",[magic.Magnet,magic.Magnet])
        atlantica_graph.add_node("Song5",[magic.Magnet,magic.Magnet,magic.Thunder,magic.Thunder,magic.Thunder])
        atlantica_graph.add_edge("Song2","Song4")
        atlantica_graph.add_edge("Song4","Song5")
        self.human_readable_lock_list[locationType.Atlantica] = atlantica_graph
        # AG
        if regular_rando:
            ag_graph = Graph()
            ag_graph.add_node("AG1",[storyunlock.Scimitar])
            ag_graph.add_node("AG2",[storyunlock.Scimitar,storyunlock.Scimitar,magic.Fire,magic.Blizzard,magic.Thunder])
            ag_graph.add_node("AGChests",[keyblade.WishingLamp])
            ag_graph.add_edge("AG1","AG2")
            ag_graph.add_edge("AG1","AGChests")
            ag_graph.add_edge("AG2","AGChests")
            ag_graph.add_edge("AGChests","AG2")
            self.human_readable_lock_list[locationType.Agrabah] = ag_graph
        else:
            ag_graph = Graph()
            ag_graph.add_node("AG1",[storyunlock.Scimitar]) # there are no first visit checks in reverse without the key
            ag_graph.add_node("AG1.5",[magic.Fire,magic.Blizzard,magic.Thunder])
            ag_graph.add_node("AG2",[storyunlock.Scimitar,storyunlock.Scimitar])
            ag_graph.add_node("AGChests",[storyunlock.Scimitar,keyblade.WishingLamp])
            ag_graph.add_edge("AG1","AG1.5")
            ag_graph.add_edge("AG1.5","AG2")
            ag_graph.add_edge("AG1","AGChests")
            ag_graph.add_edge("AG1.5","AGChests")
            ag_graph.add_edge("AG2","AGChests")
            ag_graph.add_edge("AGChests","AG1.5")
            ag_graph.add_edge("AGChests","AG2")
            self.human_readable_lock_list[locationType.Agrabah] = ag_graph

    def generate_locking_item_ids(self):
        def random_walk(graph: Graph):
            current_node_list = []
            current_item_data = []
            current_node = next((n for n in graph.node_list() if graph.inc_degree(n)==0),None)
            if current_node is None:
                # if there is no obvious start node, pick one at random
                current_node = random.choice(graph.node_list())

            while True:
                # populate the data for the current node
                current_node_list.append(current_node)
                current_item_data.append(graph.node_data(current_node))
                # find out edge nodes that we haven't traversed yet
                candidate_nodes = [n for n in graph.out_nbrs(current_node) if n not in current_node_list]
                if len(candidate_nodes)==0:
                    break
                current_node = random.choice(candidate_nodes)
                # repeat
            return current_item_data


        item_id_lock_list: dict[locationType,list[list[int]]] = {}
        for location_type,lock_graph in self.human_readable_lock_list.items():
            # convert this from graph to randomly ordered item id list
            random_ordered_requirements = random_walk(lock_graph)

            new_list = []
            for lock_item_list in random_ordered_requirements:
                new_list.append([])
                for lock_item in lock_item_list:
                    new_list[-1].append(lock_item.id)
            item_id_lock_list[location_type] = new_list
        return item_id_lock_list

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
        self.populate_possible_locking_item_list(settings.regular_rando)

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
            if verbose:
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

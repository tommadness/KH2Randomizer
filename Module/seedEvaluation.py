import copy
import random

from altgraph.Graph import Graph

from Class.exceptions import ValidationException
from Class.newLocationClass import KH2Location
from List.NewLocationList import get_all_parent_edge_requirements, Locations
from List.configDict import ItemAccessibilityOption, locationType
from List.inventory import storyunlock, keyblade, proof, form, magic, misc
from List.inventory.misc import NullItem
from List.location import (
    agrabah as ag,
    atlantica as at,
    beastscastle as bc,
    disneycastle as dc,
    halloweentown as ht,
    hollowbastion as hb,
    hundredacrewood as haw,
    landofdragons as lod,
    olympuscoliseum as oc,
    portroyal as pr,
    pridelands as pl,
    simulatedtwilighttown as stt,
    spaceparanoids as sp,
    twilighttown as tt,
    worldthatneverwas as twtnw,
    formlevel,
    starting,
)
from List.location.graph import RequirementFunction
from Module.RandomizerSettings import RandomizerSettings
from Module.itemPlacementRestriction import ItemPlacementHelpers
from Module.newRandomize import Randomizer, SynthesisRecipe
from Module.resources import resource_path


class ValidationResult:

    def __init__(self):
        self.any_percent = False
        self.full_clear = False


class LocationInformedSeedValidator:

    def __init__(self):
        self.location_requirements: dict[KH2Location, list[RequirementFunction]] = {}
        self.human_readable_lock_list: dict[locationType,Graph] = {}
        self.location_spheres: dict[KH2Location, int] = {}

    def populate_possible_locking_item_list(self, regular_rando: bool, keyblade_locking: bool):
        # STT
        stt_graph = Graph()
        stt_graph.add_node("STT",[storyunlock.NaminesSketches])
        stt_graph.add_node("STTChests",[keyblade.BondOfFlame])
        stt_graph.add_edge("STT","STTChests")
        self.human_readable_lock_list[locationType.STT] = stt_graph
        # HB
        hb_graph = Graph()
        hb_graph.add_node("HB1",[storyunlock.MembershipCard])
        hb_graph.add_node("HB2",[storyunlock.MembershipCard,storyunlock.MembershipCard])
        hb_graph.add_edge("HB1","HB2")
        if keyblade_locking:
            hb_graph.add_node("HBChests",[keyblade.SleepingLion])
            hb_graph.add_node("CoR",[keyblade.WinnersProof])
            hb_graph.add_edge("HBChests","HB2")
            hb_graph.add_edge("HBChests","CoR")
            hb_graph.add_edge("CoR","HBChests")
            hb_graph.add_edge("HB1","HBChests")
            hb_graph.add_edge("HB2","HBChests")
            hb_graph.add_edge("HB2","CoR")
        if regular_rando:
            hb_graph.add_node("PoP",[proof.ProofOfPeace])
            hb_graph.add_edge("HB2","PoP")
            if keyblade_locking:
                hb_graph.add_edge("PoP","HBChests")
                hb_graph.add_edge("CoR","PoP")
                hb_graph.add_edge("PoP","CoR")
        self.human_readable_lock_list[locationType.HB] = hb_graph
        # OC
        oc_graph = Graph()
        oc_graph.add_node("OC1",[storyunlock.BattlefieldsOfWar])
        oc_graph.add_node("OC2",[storyunlock.BattlefieldsOfWar,storyunlock.BattlefieldsOfWar])
        oc_graph.add_edge("OC1","OC2")
        if keyblade_locking:
            oc_graph.add_node("OCChests",[keyblade.HerosCrest])
            oc_graph.add_edge("OC1","OCChests")
            oc_graph.add_edge("OC2","OCChests")
            oc_graph.add_edge("OCChests","OC2")
        self.human_readable_lock_list[locationType.OC] = oc_graph
        # LoD
        lod_graph = Graph()
        lod_graph.add_node("LoD1",[storyunlock.SwordOfTheAncestor])
        lod_graph.add_node("LoD2",[storyunlock.SwordOfTheAncestor,storyunlock.SwordOfTheAncestor])
        lod_graph.add_edge("LoD1","LoD2")
        if keyblade_locking:
            lod_graph.add_node("LoDChests",[keyblade.HiddenDragon])
            lod_graph.add_edge("LoD1","LoDChests")
            lod_graph.add_edge("LoD2","LoDChests")
            lod_graph.add_edge("LoDChests","LoD2")
        self.human_readable_lock_list[locationType.LoD] = lod_graph
        # PL
        pl_graph = Graph()
        pl_graph.add_node("PL1",[storyunlock.ProudFang])
        pl_graph.add_node("PL2",[storyunlock.ProudFang,storyunlock.ProudFang])
        pl_graph.add_edge("PL1","PL2")
        if keyblade_locking:
            pl_graph.add_node("PLChests",[keyblade.CircleOfLife])
            pl_graph.add_edge("PL1","PLChests")
            pl_graph.add_edge("PL2","PLChests")
            pl_graph.add_edge("PLChests","PL2")
        self.human_readable_lock_list[locationType.PL] = pl_graph
        # HT
        ht_graph = Graph()
        ht_graph.add_node("HT1",[storyunlock.BoneFist])
        ht_graph.add_node("HT2",[storyunlock.BoneFist,storyunlock.BoneFist])
        ht_graph.add_edge("HT1","HT2")
        if keyblade_locking:
            ht_graph.add_node("HTChests",[keyblade.DecisivePumpkin])
            ht_graph.add_edge("HT1","HTChests")
            ht_graph.add_edge("HT2","HTChests")
            ht_graph.add_edge("HTChests","HT2")
        self.human_readable_lock_list[locationType.HT] = ht_graph
        # SP
        sp_graph = Graph()
        sp_graph.add_node("SP1",[storyunlock.IdentityDisk])
        sp_graph.add_node("SP2",[storyunlock.IdentityDisk,storyunlock.IdentityDisk])
        sp_graph.add_edge("SP1","SP2")
        if keyblade_locking:
            sp_graph.add_node("SPChests",[keyblade.PhotonDebugger])
            sp_graph.add_edge("SP1","SPChests")
            sp_graph.add_edge("SP2","SPChests")
            sp_graph.add_edge("SPChests","SP2")
        self.human_readable_lock_list[locationType.SP] = sp_graph
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
        tt_graph.add_edge("TT1","TT2")
        tt_graph.add_edge("TT2","TT3")
        if keyblade_locking:
            tt_graph.add_node("TTChests",[keyblade.Oathkeeper])
            tt_graph.add_edge("TT1","TTChests")
            tt_graph.add_edge("TT2","TTChests")
            tt_graph.add_edge("TT3","TTChests")
            tt_graph.add_edge("TTChests","TT2")
            tt_graph.add_edge("TTChests","TT3")
        self.human_readable_lock_list[locationType.TT] = tt_graph
        # BC
        bc_graph = Graph()
        bc_graph.add_node("BC1",[storyunlock.BeastsClaw])
        bc_graph.add_node("BC2",[storyunlock.BeastsClaw,storyunlock.BeastsClaw])
        bc_graph.add_edge("BC1","BC2")
        if keyblade_locking:
            bc_graph.add_node("BCChests",[keyblade.RumblingRose])
            bc_graph.add_edge("BC1","BCChests")
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
        if keyblade_locking:
            haw_graph.add_node("PoohChests",[keyblade.SweetMemories])
            haw_graph.add_edge("PoohChests","Page1")
        haw_graph.add_edge("Page1","Page2")
        haw_graph.add_edge("Page2","Page3")
        haw_graph.add_edge("Page3","Page4")
        haw_graph.add_edge("Page4","Page5")
        self.human_readable_lock_list[locationType.HUNDREDAW] = haw_graph
        # DC
        dc_graph = Graph()
        dc_graph.add_node("DC1", [storyunlock.RoyalSummons])
        dc_graph.add_node("DC2", [storyunlock.RoyalSummons, storyunlock.RoyalSummons])
        dc_graph.add_node("PoC",[proof.ProofOfConnection])
        dc_graph.add_edge("DC1","DC2")
        dc_graph.add_edge("DC2","PoC")
        if keyblade_locking:
            dc_graph.add_node("DCChests",[keyblade.Monochrome])
            dc_graph.add_edge("DC1","DCChests")
            dc_graph.add_edge("DC2","DCChests")
            dc_graph.add_edge("DCChests","DC2")
            dc_graph.add_edge("DCChests","PoC")
        self.human_readable_lock_list[locationType.DC] = dc_graph
        # PR
        pr_graph = Graph()
        pr_graph.add_node("PR1",[storyunlock.SkillAndCrossbones])
        pr_graph.add_node("PR2",[storyunlock.SkillAndCrossbones,storyunlock.SkillAndCrossbones])
        pr_graph.add_edge("PR1","PR2")
        if keyblade_locking:
            pr_graph.add_node("PRChests",[keyblade.FollowTheWind])
            pr_graph.add_edge("PR1","PRChests")
            pr_graph.add_edge("PR2","PRChests")
            pr_graph.add_edge("PRChests","PR2")
        self.human_readable_lock_list[locationType.PR] = pr_graph
        # TWTNW
        twtnw_graph = Graph()
        twtnw_graph.add_node("TWTNW1",[storyunlock.WayToTheDawn])
        twtnw_graph.add_node("TWTNW2",[storyunlock.WayToTheDawn,storyunlock.WayToTheDawn])
        twtnw_graph.add_edge("TWTNW1","TWTNW2")
        if keyblade_locking:
            twtnw_graph.add_node("TWTNWChests",[keyblade.TwoBecomeOne])
            twtnw_graph.add_edge("TWTNW1","TWTNWChests")
            twtnw_graph.add_edge("TWTNW2","TWTNWChests")
            twtnw_graph.add_edge("TWTNWChests","TWTNW2")
        self.human_readable_lock_list[locationType.TWTNW] = twtnw_graph
        # Atlantica
        atlantica_graph = Graph()
        atlantica_graph.add_node("Song4",[magic.Magnet,magic.Magnet])
        atlantica_graph.add_node("Song5",[magic.Magnet,magic.Magnet,magic.Thunder,magic.Thunder,magic.Thunder])
        atlantica_graph.add_edge("Song4","Song5")
        if not regular_rando:
            atlantica_graph.add_node("Song2",[magic.Magnet])
            atlantica_graph.add_edge("Song2","Song4")
        self.human_readable_lock_list[locationType.Atlantica] = atlantica_graph
        # AG
        if regular_rando:
            ag_graph = Graph()
            ag_graph.add_node("AG1",[storyunlock.Scimitar])
            ag_graph.add_node("AG2",[storyunlock.Scimitar,storyunlock.Scimitar,magic.Fire,magic.Blizzard,magic.Thunder])
            ag_graph.add_edge("AG1","AG2")
            if keyblade_locking:
                ag_graph.add_node("AGChests",[keyblade.WishingLamp])
                ag_graph.add_edge("AG1","AGChests")
                ag_graph.add_edge("AG2","AGChests")
                ag_graph.add_edge("AGChests","AG2")
            self.human_readable_lock_list[locationType.Agrabah] = ag_graph
        else:
            ag_graph = Graph()
            ag_graph.add_node("AG1",[storyunlock.Scimitar]) # there are no first visit checks in reverse without the key
            ag_graph.add_node("AG1.5",[magic.Fire,magic.Blizzard,magic.Thunder])
            ag_graph.add_node("AG2",[storyunlock.Scimitar,storyunlock.Scimitar])
            ag_graph.add_edge("AG1","AG1.5")
            ag_graph.add_edge("AG1.5","AG2")
            if keyblade_locking:
                ag_graph.add_node("AGChests",[storyunlock.Scimitar,keyblade.WishingLamp])
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
            if len(graph.node_list()) != len(current_item_data):
                return None
            return current_item_data


        item_id_lock_list: dict[locationType,list[list[int]]] = {}
        for location_type,lock_graph in self.human_readable_lock_list.items():
            # convert this from graph to randomly ordered item id list
            random_ordered_requirements = None
            while random_ordered_requirements is None:
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
        self.populate_possible_locking_item_list(settings.regular_rando, settings.keyblades_unlock_chests)

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
            items_to_add_to_inventory = []
            for location, requirements in location_requirements.items():
                if self.evaluate(inventory, requirements):
                    # find assigned item to location
                    for assignment in randomizer.assignments:
                        # if assignment is one of the struggle win/lose items, only count one, and not count the second.
                        if assignment.location.name() == stt.CheckLocation.StruggleWinnerChampionBelt:
                            continue
                        if location == assignment.location:
                            items_to_add_to_inventory.append(assignment.item.Id)
                            if assignment.item2 is not None:
                                items_to_add_to_inventory.append(assignment.item2.Id)
                            break
                    locations_to_remove.append(location)
                    self.location_spheres[location] = depth-1
                    changed = True
            for shop_item in locations_to_remove:
                location_requirements.pop(shop_item)
            inventory.extend(items_to_add_to_inventory)

        if (settings.item_accessibility == ItemAccessibilityOption.ALL and results.full_clear) \
                or (settings.item_accessibility == ItemAccessibilityOption.BEATABLE and results.any_percent):
            # we all good
            if verbose:
                print(f"Unreachable locations {len(location_requirements)}")
            return self.location_spheres
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


class SeedCheckerLuaGenerator:

    def __init__(self, randomizer: Randomizer, verbose: bool):
        super().__init__()
        self.randomizer = randomizer
        self.verbose = verbose

    def get_script_content(self) -> str:
        lua_file_text = ""
        with open(resource_path("static/RandoSeedChecker.lua"), encoding="utf-8") as opened_file:
            lua_file_text = opened_file.read()

        lua_code_lines: list[str] = []
        if self.verbose:
            lua_code_lines.append("verbose = true")

        def add_checks(fn_name: str, addresses_and_locations: list[tuple[int, str]]):
            for pair in addresses_and_locations:
                address, location_name = pair

                assignment = self.randomizer.assignment_for_location(location_name)
                if assignment is not None:
                    assignment_item = assignment.item
                    if assignment_item is not None and assignment_item.item != NullItem:
                        label = location_name if self.verbose else ""
                        lua_code_lines.append(
                            f'    {fn_name}(0x{address:X}, {assignment_item.item.id}, "{label}")'
                        )

        def add_level_checks(addresses_and_levels: list[tuple[int, int]]):
            for pair in addresses_and_levels:
                address, level = pair

                assignment = self.randomizer.assignment_for_sword_level(level)
                if assignment is not None:
                    assignment_item = assignment.item
                    if assignment_item is not None and assignment_item.item != NullItem:
                        label = f"Level {level}" if self.verbose else ""
                        lua_code_lines.append(
                            f'    check_level_up_item(0x{address:X}, {assignment_item.item.id}, "{label}")'
                        )

        add_checks(
            "check_chest_item",
            [
                (0x1CDF826, ag.CheckLocation.AgrabahDarkShard),
                (0x1CDF8CE, ag.CheckLocation.CaveEntrancePowerStone),
                (0x1CDFC16, bc.CheckLocation.BellesRoomCastleMap),
                (0x1CDFCE2, bc.CheckLocation.BeastsRoomBlazingShard),
                (0x1CDF95E, dc.CheckLocation.CornerstoneHillMap),
                (0x1CDFA06, dc.CheckLocation.LibraryTornPages),
                (0x1CDFD96, ht.CheckLocation.GraveyardMythrilShard),
                (0x1CDFDF6, ht.CheckLocation.CandyCaneLaneMegaPotion),
                (0x1CDFF3A, hb.CheckLocation.BoroughDriveRecovery),
                (0x1CDFFD6, hb.CheckLocation.UkuleleCharm),
                (0x1CE001E, hb.CheckLocation.CrystalFissureApBoost),
                (0x1CE0036, hb.CheckLocation.HeartlessManufactoryCosmicChain),
                (0x1CE0522, hb.CheckLocation.CorDepthsUpperLevelRemembranceGem),
                (0x1CE0576, hb.CheckLocation.CorEngineChamberSerenityCrystal),
                (0x1CDFA12, haw.CheckLocation.PoohsHowseHundredAcreWoodMap),
                (0x1CDFAA2, haw.CheckLocation.SpookyCaveMyhtrilGem),
                (0x1CDF72A, lod.CheckLocation.BambooGroveDarkShard),
                (0x1CDF7C6, lod.CheckLocation.ThroneRoomTornPages),
                (0x1CDFB02, oc.CheckLocation.UnderworldEntrancePowerBoost),
                (0x1CDFBCE, oc.CheckLocation.LockCavernsMap),
                (0x1CDFE3E, pr.CheckLocation.RampartNavalMap),
                (0x1CDFEE6, pr.CheckLocation.InterceptorsHoldFeatherCharm),
                (0x1CE005A, pl.CheckLocation.GorgeMyhtrilStone),
                (0x1CE0126, pl.CheckLocation.JungleSerenityGem),
                (0x1CE0192, stt.CheckLocation.CentralStationHiPotion),
                (0x1CE0216, stt.CheckLocation.MansionLibraryHiPotion),
                (0x1CDFCEE, sp.CheckLocation.PitCellAreaMap),
                (0x1CDFD66, sp.CheckLocation.CentralComputerCoreApBoost),
                (0x1CE0246, tt.CheckLocation.WoodsPotion),
                (0x1CE0282, tt.CheckLocation.TramCommonTent),
                (0x1CE0282, tt.CheckLocation.TramCommonTent),
                (0x1CE0306, tt.CheckLocation.TowerEntrywayEther),
                (0x1CE03EA, tt.CheckLocation.MansionLibraryOrichalcum),
                (0x1CE041A, twtnw.CheckLocation.FragmentCrossingApBoost),
                (0x1CE0486, twtnw.CheckLocation.TwilightsViewCosmicBelt),
                (0x1CE04CE, twtnw.CheckLocation.RuinCreationsPassageMythrilCrystal),
                (0x1CE05E2, starting.CheckLocation.GardenOfAssemblageMap),
            ]
        )

        add_checks(
            "check_popup_item",
            [
                (0x107A, ag.CheckLocation.LampCharm),
                (0x11D6, at.CheckLocation.MusicalOrichalcumPlus),
                (0x112E, bc.CheckLocation.RumblingRose),
                (0x103E, dc.CheckLocation.WisdomForm),
                (0x13F2, dc.CheckLocation.LingeringWillProofOfConnection),
                (0x11A6, ht.CheckLocation.DecoyPresents),
                (0x140A, hb.CheckLocation.WinnersProof),
                (0x11FA, haw.CheckLocation.StarryHillCureElement),
                (0x13C2, lod.CheckLocation.DataXigbarDefenseBoost),
                (0x1332, oc.CheckLocation.ZexionBookOfShadows),
                (0x1176, oc.CheckLocation.TitanCupGenjiShield),
                (0x1152, pr.CheckLocation.SeadriftRowShipGraveyardMap),
                (0x109E, pl.CheckLocation.ScarFireElement),
                (0x0EEE, stt.CheckLocation.StruggleWinnerChampionBelt),
                (0x0F06, stt.CheckLocation.StruggleTrophy),
                (0x13E6, stt.CheckLocation.DataRoxasMagicBoost),
                (0x10F2, sp.CheckLocation.PhotonDebugger),
                (0x1242, tt.CheckLocation.BetwixtAndBetweenBondOfFlame),
                (0x12DE, twtnw.CheckLocation.LuxordSecretAnsemReport9),
                (0x13B6, twtnw.CheckLocation.DataXemnas),
            ]
        )

        add_level_checks(
            [
                (0x054, 2),
                (0x0D4, 10),
                (0x174, 20),
                (0x214, 30),
                (0x354, 50),
                (0x664, 99),
            ]
        )

        add_checks(
            "check_form_level_item",
            [
                (0x0044, formlevel.CheckLocation.Valor2),
                (0x005C, formlevel.CheckLocation.Valor5),
                (0x006C, formlevel.CheckLocation.Valor7),
                (0x0084, formlevel.CheckLocation.Wisdom3),
                (0x00DC, formlevel.CheckLocation.Limit7),
                (0x00EC, formlevel.CheckLocation.Master2),
                (0x0144, formlevel.CheckLocation.Final6),
            ]
        )

        lua_file_text = lua_file_text.replace("-- {REPLACE_ME}", "\n".join(lua_code_lines))
        return lua_file_text

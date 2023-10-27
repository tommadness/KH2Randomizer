import base64
import copy
import json
import random
from itertools import permutations, chain
import textwrap
from zipfile import ZipFile

from Class.exceptions import HintException
from Class.itemClass import KH2Item
from Class.newLocationClass import KH2Location
from List.configDict import itemType, locationType, locationCategory
from List.inventory import ability, form, magic, misc, storyunlock, summon, proof
from List.location import simulatedtwilighttown as stt
from Module import version
from Module.RandomizerSettings import RandomizerSettings
from Module.newRandomize import Randomizer, ItemAssignment
from Module.seedmod import SeedModBuilder


class Hints:
    @staticmethod
    def convert_item_assignment_to_tuple(
        item_assignment: list[ItemAssignment], shop_items: list[KH2Item]
    ) -> list[tuple[KH2Location, KH2Item]]:
        location_items: list[tuple[KH2Location, KH2Item]] = []
        for assignment in item_assignment:
            location = assignment.location
            if location.name() != stt.CheckLocation.StruggleLoserMedal:
                location_items.append((location, assignment.item))
                if assignment.item2 is not None:
                    location_items.append((location, assignment.item2))

        fake_shop_location = KH2Location(
            999, "Shop Item", locationCategory.CREATION, [locationType.SHOP]
        )
        for shop_item in shop_items:
            location_items.append((fake_shop_location, shop_item))

        return location_items

    @staticmethod
    def generator_journal_hints(
        location_item_data: list[tuple[KH2Location, KH2Item]],
        settings: RandomizerSettings,
        hintData,
    ):
        journal_data = {}
        for report_num in range(1, 14):
            journal_data[report_num] = ""
        # find any settings relating to journal hints
        independent_hints = settings.journal_hints != "Off"
        independent_hint_specific = settings.journal_hints == "exact"
        dependent_hints = True
        # if dependent hints, depending on hint system, write a tracker-like message to data
        if dependent_hints:
            pass

        # if independent hints, need to make "useful" query on the randomized locations and items
        Hints.independent_journal_hints(
            location_item_data,
            journal_data,
            independent_hints,
            independent_hint_specific,
        )

        # add journal text to hintsText structure
        for report_num in range(1, 14):
            hintData["Reports"][report_num]["JournalText"] = journal_data[report_num]

    @staticmethod
    def independent_journal_hints(
        location_item_data: list[tuple[KH2Location, KH2Item]],
        journal_data,
        independent_hints,
        independent_hint_specific,
    ):
        if independent_hints:
            all_possible_independent_hints = []
            # find the items
            items_to_find = [
                ability.ComboMaster,
                ability.FinishingPlus,
                ability.ExperienceBoost,
                ability.BerserkCharge,
                ability.HorizontalSlash,
                ability.Slapshot,
                ability.FinishingLeap,
                ability.FlashStep,
                ability.SlideDash,
                ability.GuardBreak,
                ability.Explosion,
                ability.AerialSpiral,
                ability.AerialDive,
                ability.MagnetBurst,
                ability.AutoValor,
                ability.AutoWisdom,
                ability.AutoLimitForm,
                ability.AutoMaster,
                ability.AutoFinal,
                ability.TrinityLimit,
                ability.NegativeCombo,
            ]
            hintableWorlds = [
                locationType.Level,
                locationType.LoD,
                locationType.BC,
                locationType.HB,
                locationType.TT,
                locationType.TWTNW,
                locationType.SP,
                locationType.Atlantica,
                locationType.PR,
                locationType.OC,
                locationType.Agrabah,
                locationType.HT,
                locationType.PL,
                locationType.DC,
                locationType.HUNDREDAW,
                locationType.STT,
                locationType.FormLevel,
            ]
            for loc_data, item_data in location_item_data:
                if item_data.item in items_to_find:
                    # if ability is on keyblade, just say the keyblade for now
                    if independent_hint_specific:
                        # hint the specific location
                        all_possible_independent_hints.append(
                            f"{item_data.Name} is in {loc_data.Description}"
                        )
                    else:
                        # hint the world only
                        hintable_worlds_of_location = [
                            l for l in loc_data.LocationTypes if l in hintableWorlds
                        ]
                        if len(hintable_worlds_of_location) == 0:
                            # TODO fix keyblades with abilities
                            print("Hey, something borked")
                        else:
                            all_possible_independent_hints.append(
                                f"{item_data.Name} is in {hintable_worlds_of_location[0].value}"
                            )

            # at this point, we should have all our hint text, just need to assign to each report
            report_index = 0
            while len(all_possible_independent_hints):
                journal_data[report_index + 1] += (
                    all_possible_independent_hints[-1] + "\n\n"
                )
                report_index = (report_index + 1) % 13
                all_possible_independent_hints.pop()

    @staticmethod
    def generate_hints(randomizer: Randomizer, settings: RandomizerSettings):
        hintsType = settings.hintsType
        if hintsType == "Disabled":
            return None

        excludeList = copy.deepcopy(settings.disabledLocations)
        if locationType.HB in excludeList and (
            locationType.TTR not in excludeList or locationType.CoR not in excludeList
        ):
            excludeList.remove(locationType.HB)
        if locationType.OC in excludeList and (locationType.OCCups not in excludeList):
            excludeList.remove(locationType.OC)

        if (
            locationType.SYNTH in excludeList
            and locationType.Puzzle in excludeList
            and not settings.shop_hintable
        ):
            excludeList.append("Creations")

        for l in settings.vanillaLocations:
            if l in excludeList:
                excludeList.remove(l)

        locationItems = randomizer.assignments
        locationItems = Hints.convert_item_assignment_to_tuple(
            locationItems, randomizer.shop_items
        )

        preventSelfHinting = settings.prevent_self_hinting
        allowProofHinting = settings.allow_proof_hinting
        allowReportHinting = settings.allow_report_hinting
        pointHintValues = settings.point_hint_values
        spoilerHintValues = settings.spoiler_hint_values
        hintedItemValues = settings.hintable_check_types
        tracker_includes = settings.tracker_includes + (
            []
            if not settings.shop_hintable
            or locationType.SYNTH.value in settings.tracker_includes
            else [locationType.SYNTH.value]
        )

        importantChecks = settings.important_checks

        # remove any items that aren't enabled by settings
        if settings.promiseCharm:
            tracker_includes.append("PromiseCharm")
        if (
            itemType.OCSTONE in importantChecks
        ):  # questionable tracker_include. Consider more general alternative
            tracker_includes.append("extra_ics")
        if settings.antiform:
            tracker_includes.append("Anti-Form")
        if settings.dummy_forms:
            tracker_includes.append("dummy_forms")

        # start making the hint file
        hintsText = {}
        if settings.progression_hints:
            hintsText["ProgressionSettings"] = settings.progression_hint_settings
            num_progression_worlds = len(hintsText["ProgressionSettings"]["HintCosts"])
        hintsText["hintsType"] = hintsType
        hintsText["generatorVersion"] = settings.ui_version
        hintsText["settings"] = tracker_includes
        hintsText["checkValue"] = pointHintValues
        hintsText["hintableItems"] = hintedItemValues
        if settings.dummy_forms:
            hintsText["dummy_forms"] = True
        hintableWorlds = [
            locationType.Level,
            locationType.LoD,
            locationType.BC,
            locationType.HB,
            locationType.TT,
            locationType.TWTNW,
            locationType.SP,
            locationType.Atlantica,
            locationType.PR,
            locationType.OC,
            locationType.Agrabah,
            locationType.HT,
            locationType.PL,
            locationType.DC,
            locationType.HUNDREDAW,
            locationType.STT,
            locationType.FormLevel,
            "Creations",
        ]

        # All hints do the Shananas thing except JSmartee
        if hintsType != "JSmartee":
            hintsText["world"] = {}
            hintsText["world"][locationType.Critical] = []
            hintsText["world"][locationType.Free] = []
            for x in hintableWorlds:
                hintsText["world"][x] = []
            for location, item in locationItems:
                if location.LocationTypes[0] == locationType.WeaponSlot:
                    continue
                if item.ItemType in importantChecks or item.Name in importantChecks:
                    world_of_location = location.LocationTypes[0]
                    if (
                        world_of_location == locationType.Puzzle
                        or world_of_location == locationType.SYNTH
                        or world_of_location == locationType.SHOP
                    ):
                        world_of_location = "Creations"
                    if not world_of_location in hintsText["world"]:
                        raise HintException(
                            f"Something is going wrong with initializing hintText worlds {world_of_location} {hintsText['world']}"
                        )
                        # hintsText['world'][world_of_location] = []
                    hintsText["world"][world_of_location].append(item.Name)

        if hintsType != "Shananas":
            hintsText["Reports"] = {}
            # importantChecks += [itemType.REPORT]

        report_master = [[locationType.Free]] * 14
        if settings.progression_hints:
            report_master = [[locationType.Free]] * 19
        found_reports = False
        for location, item in locationItems:
            if item.ItemType is itemType.REPORT:
                reportNumber = int(item.Name.replace("Secret Ansem's Report ", ""))
                found_reports = True
                if locationType.Critical in location.LocationTypes:
                    report_master[reportNumber] = [""]
                elif locationType.SYNTH in location.LocationTypes:
                    report_master[reportNumber] = ["Creations"]
                elif locationType.SHOP in location.LocationTypes:
                    report_master[reportNumber] = ["Creations"]
                else:
                    report_master[reportNumber] = location.LocationTypes

        if hintsType == "Path":
            world_to_vanilla_ICs = {}
            world_to_vanilla_ICs[locationType.Level] = [
                ability.SecondChance.id,
                ability.OnceMore.id,
            ]
            world_to_vanilla_ICs[locationType.FormLevel] = [
                form.ValorForm.id,
                form.WisdomForm.id,
                form.FinalForm.id,
                form.MasterForm.id,
                form.LimitForm.id,
            ]
            world_to_vanilla_ICs[locationType.Atlantica] = [magic.Blizzard.id]
            world_to_vanilla_ICs[locationType.TWTNW] = [magic.Magnet.id]
            world_to_vanilla_ICs[locationType.PR] = [
                magic.Magnet.id,
                summon.FeatherCharm.id,
                storyunlock.SkillAndCrossbones.id,
            ]
            world_to_vanilla_ICs[locationType.DC] = [
                misc.TornPages.id,
                magic.Reflect.id,
                form.WisdomForm.id,
            ]
            world_to_vanilla_ICs[locationType.HUNDREDAW] = [
                magic.Cure.id,
                misc.TornPages.id,
            ]
            world_to_vanilla_ICs[locationType.Agrabah] = [
                summon.LampCharm.id,
                magic.Fire.id,
                misc.TornPages.id,
                storyunlock.Scimitar.id,
            ]
            world_to_vanilla_ICs[locationType.BC] = [
                magic.Cure.id,
                magic.Reflect.id,
                storyunlock.BeastsClaw.id,
            ]
            world_to_vanilla_ICs[locationType.TT] = [
                form.ValorForm.id,
                form.LimitForm.id,
                storyunlock.IceCream.id,
                storyunlock.Picture.id,
            ]
            world_to_vanilla_ICs[locationType.SP] = [
                magic.Reflect.id,
                storyunlock.IdentityDisk.id,
            ]
            world_to_vanilla_ICs[locationType.HT] = [
                magic.Magnet.id,
                storyunlock.BoneFist.id,
            ]
            world_to_vanilla_ICs[locationType.PL] = [
                misc.TornPages.id,
                magic.Fire.id,
                magic.Thunder.id,
                storyunlock.ProudFang.id,
            ]
            world_to_vanilla_ICs[locationType.LoD] = [
                magic.Thunder.id,
                misc.TornPages.id,
                storyunlock.SwordOfTheAncestor.id,
            ]
            world_to_vanilla_ICs[locationType.OC] = [
                magic.Thunder.id,
                storyunlock.BattlefieldsOfWar.id,
            ]
            world_to_vanilla_ICs[locationType.HB] = [
                magic.Fire.id,
                magic.Blizzard.id,
                summon.BaseballCharm.id,
                summon.UkuleleCharm.id,
                form.MasterForm.id,
                magic.Cure.id,
                misc.TornPages.id,
                storyunlock.MembershipCard.id,
            ]
            world_to_vanilla_ICs[locationType.STT] = [
                form.ValorForm.id,
                form.LimitForm.id,
            ]
            world_to_vanilla_ICs["Creations"] = []
            world_to_vanilla_ICs[locationType.Critical] = []
            world_to_vanilla_ICs[locationType.Free] = []

            ICs_to_hintable_worlds = {}

            # where did each world drop their breadcrumbs
            # vanilla world to randomized world
            breadcrumb_map = {}

            for key, item_list in world_to_vanilla_ICs.items():
                if key not in breadcrumb_map:
                    breadcrumb_map[key] = set()
                for i in item_list:
                    if i not in ICs_to_hintable_worlds:
                        ICs_to_hintable_worlds[i] = []
                    ICs_to_hintable_worlds[i].append(key)
            proof_of_connection_world = None
            proof_of_peace_world = None
            proof_of_nonexistence_world = None

            for location, item in locationItems:
                if location.LocationTypes[0] == locationType.WeaponSlot:
                    continue
                if item.ItemType in importantChecks or item.Name in importantChecks:
                    world_of_location = location.LocationTypes[0]
                    if (
                        world_of_location == locationType.Puzzle
                        or world_of_location == locationType.SYNTH
                        or world_of_location == locationType.SHOP
                    ):
                        world_of_location = "Creations"
                    if item.ItemType in proof.proof_item_types():
                        if item.ItemType is itemType.PROOF_OF_CONNECTION:
                            proof_of_connection_world = world_of_location
                        elif item.ItemType is itemType.PROOF_OF_PEACE:
                            proof_of_peace_world = world_of_location
                        elif item.ItemType is itemType.PROOF_OF_NONEXISTENCE:
                            proof_of_nonexistence_world = world_of_location
                    elif item.ItemType not in [
                        itemType.KEYITEM,
                        itemType.REPORT,
                        itemType.PROMISE_CHARM,
                        itemType.OCSTONE,
                        itemType.TROPHY,
                        itemType.MANUFACTORYUNLOCK,
                        itemType.MUNNY_POUCH,
                    ]:
                        # this item could have come from any world from this list
                        for w in ICs_to_hintable_worlds[item.Id]:
                            if world_of_location in hintableWorlds:
                                breadcrumb_map[w].add(world_of_location)

            hintable_world_list = list(
                set(
                    chain(
                        breadcrumb_map[proof_of_connection_world]
                        if proof_of_connection_world
                        else [],
                        breadcrumb_map[proof_of_peace_world]
                        if proof_of_peace_world
                        else [],
                        breadcrumb_map[proof_of_nonexistence_world]
                        if proof_of_nonexistence_world
                        else [],
                    )
                )
            )
            hintable_world_list.sort()
            barren_world_list = [
                x
                for x in hintableWorlds
                if x not in hintable_world_list and x not in excludeList
            ]

            hintable_world_list.sort(
                reverse=True, key=lambda x: len(hintsText["world"][x])
            )
            barren_world_list.sort(
                reverse=True, key=lambda x: len(hintsText["world"][x])
            )

            report_texts = []

            def create_hint_text(world):
                num_items = len(hintsText["world"][world])
                hint_text = ""
                world_text = world
                if world == locationType.Level:
                    world_text = "Sora's Heart"
                if world == locationType.TWTNW:
                    world_text = "TWTNW"
                if world == locationType.DC:
                    world_text = "Disney Castle"
                if world == locationType.HUNDREDAW:
                    world_text = "100 Acre"

                points_to_connection = (
                    proof_of_connection_world
                    and world in breadcrumb_map[proof_of_connection_world]
                )
                points_to_peace = (
                    proof_of_peace_world
                    and world in breadcrumb_map[proof_of_peace_world]
                )
                points_to_nonexistence = (
                    proof_of_nonexistence_world
                    and world in breadcrumb_map[proof_of_nonexistence_world]
                )

                proof_list = (
                    []
                    + (["Connection"] if points_to_connection else [])
                    + (["Peace"] if points_to_peace else [])
                    + (["Nonexistence"] if points_to_nonexistence else [])
                )
                if len(proof_list) == 0:
                    proof_list = ["none"]

                if num_items == 0:
                    hint_text = f"{world_text} has nothing, sorry."
                elif (
                    not points_to_connection
                    and not points_to_nonexistence
                    and not points_to_peace
                ):
                    hint_text = f"{world_text} has no path to the light."
                elif (
                    points_to_connection and points_to_nonexistence and points_to_peace
                ):
                    hint_text = f"{world_text} has a path to all lights."
                elif points_to_connection and points_to_peace:
                    hint_text = f"{world_text} is on the path to Connection and Peace."
                elif points_to_connection and points_to_nonexistence:
                    hint_text = (
                        f"{world_text} is on the path to Connection and Nonexistence."
                    )
                elif points_to_nonexistence and points_to_peace:
                    hint_text = (
                        f"{world_text} is on the path to Nonexistence and Peace."
                    )
                elif points_to_nonexistence:
                    hint_text = f"{world_text} is on the path to Nonexistence."
                elif points_to_peace:
                    hint_text = f"{world_text} is on the path to Peace."
                elif points_to_connection:
                    hint_text = f"{world_text} is on the path to Connection."

                return hint_text, world, proof_list

            for x in hintable_world_list:
                report_texts.append(create_hint_text(x))
            for x in barren_world_list:
                report_texts.append(create_hint_text(x))

            if not found_reports:
                for reportNumber in range(1, 14):
                    report_master[reportNumber] = [""]

            if not settings.progression_hints:
                valid_reports = False
                for iter in range(1, 10):
                    report_texts = report_texts[0:13]
                    random.shuffle(report_texts)
                    valid_reports = True
                    for x in range(1, 14):
                        report_location = report_master[x][0]
                        report_hint_world = report_texts[x - 1][1]
                        if report_hint_world == report_location:
                            valid_reports = False
                            break
                    if valid_reports:
                        break
                if not valid_reports:
                    raise HintException(
                        "Failed to assign path hints due to self hinting"
                    )

                for x in range(1, 14):
                    report_location = report_master[x][0]
                    hintsText["Reports"][x] = {
                        "Text": report_texts[x - 1][0],
                        "HintedWorld": report_texts[x - 1][1],
                        "ProofPath": report_texts[x - 1][2],
                        "Location": report_location,
                    }
            else:  # we are doing progression hints
                valid_reports = False
                for reportNumber in range(14, num_progression_worlds):
                    report_master[reportNumber] = [""]
                for iter in range(1, 10):
                    report_texts = report_texts[0:num_progression_worlds]
                    random.shuffle(report_texts)
                    valid_reports = True
                    for x in range(1, 14):
                        report_location = report_master[x][0]
                        report_hint_world = report_texts[x - 1][1]
                        if report_hint_world == report_location:
                            valid_reports = False
                            break
                    if valid_reports:
                        break
                if not valid_reports:
                    raise HintException(
                        "Failed to assign path hints due to self hinting"
                    )

                for x in range(1, num_progression_worlds + 1):
                    report_location = report_master[x][0]
                    hintsText["Reports"][x] = {
                        "Text": report_texts[x - 1][0],
                        "HintedWorld": report_texts[x - 1][1],
                        "ProofPath": report_texts[x - 1][2],
                        "Location": report_location,
                    }

        if hintsType == "JSmartee":
            proof_of_connection_index = None
            proof_of_peace_index = None
            proof_of_nonexistence_index = None
            worldsToHint = []
            reportRestrictions = [[], [], [], [], [], [], [], [], [], [], [], [], []]
            reportsList = list(range(1, 14))

            freeReports = []

            worldChecks = {}
            for h in hintableWorlds:
                if h not in excludeList:
                    worldChecks[h] = []

            for location, item in locationItems:
                if location.LocationTypes[0] in [
                    locationType.WeaponSlot,
                    locationType.Free,
                    locationType.Critical,
                ]:
                    continue
                if item.ItemType in importantChecks or item.Name in importantChecks:
                    world_of_location = location.LocationTypes[0]
                    if (
                        world_of_location == locationType.Puzzle
                        or world_of_location == locationType.SYNTH
                        or world_of_location == locationType.SHOP
                    ):
                        world_of_location = "Creations"
                    worldChecks[world_of_location].append(item)
                    if item.ItemType in proof.proof_item_types():
                        if not world_of_location in worldsToHint:
                            if item.ItemType is itemType.PROOF_OF_CONNECTION:
                                proof_of_connection_index = len(worldsToHint)
                            elif item.ItemType is itemType.PROOF_OF_PEACE:
                                proof_of_peace_index = len(worldsToHint)
                            elif item.ItemType is itemType.PROOF_OF_NONEXISTENCE:
                                proof_of_nonexistence_index = len(worldsToHint)
                            worldsToHint.append(world_of_location)
                        else:
                            if item.ItemType is itemType.PROOF_OF_CONNECTION:
                                proof_of_connection_index = worldsToHint.index(
                                    world_of_location
                                )
                            elif item.ItemType is itemType.PROOF_OF_PEACE:
                                proof_of_peace_index = worldsToHint.index(
                                    world_of_location
                                )
                            elif item.ItemType is itemType.PROOF_OF_NONEXISTENCE:
                                proof_of_nonexistence_index = worldsToHint.index(
                                    world_of_location
                                )
            for location, item in locationItems:
                world_of_location = location.LocationTypes[0]
                if (
                    world_of_location == locationType.Puzzle
                    or world_of_location == locationType.SYNTH
                    or world_of_location == locationType.SHOP
                ):
                    world_of_location = "Creations"
                if world_of_location in [locationType.Free, locationType.Critical]:
                    if item.ItemType is itemType.REPORT:
                        reportNumber = int(
                            item.Name.replace("Secret Ansem's Report ", "")
                        )
                        freeReports.append(reportNumber)
                    continue
                if item.ItemType is itemType.REPORT:
                    reportNumber = int(item.Name.replace("Secret Ansem's Report ", ""))
                    # report can't hint itself
                    if preventSelfHinting:
                        reportRestrictions[reportNumber - 1].append(world_of_location)
                    if locationType.LW in location.LocationTypes:
                        # if report on LW, can't hint world that contains proof of connection
                        if proof_of_connection_index is not None:
                            reportRestrictions[reportNumber - 1].append(
                                worldsToHint[proof_of_connection_index]
                            )
                    if locationType.Mush13 in location.LocationTypes:
                        # if report on Mushroom, can't hint world that contains proof of peace
                        if proof_of_peace_index is not None:
                            reportRestrictions[reportNumber - 1].append(
                                worldsToHint[proof_of_peace_index]
                            )

            if len(worldChecks.keys()) < 13:
                while len(worldChecks.keys()) < 13:
                    new_choice = random.choice(hintableWorlds)
                    if new_choice not in worldChecks:
                        worldChecks[new_choice] = []

                # raise HintException("Too few worlds. Add more worlds or change hint system.")

            numProofWorlds = len(worldsToHint)

            forms_need_hints = locationType.FormLevel in worldsToHint
            pages_need_hints = locationType.HUNDREDAW in worldsToHint
            mag_thun_need_hints = locationType.Atlantica in worldsToHint

            # following the priority of Proofs > Story Unlocks > Forms > Pages > Thunders > Magnets > Proof Reports

            story_unlock_ids = {
                locationType.OC: [storyunlock.BattlefieldsOfWar.id],
                locationType.LoD: [storyunlock.SwordOfTheAncestor.id],
                locationType.BC: [storyunlock.BeastsClaw.id],
                locationType.HT: [storyunlock.BoneFist.id],
                locationType.PL: [storyunlock.ProudFang.id],
                locationType.PR: [storyunlock.SkillAndCrossbones.id],
                locationType.Agrabah: [storyunlock.Scimitar.id],
                locationType.HB: [storyunlock.MembershipCard.id],
                locationType.SP: [storyunlock.IdentityDisk.id],
                locationType.TT: [storyunlock.IceCream.id, storyunlock.Picture.id],
            }
            story_unlocks_for_proofs = []
            for world in hintableWorlds:
                if world in story_unlock_ids:
                    story_unlocks_for_proofs += story_unlock_ids[world]
            for unlock in story_unlocks_for_proofs:
                # find the unlock item
                for world in worldChecks:
                    items_in_world = worldChecks[world]
                    for item in items_in_world:
                        if item.Id == unlock:
                            if not world in worldsToHint:
                                worldsToHint.append(world)

            if forms_need_hints:
                for world in worldChecks:
                    if not world in worldsToHint and any(
                        item.ItemType == itemType.FORM for item in worldChecks[world]
                    ):
                        worldsToHint.append(world)

            if pages_need_hints:
                for world in worldChecks:
                    if not world in worldsToHint and any(
                        item.ItemType == itemType.TORN_PAGE
                        for item in worldChecks[world]
                    ):
                        worldsToHint.append(world)

            if mag_thun_need_hints:
                for world in worldChecks:
                    if not world in worldsToHint and any(
                        item.ItemType == itemType.THUNDER for item in worldChecks[world]
                    ):
                        worldsToHint.append(world)

            if mag_thun_need_hints:
                for world in worldChecks:
                    if not world in worldsToHint and any(
                        item.ItemType == itemType.MAGNET for item in worldChecks[world]
                    ):
                        worldsToHint.append(world)

            # worldsToHint is now all the required hinted worlds. We'll see if we can also hint the reports that hint proofs
            if len(worldsToHint) > 13:
                worldsToHint = worldsToHint[0:13]

            # at least 1 proof is in a hintable world, so we need to hint it
            if numProofWorlds > 0:
                # different possibilities for how to make the reports hinting the proofs hinted
                temp_ordering = permutations(reportsList, numProofWorlds)
                reportOrdering = []
                for o in temp_ordering:
                    reportOrdering.append(o)
                random.shuffle(reportOrdering)
                # for each assignment of reports to proof locations, try to assign hints to reports
                for ordering in reportOrdering:
                    remaining_report_slots = 13 - len(worldsToHint)
                    worlds_to_add = []
                    invalid = False
                    # for each of the chosen reports
                    for index, reportNumber in enumerate(ordering):
                        # figure out which world has that report
                        if reportNumber in freeReports:
                            # if the report is free, it doesn't need to be hinted, and it won't have a restriction
                            continue
                        for world in worldChecks:
                            if world in report_master[reportNumber]:
                                # if any(item.Name.replace("Secret Ansem's Report ","") == str(reportNumber) for item in worldChecks[world] ):
                                # found the world with this report, now to see if this report can hint a proof location
                                if (
                                    worldsToHint[index]
                                    in reportRestrictions[reportNumber - 1]
                                ):
                                    invalid = True
                                    break

                                # we found a report that can hint this proof, add the report's world to the list of worlds we want to hint
                                if world not in worldsToHint:
                                    # totally fine if we have space
                                    if world not in worlds_to_add:
                                        worlds_to_add.append(world)
                                        remaining_report_slots -= 1
                                break
                        if invalid:
                            break
                    # this check makes it's best attempt to get the proof reports hinted
                    if remaining_report_slots < 0:
                        continue
                    # found a good assignment of reports to point to proofs, lets try assigning the rest
                    if not invalid:
                        proof_report_order = ordering
                        tempWorldsToHint = worldsToHint + worlds_to_add
                        if len(tempWorldsToHint) > 13:
                            tempWorldsToHint = tempWorldsToHint[0:13]

                        # ------------------ Done filling required hinted worlds --------------------------------
                        # ------------------ Attempting to find a good assignment for the hints, after too many tries, return an error
                        for try_number in range(10):
                            hintsText["Reports"] = {}
                            reportsList = list(range(1, 14))
                            for index, world in enumerate(tempWorldsToHint):
                                reportNumber = None
                                if index < len(proof_report_order):
                                    reportNumber = proof_report_order[index]
                                    reportsList.remove(reportNumber)
                                else:
                                    random.shuffle(reportsList)
                                    for maybeReportNumber in reportsList:
                                        if (
                                            world
                                            not in reportRestrictions[
                                                maybeReportNumber - 1
                                            ]
                                        ):
                                            reportsList.remove(maybeReportNumber)
                                            reportNumber = maybeReportNumber
                                            break
                                if reportNumber is None:
                                    hintsText["Reports"] = {}
                                    break

                                hintsText["Reports"][reportNumber] = {
                                    "World": world,
                                    "Count": len(worldChecks[world]),
                                    "Location": "",
                                }
                            if len(hintsText["Reports"]) == 0:
                                continue
                        if len(hintsText["Reports"]) != 0:
                            worldsToHint = tempWorldsToHint
                            break

                if len(hintsText["Reports"]) == 0:
                    raise HintException("Unable to find valid assignment for hints...")

            # slack worlds to hint, can point to anywhere
            while len(reportsList) > 0:
                random.shuffle(reportsList)
                worlds = list(worldChecks.keys())
                random.shuffle(worlds)
                randomWorld = None

                if (worlds[0] not in worldsToHint) and (
                    worlds[0] not in reportRestrictions[reportsList[0] - 1]
                ):
                    reportNumber = reportsList.pop(0)
                    randomWorld = worlds[0]
                else:
                    continue

                hintsText["Reports"][reportNumber] = {
                    "World": randomWorld,
                    "Count": len(worldChecks[randomWorld]),
                    "Location": "",
                }
                worldsToHint.append(randomWorld)

            for reportNumber in range(1, 14):
                if hintsText["Reports"][reportNumber]["Location"] != "":
                    continue
                else:
                    hintsText["Reports"][reportNumber]["Location"] = report_master[
                        reportNumber
                    ][0]

            if len(worldsToHint) != len(set(worldsToHint)):
                raise HintException(
                    "Two reports hint the same location. This is an error, try a new seedname."
                )

            if settings.progression_hints:
                # get the hinted worlds
                hinted_worlds = []
                for reportNumber in range(1, 14):
                    hinted_worlds.append(hintsText["Reports"][reportNumber]["World"])

                unhinted_worlds = []
                for h in hintableWorlds:
                    if h not in excludeList and h not in hinted_worlds:
                        unhinted_worlds.append(h)

                for reportNumber in range(14, num_progression_worlds + 1):
                    hintsText["Reports"][reportNumber] = {
                        "World": unhinted_worlds[reportNumber - 14],
                        "Location": "",
                        "Count": len(worldChecks[unhinted_worlds[reportNumber - 14]]),
                    }

        if hintsType == "Points":
            reportRestrictions = [[] for x in range(13)]
            reportsList = list(range(1, 14))
            reportRepetition = 0
            tempWorldR = None
            tempItemR = None
            tempExcludeList = []

            worldChecks = {}
            worldChecksEdit = {}
            for h in hintableWorlds:
                if h not in excludeList:
                    worldChecks[h] = []
                    worldChecksEdit[h] = []

            hintable_item_count = 0
            for location, item in locationItems:
                world_of_location = location.LocationTypes[0]
                if (
                    world_of_location == locationType.Puzzle
                    or world_of_location == locationType.SYNTH
                    or world_of_location == locationType.SHOP
                ):
                    world_of_location = "Creations"
                if (
                    world_of_location == locationType.WeaponSlot
                    or world_of_location == locationType.Free
                    or world_of_location == locationType.Critical
                ):
                    continue
                if item.ItemType in importantChecks or item.Name in importantChecks:
                    if (
                        item.ItemType
                        not in [
                            itemType.PROOF_OF_NONEXISTENCE,
                            itemType.PROOF_OF_CONNECTION,
                            itemType.PROOF_OF_PEACE,
                            itemType.PROMISE_CHARM,
                            itemType.REPORT,
                        ]
                        or (
                            item.ItemType
                            in [
                                itemType.PROOF_OF_NONEXISTENCE,
                                itemType.PROOF_OF_CONNECTION,
                                itemType.PROOF_OF_PEACE,
                                itemType.PROMISE_CHARM,
                            ]
                            and allowProofHinting
                        )
                        or (item.ItemType in [itemType.REPORT] and allowReportHinting)
                    ):
                        hintable_item_count += 1
                    worldChecks[world_of_location].append(item)
                    worldChecksEdit[world_of_location].append(item)
                if item.ItemType is itemType.REPORT and preventSelfHinting:
                    # report can't hint itself
                    reportNumber = int(item.Name.replace("Secret Ansem's Report ", ""))
                    reportRestrictions[reportNumber - 1].append(world_of_location)
            attempts = 0
            while len(reportsList) > 0:
                # condition for running out of hintable items
                if 13 - len(reportsList) == hintable_item_count:
                    break
                attempts += 1
                if attempts > 500:
                    raise HintException(
                        f"Points hints got stuck assigning {len(reportsList)} reports"
                    )

                temp_worlds = list(worldChecksEdit.keys())
                worlds = []

                for place in temp_worlds:
                    if place not in tempExcludeList:
                        worlds.append(place)

                random.shuffle(reportsList)
                random.shuffle(worlds)
                randomWorld = None

                # reset list
                if len(worlds) == 0:
                    print("reset list")
                    tempExcludeList.clear()
                    continue

                if len(worldChecksEdit[worlds[0]]) != 0:
                    if worlds[0] not in reportRestrictions[reportsList[0] - 1]:
                        reportNumber = reportsList.pop(0)
                        randomWorld = worlds[0]
                    else:
                        continue
                else:
                    tempExcludeList.append(worlds[0])
                    continue

                randomItem = random.choice(worldChecksEdit[randomWorld])

                # compare current selected world and item to previously rerolled reports
                # more of a jank failsafe really
                if randomWorld == tempWorldR and randomItem.Name == tempItemR:
                    reportRepetition = reportRepetition + 1

                # should we hint proofs?
                if randomItem.ItemType in [
                    itemType.PROOF_OF_NONEXISTENCE,
                    itemType.PROOF_OF_PEACE,
                    itemType.PROOF_OF_CONNECTION,
                    itemType.PROMISE_CHARM,
                ]:
                    if not allowProofHinting:
                        worldChecksEdit[randomWorld].remove(randomItem)
                        reportsList.append(reportNumber)
                        continue

                # try to hint other reports
                if "Report" in randomItem.Name:
                    if allowReportHinting:
                        # prevent reports from hinting themselves (redundant?)
                        if reportNumber == int(
                            randomItem.Name.replace("Secret Ansem's Report ", "")
                        ):
                            tempWorldR = randomWorld
                            tempItemR = randomItem.Name
                            reportsList.append(reportNumber)
                            continue

                        # if we tried to roll for this 3 times already then stop trying and remove the report from being hinted
                        if reportRepetition > 2:
                            worldChecksEdit[randomWorld].remove(randomItem)
                            tempWorldR = None
                            tempItemR = None
                            reportRepetition = 0
                            reportsList.append(reportNumber)
                            continue

                        random_number = random.randint(1, 3)

                        if random_number != 1:
                            tempWorldR = randomWorld
                            tempItemR = randomItem.Name
                            reportsList.append(reportNumber)
                            continue
                    else:
                        # print("No. removing item and rerolling...")
                        worldChecksEdit[randomWorld].remove(randomItem)
                        reportsList.append(reportNumber)
                        continue

                hintsText["Reports"][reportNumber] = {
                    "World": randomWorld,
                    "check": randomItem.Name,
                    "Location": "",
                }

                # remove hinted item from list
                worldChecksEdit[randomWorld].remove(randomItem)
                tempExcludeList.append(randomWorld)

            for r in reportsList:
                hintsText["Reports"][r] = {"World": "", "check": "", "Location": ""}

            for reportNumber in range(1, 14):
                # cant make reports anonymous because then report ghosts are unable to know which report was hinted
                # if "Report" in hintsText["Reports"][reportNumber]["check"]:
                #     hintsText["Reports"][reportNumber]["check"] = "Ansem Report"
                if hintsText["Reports"][reportNumber]["Location"] != "":
                    continue
                hintsText["Reports"][reportNumber]["Location"] = report_master[
                    reportNumber
                ][0]

        if hintsType == "Spoiler":
            hintsText["reveal"] = spoilerHintValues
            worldsToHint = []
            reportRestrictions = [[], [], [], [], [], [], [], [], [], [], [], [], []]
            reportsList = list(range(1, 14))
            tempExcludeList = []
            IC_Types = {}
            IC_Types["magic"] = [
                itemType.FIRE,
                itemType.BLIZZARD,
                itemType.THUNDER,
                itemType.CURE,
                itemType.REFLECT,
                itemType.MAGNET,
            ]
            IC_Types["page"] = [itemType.TORN_PAGE]
            IC_Types["summon"] = [itemType.SUMMON]
            IC_Types["ability"] = ["Second Chance", "Once More"]
            IC_Types["proof"] = [
                itemType.PROOF_OF_NONEXISTENCE,
                itemType.PROOF_OF_CONNECTION,
                itemType.PROOF_OF_PEACE,
                itemType.PROMISE_CHARM,
            ]
            IC_Types["form"] = [itemType.FORM, "Anti-Form"]
            IC_Types["other"] = ["Hades Cup Trophy", "Unknown Disk", "Olympus Stone"]
            IC_Types["report"] = [itemType.REPORT]
            IC_Types["visit"] = [itemType.STORYUNLOCK]
            worldItemTypes = {}

            for location, item in locationItems:
                if location.LocationTypes[0] == locationType.WeaponSlot:
                    continue
                if item.ItemType in importantChecks or item.Name in importantChecks:
                    world_of_location = location.LocationTypes[0]
                    if (
                        world_of_location == locationType.SYNTH
                        or world_of_location == locationType.Puzzle
                        or world_of_location == locationType.SHOP
                    ):
                        world_of_location = "Creations"
                    # make a list of worlds and the checks they have depending on reveal list
                    if not world_of_location in worldItemTypes:
                        worldItemTypes[world_of_location] = []
                    for type_name in spoilerHintValues:
                        if type_name in IC_Types and (
                            item.ItemType in IC_Types[type_name]
                            or item.Name in IC_Types[type_name]
                        ):
                            worldItemTypes[world_of_location].append(item)

            worldChecks = {}
            worldChecksEdit = {}
            for h in hintableWorlds:
                if h not in excludeList:
                    worldChecks[h] = []
                    worldChecksEdit[h] = []

            for location, item in locationItems:
                world_of_location = location.LocationTypes[0]
                if (
                    world_of_location == locationType.Puzzle
                    or world_of_location == locationType.SYNTH
                    or world_of_location == locationType.SHOP
                ):
                    world_of_location = "Creations"
                if (
                    world_of_location == locationType.WeaponSlot
                    or world_of_location == locationType.Free
                    or world_of_location == locationType.Critical
                ):
                    continue
                if item.ItemType in importantChecks or item.Name in importantChecks:
                    worldChecks[world_of_location].append(item)
                    worldChecksEdit[world_of_location].append(item)
                if item.ItemType is itemType.REPORT and preventSelfHinting:
                    # report can't hint itself
                    reportNumber = int(item.Name.replace("Secret Ansem's Report ", ""))
                    reportRestrictions[reportNumber - 1].append(world_of_location)

            attempts = 0
            while len(reportsList) > 0:
                attempts += 1
                if attempts > 500:
                    raise HintException(
                        f"spoiler hints got stuck assigning report text with {len(reportsList)}"
                    )

                temp_worlds = list(worldChecksEdit.keys())
                worlds = []

                for place in temp_worlds:
                    if place not in tempExcludeList:
                        worlds.append(place)

                random.shuffle(reportsList)
                random.shuffle(worlds)
                randomWorld = None

                # bandaid kinda fix with this part i guess. for some reson Creation is always enabled even if puzzle and synthesis toggles are off.
                if (
                    "Puzzle" not in tracker_includes
                    and "Synthesis" not in tracker_includes
                    and not "Creations" in tempExcludeList
                ):
                    # print("Puzzle or Synth isn't enabled! removing Creations world from list...")
                    # print("-----------------------------------------------------------------------------")
                    tempExcludeList.append("Creations")

                if len(worlds) == 0:
                    # print("ran out of worlds! Setting report text as Empty...")
                    # print("-----------------------------------------------------------------------------")
                    randomWorld = "Empty"
                    reportNumber = reportsList.pop(0)
                else:
                    if len(worldChecksEdit[worlds[0]]) != 0:
                        if worlds[0] not in reportRestrictions[reportsList[0] - 1]:
                            # check if world contains at least 1 of an item type in reveal list. avoid setting reports if it can't reveal anything
                            if any(
                                x in worldItemTypes[worlds[0]]
                                for x in worldChecks[worlds[0]]
                            ):
                                reportNumber = reportsList.pop(0)
                                randomWorld = worlds[0]
                            else:
                                # print(worlds[0] + " has nothing we can reveal! removing form list and rerolling")
                                # print("-----------------------------------------------------------------------------")
                                tempExcludeList.append(worlds[0])
                                continue
                        else:
                            # print("Self hinting world! Rerolling...")
                            # print("-----------------------------------------------------------------------------")
                            continue
                    elif "complete" not in spoilerHintValues:
                        # don't skip worlds with 0 checks, we want to know if a world is empty if world color change is disabled
                        # print(worlds[0] + " has 0 checks! setting report text as Nothing")
                        # print("-----------------------------------------------------------------------------")
                        reportNumber = reportsList.pop(0)
                        randomWorld = "Nothing_" + worlds[0]
                        # print("Removing " + worlds[0] + " from hintable worlds")
                        # print("-----------------------------------------------------------------------------")
                        tempExcludeList.append(worlds[0])
                    else:
                        # print(worlds[0] + " has 0 checks and World Color Change is on! removing form list and rerolling...")
                        # print("-----------------------------------------------------------------------------")
                        tempExcludeList.append(worlds[0])
                        continue

                hintsText["Reports"][reportNumber] = {
                    "World": randomWorld,
                    "Location": "",
                }

                # remove world from list
                if (
                    randomWorld != "Empty"
                    and randomWorld.startswith("Nothing_") == False
                ):
                    # print("Removing " + randomWorld + " from hintable worlds")
                    # print("-----------------------------------------------------------------------------")
                    tempExcludeList.append(randomWorld)

            for reportNumber in range(1, 14):
                if hintsText["Reports"][reportNumber]["Location"] != "":
                    continue
                for world in worldChecks:
                    if any(
                        item.Name.replace("Secret Ansem's Report ", "")
                        == str(reportNumber)
                        for item in worldChecks[world]
                    ):
                        hintsText["Reports"][reportNumber]["Location"] = world

            if settings.progression_hints:
                # TODO: Make this more general in refactor
                if settings.revealMode == "bossreports":
                    hintsText["ProgressionType"] = "Bosses"
                # get the hinted worlds
                hinted_worlds = []
                for reportNumber in range(1, 14):
                    hinted_worlds.append(hintsText["Reports"][reportNumber]["World"])

                unhinted_worlds = []
                for h in hintableWorlds:
                    if h not in excludeList and h not in hinted_worlds:
                        unhinted_worlds.append(h)

                for reportNumber in range(14, num_progression_worlds + 1):
                    hintsText["Reports"][reportNumber] = {
                        "World": unhinted_worlds[reportNumber - 14],
                        "Location": "",
                    }

        # report validation for some hint systems
        if (
            hintsType in ["Points", "JSmartee", "Spoiler"]
            and found_reports
            and "report" in hintedItemValues
        ):
            for reportNumber in range(1, 14):
                if (
                    hintsText["Reports"][reportNumber]["Location"]
                    not in report_master[reportNumber]
                ):
                    if hintsText["Reports"][reportNumber]["Location"] == "" and (
                        locationType.Critical in report_master[reportNumber]
                        or locationType.Free in report_master[reportNumber]
                    ):
                        # this is fine, continue
                        continue
                    raise RuntimeError(
                        f"Report {reportNumber} has location written as {hintsText['Reports'][reportNumber]['Location']} but the actual location is {report_master[reportNumber]}"
                    )
        Hints.generator_journal_hints(locationItems, settings, hintsText)
        return hintsText

    @staticmethod
    def write_hints(hint_data, out_zip: ZipFile):
        json_bytes = json.dumps(hint_data).encode("utf-8")
        if version.debug_mode():
            out_zip.writestr("HintFile_DebugHints.json", json_bytes)
        out_zip.writestr("HintFile.Hints", base64.b64encode(json_bytes).decode("utf-8"))

    @staticmethod
    def write_hint_text(hint_data, mod: SeedModBuilder):
        def convert_string_to_unicode(string: str):
            return "".join(
                r"\u{:04X}".format(ord(chr)) for chr in textwrap.fill(string, width=30)
            )

        for report_number in range(0, 13):
            if "JournalText" in hint_data["Reports"][report_number + 1]:
                # print(hint_data["Reports"][report_number + 1]["JournalText"])
                report_text = convert_string_to_unicode(
                    hint_data["Reports"][report_number + 1]["JournalText"]
                )
                mod.journal_txt.add_message(
                    message_id=14052 + report_number * 2, en=report_text
                )

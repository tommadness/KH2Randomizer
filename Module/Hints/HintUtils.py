import copy
from itertools import chain
import random
from Class.exceptions import HintException
from Class.itemClass import KH2Item
from Class.newLocationClass import KH2Location
from List.configDict import HintType, itemType, locationCategory, locationType
from Module import RandomizerSettings
from Module.newRandomize import ItemAssignment, Randomizer
from List.inventory import ability, form, magic, misc, storyunlock, summon, proof
from List.location import simulatedtwilighttown as stt


class CommonTrackerInfo:
    def __init__(self, settings: RandomizerSettings):
        self.hintsType = settings.hintsType
        self.generatorVersion = settings.ui_version
        tracker_includes = settings.tracker_includes + (
            []
            if not settings.shop_hintable
            or locationType.SYNTH.value in settings.tracker_includes
            else [locationType.SYNTH.value]
        )
        self.important_check_list = settings.important_checks
        self.spoiler_reveal_list = settings.spoiler_reveal_checks
        # remove any items that aren't enabled by settings
        if settings.promiseCharm:
            tracker_includes.append("PromiseCharm")
        if (
            itemType.OCSTONE in self.important_check_list
        ):  # questionable tracker_include. Consider more general alternative
            tracker_includes.append("extra_ics")
        if settings.antiform:
            tracker_includes.append("Anti-Form")
        if settings.dummy_forms:
            tracker_includes.append("dummy_forms")
        self.settings = tracker_includes
        self.point_values = settings.point_hint_values
        self.hintable_categories = settings.hintable_check_types
        self.dummy_forms = True if settings.dummy_forms else None
        self.progression_settings = (
            settings.progression_hint_settings if settings.progression_hints else None
        )
        self.spoiler_reveal = (
            settings.spoiler_hint_values if self.hintsType == HintType.SPOILER else None
        )
        self.reveal_mode = settings.revealMode

    def to_dict(self):
        data = {}
        data["hintsType"] = self.hintsType
        data["generatorVersion"] = self.generatorVersion
        data["settings"] = self.settings
        data["checkValue"] = self.point_values
        data["hintableItems"] = self.hintable_categories
        if self.reveal_mode == "bossreports":
            data["ProgressionType"] = "Bosses"
        if self.dummy_forms is not None:
            data["dummy_forms"] = True
        if self.progression_settings is not None:
            data["ProgressionSettings"] = self.progression_settings
        if self.spoiler_reveal is not None:
            data["reveal"] = self.spoiler_reveal
        return data


class WorldItems:
    def __init__(
        self,
        location_item_tuples: list[tuple[KH2Location, KH2Item]],
        tracker_info: CommonTrackerInfo,
    ):
        self.world_to_item_list = {}
        for world in HintUtils.hintable_worlds():
            self.world_to_item_list[world] = []
        # add in the starting items
        self.world_to_item_list[locationType.Critical] = []
        self.world_to_item_list[locationType.Free] = []
        self.report_information = {}
        self.proof_of_connection_world = None
        self.proof_of_peace_world = None
        self.proof_of_nonexistence_world = None
        self.path_breadcrump_map = {}

        for key in HintUtils.world_to_vanilla().keys():
            if key not in self.path_breadcrump_map:
                self.path_breadcrump_map[key] = set()
        for i in range(1, 14):
            self.report_information[i] = {
                "FoundIn": "Garden of Assemblage"
            }  # default to found in starting
        importantChecks = tracker_info.important_check_list
        for location, item in location_item_tuples:
            if locationType.WeaponSlot in location.LocationTypes:
                continue
            if item.ItemType is itemType.REPORT:
                reportNumber = int(item.Name.replace("Secret Ansem's Report ", ""))
                world_of_location = HintUtils.location_to_tracker_world(
                    location.LocationTypes
                )
                self.report_information[reportNumber]["FoundIn"] = world_of_location

            if item.ItemType in importantChecks or item.Name in importantChecks:
                world_of_location = HintUtils.location_to_tracker_world(
                    location.LocationTypes
                )
                if not world_of_location in self.world_to_item_list:
                    raise HintException(
                        f"Something is going wrong with initializing worlds {world_of_location}"
                    )
                self.world_to_item_list[world_of_location].append(item)
                if item.ItemType is itemType.PROOF_OF_PEACE:
                    self.proof_of_peace_world = world_of_location
                elif item.ItemType is itemType.PROOF_OF_CONNECTION:
                    self.proof_of_connection_world = world_of_location
                elif item.ItemType is itemType.PROOF_OF_NONEXISTENCE:
                    self.proof_of_nonexistence_world = world_of_location
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
                    for w in HintUtils.vanilla_to_world()[item.Id]:
                        if world_of_location in HintUtils.hintable_worlds():
                            self.path_breadcrump_map[w].add(world_of_location)

    def world_dict(self):
        dictionary = {}
        for key, it in self.world_to_item_list.items():
            dictionary[key] = []
            for x in it:
                dictionary[key].append(x.Name)
        return dictionary


class JsmarteeHintData:
    def __init__(
        self,
        world_items: WorldItems,
        world_to_hint: locationType,
    ):
        self.world = world_to_hint
        self.count = len(world_items.world_to_item_list[world_to_hint])


class PointHintData:
    def __init__(
        self,
        settings: RandomizerSettings,
        common_tracker_data: CommonTrackerInfo,
        world_items: WorldItems,
        world_to_hint: locationType,
    ):
        self.prevent_self_hinting = settings.prevent_self_hinting
        self.allow_proof_hinting = settings.allow_proof_hinting
        self.allow_report_hinting = settings.allow_report_hinting
        self.world = world_to_hint
        self.unique_items = []
        IC_list = common_tracker_data.important_check_list
        for it in world_items.world_to_item_list[world_to_hint]:
            if it.ItemType in IC_list or it.Name in IC_list:
                self.unique_items.append(it)
        self.unique_items = set(self.unique_items)

    def candidate_hints(self):
        candidate_items = []
        proofs = set(
            [
                itemType.PROOF_OF_PEACE,
                itemType.PROOF_OF_CONNECTION,
                itemType.PROOF_OF_NONEXISTENCE,
                itemType.PROMISE_CHARM,
            ]
        )
        for u in self.unique_items:
            if u.ItemType in proofs:
                if self.allow_proof_hinting:
                    candidate_items.append(u)
            elif u.ItemType is itemType.REPORT:
                if self.allow_report_hinting:
                    candidate_items.append(u)
            else:
                candidate_items.append(u)
        return candidate_items


class PathHintData:
    def __init__(
        self,
        world_items: WorldItems,
        world_to_hint: locationType,
    ):
        self.num_items = len(world_items.world_to_item_list[world_to_hint])
        self.world = world_to_hint
        world_text = world_to_hint
        if world_to_hint == locationType.Level:
            world_text = "Sora's Heart"
        if world_to_hint == locationType.TWTNW:
            world_text = "TWTNW"
        if world_to_hint == locationType.DC:
            world_text = "Disney Castle"
        if world_to_hint == locationType.HUNDREDAW:
            world_text = "100 Acre"
        points_to_connection = (
            world_items.proof_of_connection_world
            and world_to_hint
            in world_items.path_breadcrump_map[world_items.proof_of_connection_world]
        )
        points_to_peace = (
            world_items.proof_of_peace_world
            and world_to_hint
            in world_items.path_breadcrump_map[world_items.proof_of_peace_world]
        )
        points_to_nonexistence = (
            world_items.proof_of_nonexistence_world
            and world_to_hint
            in world_items.path_breadcrump_map[world_items.proof_of_nonexistence_world]
        )

        self.proof_list = (
            []
            + (["Connection"] if points_to_connection else [])
            + (["Peace"] if points_to_peace else [])
            + (["Nonexistence"] if points_to_nonexistence else [])
        )
        if len(self.proof_list) == 0:
            self.proof_list = ["none"]

        if self.num_items == 0:
            hint_text = f"{world_text} has nothing, sorry."
        elif (
            not points_to_connection
            and not points_to_nonexistence
            and not points_to_peace
        ):
            hint_text = f"{world_text} has no path to the light."
        elif points_to_connection and points_to_nonexistence and points_to_peace:
            hint_text = f"{world_text} has a path to all lights."
        elif points_to_connection and points_to_peace:
            hint_text = f"{world_text} is on the path to Connection and Peace."
        elif points_to_connection and points_to_nonexistence:
            hint_text = f"{world_text} is on the path to Connection and Nonexistence."
        elif points_to_nonexistence and points_to_peace:
            hint_text = f"{world_text} is on the path to Nonexistence and Peace."
        elif points_to_nonexistence:
            hint_text = f"{world_text} is on the path to Nonexistence."
        elif points_to_peace:
            hint_text = f"{world_text} is on the path to Peace."
        elif points_to_connection:
            hint_text = f"{world_text} is on the path to Connection."
        self.hint_text = hint_text


class HintUtils:
    @staticmethod
    def hintable_worlds():
        return [
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
            locationType.Creations,
        ]

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
            999,
            "Shop Item",
            locationCategory.CREATION,
            [locationType.SHOP, locationType.Creations],
        )
        for shop_item in shop_items:
            location_items.append((fake_shop_location, shop_item))

        return location_items

    @staticmethod
    def location_to_tracker_world(
        location_categories: list[locationType],
    ) -> locationType:
        hintableWorlds = HintUtils.hintable_worlds() + [
            locationType.Free,
            locationType.Critical,
        ]
        overlap = list(set(location_categories).intersection(hintableWorlds))
        if len(overlap) > 1:
            raise HintException(f"Location has two tracker worlds")
        elif len(overlap) == 0:
            raise HintException(f"Location has no tracker worlds")
        return overlap[0]

    @staticmethod
    def update_disabled_worlds_on_tracker(settings: RandomizerSettings):
        excludeList = copy.deepcopy(settings.disabledLocations)
        # If HB is off, but Transport or CoR are on, we gotta turn HB on
        if locationType.HB in excludeList and (
            locationType.TTR not in excludeList or locationType.CoR not in excludeList
        ):
            excludeList.remove(locationType.HB)

        # If OC is off, but Cups are on, gotta turn OC on
        if locationType.OC in excludeList and (locationType.OCCups not in excludeList):
            excludeList.remove(locationType.OC)

        # find out if we need to turn on the creations world (default yes, this will disable it)
        if (
            locationType.SYNTH in excludeList
            and locationType.Puzzle in excludeList
            and not settings.shop_hintable
        ):
            excludeList.append("Creations")

        # make sure vanilla worlds are in the tracker
        for l in settings.vanillaLocations:
            if l in excludeList:
                excludeList.remove(l)

        return excludeList

    @staticmethod
    def world_to_vanilla():
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
        world_to_vanilla_ICs[locationType.Creations] = []
        world_to_vanilla_ICs[locationType.Critical] = []
        world_to_vanilla_ICs[locationType.Free] = []
        return world_to_vanilla_ICs

    @staticmethod
    def vanilla_to_world():
        ICs_to_hintable_worlds = {}
        w_to_v = HintUtils.world_to_vanilla()
        for key, item_list in w_to_v.items():
            for i in item_list:
                if i not in ICs_to_hintable_worlds:
                    ICs_to_hintable_worlds[i] = []
                ICs_to_hintable_worlds[i].append(key)
        return ICs_to_hintable_worlds

    @staticmethod
    def point_hint_report_assignment(
        settings: RandomizerSettings,
        world_items: WorldItems,
        point_data: list[PointHintData],
    ):
        prevent_self_hinting = settings.prevent_self_hinting
        report_number_to_world_to_item = []
        for num in range(1, 14):
            for p in point_data:
                if (
                    not prevent_self_hinting
                    or world_items.report_information[num]["FoundIn"] != p.world
                ):
                    for cand in p.candidate_hints():
                        report_number_to_world_to_item.append((num, p.world, cand))

        def pick_item(report_num, world, data):
            filtered_list = [
                (r, w, i) for r, w, i in data if w == world and r == report_num
            ]
            if len(filtered_list) == 0:
                return None, None, None
            return random.choice(filtered_list)

        def reduce_list(report_num, world, item, data):
            filtered_list = [(r, w, i) for r, w, i in data if r != report_num]
            filtered_list = [
                (r, w, i) for r, w, i in filtered_list if world != w or item != i
            ]
            return filtered_list

        # populate the hintable world list with ones that have valid items
        hintable_worlds = [p.world for p in point_data if len(p.candidate_hints()) > 0]
        for _ in range(50):
            data = copy.deepcopy(report_number_to_world_to_item)
            report_assignments = {}
            random.shuffle(hintable_worlds)
            if len(hintable_worlds) >= 13:
                final_hintable_worlds = hintable_worlds[0:13]
            else:
                final_hintable_worlds = hintable_worlds * 13
                final_hintable_worlds = final_hintable_worlds[0:13]
            for report_num in range(1, 14):
                selected_report, selected_world, selected_item = pick_item(
                    report_num, final_hintable_worlds[report_num - 1], data
                )
                if selected_report is None:
                    break
                if (
                    selected_report != report_num
                    or selected_world != final_hintable_worlds[report_num - 1]
                ):
                    raise HintException("Improper data computation for point hints")
                report_assignments[report_num] = {
                    "World": selected_world,
                    "check": selected_item.Name,
                    "Location": world_items.report_information[report_num]["FoundIn"],
                }
                data = reduce_list(report_num, selected_world, selected_item, data)
            if len(report_assignments) == 13:
                return report_assignments

        raise HintException("Can't find valid point hint assignment")

    @staticmethod
    def jsmartee_hint_report_assignment(
        settings: RandomizerSettings,
        world_items: WorldItems,
        jsmartee_data: list[JsmarteeHintData],
    ):
        prevent_self_hinting: bool = settings.prevent_self_hinting
        augmented_jsmartee_data = copy.deepcopy(jsmartee_data)
        # populate the hintable world list with ones that have valid items
        hintable_worlds = [j.world for j in augmented_jsmartee_data]
        # if we aren't progression hints, we need 13 hints at least
        if len(hintable_worlds) < 13:
            # if there aren't 13 worlds to hint, add the difference as zero IC worlds
            excludedWorlds = list(
                set(HintUtils.hintable_worlds()).difference(hintable_worlds)
            )
            augmented_jsmartee_data = augmented_jsmartee_data + [
                JsmarteeHintData(world_items, w)
                for w in excludedWorlds[0 : (13 - len(augmented_jsmartee_data))]
            ]
            hintable_worlds = [j.world for j in augmented_jsmartee_data]
        report_number_to_world_to_count = []
        for num in range(1, 14):
            for p in augmented_jsmartee_data:
                if (
                    not prevent_self_hinting
                    or world_items.report_information[num]["FoundIn"] != p.world
                ):
                    report_number_to_world_to_count.append((num, p.world, p.count))

        def pick_world(report_num, world, data):
            filtered_list = [
                (r, w, c) for r, w, c in data if w == world and r == report_num
            ]
            if len(filtered_list) == 0:
                return None, None
            return random.choice(filtered_list)

        def reduce_list(report_num, world, data):
            filtered_list = [(r, w, c) for r, w, c in data if r != report_num]
            filtered_list = [(r, w, c) for r, w, c in filtered_list if world != w]
            return filtered_list

        proof_worlds = [
            world_items.proof_of_connection_world,
            world_items.proof_of_peace_world,
            world_items.proof_of_nonexistence_world,
        ]
        proof_worlds = [
            w for w in proof_worlds if w in HintUtils.hintable_worlds()
        ]  # validation for starting proof locations
        priority_worlds = []
        # TODO add warning about using visit locks with Jsmartee in RandomizerSettings
        if locationType.FormLevel in proof_worlds:
            # add the worlds with forms to priority list
            for w, item_list in world_items.world_to_item_list.items():
                if any([i.ItemType == itemType.FORM for i in item_list]):
                    priority_worlds.append(w)
        if locationType.HUNDREDAW in proof_worlds:
            # add the worlds with pages to priority list
            for w, item_list in world_items.world_to_item_list.items():
                if any([i.ItemType == itemType.TORN_PAGE for i in item_list]):
                    priority_worlds.append(w)
        if locationType.Atlantica in proof_worlds:
            # add the worlds with thunders and magnets to priority list
            for w, item_list in world_items.world_to_item_list.items():
                if any([i.ItemType == itemType.THUNDER for i in item_list]):
                    priority_worlds.append(w)
                if any([i.ItemType == itemType.MAGNET for i in item_list]):
                    priority_worlds.append(w)

        full_priority_list = [w for w in proof_worlds]
        for w in priority_worlds:
            if w not in full_priority_list:
                full_priority_list.append(w)

        for _ in range(100):
            data = copy.deepcopy(report_number_to_world_to_count)
            priorities = copy.deepcopy(full_priority_list)

            # cull down the world list to a set of 13
            selected_worlds = copy.deepcopy(priorities)
            remaining_worlds = [w for w in hintable_worlds if w not in selected_worlds]
            random.shuffle(remaining_worlds)
            selected_worlds = selected_worlds + remaining_worlds
            selected_worlds = selected_worlds[0:13]

            # sanity check, if we already failed to select all priority worlds, fail
            if any(w not in selected_worlds for w in priorities):
                continue

            report_numbers = list(range(1, 14))
            random.shuffle(report_numbers)
            report_assignments = {}
            # try to assign the proof reports
            for index, w in enumerate(selected_worlds):
                chosen_report = report_numbers[index]
                selected_report, selected_world, selected_count = pick_world(
                    chosen_report, w, data
                )
                # failed to select this report/world pair (likely self hinting)
                if selected_report is None:
                    break
                # Sanity check that we returned the same stuff
                if (
                    selected_report != chosen_report
                    or selected_world != selected_worlds[index]
                ):
                    raise HintException("Improper data computation for Jsmartee hints")
                # augment the priority list if we are hinting proof worlds
                if selected_world in proof_worlds:
                    report_world = world_items.report_information[chosen_report][
                        "FoundIn"
                    ]
                    if report_world not in priorities:
                        priorities.append(report_world)
                    if any(inner_w not in selected_worlds for inner_w in priorities):
                        break
                    if len(priorities) > 13:
                        break

                report_assignments[chosen_report] = {
                    "World": selected_world,
                    "Location": world_items.report_information[chosen_report][
                        "FoundIn"
                    ],
                    "Count": selected_count,
                }
                data = reduce_list(chosen_report, selected_world, data)

            if len(report_assignments) == 13:
                return report_assignments

        raise HintException("Can't find valid Jsmartee hint assignment")

    @staticmethod
    def jsmartee_progression_hints(
        world_items: WorldItems,
        jsmartee_data: list[JsmarteeHintData],
    ):
        # output all the data as sequential reports
        report_assignments = {}
        for chosen_report, hint_data in enumerate(jsmartee_data):
            if chosen_report < 13:
                location = world_items.report_information[chosen_report + 1]["FoundIn"]
            else:
                location = ""
            report_assignments[chosen_report + 1] = {
                "World": hint_data.world,
                "Location": location,
                "Count": hint_data.count,
            }
        return report_assignments

    @staticmethod
    def path_hint_assignment(
        world_items: WorldItems,
        path_data: list[PathHintData],
        tracker_data: CommonTrackerInfo,
    ):
        progression_hints = tracker_data.progression_settings is not None
        must_hint = list(
            set(
                chain(
                    world_items.path_breadcrump_map[
                        world_items.proof_of_connection_world
                    ]
                    if world_items.proof_of_connection_world
                    else [],
                    world_items.path_breadcrump_map[world_items.proof_of_peace_world]
                    if world_items.proof_of_peace_world
                    else [],
                    world_items.path_breadcrump_map[
                        world_items.proof_of_nonexistence_world
                    ]
                    if world_items.proof_of_nonexistence_world
                    else [],
                )
            )
        )
        must_hint_data = [p for p in path_data if p.world in must_hint]
        other_data = [p for p in path_data if p.world not in must_hint]
        # prioritize hinting the most items possible
        must_hint_data.sort(reverse=True, key=lambda x: x.num_items)
        other_data.sort(reverse=True, key=lambda x: x.num_items)
        all_data = must_hint_data + other_data

        for _ in range(50):
            report_assignments = {}
            report_numbers = list(range(1, 14))
            random.shuffle(report_numbers)
            if progression_hints:
                report_numbers = report_numbers + list(range(14, len(all_data) + 1))
            for index, report_number in enumerate(report_numbers):
                if index < 13:
                    location = world_items.report_information[report_number]["FoundIn"]
                else:
                    location = ""
                report_assignments[report_number] = {
                    "HintedWorld": all_data[index].world,
                    "Location": location,
                    "ProofPath": all_data[index].proof_list,
                    "Text": all_data[index].hint_text,
                }
            if len(report_numbers) == len(report_assignments):
                return report_assignments

        raise HintException("Can't find valid Path hint assignment")

    @staticmethod
    def spoiler_hint_assignment(
        settings: RandomizerSettings,
        tracker_data: CommonTrackerInfo,
        world_items: WorldItems,
        hintable_worlds: list[locationType],
    ):
        worlds_to_hint = copy.deepcopy(hintable_worlds)
        if tracker_data.progression_settings is not None:
            # report locations don't matter
            data = {}
            for index, w in enumerate(worlds_to_hint):
                data[index + 1] = {"World": w, "Location": ""}
            return data

        for _ in range(50):
            random.shuffle(worlds_to_hint)
            selected_worlds = worlds_to_hint[0:13]
            data = {}
            for index, w in enumerate(selected_worlds):
                if (
                    not settings.prevent_self_hinting
                    or world_items.report_information[index + 1]["FoundIn"] != w
                ):
                    data[index + 1] = {
                        "World": w,
                        "Location": world_items.report_information[index + 1][
                            "FoundIn"
                        ],
                    }
            if len(data) == 13:
                return data

        raise HintException("Can't find valid Jsmartee hint assignment")

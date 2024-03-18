import copy
import random
from itertools import chain
from typing import Any, Optional

from Class.exceptions import HintException
from Class.itemClass import KH2Item
from Class.newLocationClass import KH2Location
from List.configDict import HintType, itemType, locationCategory, locationType
from List.inventory import ability, form, magic, misc, storyunlock, summon
from List.inventory.item import InventoryItem
from List.inventory.report import AnsemReport
from List.location import simulatedtwilighttown as stt
from Module.RandomizerSettings import RandomizerSettings
from Module.newRandomize import ItemAssignment


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

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "hintsType": self.hintsType,
            "generatorVersion": self.generatorVersion,
            "settings": self.settings,
            "checkValue": self.point_values,
            "hintableItems": self.hintable_categories
        }
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
        hintable_worlds = HintUtils.hintable_worlds()
        item_to_vanilla_world = HintUtils.item_to_vanilla_world()

        self.world_to_item_list: dict[locationType, list[KH2Item]] = {}
        for world in hintable_worlds:
            self.world_to_item_list[world] = []
        # add in the starting items
        self.world_to_item_list[locationType.Critical] = []
        self.world_to_item_list[locationType.Free] = []
        self.report_information: dict[int, dict[str, Any]] = {}
        self.proof_of_connection_world: Optional[locationType] = None
        self.proof_of_peace_world: Optional[locationType] = None
        self.proof_of_nonexistence_world: Optional[locationType] = None
        self.path_breadcrump_map: dict[locationType, set[locationType]] = {}

        for world_with_vanilla in HintUtils.world_to_vanilla_items().keys():
            if world_with_vanilla not in self.path_breadcrump_map:
                self.path_breadcrump_map[world_with_vanilla] = set()
        for i in range(1, 14):
            self.report_information[i] = {
                "FoundIn": "Garden of Assemblage"
            }  # default to found in starting
        important_checks = tracker_info.important_check_list
        for location, item in location_item_tuples:
            if locationType.WeaponSlot in location.LocationTypes:
                continue

            inventory_item = item.item
            if isinstance(inventory_item, AnsemReport):
                world_of_location = HintUtils.location_to_tracker_world(location.LocationTypes)
                self.report_information[inventory_item.report_number]["FoundIn"] = world_of_location

            if item.ItemType in important_checks or item.Name in important_checks:
                world_of_location = HintUtils.location_to_tracker_world(location.LocationTypes)
                if world_of_location not in self.world_to_item_list:
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
                    itemType.KEYBLADE,
                ] and item.Id not in [form.AntiForm.id]:
                    # this item could have come from any world from this list
                    for vanilla_world in item_to_vanilla_world[inventory_item]:
                        if world_of_location in hintable_worlds:
                            self.path_breadcrump_map[vanilla_world].add(world_of_location)

    def world_to_item_ids(self) -> dict[locationType, list[int]]:
        """
        Returns a dictionary of world to a list of IDs of items in that world.
        """
        dictionary: dict[locationType, list[int]] = {}
        for world, item_list in self.world_to_item_list.items():
            dictionary[world] = [item.Id for item in item_list]
        return dictionary
    
    def item_ids_to_names(self) -> dict[int, str]:
        """
        Returns a dictionary of world to a list of IDs of items in that world.
        """
        dictionary: dict[int, str] = {}
        for _, item_list in self.world_to_item_list.items():
            for item in item_list:
                dictionary[item.Id] = item.Name
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
        unique_items = []
        ic_list = common_tracker_data.important_check_list
        for item in world_items.world_to_item_list[world_to_hint]:
            if item.ItemType in ic_list or item.Name in ic_list:
                unique_items.append(item)
        self.unique_items = set(unique_items)

    def candidate_hints(self) -> list[KH2Item]:
        candidate_items: list[KH2Item] = []
        proofs = {
            itemType.PROOF_OF_PEACE,
            itemType.PROOF_OF_CONNECTION,
            itemType.PROOF_OF_NONEXISTENCE,
            itemType.PROMISE_CHARM
        }
        for item in self.unique_items:
            if item.ItemType in proofs:
                if self.allow_proof_hinting:
                    candidate_items.append(item)
            elif item.ItemType is itemType.REPORT:
                if self.allow_report_hinting:
                    candidate_items.append(item)
            else:
                candidate_items.append(item)
        return candidate_items


class PathHintData:
    def __init__(
        self,
        world_items: WorldItems,
        world_to_hint: locationType,
    ):
        self.num_items = len(world_items.world_to_item_list[world_to_hint])
        self.world = world_to_hint
        world_text = HintUtils.location_hint_user_friendly_text(world_to_hint)

        poc_world = world_items.proof_of_connection_world
        points_to_connection = (poc_world and world_to_hint in world_items.path_breadcrump_map[poc_world])
        pop_world = world_items.proof_of_peace_world
        points_to_peace = (pop_world and world_to_hint in world_items.path_breadcrump_map[pop_world])
        pon_world = world_items.proof_of_nonexistence_world
        points_to_nonexistence = (pon_world and world_to_hint in world_items.path_breadcrump_map[pon_world])

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
        elif not points_to_connection and not points_to_nonexistence and not points_to_peace:
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
        else:
            raise HintException("Invalid combination of path proof hinting")
        self.hint_text = hint_text


class HintUtils:
    @staticmethod
    def hintable_worlds() -> list[locationType]:
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
            item_assignment: list[ItemAssignment],
            shop_items: list[KH2Item]
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
        hintable_worlds = HintUtils.hintable_worlds() + [
            locationType.Free,
            locationType.Critical,
        ]
        overlap = list(set(location_categories).intersection(hintable_worlds))
        if len(overlap) > 1:
            raise HintException(f"Location has two tracker worlds")
        elif len(overlap) == 0:
            raise HintException(f"Location has no tracker worlds")
        return overlap[0]

    @staticmethod
    def update_disabled_worlds_on_tracker(settings: RandomizerSettings) -> list[locationType]:
        exclude_list = copy.deepcopy(settings.disabledLocations)
        # If HB is off, but Transport or CoR are on, we gotta turn HB on
        if locationType.HB in exclude_list and (
            locationType.TTR not in exclude_list or locationType.CoR not in exclude_list
        ):
            exclude_list.remove(locationType.HB)

        # If OC is off, but Cups are on, gotta turn OC on
        if locationType.OC in exclude_list and (locationType.OCCups not in exclude_list):
            exclude_list.remove(locationType.OC)

        # find out if we need to turn on the creations world (default yes, this will disable it)
        if (
            locationType.SYNTH in exclude_list
            and locationType.Puzzle in exclude_list
            and not settings.shop_hintable
        ):
            exclude_list.append(locationType.Creations)

        # make sure vanilla worlds are in the tracker
        for vanilla in settings.vanillaLocations:
            if vanilla in exclude_list:
                exclude_list.remove(vanilla)

        return exclude_list

    @staticmethod
    def world_to_vanilla_items() -> dict[locationType, list[InventoryItem]]:
        """
        Returns a dictionary of worlds to a list of vanilla items in that world.
        """
        return {
            locationType.Level: [
                ability.SecondChance,
                ability.OnceMore,
            ],
            locationType.FormLevel: [
                form.ValorForm,
                form.WisdomForm,
                form.FinalForm,
                form.MasterForm,
                form.LimitForm,
            ],
            locationType.Atlantica: [magic.Blizzard],
            locationType.TWTNW: [
                magic.Magnet,
                storyunlock.WayToTheDawn,
            ],
            locationType.PR: [
                magic.Magnet,
                summon.FeatherCharm,
                storyunlock.SkillAndCrossbones,
            ],
            locationType.DC: [
                misc.TornPages,
                magic.Reflect,
                form.WisdomForm,
                storyunlock.DisneyCastleKey
            ],
            locationType.HUNDREDAW: [
                magic.Cure,
                misc.TornPages,
            ],
            locationType.Agrabah: [
                summon.LampCharm,
                magic.Fire,
                misc.TornPages,
                storyunlock.Scimitar,
            ],
            locationType.BC: [
                magic.Cure,
                magic.Reflect,
                storyunlock.BeastsClaw,
            ],
            locationType.TT: [
                form.ValorForm,
                form.LimitForm,
                storyunlock.IceCream,
                # storyunlock.Picture,
            ],
            locationType.SP: [
                magic.Reflect,
                storyunlock.IdentityDisk,
            ],
            locationType.HT: [
                magic.Magnet,
                storyunlock.BoneFist,
            ],
            locationType.PL: [
                misc.TornPages,
                magic.Fire,
                magic.Thunder,
                storyunlock.ProudFang,
            ],
            locationType.LoD: [
                magic.Thunder,
                misc.TornPages,
                storyunlock.SwordOfTheAncestor,
            ],
            locationType.OC: [
                magic.Thunder,
                storyunlock.BattlefieldsOfWar,
            ],
            locationType.HB: [
                magic.Fire,
                magic.Blizzard,
                summon.BaseballCharm,
                summon.UkuleleCharm,
                form.MasterForm,
                magic.Cure,
                misc.TornPages,
                storyunlock.MembershipCard,
            ],
            locationType.STT: [
                form.ValorForm,
                form.LimitForm,
                storyunlock.NaminesSketches
            ],
            locationType.Creations: [],
            locationType.Critical: [],
            locationType.Free: []
        }

    @staticmethod
    def item_to_vanilla_world() -> dict[InventoryItem, list[locationType]]:
        """
        Returns a dictionary of item to the list of vanilla worlds that contain that item.
        """
        result: dict[InventoryItem, list[locationType]] = {}
        for world, item_list in HintUtils.world_to_vanilla_items().items():
            for item in item_list:
                if item not in result:
                    result[item] = []
                result[item].append(world)
        return result

    @staticmethod
    def point_hint_report_assignment(
        settings: RandomizerSettings,
        world_items: WorldItems,
        point_data: list[PointHintData],
    ) -> dict[int, dict[str, Any]]:
        prevent_self_hinting = settings.prevent_self_hinting
        report_number_to_world_to_item = []
        for report_number in range(1, 14):
            for p in point_data:
                if (
                    not prevent_self_hinting
                    or world_items.report_information[report_number]["FoundIn"] != p.world
                ):
                    for cand in p.candidate_hints():
                        report_number_to_world_to_item.append((report_number, p.world, cand))

        def pick_item(
                input_report_num: int,
                input_world: locationType,
                input_data: list[tuple[int, locationType, KH2Item]]
        ) -> tuple[Optional[int], Optional[locationType], Optional[KH2Item]]:
            filtered_list = [
                (r, w, i) for r, w, i in input_data if w == input_world and r == input_report_num
            ]
            if len(filtered_list) == 0:
                return None, None, None
            return random.choice(filtered_list)

        def reduce_list(
                input_report_num: int,
                input_world: Optional[locationType],
                input_item: Optional[KH2Item],
                input_data: list[tuple[int, locationType, KH2Item]]
        ) -> list[tuple[int, locationType, KH2Item]]:
            filtered_list = [(r, w, i) for r, w, i in input_data if r != input_report_num]
            filtered_list = [
                (r, w, i) for r, w, i in filtered_list if input_world != w or input_item != i
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
    ) -> dict[int, dict[str, Any]]:
        prevent_self_hinting: bool = settings.prevent_self_hinting
        augmented_jsmartee_data = copy.deepcopy(jsmartee_data)
        # populate the hintable world list with ones that have valid items
        hintable_worlds = [j.world for j in augmented_jsmartee_data]
        # if we aren't progression hints, we need 13 hints at least
        if len(hintable_worlds) < 13:
            # if there aren't 13 worlds to hint, add the difference as zero IC worlds
            excluded_worlds = list(
                set(HintUtils.hintable_worlds()).difference(hintable_worlds)
            )
            augmented_jsmartee_data = augmented_jsmartee_data + [
                JsmarteeHintData(world_items, w)
                for w in excluded_worlds[0: (13 - len(augmented_jsmartee_data))]
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

        def pick_world(
                input_report_num: int,
                input_world: locationType,
                input_data: list[tuple[int, locationType, int]]
        ) -> tuple[Optional[int], Optional[locationType], Optional[int]]:
            filtered_list = [
                (r, w, c) for r, w, c in input_data if w == input_world and r == input_report_num
            ]
            if len(filtered_list) == 0:
                return None, None, None
            return random.choice(filtered_list)

        def reduce_list(
                input_report_num: Optional[int],
                input_world: Optional[locationType],
                input_data: list[tuple[int, locationType, int]]
        ) -> list[tuple[int, locationType, int]]:
            filtered_list = [(r, w, c) for r, w, c in input_data if r != input_report_num]
            filtered_list = [(r, w, c) for r, w, c in filtered_list if input_world != w]
            return filtered_list

        proof_worlds = [
            world_items.proof_of_connection_world,
            world_items.proof_of_peace_world,
            world_items.proof_of_nonexistence_world,
        ]
        # validation for starting proof locations
        proof_worlds = [
            proof_world for proof_world in proof_worlds if proof_world in HintUtils.hintable_worlds()
        ]
        priority_worlds = []
        # TODO add warning about using visit locks with Jsmartee in RandomizerSettings
        if locationType.FormLevel in proof_worlds:
            # add the worlds with forms to priority list
            for world, item_list in world_items.world_to_item_list.items():
                if any([i.ItemType == itemType.FORM for i in item_list]):
                    priority_worlds.append(world)
        if locationType.HUNDREDAW in proof_worlds:
            # add the worlds with pages to priority list
            for world, item_list in world_items.world_to_item_list.items():
                if any([i.ItemType == itemType.TORN_PAGE for i in item_list]):
                    priority_worlds.append(world)
        if locationType.Atlantica in proof_worlds:
            # add the worlds with thunders and magnets to priority list
            for world, item_list in world_items.world_to_item_list.items():
                if any([i.ItemType == itemType.THUNDER for i in item_list]):
                    priority_worlds.append(world)
                if any([i.ItemType == itemType.MAGNET for i in item_list]):
                    priority_worlds.append(world)

        full_priority_list = [proof_world for proof_world in proof_worlds]
        for world in priority_worlds:
            if world not in full_priority_list:
                full_priority_list.append(world)

        for _ in range(100):
            data = copy.deepcopy(report_number_to_world_to_count)
            priorities = copy.deepcopy(full_priority_list)

            # cull down the world list to a set of 13
            selected_worlds = copy.deepcopy(priorities)
            remaining_worlds = [world for world in hintable_worlds if world not in selected_worlds]
            random.shuffle(remaining_worlds)
            selected_worlds = selected_worlds + remaining_worlds
            selected_worlds = selected_worlds[0:13]

            # sanity check, if we already failed to select all priority worlds, fail
            if any(world not in selected_worlds for world in priorities):
                continue

            report_numbers = list(range(1, 14))
            random.shuffle(report_numbers)
            report_assignments = {}
            # try to assign the proof reports
            for index, world in enumerate(selected_worlds):
                chosen_report = report_numbers[index]
                selected_report, selected_world, selected_count = pick_world(
                    chosen_report, world, data
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
    ) -> dict[int, dict[str, Any]]:
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
    ) -> dict[int, dict[str, Any]]:
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
    ) -> dict[int, dict[str, Any]]:
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

    @staticmethod
    def location_hint_user_friendly_text(location: locationType) -> str:
        """
        Returns a user-friendly variation of the location's name for use in hints.
        """
        if location == locationType.Level:
            return "Sora's Heart"
        elif location == locationType.TWTNW:
            return "TWTNW"
        elif location == locationType.DC:
            return "Disney Castle"
        elif location == locationType.HUNDREDAW:
            return "100 Acre"
        else:
            return location.value

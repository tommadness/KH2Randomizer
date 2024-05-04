import base64
import copy
import json
import random
import textwrap
from itertools import permutations, chain
from typing import Optional, Any
from zipfile import ZipFile

from Class.exceptions import HintException
from Class.itemClass import KH2Item
from Class.newLocationClass import KH2Location
from List.ItemList import Items
from List.configDict import itemType, locationType, locationCategory, HintType
from List.inventory import ability, form, magic, misc, storyunlock, summon, proof
from List.location import weaponslot
from Module import version
from Module.Hints.HintOutput import HintOutput
from Module.Hints.HintUtils import (
    CommonTrackerInfo,
    HintUtils,
    JsmarteeHintData,
    PathHintData,
    PointHintData,
    WorldItems,
)
from Module.RandomizerSettings import RandomizerSettings
from Module.newRandomize import Randomizer
from Module.seedmod import SeedModBuilder


HintData = dict[str, Any]


class Hints:

    @staticmethod
    def generator_journal_hints(
        location_item_data: list[tuple[KH2Location, KH2Item]],
        settings: RandomizerSettings,
        hint_data: HintData,
    ):
        journal_data: dict[int, str] = {}
        for report_num in range(1, 14):
            journal_data[report_num] = ""
        # find any settings relating to journal hints
        independent_hints = settings.journal_hints != "Off"
        independent_hint_specific = settings.journal_hints == "exact"

        # if independent hints, need to make "useful" query on the randomized locations and items
        if independent_hints:
            Hints.independent_journal_hints(location_item_data, journal_data, independent_hint_specific)

        # add journal text to hintsText structure
        if "Reports" not in hint_data:
            hint_data["Reports"] = {}
            for report_num in range(1, 14):
                hint_data["Reports"][report_num] = {}
        for report_num in range(1, 14):
            hint_data["Reports"][report_num]["JournalText"] = journal_data[report_num]

    @staticmethod
    def get_journal_hint(
            location: KH2Location,
            item_data: KH2Item,
            location_item_data: list[tuple[KH2Location, KH2Item]],
            independent_hint_specific: bool,
    ) -> Optional[str]:
        """
        If applicable, returns hint text to be used in the journal for the given item at the given location. Returns
        None if the location is not hintable or the item is not one that should receive a journal hint.
        """

        location_id = location.LocationId
        if location_id == weaponslot.LocationId.KingdomKey:
            # Kinda useless to hint Kingdom Key
            return None

        items_to_find = [
            ability.Scan,
            ability.AerialRecovery,
            ability.Guard,
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
        if item_data.item not in items_to_find:
            return None

        hintable_worlds = [
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

        hinted_item_name = item_data.Name

        # if ability is on keyblade, check location of keyblade
        if locationCategory.WEAPONSLOT in location.LocationCategory:
            special_key_to_location = {
                weaponslot.LocationId.KingdomKeyD: "Valor Form",
                weaponslot.LocationId.AlphaWeapon: "Master Form",
                weaponslot.LocationId.OmegaWeapon: "Final Form"
            }
            if location_id in special_key_to_location:
                # Form keys we don't give additional information to avoid hinting the forms themselves
                return f"{hinted_item_name} is on {special_key_to_location[location_id]}'s Keyblade."

            # find the location of the keyblade
            keyblade_item = Items.weaponslot_id_to_keyblade_item(location_id)
            keyblade_location = next(
                key_loc for key_loc, key_item in location_item_data if key_item.Name == keyblade_item.name
            )
            hintable_world = next(
                (world for world in keyblade_location.LocationTypes if world in hintable_worlds), None
            )
            if hintable_world is None:
                # Not in a world we're allowed to hint
                return None

            world_text = HintUtils.location_hint_user_friendly_text(hintable_world)
            if independent_hint_specific:
                key_location_text = f"{world_text} - {keyblade_location.Description}"
                return f"{hinted_item_name} is at {key_location_text} (on {keyblade_item.name})."
            else:
                return f"{hinted_item_name} is in {world_text} (on {keyblade_item.name})."
        else:
            hintable_world = next((world for world in location.LocationTypes if world in hintable_worlds), None)
            if hintable_world is None:
                # Not in a world we're allowed to hint
                return None

            world_text = HintUtils.location_hint_user_friendly_text(hintable_world)
            if independent_hint_specific:
                return f"{hinted_item_name} is at {world_text} - {location.Description}."
            else:
                return f"{hinted_item_name} is in {world_text}."

    @staticmethod
    def independent_journal_hints(
        location_item_data: list[tuple[KH2Location, KH2Item]],
        journal_data: dict[int, str],
        independent_hint_specific: bool,
    ):
        all_possible_independent_hints = []
        for location, item_data in location_item_data:
            hint = Hints.get_journal_hint(location, item_data, location_item_data, independent_hint_specific)
            if hint is not None:
                all_possible_independent_hints.append(hint)

        # at this point, we should have all our hint text, just need to assign to each report
        report_index = 0
        while len(all_possible_independent_hints):
            journal_data[report_index + 1] += (all_possible_independent_hints[-1] + "\n\n")
            report_index = (report_index + 1) % 13
            all_possible_independent_hints.pop()

    @staticmethod
    def generate_hints_v2(randomizer: Randomizer, settings: RandomizerSettings) -> HintData:
        # this list is meant to disallow worlds from being hinted, since they will never have hintable items
        exclude_list = HintUtils.update_disabled_worlds_on_tracker(settings)
        location_item_tuples = HintUtils.convert_item_assignment_to_tuple(
            randomizer.assignments, randomizer.shop_items
        )

        common_tracker_data = CommonTrackerInfo(settings)
        world_items = WorldItems(location_item_tuples, common_tracker_data)
        hintable_worlds = [
            world for world in HintUtils.hintable_worlds() if world not in exclude_list
        ]
        hint_data = common_tracker_data.to_dict()
        hint_data["level_data"] = world_items.level_checks
        if settings.emblems:
            hint_data["emblems"] = {"max_emblems_available":settings.max_emblems_available,"num_emblems_needed":settings.num_emblems_needed}

        if settings.objective_rando:
            objective_locations = [o.Location for o in randomizer.objectives]
            # find these locations in location_item_tuples
            objective_tuples = [{"category":l_i[0].LocationCategory, "location_id":l_i[0].LocationId} for l_i in location_item_tuples if l_i[0].Description in objective_locations]
            # remove duplicates
            objective_tuples = [dict(t) for t in {tuple(d.items()) for d in objective_tuples}]
            
            hint_data["objective_list"] = [o.Name for o in randomizer.objectives]
            hint_data["objective_locations"] = objective_tuples
            hint_data["num_objectives_needed"] = settings.num_objectives_needed
        if settings.hintsType == HintType.SHANANAS:
            hint_data["world"] = world_items.world_to_item_ids()
            hint_data["Reports"] = copy.deepcopy(world_items.report_information)
            if common_tracker_data.progression_settings is not None:
                world_list = list(hint_data["world"].keys())
                random.shuffle(world_list)
                hint_data["world_order"] = world_list
        elif settings.hintsType == HintType.JSMARTEE:
            jsmartee_data = []
            for world in hintable_worlds:
                jsmartee_data.append(JsmarteeHintData(world_items, world))
            if common_tracker_data.progression_settings is not None:
                hint_data["Reports"] = HintUtils.jsmartee_progression_hints(
                    world_items, jsmartee_data
                )
            else:
                hint_data["Reports"] = HintUtils.jsmartee_hint_report_assignment(
                    settings, world_items, jsmartee_data
                )
        elif settings.hintsType == HintType.POINTS:
            hint_data["world"] = world_items.world_to_item_ids()
            if common_tracker_data.progression_settings is not None:
                world_list = list(hint_data["world"].keys())
                random.shuffle(world_list)
                hint_data["world_order"] = world_list
            point_data = []
            for world in hintable_worlds:
                point_data.append(
                    PointHintData(settings, common_tracker_data, world_items, world)
                )
            hint_data["Reports"] = HintUtils.point_hint_report_assignment(
                settings, world_items, point_data
            )
        elif settings.hintsType == HintType.SPOILER:
            hint_data["world"] = world_items.world_to_item_ids()
            hint_data["aux_data"] = world_items.item_ids_to_names()
            hint_data["Reports"] = HintUtils.spoiler_hint_assignment(
                settings, common_tracker_data, world_items, hintable_worlds
            )
        elif settings.hintsType == HintType.PATH:
            hint_data["world"] = world_items.world_to_item_ids()
            path_data = []
            for world in HintUtils.hintable_worlds():
                path_data.append(PathHintData(world_items, world))
            hint_data["Reports"] = HintUtils.path_hint_assignment(
                world_items,
                path_data,
                common_tracker_data,
            )
        elif settings.hintsType == HintType.DISABLED:
            # don't need to do anything extra
            pass
        else:
            raise HintException("Unable to generate hints for nonexistent hint system")

        hint_data["startingInventory"] = randomizer.starting_item_ids

        Hints.generator_journal_hints(location_item_tuples, settings, hint_data)
        return hint_data

    @staticmethod
    def write_hints(hint_data: HintData, out_zip: ZipFile):
        # too many things in unhinted now to not send the tracker a file
        # if hint_data["hintsType"] != HintType.DISABLED:
        json_bytes = json.dumps(hint_data).encode("utf-8")
        if version.debug_mode():
            out_zip.writestr("HintFile_DebugHints.json", json_bytes)
        out_zip.writestr(
            "HintFile.Hints", base64.b64encode(json_bytes).decode("utf-8")
        )

    @staticmethod
    def write_hint_text(hint_data: HintData, mod: SeedModBuilder, journal_hints_spoiler: dict[str, str]):
        def convert_string_to_unicode(string: str, newlines: int = 0):
            return (
                    "".join(r"\u{:04X}".format(ord(character)) for character in textwrap.fill(string, width=30))
                    + "NEWLINE" * newlines
            )

        def hinted_world_text(input_hinted_world: Any) -> str:
            if isinstance(input_hinted_world, locationType):
                return HintUtils.location_hint_user_friendly_text(input_hinted_world)
            else:
                return str(input_hinted_world)

        for report_number in range(0, 13):
            report_data = hint_data["Reports"][report_number + 1]

            spoiler_text = ""
            encoded_text = ""

            hint_text = []
            if "ProgressionSettings" in hint_data:
                if hint_data["hintsType"] == HintType.POINTS:
                    hinted_world = report_data["World"]
                    hint_text.append(f"{hinted_world_text(hinted_world)} has {report_data['check']}.")
            else:
                if hint_data["hintsType"] == HintType.JSMARTEE:
                    hinted_world = report_data["World"]
                    check_count = report_data["Count"]
                    if check_count == 1:
                        hint_text.append(f"{hinted_world_text(hinted_world)} has {check_count} important check.")
                    else:
                        hint_text.append(f"{hinted_world_text(hinted_world)} has {check_count} important checks.")

                if hint_data["hintsType"] == HintType.PATH:
                    hint_text.append(report_data["Text"])

                if hint_data["hintsType"] == HintType.POINTS:
                    hinted_world = report_data["World"]
                    hint_text.append(f"{hinted_world_text(hinted_world)} has {report_data['check']}.")

                if hint_data["hintsType"] == HintType.SPOILER:
                    hinted_world = report_data["World"]
                    hint_text.append(f"{hinted_world_text(hinted_world)} has:")
                    for c in hint_data["world"][hinted_world]:
                        c_txt = hint_data["aux_data"][c]
                        hint_text.append(c_txt)

            for hint_text_instance in hint_text:
                spoiler_text += hint_text_instance + "\n"
                encoded_text += convert_string_to_unicode(hint_text_instance, newlines=1)
            spoiler_text += "\n"
            encoded_text += convert_string_to_unicode("", newlines=1)

            if "JournalText" in report_data:
                for line in report_data["JournalText"].splitlines():
                    stripped = line.strip()
                    if len(stripped) > 0:
                        spoiler_text += stripped + "\n\n"
                        encoded_text += convert_string_to_unicode(stripped, newlines=2)

            if "Location" in report_data:
                report_location = report_data["Location"]
                if isinstance(report_location, locationType):
                    report_location_text = HintUtils.location_hint_user_friendly_text(report_location)
                elif report_location == "":
                    report_location_text = "Sora's pocket"
                else:
                    report_location_text = report_location
                location_text = f"This report was found in {report_location_text}."
                spoiler_text += location_text + "\n\n"
                encoded_text += convert_string_to_unicode(location_text, newlines=2)

            if report_number < 10:
                report_message_id = 14052 + report_number * 2
            else:  # for some god awful reason, report 11-13 aren't contiguous with 1-10
                report_message_id = 14255 + (report_number - 10) * 2

            mod.journal_txt.add_message(
                message_id=report_message_id,
                en=encoded_text
            )

            journal_hints_spoiler[f"Report {report_number + 1}"] = spoiler_text.strip()

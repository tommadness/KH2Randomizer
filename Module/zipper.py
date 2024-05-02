import base64
import io
import json
import random
from itertools import accumulate
from typing import Optional, Any
from zipfile import ZipFile, ZIP_DEFLATED

import yaml

from Class import settingkey
from Class.exceptions import GeneratorException
from Class.itemClass import ItemEncoder
from Class.newLocationClass import KH2Location
from Class.openkhmod import ATKPObject, AttackEntriesOrganizer, ModYml
from Class.seedSettings import SeedSettings, ExtraConfigurationData, makeKHBRSettings
from List import ChestList
from List.DropRateIds import id_to_enemy_name
from List.ItemList import Items
from List.LvupStats import DreamWeaponOffsets
from List.ObjectiveList import KH2Objective
from List.configDict import itemType, locationCategory, locationType, BattleLevelOption
from List.inventory import bonus
from List.location import simulatedtwilighttown as stt
from Module import hashimage
from Module.RandomizerSettings import RandomizerSettings
from Module.battleLevels import BtlvViewer
from Module.cosmetics import CosmeticsMod
from Module.hints import Hints, HintData
from Module.knockbackTypes import KnockbackTypes
from Module.multiworld import MultiWorldOutput
from Module.newRandomize import Randomizer, SynthesisRecipe, ItemAssignment
from Module.resources import resource_path
from Module.seedmod import SeedModBuilder, ChestVisualAssignment, CosmeticsModAppender
from Module.spoilerLog import (
    item_spoiler_dictionary,
    levelStatsDictionary,
    synth_recipe_dictionary,
    weapon_stats_dictionary,
    objectives_dictionary,
)
from Module.version import LOCAL_UI_VERSION


def noop(self, *args, **kw):
    pass


def number_to_bytes(item) -> tuple[int, int]:
    # for byte1, find the most significant bits from the item Id
    item_byte1 = item >> 8
    # for byte0, isolate the least significant bits from the item Id
    item_byte0 = item & 0x00FF
    return item_byte0, item_byte1


def bytes_to_number(byte0, byte1=0) -> int:
    return int(byte0) + int(byte1 << 8)


def _assignment_subset(
    assigned: list[ItemAssignment], categories: list[locationCategory]
) -> list[ItemAssignment]:
    return [
        assignment
        for assignment in assigned
        if any(item is assignment.location.LocationCategory for item in categories)
    ]


def _assignment_subset_from_type(
    assigned: list[ItemAssignment], types: list[locationType]
) -> list[ItemAssignment]:
    return [
        assignment
        for assignment in assigned
        if any(item in assignment.location.LocationTypes for item in types)
    ]


def _run_khbr(
    platform: str, enemy_options: dict, mod_yml: ModYml, out_zip: ZipFile
) -> tuple[Optional[str], dict[str, list]]:
    if platform == "PC":
        enemy_options["memory_expansion"] = True
    else:
        enemy_options["memory_expansion"] = False

    enemy_spoilers = _invoke_khbr_with_overrides(enemy_options, mod_yml.data, out_zip)

    lines = enemy_spoilers.split("\n")

    current_key = ""
    enemy_spoilers_json = {}
    for line in lines:
        if "\t" in line:
            modded_line = line.replace("\t", "")
            enemies = modded_line.split(" became ")
            # this is adding to the current list
            new_entry = {"original": enemies[0], "new": enemies[1]}
            enemy_spoilers_json[current_key].append(new_entry)
        elif line != "":
            current_key = line
            enemy_spoilers_json[current_key] = []
    if enemy_spoilers_json:
        out_zip.writestr(
            "enemies.rando",
            base64.b64encode(json.dumps(enemy_spoilers_json).encode("utf-8")).decode(
                "utf-8"
            ),
        )
        # for boss_replacement in enemy_spoilers_json["BOSSES"]:
        #     print(f"{boss_replacement['original']} {boss_replacement['new']}")

    return enemy_spoilers, enemy_spoilers_json


def _add_cosmetics(out_zip: ZipFile, mod_yml: ModYml, settings: SeedSettings):
    appender = CosmeticsModAppender(out_zip=out_zip, mod_yml=mod_yml)

    mod_yml.add_assets(CosmeticsMod.randomize_field2d(settings))
    mod_yml.add_assets(CosmeticsMod.randomize_itempics(settings))
    mod_yml.add_assets(CosmeticsMod.randomize_end_screen(settings))

    keyblade_assets, keyblade_replacements = CosmeticsMod.randomize_keyblades(settings)
    appender.write_keyblade_rando_assets(keyblade_assets, keyblade_replacements)

    music_assets, music_replacements = CosmeticsMod.randomize_music(settings)
    appender.write_music_rando_assets(music_assets, music_replacements)

    from Module.cosmeticsmods.texture import TextureRecolorizer
    texture_assets = TextureRecolorizer(settings).recolor_textures()
    mod_yml.add_assets(texture_assets)

    if settings.get(settingkey.RANDO_THEMED_TEXTURES):
        appender.write_rando_themed_texture_assets()


class SynthList:
    def __init__(self, offset: int, binary: bytearray):
        self.offset = offset
        self.id = bytes_to_number(binary[0], binary[1])
        self.reward = bytes_to_number(binary[2], binary[3])
        self.reward_type = bytes_to_number(binary[4])
        self.material_type = bytes_to_number(binary[5])
        self.material_rank = bytes_to_number(binary[6])
        self.condition_type = bytes_to_number(binary[7])
        self.count_needed = bytes_to_number(binary[8], binary[9])
        self.unlock_event_shop = bytes_to_number(binary[10], binary[11])

    def __str__(self):
        if self.reward_type == 1:
            return f"{self.offset}: ID{self.id} R{self.reward} RT{self.reward_type} MT{self.material_type} MR{self.material_rank} CT{self.condition_type} CN{self.count_needed}"
        else:
            return ""


class DropRates:
    def __init__(self, offset: int, binary: bytearray):
        self.offset = offset
        self.id = bytes_to_number(binary[0], binary[1])
        self.small_hp = bytes_to_number(binary[2])
        self.big_hp = bytes_to_number(binary[3])
        self.big_munny = bytes_to_number(binary[4])
        self.medium_munny = bytes_to_number(binary[5])
        self.small_munny = bytes_to_number(binary[6])
        self.small_mp = bytes_to_number(binary[7])
        self.big_mp = bytes_to_number(binary[8])
        self.small_drive = bytes_to_number(binary[9])
        self.big_drive = bytes_to_number(binary[10])
        self.item1 = bytes_to_number(binary[12], binary[13])
        self.item1_chance = bytes_to_number(binary[14], binary[15])
        self.item2 = bytes_to_number(binary[16], binary[17])
        self.item2_chance = bytes_to_number(binary[18], binary[19])
        self.item3 = bytes_to_number(binary[20], binary[21])
        self.item3_chance = bytes_to_number(binary[22], binary[23])

    def __str__(self):
        if True:  # self.item1_chance and self.id not in id_to_enemy_name:
            dummy = ""
            return f"{self.id} {(id_to_enemy_name[self.id] if self.id in id_to_enemy_name else dummy)} \n HP ({self.small_hp},{self.big_hp}) \n MP ({self.small_mp},{self.big_mp}) \n Munny ({self.small_munny},{self.medium_munny},{self.big_munny}) \n Orbs ({self.small_drive},{self.big_drive}) Items: \n--- {self.item1} ({self.item1_chance/1.0}%)\n--- {self.item2} ({self.item2_chance/1.0}%)\n--- {self.item3} ({self.item3_chance/1.0}%)"
        # elif self.id in id_to_enemy_name:
        #     return f"{self.id} {id_to_enemy_name[self.id]}"
        # else:
        #     return ""


class SynthLocation:
    def __init__(self, loc: int, item: int, in_recipe: SynthesisRecipe):
        self.location = loc
        self.item = item
        self.requirements = [(0, 0)] * 6
        self.unlock_rank = in_recipe.unlock_rank
        for i, recipe_requirement in enumerate(in_recipe.requirements):
            self.requirements[i] = (
                recipe_requirement.synth_item.Id,
                recipe_requirement.amount,
            )

    def get_starting_location(self) -> int:
        # header bytes + offset to the specific recipe + skip over the recipe bytes
        return 16 + self.location * 32 + 2

    def get_bytes(self) -> list[int]:
        binary = [self.unlock_rank, 0]  # unlock condition/rank
        item_byte0, item_byte1 = number_to_bytes(self.item)
        # add the item for this recipe
        binary.append(item_byte0)
        binary.append(item_byte1)
        # add the item as the upgraded version
        binary.append(item_byte0)
        binary.append(item_byte1)

        for req in self.requirements:
            item_byte0, item_byte1 = number_to_bytes(req[0])
            # add the item as an ingredient
            binary.append(item_byte0)
            binary.append(item_byte1)
            item_byte0, item_byte1 = number_to_bytes(req[1])
            # add the amount of that ingredient
            binary.append(item_byte0)
            binary.append(item_byte1)
        return binary


# (output zip, spoiler log, enemy log)
SeedZipResult = tuple[io.BytesIO, Optional[str], Optional[str]]
SeedNotZipResult = tuple[Optional[str], Optional[str]]


def _invoke_khbr_with_overrides(
    enemy_options: dict, mod: dict[str, Any], out_zip: ZipFile
):
    """
    A function that mimics the call to generateToZip in khbr. Splitting this out to allow for granular control of
    khbr's boss placement.
    """
    from khbr.randomizer import Randomizer as BossEnemyRandomizer
    from khbr.KH2.EnemyManager import EnemyManager
    from khbr.textutils import create_spoiler_text

    random.seed(
        str(enemy_options)
    )  # seed boss/enemy with enemy options, which should include the seed name
    del enemy_options["seed_name"]  # remove it so khbr doesn't complain

    khbr_randomizer = BossEnemyRandomizer()

    # get kh2's data
    game_data = khbr_randomizer._get_game("kh2")

    # make a new enemy manager with custom jsons
    game_data.enemy_manager = EnemyManager(resource_path("static/khbr_override/"))

    # ###  MANUAL STEP: updating records
    # import os
    # full_records = game_data.enemy_manager.create_enemy_records(ispc=False)
    # name = "full_enemy_records.json"
    # json.dump(full_records, open(os.path.join(resource_path("static/khbr_override/"), name), "w"), indent=4)

    # full_records = game_data.enemy_manager.create_enemy_records(ispc=True)
    # name = "full_enemy_records_pc.json"
    # json.dump(full_records, open(os.path.join(resource_path("static/khbr_override/"), name), "w"), indent=4)

    # ### DEBUGGING
    # valid_boss_replacements = {}
    # boss_list = game_data.enemy_manager.get_boss_list(enemy_options)
    # for _,source_boss in boss_list.items():
    #     valid_boss_replacements[source_boss["name"]] = []
    # for _,source_boss in boss_list.items():
    #     for __,dest_boss in boss_list.items():
    #         if source_boss["name"]!=dest_boss["name"]:
    #             if not EnemyManager.isReplacementBlocked(source_boss,dest_boss):
    #                 valid_boss_replacements[source_boss["name"]].append(dest_boss["name"])
    # with open("valid_boss_replacements.json","w") as f:
    #     json.dump(valid_boss_replacements, f, indent=4)

    # make sure the options are formatted properly
    khbr_randomizer._validate_options(
        khbr_randomizer.get_options_cli(game_data), enemy_options
    )

    # actually perform the randomization
    randomization = game_data.perform_randomization(enemy_options)

    # add the assets to the zip and mod yml
    assets = game_data.generate_files(randomization=randomization, outzip=out_zip)
    mod["assets"].extend(assets)

    # create the spoiler log
    return create_spoiler_text(game_data.spoilers)

    ### Backup old way
    # enemySpoilers = khbr().generateToZip("kh2", enemy_options, mod, outZip)
    # return enemySpoilers


class SeedZip:
    def __init__(
        self,
        settings: RandomizerSettings,
        randomizer: Randomizer,
        hints: HintData,
        extra_data: ExtraConfigurationData,
        location_spheres: dict[KH2Location,int],
        multiworld: Optional[MultiWorldOutput] = None,
    ):
        self.settings = settings
        self.randomizer = randomizer
        self.hints = hints
        self.extra_data = extra_data
        self.location_spheres = location_spheres
        self.multiworld = multiworld

    def make_spoiler_without_zip(self) -> str:
        enemy_spoilers_json: dict[str, str] = {}

        settings = self.settings
        btlv_option_name = settings.battle_level_rando

        btlv = BtlvViewer()
        btlv.use_setting(
            btlv_option_name,
            battle_level_offset=settings.battle_level_offset,
            battle_level_range=settings.battle_level_range,
            battle_level_random_min_max=settings.battle_level_random_min_max,
        )
        battle_level_spoiler = btlv.get_spoiler()
        journal_hints_spoiler = {}
        spoiler_log_output = self.generate_spoiler_html(
            enemy_spoilers_json, battle_level_spoiler, journal_hints_spoiler
        )
        return spoiler_log_output

    def create_zip(self) -> SeedZipResult:
        settings = self.settings
        spoiler_log = settings.spoiler_log
        extra_data = self.extra_data
        tourney_gen = extra_data.tourney

        title = "Randomizer Seed"
        if spoiler_log and not tourney_gen:
            title += " w/ Spoiler"

        zip_data = io.BytesIO()
        spoiler_log_output: Optional[str] = None
        enemy_log_output: Optional[str] = None
        with ZipFile(zip_data, "w", ZIP_DEFLATED) as out_zip:
            yaml.emitter.Emitter.process_tag = noop
            mod = SeedModBuilder(title, out_zip)
            mod.add_base_assets()
            mod.add_base_messages(settings.seedHashIcons, settings.crit_mode)
            self.prepare_companion_damage_knockback(mod)

            if settings.dummy_forms:
                # convert the valor and final ids to their dummy values
                for a in self.randomizer.assignments:
                    for dummy_form_item in Items.getDummyFormItems():
                        if a.item.Name == dummy_form_item.Name:
                            a.item = dummy_form_item

            self.assign_treasures(mod)
            self.assign_levels(mod)
            self.assign_bonuses(mod)
            self.assign_form_levels(mod)
            self.assign_weapon_stats(mod)
            self.assign_starting_items(mod)

            enemy_spoilers, enemy_spoilers_json = self.run_khbr_if_needed(mod, out_zip)

            if self.multiworld:
                out_zip.writestr("multiworld.multi", json.dumps(self.multiworld()))

            self.generate_seed_hash_image(out_zip)
            self.create_puzzle_assets(mod)
            self.create_synth_assets(mod)
            if settings.as_data_split:
                mod.write_as_data_split_assets()
            if settings.disable_antiform:
                self.disable_antiform(mod)
            if settings.skip_carpet_escape:
                mod.write_skip_carpet_escape_assets()
            if settings.pr_map_skip:
                mod.write_map_skip_assets()
            if settings.block_cor_skip:
                mod.write_block_cor_skip_assets()
            if settings.block_shan_yu_skip:
                mod.write_block_shan_yu_skip_assets()
            if settings.atlantica_skip:
                mod.write_atlantica_tutorial_skip_assets()
            if settings.wardrobe_skip:
                mod.write_wardrobe_skip_assets()
            self.create_drop_rate_assets(mod)
            self.create_shop_rando_assets(mod)
            if settings.objective_rando:
                self.create_objective_rando_assets(mod,settings.num_objectives_needed, self.randomizer.objectives)
            if settings.emblems:
                self.create_emblem_rando_assets(mod,settings.num_emblems_needed)
            self.create_chest_visual_assets(mod)
            battle_level_spoiler = self.create_battle_level_rando_assets(mod)
            journal_hints_spoiler: dict[str, str] = {}

            hints = self.hints
            if hints is not None:
                Hints.write_hints(hints, out_zip)
                Hints.write_hint_text(hints, mod, journal_hints_spoiler)

            if settings.roxas_abilities_enabled:
                boss_enabled = not settings.enemy_options.get("boss", False) in [
                    False,
                    "Disabled",
                ]
                mod.write_better_stt_assets(boss_enabled)
            
            if settings.keyblades_unlock_chests:
                mod.write_keyblade_locking_lua()

            if "beta" in LOCAL_UI_VERSION:
                print("Writing beta stuff")
                mod.write_goa_lua()

            self.add_cmd_list_modifications(mod)

            if spoiler_log or tourney_gen:
                # For a tourney seed, generate the spoiler log to return to the caller but don't include it in the zip
                spoiler_log_output = self.generate_spoiler_html(
                    enemy_spoilers_json, battle_level_spoiler, journal_hints_spoiler
                )
                if not tourney_gen:
                    out_zip.writestr("spoilerlog.html", spoiler_log_output)
                    out_zip.write(resource_path("static/KHMenu.otf"), "misc/KHMenu.otf")

                # For a tourney seed, return the enemy log to the caller but don't include it in the zip
                enemy_log_output = enemy_spoilers
                if enemy_spoilers and not tourney_gen:
                    out_zip.writestr("enemyspoilers.txt", enemy_spoilers)

            _add_cosmetics(out_zip=out_zip, mod_yml=mod.mod_yml, settings=settings.ui_settings)

            out_zip.write(resource_path("Module/icon.png"), "icon.png")

            mod.write_mod_ymls(
                include_main_mod_yml=False
            )  # We'll add the main mod.yml after the validation
            out_zip.close()
        zip_data.seek(0)

        new_data = mod.validate_and_write_mod_yml(zip_data, settings)

        return new_data, spoiler_log_output, enemy_log_output

    def run_khbr_if_needed(
        self, mod: SeedModBuilder, out_zip: ZipFile
    ) -> tuple[Optional[str], dict[str, list]]:
        enemy_options = self.settings.enemy_options

        def _should_run_khbr() -> bool:
            if not enemy_options.get("boss", False) in [False, "Disabled"]:
                return True
            if not enemy_options.get("enemy", False) in [False, "Disabled"]:
                return True
            if enemy_options.get("remove_damage_cap", False):
                return True
            if enemy_options.get("cups_give_xp", False):
                return True
            if enemy_options.get("retry_data_final_xemnas", False):
                return True
            if enemy_options.get("retry_dark_thorn", False):
                return True
            if enemy_options.get("costume_rando", False):
                return True
            if enemy_options.get("party_member_rando", False):
                return True
            if not enemy_options.get("remove_cutscenes", False) in [False, "Disabled"]:
                return True
            if not enemy_options.get("revenge_limit_rando", False) in [
                False,
                "Vanilla",
            ]:
                return True

            return False

        if _should_run_khbr():
            return _run_khbr(
                self.extra_data.platform, enemy_options, mod.mod_yml, out_zip
            )
        else:
            return None, {}

    def generate_spoiler_html(
            self,
            enemy_spoilers_json,
            battle_level_spoiler,
            journal_hints_spoiler: dict[str, str]
    ) -> str:
        settings = self.settings
        randomizer = self.randomizer
        platform = self.extra_data.platform

        if platform == "Both":
            platform = "PC/PCSX2"

        exp_multipliers_json = {
            "Summon": {
                "multiplier": settings.summon_exp_multiplier,
                "values": list(accumulate(settings.summon_exp())),
            },
            "Valor": {
                "multiplier": settings.valor_exp_multiplier,
                "values": list(accumulate(settings.valor_exp())),
            },
            "Wisdom": {
                "multiplier": settings.wisdom_exp_multiplier,
                "values": list(accumulate(settings.wisdom_exp())),
            },
            "Limit": {
                "multiplier": settings.limit_exp_multiplier,
                "values": list(accumulate(settings.limit_exp())),
            },
            "Master": {
                "multiplier": settings.master_exp_multiplier,
                "values": list(accumulate(settings.master_exp())),
            },
            "Final": {
                "multiplier": settings.final_exp_multiplier,
                "values": list(accumulate(settings.final_exp())),
            },
        }
        sora_items_json = item_spoiler_dictionary(
            item_assignments=randomizer.assignments,
            starting_inventory_ids=randomizer.starting_item_ids,
            shop_items=randomizer.shop_items,
            weights=randomizer.location_weights,
            location_spheres=self.location_spheres,
        )
        donald_items_json = item_spoiler_dictionary(randomizer.donald_assignments)
        goofy_items_json = item_spoiler_dictionary(randomizer.goofy_assignments)
        synthesis_recipe_json = synth_recipe_dictionary(
            randomizer.assignments, randomizer.synthesis_recipes
        )
        settings_spoiler_json = self.settings.ui_settings.settings_spoiler_json()
        weapon_stats_spoiler = weapon_stats_dictionary(
            sora_assignments=randomizer.assignments,
            donald_assignments=randomizer.donald_assignments,
            goofy_assignments=randomizer.goofy_assignments,
            weapons=randomizer.weapon_stats,
        )
        objectives_json = objectives_dictionary(randomizer.objectives)

        with open(resource_path("static/spoilerlog.html")) as spoiler_site:
            return (
                spoiler_site.read()
                .replace("{SEED_NAME_STRING}", settings.random_seed)
                .replace("{SEED_STRING}", settings.seed_string)
                .replace("{PLATFORM_GENERATED}", platform)
                .replace("{LEVEL_STATS_JSON}", json.dumps(levelStatsDictionary(randomizer.level_stats)))
                .replace("{FORM_EXP_JSON}", json.dumps(exp_multipliers_json))
                .replace("{DEPTH_VALUES_JSON}", json.dumps(randomizer.location_weights.weights))
                .replace("{SORA_ITEM_JSON}", json.dumps(sora_items_json, indent=4, cls=ItemEncoder))
                .replace("{DONALD_ITEM_JSON}", json.dumps(donald_items_json, indent=4, cls=ItemEncoder))
                .replace("{GOOFY_ITEM_JSON}", json.dumps(goofy_items_json, indent=4, cls=ItemEncoder))
                .replace("{BOSS_ENEMY_JSON}", json.dumps(enemy_spoilers_json))
                .replace("{BATTLE_LEVEL_JSON}", json.dumps(battle_level_spoiler))
                .replace("{SYNTHESIS_RECIPE_JSON}", json.dumps(synthesis_recipe_json))
                .replace("{WEAPON_STATS_JSON}", json.dumps(weapon_stats_spoiler))
                .replace("{JOURNAL_HINTS_JSON}", json.dumps(journal_hints_spoiler))
                .replace("{OBJECTIVES_JSON}", json.dumps(objectives_json))
                .replace("{SETTINGS_JSON}", json.dumps(settings_spoiler_json))
                .replace("PromiseCharm", "Promise Charm")
            )

    def generate_seed_hash_image(self, out_zip: ZipFile):
        hash_icons = self.settings.seedHashIcons
        image_data = hashimage.generate_seed_hash_image(hash_icons, use_bitmap=False)
        out_zip.writestr("preview.png", image_data)
        out_zip.writestr("misc/randoseed-hash-icons.csv", ",".join(hash_icons))

    def create_battle_level_rando_assets(
        self, mod: SeedModBuilder
    ) -> dict[locationType, list[int]]:
        settings = self.settings
        btlv_option_name = settings.battle_level_rando

        btlv = BtlvViewer()
        btlv.use_setting(
            btlv_option_name,
            battle_level_offset=settings.battle_level_offset,
            battle_level_range=settings.battle_level_range,
            battle_level_random_min_max=settings.battle_level_random_min_max,
        )
        if (
            (btlv_option_name == BattleLevelOption.NORMAL.name)
            or (
                btlv_option_name == BattleLevelOption.OFFSET.name
                and settings.battle_level_offset == 0
            )
            or (
                btlv_option_name == BattleLevelOption.RANDOM_WITHIN_RANGE.name
                and settings.battle_level_range == 0
            )
        ):
            return btlv.get_spoiler()

        modified_battle_level_binary = btlv.write_modifications()
        mod.write_battle_level_assets(modified_battle_level_binary)

        return btlv.get_spoiler()

    def add_cmd_list_modifications(self, mod: SeedModBuilder):
        settings = self.settings
        if settings.roxas_abilities_enabled and not settings.disable_final_form:
            cmd_yml = "better_stt/CmdList.yml"
        elif settings.roxas_abilities_enabled and settings.disable_final_form:
            cmd_yml = "better_stt/CmdListWDisableFinal.yml"
        elif not settings.roxas_abilities_enabled and settings.disable_final_form:
            cmd_yml = "disable_final_form.yml"
        else:  # Roxas abilities not enabled and final form not disabled - nothing to do
            return
        mod.write_cmd_list_modifications(modified_cmd_list_yml=cmd_yml)

    def create_puzzle_assets(self, mod: SeedModBuilder):
        if locationType.Puzzle not in self.settings.disabledLocations:
            assigned_puzzles = _assignment_subset_from_type(
                self.randomizer.assignments, [locationType.Puzzle]
            )
            with open(resource_path("static/puzzle.bin"), "rb") as puzzleBar:
                modified_puzzle_binary = bytearray(puzzleBar.read())
                for puzz in assigned_puzzles:
                    byte0 = 20 + puzz.location.LocationId * 16
                    byte1 = 20 + puzz.location.LocationId * 16 + 1
                    item = puzz.item.Id

                    item_byte_0, item_byte_1 = number_to_bytes(item)
                    modified_puzzle_binary[byte0] = item_byte_0
                    modified_puzzle_binary[byte1] = item_byte_1
                mod.write_puzzle_assets(modified_puzzle_binary)

    def create_drop_rate_assets(self, mod: SeedModBuilder):
        settings = self.settings
        global_jackpot = settings.global_jackpot
        global_lucky_lucky = settings.global_lucky
        fast_urns = settings.fast_urns
        rich_enemies = settings.rich_enemies
        near_unlimited_mp = settings.unlimited_mp

        if (
            global_jackpot > 0
            or global_lucky_lucky > 0
            or fast_urns
            or rich_enemies
            or near_unlimited_mp
        ):
            all_drops = {}
            testing = []
            with open(resource_path("static/drops.bin"), "rb") as drops_bar:
                drops_binary = bytearray(drops_bar.read())
                for i in range(0, 184):
                    start_index = 8 + 24 * i
                    rate = DropRates(
                        start_index, drops_binary[start_index : start_index + 24]
                    )
                    all_drops[rate.id] = rate

                    if rate.id not in id_to_enemy_name:
                        testing.append(rate.id)

            spawnable_enemy_ids = [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                15,
                17,
                18,
                22,
                23,
                24,
                25,
                26,
                27,
                28,
                29,
                30,
                32,
                33,
                34,
                35,
                36,
                37,
                38,
                39,
                40,
                41,
                42,
                43,
                44,
                45,
                46,
                47,
                48,
                49,
                50,
                51,
                52,
                63,
                64,
                65,
                66,
                69,
                73,
                87,
                88,
                89,
                96,
                112,
                171,
                172,
                173,
                174,
                175,
                176,
                177,
                178,
                179,
                180,
                181,
                182,
            ]
            urn_ids = [70, 71]
            stt_enemies = [119, 120, 121, 130, 145]
            struggles = [122, 131, 132]

            modded_ids = []

            if rich_enemies:
                for drop in all_drops.values():
                    if drop.id in spawnable_enemy_ids:
                        modded_ids.append(drop.id)
                        drop.medium_munny = max(drop.medium_munny, 2)
                        drop.small_munny = max(drop.small_munny, 2)
            if near_unlimited_mp:
                for drop in all_drops.values():
                    if drop.id in spawnable_enemy_ids:
                        modded_ids.append(drop.id)
                        drop.big_mp = max(drop.big_mp, 5)
                        drop.small_mp = max(drop.small_mp, 5)

            if global_lucky_lucky > 0:
                for drop in all_drops.values():
                    if drop.item1 != 0:
                        modded_ids.append(drop.id)
                        drop.item1_chance = min(
                            drop.item1_chance
                            + (drop.item1_chance // 2) * global_lucky_lucky,
                            100,
                        )
                    if drop.item2 != 0:
                        modded_ids.append(drop.id)
                        drop.item2_chance = min(
                            drop.item2_chance
                            + (drop.item2_chance // 2) * global_lucky_lucky,
                            100,
                        )
                    if drop.item3 != 0:
                        modded_ids.append(drop.id)
                        drop.item3_chance = min(
                            drop.item3_chance
                            + (drop.item3_chance // 2) * global_lucky_lucky,
                            100,
                        )
            if global_jackpot > 0:
                for drop in all_drops.values():
                    modded_ids.append(drop.id)
                    drop.small_hp = min(
                        drop.small_hp + (drop.small_hp // 2) * global_jackpot, 64
                    )
                    drop.big_hp = min(
                        drop.big_hp + (drop.big_hp // 2) * global_jackpot, 64
                    )
                    drop.big_munny = min(
                        drop.big_munny + (drop.big_munny // 2) * global_jackpot, 64
                    )
                    drop.medium_munny = min(
                        drop.medium_munny + (drop.medium_munny // 2) * global_jackpot,
                        64,
                    )
                    drop.small_munny = min(
                        drop.small_munny + (drop.small_munny // 2) * global_jackpot, 64
                    )
                    drop.small_mp = min(
                        drop.small_mp + (drop.small_mp // 2) * global_jackpot, 64
                    )
                    drop.big_mp = min(
                        drop.big_mp + (drop.big_mp // 2) * global_jackpot, 64
                    )
                    drop.small_drive = min(
                        drop.small_drive + (drop.small_drive // 2) * global_jackpot, 64
                    )
                    drop.big_drive = min(
                        drop.big_drive + (drop.big_drive // 2) * global_jackpot, 64
                    )

            if fast_urns:
                for u in urn_ids:
                    modded_ids.append(u)
                    all_drops[u].big_hp = 64

            for drop in all_drops.values():
                if drop.id in modded_ids:
                    mod.prize_table.add_prize(
                        identifier=drop.id,
                        small_hp_orbs=drop.small_hp,
                        big_hp_orbs=drop.big_hp,
                        big_money_orbs=drop.big_munny,
                        medium_money_orbs=drop.medium_munny,
                        small_money_orbs=drop.small_munny,
                        small_mp_orbs=drop.small_mp,
                        big_mp_orbs=drop.big_mp,
                        small_drive_orbs=drop.small_drive,
                        big_drive_orbs=drop.big_drive,
                        item_1=drop.item1,
                        item_1_percentage=drop.item1_chance,
                        item_2=drop.item2,
                        item_2_percentage=drop.item2_chance,
                        item_3=drop.item3,
                        item_3_percentage=drop.item3_chance,
                    )

    def create_objective_rando_assets(self, mod: SeedModBuilder, num_objectives_needed: int, objective_list: list[KH2Objective]):
        mod.add_objective_randomization_mods(num_objectives_needed, objective_list)
        mod.items.add_item(
            item_id=363,
            item_type="Recipe",
            flag_0=0,
            flag_1=0,
            rank="C",
            stat_entry=0,
            name=47883,
            description=47884,
            shop_buy=num_objectives_needed,
            shop_sell=0,
            command=0,
            slot=189,
            picture=226,
            icon_1=0,
            icon_2=2,
        )
    def create_emblem_rando_assets(self, mod: SeedModBuilder, num_emblems_needed: int):
        mod.add_emblem_randomization_mods(num_emblems_needed)
        mod.items.add_item(
            item_id=363,
            item_type="Recipe",
            flag_0=0,
            flag_1=0,
            rank="C",
            stat_entry=0,
            name=47883,
            description=47884,
            shop_buy=num_emblems_needed,
            shop_sell=0,
            command=0,
            slot=189,
            picture=226,
            icon_1=0,
            icon_2=2,
        )

    def create_shop_rando_assets(self, mod: SeedModBuilder):
        shop_items = self.randomizer.shop_items
        if len(shop_items) > 0:
            items_for_shop = []
            keyblade_item_ids = [
                i.Id for i in shop_items if i.ItemType == itemType.KEYBLADE
            ]
            report_item_ids = [
                i.Id for i in shop_items if i.ItemType == itemType.REPORT
            ]
            story_unlock_ids = [
                i.Id for i in shop_items if i.ItemType == itemType.STORYUNLOCK
            ]
            consumable_ids = [i.Id for i in shop_items if i.ItemType == itemType.ITEM]
            used_ids = (
                keyblade_item_ids + report_item_ids + story_unlock_ids + consumable_ids
            )
            remaining_items = [i.Id for i in shop_items if i.Id not in used_ids]

            if len(keyblade_item_ids) > 0:
                for keyblade_id in keyblade_item_ids:
                    items_for_shop.append((keyblade_id, 400))

            if len(report_item_ids) > 0:
                for report_id in report_item_ids:
                    items_for_shop.append((report_id, 75 * (report_id - 225)))
                for report_number in range(13):
                    short_name = f"Ansem Report {report_number + 1}"
                    mod.messages.add_message(
                        message_id=46778 - 32768 + report_number * 2, en=short_name
                    )

            if len(story_unlock_ids) > 0:
                for story_unlock_id in story_unlock_ids:
                    items_for_shop.append((story_unlock_id, 500))

            if len(consumable_ids) > 0:
                consumable_price_map = {
                    4: 400,
                    7: 600,
                    274: 400,
                    275: 600,
                    276: 250,
                    277: 250,
                    278: 250,
                    279: 250,
                }
                for consumable_id in consumable_ids:
                    if consumable_id in consumable_price_map:
                        items_for_shop.append(
                            (consumable_id, consumable_price_map[consumable_id])
                        )
                    else:
                        items_for_shop.append((consumable_id, 700))

            if len(remaining_items) > 0:
                raise GeneratorException(
                    f"Trying to put unexpected items in the shop: {len(remaining_items)}"
                )
                # price_map = {itemRarity.COMMON:100,itemRarity.UNCOMMON:300, itemRarity.RARE:500, itemRarity.MYTHIC:1000}
                # for i in remaining_items:
                #     items_for_shop.append((i.Id,price_map[i.Rarity]))

            with open(resource_path("static/full_items.json"), "r") as item_json:
                all_item_jsons = json.loads(item_json.read())
                for item_id, price in items_for_shop:
                    item_json = None
                    for y in all_item_jsons["Items"]:
                        if y["Id"] == item_id:
                            item_json = y
                            break
                    item_json["ShopBuy"] = price
                    mod.items.add_item(
                        item_id=item_json["Id"],
                        item_type=item_json["Type"],
                        flag_0=item_json["Flag0"],
                        flag_1=item_json["Flag1"],
                        rank=item_json["Rank"],
                        stat_entry=item_json["StatEntry"],
                        name=item_json["Name"],
                        description=item_json["Description"],
                        shop_buy=item_json["ShopBuy"],
                        shop_sell=item_json["ShopSell"],
                        command=item_json["Command"],
                        slot=item_json["Slot"],
                        picture=item_json["Picture"],
                        icon_1=item_json["Icon1"],
                        icon_2=item_json["Icon2"],
                    )

            with open(resource_path("static/shop.bin"), "rb") as shop_bar:
                modified_shop_binary = bytearray(shop_bar.read())

                byte0, byte1 = number_to_bytes(80 + len(items_for_shop))
                modified_shop_binary[10] = byte0
                modified_shop_binary[11] = byte1

                byte0, byte1 = number_to_bytes(len(items_for_shop))

                # inventory 752
                modified_shop_binary[754] = byte0
                modified_shop_binary[755] = byte1
                byte0, byte1 = number_to_bytes(984)
                modified_shop_binary[756] = byte0
                modified_shop_binary[757] = byte1

                valid_start = bytes_to_number(
                    modified_shop_binary[12], modified_shop_binary[13]
                )
                for asset in range(len(items_for_shop)):
                    product_index = 984 + 2 * asset
                    valid_item_index = valid_start + (60 + asset) * 2
                    byte0, byte1 = number_to_bytes(items_for_shop[asset][0])
                    modified_shop_binary[product_index] = byte0
                    modified_shop_binary[product_index + 1] = byte1
                    modified_shop_binary[valid_item_index] = byte0
                    modified_shop_binary[valid_item_index + 1] = byte1

                mod.write_shop_assets(modified_shop_binary)

                # ## code below prints out the shop information in relevant format

                # print(f"file type: {bytes_to_number(binaryContent[4],binaryContent[5])}")
                # shop_list_count = bytes_to_number(binaryContent[6],binaryContent[7])
                # print(f"shop list count: {shop_list_count}")
                # inventory_list_count = bytes_to_number(binaryContent[8],binaryContent[9])
                # print(f"inventory entry count: {inventory_list_count}")
                # product_list_count = bytes_to_number(binaryContent[10],binaryContent[11])
                # print(f"product entry count: {product_list_count}")
                # valid_start = bytes_to_number(binaryContent[12],binaryContent[13])
                # print(f"valid items offset: {valid_start}")

                # shop_start = 16
                # print("Shop Entries")
                # for x in range(shop_list_count):
                #     shop_index = shop_start+x*24
                #     print(f"---- Shop ID: {bytes_to_number(binaryContent[shop_index+18])}")
                #     print(f"---- Inventory Amount: {bytes_to_number(binaryContent[shop_index+16],binaryContent[shop_index+17])}")
                #     print(f"---- Inventory Offset: {bytes_to_number(binaryContent[shop_index+20],binaryContent[shop_index+21])}")
                #     print("----------")

                # inventory_start = shop_start+shop_list_count*24
                # print("Inventory Entries")
                # for x in range(inventory_list_count):
                #     inventory_index = inventory_start+x*8
                #     print(f"---- Inventory Address: {inventory_index}")
                #     print(f"---- Unlock event: {bytes_to_number(binaryContent[inventory_index],binaryContent[inventory_index+1])}")
                #     print(f"---- Product Amount: {bytes_to_number(binaryContent[inventory_index+2],binaryContent[inventory_index+3])}")
                #     print(f"---- Product Offset: {bytes_to_number(binaryContent[inventory_index+4],binaryContent[inventory_index+5])}")
                #     print("----------")

                # product_start = inventory_start+inventory_list_count*8
                # print("Product Entries")
                # for x in range(product_list_count):
                #     product_index = product_start+x*2
                #     print(f"---- Address {product_index}")
                #     print(f"---- Product (Item Id):  {bytes_to_number(binaryContent[product_index],binaryContent[product_index+1])}")

                # print("Valid Items")
                # for x in range(63):
                #     valid_index = valid_start+x*2
                #     item_id = bytes_to_number(binaryContent[valid_index],binaryContent[valid_index+1])
                #     if item_id!=0:
                #         print(f"---- Valid Item (Item Id):  {item_id}")

    def create_synth_assets(self, mod: SeedModBuilder):
        if locationType.SYNTH in self.settings.disabledLocations:
            return

        randomizer = self.randomizer
        assigned_synth = _assignment_subset_from_type(
            randomizer.assignments, [locationType.SYNTH]
        )

        synth_items = []
        for assignment in assigned_synth:
            synth_items.append(
                SynthLocation(
                    assignment.location.LocationId,
                    assignment.item.Id,
                    [
                        r
                        for r in randomizer.synthesis_recipes
                        if r.location == assignment.location
                    ][0],
                )
            )

        with open(resource_path("static/synthesis.bin"), "rb") as recipes_bar:
            modified_recipes_binary = bytearray(recipes_bar.read())
            for synth_loc in synth_items:
                starting_byte = synth_loc.get_starting_location()
                data = synth_loc.get_bytes()

                for i, item in enumerate(data):
                    modified_recipes_binary[starting_byte + i] = 0xFF & item

        with open(resource_path("static/synthesis_reqs.bin"), "rb") as requirements_bar:
            modified_requirements_binary = bytearray(requirements_bar.read())

            # uncomment to see some data about the synth lists
            # index = 16
            # while index + 12 < len(modified_requirements_binary):
            #     print(SynthList(index, modified_requirements_binary[index:]))
            #     index += 12

            # 3/6 free dev 8,9 bytes from offset index
            free_dev1 = number_to_bytes(3)
            free_dev2 = number_to_bytes(6)
            modified_requirements_binary[36] = free_dev1[0]
            modified_requirements_binary[37] = free_dev1[1]
            modified_requirements_binary[72] = free_dev2[0]
            modified_requirements_binary[73] = free_dev2[1]

            # 1,3 ori+ version,
            # free_dev1 = number_to_bytes(1)
            # free_dev2 = number_to_bytes(3)
            # ori_plus_id = number_to_bytes(12) # not sure on this
            # binaryContent[33] = ori_plus_id[0]
            # binaryContent[35] = 0
            # binaryContent[36] = free_dev1[0]
            # binaryContent[37] = free_dev1[1]
            # binaryContent[69] = ori_plus_id[0]
            # binaryContent[71] = 0
            # binaryContent[72] = free_dev2[0]
            # binaryContent[73] = free_dev2[1]

            # uncomment to make all existing synth buyable conditions need 7 of that material
            # new_required_items = number_to_bytes(7)
            # start_index=376
            # for i in range(0,24):
            #     binaryContent[start_index+i*12+8] = new_required_items[0]
            #     binaryContent[start_index+i*12+9] = new_required_items[1]

        mod.write_synth_assets(modified_recipes_binary, modified_requirements_binary)

    def create_chest_visual_assets(self, mod: SeedModBuilder):
        if not self.settings.chests_match_item:
            return

        chest_item_assignments = _assignment_subset(
            self.randomizer.assignments, [locationCategory.CHEST]
        )
        chest_item_assignments = [
            trsr
            for trsr in chest_item_assignments
            if locationType.Puzzle not in trsr.location.LocationTypes
            and locationType.Critical not in trsr.location.LocationTypes
            and locationType.SYNTH not in trsr.location.LocationTypes
        ]

        chests_by_location_id = ChestList.chests_by_location_id()
        chest_visual_assignments: list[ChestVisualAssignment] = []
        for chest_item_assignment in chest_item_assignments:
            location = chest_item_assignment.location
            location_types = location.LocationTypes

            item = chest_item_assignment.item
            item_type = item.ItemType

            # Just in case because D/G starting items are labeled as free and chests
            if locationType.Free in location_types and location.LocationId in range(
                1, 3
            ):
                # print('party stating item?')
                continue
            if (
                location.name() == stt.CheckLocation.StationOfSerenityPotion
                and item_type
                in [
                    itemType.PROOF_OF_CONNECTION,
                    itemType.PROOF_OF_PEACE,
                    itemType.PROOF_OF_NONEXISTENCE,
                    itemType.PROMISE_CHARM,
                ]
            ):
                # if this chest in STT Station of Serenity is a proof, it can't be big since it's a tutorial chest
                continue

            # use location id to get chest index and name
            chest = chests_by_location_id[location.LocationId]
            chest_visual_id = ChestList.chest_visual_id(location_types, item_type)
            chest_visual_assignments.append(
                ChestVisualAssignment(
                    chest.ChestIndex, chest.spawn_file_path(), chest_visual_id
                )
            )

        mod.write_chest_visuals_assets(chest_visual_assignments)

    def assign_starting_items(self, mod: SeedModBuilder):
        def pad_items(item_list):
            while len(item_list) < 32:
                item_list.append(0)

        settings = self.settings
        randomizer = self.randomizer
        master_item_list = (
            Items.getItemList()
            + Items.getActionAbilityList()
            + Items.getSupportAbilityList()
            + Items.getKeybladeAbilityList()
            + Items.getLevelAbilityList()
            + [Items.getTT1Jailbreak()]
            + [Items.objectiveReportItem()]
            + [Items.getPromiseCharm()]
        )
        growth_abilities = [
            i.Id
            for i in master_item_list
            if (
                i.ItemType == itemType.GROWTH_ABILITY
            )
        ]
        sora_abilities = [
            i.Id
            for i in master_item_list
            if (
                i.ItemType == itemType.GROWTH_ABILITY
                or i.ItemType == itemType.ACTION_ABILITY
                or i.ItemType == itemType.SUPPORT_ABILITY
            )
        ]

        donald_starting_items = (
            [1 + 0x8000, 3 + 0x8000]
            + [
                l.item.Id
                for l in _assignment_subset_from_type(
                    randomizer.donald_assignments, [locationType.Free]
                )
            ]
        )
        mod.player_params.add_player(
            character_id=2,  # Donald Starting Items
            identifier=0,
            hp=20,
            mp=100,
            ap=settings.donald_ap - 5,
            armor_slot_max=1,
            accessory_slot_max=2,
            item_slot_max=2,
            items=donald_starting_items,
            padding=[0] * 52,
        )

        goofy_starting_items = (
            [
                1 + 0x8000,
                1 + 0x8000,
                1 + 0x8000,
            ]
            + [
                l.item.Id
                for l in _assignment_subset_from_type(
                    randomizer.goofy_assignments, [locationType.Free]
                )
            ]
        )
        mod.player_params.add_player(
            character_id=3,  # Goofy Starting Items
            identifier=0,
            hp=20,
            mp=100,
            ap=settings.goofy_ap - 4,
            armor_slot_max=2,
            accessory_slot_max=1,
            item_slot_max=3,
            items=goofy_starting_items,
            padding=[0] * 52,
        )

        ability_equip = 0x8000 if settings.auto_equip_abilities else 0
        sora_bdscript_abilities = [
            i
            for i in randomizer.starting_item_ids
            if i in sora_abilities and i not in growth_abilities
        ]
        sora_bdscript_items = [
            i
            for i in randomizer.starting_item_ids
            if i not in sora_abilities
        ]

        mod.add_sora_bdscript(sora_bdscript_items,sora_bdscript_abilities,settings.auto_equip_abilities)

        sora_starting_items = [
            l.item.Id
            for l in _assignment_subset_from_type(
                randomizer.assignments, [locationType.Critical]
            )
        ] + [
            i + ability_equip
            for i in randomizer.starting_item_ids
            if i in sora_abilities and i in growth_abilities
        ]
        pad_items(sora_starting_items)
        mod.player_params.add_player(
            character_id=1,  # Sora Starting Items (Crit)
            identifier=7,  # crit difficulty
            hp=20,
            mp=100,
            ap=settings.sora_ap,
            armor_slot_max=1,
            accessory_slot_max=1,
            item_slot_max=3,
            items=sora_starting_items[:7],
            padding=[0] * 52,
        )

        lion_sora_items = [32930, 32930, 32931, 32931, 33288, 33289, 33290, 33294]
        pad_items(lion_sora_items)
        mod.player_params.add_player(
            character_id=135,  # Lion Dash on Lion Sora
            identifier=0,
            hp=0,
            mp=0,
            ap=0,
            armor_slot_max=0,
            accessory_slot_max=0,
            item_slot_max=0,
            items=lion_sora_items,
            padding=[0] * 52,
        )

        mod.player_params.add_player(
            character_id=1,  # Sora Starting Items (Non Crit)
            identifier=0,
            hp=20,
            mp=100,
            ap=settings.sora_ap,
            armor_slot_max=1,
            accessory_slot_max=1,
            item_slot_max=3,
            items=sora_starting_items[7:],
            padding=[0] * 52,
        )

    def assign_weapon_stats(self, mod: SeedModBuilder):
        randomizer = self.randomizer
        weapons = []
        weapons.extend(
            _assignment_subset(randomizer.assignments, [locationCategory.WEAPONSLOT])
        )
        weapons.extend(
            _assignment_subset(
                randomizer.donald_assignments, [locationCategory.WEAPONSLOT]
            )
        )
        weapons.extend(
            _assignment_subset(
                randomizer.goofy_assignments, [locationCategory.WEAPONSLOT]
            )
        )

        for weapon in weapons:
            weapon_stats = next(
                stat
                for stat in randomizer.weapon_stats
                if stat.location == weapon.location
            )
            mod.items.add_stats(
                location_id=weapon.location.LocationId,
                attack=weapon_stats.strength,
                magic=weapon_stats.magic,
                defense=0,
                ability=weapon.item.Id,
                ability_points=0,
                unknown_08=100,
                fire_resistance=100,
                ice_resistance=100,
                lightning_resistance=100,
                dark_resistance=100,
                unknown_0d=100,
                general_resistance=100,
                unknown=0,
            )

    def disable_antiform(self, mod: SeedModBuilder):
        mod.form_levels.turn_off_anti()

    def assign_form_levels(self, mod: SeedModBuilder):
        form_dict = {
            0: "Summon",
            1: "Valor",
            2: "Wisdom",
            3: "Limit",
            4: "Master",
            5: "Final",
        }
        form_category_list = [
            locationCategory.SUMMONLEVEL,
            locationCategory.VALORLEVEL,
            locationCategory.WISDOMLEVEL,
            locationCategory.LIMITLEVEL,
            locationCategory.MASTERLEVEL,
            locationCategory.FINALLEVEL,
        ]
        for index, levelType in enumerate(form_category_list):
            levels = _assignment_subset(self.randomizer.assignments, [levelType])
            form_name = form_dict[index]
            for level_number in range(1, 8):
                for lvl in levels:
                    if lvl.location.LocationId == level_number:
                        form_exp = next(
                            exp
                            for exp in self.randomizer.form_level_exp
                            if exp == lvl.location
                        )
                        mod.form_levels.add_form_level(
                            form_name=form_name,
                            form_id=index,
                            form_level=lvl.location.LocationId,
                            ability=lvl.item.Id
                            if index != 0
                            else 0,  # making summon junk items zero
                            experience=form_exp.experience,
                            growth_ability_level=0,
                        )

    def assign_bonuses(self, mod: SeedModBuilder):
        self._assign_sora_bonuses(mod, self.randomizer.assignments)
        self._assign_party_bonuses(mod, 2, "Donald", self.randomizer.donald_assignments)
        self._assign_party_bonuses(mod, 3, "Goofy", self.randomizer.goofy_assignments)

    @staticmethod
    def _assign_party_bonuses(
        mod: SeedModBuilder,
        character_id: int,
        character_name: str,
        assigned_items: list[ItemAssignment],
    ):
        for bon in _assignment_subset(
            assigned_items, locationCategory.bonus_categories()
        ):
            item1 = bon.item.Id
            item2 = 0
            if bon.item2 is not None:
                item2 = bon.item2.Id
            mod.bonuses.add_bonus(
                reward_id=bon.location.LocationId,
                character_id=character_id,
                character_name=character_name,
                hp_increase=0,
                mp_increase=0,
                drive_gauge_increase=0,
                item_slot_upgrade=0,
                accessory_slot_upgrade=0,
                armor_slot_upgrade=0,
                bonus_item_1=item1,
                bonus_item_2=item2,
                padding=0,
            )

    @staticmethod
    def _assign_sora_bonuses(mod: SeedModBuilder, assigned_items: list[ItemAssignment]):
        for bon in _assignment_subset(
            assigned_items, locationCategory.bonus_categories()
        ):
            character_id = 1  # Sora id
            character_name = "Sora"
            if locationType.STT in bon.location.LocationTypes:
                character_id = 14  # Roxas id
                character_name = "Roxas"

            # determine if assigned item is a stat bonus, and if so, use the bonuses native stat update
            hp_increase = 0
            mp_increase = 0
            drive_increase = 0
            item_slot_increase = 0
            accessory_slot_increase = 0
            armor_slot_increase = 0
            bonus_item_1 = 0
            bonus_item_2 = 0

            assigned_item_1 = bon.item.item
            if assigned_item_1 == bonus.MaxHpUp:
                hp_increase += 5
            elif assigned_item_1 == bonus.MaxMpUp:
                mp_increase += 10
            elif assigned_item_1 == bonus.DriveGaugeUp:
                drive_increase += 1
            elif assigned_item_1 == bonus.ArmorSlotUp:
                armor_slot_increase += 1
            elif assigned_item_1 == bonus.AccessorySlotUp:
                accessory_slot_increase += 1
            elif assigned_item_1 == bonus.ItemSlotUp:
                item_slot_increase += 1
            else:
                bonus_item_1 = assigned_item_1.id

            if bon.item2 is not None:
                assigned_item_2 = bon.item2.item
                if assigned_item_2 == bonus.MaxHpUp:
                    hp_increase += 5
                elif assigned_item_2 == bonus.MaxMpUp:
                    mp_increase += 10
                elif assigned_item_2 == bonus.DriveGaugeUp:
                    drive_increase += 1
                elif assigned_item_2 == bonus.ArmorSlotUp:
                    armor_slot_increase += 1
                elif assigned_item_2 == bonus.AccessorySlotUp:
                    accessory_slot_increase += 1
                elif assigned_item_2 == bonus.ItemSlotUp:
                    item_slot_increase += 1
                else:
                    bonus_item_2 = assigned_item_2.id

            mod.bonuses.add_bonus(
                reward_id=bon.location.LocationId,
                character_id=character_id,
                character_name=character_name,
                hp_increase=hp_increase,
                mp_increase=mp_increase,
                drive_gauge_increase=drive_increase,
                item_slot_upgrade=item_slot_increase,
                accessory_slot_upgrade=accessory_slot_increase,
                armor_slot_upgrade=armor_slot_increase,
                bonus_item_1=bonus_item_1,
                bonus_item_2=bonus_item_2,
                padding=0,
            )

    def assign_levels(self, mod: SeedModBuilder):
        settings = self.settings
        levels = _assignment_subset(
            self.randomizer.assignments, [locationCategory.LEVEL]
        )
        level_checks = settings.max_level_checks

        # get the triple of items for each level
        items_for_sword_level = {}
        offsets = DreamWeaponOffsets()
        for sword_level in range(1, 100):
            sword_item = 0
            shield_item = 0
            staff_item = 0
            shield_level = (
                offsets.get_item_lookup_for_shield(level_checks, sword_level)
                if settings.split_levels
                else sword_level
            )
            staff_level = (
                offsets.get_item_lookup_for_staff(level_checks, sword_level)
                if settings.split_levels
                else sword_level
            )
            for lvup in levels:
                if lvup.location.LocationId == sword_level:
                    sword_item = lvup.item.Id
                if lvup.location.LocationId == shield_level:
                    shield_item = lvup.item.Id
                if lvup.location.LocationId == staff_level:
                    staff_item = lvup.item.Id
            items_for_sword_level[sword_level] = (sword_item, shield_item, staff_item)

        for lvup in levels:
            level_stats = next(
                lv for lv in self.randomizer.level_stats if lv.location == lvup.location
            )
            level = lvup.location.LocationId
            item_id = items_for_sword_level[level]
            mod.level_ups.add_sora_level(
                level=level,
                experience=level_stats.experience,
                strength=level_stats.strength,
                magic=level_stats.magic,
                defense=level_stats.defense,
                ap=level_stats.ap,
                sword_ability=item_id[0],
                shield_ability=item_id[1],
                staff_ability=item_id[2],
                padding=0,
            )
            
        companion_names = ["Donald","Goofy","PingMulan","Beast","Auron","Sparrow","Aladdin","Jack","Simba","Tron","Riku"]
        companion_exp = settings.companion_exp()
        for c_name in companion_names:
            companion_levels = mod.level_ups.get_companion_levels(c_name)
            for level in companion_levels:
                mod.level_ups.add_companion_level(
                    level=level,
                    experience=companion_exp[level],
                    strength=companion_levels[level]["Strength"],
                    magic=companion_levels[level]["Magic"],
                    defense=companion_levels[level]["Defense"],
                    ap=companion_levels[level]["Ap"],
                    companion_name=c_name,
                    padding=0
                )

    def assign_treasures(self, mod: SeedModBuilder):
        treasures = _assignment_subset(
            self.randomizer.assignments,
            [locationCategory.POPUP, locationCategory.CHEST],
        )
        treasures = [
            trsr
            for trsr in treasures
            if locationType.Puzzle not in trsr.location.LocationTypes
            and locationType.Critical not in trsr.location.LocationTypes
            and locationType.SYNTH not in trsr.location.LocationTypes
        ]

        for trsr in treasures:
            mod.treasures.add_treasure(
                location_id=trsr.location.LocationId, item_id=trsr.item.Id
            )

    def check_if_companion_changed(
        self, settings: SeedSettings, keys: settingkey
    ):
        return settings.get(keys.COMPANION_DAMAGE_TOGGLE)

    def prepare_companion_damage_knockback(self, mod: SeedModBuilder):
        keys = settingkey
        atkp_organizer = mod._get_atkp_organizer()
        ui_settings = self.settings.ui_settings
        companions_changed = self.check_if_companion_changed(ui_settings, keys)
        knockback_organizer = KnockbackTypes.get_knockback_value

        if not companions_changed:
            return
        kill_boss = 0
        if ui_settings.get(keys.COMPANION_KILL_BOSS):
            kill_boss = "KillBoss"

        # Donald
        options_list = []
        options_list.append(
            knockback_organizer(
                ui_settings.get(keys.DONALD_MELEE_ATTACKS_KNOCKBACK_TYPE)
            )
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.DONALD_FIRE_KNOCKBACK_TYPE))
        )
        options_list.append(
            knockback_organizer(
                ui_settings.get(keys.DONALD_BLIZZARD_KNOCKBACK_TYPE)
            )
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.DONALD_THUNDER_KNOCKBACK_TYPE))
        )
        self.ready_companion_damage_knockback_atkp_entries(
            atkp_organizer, "Donald/PL_Donald", options_list, kill_boss
        )
        
        # Goofy
        options_list = []
        options_list.append(
            knockback_organizer(
                ui_settings.get(keys.GOOFY_MELEE_ATTACKS_KNOCKBACK_TYPE)
            )
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.GOOFY_BASH_KNOCKBACK_TYPE))
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.GOOFY_TURBO_KNOCKBACK_TYPE))
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.GOOFY_TORNADO_KNOCKBACK_TYPE))
        )
        self.ready_companion_damage_knockback_atkp_entries(
            atkp_organizer, "Goofy/PL_Goofy", options_list, kill_boss
        )
        
        # Jack Skellington
        options_list = []
        options_list.append(
            knockback_organizer(
                ui_settings.get(keys.JACK_SKELLINGTON_MELEE_ATTACKS_KNOCKBACK_TYPE)
            )
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.JACK_SKELLINGTON_BLAZING_FURY_KNOCKBACK_TYPE))
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.JACK_SKELLINGTON_ICY_TERROR_KNOCKBACK_TYPE))
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.JACK_SKELLINGTON_BOLTS_OF_SORROW_KNOCKBACK_TYPE))
        )
        self.ready_companion_damage_knockback_atkp_entries(
            atkp_organizer, "Jack Skellington", options_list, kill_boss
        )
        
        # Simba
        options_list = []
        options_list.append(
            knockback_organizer(
                ui_settings.get(keys.SIMBA_MELEE_ATTACKS_KNOCKBACK_TYPE)
            )
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.SIMBA_FIERCE_CLAW_KNOCKBACK_TYPE))
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.SIMBA_GROUNDSHAKER_KNOCKBACK_TYPE))
        )
        self.ready_companion_damage_knockback_atkp_entries(
            atkp_organizer, "Simba", options_list, kill_boss
        )

        # Aladdin
        options_list = []
        options_list.append(
            knockback_organizer(
                ui_settings.get(keys.ALADDIN_MELEE_ATTACKS_KNOCKBACK_TYPE)
            )
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.ALADDIN_SLASH_FRENZY_KNOCKBACK_TYPE))
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.ALADDIN_QUICKPLAY_KNOCKBACK_TYPE))
        )
        self.ready_companion_damage_knockback_atkp_entries(
            atkp_organizer, "Aladdin", options_list, kill_boss
        )
        
        # Ping/Mulan
        options_list = []
        options_list.append(
            knockback_organizer(
                ui_settings.get(keys.PING_MULAN_MELEE_ATTACKS_KNOCKBACK_TYPE)
            )
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.MULAN_MUSHU_FIRE_KNOCKBACK_TYPE))
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.MULAN_FLAMETONGUE_KNOCKBACK_TYPE))
        )
        self.ready_companion_damage_knockback_atkp_entries(
            atkp_organizer, "Ping/Mulan", options_list, kill_boss
        )
        
        # Beast
        options_list = []
        options_list.append(
            knockback_organizer(
                ui_settings.get(keys.BEAST_MELEE_ATTACKS_KNOCKBACK_TYPE)
            )
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.BEAST_SHOUT_KNOCKBACK_TYPE))
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.BEAST_RUSH_KNOCKBACK_TYPE))
        )
        self.ready_companion_damage_knockback_atkp_entries(
            atkp_organizer, "Beast", options_list, kill_boss
        )
        
        # Tron
        options_list = []
        options_list.append(
            knockback_organizer(
                ui_settings.get(keys.TRON_MELEE_ATTACKS_KNOCKBACK_TYPE)
            )
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.TRON_SCOUTING_DISK_KNOCKBACK_TYPE))
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.TRON_PULSING_THUNDER_KNOCKBACK_TYPE))
        )
        self.ready_companion_damage_knockback_atkp_entries(
            atkp_organizer, "Tron", options_list, kill_boss
        )
        
        # Jack Sparrow
        options_list = []
        options_list.append(
            knockback_organizer(
                ui_settings.get(keys.JACK_SPARROW_MELEE_ATTACKS_KNOCKBACK_TYPE)
            )
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.JACK_SPARROW_NO_MERCY_KNOCKBACK_TYPE))
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.JACK_SPARROW_RAIN_STORM_KNOCKBACK_TYPE))
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.JACK_SPARROW_BONE_SMASH_KNOCKBACK_TYPE))
        )
        self.ready_companion_damage_knockback_atkp_entries(
            atkp_organizer, "Jack Sparrow", options_list, kill_boss
        )
        
        # Riku
        options_list = []
        options_list.append(
            knockback_organizer(
                ui_settings.get(keys.RIKU_MELEE_ATTACKS_KNOCKBACK_TYPE)
            )
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.RIKU_DARK_AURA_KNOCKBACK_TYPE))
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.RIKU_DARK_SHIELD_KNOCKBACK_TYPE))
        )
        self.ready_companion_damage_knockback_atkp_entries(
            atkp_organizer, "Riku", options_list, kill_boss
        )
        
        # Auron
        options_list = []
        options_list.append(
            knockback_organizer(
                ui_settings.get(keys.AURON_MELEE_ATTACKS_KNOCKBACK_TYPE)
            )
        )
        options_list.append(
            knockback_organizer(ui_settings.get(keys.AURON_DIVIDER_KNOCKBACK_TYPE))
        )
        self.ready_companion_damage_knockback_atkp_entries(
            atkp_organizer, "Auron", options_list, kill_boss
        )

    def ready_companion_damage_knockback_atkp_entries(
        self,
        atkp_organizer: AttackEntriesOrganizer,
        companion_name,
        melee_ability_knockback_types_list,
        kill_boss,
    ):
        companion_melee_ids = self._get_companion_ids_for_damage_knockback_options(
            companion_name, "Melee"
        )
        companion_melee_objects = []
        for melee_entry in companion_melee_ids:
            companion_melee_objects.append(
                atkp_organizer.get_attack_using_ids(melee_entry[0], melee_entry[1])
            )
        for melee_object in companion_melee_objects:
            melee_object: ATKPObject
            melee_object.EnemyReaction = melee_ability_knockback_types_list[0]
            melee_object.Flags = kill_boss

        companion_ability_ids = self._get_companion_ids_for_damage_knockback_options(
            companion_name, "Ability"
        )
        companion_ability_objects = []
        for i in range(len(companion_ability_ids)):
            # The third entry is for when we need the power field to distinguish different entries for the same attack (like goofy tornado)
            for ability_entry in companion_ability_ids[i]:
                if len(ability_entry) == 3:
                    entry_object = atkp_organizer.get_attack_using_ids_plus_power(
                        ability_entry[0], ability_entry[1], ability_entry[2]
                    )
                    entry_object: ATKPObject
                    entry_object.EnemyReaction = melee_ability_knockback_types_list[i + 1]
                    entry_object.Flags = kill_boss
                    companion_ability_objects.append(entry_object)
                    continue
                
                entry_object = atkp_organizer.get_attack_using_ids(
                    ability_entry[0], ability_entry[1]
                )
                entry_object: ATKPObject
                entry_object.EnemyReaction = melee_ability_knockback_types_list[i+1]
                entry_object.Flags = kill_boss
                companion_ability_objects.append(entry_object)

        for atkp_object in companion_melee_objects:
            atkp_organizer.convert_atkp_object_to_dict_and_add_to_data(atkp_object)
        for atkp_object in companion_ability_objects:
            atkp_organizer.convert_atkp_object_to_dict_and_add_to_data(atkp_object)

    def _get_companion_ids_for_damage_knockback_options(
        self, companion_name, id_group
    ) -> dict[{str, list[int]}]:
        # SubId first, then Id
        if companion_name == "Donald/PL_Donald":
            if id_group == "Melee":
                return [[0, 151], [0, 152], [0, 153], [0, 154], [0, 155], [0, 153], [0, 154]]
            return [
                [[0, 1163], [2, 1163], [0, 1716], [2, 1716]],
                [[0, 1164], [0, 1717]],
                [[0, 1165], [0, 1165], [0, 1718], [0, 1718]],
            ]  # There are two entries in atkp for thunder that have same Id, SubId and Power...
        elif companion_name == "Goofy/PL_Goofy":
            if id_group == "Melee":
                return [[0, 146], [1, 146], [0, 156], [0, 157], [0, 158], [0, 159], [0, 1942], [1, 1942], [0, 85], [0, 86], [0, 87], [0, 95]]
            return [
                [[0, 1161]],
                [[0, 1162], [0, 1253]],
                [[0, 1160, 25], [0, 1258, 25]],
            ]  # Third entry in last one is for power
        elif companion_name == "Jack Skellington":
            if id_group == "Melee":
                return [[0, 224], [0, 895], [0, 225], [0, 563], [0,564], [0, 565], [0, 273], [1, 273], [0, 274]]
            return [
                [[0, 1176]],
                [[0, 1176], [0, 1176]], # Same as Donald Thunder
                [[0, 1178]],
            ]
        elif companion_name == "Simba":
            if id_group == "Melee":
                return [[0, 861], [0, 941], [0, 862], [0, 863], [0, 864], [0, 864]]
            return [
                [[0, 1180]],
                [[0, 1179], [1, 1179], [4, 1179]],
            ]
        elif companion_name == "Aladdin":
            if id_group == "Melee":
                return [[0, 214], [0, 215], [0, 216], [0, 217], [0, 218]]
            return [
                [[0, 1174], [1, 1174]],
                [[0, 1175], [0, 1193], [1, 1193]], # Quickplay spans over 2 parent IDs
            ]
        elif companion_name == "Ping/Mulan":
            if id_group == "Melee":
                return [[0, 365], [0, 366], [0, 367], [0, 368], [0, 369], [1, 369], [0, 371], [0, 384], [0, 387], [0, 385], [0, 372], [0, 373]]
            return [
                [[0, 1169], [3, 1169]],
                [[0, 622], [1, 622]],
            ]
        elif companion_name == "Beast":
            if id_group == "Melee":
                return [[0, 219], [0, 220], [0, 223], [0, 221], [0, 222]]
            return [
                [[0, 1166]],
                [[0, 570], [0, 575]], # Rush spans over 2 parent IDs
            ]
        elif companion_name == "Tron":
            if id_group == "Melee":
                return [[0, 361], [0, 1527], [0, 1528], [0, 1529]]
            return [
                [[0, 627]],
                [[0, 1181]],
            ]
        elif companion_name == "Jack Sparrow":
            if id_group == "Melee":
                return [[0, 494], [0, 495], [0, 646], [0, 647], [0, 648], [0, 648], [0, 515], [0, 649]]
            return [
                [[0, 1171]],
                [[0, 1172]],
                [[0, 1173]],
            ]
        elif companion_name == "Riku":
            if id_group == "Melee":
                return [[0, 1494], [0, 1495], [0, 1496], [0, 1497], [0, 1498], [0, 1499], [0, 1500], [0, 1501], [0, 1502], [0, 1503], [0, 1504], [0, 1505], [0, 1506], [0, 1507], [0, 1508], [0, 1509], [0, 1510], [0, 1511], [0, 1512], [0, 1513], [0, 1514], [0, 1515], [0, 1516]]
            return [
                [[0, 1531]],
                [[0, 1532]]
            ]
        elif companion_name == "Auron":
            if id_group == "Melee":
                return [[0, 193], [0, 194], [0, 195], [0, 196]]
            return [
                [[0, 1272], [1, 1272], [0, 1576]],
            ]


class CosmeticsOnlyZip:

    def __init__(self, ui_settings: SeedSettings):
        self.settings = ui_settings

    def create_zip(self) -> io.BytesIO:
        data = io.BytesIO()
        with ZipFile(data, "w", ZIP_DEFLATED) as out_zip:
            mod = ModYml(
                "Randomized Cosmetics",
                description="Generated by the KH2 Randomizer Seed Generator.",
            )

            _add_cosmetics(out_zip=out_zip, mod_yml=mod, settings=self.settings)

            mod.write_to_zip_file(out_zip)

            out_zip.write(
                resource_path("static/icons/misc/Kingdom Hearts II.png"), "icon.png"
            )

        data.seek(0)
        return data


class BossEnemyOnlyZip:
    def __init__(self, seed_name: str, ui_settings: SeedSettings, platform: str):
        self.settings = ui_settings
        self.enemy_options = makeKHBRSettings(seed_name, self.settings)
        self.platform = platform

    def create_zip(self) -> io.BytesIO:
        def _should_run_khbr():
            if not self.enemy_options.get("boss", False) in [False, "Disabled"]:
                return True
            if not self.enemy_options.get("enemy", False) in [False, "Disabled"]:
                return True
            return False

        if not _should_run_khbr():
            raise GeneratorException(
                "Trying to generate boss/enemy only mod without enabling those settings."
            )

        data = io.BytesIO()
        with ZipFile(data, "w", ZIP_DEFLATED) as out_zip:
            mod = ModYml(
                "Randomized Bosses/Enemies",
                description="Generated by the KH2 Randomizer Seed Generator.",
            )

            enemy_spoilers, _ = _run_khbr(
                self.platform, self.enemy_options, mod, out_zip
            )

            mod.write_to_zip_file(out_zip)

            out_zip.write(
                resource_path("static/icons/misc/Kingdom Hearts II.png"), "icon.png"
            )
            out_zip.writestr("enemyspoilers.txt", enemy_spoilers)

            data.seek(0)
            return data

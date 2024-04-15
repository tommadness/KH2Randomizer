from collections import Counter
import copy
import itertools
import random
from dataclasses import dataclass
from dataclasses import field
from typing import Optional

from Class.exceptions import (
    GeneratorException,
    CantAssignItemException,
    SettingsException,
)
from Class.itemClass import KH2Item
from Class.newLocationClass import KH2Location
from Class.randomUtils import weighted_sample_without_replacement
from List.ObjectiveList import KH2Objective
from List.ItemList import Items
from List.NewLocationList import Locations
from List.configDict import (
    ObjectivePoolOption,
    locationCategory,
    itemRarity,
    itemType,
    locationDepth,
    locationType,
    LevelUpStatBonus,
)
from List.inventory import (
    ability,
    consumable,
    form,
    growth,
    keyblade,
    magic,
    misc,
    proof,
    report,
    storyunlock,
)
from List.inventory.item import InventoryItem
from List.location import (
    simulatedtwilighttown as stt,
    weaponslot,
    hundredacrewood as haw,
    hollowbastion as hb,
    starting,
)
from Module.RandomizerSettings import RandomizerSettings
from Module.depths import ItemDepths
from Module.modifier import SeedModifier
from Module.weighting import LocationWeights


@dataclass
class ItemAssignment:
    location: KH2Location
    item: Optional[KH2Item]
    item2: Optional[KH2Item] = None

    def items(self) -> list[KH2Item]:
        """Returns the items (if any) for this assignment."""
        result = []
        if self.item is not None:
            result.append(self.item)
        if self.item2 is not None:
            result.append(self.item2)
        return result

    def __eq__(self, o: object) -> bool:
        if isinstance(o, ItemAssignment):
            return self.location == o.location
        elif isinstance(o, KH2Location):
            return self.location == o
        else:
            return NotImplemented


@dataclass
class WeaponStats:
    location: KH2Location
    strength: int
    magic: int

    def __eq__(self, o: object) -> bool:
        if isinstance(o, WeaponStats):
            return self.location == o.location
        elif isinstance(o, KH2Location):
            return self.location == o
        else:
            return NotImplemented


@dataclass
class LevelStats:
    location: KH2Location
    experience: int
    strength: int
    magic: int
    defense: int
    ap: int

    def __eq__(self, o: object) -> bool:
        if isinstance(o, LevelStats):
            return self.location == o.location
        elif isinstance(o, KH2Location):
            return self.location == o
        else:
            return NotImplemented


@dataclass
class FormExp:
    location: KH2Location
    experience: int

    def __eq__(self, o: object) -> bool:
        if isinstance(o, FormExp):
            return self.location == o.location
        elif isinstance(o, KH2Location):
            return self.location == o
        else:
            return NotImplemented


@dataclass
class SynthRequirement:
    synth_item: KH2Item
    amount: int


@dataclass
class SynthesisRecipe:
    location: KH2Location
    unlock_rank: int
    requirements: list[SynthRequirement] = field(default_factory=list)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, SynthesisRecipe):
            return self.location == o.location
        elif isinstance(o, KH2Location):
            return self.location == o
        else:
            return NotImplemented


def _find_location(
    location_name: str, locations: list[KH2Location]
) -> Optional[KH2Location]:
    return next((loc for loc in locations if loc.name() == location_name), None)


def _find_locations(
    location_names: list[str], locations: list[KH2Location]
) -> list[KH2Location]:
    return [loc for loc in locations if loc.name() in location_names]


class Randomizer:
    def __init__(self, settings: RandomizerSettings, progress_bar_vis: bool = False):
        if settings is None:
            raise SettingsException(
                "Invalid settings passed to randomize. Change settings and try again"
            )
        random.seed(settings.full_rando_seed)
        self.progress_bar_vis = progress_bar_vis
        self.regular_locations = Locations(settings, secondary_graph=False)
        self.reverse_locations = Locations(settings, secondary_graph=True)
        self.master_locations = (
            self.regular_locations if settings.regular_rando else self.reverse_locations
        )
        self.location_weights = LocationWeights(
            settings, self.regular_locations, self.reverse_locations
        )
        self.report_depths = ItemDepths(settings.reportDepth, self.master_locations)
        self.proof_depths = ItemDepths(settings.proofDepth, self.master_locations)
        self.story_depths = ItemDepths(settings.storyDepth, self.master_locations)
        self.promise_charm_depths = ItemDepths(settings.promiseCharmDepth, self.master_locations)
        self.yeet_the_bear = settings.yeetTheBear
        self.num_valid_locations = None
        self.num_available_items = None
        self.starting_item_ids: list[int] = []
        self.assignments: list[ItemAssignment] = []
        self.donald_assignments: list[ItemAssignment] = []
        self.goofy_assignments: list[ItemAssignment] = []
        self.weapon_stats: list[WeaponStats] = []
        self.level_stats: list[LevelStats] = []
        self.form_level_exp: list[FormExp] = []
        self.synthesis_recipes: list[SynthesisRecipe] = []
        self.shop_items: list[KH2Item] = []
        self.objectives: list[KH2Objective] = []
        self.assign_sora_items(settings)
        if progress_bar_vis:
            return
        self.assign_party_items()
        self.assign_weapon_stats(settings)
        self.assign_level_stats(settings)
        self.assign_form_level_exp(settings)

    def assign_form_level_exp(self, settings: RandomizerSettings):
        """Assigns experience values to each form level."""
        experience_values = {
            locationCategory.SUMMONLEVEL: settings.summon_exp(),
            locationCategory.VALORLEVEL: settings.valor_exp(),
            locationCategory.WISDOMLEVEL: settings.wisdom_exp(),
            locationCategory.LIMITLEVEL: settings.limit_exp(),
            locationCategory.MASTERLEVEL: settings.master_exp(),
            locationCategory.FINALLEVEL: settings.final_exp(),
        }
        for category, experience in experience_values.items():
            locations = self.master_locations.locations_for_category(category)
            for index, location in enumerate(locations):
                self.form_level_exp.append(FormExp(location, experience[index]))

    def assign_level_stats(self, settings: RandomizerSettings):
        """Assigns stat increases to each level."""
        locations = self.master_locations.locations_for_category(locationCategory.LEVEL)
        locations.sort(key=lambda x: x.LocationId)

        # All the stats are accumulated as we go
        acc_strength = 2
        acc_magic = 6
        acc_defense = 2
        acc_ap = 0
        acc_exp = 0

        def add_stat(choice: tuple[LevelUpStatBonus, int]):
            nonlocal acc_strength
            nonlocal acc_magic
            nonlocal acc_defense
            nonlocal acc_ap

            chosen_stat, stat_increase = choice
            if chosen_stat == LevelUpStatBonus.STRENGTH:
                acc_strength += stat_increase
            elif chosen_stat == LevelUpStatBonus.MAGIC:
                acc_magic += stat_increase
            elif chosen_stat == LevelUpStatBonus.DEFENSE:
                acc_defense += stat_increase
            elif chosen_stat == LevelUpStatBonus.AP:
                acc_ap += stat_increase
            else:
                raise GeneratorException("We had a problem assigning stats to levels")

        def add_no_stats(_):
            return

        adder_function = add_no_stats if settings.vanilla_level_one else add_stat

        level_stat_pool = [(s[0], s[1]) for s in settings.level_stat_pool]
        stat_weights = [s[2] for s in settings.level_stat_pool]
        experience = settings.sora_exp()
        excluded_levels = settings.excluded_levels()
        for index, location in enumerate(locations):
            if index != 0:
                stat_choices = weighted_sample_without_replacement(
                    population=level_stat_pool, weights=stat_weights, k=2
                )
                adder_function(stat_choices[0])
                if location.LocationId in excluded_levels:
                    adder_function(stat_choices[1])
            acc_exp += experience[index + 1] - experience[index]
            self.level_stats.append(
                LevelStats(
                    location, acc_exp, acc_strength, acc_magic, acc_defense, acc_ap
                )
            )

    def assign_weapon_stats(self, settings: RandomizerSettings):
        """Assigns stats to each weapon."""
        key_min = settings.keyblade_min_stat
        key_max = settings.keyblade_max_stat
        sora_average = (key_min + key_max) // 2

        for key in weaponslot.keyblade_slots():
            if (
                key.LocationId == weaponslot.LocationId.Pureblood
                and not settings.pureblood
            ):
                continue
            self.weapon_stats.append(
                WeaponStats(
                    key,
                    strength=random.randint(key_min, key_max),
                    magic=random.randint(key_min, key_max),
                )
            )
        for struggle_weapon in weaponslot.struggle_weapon_slots():
            self.weapon_stats.append(
                WeaponStats(struggle_weapon, strength=sora_average, magic=sora_average)
            )
        for staff in weaponslot.donald_staff_slots():
            self.weapon_stats.append(
                WeaponStats(
                    staff, strength=random.randint(1, 13), magic=random.randint(1, 13)
                )
            )
        for shield in weaponslot.goofy_shield_slots():
            self.weapon_stats.append(
                WeaponStats(shield, strength=random.randint(1, 13), magic=0)
            )

    def assign_party_items(self):
        """Assigns items to locations for party members."""
        donald_locations = Locations.all_donald_locations()
        for donald_ability in Items.donald_ability_list():
            random_location = random.choice(donald_locations)
            if self.assign_item(
                random_location, donald_ability, self.donald_assignments
            ):
                donald_locations.remove(random_location)

        goofy_locations = Locations.all_goofy_locations()
        for goofy_ability in Items.goofy_ability_list():
            random_location = random.choice(goofy_locations)
            if self.assign_item(random_location, goofy_ability, self.goofy_assignments):
                goofy_locations.remove(random_location)

    def apply_starting_items(self, settings: RandomizerSettings):
        """Populates the starting items list, based on settings for starting inventory, growth, etc."""
        self.starting_item_ids.extend(settings.starting_inventory_ids)

        starting_growth_abilities = SeedModifier.starting_growth(
            settings.starting_growth_option
        )
        self.starting_item_ids.extend(
            growth_ability.id for growth_ability in starting_growth_abilities
        )

        starting_reports = random.sample(
            report.all_reports(), k=settings.starting_report_count
        )
        self.starting_item_ids.extend(rpt.id for rpt in starting_reports)

        starting_unlocks = SeedModifier.starting_unlocks(
            mode=settings.starting_visit_mode,
            random_range=settings.starting_visit_random_range,
            specific_unlocks=settings.starting_unlocks_per_world
        )
        self.starting_item_ids.extend(unlock.id for unlock in starting_unlocks)

        if settings.tt1_jailbreak:
            self.starting_item_ids.append(Items.getTT1Jailbreak().Id)
        if settings.objective_rando:
            self.starting_item_ids.append(Items.objectiveReportItem().Id)

    def initial_item_pool(self, settings: RandomizerSettings) -> list[KH2Item]:
        """
        Builds the initial item pool, based on settings.
        Also adds the configured number of reports and visit unlocks to the shop.
        """
        item_pool = Items.getItemList(
            story_unlocking_rarity=settings.story_unlock_rarity
        )

        # Add any additional items to the pool based on settings
        if settings.statSanity:
            item_pool.extend(Items.getStatItems())
        if settings.fifty_ap:
            item_pool.extend(itertools.repeat(KH2Item(consumable.ApBoost), 50))
        if settings.promiseCharm:
            item_pool.append(Items.getPromiseCharm())

        # Remove various items from the pool based on settings
        item_ids_to_remove: list[int] = []
        item_types_to_remove: list[itemType] = []
        if not settings.pureblood:
            item_ids_to_remove.append(keyblade.Pureblood.id)
        if not settings.antiform:
            item_ids_to_remove.append(form.AntiForm.id)
        if not settings.include_maps:
            item_types_to_remove.append(itemType.MAP)
        if not settings.include_recipes:
            item_types_to_remove.append(itemType.RECIPE)
        if not settings.include_accessories:
            item_types_to_remove.append(itemType.ACCESSORY)
        if not settings.include_armor:
            item_types_to_remove.append(itemType.ARMOR)
        if not settings.include_munny_pouches:
            item_types_to_remove.append(itemType.MUNNY_POUCH)

        # Any starting items get removed from the item pool
        item_ids_to_remove.extend(self.starting_item_ids)

        def include_item(item: KH2Item) -> bool:
            return item.ItemType not in item_types_to_remove
        item_pool = list(filter(include_item, item_pool))

        # Remove these one at a time since we can have duplicate IDs for starting inventory
        # (at the very least, visit unlocks)
        for item_id_to_remove in item_ids_to_remove:
            item_to_remove = next((item for item in item_pool if item.Id == item_id_to_remove), None)
            if item_to_remove is not None:
                item_pool.remove(item_to_remove)

        # Reports and visit unlocks in the shop (these do affect the item pool)
        if settings.shop_reports > 0:
            report_pool = [i for i in item_pool if i.ItemType == itemType.REPORT]
            num_reports_in_shop = min(settings.shop_reports, len(report_pool))
            chosen_reports: list[KH2Item] = random.sample(
                report_pool, k=num_reports_in_shop
            )
            self.shop_items.extend(chosen_reports)
            for chosen_report in chosen_reports:
                item_pool.remove(chosen_report)
        if settings.shop_unlocks > 0:
            visit_unlock_pool = [
                i for i in item_pool if i.ItemType == itemType.STORYUNLOCK
            ]
            num_visit_unlocks_in_shop = min(
                settings.shop_unlocks, len(visit_unlock_pool)
            )
            chosen_unlocks: list[KH2Item] = random.sample(
                visit_unlock_pool, k=num_visit_unlocks_in_shop
            )
            self.shop_items.extend(chosen_unlocks)
            for chosen_unlock in chosen_unlocks:
                item_pool.remove(chosen_unlock)

        return item_pool

    def initial_ability_pool(self, settings: RandomizerSettings) -> list[KH2Item]:
        """Builds the initial ability pool, based on settings."""
        modifier = SeedModifier.ability_list_modifier(settings.ability_pool_option)
        ability_pool: list[KH2Item] = modifier(
            Items.getActionAbilityList(),
            Items.getSupportAbilityList() + Items.getLevelAbilityList(),
        )

        # Remove any starting abilities from the pool
        # (make sure to only remove one copy for each starting item)
        remove_abilities = []
        for starting_item_id in settings.starting_inventory_ids:
            for pool_ability in ability_pool:
                if pool_ability.Id == starting_item_id:
                    remove_abilities.append(pool_ability)
                    break
        for remove_ability in remove_abilities:
            ability_pool.remove(remove_ability)

        return ability_pool

    def partition_locations(
        self, settings: RandomizerSettings
    ) -> tuple[list[KH2Location], list[KH2Location]]:
        """Splits all locations into lists of valid and invalid locations, based on settings."""
        all_locations = self.master_locations.all_locations()
        self.augment_invalid_checks(all_locations, settings)

        # If not "statsanity", even disabled locations should get stat bonuses
        if not settings.statSanity:
            self.assign_stat_bonuses(all_locations)

        def invalid_checker(location: KH2Location) -> bool:
            types = location.LocationTypes
            check_list = [
                locationType.OCCups,
                locationType.OCParadoxCup,
                locationType.CoR,
                locationType.TTR,
            ]
            invalid = any(
                disabled_type in types for disabled_type in settings.disabledLocations
            )
            if any(loc_type in check_list for loc_type in types):
                invalid = not any(
                    loc_type in settings.enabledLocations and loc_type in check_list
                    for loc_type in types
                )
            return invalid

        def remove_popupchecker(location: KH2Location) -> bool:
            if not settings.remove_popups:
                return False
            relevant_categories = [
                locationCategory.POPUP,
                locationCategory.DOUBLEBONUS,
                locationCategory.HYBRIDBONUS,
                locationCategory.ITEMBONUS,
                locationCategory.STATBONUS,
            ]
            superboss_types = [
                locationType.AS,
                locationType.DataOrg,
                locationType.LW,
                locationType.Sephi,
            ]
            category = location.LocationCategory
            if category in relevant_categories and not any(
                item in location.LocationTypes for item in superboss_types
            ):
                return True
            else:
                return False

        def no_final_form(location: KH2Location) -> bool:
            if not settings.disable_final_form:
                return False
            return location.LocationCategory is locationCategory.FINALLEVEL

        valid_locations: list[KH2Location] = []
        invalid_locations: list[KH2Location] = []
        excluded_levels = settings.excluded_levels()
        for loc in all_locations:
            if (
                no_final_form(loc)
                or invalid_checker(loc)
                or remove_popupchecker(loc)
                or (
                    loc.LocationCategory is locationCategory.LEVEL
                    and loc.LocationId in excluded_levels
                )
            ):
                invalid_locations.append(loc)
            else:
                valid_locations.append(loc)

        if len(all_locations) != (len(invalid_locations) + len(valid_locations)):
            raise GeneratorException(
                f"Separating valid {len(valid_locations)} and invalid {len(invalid_locations)} locations removed locations from existence (total {len(all_locations)})"
            )

        return valid_locations, invalid_locations

    @staticmethod
    def split_vanilla_abilities(
        ability_pool: list[KH2Item], vanilla_item_ids: list[int]
    ) -> tuple[list[KH2Item], list[KH2Item]]:
        """Splits the ability pool into lists of vanilla and randomizable abilities."""
        vanilla_item_ids_copy = copy.deepcopy(vanilla_item_ids)
        vanilla_abilities = []
        randomizable_abilities = []
        for item in ability_pool:
            if item.Id in vanilla_item_ids_copy:
                vanilla_item_ids_copy.remove(item.Id)
                vanilla_abilities.append(item)
            else:
                randomizable_abilities.append(item)
        return vanilla_abilities, randomizable_abilities

    def assign_sora_items(self, settings: RandomizerSettings):
        """Assigns items to locations for Sora."""
        self.apply_starting_items(settings)

        item_pool = self.initial_item_pool(settings)
        ability_pool = self.initial_ability_pool(settings)

        # Items in the shop that don't affect the item pool.
        # In particular, the keyblades in the shop don't get removed from the pool.
        if settings.shop_keyblades:
            self.shop_items.extend(
                item for item in item_pool if item.ItemType == itemType.KEYBLADE
            )
        if settings.shop_elixirs:
            self.shop_items.append(KH2Item(consumable.Elixir))
            self.shop_items.append(KH2Item(consumable.Megalixir))
        if settings.shop_recoveries:
            self.shop_items.append(KH2Item(consumable.DriveRecovery))
            self.shop_items.append(KH2Item(consumable.HighDriveRecovery))
        if settings.shop_boosts:
            self.shop_items.append(KH2Item(consumable.PowerBoost))
            self.shop_items.append(KH2Item(consumable.MagicBoost))
            self.shop_items.append(KH2Item(consumable.DefenseBoost))
            self.shop_items.append(KH2Item(consumable.ApBoost))

        valid_locations, invalid_locations = self.partition_locations(settings)

        locations_with_vanilla_items = [
            l
            for l in invalid_locations
            if len(l.VanillaItems) > 0
            and any(item in l.LocationTypes for item in settings.vanillaLocations)
        ]
        vanilla_item_ids = []
        for loc_with_vanilla in locations_with_vanilla_items:
            vanilla_item_ids.extend(loc_with_vanilla.VanillaItems)

        if len(vanilla_item_ids) > 0 and settings.chainLogic:
            raise GeneratorException(
                "Can't use vanilla worlds with chain logic for now. Sorry"
            )

        self.num_valid_locations = (
            len(valid_locations)
            + (
                len(
                    [
                        loc
                        for loc in valid_locations
                        if loc.LocationCategory
                        in [locationCategory.DOUBLEBONUS, locationCategory.HYBRIDBONUS]
                    ]
                )
                if settings.statSanity
                else 0
            )
            + (
                len(
                    [
                        loc
                        for loc in valid_locations
                        if loc.LocationCategory in [locationCategory.DOUBLEBONUS]
                    ]
                )
                if settings.statSanity
                else 0
            )
        )
        self.num_available_items = (
            len(ability_pool)
            + len(item_pool) 
            + (settings.max_objectives_available if settings.objective_rando else 0) 
            + (settings.max_emblems_available if settings.emblems else 0)
            - (sum([len(l.VanillaItems) for l in locations_with_vanilla_items]))
        )

        if self.progress_bar_vis:
            return

        # actual item assignment code starts here
        
        # give synth recipes their ingredients (if they are in valid locations)
        for location in valid_locations:
            if locationType.SYNTH in location.LocationTypes:
                # assign a recipe to this item
                items: list[KH2Item] = random.sample(
                    Items.getSynthRequirementsList(), k=random.randint(1, 3)
                )
                requirements = [
                    SynthRequirement(synth_item=item, amount=random.randint(1, 3))
                    for item in items
                ]
                recipe = SynthesisRecipe(
                    location=location,
                    unlock_rank=1 if location.LocationId < 15 else 2,
                    requirements=requirements,
                )
                self.synthesis_recipes.append(recipe)


        vanilla_abilities, randomizable_abilities = self.split_vanilla_abilities(
            ability_pool, vanilla_item_ids
        )
        valid_junk = self.get_n_junk(
            settings, num_junk_items=self.num_valid_locations - self.num_available_items
        )

        self.assign_keyblade_abilities(settings, randomizable_abilities, item_pool)
        item_pool.extend(vanilla_abilities)
        item_pool.extend(randomizable_abilities)
        item_pool.extend(valid_junk)
        if settings.emblems:
            item_pool.extend([Items.emblemItem() for _ in range(settings.max_emblems_available)])
            # remove proof of nonexistence
            item_pool = [i for i in item_pool if i.Id != proof.ProofOfNonexistence.id]
        random.shuffle(item_pool)

        # vanilla location item assignment
        for loc_with_vanilla in locations_with_vanilla_items:
            # find item in item list
            for vanilla_item_id in loc_with_vanilla.VanillaItems:
                vanilla_item = next(
                    (item for item in item_pool if item.Id == vanilla_item_id), None
                )
                if vanilla_item is None:
                    # if we don't have the item, it means that we started with the item, or it was randomized away
                    continue
                if vanilla_item.ItemType not in loc_with_vanilla.InvalidChecks:
                    item_pool.remove(vanilla_item)
                    if self.assign_item(loc_with_vanilla, vanilla_item):
                        invalid_locations.remove(loc_with_vanilla)

        # assign items that have very restricted locations (boss depths, yeet, etc.)
        self.assign_plando_like_items(settings, item_pool, valid_locations)

        # check for objective rando
        if settings.objective_rando:
            # get the objective pool
            objective_pool = settings.available_objectives
            # filter down the pool based on what valid locations there are
            valid_location_descriptions = [v.Description for v in valid_locations]
            objective_pool = [o for o in objective_pool if o.Location in valid_location_descriptions]
            # remove proof of nonexistence
            item_pool = [i for i in item_pool if i.Id != proof.ProofOfNonexistence.id]
            # remove duplicates for AS/Data split
            if locationType.AS in settings.enabledLocations and locationType.DataOrg in settings.enabledLocations:
                if settings.as_data_split:
                    # remove duplicates for ASs
                    objective_pool = [o for o in objective_pool if "Defeat AS" not in o.Name]
                else:
                    # remove duplicates for Datas
                    objective_pool = [o for o in objective_pool if not any(t in o.Name for t in ["Data Vexen","Data Zexion","Data Larxene","Data Lexaeus","Data Marluxia"])]
            if settings.objective_pool_type==ObjectivePoolOption.HITLIST.name:
                # remove all but one of the form objectives
                form_objectives = [o for o in objective_pool if "Level 7" in o.Name]
                objective_pool = [o for o in objective_pool if "Level 7" not in o.Name] + [random.choice(form_objectives)]

            if len(objective_pool) < settings.max_objectives_available:
                raise SettingsException("Not enough objective locations available to allow the max number of objectives to be placed.")

            # pick a number of objectives
            self.objectives = random.sample(objective_pool,k=settings.max_objectives_available)
            picked_objectives_location_names = [o.Location for o in self.objectives]
            # plando completion marks onto the selected objectives
            objective_locations = [v for v in valid_locations if v.Description in picked_objectives_location_names]
            for o in objective_locations:
                locations_to_remove = self.randomly_assign_single_item(Items.objectiveItem(),[o])
                for l in locations_to_remove:
                    valid_locations.remove(l)
            

        if settings.chainLogic:
            self.assign_chain_logic(settings, item_pool, valid_locations)    
        else:
            # create some space for random assignment by doing a forward-pass assignment
            self.create_available_location_space(settings, item_pool, valid_locations)                

        self.randomly_assign_items(item_pool, valid_locations)

        # move remaining items to invalid locations for junk item assignment
        invalid_locations.extend(valid_locations)
        self.assign_junk_locations(settings, invalid_locations)

    def assign_chain_logic(self, settings : RandomizerSettings, item_pool, valid_locations):
        def contains(bigger_list,smaller_list):
            return not (Counter(smaller_list)-Counter(bigger_list))
        def missing_items(bigger_list,smaller_list):
            return list((Counter(smaller_list)-Counter(bigger_list)).elements())
        # determine available unlocks for
        #   1) regular/reverse
        #   2) keyblade locking on/off
        #   3) Anything already placed
        #       a) specifically visit locks and proofs from the "very restricted" pool
        #   4) Determine the existing dependency graph (we will use this to make sure we don't overlap two unlocks in the chain)
        from Module.seedEvaluation import LocationInformedSeedValidator
        validator = LocationInformedSeedValidator()
        validator.prep_requirements_list(settings, self)
        item_locking_ids_per_world = validator.generate_locking_item_ids()

        item_depth = 0
        min_item_depth = settings.chainLogicMinLength
        max_item_depth = settings.chainLogicMinLength+50

        acquired_items,accessible_locations = self.get_accessible_locations(valid_locations,validator)
        last_unlocked_sphere = accessible_locations

        world_names_to_unlock = [w for w in item_locking_ids_per_world.keys() for _ in item_locking_ids_per_world[w]]
        random.shuffle(world_names_to_unlock)
        world_names_to_unlock = [w for w in world_names_to_unlock if w in settings.enabledLocations]

        proof_nonexistence_assignment = self.assignment_for_item_id(proof.ProofOfNonexistence.id)
        proof_of_nonexistence_last_unlock = None

        second_pass_worlds = []

        if proof_nonexistence_assignment is not None:
            # find the world that has the proof, and how many items it takes to get it
            proof_world = list(set(proof_nonexistence_assignment.location.LocationTypes).intersection(item_locking_ids_per_world.keys()))[0]
            # figure out how far into the world you need to go
            world_progression = item_locking_ids_per_world[proof_world]
            items_needed = []
            for w in world_progression:
                if validator.is_location_available(self.starting_item_ids + items_needed, proof_nonexistence_assignment.location):
                    # uh, bad chain
                    raise GeneratorException("Chain logic couldn't make a seed that ended on proof of nonexistence. Try changing proof depths.")
                proof_of_nonexistence_last_unlock = missing_items(items_needed,w)
                items_needed.extend(proof_of_nonexistence_last_unlock)

            # confirmed location, check last instance of this world and move it last
            last_index = [i for i in range(len(world_names_to_unlock)) if world_names_to_unlock[i] == proof_world][-1]
            del world_names_to_unlock[last_index]
            second_pass_worlds = [proof_world]     

        # this is checking for access into CoR, we'll need to simulate having the necessary movement
        simulated_growth = [growth.HighJump1.id,growth.HighJump2.id,growth.HighJump3.id,
                                                 growth.QuickRun1.id,growth.QuickRun2.id,growth.QuickRun3.id,
                                                 growth.AerialDodge1.id,growth.AerialDodge2.id,growth.AerialDodge3.id,
                                                 growth.Glide1.id,growth.Glide2.id,growth.Glide3.id,
                                                 ]
        history_of_items = []
        # print("Starting chain....")
        while (item_depth < min_item_depth or (item_depth < max_item_depth and random.random() < 0.75)): # 25% chance of breaking early
            # print("--iter")
            # pick a world to unlock checks from
            if world_names_to_unlock is None:
                break
            if len(world_names_to_unlock) == 0:
                break
            chosen_world = world_names_to_unlock[0]
            chosen_checks = item_locking_ids_per_world[chosen_world][0]
            def pop_world_from_list():
                nonlocal world_names_to_unlock
                nonlocal second_pass_worlds
                world_names_to_unlock.pop(0)
                if len(world_names_to_unlock)==0:
                    world_names_to_unlock = second_pass_worlds
                    second_pass_worlds = None
                item_locking_ids_per_world[chosen_world].pop(0)
            if contains(acquired_items,chosen_checks):
                # print(chosen_world)
                # print(f"--Already have these items {chosen_checks}")
                pop_world_from_list()
                continue
            chosen_checks = missing_items(acquired_items,chosen_checks)
            sphere_1 = [loc for loc in valid_locations if locationType.Level not in loc.LocationTypes and validator.is_location_available(self.starting_item_ids + acquired_items + chosen_checks + simulated_growth,loc) and loc not in accessible_locations]
            # print("*******************")
            # print(acquired_items)
            # print(chosen_checks)
            # print([s.Description for s in sphere_1])
            # print("*******************")
            if len(sphere_1) and len(last_unlocked_sphere) >= len(chosen_checks):
                pop_world_from_list()
                # assign new items
                history_of_items.append(chosen_checks)
                for i in chosen_checks:
                    # print(f"placing {i}")
                    i_data = next((it for it in item_pool if it.Id == i), None)
                    if i_data is not None:
                        # assign this item somewhere
                        locations_to_remove = self.randomly_assign_single_item(i_data,last_unlocked_sphere)
                        for l in locations_to_remove:
                            valid_locations.remove(l)
                        item_pool.remove(i_data)
                    else:
                        raise GeneratorException(f"Uh....chain logic couldn't find an item with the id {i} from the unlock list. This shouldn't happen. History {history_of_items}")
                acquired_items,accessible_locations = self.get_accessible_locations(valid_locations,validator, simulated_growth)
                last_unlocked_sphere = sphere_1
                item_depth+=1
            else:
                if chosen_world not in settings.enabledLocations:
                    # print(f"{chosen_world} checks are disabled")
                    pop_world_from_list()
                else:
                    # print(chosen_world)
                    # print(f"{len(sphere_1)} and {len(last_unlocked_sphere) }>={len(chosen_checks)} {chosen_checks}")
                    # print("--This item doesn't unlock enough right now, trying again later")
                    world_names_to_unlock.pop(0)
                    if second_pass_worlds is not None:
                        second_pass_worlds.insert(0,chosen_world)              

        if item_depth < min_item_depth:
            raise GeneratorException("Couldn't generate a chain long enough, are enough worlds on?...")

        i_data = next((it for it in item_pool if it.Id == proof.ProofOfNonexistence.id), None)
        if i_data is not None:
            # assign this item somewhere
            locations_to_remove = self.randomly_assign_single_item(i_data,last_unlocked_sphere)
            for l in locations_to_remove:
                valid_locations.remove(l)
            item_pool.remove(i_data)
        else:
            # make sure we have access to nonexistence
            acquired_items,accessible_locations = self.get_accessible_locations(valid_locations,validator, simulated_growth)
            if proof.ProofOfNonexistence.id not in acquired_items:
                raise GeneratorException("Couldn't access proof of nonexistence in chain logic")
            
    def create_available_location_space(self, settings, item_pool, valid_locations):
        # (a)determine sphere 0
        #    if sphere 0 is big enough
        #       return
        #    if sphere 0 is too small
        #    determine available unlocks for available checks
        #    place that somewhere that's available
        #    loop again        
        from Module.seedEvaluation import LocationInformedSeedValidator
        validator = LocationInformedSeedValidator()
        validator.prep_requirements_list(settings, self)

        sphere_0_check = True
        num_available_locations_needed_to_allow_random_assignment = 150 # TODO(zak) this is arbitrary and may need tuning
        while sphere_0_check:
            # calculate the available checks
            acquired_items, sphere_0 = self.get_accessible_locations(valid_locations, validator)
            if len(sphere_0) < num_available_locations_needed_to_allow_random_assignment:
                # pick a locking item we don't have, assign it somewhere valid, repeat
                unlocks = [] + [s.id for s in storyunlock.all_story_unlocks()] + [k.id for k in keyblade.get_locking_keyblades()]
                random.shuffle(unlocks)
                for u in unlocks:
                    i_data = next((it for it in item_pool if it.Id == u), None)
                    if i_data is not None:
                        sphere_1 = [loc for loc in valid_locations if validator.is_location_available(self.starting_item_ids + acquired_items + [i_data.Id],loc)]
                        if len(sphere_1) > len(sphere_0):
                            # assign this item somewhere
                            locations_to_remove = self.randomly_assign_single_item(i_data,sphere_0)
                            for l in locations_to_remove:
                                valid_locations.remove(l)
                            item_pool.remove(i_data)
                            break
            else:
                sphere_0_check = False

    def get_accessible_locations(self, valid_locations, validator, aux_items = None):
        if aux_items is None:
            aux_items = []
        acquired_item_locations = []
        acquired_items = []
        sphere_0 = []
        found_new_item = True
        # check if any of the already assigned locations are valid right now, and if so, add their item to current inventory
        while found_new_item:
            found_new_item = False
            # get unassigned locations that are available
            sphere_0 = [loc for loc in valid_locations if validator.is_location_available(self.starting_item_ids + acquired_items + aux_items,loc)]
            # get already assigned items from available locations
            for assignment in self.assignments:
                if assignment.location.LocationCategory is not locationCategory.WEAPONSLOT and assignment.location not in acquired_item_locations and validator.is_location_available(self.starting_item_ids + acquired_items + aux_items, assignment.location):
                    if assignment.location.Description != stt.CheckLocation.StruggleWinnerChampionBelt:
                        acquired_item_locations.append(assignment.location)
                        acquired_items.extend([i.Id for i in assignment.items()])
                        found_new_item = True
        return acquired_items,sphere_0

    def assign_plando_like_items(self, settings, item_pool, valid_locations):
        restricted_reports = self.report_depths.very_restricted_locations
        restricted_proofs = self.proof_depths.very_restricted_locations
        restricted_promise_charm = self.promise_charm_depths.very_restricted_locations
        restricted_story = self.story_depths.very_restricted_locations

        if self.yeet_the_bear:
            # Manually assign to Starry Hill
            yeet_locations = _find_locations(
                haw.yeet_the_bear_location_names(), valid_locations
            )
            if len(yeet_locations) > 0:
                yeet_location = random.choice(yeet_locations)
                proof_item = next(
                        key for key in item_pool if key.Id == proof.ProofOfNonexistence.id
                    )
                if self.assign_item(yeet_location, proof_item):
                    valid_locations.remove(yeet_location)
                    item_pool.remove(proof_item)
            else:
                raise CantAssignItemException(
                    "None of the Starry Hill locations are available for Yeet the Bear. Is HAW not randomized?"
                )
            
        if restricted_proofs:
            remaining_proofs = [i for i in item_pool if i.ItemType in proof.proof_item_types()]
            # pick N valid locations for these items
            valid_for_proofs = [loc for loc in valid_locations if self.proof_depths.is_valid(loc)]

            # Check if both AS's and datas are enabled, and remove AS locations if so
            # We do this mainly to prevent the AS and data fight in the same world from both having proofs.
            if (
                locationType.AS in settings.enabledLocations
                and locationType.DataOrg in settings.enabledLocations
            ):
                valid_for_proofs = [loc for loc in valid_for_proofs if locationType.AS not in loc.LocationTypes]

            good_choices = False
            while not good_choices:
                good_choices = True
                chosen_locations = random.sample(valid_for_proofs,k=len(remaining_proofs))
                for index,c in enumerate(chosen_locations):
                    # check that each proof is valid for the location (i.e. no connection on Terra)
                    if remaining_proofs[index].ItemType in c.InvalidChecks:
                        good_choices = False                    

            for index,c in enumerate(chosen_locations):
                item_pool.remove(remaining_proofs[index])
                if self.assign_item(c, remaining_proofs[index]):
                    valid_locations.remove(c)
        if restricted_promise_charm:
            promise_charm_item_list = [i for i in item_pool if i.ItemType is misc.PromiseCharm.type]
            # pick N valid locations for these items
            valid_for_promise_charm = [loc for loc in valid_locations if self.promise_charm_depths.is_valid(loc)]
            chosen_locations = random.sample(valid_for_promise_charm,k=len(promise_charm_item_list))
            for index,c in enumerate(chosen_locations):
                item_pool.remove(promise_charm_item_list[index])
                if self.assign_item(c, promise_charm_item_list[index]):
                    valid_locations.remove(c)
        if restricted_story:
            remaining_unlocks = [i for i in item_pool if i.ItemType is itemType.STORYUNLOCK]
            # pick N valid locations for these items
            valid_for_unlocks = [loc for loc in valid_locations if self.story_depths.is_valid(loc)]
            number_of_choices = min(len(remaining_unlocks),len(valid_for_unlocks))
            chosen_locations = random.sample(valid_for_unlocks,k=number_of_choices)
            for index,c in enumerate(chosen_locations):
                item_pool.remove(remaining_unlocks[index])
                if self.assign_item(c, remaining_unlocks[index]):
                    valid_locations.remove(c)
        if restricted_reports:
            remaining_reports = [i for i in item_pool if i.ItemType is itemType.REPORT]
            # pick N valid locations for these items
            valid_for_reports = [loc for loc in valid_locations if self.story_depths.is_valid(loc)]
            number_of_choices = min(len(remaining_reports),len(valid_for_reports))
            chosen_locations = random.sample(valid_for_reports,k=number_of_choices)
            for index,c in enumerate(chosen_locations):
                item_pool.remove(remaining_reports[index])
                if self.assign_item(c, remaining_reports[index]):
                    valid_locations.remove(c)

    def randomly_assign_single_item(self, item, location_pool):
        locations_to_remove = []
        if len(location_pool) == 0:
            raise CantAssignItemException(f"Ran out of locations to assign items {item}")

        weights = self.compute_location_weights(item, location_pool)

        count = 0
        while True:
            count += 1
            if len(weights) == 0:
                raise CantAssignItemException(
                    f"Ran out of locations to assign items to."
                )
            if sum(weights) == 0:
                raise CantAssignItemException(
                    f"Somehow, can't assign an item because there are no valid locations for {item.Name}."
                )

            random_location: KH2Location = random.choices(location_pool, weights)[
                0
            ]
            if item.ItemType not in random_location.InvalidChecks:
                if self.assign_item(random_location, item):
                    location_pool.remove(random_location)
                    locations_to_remove.append(random_location)

                    struggle_pair = self._maybe_assign_struggle_pair(
                        random_location, item, location_pool
                    )
                    if struggle_pair is not None:
                        location_pool.remove(struggle_pair)
                        locations_to_remove.append(struggle_pair)
                break
            if count == 100:
                raise CantAssignItemException(
                    f"Trying to assign {item} and failed 100 times in {len([i for i in location_pool if i.LocationCategory==locationCategory.POPUP])} popups left out of {len(location_pool)}"
                )
        return locations_to_remove


    def randomly_assign_items(self, item_pool, valid_locations):
        for item in item_pool:
            if len(valid_locations) == 0:
                raise CantAssignItemException(f"Ran out of locations to assign items")

            weights = self.compute_location_weights(item, valid_locations)

            count = 0
            while True:
                count += 1
                if len(weights) == 0:
                    raise CantAssignItemException(
                        f"Ran out of locations to assign items to."
                    )
                if sum(weights) == 0:
                    raise CantAssignItemException(
                        f"Somehow, can't assign an item because there are no valid locations for {item.Name}."
                    )

                random_location: KH2Location = random.choices(valid_locations, weights)[
                    0
                ]
                if item.ItemType not in random_location.InvalidChecks:
                    if self.assign_item(random_location, item):
                        valid_locations.remove(random_location)

                        struggle_pair = self._maybe_assign_struggle_pair(
                            random_location, item, valid_locations
                        )
                        if struggle_pair is not None:
                            valid_locations.remove(struggle_pair)
                    break
                if count == 100:
                    raise CantAssignItemException(
                        f"Trying to assign {item} and failed 100 times in {len([i for i in valid_locations if i.LocationCategory==locationCategory.POPUP])} popups left out of {len(valid_locations)}"
                    )


    def compute_location_weights(
        self, item: KH2Item, location_pool: list[KH2Location]
    ) -> list[int]:
        loc_weights = self.location_weights
        result = [
            loc_weights.get_weight(item.ItemType, loc) for loc in location_pool
        ]
        return result

    def assign_junk_locations(
        self, settings: RandomizerSettings, locations: list[KH2Location]
    ):
        """Assign the rest of the locations with "junk"."""
        junk_items = [
            item
            for item in Items.getJunkList(betterJunk=False)
            if item.Id in settings.junk_pool
        ]

        # Assign the same item to both struggle winner and loser if those locations are still available
        struggle_winner = _find_location(
            stt.CheckLocation.StruggleWinnerChampionBelt, locations
        )
        struggle_loser = _find_location(stt.CheckLocation.StruggleLoserMedal, locations)
        if struggle_winner is not None and struggle_loser is not None:
            junk_item = random.choice(junk_items)
            self.assign_item(struggle_winner, junk_item)
            self.assign_item(struggle_loser, junk_item)
            locations.remove(struggle_winner)
            locations.remove(struggle_loser)
        elif struggle_winner is not None and struggle_loser is None:
            raise GeneratorException(
                "Attempting to assign junk to struggle winner but loser already has an item"
            )
        elif struggle_loser is not None and struggle_winner is None:
            raise GeneratorException(
                "Attempting to assign junk to struggle loser but winner already has an item"
            )

        excluded_levels = settings.excluded_levels()
        for loc in locations:
            if loc.LocationCategory is not locationCategory.LEVEL or (
                loc.LocationCategory is locationCategory.LEVEL
                and loc.LocationId not in excluded_levels
            ):
                junk_item = random.choice(junk_items)
                # assign another junk item if that location needs another item
                if not self.assign_item(loc, junk_item):
                    junk_item = random.choice(junk_items)
                    self.assign_item(loc, junk_item)
            else:
                self.assign_item(loc, Items.getNullItem())

    @staticmethod
    def get_n_junk(settings: RandomizerSettings, num_junk_items: int) -> list[KH2Item]:
        """Returns a given number of "junk" items."""
        all_junk_items = [
            item
            for item in Items.getJunkList(betterJunk=False)
            if item.Id in settings.junk_pool
        ]
        return random.choices(all_junk_items, k=num_junk_items)

    def augment_invalid_checks(
        self, locations: list[KH2Location], settings: RandomizerSettings
    ):
        """Add invalid check types to locations."""
        for loc in locations:
            if loc.LocationCategory in [
                locationCategory.POPUP,
                locationCategory.CREATION,
            ]:
                loc.InvalidChecks.append(itemType.GROWTH_ABILITY)
                loc.InvalidChecks.append(itemType.ACTION_ABILITY)
                loc.InvalidChecks.append(itemType.SUPPORT_ABILITY)
                loc.InvalidChecks.append(itemType.GAUGE)
            if (
                locationType.STT in loc.LocationTypes
                and loc.LocationCategory != locationCategory.STATBONUS
            ):
                loc.InvalidChecks.append(itemType.GAUGE)
            if locationType.Critical in loc.LocationTypes:
                loc.InvalidChecks.append(itemType.GAUGE)

            # handle the easy depth options, restricted versions are handled specially
            if not self.report_depths.very_restricted_locations:
                if not self.report_depths.is_valid(loc):
                    loc.InvalidChecks.append(itemType.REPORT)

            if not self.proof_depths.very_restricted_locations:
                if not self.proof_depths.is_valid(loc):
                    loc.InvalidChecks.extend(proof.proof_item_types())

            if not self.story_depths.very_restricted_locations:
                if not self.story_depths.is_valid(loc):
                    loc.InvalidChecks.append(itemType.STORYUNLOCK)

            if not self.promise_charm_depths.very_restricted_locations:
                if not self.promise_charm_depths.is_valid(loc):
                    loc.InvalidChecks.append(itemType.PROMISE_CHARM)

            ''' Commenting this code out because new plando logic should account for this
            # if both reports and proofs are very restricted (only in 13 locations)
            # add extra proof restrictions to allow reports to be assigned
            if self.report_depths.is_valid(loc) and self.proof_depths.is_valid(loc):
                if (
                    self.report_depths.very_restricted_locations
                    and self.proof_depths.very_restricted_locations
                ):
                    loc.InvalidChecks.extend(proof.proof_item_types())

            if (
                self.proof_depths.is_valid(loc)
                and self.proof_depths.very_restricted_locations
            ):
                # Check if both AS's and datas are enabled, and if this is an AS location, disable that.
                # We do this mainly to prevent the AS and data fight in the same world from both having proofs.
                if (
                    locationType.AS in settings.enabledLocations
                    and locationType.DataOrg in settings.enabledLocations
                ):
                    if locationType.AS in loc.LocationTypes:
                        loc.InvalidChecks.extend(proof.proof_item_types())

            # Only allow Proof of Nonexistence on one of the yeet the bear check locations
            # (this may override a proof depth option but player chose to put the proof here)
            if self.yeet_the_bear:
                if loc.name() in haw.yeet_the_bear_location_names():
                    while itemType.PROOF_OF_NONEXISTENCE in loc.InvalidChecks:
                        loc.InvalidChecks.remove(itemType.PROOF_OF_NONEXISTENCE)
                else:
                    loc.InvalidChecks.append(itemType.PROOF_OF_NONEXISTENCE)
            '''

    def assign_keyblade_abilities(
        self,
        settings: RandomizerSettings,
        ability_pool: list[KH2Item],
        item_pool: list[KH2Item],
    ):
        """Assign abilities to keyblades."""
        eligible_ids = set(
            settings.keyblade_support_abilities + settings.keyblade_action_abilities
        )

        # remove auto abilities from keyblades
        if settings.extended_placement_logic:
            eligible_ids.discard(ability.AutoValor.id)
            eligible_ids.discard(ability.AutoWisdom.id)
            eligible_ids.discard(ability.AutoMaster.id)
            eligible_ids.discard(ability.AutoFinal.id)
            eligible_ids.discard(ability.AutoLimitForm.id)

        eligible_abilities = [abil for abil in ability_pool if abil.Id in eligible_ids]
        nightmare_rarity_weights = {
            itemRarity.COMMON: 1,
            itemRarity.UNCOMMON: 2,
            itemRarity.RARE: 5,
            itemRarity.MYTHIC: 5,
        }

        keyblade_ids_to_exclude = [
            weaponslot.LocationId.KingdomKeyD,
            weaponslot.LocationId.AlphaWeapon,
            weaponslot.LocationId.OmegaWeapon,
            weaponslot.LocationId.KingdomKey,
        ]

        # assign all the abilities for keyblades
        for key in weaponslot.keyblade_slots():
            if (
                key.LocationId == weaponslot.LocationId.Pureblood
                and not settings.pureblood
            ):
                continue

            if len(eligible_abilities) == 0:
                raise GeneratorException(
                    "Keyblades: Not enough abilities are available to assign an ability to every keyblade"
                )

            if (
                settings.extended_placement_logic
                and key.LocationId not in keyblade_ids_to_exclude
            ):
                ability_weights = [
                    nightmare_rarity_weights[abil.Rarity] for abil in eligible_abilities
                ]
            else:
                ability_weights = [1 for _ in eligible_abilities]

            random_ability = random.choices(eligible_abilities, ability_weights)[0]
            self.assign_item(key, random_ability)
            ability_pool.remove(random_ability)
            eligible_abilities.remove(random_ability)

            if settings.extended_placement_logic and random_ability.Rarity in [
                itemRarity.RARE,
                itemRarity.MYTHIC,
            ]:
                # change the rarity of the keyblade item to the rarity of the ability
                keyblade_inventory_item = Items.weaponslot_id_to_keyblade_item(
                    key.LocationId
                )
                if keyblade_inventory_item is not None:
                    keyblade_id = keyblade_inventory_item.id
                    keyblade_item = next(
                        key for key in item_pool if key.Id == keyblade_id
                    )
                    item_pool.remove(keyblade_item)
                    item_pool.append(KH2Item(keyblade_item.item, random_ability.Rarity))

        # Assign draws to struggle weapons
        for weapon in weaponslot.struggle_weapon_slots():
            self.assign_item(weapon, KH2Item(ability.Draw))

    def assign_stat_bonuses(self, avail_locations: list[KH2Location]):
        """Assign all the stat items to bonuses for stats. Only used when "statsanity" is off."""
        stat_items = Items.getStatItems()
        double_stat = [
            loc
            for loc in avail_locations
            if loc.LocationCategory == locationCategory.DOUBLEBONUS
        ]
        single_stat = [
            loc
            for loc in avail_locations
            if loc.LocationCategory
            in [locationCategory.STATBONUS, locationCategory.HYBRIDBONUS]
        ]

        if len(double_stat) != 1:
            raise GeneratorException(
                f"Somehow have two locations with double stat gains {double_stat}"
            )

        # Select two different stats to put on Xemnas 1
        stat1 = random.choice(stat_items)
        stat_items.remove(stat1)
        stat2 = stat1
        while stat1 == stat2:
            stat2 = random.choice(stat_items)
        stat_items.remove(stat2)
        self.assign_item(double_stat[0], stat1)
        self.assign_item(double_stat[0], stat2)
        avail_locations.remove(double_stat[0])

        if len(single_stat) != len(stat_items):
            raise GeneratorException(
                f"The number of stat bonus locations {len(single_stat)} doesn't match remaining stat items {len(stat_items)}"
            )

        # Assign the rest
        for item in stat_items:
            loc = random.choice(single_stat)
            single_stat.remove(loc)
            if self.assign_item(loc, item):
                avail_locations.remove(loc)

        if len(single_stat) != 0:
            raise GeneratorException(
                f"Leftover stat locations were not assigned. Num remaining {len(single_stat)}"
            )

    def assign_item(
        self,
        location: KH2Location,
        item: KH2Item,
        party_member_assigned_items: Optional[list[ItemAssignment]] = None,
    ) -> bool:
        """
        Assigns the given item to the given location. Returns True if the location has all needed items assigned, or
        False if it is a location with two slots and the other slot still needs to be filled.
        """
        double_item = location.LocationCategory in [
            locationCategory.DOUBLEBONUS,
            locationCategory.HYBRIDBONUS,
        ]

        assigned_items = party_member_assigned_items
        if assigned_items is None:
            assigned_items = self.assignments

        if item.ItemType in location.InvalidChecks:
            raise GeneratorException(
                f"Trying to assign {item} to {location} even though it's invalid."
            )

        assignment = next(
            filter(lambda a: a.location == location, assigned_items), None
        )
        if assignment is None:
            assigned_items.append(ItemAssignment(location, item))
            all_slots_filled = not double_item
        else:
            if assignment.item is None:
                raise GeneratorException(
                    f"Somehow assigned no item to a location {assignment}"
                )
            if not double_item:
                raise GeneratorException(
                    f"Assigning a second item to a location that can't have one {assignment}"
                )
            if assignment.item2 is not None:
                raise GeneratorException(
                    f"Assigning a third item to a location that already has two {assignment}"
                )
            assignment.item2 = item
            all_slots_filled = True

        return all_slots_filled

    def _maybe_assign_struggle_pair(
        self, loc: KH2Location, item: KH2Item, available_locations: list[KH2Location]
    ) -> Optional[KH2Location]:
        """
        If the assigned location is the struggle winner or loser, assigns the same item to the opposite.
        Returns the paired struggle location if the assigned location was either of the struggle winner or loser, or
        returns None otherwise.
        """
        if loc.name() == stt.CheckLocation.StruggleWinnerChampionBelt:
            opposite = _find_location(
                stt.CheckLocation.StruggleLoserMedal, available_locations
            )
        elif loc.name() == stt.CheckLocation.StruggleLoserMedal:
            opposite = _find_location(
                stt.CheckLocation.StruggleWinnerChampionBelt, available_locations
            )
        else:
            return None
        if opposite is None:
            raise GeneratorException("Tried assigning struggle reward, but failed")

        self.assign_item(opposite, item)
        return opposite

    def assignment_for_location(self, location_name: str) -> Optional[ItemAssignment]:
        return next(
            (a for a in self.assignments if a.location.name() == location_name), None
        )

    def assignment_for_item(self, item: InventoryItem) -> Optional[ItemAssignment]:
        return next((a for a in self.assignments if a.item.item == item), None)
    
    def assignment_for_item_id(self, item_id: int) -> Optional[ItemAssignment]:
        return next((a for a in self.assignments if a.item.item.id == item_id), None)

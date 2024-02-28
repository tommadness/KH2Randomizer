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
from List.ItemList import Items
from List.NewLocationList import Locations
from List.configDict import (
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
            - (sum([len(l.VanillaItems) for l in locations_with_vanilla_items]))
        )

        if self.progress_bar_vis:
            return

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

        restricted_reports = self.report_depths.very_restricted_locations
        restricted_proofs = self.proof_depths.very_restricted_locations
        restricted_story = self.story_depths.very_restricted_locations

        # leaving this code here for future bug testing. Puts a specific item in a specific location
        # placed_item = False
        # for item in allItems:
        #     if not placed_item and item.Id == 23:
        #         location_to_place = [loc for loc in validLocations if loc.LocationCategory is locationCategory.CHEST and loc.LocationId==463][0]
        #         if self.assignItem(location_to_place,item):
        #             validLocations.remove(location_to_place)
        #         allItems.remove(item)
        #         placed_item = True
        #         break

        invalid_test = []
        if restricted_reports:
            invalid_test.append(itemType.REPORT)
        if restricted_proofs:
            invalid_test.extend(proof.proof_item_types())
        if restricted_story:
            invalid_test.append(itemType.STORYUNLOCK)

        def item_sorter(item: KH2Item) -> int:
            if item.ItemType in invalid_test:
                # put the most restricted things first in the ordering
                return 3
            elif item.Rarity == itemRarity.MYTHIC:
                # put mythic things second, to let proofs get most leeway possible
                return 2
            else:
                return 1

        random.shuffle(item_pool)
        item_pool.sort(reverse=True, key=item_sorter)

        def compute_location_weights(
            item: KH2Item, location_pool: list[KH2Location]
        ) -> list[int]:
            loc_weights = self.location_weights
            if restricted_proofs or restricted_reports or restricted_story:
                result = [
                    loc_weights.get_weight(item.Rarity, loc)
                    if (any(i_type in loc.InvalidChecks for i_type in invalid_test))
                    else 0
                    for loc in location_pool
                ]
            else:
                result = [
                    loc_weights.get_weight(item.Rarity, loc) for loc in location_pool
                ]

            if restricted_reports and item.ItemType is itemType.REPORT:
                result = [
                    1 if itemType.REPORT not in loc.InvalidChecks else 0
                    for loc in location_pool
                ]
            if restricted_proofs and item.ItemType in proof.proof_item_types():
                result = [
                    1 if item.ItemType not in loc.InvalidChecks else 0
                    for loc in location_pool
                ]
            if restricted_story and item.ItemType is itemType.STORYUNLOCK:
                result = [
                    1 if itemType.STORYUNLOCK not in loc.InvalidChecks else 0
                    for loc in location_pool
                ]
            return result

        # chain logic placement
        if settings.chainLogic:
            from Module.seedEvaluation import LocationInformedSeedValidator

            validator = LocationInformedSeedValidator()

            if not any(item.item == proof.ProofOfNonexistence for item in item_pool):
                raise CantAssignItemException(
                    "Chain logic expects Proof of Nonexistence to be available"
                )

            unlocks = {}
            if settings.regular_rando:
                unlocks[locationType.HB] = [
                    [proof.ProofOfPeace.id],
                    [storyunlock.MembershipCard.id],
                ]
            elif settings.reverse_rando:
                unlocks[locationType.HB] = [[storyunlock.MembershipCard.id]]
            unlocks[locationType.OC] = [[storyunlock.BattlefieldsOfWar.id]]
            unlocks[locationType.LoD] = [[storyunlock.SwordOfTheAncestor.id]]
            unlocks[locationType.PL] = [[storyunlock.ProudFang.id]]
            unlocks[locationType.HT] = [[storyunlock.BoneFist.id]]
            unlocks[locationType.SP] = [[storyunlock.IdentityDisk.id]]
            unlocks[locationType.FormLevel] = [
                [form.ValorForm.id],
                [form.WisdomForm.id],
                [form.FinalForm.id],
                [form.MasterForm.id],
                [form.LimitForm.id],
            ]
            unlocks[locationType.TT] = [
                [storyunlock.IceCream.id],
                [storyunlock.IceCream.id],
            ]
            unlocks[locationType.BC] = [[storyunlock.BeastsClaw.id]]
            if settings.regular_rando:
                unlocks[locationType.Agrabah] = [
                    [
                        storyunlock.Scimitar.id,
                        magic.Fire.id,
                        magic.Blizzard.id,
                        magic.Thunder.id,
                    ]
                ]
            elif settings.reverse_rando:
                unlocks[locationType.Agrabah] = [
                    [storyunlock.Scimitar.id],
                    [magic.Fire.id, magic.Blizzard.id, magic.Thunder.id],
                ]
            unlocks[locationType.HUNDREDAW] = [
                [misc.TornPages.id],
                [misc.TornPages.id],
                [misc.TornPages.id],
                [misc.TornPages.id],
                [misc.TornPages.id],
            ]
            unlocks[locationType.LW] = [[proof.ProofOfConnection.id]]
            unlocks[locationType.PR] = [[storyunlock.SkillAndCrossbones.id]]
            unlocks[locationType.Atlantica] = [
                [magic.Thunder.id, magic.Thunder.id, magic.Thunder.id],
                [magic.Magnet.id, magic.Magnet.id],
            ]

            second_visit_locking_items = [
                storyunlock.MembershipCard.id,
                storyunlock.BattlefieldsOfWar.id,
                storyunlock.SwordOfTheAncestor.id,
                storyunlock.ProudFang.id,
                storyunlock.BoneFist.id,
                storyunlock.IdentityDisk.id,
                storyunlock.IceCream.id,
                storyunlock.BeastsClaw.id,
                storyunlock.Scimitar.id,
                storyunlock.SkillAndCrossbones.id,
            ]
            # stuff that we can safely remove the first step from
            flex_logical_locks = [
                storyunlock.BattlefieldsOfWar.id,
                storyunlock.SwordOfTheAncestor.id,
                storyunlock.ProudFang.id,
                storyunlock.BoneFist.id,
                storyunlock.IdentityDisk.id,
                storyunlock.BeastsClaw.id,
                storyunlock.SkillAndCrossbones.id,
                form.ValorForm.id,
                form.WisdomForm.id,
                form.FinalForm.id,
                form.MasterForm.id,
                form.LimitForm.id,
            ]

            locking_items = []
            for loc_type in settings.enabledLocations:
                if loc_type in unlocks:
                    locking_items.extend(unlocks[loc_type])

            for i in self.starting_item_ids + [
                shop_item.Id for shop_item in self.shop_items
            ]:
                if [i] in locking_items:
                    locking_items.remove([i])
                if [
                    i,
                    magic.Fire.id,
                    magic.Blizzard.id,
                    magic.Thunder.id,
                ] in locking_items:
                    locking_items.remove(
                        [i, magic.Fire.id, magic.Blizzard.id, magic.Thunder.id]
                    )
            for i in vanilla_item_ids:  # TODO add vanilla worlds to chain
                if [i] in locking_items:
                    locking_items.remove([i])

            if not settings.chainLogicIncludeTerra:
                if [proof.ProofOfConnection.id] in locking_items:
                    locking_items.remove([proof.ProofOfConnection.id])

            if len(locking_items) > settings.chainLogicMinLength:
                # keep the last parts of the chain
                num_to_remove = min(
                    len(locking_items) - settings.chainLogicMinLength,
                    len(flex_logical_locks),
                )

                random.shuffle(flex_logical_locks)
                # remove N flex locks from the list
                for i in range(num_to_remove):
                    print(locking_items)
                    print(flex_logical_locks)
                    locking_items.remove([flex_logical_locks[i]])

            minimum_terra_depth = (
                len(locking_items) - 5 if settings.chainLogicTerraLate else 0
            )

            if self.yeet_the_bear:
                locking_items.remove([misc.TornPages.id])

            if settings.extended_placement_logic:
                locking_items.remove([form.FinalForm.id])

            terra = (
                settings.chainLogicIncludeTerra
                and [proof.ProofOfConnection.id] in locking_items
            )
            tt_condition = [storyunlock.IceCream.id] in locking_items and [
                storyunlock.IceCream.id
            ] in locking_items
            pop_condition = [proof.ProofOfPeace.id] in locking_items
            hb_condition = [
                storyunlock.MembershipCard.id
            ] in locking_items and pop_condition
            ag_condition = [storyunlock.Scimitar.id] in locking_items
            atlantica_condition = [magic.Magnet.id, magic.Magnet.id] in locking_items
            second_visit_condition = settings.proofDepth in [
                locationDepth.Superbosses,
                locationDepth.SecondVisitOnly,
                locationDepth.LastStoryBoss,
            ]
            data_condition = settings.proofDepth is locationDepth.Superbosses
            story_data_condition = settings.storyDepth is locationDepth.Superbosses

            if second_visit_condition:
                # check if enough unlock items are available for the chain
                num_proofs_in_chain = (
                    int(pop_condition) + int(terra) + int(not self.yeet_the_bear)
                )

                counter = 0
                for world_unlocks in locking_items:
                    for i in world_unlocks:
                        if i in second_visit_locking_items:
                            counter += 1
                if counter < num_proofs_in_chain:
                    raise SettingsException(
                        "Not enough locked second visits for chain logic."
                    )

            while True:
                random.shuffle(locking_items)
                # scimitar has to be after fire/blizz/thunder
                if ag_condition and locking_items.index(
                    [magic.Fire.id, magic.Blizzard.id, magic.Thunder.id]
                ) > locking_items.index([storyunlock.Scimitar.id]):
                    continue
                # ice cream needs to be after ice cream
                if tt_condition and locking_items.index(
                    [storyunlock.IceCream.id]
                ) > locking_items.index([storyunlock.IceCream.id]):
                    continue
                # proof of peace needs to be after membership card
                if hb_condition and locking_items.index(
                    [storyunlock.MembershipCard.id]
                ) > locking_items.index([proof.ProofOfPeace.id]):
                    continue
                if (
                    terra
                    and locking_items.index([proof.ProofOfConnection.id])
                    < minimum_terra_depth
                ):
                    continue
                if atlantica_condition and locking_items.index(
                    [magic.Magnet.id, magic.Magnet.id]
                ) > locking_items.index(
                    [magic.Thunder.id, magic.Thunder.id, magic.Thunder.id]
                ):
                    continue
                if story_data_condition:
                    form_indices = [
                        locking_items.index(x) for x in unlocks[locationType.FormLevel]
                    ]
                    membership_index = locking_items.index(
                        [storyunlock.MembershipCard.id]
                    )

                    # print(f"{storyunlock.MembershipCard.id in locking_items[proof_index-1]} {not all(x<proof_index for x in form_indices)}")
                    if not all(x < membership_index for x in form_indices):
                        continue

                # proof depth checking
                if second_visit_condition:
                    if pop_condition:
                        proof_index = locking_items.index([proof.ProofOfPeace.id])
                        if proof_index == 0:
                            continue
                        if not any(
                            it in locking_items[proof_index - 1]
                            for it in second_visit_locking_items
                        ):
                            continue
                        form_indices = [
                            locking_items.index(x)
                            for x in unlocks[locationType.FormLevel]
                        ]
                        # print(f"{storyunlock.MembershipCard.id in locking_items[proof_index-1]} {not all(x<proof_index for x in form_indices)}")
                        if (
                            data_condition
                            and storyunlock.MembershipCard.id
                            in locking_items[proof_index - 1]
                            and not all(x < proof_index for x in form_indices)
                        ):
                            continue
                    if terra:
                        proof_index = locking_items.index([proof.ProofOfConnection.id])
                        if proof_index == 0:
                            continue
                        if not any(
                            it in locking_items[proof_index - 1]
                            for it in second_visit_locking_items
                        ):
                            continue
                        form_indices = [
                            locking_items.index(x)
                            for x in unlocks[locationType.FormLevel]
                        ]
                        # print(f"{storyunlock.MembershipCard.id in locking_items[proof_index-1]} {not all(x<proof_index for x in form_indices)}")
                        if (
                            data_condition
                            and storyunlock.MembershipCard.id
                            in locking_items[proof_index - 1]
                            and not all(x < proof_index for x in form_indices)
                        ):
                            continue
                    if not self.yeet_the_bear:
                        if not any(
                            it in locking_items[-1] for it in second_visit_locking_items
                        ):
                            continue
                break
            if self.yeet_the_bear:
                locking_items.append([misc.TornPages.id])

            force_obtained = []
            if len(locking_items) > settings.chainLogicMinLength:
                # keep the last parts of the chain
                num_to_remove = len(locking_items) - settings.chainLogicMinLength
                force_obtained = locking_items[:num_to_remove]
                locking_items = locking_items[num_to_remove:]

            # add the proof of nonexistence at the end of the chain
            locking_items.append([proof.ProofOfNonexistence.id])

            if settings.extended_placement_logic:
                locking_items[-1].append(form.FinalForm.id)

            # print(locking_items)

            validator.prep_requirements_list(settings, self)

            current_inventory = [] + self.starting_item_ids
            for i in force_obtained:
                current_inventory += i
            if settings.reverse_rando:
                current_inventory += [
                    growth.HighJump1.id,
                    growth.HighJump2.id,
                    growth.HighJump3.id,
                    growth.QuickRun1.id,
                    growth.QuickRun2.id,
                    growth.QuickRun3.id,
                    growth.AerialDodge1.id,
                    growth.AerialDodge2.id,
                    growth.AerialDodge3.id,
                    growth.Glide1.id,
                    growth.Glide2.id,
                    growth.Glide3.id,
                    growth.DodgeRoll1.id,
                    growth.DodgeRoll2.id,
                    growth.DodgeRoll3.id,
                ]

            def open_location(inv, loc):
                return (
                    validator.is_location_available(inv, loc)
                    and (
                        not settings.extended_placement_logic
                        or loc.name() != hb.CheckLocation.DataDemyxApBoost
                    )
                    and (locationType.SYNTH not in loc.LocationTypes)
                )

            accessible_locations = [
                [l for l in valid_locations if open_location(current_inventory, l)]
            ]
            for items in locking_items:
                accessible_locations_start = [
                    l for l in valid_locations if open_location(current_inventory, l)
                ]
                accessible_locations_new = [
                    l
                    for l in valid_locations
                    if open_location(current_inventory + items, l)
                    and l not in accessible_locations_start
                ]
                accessible_locations.append(accessible_locations_new)
                # print(f"{items} unlocked {len(accessible_locations[-1])}")
                current_inventory += items
            for iter, items in enumerate(locking_items):
                accessible_locations_new = accessible_locations[iter]
                if len(accessible_locations_new) == 0:
                    raise GeneratorException(
                        "Chain logic created a situation where the chain item couldn't be placed"
                    )
                for i in items:
                    # find item in item list
                    if len(accessible_locations_new) == 0:
                        raise GeneratorException(
                            f"Chain logic couldn't place an item because it ran out of locations."
                        )

                    i_data = next((it for it in item_pool if it.Id == i), None)
                    if i_data is None:
                        continue
                    weights = compute_location_weights(i_data, accessible_locations_new)
                    # if len(weights)==0:
                    #     raise GeneratorException(f"Chain Logic failed to place {i_data}")
                    # if sum(weights)==0:
                    #     raise GeneratorException(f"Chain Logic failed to place {i_data}")

                    # try to assign the item multiple times
                    goa_location_list = [
                        loc
                        for loc in accessible_locations_new
                        if loc.name() == starting.CheckLocation.GoaLostIllusion
                    ]
                    for _ in range(5):
                        if (
                            iter == 0 and len(goa_location_list) > 0
                        ):  # put the first chain item in the goa
                            random_location = goa_location_list[0]
                        else:
                            random_location = random.choices(
                                accessible_locations_new, weights
                            )[0]
                        if i_data.ItemType not in random_location.InvalidChecks:
                            item_pool.remove(i_data)
                            if self.assign_item(random_location, i_data):
                                valid_locations.remove(random_location)
                                accessible_locations_new.remove(random_location)

                                struggle_pair = self._maybe_assign_struggle_pair(
                                    random_location, i_data, accessible_locations_new
                                )
                                if struggle_pair is not None:
                                    valid_locations.remove(struggle_pair)
                                    accessible_locations_new.remove(struggle_pair)
                            break

        # assign valid items to all valid locations remaining
        if self.yeet_the_bear:
            # move proof of nonexistence to the front of the item pool if it's in there
            if proof.ProofOfNonexistence in item_pool:
                item_pool.insert(0,item_pool.pop(item_pool.index(proof.ProofOfNonexistence)))

        for item in item_pool:
            if len(valid_locations) == 0:
                raise CantAssignItemException(f"Ran out of locations to assign items")

            if item.item == proof.ProofOfNonexistence and self.yeet_the_bear:
                # Manually assign to Starry Hill
                yeet_locations = _find_locations(
                    haw.yeet_the_bear_location_names(), valid_locations
                )
                if len(yeet_locations) > 0:
                    yeet_location = random.choice(yeet_locations)
                    if self.assign_item(yeet_location, item):
                        valid_locations.remove(yeet_location)
                    continue
                else:
                    raise CantAssignItemException(
                        "None of the Starry Hill locations are available for Yeet the Bear"
                    )

            weights = compute_location_weights(item, valid_locations)

            count = 0
            while True:
                count += 1
                if len(weights) == 0:
                    raise CantAssignItemException(
                        f"Ran out of locations to assign items to."
                    )
                if sum(weights) == 0 and restricted_reports:
                    raise CantAssignItemException(
                        f"Somehow, can't assign an item. If using report depth option that restricts to specific bosses, make sure all worlds with doors in GoA are enabled."
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

        invalid_locations.extend(valid_locations)
        self.assign_junk_locations(settings, invalid_locations)

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

            if not self.report_depths.is_valid(loc):
                loc.InvalidChecks.append(itemType.REPORT)

            if not self.proof_depths.is_valid(loc):
                loc.InvalidChecks.extend(proof.proof_item_types())

            if not self.story_depths.is_valid(loc):
                loc.InvalidChecks.append(itemType.STORYUNLOCK)

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

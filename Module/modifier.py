import random
from collections import Counter
from typing import Callable

from Class.exceptions import GeneratorException, SettingsException
from Class.itemClass import KH2Item
from List.configDict import LevelUpStatBonus, AbilityPoolOption
from List.inventory import growth, ability, storyunlock, magic
from List.inventory.growth import GrowthAbility, GrowthType
from List.inventory.magic import MagicElement
from List.inventory.storyunlock import StoryUnlock


class SeedModifier:
    @staticmethod
    def ability_list_modifier(
        option: AbilityPoolOption,
    ) -> Callable[[list[KH2Item], list[KH2Item]], list[KH2Item]]:
        if option == AbilityPoolOption.DEFAULT:
            return SeedModifier.default_ability_pool
        elif option == AbilityPoolOption.RANDOMIZE:
            return SeedModifier.random_ability_pool
        elif option == AbilityPoolOption.RANDOMIZE_SUPPORT:
            return SeedModifier.random_support_ability_pool
        elif option == AbilityPoolOption.RANDOMIZE_STACKABLE:
            return SeedModifier.random_stackable_ability_pool
        else:
            raise SettingsException("Invalid ability pool option")

    @staticmethod
    def default_ability_pool(
        action: list[KH2Item], support: list[KH2Item]
    ) -> list[KH2Item]:
        return action + support

    @staticmethod
    def random_ability_pool(
        action: list[KH2Item], support: list[KH2Item]
    ) -> list[KH2Item]:
        randomizable_list = action + support
        randomizable_dict: dict[str, KH2Item] = {i.Name: i for i in randomizable_list}
        possible_abilities = list(
            set(
                i.Name
                for i in randomizable_list
                if i.Name not in [ability.SecondChance.name, ability.OnceMore.name]
            )
        )
        possible_abilities.sort()
        random_ability_pool = []
        for _ in range(len(randomizable_list) - 2):
            choice: str = random.choice(possible_abilities)
            random_ability_pool.append(randomizable_dict[choice])
            # Limit only 1 of each action ability in the pool, to make it more interesting
            if choice in [i.Name for i in action]:
                possible_abilities.remove(choice)

        # Make sure there is one OM and one SC so the tracker behaves
        random_ability_pool.append(randomizable_dict[ability.SecondChance.name])
        random_ability_pool.append(randomizable_dict[ability.OnceMore.name])
        return random_ability_pool

    @staticmethod
    def random_support_ability_pool(
        action: list[KH2Item], support: list[KH2Item]
    ) -> list[KH2Item]:
        randomizable_list = support
        randomizable_dict: dict[str, KH2Item] = {i.Name: i for i in randomizable_list}
        possible_abilities = list(
            set(
                i.Name
                for i in randomizable_list
                if i.Name not in [ability.SecondChance.name, ability.OnceMore.name]
            )
        )
        possible_abilities.sort()
        random_ability_pool = []
        for _ in range(len(randomizable_list) - 2):
            choice: str = random.choice(possible_abilities)
            random_ability_pool.append(randomizable_dict[choice])

        # Make sure there is one OM and one SC so the tracker behaves
        random_ability_pool.append(randomizable_dict[ability.SecondChance.name])
        random_ability_pool.append(randomizable_dict[ability.OnceMore.name])
        return random_ability_pool + action

    @staticmethod
    def random_stackable_ability_pool(
        action: list[KH2Item], support: list[KH2Item]
    ) -> list[KH2Item]:
        stackable_abilities = [
            ability.ComboPlus.name,
            ability.AirComboPlus.name,
            ability.ComboBoost.name,
            ability.AirComboBoost.name,
            ability.ReactionBoost.name,
            ability.FinishingPlus.name,
            ability.NegativeCombo.name,
            ability.BerserkCharge.name,
            ability.DamageDrive.name,
            ability.DriveBoost.name,
            ability.FormBoost.name,
            ability.SummonBoost.name,
            ability.ExperienceBoost.name,
            ability.Draw.name,
            ability.Jackpot.name,
            ability.LuckyLucky.name,
            ability.DriveConverter.name,
            ability.FireBoost.name,
            ability.BlizzardBoost.name,
            ability.ThunderBoost.name,
            ability.ItemBoost.name,
            ability.MpRage.name,
            ability.MpHaste.name,
            ability.MpHastera.name,
            ability.MpHastega.name,
            ability.Defender.name,
            ability.DamageControl.name,
            ability.CombinationBoost.name,
        ]
        ability_list = support + action
        ability_dict: dict[str, KH2Item] = {i.Name: i for i in ability_list}
        unique_abilities = list(set(i.Name for i in ability_list))
        unique_abilities.sort()
        random_ability_pool = []
        for unique_ability in unique_abilities:
            random_ability_pool.append(ability_dict[unique_ability])
        for _ in range(len(ability_list) - len(unique_abilities)):
            choice = random.choice(stackable_abilities)
            random_ability_pool.append(ability_dict[choice])

        return random_ability_pool

    @staticmethod
    def level_up_stat_pool(glass_cannon: bool) -> list[tuple[LevelUpStatBonus, int]]:
        stat_pool = SeedModifier.level_up_stat_pool_weighted(
            def_rate=0 if glass_cannon else 25
        )
        return [(s[0], s[1]) for s in stat_pool]

    @staticmethod
    def level_up_stat_pool_weighted(
        str_rate: int = 25,
        mag_rate: int = 25,
        def_rate: int = 25,
        ap_rate: int = 25,
    ) -> list[tuple[LevelUpStatBonus, int, int]]:
        valid_stat_list = [
            (LevelUpStatBonus.STRENGTH, 2, str_rate),
            (LevelUpStatBonus.MAGIC, 2, mag_rate),
            (LevelUpStatBonus.DEFENSE, 1, def_rate),
            (LevelUpStatBonus.AP, 2, ap_rate),
        ]
        # remove any stats with zero weight
        valid_stat_list = [
            stat_config for stat_config in valid_stat_list if stat_config[2] > 0
        ]
        if len(valid_stat_list)<2:
            raise GeneratorException("Not enough valid stats for level ups")

        # rescale the weights to sum to 100
        total_sum = sum([stat_config[2] for stat_config in valid_stat_list])
        valid_stat_list = [
            (stat_config[0], stat_config[1], (100 * stat_config[2]) // total_sum)
            for stat_config in valid_stat_list
        ]
        new_total_sum = sum([stat_config[2] for stat_config in valid_stat_list])
        diff_adjustment = 0
        while new_total_sum + diff_adjustment < 100:
            old_tuple = valid_stat_list[diff_adjustment % len(valid_stat_list)]
            valid_stat_list[diff_adjustment % len(valid_stat_list)] = (
                old_tuple[0],
                old_tuple[1],
                old_tuple[2] + 1,
            )
            diff_adjustment += 1

        return valid_stat_list

    @staticmethod
    def starting_growth(specific_growth: dict[GrowthType, int], random_range: tuple[int, int]) -> list[GrowthAbility]:
        available_growth = growth.all_individual_growth_types().copy()

        chosen: list[GrowthType] = []
        for growth_type, count in specific_growth.items():
            for _ in range(count):
                chosen.append(growth_type)
                available_growth.remove(growth_type)

        random_min, random_max = random_range
        random_count = random.randint(random_min, random_max)
        if random_count == 0:
            pass
        elif random_count >= len(available_growth):
            chosen.extend(available_growth)
        else:
            chosen.extend(random.sample(available_growth, k=random_count))

        result: list[GrowthAbility] = []
        for growth_type, level in Counter(chosen).items():
            result.extend(growth.growth_to_level(level, growth_type))
        return result

    @staticmethod
    def starting_magic(specific_magics: dict[MagicElement, int], random_range: tuple[int, int]) -> list[MagicElement]:
        available_magic_elements = magic.all_individual_magics().copy()

        result: list[MagicElement] = []
        for magic_element, count in specific_magics.items():
            for _ in range(count):
                result.append(magic_element)
                available_magic_elements.remove(magic_element)

        random_min, random_max = random_range
        random_count = random.randint(random_min, random_max)
        if random_count == 0:
            return result
        elif random_count >= len(available_magic_elements):
            result.extend(available_magic_elements)
            return result
        else:
            result.extend(random.sample(available_magic_elements, k=random_count))
            return result

    @staticmethod
    def starting_unlocks(specific_unlocks: dict[StoryUnlock, int], random_range: tuple[int, int]) -> list[StoryUnlock]:
        available_unlocks = storyunlock.all_individual_story_unlocks().copy()

        result: list[StoryUnlock] = []
        for unlock, count in specific_unlocks.items():
            for _ in range(count):
                result.append(unlock)
                available_unlocks.remove(unlock)

        random_min, random_max = random_range
        random_count = random.randint(random_min, random_max)
        if random_count == 0:
            return result
        elif random_count >= len(available_unlocks):
            result.extend(available_unlocks)
            return result
        else:
            result.extend(random.sample(available_unlocks, k=random_count))
            return result

import random
from typing import Callable

from Class.exceptions import GeneratorException, SettingsException
from Class.itemClass import KH2Item
from List.configDict import LevelUpStatBonus, StartingMovementOption, AbilityPoolOption, StartingVisitMode, locationType
from List.inventory import growth, ability, storyunlock
from List.inventory.growth import GrowthAbility, GrowthType
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
    def starting_growth(option: StartingMovementOption) -> list[GrowthAbility]:
        if option == StartingMovementOption.DISABLED:
            return []
        elif option == StartingMovementOption.LEVEL_1:
            return growth.all_growth_to_level(1)
        elif option == StartingMovementOption.LEVEL_2:
            return growth.all_growth_to_level(2)
        elif option == StartingMovementOption.LEVEL_3:
            return growth.all_growth_to_level(3)
        elif option == StartingMovementOption.LEVEL_4:
            return growth.all_growth_to_level(4)
        elif option == StartingMovementOption.RANDOM_3:
            return SeedModifier._random_growth(3)
        elif option == StartingMovementOption.RANDOM_5:
            return SeedModifier._random_growth(5)
        else:
            raise GeneratorException(f"Unknown option {option}")

    @staticmethod
    def _random_growth(num_growth_abilities: int) -> list[GrowthAbility]:
        options = [growth_ability.growth_type for growth_ability in growth.all_growth()]
        levels_by_growth_type: dict[GrowthType, int] = {}
        for chosen_growth_type in random.sample(options, k=num_growth_abilities):
            if chosen_growth_type in levels_by_growth_type:
                levels_by_growth_type[chosen_growth_type] = (
                    levels_by_growth_type[chosen_growth_type] + 1
                )
            else:
                levels_by_growth_type[chosen_growth_type] = 1

        random_growth = []
        for growth_type, level in levels_by_growth_type.items():
            random_growth.extend(growth.growth_to_level(level, growth_type))
        return random_growth

    @staticmethod
    def starting_unlocks(
            mode: StartingVisitMode,
            random_range: tuple[int, int],
            specific_unlocks: dict[locationType, int],
    ) -> list[StoryUnlock]:
        if mode is StartingVisitMode.ALL:
            return storyunlock.all_individual_story_unlocks()
        elif mode is StartingVisitMode.FIRST:
            return storyunlock.all_story_unlocks()
        elif mode is StartingVisitMode.NONE:
            return []
        elif mode is StartingVisitMode.RANDOM:
            random_min, random_max = random_range
            random_count = random.randint(random_min, random_max)
            return random.sample(storyunlock.all_individual_story_unlocks(), k=random_count)
        elif mode is StartingVisitMode.SPECIFIC:
            result: list[StoryUnlock] = []
            for location, count in specific_unlocks.items():
                result.extend([storyunlock.story_unlock_for_location(location)] * count)
            return result
        elif mode is StartingVisitMode.CUSTOM:
            result: list[StoryUnlock] = []
            for location, count in specific_unlocks.items():
                result.extend([storyunlock.story_unlock_for_location(location)] * count)
            random_pool: list[StoryUnlock] = []
            for unlock in storyunlock.all_story_unlocks():
                random_pool.extend([unlock] * (unlock.visit_count - specific_unlocks[unlock.location]))
            random_min, random_max = random_range
            random_count = random.randint(random_min, random_max)
            result.extend(random.sample(random_pool, k=random_count))
            return result
        else:
            raise GeneratorException(f"Unknown mode {mode}")

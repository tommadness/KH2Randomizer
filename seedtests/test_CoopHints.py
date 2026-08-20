import random
import unittest

from Class import settingkey
from Class.seedSettings import SeedSettings
from List.configDict import HintType
from Module import RandomizerSettings
from Module.Hints.HintUtils import HintUtils
from Module.hints import Hints, HintData
from seedtests import seedtest

_COOP_SEED_COUNT = 5

_COOP_HINT_SYSTEMS = [HintType.SHANANAS, HintType.JSMARTEE, HintType.POINTS, HintType.SPOILER, HintType.PATH]

_COOP_HINT_TYPES = ["default", "reversed", "random"]


class Tests(unittest.TestCase):

    def test_coop_world_order_for_all_hint_system_and_coop_order_combinations(self):
        for player1_hint_system in _COOP_HINT_SYSTEMS:
            for player2_hint_system in _COOP_HINT_SYSTEMS:
                for coop_hint_type in _COOP_HINT_TYPES:
                    with self.subTest(
                        player1_hint_system=player1_hint_system,
                        player2_hint_system=player2_hint_system,
                        coop_hint_type=coop_hint_type,
                    ):
                        self._assert_coop_world_order_relationship(
                            player1_hint_system, player2_hint_system, coop_hint_type
                        )

    def _assert_coop_world_order_relationship(
        self, player1_hint_system: str, player2_hint_system: str, coop_hint_type: str
    ):
        seed_settings = SeedSettings()
        # Co-op hints require progression hints to be enabled.
        seed_settings.set(settingkey.PROGRESSION_HINTS, True)
        seed_settings.set(settingkey.HINT_SYSTEM, HintType.SHANANAS)
        seed_settings.set(settingkey.COOP_HINTS_ENABLED, True)
        seed_settings.set(settingkey.COOP_HINT_TYPE, coop_hint_type)
        seed_settings.set(settingkey.COOP_PLAYER1_HINT_SYSTEM, player1_hint_system)
        seed_settings.set(settingkey.COOP_PLAYER2_HINT_SYSTEM, player2_hint_system)
        seed_settings.set(settingkey.COOP_PLAYER_NUMBER, "1")

        for randomizer, settings in seedtest.test_seeds_with_settings(seed_settings, _COOP_SEED_COUNT):
            random_state = random.getstate()
            settings.coop_player_number = "1"
            player1_world_order = self._world_order(Hints.generate_hints_v2(randomizer, settings),settings)

            random.setstate(random_state)
            settings.coop_player_number = "2"
            player2_world_order = self._world_order(Hints.generate_hints_v2(randomizer, settings),settings)

            failure_message = (
                f"player 1 hint system={player1_hint_system}, player 2 hint system={player2_hint_system}, "
                f"coop hint type={coop_hint_type}, seed={settings.random_seed}\n"
                f"player 1 world order: {player1_world_order}\n"
                f"player 2 world order: {player2_world_order}"
            )
            if coop_hint_type == "default":
                self.assertEqual(player1_world_order, player2_world_order, failure_message)
            elif coop_hint_type == "reversed":
                self.assertEqual(list(reversed(player1_world_order)), player2_world_order, failure_message)
            elif coop_hint_type == "random":
                self.assertCountEqual(player1_world_order, player2_world_order, failure_message)
                # it's so unlikely to get the same order as the reversed and same ordering, we can test for inequality with other orderings.
                self.assertNotEqual(list(reversed(player1_world_order)), player2_world_order, failure_message)
                self.assertNotEqual(player1_world_order, player2_world_order, failure_message)
            else:
                self.fail(f"Unknown coop hint type: {coop_hint_type}")

    @staticmethod
    def _world_order(hint_data: HintData, settings: RandomizerSettings) -> list:
        exclude_list = HintUtils.update_disabled_worlds_on_tracker(settings)
        hintable_worlds = [
            world for world in HintUtils.hintable_worlds() if world not in exclude_list
        ]

        if hint_data.get("hintsType") in (HintType.SHANANAS, HintType.POINTS) and "world_order" in hint_data:
            temp_world_order = list(hint_data["world_order"])
            return [w for w in temp_world_order if w in hintable_worlds]
        world_key = "HintedWorld" if hint_data.get("hintsType") == HintType.PATH else "World"
        reports = hint_data["Reports"]
        sorted_keys = sorted(reports.keys())
        temp_world_order = [reports[slot][world_key] for slot in sorted_keys]
        return [w for w in temp_world_order if w in hintable_worlds]


if __name__ == '__main__':
    unittest.main()

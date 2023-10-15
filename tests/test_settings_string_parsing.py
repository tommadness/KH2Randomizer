import unittest

from Class.seedSettings import Toggle, IntSpinner, FloatSpinner, SingleSelect, MultiSelect, SeedSettings, \
    SettingGroup, settings_by_name


class Tests(unittest.TestCase):

    def test_toggle(self):
        setting = Toggle(name='Test', group=SettingGroup.EXP_STATS, ui_label='Test', shared=True, default=False)

        self.assertEqual(True, setting.parse_settings_string(setting.settings_string(True)))
        self.assertEqual(False, setting.parse_settings_string(setting.settings_string(False)))

    def test_int_spinner(self):
        setting = IntSpinner(
            name='Test',
            group=SettingGroup.EXP_STATS,
            ui_label='Test',
            minimum=5,
            maximum=750,
            step=1,
            shared=True,
            default=500
        )

        self.assertEqual(5, setting.parse_settings_string(setting.settings_string(5)))
        self.assertEqual(299, setting.parse_settings_string(setting.settings_string(299)))
        self.assertEqual(750, setting.parse_settings_string(setting.settings_string(750)))

    def test_float_spinner(self):
        setting = FloatSpinner(
            name='Test',
            group=SettingGroup.EXP_STATS,
            ui_label='Test',
            minimum=3.0,
            maximum=180.5,
            step=0.5,
            shared=True,
            default=10.0
        )

        self.assertEqual(3.0, setting.parse_settings_string(setting.settings_string(3.0)))
        self.assertEqual(99.5, setting.parse_settings_string(setting.settings_string(99.5)))
        self.assertEqual(180.5, setting.parse_settings_string(setting.settings_string(180.5)))

    def test_single_select(self):
        setting = SingleSelect(
            name='Test',
            group=SettingGroup.EXP_STATS,
            ui_label='Test',
            choices={'key' + str(i): 'value' + str(i) for i in range(1000)},
            shared=True,
            default="a"
        )

        self.assertEqual('key0', setting.parse_settings_string(setting.settings_string('key0')))
        self.assertEqual('key527', setting.parse_settings_string(setting.settings_string('key527')))
        self.assertEqual('key999', setting.parse_settings_string(setting.settings_string('key999')))

    def test_multi_select(self):
        setting = MultiSelect(
            name='Test',
            group=SettingGroup.EXP_STATS,
            ui_label='Test',
            choices={'key' + str(i): 'value' + str(i) for i in range(1000)},
            shared=True,
            default=[]
        )

        self.assertEqual([], setting.parse_settings_string(setting.settings_string([])))
        self.assertEqual(['key482'], setting.parse_settings_string(setting.settings_string(['key482'])))
        self.assertEqual(
            ['key0', 'key527', 'key999'],
            setting.parse_settings_string(setting.settings_string(['key999', 'key0', 'key527']))
        )
        self.assertEqual(
            setting.choice_keys,
            setting.parse_settings_string(setting.settings_string(setting.choice_keys))
        )

    def test_full_string_toggles_all_true(self):
        toggle_setting_names = []
        for setting in settings_by_name.values():
            if isinstance(setting, Toggle):
                toggle_setting_names.append(setting.name)

        settings = SeedSettings()
        for name in toggle_setting_names:
            settings.set(name, True)

        string = settings.settings_string(include_private=True)

        for name in toggle_setting_names:
            settings.set(name, False)

        settings.apply_settings_string(string, include_private=True)

        for name in toggle_setting_names:
            self.assertTrue(settings.get(name), msg=name)

    def test_full_string_toggles_all_false(self):
        toggle_setting_names = []
        for setting in settings_by_name.values():
            if isinstance(setting, Toggle):
                toggle_setting_names.append(setting.name)

        settings = SeedSettings()
        for name in toggle_setting_names:
            settings.set(name, False)

        string = settings.settings_string(include_private=True)

        for name in toggle_setting_names:
            settings.set(name, True)

        settings.apply_settings_string(string, include_private=True)

        for name in toggle_setting_names:
            self.assertFalse(settings.get(name), msg=name)


if __name__ == '__main__':
    unittest.main()

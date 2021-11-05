# import unittest

# from Module.seedshare import SharedSeed, InvalidShareStringFormatException, IncompatibleShareStringVersionException


# class Tests(unittest.TestCase):

#     def test_unrecognized_formats(self):
#         with self.assertRaises(InvalidShareStringFormatException):
#             SharedSeed.from_share_string(local_generator_version='1.0', share_string='')
#         with self.assertRaises(InvalidShareStringFormatException):
#             SharedSeed.from_share_string(local_generator_version='1.0', share_string='this_is_a_bad_string')

#     def test_version_mismatch(self):
#         with self.assertRaises(IncompatibleShareStringVersionException):
#             SharedSeed.from_share_string(local_generator_version='1.1', share_string='1.0$test_seed$1$0-0-0')

#     def test_valid_format_spoiler_on(self):
#         shared_seed = SharedSeed.from_share_string(local_generator_version='1.0', share_string='1.0$test_seed$1$0-0-0')
#         self.assertEqual('1.0', shared_seed.generator_version)
#         self.assertEqual('test_seed', shared_seed.seed_name)
#         self.assertTrue(shared_seed.spoiler_log)
#         self.assertEqual('0-0-0', shared_seed.settings_string)

#     def test_valid_format_spoiler_off(self):
#         shared_seed = SharedSeed.from_share_string(local_generator_version='1.1', share_string='1.1$test_seed$0$0-0-0')
#         self.assertEqual('1.1', shared_seed.generator_version)
#         self.assertEqual('test_seed', shared_seed.seed_name)
#         self.assertFalse(shared_seed.spoiler_log)
#         self.assertEqual('0-0-0', shared_seed.settings_string)

#     def test_back_and_forth_spoiler_on(self):
#         shared_seed_before = SharedSeed(
#             generator_version='1.0',
#             seed_name='test_seed',
#             spoiler_log=True,
#             settings_string='0-1-A'
#         )
#         share_string = shared_seed_before.to_share_string()
#         shared_seed_after = SharedSeed.from_share_string(local_generator_version='1.0', share_string=share_string)
#         self.assertEqual('1.0', shared_seed_after.generator_version)
#         self.assertEqual('test_seed', shared_seed_after.seed_name)
#         self.assertTrue(shared_seed_after.spoiler_log)
#         self.assertEqual('0-1-A', shared_seed_after.settings_string)

#     def test_back_and_forth_spoiler_off(self):
#         shared_seed_before = SharedSeed(
#             generator_version='1.1',
#             seed_name='test_it',
#             spoiler_log=False,
#             settings_string='G-O-A'
#         )
#         share_string = shared_seed_before.to_share_string()
#         shared_seed_after = SharedSeed.from_share_string(local_generator_version='1.1', share_string=share_string)
#         self.assertEqual('1.1', shared_seed_after.generator_version)
#         self.assertEqual('test_it', shared_seed_after.seed_name)
#         self.assertFalse(shared_seed_after.spoiler_log)
#         self.assertEqual('G-O-A', shared_seed_after.settings_string)


# if __name__ == '__main__':
#     unittest.main()

import unittest

from Module.paths import with_caps_extensions


class Tests(unittest.TestCase):

    def test_with_caps_extensions(self):
        result = with_caps_extensions(".png", ".dds")
        self.assertEqual({ ".dds", ".DDS", ".png", ".PNG" }, result)


if __name__ == "__main__":
    unittest.main()

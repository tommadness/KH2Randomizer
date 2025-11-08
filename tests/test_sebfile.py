import struct
import unittest

from Module.cosmeticsmods.keyblade import KeybladeRandomizer


class Tests(unittest.TestCase):

    def test_generate_501(self):
        data = KeybladeRandomizer.seb_file_data(sound_id=501)
        origin, sound_id_a, _, sound_id_b, scd_path = struct.unpack("<8sHHH2x32s", data)
        self.assertEqual(501, sound_id_a)
        self.assertEqual(501, sound_id_b)
        self.assertEqual("se/obj/se501", scd_path.decode("utf-8").strip("\x00"))

    def test_generate_9500(self):
        data = KeybladeRandomizer.seb_file_data(sound_id=9500)
        origin, sound_id_a, _, sound_id_b, scd_path = struct.unpack("<8sHHH2x32s", data)
        self.assertEqual(9500, sound_id_a)
        self.assertEqual(9500, sound_id_b)
        self.assertEqual("se/obj/se9500", scd_path.decode("utf-8").strip("\x00"))


if __name__ == '__main__':
    unittest.main()

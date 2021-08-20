
import sys
sys.path.append("..")
from Module.randomBGM import RandomBGM, musicList, musicPaths
import unittest


class Tests(unittest.TestCase):
    def test_bgm_no_pc(self):
        options = {
            "games": ["KH2"],
            "options": []
        }
        platform = "PS2"
        result = RandomBGM.randomizeBGM(options, platform)
        assert result == ""

    def test_bgm_no_games(self):
        options = {
            "games": [],
            "options": []
        }
        platform = "PC"
        result = RandomBGM.randomizeBGM(options, platform)
        assert result == ""

    def test_bgm_kh2(self):
        options = {
            "games": ["KH2"],
            "options": []
        }
        platform = "PC"
        result = RandomBGM.randomizeBGM(options, platform)
        assert type(result) == list
        assert self.check_songs_are_from(result, games=["KH2"])


    def test_bgm_kh1(self):
        options = {
            "games": ["KH1"],
            "options": []
        }
        platform = "PC"
        result = RandomBGM.randomizeBGM(options, platform)
        assert type(result) == list
        assert self.check_songs_are_from(result, games=["KH1"])


    def test_bgm_bbs(self):
        options = {
            "games": ["BBS"],
            "options": []
        }
        platform = "PC"
        result = RandomBGM.randomizeBGM(options, platform)
        assert type(result) == list
        assert self.check_songs_are_from(result, games=["BBS"])


    def test_bgm_recom(self):
        options = {
            "games": ["RECOM"],
            "options": []
        }
        platform = "PC"
        result = RandomBGM.randomizeBGM(options, platform)
        assert type(result) == list
        assert self.check_songs_are_from(result, games=["RECOM"])

    def test_bgm_some(self):
        options = {
            "games": ["KH2", "KH1"],
            "options": []
        }
        platform = "PC"
        result = RandomBGM.randomizeBGM(options, platform)
        assert type(result) == list
        assert self.check_songs_are_from(result, games=["KH2", "KH1"])

    def test_bgm_all(self):
        options = {
            "games": ["KH2", "KH1", "RECOM", "BBS"],
            "options": []
        }
        platform = "PC"
        result = RandomBGM.randomizeBGM(options, platform)
        assert type(result) == list
        assert self.check_songs_are_from(result, games=["KH1", "KH2", "RECOM", "BBS"])

    def test_bgm_field_battle(self):
        options = {
            "games": ["KH2", "BBS"],
            "options": ["Randomize Field and Battle Music Separately"]
        }
        platform = "PC"
        result = RandomBGM.randomizeBGM(options, platform)
        assert type(result) == list
        assert self.check_songs_are_from(result, games=["KH2", "BBS"], field_battle_unknown=True)

    def test_bgm_field_battle_with_custom(self):
        options = {
            "games": ["KH2", "CUSTOM 10"],
            "options": ["Randomize Field and Battle Music Separately"]
        }
        platform = "PC"
        result = RandomBGM.randomizeBGM(options, platform)
        assert type(result) == list
        assert self.check_songs_are_from(result, games=["KH2"], field_battle_unknown=True, custom=10)

    def test_bgm_no_dmca(self):
        for i in range(100):
            options = {
                "games": ["KH2"],
                "options": ["DMCA-SAFE"]
            }
            platform = "PC"
            result = RandomBGM.randomizeBGM(options, platform)
            assert type(result) == list
            assert self.check_songs_are_from(result, games=["KH2"], dmca_safe=True)

    def test_bgm_custom_3(self):
        options = {
            "games": ["CUSTOM 3"],
            "options": []
        }
        platform = "PC"
        result = RandomBGM.randomizeBGM(options, platform)
        assert type(result) == list
        assert self.check_songs_are_from(result, custom=3)

    def test_bgm_custom_5_10(self):
        options = {
            "games": ["CUSTOM 5", "CUSTOM 10"],
            "options": []
        }
        platform = "PC"
        result = RandomBGM.randomizeBGM(options, platform)
        assert type(result) == list
        assert self.check_songs_are_from(result, custom=10)

    @staticmethod
    def check_songs_are_from(assets, games=[], custom=0, field_battle_unknown=False, dmca_safe=False):
        valid_songs = {}
        for game in games:
            if game.startswith("CUSTOM"):
                continue
            for song in musicList[game]:
                valid_songs[musicPaths[game]+"\\"+song["name"]] = song
        for i in range(custom):
            name = musicPaths["CUSTOM"]+"\\"+"custom_{}.scd".format(i)
            valid_songs[name] = {"name": name, "kind": "unknown"}
        for asset in assets:
            newpath = asset["source"][0]["name"]
            originalname = asset["name"].split("\\")[-1]
            assert newpath in valid_songs
            newsong = valid_songs[newpath]
            originalsong = [s for s in musicList["KH2"] if s["name"] == originalname][0]
            if field_battle_unknown and newsong["kind"] != "unknown" and originalsong["kind"] != "unknown":
                assert originalsong["kind"] == newsong["kind"]
            if dmca_safe:
                assert not newsong.get("dmca")
        return True

# Uncomment to debug a single test through ipython
ut = Tests()
#ut.test_bgm_custom_5_10()

# Uncomment to run the actual tests
unittest.main()

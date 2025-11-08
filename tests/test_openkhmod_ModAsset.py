import unittest
from pathlib import Path

from Class.openkhmod import ModAsset, ModYmlSyntaxException, AssetMethod, BinarcMethod, AssetPlatform, \
    ModBinarcSource, ModSourceFile


class Tests(unittest.TestCase):

    def test_game_file_missing_name(self):
        data = {}
        asset = ModAsset(data)
        with self.assertRaises(ModYmlSyntaxException):
            asset.primary_game_file()

    def test_game_file_absolute_path_as_name(self):
        bad_path = Path("-0.dds").absolute()
        data = {"name": str(bad_path)}
        asset = ModAsset(data)
        with self.assertRaises(ModYmlSyntaxException):
            asset.primary_game_file()

    def test_game_file_relative_path_as_name(self):
        data = {"name": "foo/bar/0.dds"}
        asset = ModAsset(data)
        game_file = asset.primary_game_file()
        self.assertEqual(Path("foo", "bar", "0.dds"), game_file)

    def test_game_files_missing_name(self):
        data = {}
        asset = ModAsset(data)
        with self.assertRaises(ModYmlSyntaxException):
            asset.game_files()

    def test_game_files_absolute_path_as_name(self):
        bad_path = Path("-0.dds").absolute()
        data = {"name": str(bad_path)}
        asset = ModAsset(data)
        with self.assertRaises(ModYmlSyntaxException):
            asset.game_files()

    def test_game_files_single(self):
        data = {"name": "foo/bar/0.dds"}
        asset = ModAsset(data)
        game_files = asset.game_files()
        self.assertEqual([Path("foo", "bar", "0.dds")], game_files)

    def test_game_files_multiple(self):
        data = {
            "name": "foo/bar/0.dds",
            "multi": [
                {"name": "0.dds"},
                {"name": "baz/1.dds"},
            ]
        }
        asset = ModAsset(data)
        game_files = asset.game_files()
        expected = [
            Path("foo", "bar", "0.dds"),
            Path("0.dds"),
            Path("baz", "1.dds"),
        ]
        self.assertEqual(expected, game_files)

    def test_method_missing(self):
        data = {"name": "foo/bar/0.dds"}
        asset = ModAsset(data)
        with self.assertRaises(ModYmlSyntaxException):
            asset.method()

    def test_method_copy(self):
        data = {"method": "copy"}
        asset = ModAsset(data)
        self.assertEqual(AssetMethod.COPY, asset.method())

    def test_method_binarc(self):
        data = {"method": "binarc"}
        asset = ModAsset(data)
        self.assertEqual(AssetMethod.BINARC, asset.method())

    def test_source_missing(self):
        data = {"name": "foo/bar/0.dds"}
        asset = ModAsset(data)
        with self.assertRaises(ModYmlSyntaxException):
            asset.sources()

    def test_source_single(self):
        data = {
            "name": "foo/bar/0.dds",
            "source": [
                {"foo": "bar"},
            ],
        }
        asset = ModAsset(data)
        self.assertEqual([{"foo": "bar"}], asset.sources())

    def test_source_multiple(self):
        data = {
            "name": "foo/bar/0.dds",
            "source": [
                {"foo": "sora"},
                {"bar": "roxas"},
            ],
        }
        asset = ModAsset(data)
        self.assertEqual([{"foo": "sora"}, {"bar": "roxas"}], asset.sources())

    def test_make_copy_asset_no_game_files(self):
        with self.assertRaises(ValueError):
            ModAsset.make_copy_asset(game_files=[], source_file="source.dds")

    def test_make_binarc_asset_no_game_files(self):
        source = ModBinarcSource.make_source(
            name="wave",
            type_="wd",
            method=BinarcMethod.COPY,
            sources=[ModSourceFile.make_source_file("source.wd")],
        )
        with self.assertRaises(ValueError):
            ModAsset.make_binarc_asset(game_files=[], sources=[source])

    def test_make_copy_asset_absolute_game_file(self):
        bad_file = Path("foo/-1.dds").absolute()
        with self.assertRaises(ValueError):
            ModAsset.make_copy_asset(game_files=[bad_file], source_file="source.dds")

    def test_make_binarc_asset_absolute_game_file(self):
        bad_file = Path("foo/bar.a.us").absolute()
        source = ModBinarcSource.make_source(
            name="wave",
            type_="wd",
            method=BinarcMethod.COPY,
            sources=[ModSourceFile.make_source_file(bad_file)],
        )
        with self.assertRaises(ValueError):
            ModAsset.make_binarc_asset(game_files=[bad_file], sources=[source])

    def test_make_copy_asset_pc_platform_applied(self):
        asset = ModAsset.make_copy_asset(
            game_files=["foo/-1.dds"],
            source_file="source.dds",
            platform=AssetPlatform.PC,
        )
        expected = {
            "name": "foo/-1.dds",
            "platform": "pc",
            "method": "copy",
            "source": [{"name": "source.dds"}],
        }
        self.assertEqual(expected, asset.data)

    def test_make_binarc_asset_pc_platform_applied(self):
        source = ModBinarcSource.make_source(
            name="wave",
            type_="wd",
            method=BinarcMethod.COPY,
            sources=[ModSourceFile.make_source_file("source.wd")],
        )
        asset = ModAsset.make_binarc_asset(
            game_files=["foo/bar.a.us"],
            sources=[source],
            platform=AssetPlatform.PC,
        )
        expected = {
            "name": "foo/bar.a.us",
            "platform": "pc",
            "method": "binarc",
            "source": [{
                "name": "wave",
                "type": "wd",
                "method": "copy",
                "source": [{"name": "source.wd"}]
            }],
        }
        self.assertEqual(expected, asset.data)

    def test_make_copy_asset_ps2_platform_applied(self):
        asset = ModAsset.make_copy_asset(
            game_files=["foo/-1.dds"],
            source_file="source.dds",
            platform=AssetPlatform.PS2,
        )
        expected = {
            "name": "foo/-1.dds",
            "platform": "ps2",
            "method": "copy",
            "source": [{"name": "source.dds"}],
        }
        self.assertEqual(expected, asset.data)

    def test_make_binarc_asset_ps2_platform_applied(self):
        source = ModBinarcSource.make_source(
            name="wave",
            type_="wd",
            method=BinarcMethod.COPY,
            sources=[ModSourceFile.make_source_file("source.wd")],
        )
        asset = ModAsset.make_binarc_asset(
            game_files=["foo/bar.a.us"],
            sources=[source],
            platform=AssetPlatform.PS2,
        )
        expected = {
            "name": "foo/bar.a.us",
            "platform": "ps2",
            "method": "binarc",
            "source": [{
                "name": "wave",
                "type": "wd",
                "method": "copy",
                "source": [{"name": "source.wd"}]
            }],
        }
        self.assertEqual(expected, asset.data)

    def test_make_copy_asset_internal(self):
        asset = ModAsset.make_copy_asset(
            game_files=["foo/-1.dds"],
            source_file="source.dds",
            internal=True,
        )
        expected = {
            "name": "foo/-1.dds",
            "method": "copy",
            "source": [{"name": "source.dds", "type": "internal"}],
        }
        self.assertEqual(expected, asset.data)

    def test_make_copy_asset_single_game_file_string(self):
        asset = ModAsset.make_copy_asset(
            game_files=["foo/-1.dds"],
            source_file="source.dds",
        )
        expected = {
            "name": "foo/-1.dds",
            "method": "copy",
            "source": [{"name": "source.dds"}],
        }
        self.assertEqual(expected, asset.data)

    def test_make_binarc_asset_single_game_file_string(self):
        source = ModBinarcSource.make_source(
            name="wave",
            type_="wd",
            method=BinarcMethod.COPY,
            sources=[ModSourceFile.make_source_file("source.wd")],
        )
        asset = ModAsset.make_binarc_asset(
            game_files=["foo/bar.a.us"],
            sources=[source],
        )
        expected = {
            "name": "foo/bar.a.us",
            "method": "binarc",
            "source": [{
                "name": "wave",
                "type": "wd",
                "method": "copy",
                "source": [{"name": "source.wd"}]
            }],
        }
        self.assertEqual(expected, asset.data)

    def test_make_binarc_asset_single_game_file_string_internal(self):
        source = ModBinarcSource.make_source(
            name="wave",
            type_="wd",
            method=BinarcMethod.COPY,
            sources=[ModSourceFile.make_source_file("source.wd", internal=True)],
        )
        asset = ModAsset.make_binarc_asset(
            game_files=["foo/bar.a.us"],
            sources=[source],
        )
        expected = {
            "name": "foo/bar.a.us",
            "method": "binarc",
            "source": [{
                "name": "wave",
                "type": "wd",
                "method": "copy",
                "source": [{"name": "source.wd", "type": "internal"}]
            }],
        }
        self.assertEqual(expected, asset.data)

    def test_make_copy_asset_multi_game_file_string(self):
        asset = ModAsset.make_copy_asset(
            game_files=["foo/-1.dds", "bar/-1.dds", "baz/-1.dds"],
            source_file="source.dds",
        )
        expected = {
            "name": "foo/-1.dds",
            "multi": [
                {"name": "bar/-1.dds"},
                {"name": "baz/-1.dds"},
            ],
            "method": "copy",
            "source": [{"name": "source.dds"}],
        }
        self.assertEqual(expected, asset.data)

    def test_make_binarc_asset_multi_game_file_string(self):
        source = ModBinarcSource.make_source(
            name="wave",
            type_="wd",
            method=BinarcMethod.COPY,
            sources=[ModSourceFile.make_source_file("source.wd")],
        )
        asset = ModAsset.make_binarc_asset(
            game_files=["foo/bar.a.us", "foo/baz.a.us", "bar/baz.a.us"],
            sources=[source],
        )
        expected = {
            "name": "foo/bar.a.us",
            "multi": [
                {"name": "foo/baz.a.us"},
                {"name": "bar/baz.a.us"},
            ],
            "method": "binarc",
            "source": [{
                "name": "wave",
                "type": "wd",
                "method": "copy",
                "source": [{"name": "source.wd"}]
            }],
        }
        self.assertEqual(expected, asset.data)

    def test_make_copy_asset_single_game_file_path(self):
        asset = ModAsset.make_copy_asset(
            game_files=[Path("foo", "-1.dds")],
            source_file="source.dds",
        )
        expected = {
            "name": "foo/-1.dds",
            "method": "copy",
            "source": [{"name": "source.dds"}],
        }
        self.assertEqual(expected, asset.data)

    def test_make_binarc_asset_single_game_file_path(self):
        source = ModBinarcSource.make_source(
            name="wave",
            type_="wd",
            method=BinarcMethod.COPY,
            sources=[ModSourceFile.make_source_file("source.wd")],
        )
        asset = ModAsset.make_binarc_asset(
            game_files=[Path("foo", "bar.a.us")],
            sources=[source],
        )
        expected = {
            "name": "foo/bar.a.us",
            "method": "binarc",
            "source": [{
                "name": "wave",
                "type": "wd",
                "method": "copy",
                "source": [{"name": "source.wd"}]
            }],
        }
        self.assertEqual(expected, asset.data)

    def test_make_copy_asset_multi_game_file_path(self):
        asset = ModAsset.make_copy_asset(
            game_files=[Path("foo", "-1.dds"), Path("bar", "-1.dds"), Path("baz", "-1.dds")],
            source_file="source.dds"
        )
        expected = {
            "name": "foo/-1.dds",
            "multi": [
                {"name": "bar/-1.dds"},
                {"name": "baz/-1.dds"},
            ],
            "method": "copy",
            "source": [{"name": "source.dds"}],
        }
        self.assertEqual(expected, asset.data)

    def test_make_binarc_asset_multi_game_file_path(self):
        source = ModBinarcSource.make_source(
            name="wave",
            type_="wd",
            method=BinarcMethod.COPY,
            sources=[ModSourceFile.make_source_file("source.wd")],
        )
        asset = ModAsset.make_binarc_asset(
            game_files=[Path("foo", "bar.a.us"), Path("foo", "baz.a.us"), Path("bar", "baz.a.us")],
            sources=[source],
        )
        expected = {
            "name": "foo/bar.a.us",
            "multi": [
                {"name": "foo/baz.a.us"},
                {"name": "bar/baz.a.us"},
            ],
            "method": "binarc",
            "source": [{
                "name": "wave",
                "type": "wd",
                "method": "copy",
                "source": [{"name": "source.wd"}]
            }],
        }
        self.assertEqual(expected, asset.data)

    def test_make_copy_asset_path_source(self):
        source_path = Path("bar", "source.dds")
        asset = ModAsset.make_copy_asset(
            game_files=["foo/-1.dds"],
            source_file=source_path,
        )
        expected = {
            "name": "foo/-1.dds",
            "method": "copy",
            "source": [{"name": "bar/source.dds"}],
        }
        self.assertEqual(expected, asset.data)

    def test_make_binarc_asset_path_source(self):
        source_path = Path("mod", "source.wd")
        source = ModBinarcSource.make_source(
            name="wave",
            type_="wd",
            method=BinarcMethod.COPY,
            sources=[ModSourceFile.make_source_file(source_path)],
        )
        asset = ModAsset.make_binarc_asset(
            game_files=["foo/bar.a.us"],
            sources=[source],
        )
        expected = {
            "name": "foo/bar.a.us",
            "method": "binarc",
            "source": [{
                "name": "wave",
                "type": "wd",
                "method": "copy",
                "source": [{"name": "mod/source.wd"}]
            }],
        }
        self.assertEqual(expected, asset.data)

    def test_make_binarc_asset_absolute_source(self):
        source_path = Path("mod", "source.wd").absolute()
        source = ModBinarcSource.make_source(
            name="wave",
            type_="wd",
            method=BinarcMethod.COPY,
            sources=[ModSourceFile.make_source_file(source_path)],
        )
        asset = ModAsset.make_binarc_asset(
            game_files=["foo/bar.a.us"],
            sources=[source],
        )
        expected = {
            "name": "foo/bar.a.us",
            "method": "binarc",
            "source": [{
                "name": "wave",
                "type": "wd",
                "method": "copy",
                # Can't expect a specific string here because absolute path formatting is file-system dependent
                "source": [{"name": str(source_path)}]
            }],
        }
        self.assertEqual(expected, asset.data)

    def test_make_binarc_asset_raw_source(self):
        source = ModBinarcSource.make_source(
            name="wave",
            type_="wd",
            method=BinarcMethod.COPY,
            sources=[ModSourceFile({"name": r"source\path\a.us"})],
        )
        asset = ModAsset.make_binarc_asset(
            game_files=["foo/bar.a.us"],
            sources=[source],
        )
        expected = {
            "name": "foo/bar.a.us",
            "method": "binarc",
            "source": [{
                "name": "wave",
                "type": "wd",
                "method": "copy",
                "source": [{"name": "source/path/a.us"}]
            }],
        }
        self.assertEqual(expected, asset.data)

    def test_make_binarc_asset_complex(self):
        trsr = ModBinarcSource.make_source(
            name="trsr",
            type_="List",
            method=BinarcMethod.LISTPATCH,
            sources=[ModSourceFile.make_source_file("randoseed-mod-files/TrsrList.yml", type="trsr")],
        )
        item = ModBinarcSource.make_source(
            name="item",
            type_="List",
            method=BinarcMethod.LISTPATCH,
            sources=[ModSourceFile.make_source_file("randoseed-mod-files/ItemList.yml", type="item")],
        )
        shop = ModBinarcSource.make_source(
            name="shop",
            type_="unknown41",
            method=BinarcMethod.COPY,
            sources=[ModSourceFile.make_source_file("randoseed-mod-files/modified_shop.bin")],
        )
        cmd = ModBinarcSource.make_source(
            name="cmd",
            type_="list",
            method=BinarcMethod.LISTPATCH,
            sources=[ModSourceFile.make_source_file("randoseed-mod-files/cmd_list_merged.yml", type="cmd")],
        )
        titl = ModBinarcSource.make_source(
            name="titl",
            type_="imgz",
            method=BinarcMethod.IMGZ,
            sources=[ModSourceFile.make_source_file("title/title1.png", highdef="title/title1_hd.png", index=1)]
        )
        asset = ModAsset.make_binarc_asset(
            game_files=["03system.bin"],
            sources=[trsr, item, shop, cmd, titl],
        )
        expected = {
            "name": "03system.bin",
            "method": "binarc",
            "source": [
                {
                    "name": "trsr",
                    "method": "listpatch",
                    "type": "List",
                    "source": [{"name": "randoseed-mod-files/TrsrList.yml", "type": "trsr"}]
                },
                {
                    "name": "item",
                    "method": "listpatch",
                    "type": "List",
                    "source": [{"name": "randoseed-mod-files/ItemList.yml", "type": "item"}]
                },
                {
                    "name": "shop",
                    "method": "copy",
                    "type": "unknown41",
                    "source": [{"name": "randoseed-mod-files/modified_shop.bin"}]
                },
                {
                    "name": "cmd",
                    "method": "listpatch",
                    "type": "list",
                    "source": [{"name": "randoseed-mod-files/cmd_list_merged.yml", "type": "cmd"}]
                },
                {
                    "name": "titl",
                    "type": "imgz",
                    "method": "imgz",
                    "source": [{"name": "title/title1.png", "highdef": "title/title1_hd.png", "index": 1}]
                }
            ],
        }
        self.assertEqual(expected, asset.data)

    def test_make_bdscript_asset(self):
        asset = ModAsset.make_asset(
            game_files=["00common.bdx"],
            method=AssetMethod.BDSCRIPT,
            sources=[ModSourceFile.make_source_file("00common.bdscript")],
        )
        expected = {
            "name": "00common.bdx",
            "method": "bdscript",
            "source": [{"name": "00common.bdscript"}],
        }
        self.assertEqual(expected, asset.data)

    def test_make_listpatch_asset(self):
        asset = ModAsset.make_asset(
            game_files=["00objentry.bin"],
            method=AssetMethod.LISTPATCH,
            type_="List",
            sources=[ModSourceFile.make_source_file("ObjList.yml", type="objentry")],
        )
        expected = {
            "name": "00objentry.bin",
            "method": "listpatch",
            "type": "List",
            "source": [{"name": "ObjList.yml", "type": "objentry"}],
        }
        self.assertEqual(expected, asset.data)


if __name__ == '__main__':
    unittest.main()

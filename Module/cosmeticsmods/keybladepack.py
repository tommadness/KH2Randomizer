import io
import os
import shutil
import zipfile
from pathlib import Path

import requests

from Class.exceptions import GeneratorException
from Module import appconfig
from Module.cosmeticsmods.keyblade import KeybladeRandomizer


class Kh1Keyblade:

    def __init__(
            self,
            name: str,
            itempic_name: str,
            model_name: str,
            texture_count: int,
            pax_name: str,
            sound_name: str,
    ):
        super().__init__()
        self.name = name
        self.itempic_name = itempic_name
        self.model_name = model_name
        self.texture_count = texture_count
        self.pax_name = pax_name
        self.sound_name = sound_name


class Kh1KeybladePack:

    @staticmethod
    def _keyblade_list() -> list[Kh1Keyblade]:
        return [
            Kh1Keyblade(
                name="Crabclaw",
                itempic_name="item-060.imd",
                model_name="Crabclaw.model",
                texture_count=2,
                pax_name="crabclaw.pax",
                sound_name="se521",
            ),
            Kh1Keyblade(
                name="Diamond Dust",
                itempic_name="item-047.imd",
                model_name="DiamondDust.model",
                texture_count=2,
                pax_name="diamond_dust.pax",
                sound_name="se508",
            ),
            Kh1Keyblade(
                name="Divine Rose",
                itempic_name="item-054.imd",
                model_name="DivineRose.model",
                texture_count=2,
                pax_name="divine_rose.pax",
                sound_name="se515",
            ),
            Kh1Keyblade(
                name="Fairy Harp",
                itempic_name="item-053.imd",
                model_name="FairyHarp.model",
                texture_count=2,
                pax_name="fairy_harp.pax",
                sound_name="se514",
            ),
            Kh1Keyblade(
                name="Jungle King",
                itempic_name="item-051.imd",
                model_name="JungleKing.model",
                texture_count=2,
                pax_name="jungle_king.pax",
                sound_name="se512",
            ),
            Kh1Keyblade(
                name="Lady Luck",
                itempic_name="item-050.imd",
                model_name="LadyLuck.model",
                texture_count=2,
                pax_name="lady_luck.pax",
                sound_name="se511",
            ),
            Kh1Keyblade(
                name="Lionheart",
                itempic_name="item-058.imd",
                model_name="Lionheart.model",
                texture_count=2,
                pax_name="lionheart.pax",
                sound_name="se519",
            ),
            Kh1Keyblade(
                name="Metal Chocobo",
                itempic_name="item-055.imd",
                model_name="MetalChocobo.model",
                texture_count=2,
                pax_name="metal_chocobo.pax",
                sound_name="se516",
            ),
            Kh1Keyblade(
                name="Olympia",
                itempic_name="item-048.imd",
                model_name="Olympia.model",
                texture_count=2,
                pax_name="olympia.pax",
                sound_name="se509",
            ),
            Kh1Keyblade(
                name="Pumpkinhead",
                itempic_name="item-057.imd",
                model_name="Pumpkinhead.model",
                texture_count=2,
                pax_name="pumpkinhead.pax",
                sound_name="se518",
            ),
            Kh1Keyblade(
                name="Spellbinder",
                itempic_name="item-052.imd",
                model_name="Spellbinder.model",
                texture_count=2,
                pax_name="spellbinder.pax",
                sound_name="se513",
            ),
            Kh1Keyblade(
                name="Three Wishes",
                itempic_name="item-056.imd",
                model_name="ThreeWishes.model",
                texture_count=2,
                pax_name="three_wishes.pax",
                sound_name="se517",
            ),
            Kh1Keyblade(
                name="Wishing Star",
                itempic_name="item-059.imd",
                model_name="WishingStar.model",
                texture_count=2,
                pax_name="wishing_star.pax",
                sound_name="se520",
            ),
            Kh1Keyblade(
                name="One-Winged Angel",
                itempic_name="item-063.imd",
                model_name="OneWingedAngel.model",
                texture_count=1,
                pax_name="onewingedangel.pax",
                sound_name="se524",
            ),
        ]

    @staticmethod
    def download_keyblade_pack(destination: Path):
        # Using a well-known commit in case the repository structure changes
        url = "https://github.com/Zurphing/KH1_Keyblades/archive/626145770bbe704ddb5c3f28228c11a7f21f4f62.zip"
        response = requests.get(url)
        response.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            zip_file.extractall(destination)

    @staticmethod
    def import_keyblades(pack_path: Path) -> Path:
        if not pack_path.is_dir():
            raise GeneratorException("Could not locate the Kingdom Hearts keyblade files. Can't import keyblades.")

        custom_visuals_path = appconfig.read_custom_visuals_path()
        if custom_visuals_path is None:
            raise GeneratorException("No custom visuals path configured. Can't import keyblades.")

        keyblades_path = custom_visuals_path / "keyblades"
        keyblades_path.mkdir(exist_ok=True)

        for keyblade in Kh1KeybladePack._keyblade_list():
            Kh1KeybladePack._import_keyblade(
                pack_path=pack_path,
                keyblade=keyblade,
                output_path=keyblades_path,
            )

        return keyblades_path

    @staticmethod
    def _import_keyblade(pack_path: Path, keyblade: Kh1Keyblade, output_path: Path):
        keyblade_name = keyblade.name

        keyblade_output_location = output_path / f"{keyblade_name} (KH1)"
        keyblade_output_location.mkdir(parents=True, exist_ok=True)

        base_variant_path = keyblade_output_location / "base"
        nm_path = keyblade_output_location / "nm"
        tr_path = keyblade_output_location / "tr"
        wi_path = keyblade_output_location / "wi"

        # Base model / texture / effects
        base_variant_path.mkdir(parents=True, exist_ok=True)
        shutil.copy2(pack_path / "Models" / keyblade.model_name, base_variant_path)
        if keyblade.texture_count == 2:
            shutil.copy2(pack_path / "Models" / "TwoTextures.tim", base_variant_path)
        else:
            shutil.copy2(pack_path / "Models" / "OneTexture.tim", base_variant_path)
        shutil.copy2(pack_path / "Effects" / keyblade_name / keyblade.pax_name, base_variant_path)
        shutil.copy2(pack_path / "Effects" / "dummy_wave.wd", base_variant_path)

        # Remastered textures
        source_remastered_textures_path = pack_path / "Textures" / keyblade_name
        def copy_remastered_texture(source_file: str, variant_path: Path, destination_file: str):
            destination_path = variant_path / "remastered-textures"
            destination_path.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_remastered_textures_path / source_file, destination_path / destination_file)
        copy_remastered_texture(source_file="DF.dds", variant_path=base_variant_path, destination_file="-0.dds")
        copy_remastered_texture(source_file="NM.dds", variant_path=nm_path, destination_file="-0.dds")
        copy_remastered_texture(source_file="TR.dds", variant_path=tr_path, destination_file="-0.dds")
        copy_remastered_texture(source_file="WI.dds", variant_path=wi_path, destination_file="-0.dds")
        if keyblade.texture_count == 2:
            copy_remastered_texture(source_file="DF1.dds", variant_path=base_variant_path, destination_file="-1.dds")
            copy_remastered_texture(source_file="NM1.dds", variant_path=nm_path, destination_file="-1.dds")
            copy_remastered_texture(source_file="TR1.dds", variant_path=tr_path, destination_file="-1.dds")
            copy_remastered_texture(source_file="WI1.dds", variant_path=wi_path, destination_file="-1.dds")

        # Remastered effects
        source_remastered_effects_path = pack_path / "Effects" / keyblade_name / "remastered"
        def copy_remastered_effects(effects_output: Path):
            effects_output.mkdir(parents=True, exist_ok=True)
            for input_file in os.listdir(source_remastered_effects_path):
                _, extension = os.path.splitext(input_file)
                if extension == ".dds":
                    shutil.copy2(source_remastered_effects_path / input_file, effects_output)
        copy_remastered_effects(effects_output=base_variant_path / "remastered-effects")

        # Remastered sound
        def copy_remastered_sound(sound_name: str, sound_output: Path):
            sound_input = source_remastered_effects_path / "se" / "obj" / sound_name
            copy_result = shutil.copy2(sound_input, sound_output)
            copy_result_path = Path(copy_result).absolute()
            renamed_path = copy_result_path.parent / f"{copy_result_path.name}.scd"
            if renamed_path.is_file():
                renamed_path.unlink()
            copy_result_path.rename(renamed_path)
        copy_remastered_sound(sound_name=keyblade.sound_name, sound_output=base_variant_path)

        out_itempic_path = keyblade_output_location / "itempic"
        out_itempic_path.mkdir(exist_ok=True)
        shutil.copy2(pack_path / "itempic" / keyblade.itempic_name, out_itempic_path)
        shutil.copy2(pack_path / "remastered" / "itempic" / keyblade.itempic_name / "-0.dds", out_itempic_path)

        KeybladeRandomizer.write_keyblade_json(
            keyblade_name=f"{keyblade_name} (KH1)",
            author="Zurphing",
            source="https://github.com/Zurphing/KH1_Keyblades",
            keyblade_output_location=keyblade_output_location,
        )


class BirthBySleepKeyblade:

    def __init__(
            self,
            name: str,
            game_id: str,
            itempic_folder_name: str,
            sound_name: str,
    ):
        super().__init__()
        self.name = name
        self.game_id = game_id
        self.itempic_folder_name = itempic_folder_name
        self.sound_name = sound_name


class BirthBySleepKeybladePack:

    @staticmethod
    def _keyblade_list() -> list[BirthBySleepKeyblade]:
        return [
            BirthBySleepKeyblade(
                name="Wayward Wind",
                game_id="W_EX010",
                itempic_folder_name="item-043.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Hyperdrive",
                game_id="W_EX010_10",
                itempic_folder_name="item-044.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Lost Memory",
                game_id="W_EX010_20",
                itempic_folder_name="item-045.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Destiny's Embrace",
                game_id="W_EX010_30",
                itempic_folder_name="item-046.imd",
                sound_name="se514",
            ),
            BirthBySleepKeyblade(
                name="Treasure Trove",
                game_id="W_EX010_40",
                itempic_folder_name="item-047.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Mark of a Hero",
                game_id="W_EX010_50",
                itempic_folder_name="item-048.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Stroke of Midnight",
                game_id="W_EX010_60",
                itempic_folder_name="item-049.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Fairy Stars",
                game_id="W_EX010_70",
                itempic_folder_name="item-050.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Sweetstack",
                game_id="W_EX010_80",
                itempic_folder_name="item-051.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Pixie Petal",
                game_id="W_EX010_90",
                itempic_folder_name="item-052.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Victory Line",
                game_id="W_EX010_A0",
                itempic_folder_name="item-053.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Earthshaker",
                game_id="W_EX010_B0",
                itempic_folder_name="item-054.imd",
                sound_name="se",
            ),
            BirthBySleepKeyblade(
                name="Chaos Ripper",
                game_id="W_EX010_C0",
                itempic_folder_name="item-055.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Stormfell",
                game_id="W_EX010_D0",
                itempic_folder_name="item-056.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Crown Unlimit",
                game_id="W_EX010_E0",
                itempic_folder_name="item-057.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Ends of the Earth",
                game_id="W_EX010_F0",
                itempic_folder_name="item-058.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Rainfell",
                game_id="W_EX010_G0",
                itempic_folder_name="item-059.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Brightcrest",
                game_id="W_EX010_H0",
                itempic_folder_name="item-060.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Darkgnaw",
                game_id="W_EX010_J0",
                itempic_folder_name="item-061.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Frolic Flame",
                game_id="W_EX010_K0",
                itempic_folder_name="item-062.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Void Gear",
                game_id="W_EX010_M0",
                itempic_folder_name="item-063.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Ultima Weapon",
                game_id="W_EX010_N0",
                itempic_folder_name="item-064.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="Master's Defender",
                game_id="W_EX010_P0",
                itempic_folder_name="item-300.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="No Name",
                game_id="W_EX010_R0",
                itempic_folder_name="item-301.imd",
                sound_name="se509",
            ),
            BirthBySleepKeyblade(
                name="X-Blade",
                game_id="W_EX010_S0",
                itempic_folder_name="X-Blade",
                sound_name="se509",
            ),
        ]

    @staticmethod
    def download_keyblade_pack(destination: Path):
        # Using a well-known commit in case the repository structure changes
        url = "https://github.com/Kite2810/Birth-by-Sleep-Keybladepack/archive/97d6ac2e6789cd0abd0ae16046b199fa1b6ad37b.zip"
        response = requests.get(url)
        response.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            zip_file.extractall(destination)

    @staticmethod
    def import_keyblades(pack_path: Path) -> Path:
        if not pack_path.is_dir():
            raise GeneratorException("Could not locate the Birth by Sleep keyblade files. Can't import keyblades.")

        custom_visuals_path = appconfig.read_custom_visuals_path()
        if custom_visuals_path is None:
            raise GeneratorException("No custom visuals path configured. Can't import keyblades.")

        keyblades_path = custom_visuals_path / "keyblades"
        keyblades_path.mkdir(exist_ok=True)

        base_obj_path = pack_path / "obj"
        remastered_itempic_path = pack_path / "remastered" / "itempic"
        remastered_obj_path = pack_path / "remastered" / "obj"

        for keyblade in BirthBySleepKeybladePack._keyblade_list():
            keyblade_itempic_path = remastered_itempic_path / keyblade.itempic_folder_name
            keyblade_game_id = keyblade.game_id
            sound_name = keyblade.sound_name

            KeybladeRandomizer.extract_keyblade(
                keyblade_name=f"{keyblade.name} (BBS)",
                author="Kite2810",
                source="https://github.com/Kite2810/Birth-by-Sleep-Keybladepack",
                output_path=keyblades_path,
                original_itempic=Path(""),
                remastered_itempic=keyblade_itempic_path / "-0.dds",
                mdlx_files=[
                    base_obj_path / f"{keyblade_game_id}.mdlx",
                    base_obj_path / f"{keyblade_game_id}_NM.mdlx",
                    base_obj_path / f"{keyblade_game_id}_TR.mdlx",
                    base_obj_path / f"{keyblade_game_id}_WI.mdlx",
                ],
                remastered_mdlx_folders=[
                    remastered_obj_path / f"{keyblade_game_id}.mdlx",
                    remastered_obj_path / f"{keyblade_game_id}_NM.mdlx",
                    remastered_obj_path / f"{keyblade_game_id}_TR.mdlx",
                    remastered_obj_path / f"{keyblade_game_id}_WI.mdlx",
                ],
                fx_files=[
                    base_obj_path / f"{keyblade_game_id}.a.us",
                    base_obj_path / f"{keyblade_game_id}_NM.a.us",
                    base_obj_path / f"{keyblade_game_id}_TR.a.us",
                    base_obj_path / f"{keyblade_game_id}_WI.a.us",
                ],
                remastered_fx_folders=[
                    remastered_obj_path / f"{keyblade_game_id}.a.us",
                    remastered_obj_path / f"{keyblade_game_id}_NM.a.us",
                    remastered_obj_path / f"{keyblade_game_id}_TR.a.us",
                    remastered_obj_path / f"{keyblade_game_id}_WI.a.us",
                ],
                remastered_sound_files=[
                    remastered_obj_path / f"{keyblade_game_id}.a.us" / "se" / "obj" / sound_name,
                    remastered_obj_path / f"{keyblade_game_id}_NM.a.us" / "se" / "obj" / sound_name,
                    remastered_obj_path / f"{keyblade_game_id}_TR.a.us" / "se" / "obj" / sound_name,
                    remastered_obj_path / f"{keyblade_game_id}_WI.a.us" / "se" / "obj" / sound_name,
                ]
            )

        return keyblades_path

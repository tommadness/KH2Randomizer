import json
import os
import random
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Any

from Class.exceptions import GeneratorException
from Class.openkhmod import Asset
from List import configDict
from Module import appconfig

_KEYBLADE_VERSION = 1


class VanillaKeyblade:

    def __init__(
            self,
            name: str,
            itempic_index: str,
            sound_name: str,
            model_name: str,
            custom: bool = False,
            can_replace_effects: bool = True
    ):
        super().__init__()
        self.name = name
        self.itempic_index = itempic_index
        self.sound_name = sound_name
        self.model_name = model_name
        self.custom = custom
        # Some of the custom keyblades share sound effect IDs with in-game keyblades. If we try to replace the
        # effects on these keyblades (even just the visual effects), the sound effects seem to get messed up. For now,
        # have a way to just skip effects for those (we can still replace the model and textures).
        # TODO: If someone more knowledgeable knows how to get around this, we can restore the ability to replace
        #  effects for the keyblades in question.
        self.can_replace_effects = can_replace_effects


def _safe_list(path: Path) -> list[str]:
    if path.is_dir():
        return os.listdir(path)
    else:
        return []


class ReplacementKeyblade:

    def __init__(self, name: str, path: Path, keyblade_json_path: Path):
        self.name = name
        self.path = path
        self.version = -1
        self.author: Optional[str] = None

        with open(keyblade_json_path, encoding="utf-8") as keyblade_json_file:
            keyblade_json: dict[str, Any] = json.load(keyblade_json_file)
            self.name = keyblade_json.get("name", self.name)
            self.version = keyblade_json.get("version", -1)
            self.author = keyblade_json.get("author", None)

    def model(self, model_type: str) -> Optional[Path]:
        full_path = self.path / model_type
        for file in _safe_list(full_path):
            name, extension = os.path.splitext(file)
            if extension == ".model":
                return full_path / file
        if model_type == "base":
            return None
        else:
            return self.model("base")

    def texture(self, model_type: str) -> Optional[Path]:
        full_path = self.path / model_type
        for file in _safe_list(full_path):
            name, extension = os.path.splitext(file)
            if extension == ".tim" or extension == ".texture":
                return full_path / file
        if model_type == "base":
            return None
        else:
            return self.texture("base")

    def pax(self, model_type: str) -> Optional[Path]:
        full_path = self.path / model_type
        for file in _safe_list(full_path):
            name, extension = os.path.splitext(file)
            if extension == ".pax":
                return full_path / file
        if model_type == "base":
            return None
        else:
            return self.pax("base")

    def remastered_textures(self, model_type: str) -> list[Path]:
        full_path = self.path / model_type / "remastered-textures"
        if not full_path.is_dir():
            if model_type == "base":
                return []
            else:
                return self.remastered_textures("base")

        textures: list[Path] = []
        for file in _safe_list(full_path):
            name, extension = os.path.splitext(file)
            if extension == ".dds":
                textures.append(full_path / file)

        if len(textures) == 0:
            if model_type == "base":
                return []
            else:
                return self.remastered_textures("base")

        return textures

    def remastered_effects(self, model_type: str) -> list[Path]:
        full_path = self.path / model_type / "remastered-effects"
        if not full_path.is_dir():
            if model_type == "base":
                return []
            else:
                return self.remastered_effects("base")

        textures: list[Path] = []
        for file in _safe_list(full_path):
            name, extension = os.path.splitext(file)
            if extension == ".dds":
                textures.append(full_path / file)

        if len(textures) == 0:
            if model_type == "base":
                return []
            else:
                return self.remastered_effects("base")

        return textures

    def remastered_sound(self, model_type: str) -> Optional[Path]:
        full_path = self.path / model_type
        for file in _safe_list(full_path):
            name, extension = os.path.splitext(file)
            if extension == ".scd":
                return full_path / file
        if model_type == "base":
            return None
        else:
            return self.remastered_sound("base")

    def original_itempic(self) -> Optional[Path]:
        full_path = self.path / "itempic"
        for file in _safe_list(full_path):
            name, extension = os.path.splitext(file)
            if extension == ".imd":
                return full_path / file
        return None

    def remastered_itempic(self) -> Optional[Path]:
        full_path = self.path / "itempic"
        for file in _safe_list(full_path):
            name, extension = os.path.splitext(file)
            if extension == ".dds":
                return full_path / file
        return None


def _vanilla_keyblades() -> list[VanillaKeyblade]:
    return [
        VanillaKeyblade("Kingdom Key", "043", "se500", "W_EX010"),
        VanillaKeyblade("Oathkeeper", "044", "se501", "W_EX010_10", can_replace_effects=False),
        VanillaKeyblade("Oblivion", "045", "se502", "W_EX010_20"),
        VanillaKeyblade("Star Seeker", "046", "se507", "W_EX010_30"),
        VanillaKeyblade("Hidden Dragon", "047", "se508", "W_EX010_40"),
        VanillaKeyblade("Heros Crest", "048", "se509", "W_EX010_50"),
        VanillaKeyblade("Monochrome", "049", "se510", "W_EX010_60"),
        VanillaKeyblade("Follow the Wind", "050", "se511", "W_EX010_70"),
        VanillaKeyblade("Circle of Life", "051", "se512", "W_EX010_80"),
        VanillaKeyblade("Photon Debugger", "052", "se513", "W_EX010_90"),
        VanillaKeyblade("Gull Wing", "053", "se514", "W_EX010_A0"),
        VanillaKeyblade("Rumbling Rose", "054", "se515", "W_EX010_B0"),
        VanillaKeyblade("Guardian Soul", "055", "se516", "W_EX010_C0"),
        VanillaKeyblade("Wishing Lamp", "056", "se517", "W_EX010_D0"),
        VanillaKeyblade("Decisive Pumpkin", "057", "se518", "W_EX010_E0"),
        VanillaKeyblade("Sleeping Lion", "058", "se519", "W_EX010_F0", can_replace_effects=False),
        VanillaKeyblade("Sweet Memories", "059", "se520", "W_EX010_G0"),
        VanillaKeyblade("Mysterious Abyss", "060", "se521", "W_EX010_H0"),
        VanillaKeyblade("Fatal Crest", "061", "se522", "W_EX010_J0"),
        VanillaKeyblade("Bond of Flame", "062", "se523", "W_EX010_K0"),
        VanillaKeyblade("Fenrir", "063", "se524", "W_EX010_M0"),
        VanillaKeyblade("Ultima Weapon", "064", "se525", "W_EX010_N0"),
        VanillaKeyblade("Two Become One", "300", "se526", "W_EX010_P0"),
        VanillaKeyblade("Struggle Hammer", "065", "se506", "W_EX010_U0"),
        VanillaKeyblade("Struggle Wand", "066", "se505", "W_EX010_V0"),
        VanillaKeyblade("Struggle Sword", "067", "se504", "W_EX010_W0"),
        VanillaKeyblade("Winners Proof", "301", "se527", "W_EX010_R0"),
        VanillaKeyblade("Pureblood", "296", "se503", "W_EX010_X0", custom=True),
        VanillaKeyblade("Alpha Weapon", "297", "se501", "W_EX010_Y0", custom=True, can_replace_effects=False),
        VanillaKeyblade("Omega Weapon", "298", "se519", "W_EX010_Z0", custom=True, can_replace_effects=False),
        VanillaKeyblade("Kingdom Key D", "299", "se9000", "W_EX010_00", custom=True),
    ]


def _model_type_suffix(model_type: str) -> str:
    if model_type == "base":
        return ""
    else:
        return "_" + model_type.upper()


class KeybladeRandomizer:

    @staticmethod
    def keyblade_rando_options() -> dict[str, str]:
        return {
            configDict.VANILLA: "Vanilla",
            configDict.RANDOMIZE_IN_GAME_ONLY: "Randomize (in-game only)",
            configDict.RANDOMIZE_CUSTOM_ONLY: "Randomize (custom only)",
            configDict.RANDOMIZE_ALL: "Randomize (in-game + custom)",
        }

    @staticmethod
    def extract_keyblade(
            keyblade_name: str,
            author: Optional[str],
            output_path: Path,
            original_itempic: Path,
            remastered_itempic: Path,
            mdlx_files: list[Path],
            remastered_mdlx_folders: list[Path],
            fx_files: list[Path],
            remastered_fx_folders: list[Path],
            remastered_sound_files: list[Path],
    ):
        """
        Extracts a keyblade to the randomizer-specific file/folder structure.

        The parameters that accept list[Path] assume the order [base, NM, TR, WI].
        """

        openkh_path = appconfig.read_openkh_path()
        if openkh_path is None:
            raise GeneratorException("No OpenKH path configured. Can't extract keyblades.")

        bar_exe = openkh_path / "OpenKh.Command.Bar.exe"
        if not bar_exe.is_file():
            raise GeneratorException("No OpenKh.Command.Bar.exe found. Can't extract keyblades.")

        def unpack_bar(bar_input: Path, bar_output: Path):
            bar_output.mkdir(parents=True, exist_ok=True)
            # -s to skip creating an extra file
            # -o specifies the output location
            subprocess.call([bar_exe, "unpack", "-s", "-o", bar_output, bar_input])

        def copy_remastered_textures(textures_input: Path, textures_output: Path):
            textures_output.mkdir(parents=True, exist_ok=True)
            for input_file in os.listdir(textures_input):
                _, extension = os.path.splitext(input_file)
                if extension == ".dds":
                    shutil.copy2(textures_input / input_file, textures_output)

        def copy_remastered_sound(sound_input: Path, sound_output: Path):
            sound_output.mkdir(parents=True, exist_ok=True)
            copy_result = shutil.copy2(sound_input, sound_output)
            copy_result_path = Path(copy_result).absolute()
            renamed_path = copy_result_path.parent / f"{copy_result_path.name}.scd"
            if renamed_path.is_file():
                renamed_path.unlink()
            copy_result_path.rename(renamed_path)

        keyblade_output_location = output_path / keyblade_name
        keyblade_output_location.mkdir(parents=True, exist_ok=True)

        for index, model_type in enumerate(["base", "nm", "tr", "wi"]):
            out_path = keyblade_output_location / model_type

            mdlx_file = mdlx_files[index]
            if mdlx_file.is_file():
                unpack_bar(mdlx_file, out_path)

            remastered_mdlx_folder = remastered_mdlx_folders[index]
            if remastered_mdlx_folder.is_dir():
                copy_remastered_textures(remastered_mdlx_folder, out_path / "remastered-textures")

            fx_file = fx_files[index]
            if fx_file.is_file():
                unpack_bar(fx_file, out_path)

            remastered_fx_folder = remastered_fx_folders[index]
            if remastered_fx_folder.is_dir():
                copy_remastered_textures(remastered_fx_folder, out_path / "remastered-effects")

            remastered_sound_file = remastered_sound_files[index]
            if remastered_sound_file.is_file():
                copy_remastered_sound(remastered_sound_file, out_path)

        out_itempic_path = keyblade_output_location / "itempic"
        out_itempic_path.mkdir(exist_ok=True)
        if original_itempic.is_file():
            shutil.copy2(original_itempic, out_itempic_path)
        if remastered_itempic.is_file():
            shutil.copy2(remastered_itempic, out_itempic_path)

        keyblade_json = {
            "version": _KEYBLADE_VERSION,
            "name": keyblade_name,
        }
        if author is not None and author != "":
            keyblade_json["author"] = author
        keyblade_json_path = keyblade_output_location / "keyblade.json"
        with open(keyblade_json_path, "w", encoding="utf-8") as keyblade_json_file:
            json.dump(keyblade_json, keyblade_json_file, indent=4)

    @staticmethod
    def extract_game_models() -> Path:
        extracted_data_path = appconfig.extracted_data_path() / "kh2"
        if extracted_data_path is None:
            raise GeneratorException("No extracted data path, can't extract keyblades")

        obj_path = extracted_data_path / "obj"
        remastered_obj_path = extracted_data_path / "remastered" / "obj"

        vanilla_keys_path = Path("cache/vanilla-keyblades")
        vanilla_keys_path.mkdir(exist_ok=True)

        for vanilla_key in _vanilla_keyblades():
            if vanilla_key.custom:
                continue

            keyblade_name = vanilla_key.name
            print(f"Extracting {keyblade_name}")

            imd_name = f"item-{vanilla_key.itempic_index}.imd"
            models = [f"{vanilla_key.model_name}{suffix}" for suffix in ["", "_NM", "_TR", "_WI"]]
            KeybladeRandomizer.extract_keyblade(
                keyblade_name=keyblade_name,
                author=None,
                output_path=vanilla_keys_path,
                original_itempic=extracted_data_path / "itempic" / imd_name,
                remastered_itempic=extracted_data_path / "remastered" / "itempic" / imd_name / "-0.dds",
                mdlx_files=[obj_path / f"{model}.mdlx" for model in models],
                remastered_mdlx_folders=[remastered_obj_path / f"{model}.mdlx" for model in models],
                fx_files=[obj_path / f"{model}.a.us" for model in models],
                remastered_fx_folders=[remastered_obj_path / f"{model}.a.us" for model in models],
                remastered_sound_files=[
                    remastered_obj_path / f"{model}.a.us/se/obj/{vanilla_key.sound_name}" for model in models
                ],
            )

        return vanilla_keys_path

    @staticmethod
    def import_keyblade(packaged_file: str) -> str:
        custom_visuals_path = appconfig.read_custom_visuals_path()
        if custom_visuals_path is None:
            raise GeneratorException("No custom visuals path configured. Can't import keyblade.")

        packaged_path = Path(packaged_file)
        keyblade_name, _ = os.path.splitext(packaged_path.name)

        keyblades_path = custom_visuals_path / "keyblades"
        keyblades_path.mkdir(exist_ok=True)

        shutil.unpack_archive(packaged_path, keyblades_path / keyblade_name, "zip")

        return keyblade_name

    @staticmethod
    def collect_vanilla_keyblades() -> list[ReplacementKeyblade]:
        result: list[ReplacementKeyblade] = []

        vanilla_keys_path = Path("cache/vanilla-keyblades").absolute()
        if not vanilla_keys_path.is_dir():
            return result

        for child in os.listdir(vanilla_keys_path):
            vanilla_key_path = vanilla_keys_path / child
            if vanilla_key_path.is_dir():
                keyblade_json_path = vanilla_key_path / "keyblade.json"
                if keyblade_json_path.is_file():
                    result.append(ReplacementKeyblade(vanilla_key_path.name, vanilla_key_path, keyblade_json_path))

        return result

    @staticmethod
    def collect_custom_keyblades() -> list[ReplacementKeyblade]:
        result: list[ReplacementKeyblade] = []

        custom_visuals_path = appconfig.read_custom_visuals_path()
        if custom_visuals_path is None:
            return result

        custom_keys_path = custom_visuals_path / "keyblades"
        if not custom_keys_path.is_dir():
            return result

        for child in os.listdir(custom_keys_path):
            custom_key_path = custom_keys_path / child
            if custom_key_path.is_dir():
                keyblade_json_path = custom_key_path / "keyblade.json"
                if keyblade_json_path.is_file():
                    result.append(ReplacementKeyblade(custom_key_path.name, custom_key_path, keyblade_json_path))

        return result

    @staticmethod
    def randomize_keyblades(
            setting: str,
            include_effects: bool,
            allow_duplicate_replacement: bool
    ) -> tuple[list[Asset], dict[str, str]]:
        if setting == configDict.VANILLA:
            return [], {}

        replacement_keys: list[ReplacementKeyblade] = []
        if setting == configDict.RANDOMIZE_IN_GAME_ONLY or setting == configDict.RANDOMIZE_ALL:
            replacement_keys.extend(KeybladeRandomizer.collect_vanilla_keyblades())
        if setting == configDict.RANDOMIZE_CUSTOM_ONLY or setting == configDict.RANDOMIZE_ALL:
            replacement_keys.extend(KeybladeRandomizer.collect_custom_keyblades())

        if len(replacement_keys) == 0:
            return [], {}

        replacement_keys = replacement_keys.copy()
        backup_keys = replacement_keys.copy()
        random.shuffle(replacement_keys)

        assets: list[Asset] = []
        replacements: dict[str, str] = {}
        vanilla_keyblades = _vanilla_keyblades()
        random.shuffle(vanilla_keyblades)
        for vanilla_key in vanilla_keyblades:
            if len(replacement_keys) == 0:
                if allow_duplicate_replacement:
                    replacement_keys = backup_keys.copy()
                    random.shuffle(replacement_keys)
                else:
                    break

            replacement = replacement_keys.pop()
            assets.extend(KeybladeRandomizer._itempic_assets(vanilla_key, replacement))
            assets.extend(KeybladeRandomizer._keyblade_assets(vanilla_key, replacement, "base", include_effects))
            assets.extend(KeybladeRandomizer._keyblade_assets(vanilla_key, replacement, "nm", include_effects))
            assets.extend(KeybladeRandomizer._keyblade_assets(vanilla_key, replacement, "tr", include_effects))
            assets.extend(KeybladeRandomizer._keyblade_assets(vanilla_key, replacement, "wi", include_effects))

            replacements[vanilla_key.name] = replacement.name

        return assets, replacements

    @staticmethod
    def _itempic_assets(vanilla: VanillaKeyblade, replacement: ReplacementKeyblade) -> list[Asset]:
        assets: list[Asset] = []

        original_itempic = replacement.original_itempic()
        if original_itempic is not None:
            assets.append({
                "name": f"itempic/item-{vanilla.itempic_index}.imd",
                "platform": "pc",
                "method": "copy",
                "source": [{"name": str(original_itempic)}]
            })

        remastered_itempic = replacement.remastered_itempic()
        if remastered_itempic is not None:
            assets.append({
                "name": f"remastered/itempic/item-{vanilla.itempic_index}.imd/-0.dds",
                "platform": "pc",
                "method": "copy",
                "source": [{"name": str(remastered_itempic)}]
            })

        return assets

    @staticmethod
    def _keyblade_assets(
            vanilla: VanillaKeyblade,
            replacement: ReplacementKeyblade,
            model_type: str,
            include_effects: bool
    ) -> list[Asset]:
        assets: list[Asset] = []

        model_name = vanilla.model_name
        suffix = _model_type_suffix(model_type)

        original_model = replacement.model(model_type)
        original_texture = replacement.texture(model_type)
        if original_model is not None and original_texture is not None:
            assets.append({
                "name": f"obj/{model_name}{suffix}.mdlx",
                "platform": "pc",
                "method": "binarc",
                "source": [
                    {
                        "name": "w_ex",
                        "type": "model",
                        "method": "copy",
                        "source": [{"name": str(original_model)}]
                    },
                    {
                        "name": "tim_",
                        "type": "modeltexture",
                        "method": "copy",
                        "source": [{"name": str(original_texture)}]
                    }
                ]
            })

        remastered_textures = replacement.remastered_textures(model_type)
        for remastered_texture_path in remastered_textures:
            assets.append({
                "name": f"remastered/obj/{model_name}{suffix}.mdlx/{remastered_texture_path.name}",
                "platform": "pc",
                "method": "copy",
                "source": [{"name": str(remastered_texture_path)}]
            })

        if not include_effects:
            return assets
        if not vanilla.can_replace_effects:
            return assets

        original_pax = replacement.pax(model_type)
        remastered_effects = replacement.remastered_effects(model_type)
        if original_pax is not None and len(remastered_effects) > 0:
            assets.append({
                "name": f"obj/{model_name}{suffix}.a.us",
                "platform": "pc",
                "method": "binarc",
                "source": [
                    {
                        "name": "w_ex",
                        "type": "pax",
                        "method": "copy",
                        "source": [{"name": str(original_pax)}]
                    }
                ]
            })

            for remastered_effect_path in remastered_effects:
                assets.append({
                    "name": f"remastered/obj/{model_name}{suffix}.a.us/{remastered_effect_path.name}",
                    "platform": "pc",
                    "method": "copy",
                    "source": [{"name": str(remastered_effect_path)}]
                })

        remastered_sound = replacement.remastered_sound(model_type)
        if remastered_sound is not None:
            # Since we're not replacing the SEB file, we should be able to use the sound name from the vanilla keyblade
            sound_name = vanilla.sound_name
            assets.append({
                "name": f"remastered/obj/{model_name}{suffix}.a.us/se/obj/{sound_name}",
                "platform": "pc",
                "method": "copy",
                "source": [{"name": str(remastered_sound)}]
            })

        return assets

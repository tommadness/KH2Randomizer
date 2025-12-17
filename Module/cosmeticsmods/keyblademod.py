import io
import json
import shutil
import zipfile
from pathlib import Path
from typing import Optional, Any

import requests
import yaml

from Class.exceptions import GeneratorException
from Class.openkhmod import ModYml, ModYmlException, AssetMethod, BinarcMethod, ModAsset, ModSourceFile, \
    ModYmlSyntaxException, StrDict
from Module import appconfig
from Module.cosmeticsmods import keyblade
from Module.cosmeticsmods.keyblade import VanillaKeyblade, KeybladeRandomizer, REMASTERED_TEXTURES, REMASTERED_EFFECTS, \
    ITEMPIC, KeybladeDdsVariants, KeybladePathVariants, VanillaKeybladePaths, KeybladeModelVariant
from Module.cosmeticsmods.openkh import BinaryArchiver
from Module.paths import children_with_extension

_KEYBLADE_VERSION = 1


class ImportableKeyblade:
    """A keyblade that can be imported into the randomizer."""

    def __init__(self):
        super().__init__()
        self.keyblade_name = ""
        self.itempic = Path()
        self.remastered_itempic = Path()
        self.remastered_mdlx = KeybladeDdsVariants()
        self.remastered_fx = KeybladeDdsVariants()
        self.remastered_scd = KeybladePathVariants()

    def validation_message(self) -> Optional[str]:
        if not self.remastered_itempic.is_file():
            return "Remastered itempic is required"
        if not self.remastered_mdlx.variant(KeybladeModelVariant.BASE):
            return "No base remastered textures found"
        return None

    def update_name(self, name: str):
        self.keyblade_name = name

    def copy_original_files(self, variant: KeybladeModelVariant, variant_path: Path, archiver: BinaryArchiver):
        raise NotImplementedError()

    def import_keyblade(
            self,
            output_path: Path,
            author: Optional[str],
            source: Optional[str],
            archiver: BinaryArchiver
    ):
        keyblade_output_location = self._create_keyblade_output_path(output_path)

        self._copy_itempics(keyblade_output_location)

        for variant in KeybladeModelVariant:
            variant_path = keyblade_output_location / variant.keyblade_mod_subdir_name()
            variant_path.mkdir(parents=True, exist_ok=True)
            self.copy_original_files(variant, variant_path, archiver)
            self._copy_remastered_files(variant, variant_path)

        self._write_keyblade_json(author=author, source=source, keyblade_output_location=keyblade_output_location)

    def _create_keyblade_output_path(self, output_path: Path) -> Path:
        safe_name = self.keyblade_name.replace("/", "-").replace("\\", "-")
        keyblade_output_location = output_path / safe_name
        keyblade_output_location.mkdir(parents=True, exist_ok=True)
        return keyblade_output_location

    def _copy_itempics(self, keyblade_output_location: Path):
        out_itempic_path = keyblade_output_location / ITEMPIC
        out_itempic_path.mkdir(parents=True, exist_ok=True)
        for itempic in [self.itempic, self.remastered_itempic]:
            if itempic.is_file():
                shutil.copy2(itempic, out_itempic_path)

    def _copy_remastered_files(self, variant: KeybladeModelVariant, variant_path: Path):
        def copy_textures(textures_input: dict[str, Path], textures_output: Path):
            if textures_input:
                textures_output.mkdir(parents=True, exist_ok=True)
                for dds_index, input_file in textures_input.items():
                    shutil.copy2(input_file, textures_output / f"{dds_index}.dds")

        def copy_sound(sound_input: Path, sound_output: Path):
            if sound_input.is_file():
                sound_output.mkdir(parents=True, exist_ok=True)
                copy_result = shutil.copy2(sound_input, sound_output)
                copy_result_path = Path(copy_result).absolute()
                renamed_path = copy_result_path.parent / f"{copy_result_path.name}.scd"
                if renamed_path.is_file():
                    renamed_path.unlink()
                copy_result_path.rename(renamed_path)

        copy_textures(self.remastered_mdlx.variant(variant), variant_path / REMASTERED_TEXTURES)
        copy_textures(self.remastered_fx.variant(variant), variant_path / REMASTERED_EFFECTS)
        copy_sound(self.remastered_scd.variant(variant), variant_path)

    def _write_keyblade_json(self, author: Optional[str], source: Optional[str], keyblade_output_location: Path):
        keyblade_json = {
            "version": _KEYBLADE_VERSION,
            "name": self.keyblade_name,
        }
        if author is not None and author != "":
            keyblade_json["author"] = author
        if source is not None and source != "":
            keyblade_json["source"] = source
        keyblade_json_path = keyblade_output_location / "keyblade.json"
        with open(keyblade_json_path, "w", encoding="utf-8") as keyblade_json_file:
            json.dump(keyblade_json, keyblade_json_file, indent=4)


class BinarcImportableKeyblade(ImportableKeyblade):
    """
    An importable keyblade whose mod uses the binarc method to patch the various subcomponents into the keyblade files.
    We can import these fairly directly.
    """

    def __init__(self):
        super().__init__()
        self.model = KeybladePathVariants()
        self.modeltexture = KeybladePathVariants()
        self.pax = KeybladePathVariants()
        self.wave = KeybladePathVariants()

    def validation_message(self) -> Optional[str]:
        super_message = super().validation_message()
        if super_message is not None:
            return super_message
        if not self.model.variant(KeybladeModelVariant.BASE).is_file():
            return "Base model is required"
        if not self.modeltexture.variant(KeybladeModelVariant.BASE).is_file():
            return "Base modeltexture is required"
        return None

    def copy_original_files(self, variant: KeybladeModelVariant, variant_path: Path, archiver: BinaryArchiver):
        for single_file_variants in [self.model, self.modeltexture, self.pax, self.wave]:
            single_file = single_file_variants.variant(variant)
            if single_file.is_file():
                shutil.copy2(single_file, variant_path)


class ExtractableKeyblade(ImportableKeyblade):
    """
    An importable keyblade whose mod completely overwrites keyblade models. We need to extract/deconstruct the files so
    that we can avoid messing with collision.
    """

    def __init__(self):
        super().__init__()
        self.mdlx = KeybladePathVariants()
        self.fx = KeybladePathVariants()

    def validation_message(self) -> Optional[str]:
        super_message = super().validation_message()
        if super_message is not None:
            return super_message
        if not self.mdlx.variant(KeybladeModelVariant.BASE).is_file():
            return "Base mdlx is required"
        return None

    def copy_original_files(self, variant: KeybladeModelVariant, variant_path: Path, archiver: BinaryArchiver):
        for single_file_variants in [self.mdlx, self.fx]:
            single_file = single_file_variants.variant(variant)
            if single_file.is_file():
                archiver.extract_bar(single_file, variant_path)


class KeybladeMod:
    """A parsed representation of an OpenKH keyblade replacement mod."""

    def __init__(self):
        super().__init__()
        self.author = ""
        self.source = ""
        self.keyblades: list[ImportableKeyblade] = []

    def import_keyblades(self) -> Path:
        """Imports all importable keyblades from this mod."""
        custom_visuals_path = appconfig.read_custom_visuals_path()
        if custom_visuals_path is None:
            raise GeneratorException("No custom visuals path configured. Can't import keyblades.")

        archiver = BinaryArchiver()

        keyblades_path = custom_visuals_path / KeybladeRandomizer.directory_name()
        keyblades_path.mkdir(exist_ok=True)

        for key in self.keyblades:
            key.import_keyblade(
                output_path=keyblades_path,
                author=self.author,
                source=self.source,
                archiver=archiver
            )

        return keyblades_path

    @staticmethod
    def extract_keyblade(
            keyblade_name: str,
            author: Optional[str],
            source: Optional[str],
            output_path: Path,
            original_itempic: Path,
            remastered_itempic: Path,
            mdlx_files: KeybladePathVariants,
            remastered_mdlx_dirs: KeybladePathVariants,
            fx_files: KeybladePathVariants,
            remastered_fx_dirs: KeybladePathVariants,
            sound_files: KeybladePathVariants,
    ):
        """Extracts a keyblade to the randomizer-specific file/folder structure."""

        def _paths_to_dds(paths: KeybladePathVariants) -> KeybladeDdsVariants:
            result = KeybladeDdsVariants()
            for variant, variant_path in paths.variants():
                variant_dds_paths = result.variant(variant)
                for dds_file in children_with_extension(variant_path, ".dds"):
                    variant_dds_paths[dds_file.stem] = dds_file
            return result

        key = ExtractableKeyblade()
        key.keyblade_name = keyblade_name
        key.itempic = original_itempic
        key.remastered_itempic = remastered_itempic
        key.mdlx = mdlx_files
        key.fx = fx_files
        key.remastered_mdlx = _paths_to_dds(remastered_mdlx_dirs)
        key.remastered_fx = _paths_to_dds(remastered_fx_dirs)
        key.remastered_scd = sound_files

        key.import_keyblade(output_path=output_path, author=author, source=source, archiver=BinaryArchiver())


class KeybladeModParser:

    def __init__(self, mod_folder: Path):
        super().__init__()
        self.mod_folder = mod_folder

    def try_parse_mod(self) -> Optional[KeybladeMod]:
        """Attempts to parse a keyblade mod."""
        mod_yml_path = self.mod_folder / "mod.yml"
        try:
            mod_yml = ModYml.from_file(mod_yml_path)

            parsed_mod = KeybladeMod()
            parsed_mod.author = mod_yml.original_author()
            parsed_mod.keyblades = self._find_keyblades(mod_yml.assets())

            return parsed_mod
        except ModYmlException:
            return None

    def _find_keyblades(self, assets: list[StrDict]) -> list[ImportableKeyblade]:
        vanilla_keyblades = keyblade.vanilla_keyblades()
        vanilla_keyblades_by_model_name = {key.model_name: key for key in vanilla_keyblades}

        found_keyblades_binarc: list[VanillaKeyblade] = []
        found_keyblades_copy: list[VanillaKeyblade] = []
        keyblade_names: dict[int, str] = {}

        for asset in assets:
            mod_asset = ModAsset(asset)
            asset_method = mod_asset.method()
            asset_game_file = mod_asset.primary_game_file()
            if asset_game_file.name == "sys.bar" and asset_method == AssetMethod.BINARC:
                keyblade_names.update(self._load_keyblade_names(mod_asset))
                continue

            matching_keyblade = vanilla_keyblades_by_model_name.get(asset_game_file.stem, None)
            if not matching_keyblade:
                continue

            if asset_method == AssetMethod.BINARC:
                found_keyblades_binarc.append(matching_keyblade)
            elif asset_method == AssetMethod.COPY:
                found_keyblades_copy.append(matching_keyblade)

        unknown_count = 1

        def keyblade_name() -> str:
            nonlocal unknown_count
            found_name = keyblade_names.get(found_keyblade.text_id, "")
            if found_name:
                return found_name
            else:
                name = f"Unnamed Keyblade {unknown_count}"
                unknown_count = unknown_count + 1
                return name

        result: list[ImportableKeyblade] = []
        for found_keyblade in found_keyblades_binarc:
            parsed = self._parse_binarc(assets, found_keyblade)
            if parsed is not None:
                parsed.keyblade_name = keyblade_name()
                result.append(parsed)
        for found_keyblade in found_keyblades_copy:
            parsed = self._parse_extractable(assets, found_keyblade)
            if parsed is not None:
                parsed.keyblade_name = keyblade_name()
                result.append(parsed)
        return result

    def _mod_relative_source_file(self, source_file: ModSourceFile) -> Path:
        source_file_path = source_file.file_path()
        if source_file_path.is_absolute():
            raise ModYmlSyntaxException("Expected mod source files to be relative")
        else:
            return self.mod_folder / source_file_path

    def _first_copy_source(self, mod_asset: ModAsset) -> Path:
        asset_copy_sources = mod_asset.copy_sources()
        if asset_copy_sources:
            return self._mod_relative_source_file(asset_copy_sources[0])
        else:
            return Path()

    def _first_binarc_source(self, mod_asset: ModAsset, type_to_match: str) -> Path:
        for asset_binarc_source in mod_asset.binarc_sources():
            if asset_binarc_source.type() == type_to_match:
                return self._mod_relative_source_file(asset_binarc_source.source_files()[0])
        return Path()

    def _parse_binarc(self, assets: list[StrDict], vanilla_key: VanillaKeyblade) -> Optional[BinarcImportableKeyblade]:
        vanilla_paths = VanillaKeybladePaths.for_vanilla_key(vanilla_key)
        result_key = BinarcImportableKeyblade()

        def handle_asset(asset: ModAsset):
            asset_game_files = asset.game_files()

            for asset_game_file in asset_game_files:
                asset_parent = asset_game_file.parent
                asset_stem = asset_game_file.stem

                # Itempics
                if asset_game_file == vanilla_paths.itempic:
                    result_key.itempic = self._first_copy_source(asset)
                    return
                elif asset_game_file == vanilla_paths.remastered_itempic:
                    result_key.remastered_itempic = self._first_copy_source(asset)
                    return

                # Model
                for variant, variant_path in vanilla_paths.mdlx_files.variants():
                    if asset_game_file == variant_path:
                        result_key.model.apply(variant, self._first_binarc_source(asset, "model"))
                        result_key.modeltexture.apply(variant, self._first_binarc_source(asset, "modeltexture"))
                        return

                # Effects
                for variant, variant_path in vanilla_paths.fx_files.variants():
                    if asset_game_file == variant_path:
                        result_key.pax.apply(variant, self._first_binarc_source(asset, "pax"))
                        result_key.wave.apply(variant, self._first_binarc_source(asset, "wd"))
                        return

                # Remastered textures
                for variant, variant_parent_path in vanilla_paths.remastered_mdlx_dirs.variants():
                    if asset_parent == variant_parent_path:
                        result_key.remastered_mdlx.variant(variant)[asset_stem] = self._first_copy_source(asset)
                        return

                # Remastered effects
                for variant, variant_parent_path in vanilla_paths.remastered_fx_dirs.variants():
                    if asset_parent == variant_parent_path:
                        result_key.remastered_fx.variant(variant)[asset_stem] = self._first_copy_source(asset)
                        return

                # Remastered sounds
                for variant, variant_sound_path in vanilla_paths.scd_files.variants():
                    if asset_parent == variant_sound_path.parent:
                        result_key.remastered_scd.apply(variant, self._first_copy_source(asset))
                        return

        for raw_asset in assets:
            handle_asset(ModAsset(raw_asset))

        validation_message = result_key.validation_message()
        if validation_message is None:
            return result_key
        else:
            print(f"Keyblade failed validation: {validation_message}")
            return None

    def _parse_extractable(self, assets: list[StrDict], vanilla_key: VanillaKeyblade) -> Optional[ExtractableKeyblade]:
        vanilla_paths = VanillaKeybladePaths.for_vanilla_key(vanilla_key)
        result_key = ExtractableKeyblade()

        def handle_asset(mod_asset: ModAsset):
            if mod_asset.method() != AssetMethod.COPY:
                return

            asset_game_files = mod_asset.game_files()

            for asset_game_file in asset_game_files:
                asset_parent = asset_game_file.parent
                asset_stem = asset_game_file.stem
                # Itempics
                if asset_game_file == vanilla_paths.itempic:
                    result_key.itempic = self._first_copy_source(mod_asset)
                    return
                elif asset_game_file == vanilla_paths.remastered_itempic:
                    result_key.remastered_itempic = self._first_copy_source(mod_asset)
                    return

                # Model
                for variant, variant_path in vanilla_paths.mdlx_files.variants():
                    if asset_game_file == variant_path:
                        result_key.mdlx.apply(variant, self._first_copy_source(mod_asset))
                        return

                # Effects
                for variant, variant_path in vanilla_paths.fx_files.variants():
                    if asset_game_file == variant_path:
                        result_key.fx.apply(variant, self._first_copy_source(mod_asset))
                        return

                # Remastered textures
                for variant, variant_parent_path in vanilla_paths.remastered_mdlx_dirs.variants():
                    if asset_parent == variant_parent_path:
                        result_key.remastered_mdlx.variant(variant)[asset_stem] = self._first_copy_source(mod_asset)
                        return

                # Remastered effects
                for variant, variant_parent_path in vanilla_paths.remastered_fx_dirs.variants():
                    if asset_parent == variant_parent_path:
                        result_key.remastered_fx.variant(variant)[asset_stem] = self._first_copy_source(mod_asset)
                        return

                # Remastered sounds
                for variant, variant_sound_path in vanilla_paths.scd_files.variants():
                    if asset_parent == variant_sound_path.parent:
                        result_key.remastered_scd.apply(variant, self._first_copy_source(mod_asset))
                        return

        for raw_asset in assets:
            handle_asset(ModAsset(raw_asset))

        validation_message = result_key.validation_message()
        if validation_message is None:
            return result_key
        else:
            print(f"Keyblade failed validation: {validation_message}")
            return None

    def _load_keyblade_names(self, asset: ModAsset) -> dict[int, str]:
        result: dict[int, str] = {}
        asset_sources = asset.binarc_sources()
        if not asset_sources:
            return result

        for asset_source in asset_sources:
            source_name = asset_source.name()
            source_type = asset_source.type()
            source_method = asset_source.method()
            if source_name == "sys" and source_type == "list" and source_method == BinarcMethod.KH2MSG:
                for source_file in asset_source.source_files():
                    if source_file["language"] == "en":
                        resolved_file = self._mod_relative_source_file(source_file)
                        with open(resolved_file, "r", encoding="utf-8") as opened_file:
                            data: list[dict[str, Any]] = yaml.safe_load(opened_file)
                            for entry in data:
                                text_id: int = entry.get("id", 0)
                                text_en: str = entry.get("en", "")
                                if text_id and text_en:
                                    result[text_id] = text_en
                            return result

        return result


class VanillaKeybladePack:

    @staticmethod
    def extract_vanilla_keyblades() -> Path:
        extracted_data_path = appconfig.extracted_game_path("kh2")
        if extracted_data_path is None:
            raise GeneratorException("No extracted KH2 game data, can't extract keyblades")

        vanilla_keys_path = Path("cache", "vanilla-keyblades")
        vanilla_keys_path.mkdir(parents=True, exist_ok=True)

        for vanilla_key in keyblade.vanilla_keyblades():
            keyblade_name = vanilla_key.name
            print(f"Extracting {keyblade_name}")

            paths = VanillaKeybladePaths.for_vanilla_key(vanilla_key, root=extracted_data_path)

            KeybladeMod.extract_keyblade(
                keyblade_name=keyblade_name,
                author=None,
                source=None,
                output_path=vanilla_keys_path,
                original_itempic=paths.itempic,
                remastered_itempic=paths.remastered_itempic,
                mdlx_files=paths.mdlx_files,
                remastered_mdlx_dirs=paths.remastered_mdlx_dirs,
                fx_files=paths.fx_files,
                remastered_fx_dirs=paths.remastered_fx_dirs,
                sound_files=paths.scd_files,
            )

        return vanilla_keys_path


class PackagedKeyblade:

    @staticmethod
    def import_keyblade(packaged_file: Path) -> str:
        custom_visuals_path = appconfig.read_custom_visuals_path()
        if custom_visuals_path is None:
            raise GeneratorException("No custom visuals path configured. Can't import keyblade.")

        keyblade_name = packaged_file.stem

        keyblades_path = custom_visuals_path / KeybladeRandomizer.directory_name()
        keyblades_path.mkdir(exist_ok=True)

        shutil.unpack_archive(packaged_file, keyblades_path / keyblade_name, "zip")

        return keyblade_name


class Kh1KeybladePack:

    @staticmethod
    def download_keyblade_pack(destination: Path):
        # Using a well-known commit in case the repository structure changes
        url = "https://github.com/Zurphing/KH1_Keyblades/archive/626145770bbe704ddb5c3f28228c11a7f21f4f62.zip"
        response = requests.get(url)
        response.raise_for_status()
        destination.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            zip_file.extractall(destination)

    @staticmethod
    def import_keyblades(pack_path: Path) -> Path:
        if not pack_path.is_dir():
            raise GeneratorException("Could not locate the Kingdom Hearts keyblade files. Can't import keyblades.")

        keyblade_mod = KeybladeModParser(pack_path).try_parse_mod()
        if keyblade_mod is None:
            raise GeneratorException("Failed to parse the Kingdom Hearts keyblade mod.")

        keyblade_mod.author = "Zurphing"
        keyblade_mod.source = "https://github.com/Zurphing/KH1_Keyblades"
        for key in keyblade_mod.keyblades:
            key.keyblade_name = f"{key.keyblade_name} (KH1)"

        return keyblade_mod.import_keyblades()


class BirthBySleepKeybladePack:

    @staticmethod
    def download_keyblade_pack(destination: Path):
        # Using a well-known commit in case the repository structure changes
        url = "https://github.com/Kite2810/Birth-by-Sleep-Keybladepack/archive/97d6ac2e6789cd0abd0ae16046b199fa1b6ad37b.zip"
        response = requests.get(url)
        response.raise_for_status()
        destination.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            zip_file.extractall(destination)

    @staticmethod
    def import_keyblades(pack_path: Path) -> Path:
        if not pack_path.is_dir():
            raise GeneratorException("Could not locate the Birth by Sleep keyblade files. Can't import keyblades.")

        keyblade_mod = KeybladeModParser(pack_path).try_parse_mod()
        if keyblade_mod is None:
            raise GeneratorException("Failed to parse the Birth by Sleep keyblade mod.")

        keyblade_mod.author = "Kite2810"
        keyblade_mod.source = "https://github.com/Kite2810/Birth-by-Sleep-Keybladepack"
        for key in keyblade_mod.keyblades:
            key.keyblade_name = f"{key.keyblade_name} (BBS)"

        return keyblade_mod.import_keyblades()

import json
import random
import shutil
import struct
from enum import Enum
from pathlib import Path
from typing import Optional, Any

from Class.exceptions import GeneratorException
from Class.openkhmod import AssetPlatform, BinarcMethod, ModAsset, ModBinarcSource, ModSourceFile, StrDict, \
    ObjectEntries
from List import configDict
from Module import appconfig
from Module.cosmeticsmods.openkh import BinaryArchiver
from Module.paths import child_with_extension, children_with_extension
from Module.resources import resource_path

ITEMPIC = "itempic"
REMASTERED_EFFECTS = "remastered-effects"
REMASTERED_TEXTURES = "remastered-textures"


class KeybladeModelVariant(str, Enum):
    BASE = "base"
    NIGHTMARE = "nm"
    TRON = "tr"
    WILLIE = "wi"

    def game_path_suffix(self) -> str:
        """Suffix used by game files for this variant."""
        if self == KeybladeModelVariant.NIGHTMARE:
            return "_NM"
        elif self == KeybladeModelVariant.TRON:
            return "_TR"
        elif self == KeybladeModelVariant.WILLIE:
            return "_WI"
        else:
            return ""

    def keyblade_mod_subdir_name(self) -> str:
        """Subdirectory used by keyblade mods for this variant."""
        return self.value


class KeybladePathVariants:
    """Associates a Path with each keyblade model variant."""

    def __init__(self):
        super().__init__()
        self._paths: dict[KeybladeModelVariant, Path] = {}

    def variant(self, variant: KeybladeModelVariant) -> Path:
        """Returns the path for the given variant."""
        return self._paths.get(variant, Path())

    def apply(self, variant: KeybladeModelVariant, value: Path):
        """Assigns the given path to the given variant."""
        self._paths[variant] = value

    def variants(self) -> list[tuple[KeybladeModelVariant, Path]]:
        """Returns each variant paired with its associated path."""
        return [(variant, self.variant(variant)) for variant in KeybladeModelVariant]


class KeybladeDdsVariants:
    """Associates Paths for .dds files with each keyblade world variant."""

    def __init__(self):
        super().__init__()
        self._data: dict[KeybladeModelVariant, dict[str, Path]] = {}

    def variant(self, variant: KeybladeModelVariant) -> dict[str, Path]:
        """Returns the stored mappings for the given variant."""
        if variant not in self._data:
            self._data[variant] = {}
        return self._data[variant]


class VanillaKeyblade:

    def __init__(
            self,
            name: str,
            itempic_index: str,
            sound_name: str,
            model_name: str,
            text_id: int,
    ):
        super().__init__()
        self.name = name
        self.itempic_index = itempic_index
        self.sound_name = sound_name
        self.model_name = model_name
        self.text_id = text_id
        # We were previously using this to allow certain keyblades (Oathkeeper and Sleeping Lion specifically) to fully
        # opt out of having their effects replaced due to sound effects getting messed up, even if just visual effects
        # were replaced. This doesn't seem to be a problem in more recent testing, either due to OpenKH Mods Manager /
        # Panacea updates, or due to the adding of a dummy wave file to randomized keyblades. If we are able to
        # reproduce this again in the future, make sure to document which custom keyblades are having the problem.
        self.can_replace_effects = True


class VanillaKeybladePaths:
    """Accumulates the file paths for a vanilla keyblade, relative to a root."""

    def __init__(self, itempic_index: str, model_name: str, sound_name: str, root: Path = Path()):
        super().__init__()

        imd_name = f"item-{itempic_index}.imd"
        self.itempic = root / "itempic" / imd_name
        self.remastered_itempic = root / "remastered" / "itempic" / imd_name / "-0.dds"

        obj = root / "obj"
        remastered_obj = root / "remastered" / "obj"
        self.mdlx_files = self._path_variants(base_path=obj, stem=model_name, extension="mdlx")
        self.fx_files = self._path_variants(base_path=obj, stem=model_name, extension="a.us")
        self.remastered_mdlx_dirs = self._path_variants(base_path=remastered_obj, stem=model_name, extension="mdlx")
        self.remastered_fx_dirs = self._path_variants(base_path=remastered_obj, stem=model_name, extension="a.us")

        self.scd_files = self._path_variants(base_path=remastered_obj, stem=model_name, extension="a.us")
        for variant, path in self.scd_files.variants():
            self.scd_files.apply(variant, path / "se" / "obj" / sound_name)

    @staticmethod
    def _path_variants(base_path: Path, stem: str, extension: str) -> KeybladePathVariants:
        variants = KeybladePathVariants()
        for model_variant in KeybladeModelVariant:
            variants.apply(model_variant, base_path / f"{stem}{model_variant.game_path_suffix()}.{extension}")
        return variants

    @staticmethod
    def for_vanilla_key(vanilla_key: VanillaKeyblade, root: Path = Path()) -> "VanillaKeybladePaths":
        return VanillaKeybladePaths(
            itempic_index=vanilla_key.itempic_index,
            model_name=vanilla_key.model_name,
            sound_name=vanilla_key.sound_name,
            root=root,
        )


class AddOnKeyblade:

    def __init__(
            self,
            name: str,
            itempic_index: str,
            override_sound_id: int,
            goa_mdlx_name_for_collision: str,
            override_model_name: str,
            objentry_object_ids: dict[KeybladeModelVariant, int],
            objentry_pages: dict[KeybladeModelVariant, int],
    ):
        super().__init__()
        self.name = name
        self.itempic_index = itempic_index
        self.override_sound_id = override_sound_id
        self.goa_mdlx_name_for_collision = goa_mdlx_name_for_collision
        self.override_model_name = override_model_name
        self._objentry_object_ids = objentry_object_ids
        self._objentry_pages = objentry_pages

    @staticmethod
    def keyblade_collisions_dir() -> Path:
        return Path("cache/keyblade-collisions").absolute()

    def override_model_name_variant(self, variant: KeybladeModelVariant) -> str:
        return f"{self.override_model_name}{variant.game_path_suffix()}"

    def override_sound_name(self) -> str:
        return f"se{self.override_sound_id}"

    def objentry_object_id(self, variant: KeybladeModelVariant) -> int:
        return self._objentry_object_ids[variant]

    def objentry_page(self, variant: KeybladeModelVariant) -> int:
        return self._objentry_pages[variant]

    def collision_file(self) -> Optional[Path]:
        candidate = self.keyblade_collisions_dir() / f"{self.name}.collision"
        if candidate.is_file():
            return candidate
        else:
            return None

    @staticmethod
    def extract_goa_collisions_if_needed() -> Path:
        keyblade_collisions_dir = AddOnKeyblade.keyblade_collisions_dir()
        keyblade_collisions_dir.mkdir(parents=True, exist_ok=True)

        found_all_collisions = True
        for add_on_key in add_on_keyblades():
            if add_on_key.collision_file() is None:
                found_all_collisions = False
                break

        if found_all_collisions:
            return keyblade_collisions_dir

        goa_mod_path = appconfig.goa_mod_path()
        if goa_mod_path is None:
            raise GeneratorException("Can't find GoA ROM mod. Can't extract GoA keyblades.")

        binary_archiver = BinaryArchiver()

        for add_on_key in add_on_keyblades():
            if add_on_key.collision_file() is not None:
                continue

            key_name = add_on_key.name
            key_dir = keyblade_collisions_dir / key_name
            key_dir.mkdir(parents=True, exist_ok=True)

            goa_keyblade_mdlx = goa_mod_path / "obj" / add_on_key.goa_mdlx_name_for_collision
            if not goa_keyblade_mdlx.is_file():
                raise GeneratorException(f"Can't find [{str(goa_keyblade_mdlx)}] to extract keyblade collision.")
            binary_archiver.extract_bar(goa_keyblade_mdlx, key_dir)

            collision_file = child_with_extension(key_dir, ".collision")
            if collision_file is not None:
                shutil.move(collision_file, keyblade_collisions_dir / f"{key_name}.collision")

            shutil.rmtree(key_dir)

            if collision_file is None:
                raise GeneratorException(f"Couldn't find a collision file in [{str(goa_keyblade_mdlx)}].")

            print(f"Extracted collision from {key_name}")

        return keyblade_collisions_dir


class ReplacementKeyblade:

    def __init__(self, name: str, keyblade_dir: Path, keyblade_json_file: Path):
        self.name = name
        self.keyblade_dir = keyblade_dir
        self.version = -1
        self.author: Optional[str] = None
        self.source: Optional[str] = None

        with open(keyblade_json_file, encoding="utf-8") as opened_file:
            keyblade_json: dict[str, Any] = json.load(opened_file)
            self.name = keyblade_json.get("name", self.name)
            self.version = keyblade_json.get("version", -1)
            self.author = keyblade_json.get("author", None)
            self.source = keyblade_json.get("source", None)

    def original_itempic(self) -> Optional[Path]:
        return child_with_extension(self.keyblade_dir / ITEMPIC, ".imd")

    def remastered_itempic(self) -> Optional[Path]:
        return child_with_extension(self.keyblade_dir / ITEMPIC, ".dds")

    def model(self, variant: KeybladeModelVariant) -> Optional[Path]:
        full_path = self.keyblade_dir / variant.keyblade_mod_subdir_name()
        file = child_with_extension(full_path, ".model")
        if file is not None:
            return file
        elif variant == KeybladeModelVariant.BASE:
            return None
        else:
            return self.model(KeybladeModelVariant.BASE)

    def texture(self, variant: KeybladeModelVariant) -> Optional[Path]:
        full_path = self.keyblade_dir / variant.keyblade_mod_subdir_name()
        file = child_with_extension(full_path, ".tim", ".texture")
        if file is not None:
            return file
        elif variant == KeybladeModelVariant.BASE:
            return None
        else:
            return self.texture(KeybladeModelVariant.BASE)

    def pax(self, variant: KeybladeModelVariant) -> Optional[Path]:
        full_path = self.keyblade_dir / variant.keyblade_mod_subdir_name()
        file = child_with_extension(full_path, ".pax")
        if file is not None:
            return file
        elif variant == KeybladeModelVariant.BASE:
            return None
        else:
            return self.pax(KeybladeModelVariant.BASE)

    def remastered_textures(self, variant: KeybladeModelVariant) -> list[Path]:
        full_path = self.keyblade_dir / variant.keyblade_mod_subdir_name() / REMASTERED_TEXTURES
        textures = children_with_extension(full_path, ".dds")
        if textures:
            return textures
        elif variant == KeybladeModelVariant.BASE:
            return []
        else:
            return self.remastered_textures(KeybladeModelVariant.BASE)

    def remastered_effects(self, variant: KeybladeModelVariant) -> list[Path]:
        full_path = self.keyblade_dir / variant.keyblade_mod_subdir_name() / REMASTERED_EFFECTS
        textures = children_with_extension(full_path, ".dds")
        if textures:
            return textures
        elif variant == KeybladeModelVariant.BASE:
            return []
        else:
            return self.remastered_effects(KeybladeModelVariant.BASE)

    def remastered_sound(self, variant: KeybladeModelVariant) -> Optional[Path]:
        full_path = self.keyblade_dir / variant.keyblade_mod_subdir_name()
        file = child_with_extension(full_path, ".scd")
        if file is not None:
            return file
        elif variant == KeybladeModelVariant.BASE:
            return None
        else:
            return self.remastered_sound(KeybladeModelVariant.BASE)


def vanilla_keyblades() -> list[VanillaKeyblade]:
    return [
        VanillaKeyblade("Kingdom Key", "043", "se500", "W_EX010", 0x05C2),
        VanillaKeyblade("Oathkeeper", "044", "se501", "W_EX010_10", 0x05C4),
        VanillaKeyblade("Oblivion", "045", "se502", "W_EX010_20", 0x05C6),
        VanillaKeyblade("Star Seeker", "046", "se507", "W_EX010_30", 0x3DFA),
        VanillaKeyblade("Hidden Dragon", "047", "se508", "W_EX010_40", 0x3DFC),
        VanillaKeyblade("Heros Crest", "048", "se509", "W_EX010_50", 0x3E2E),
        VanillaKeyblade("Monochrome", "049", "se510", "W_EX010_60", 0x3E30),
        VanillaKeyblade("Follow the Wind", "050", "se511", "W_EX010_70", 0x3E32),
        VanillaKeyblade("Circle of Life", "051", "se512", "W_EX010_80", 0x3E34),
        VanillaKeyblade("Photon Debugger", "052", "se513", "W_EX010_90", 0x3E36),
        VanillaKeyblade("Gull Wing", "053", "se514", "W_EX010_A0", 0x3E38),
        VanillaKeyblade("Rumbling Rose", "054", "se515", "W_EX010_B0", 0x3E3A),
        VanillaKeyblade("Guardian Soul", "055", "se516", "W_EX010_C0", 0x3E3C),
        VanillaKeyblade("Wishing Lamp", "056", "se517", "W_EX010_D0", 0x3E3E),
        VanillaKeyblade("Decisive Pumpkin", "057", "se518", "W_EX010_E0", 0x3E40),
        VanillaKeyblade("Sleeping Lion", "058", "se519", "W_EX010_F0", 0x3E42),
        VanillaKeyblade("Sweet Memories", "059", "se520", "W_EX010_G0", 0x3E44),
        VanillaKeyblade("Mysterious Abyss", "060", "se521", "W_EX010_H0", 0x3E46),
        VanillaKeyblade("Fatal Crest", "061", "se522", "W_EX010_J0", 0x3E48),
        VanillaKeyblade("Bond of Flame", "062", "se523", "W_EX010_K0", 0x3E4A),
        VanillaKeyblade("Fenrir", "063", "se524", "W_EX010_M0", 0x3E4C),
        VanillaKeyblade("Ultima Weapon", "064", "se525", "W_EX010_N0", 0x3E4E),
        VanillaKeyblade("Two Become One", "300", "se526", "W_EX010_P0", 0x4E35),
        VanillaKeyblade("Winners Proof", "301", "se527", "W_EX010_R0", 0x4E37),
    ]


def add_on_keyblades() -> list[AddOnKeyblade]:
    return [
        AddOnKeyblade(
            name="Kingdom Key D",
            itempic_index="299",
            override_sound_id=9100,
            goa_mdlx_name_for_collision="W_EX010_00.mdlx",
            override_model_name="W_EX010_0X",
            objentry_object_ids={
                KeybladeModelVariant.BASE: 0xBB9,
                KeybladeModelVariant.NIGHTMARE: 0xBBA,
                KeybladeModelVariant.TRON: 0xBBE,
            },
            objentry_pages={
                KeybladeModelVariant.BASE: 17,
                KeybladeModelVariant.NIGHTMARE: 17,
                KeybladeModelVariant.TRON: 17,
            },
        ),
        AddOnKeyblade(
            name="Alpha Weapon",
            itempic_index="297",
            override_sound_id=9101,
            goa_mdlx_name_for_collision="W_EX010_Y0.mdlx",
            override_model_name="W_EX010_YX",
            objentry_object_ids={
                KeybladeModelVariant.BASE: 0x6A,
                KeybladeModelVariant.NIGHTMARE: 0xBBB,
                KeybladeModelVariant.TRON: 0xBBF,
            },
            objentry_pages={
                KeybladeModelVariant.BASE: 0,
                KeybladeModelVariant.NIGHTMARE: 17,
                KeybladeModelVariant.TRON: 17,
            },
        ),
        AddOnKeyblade(
            name="Omega Weapon",
            itempic_index="298",
            override_sound_id=9102,
            goa_mdlx_name_for_collision="W_EX010_Z0.mdlx",
            override_model_name="W_EX010_ZX",
            objentry_object_ids={
                KeybladeModelVariant.BASE: 0x6B,
                KeybladeModelVariant.NIGHTMARE: 0xBBC,
                KeybladeModelVariant.TRON: 0xBC0,
            },
            objentry_pages={
                KeybladeModelVariant.BASE: 0,
                KeybladeModelVariant.NIGHTMARE: 17,
                KeybladeModelVariant.TRON: 17,
            },
        ),
        AddOnKeyblade(
            name="Pureblood",
            itempic_index="296",
            override_sound_id=9103,
            goa_mdlx_name_for_collision="W_EX010_X0.mdlx",
            override_model_name="W_EX010_XX",
            objentry_object_ids={
                KeybladeModelVariant.BASE: 0x384,
                KeybladeModelVariant.NIGHTMARE: 0xBBD,
                KeybladeModelVariant.TRON: 0xBC1,
            },
            objentry_pages={
                KeybladeModelVariant.BASE: 0,
                KeybladeModelVariant.NIGHTMARE: 17,
                KeybladeModelVariant.TRON: 17,
            },
        ),
        AddOnKeyblade(
            name="Struggle Hammer",
            itempic_index="065",
            override_sound_id=9104,
            goa_mdlx_name_for_collision="W_EX010_U0_NM.mdlx",
            override_model_name="W_EX010_UX",
            objentry_object_ids={
                KeybladeModelVariant.BASE: 0x77C,
                KeybladeModelVariant.NIGHTMARE: 0xBC4,
                KeybladeModelVariant.TRON: 0xBC7,
            },
            objentry_pages={
                KeybladeModelVariant.BASE: 0,
                KeybladeModelVariant.NIGHTMARE: 17,
                KeybladeModelVariant.TRON: 17,
            },
        ),
        AddOnKeyblade(
            name="Struggle Wand",
            itempic_index="066",
            override_sound_id=9105,
            goa_mdlx_name_for_collision="W_EX010_V0_NM.mdlx",
            override_model_name="W_EX010_VX",
            objentry_object_ids={
                KeybladeModelVariant.BASE: 0x77D,
                KeybladeModelVariant.NIGHTMARE: 0xBC3,
                KeybladeModelVariant.TRON: 0xBC6,
            },
            objentry_pages={
                KeybladeModelVariant.BASE: 0,
                KeybladeModelVariant.NIGHTMARE: 17,
                KeybladeModelVariant.TRON: 17,
            },
        ),
        AddOnKeyblade(
            name="Struggle Sword",
            itempic_index="067",
            override_sound_id=9106,
            goa_mdlx_name_for_collision="W_EX010_W0_NM.mdlx",
            override_model_name="W_EX010_WX",
            objentry_object_ids={
                KeybladeModelVariant.BASE: 0x73B,
                KeybladeModelVariant.NIGHTMARE: 0xBC2,
                KeybladeModelVariant.TRON: 0xBC5,
            },
            objentry_pages={
                KeybladeModelVariant.BASE: 0,
                KeybladeModelVariant.NIGHTMARE: 17,
                KeybladeModelVariant.TRON: 17,
            },
        ),
    ]


class KeybladeRandomizerResult:

    def __init__(self):
        super().__init__()
        self.assets: list[ModAsset] = []
        self.object_entries = ObjectEntries(source_name="")  # The source name will get filled in later
        self.replacements: dict[str, str] = {}

    def add_object_entry(self, object_id: int, model_name: str, page: int):
        self.object_entries.add_object(
            object_id=object_id,
            object_type="WEAPON",
            subtype=0,
            draw_priority=0,
            weapon_joint=25,
            model_name=model_name,
            animation_name="",
            flags=0,
            object_target_type="M",
            padding=0,
            neo_status=0,
            neo_moveset=0,
            weight=0,
            spawn_limiter=0,
            page=page,
            object_shadow_size="SmallShadow",
            object_form="Default",
            spawn_object_1=0,
            spawn_object_2=0,
            spawn_object_3=0,
            spawn_object_4=0,
            no_apdx=False,
            before=False,
            fix_color=False,
            fly=False,
            scissoring=False,
            is_pirate=False,
            wall_occlusion=False,
            hift=False,
        )


class KeybladeRandomizer:

    @staticmethod
    def directory_name() -> str:
        return "keyblades"

    @staticmethod
    def dummy_wave_resource_path() -> str:
        return resource_path("static/cosmetics/keyblades/dummy_wave.wd")

    @staticmethod
    def keyblade_rando_options() -> dict[str, str]:
        return {
            configDict.VANILLA: "Vanilla",
            configDict.RANDOMIZE_IN_GAME_ONLY: "Randomize (in-game only)",
            configDict.RANDOMIZE_CUSTOM_ONLY: "Randomize (custom only)",
            configDict.RANDOMIZE_ALL: "Randomize (in-game + custom)",
        }

    @staticmethod
    def _collect_keyblades(keyblades_dir: Path) -> list[ReplacementKeyblade]:
        result: list[ReplacementKeyblade] = []

        if not keyblades_dir.is_dir():
            return result

        for keyblade_dir in keyblades_dir.iterdir():
            if keyblade_dir.is_dir():
                keyblade_json_file = keyblade_dir / "keyblade.json"
                if keyblade_json_file.is_file():
                    result.append(ReplacementKeyblade(keyblade_dir.name, keyblade_dir, keyblade_json_file))

        return result

    @staticmethod
    def collect_vanilla_keyblades() -> list[ReplacementKeyblade]:
        vanilla_keys_path = Path("cache", "vanilla-keyblades").absolute()
        return KeybladeRandomizer._collect_keyblades(vanilla_keys_path)

    @staticmethod
    def collect_custom_keyblades() -> list[ReplacementKeyblade]:
        custom_visuals_path = appconfig.read_custom_visuals_path()
        if custom_visuals_path is None:
            return []

        custom_keys_path = custom_visuals_path / KeybladeRandomizer.directory_name()
        return KeybladeRandomizer._collect_keyblades(custom_keys_path)

    @staticmethod
    def randomize_keyblades(
            setting: str,
            include_effects: bool,
            allow_duplicate_replacement: bool,
            replace_goa_keyblades: bool,
    ) -> KeybladeRandomizerResult:
        result = KeybladeRandomizerResult()

        if setting == configDict.VANILLA:
            return result

        replacement_keys: list[ReplacementKeyblade] = []
        if setting == configDict.RANDOMIZE_IN_GAME_ONLY or setting == configDict.RANDOMIZE_ALL:
            replacement_keys.extend(KeybladeRandomizer.collect_vanilla_keyblades())
        if setting == configDict.RANDOMIZE_CUSTOM_ONLY or setting == configDict.RANDOMIZE_ALL:
            replacement_keys.extend(KeybladeRandomizer.collect_custom_keyblades())

        if len(replacement_keys) == 0:
            return result

        replacement_keys = replacement_keys.copy()
        backup_keys = replacement_keys.copy()
        random.shuffle(replacement_keys)

        vanilla_keys = vanilla_keyblades()
        random.shuffle(vanilla_keys)
        for vanilla_key in vanilla_keys:
            vanilla_paths = VanillaKeybladePaths.for_vanilla_key(vanilla_key)

            if len(replacement_keys) == 0:
                if allow_duplicate_replacement:
                    replacement_keys = backup_keys.copy()
                    random.shuffle(replacement_keys)
                else:
                    break

            replacement_key = replacement_keys.pop()

            result.assets.extend(KeybladeRandomizer._itempic_assets(vanilla_paths, replacement_key))

            for variant in KeybladeModelVariant:
                variant_assets = KeybladeRandomizer._keyblade_assets(
                    vanilla_paths=vanilla_paths,
                    replacement_key=replacement_key,
                    variant=variant,
                    include_effects=include_effects and vanilla_key.can_replace_effects,
                )
                result.assets.extend(variant_assets)

            result.replacements[vanilla_key.name] = replacement_key.name

        if not replace_goa_keyblades:
            return result

        AddOnKeyblade.extract_goa_collisions_if_needed()

        def can_use_for_add_on(candidate: ReplacementKeyblade) -> bool:
            has_model = candidate.model(KeybladeModelVariant.BASE) is not None
            has_texture = candidate.texture(KeybladeModelVariant.BASE) is not None
            has_pax = candidate.pax(KeybladeModelVariant.BASE) is not None
            has_re_textures = len(candidate.remastered_textures(KeybladeModelVariant.BASE)) > 0
            has_re_effects = len(candidate.remastered_effects(KeybladeModelVariant.BASE)) > 0
            has_scd = candidate.remastered_sound(KeybladeModelVariant.BASE) is not None
            return has_model and has_texture and has_pax and has_re_textures and has_re_effects and has_scd

        # Need to create new source lists - not all keyblades can replace add-on keys, since they need all the
        # keyblade components pre-packaged
        backup_keys = [key for key in backup_keys if can_use_for_add_on(key)]
        if not backup_keys:
            return result
        replacement_keys = [key for key in replacement_keys if can_use_for_add_on(key)]

        # None of the GoA keyblades bother with WILLIE
        add_on_variants = [KeybladeModelVariant.BASE, KeybladeModelVariant.NIGHTMARE, KeybladeModelVariant.TRON]

        add_on_keys = add_on_keyblades()
        random.shuffle(add_on_keys)
        for add_on_key in add_on_keys:
            if len(replacement_keys) == 0:
                if allow_duplicate_replacement:
                    replacement_keys = backup_keys.copy()
                    random.shuffle(replacement_keys)
                else:
                    break

            replacement_key = replacement_keys.pop()

            fake_vanilla_paths = VanillaKeybladePaths(
                itempic_index=add_on_key.itempic_index,
                model_name=add_on_key.override_model_name,
                sound_name=add_on_key.override_sound_name(),
            )

            result.assets.extend(KeybladeRandomizer._itempic_assets(fake_vanilla_paths, replacement_key))

            for variant in add_on_variants:
                # Need to add a custom object entry so that we can redirect to our override model instead of the one
                # provided by the GoA mod
                result.add_object_entry(
                    object_id=add_on_key.objentry_object_id(variant),
                    model_name=add_on_key.override_model_name_variant(variant),
                    page=add_on_key.objentry_page(variant),
                )

                result.assets.extend(KeybladeRandomizer._handle_add_on_key(
                    replacement_key,
                    variant,
                    add_on_key,
                    fake_vanilla_paths
                ))

            result.replacements[add_on_key.name] = replacement_key.name

        return result

    @staticmethod
    def _itempic_assets(vanilla_paths: VanillaKeybladePaths, replacement_key: ReplacementKeyblade) -> list[ModAsset]:
        assets: list[ModAsset] = []

        # TODO: This was crashing with at least one itempic (Fresh Faces keyblade).
        #   Since these really shouldn't matter on PC, just not bothering for now.
        #   If someone else wants to try to figure this out, feel free.
        # original_itempic = replacement_key.original_itempic()
        # if original_itempic is not None:
        #     assets.append(ModYml.make_copy_asset(
        #         game_files=[vanilla_paths.itempic],
        #         source_files=[original_itempic],
        #         platform=PC,
        #     ))

        remastered_itempic = replacement_key.remastered_itempic()
        if remastered_itempic is not None:
            assets.append(ModAsset.make_copy_asset(
                game_files=[vanilla_paths.remastered_itempic],
                source_file=remastered_itempic,
                platform=AssetPlatform.PC,
            ))

        return assets

    @staticmethod
    def _keyblade_assets(
            vanilla_paths: VanillaKeybladePaths,
            replacement_key: ReplacementKeyblade,
            variant: KeybladeModelVariant,
            include_effects: bool,
    ) -> list[ModAsset]:
        assets: list[ModAsset] = []

        original_model = replacement_key.model(variant)
        original_texture = replacement_key.texture(variant)
        if original_model is not None and original_texture is not None:
            assets.append(ModAsset.make_binarc_asset(
                game_files=[vanilla_paths.mdlx_files.variant(variant)],
                sources=[
                    ModBinarcSource.make_source(
                        name="w_ex",
                        type_="model",
                        method=BinarcMethod.COPY,
                        sources=[ModSourceFile.make_source_file(original_model)],
                    ),
                    ModBinarcSource.make_source(
                        name="tim_",
                        type_="modeltexture",
                        method=BinarcMethod.COPY,
                        sources=[ModSourceFile.make_source_file(original_texture)],
                    ),
                ],
                platform=AssetPlatform.PC,
            ))

        for remastered_texture_path in replacement_key.remastered_textures(variant):
            assets.append(ModAsset.make_copy_asset(
                game_files=[vanilla_paths.remastered_mdlx_dirs.variant(variant) / remastered_texture_path.name],
                source_file=remastered_texture_path,
                platform=AssetPlatform.PC,
            ))

        if not include_effects:
            return assets

        original_pax = replacement_key.pax(variant)
        remastered_effects = replacement_key.remastered_effects(variant)
        remastered_sound = replacement_key.remastered_sound(variant)

        # We can proceed as long as there are replacement visual effects.
        # If there is only a replacement sound file, things don't seem to be very stable.
        if original_pax is None or len(remastered_effects) == 0:
            if remastered_sound is not None:
                key_dir = replacement_key.keyblade_dir
                print(f"{key_dir} has a replacement sound but no replacement visual effects. Cannot replace sound only.")
            return assets

        from Module.seedmod import CosmeticsModAppender
        original_effect_sources: list[ModBinarcSource] = [
            ModBinarcSource.make_source(
                name="w_ex",
                type_="pax",
                method=BinarcMethod.COPY,
                sources=[ModSourceFile.make_source_file(original_pax)],
            ),
            # Adding a dummy wave file seems to prevent some crashes.
            # Inspiration taken from Zurphing's KH1 keyblade pack.
            ModBinarcSource.make_source(
                name="wave",
                type_="wd",
                method=BinarcMethod.COPY,
                sources=[ModSourceFile.make_source_file(CosmeticsModAppender.keyblade_dummy_wave_source())],
            ),
        ]
        assets.append(ModAsset.make_binarc_asset(
            game_files=[vanilla_paths.fx_files.variant(variant)],
            sources=original_effect_sources,
            platform=AssetPlatform.PC,
        ))

        for remastered_effect_path in remastered_effects:
            assets.append(ModAsset.make_copy_asset(
                game_files=[vanilla_paths.remastered_fx_dirs.variant(variant) / remastered_effect_path.name],
                source_file=remastered_effect_path,
                platform=AssetPlatform.PC,
            ))

        vanilla_scd_path = vanilla_paths.scd_files.variant(variant)
        if remastered_sound is None:
            # Copying over the sound from the vanilla keyblade seems to prevent crashes when the replacement keyblade
            # doesn't have a .scd file included, but has other effect files.
            # (BBS Destiny's Embrace in particular was crashing as a Kingdom Key replacement without this.)
            assets.append(ModAsset.make_copy_asset(
                game_files=[vanilla_scd_path],
                source_file=vanilla_scd_path,
                platform=AssetPlatform.PC,
                internal=True,
            ))
        else:
            # We're not replacing the SEB file, so should be able to use the sound file path from the vanilla keyblade
            assets.append(ModAsset.make_copy_asset(
                game_files=[vanilla_scd_path],
                source_file=remastered_sound,
                platform=AssetPlatform.PC,
            ))

        return assets

    @staticmethod
    def seb_file_data(sound_id: int) -> bytearray:
        """
        https://openkh.dev/kh2/file/type/seb.html
        seb file format:
        Offset 	Type 	Description
        0       string  Seemingly always “ORIGIN”. If removed, sound effects from se000 will play instead.
        8       uint16  Sound ID Number; not used by the game?
        10      uint16  Unknown; not used by the game?
        12      uint16  Sound ID Number
        16      string  Filepath to SCD in objects remastered folder.
        """

        # Format string:
        # 8s: 8-byte string (bytes 0-7)
        # H: 2-byte unsigned short (bytes 8-9)
        # H: 2-byte unsigned short (bytes 10-11)
        # H: 2-byte unsigned short (bytes 12-13)
        # 2x: skip 2 bytes (bytes 14-15)
        # 32s: 32-byte string (bytes 16-47)
        # The '<' indicates little-endian byte order for the integers.
        format_string = "<8sHHH2x32s"

        data_array = bytearray(48)
        struct.pack_into(
            format_string,
            data_array,
            0,
            "ORIGIN".encode("utf-8"),  # 0-7
            sound_id,  # 8-9
            61,  # 10-11 (Most of them seem to be 61)
            sound_id,  # 12-13
            f"se/obj/se{sound_id}".encode("utf-8"),  # 16-47
        )

        return data_array

    @staticmethod
    def _handle_add_on_key(
            replacement_key: ReplacementKeyblade,
            variant: KeybladeModelVariant,
            add_on_key: AddOnKeyblade,
            vanilla_paths: VanillaKeybladePaths,
    ) -> list[ModAsset]:
        # For the add-on keyblades, we pre-package .mdlx and .a.us files with the collision of the add-on keyblade.
        # If any of the pre-packaged files aren't there, create them as needed.

        target_dir = replacement_key.keyblade_dir / variant.keyblade_mod_subdir_name() / "add-ons"
        target_dir.mkdir(parents=True, exist_ok=True)

        override_model_name = add_on_key.override_model_name_variant(variant)
        mdlx_file = target_dir / f"{override_model_name}.mdlx"
        fx_file = target_dir / f"{override_model_name}.a.us"

        assets = KeybladeRandomizer._add_on_assets(
            replacement_key=replacement_key,
            variant=variant,
            vanilla_paths=vanilla_paths,
            mdlx_file=mdlx_file,
            fx_file=fx_file,
        )

        if mdlx_file.is_file() and fx_file.is_file():
            return assets

        staging_dir = target_dir / f"{override_model_name}-staging"
        staging_dir.mkdir(parents=True, exist_ok=True)

        if not mdlx_file.is_file():
            shutil.copy2(replacement_key.model(variant), staging_dir)
            shutil.copy2(replacement_key.texture(variant), staging_dir)
            # We specifically use the collision of the keyblade we're replacing
            # (this is kinda the whole point of all this)
            collision_file = add_on_key.collision_file()
            if collision_file is None:
                raise GeneratorException(f"Extracted collision file is missing for {add_on_key.name}")
            shutil.copy2(collision_file, staging_dir)

            packaged_file = KeybladeRandomizer._package_mdlx(staging_dir, keyblade_name=override_model_name)
            shutil.move(packaged_file, target_dir)

        if not fx_file.is_file():
            shutil.copy2(replacement_key.pax(variant), staging_dir)
            shutil.copy2(KeybladeRandomizer.dummy_wave_resource_path(), staging_dir)

            sound_id = add_on_key.override_sound_id
            seb_data = KeybladeRandomizer.seb_file_data(sound_id=sound_id)
            with open(staging_dir / f"se{str(sound_id)[0:2]}.seb", "wb") as opened_file:
                opened_file.write(seb_data)

            packaged_file = KeybladeRandomizer._package_fx(staging_dir, keyblade_name=override_model_name)
            shutil.move(packaged_file, target_dir)

        shutil.rmtree(staging_dir)
        return assets

    @staticmethod
    def _add_on_assets(
            replacement_key: ReplacementKeyblade,
            variant: KeybladeModelVariant,
            vanilla_paths: VanillaKeybladePaths,
            mdlx_file: Path,
            fx_file: Path,
    ) -> list[ModAsset]:
        assets: list[ModAsset] = [
            ModAsset.make_copy_asset(
                game_files=[vanilla_paths.mdlx_files.variant(variant)],
                source_file=mdlx_file,
                platform=AssetPlatform.PC,
            ),
            ModAsset.make_copy_asset(
                game_files=[vanilla_paths.fx_files.variant(variant)],
                source_file=fx_file,
                platform=AssetPlatform.PC,
            ),
        ]

        for remastered_texture_path in replacement_key.remastered_textures(variant):
            assets.append(ModAsset.make_copy_asset(
                game_files=[vanilla_paths.remastered_mdlx_dirs.variant(variant) / remastered_texture_path.name],
                source_file=remastered_texture_path,
                platform=AssetPlatform.PC,
            ))

        for remastered_effect_path in replacement_key.remastered_effects(variant):
            assets.append(ModAsset.make_copy_asset(
                game_files=[vanilla_paths.remastered_fx_dirs.variant(variant) / remastered_effect_path.name],
                source_file=remastered_effect_path,
                platform=AssetPlatform.PC,
            ))

        assets.append(ModAsset.make_copy_asset(
            game_files=[vanilla_paths.scd_files.variant(variant)],
            source_file=replacement_key.remastered_sound(variant),
            platform=AssetPlatform.PC,
        ))

        return assets

    @staticmethod
    def _package_mdlx(source_dir: Path, keyblade_name: str) -> Path:
        model_file = child_with_extension(source_dir, ".model")
        if model_file is None:
            raise GeneratorException("No model file found for mdlx")

        texture_file = child_with_extension(source_dir, ".tim", ".texture")
        if texture_file is None:
            raise GeneratorException("No texture file found for mdlx")

        collision_file = child_with_extension(source_dir, ".collision")
        if collision_file is None:
            raise GeneratorException("No collision file found for mdlx")

        mdlx_file_name = f"{keyblade_name}.mdlx"
        mdlx_project_data: StrDict = {
            "OriginalFileName": mdlx_file_name,
            "Motionset": 0,
            "Entries": [
                {
                    "FileName": model_file.name,
                    "InternalName": "w_ex",
                    "TypeId": 4,
                    "LinkIndex": 0,
                },
                {
                    "FileName": texture_file.name,
                    "InternalName": "tim_",
                    "TypeId": 7,
                    "LinkIndex": 0,
                },
                {
                    "FileName": collision_file.name,
                    "InternalName": "w_ex",
                    "TypeId": 23,
                    "LinkIndex": 0,
                },
            ],
        }
        project_json_file = source_dir / f"{mdlx_file_name}.json"
        with open(project_json_file, "w", encoding="utf-8") as opened_file:
            json.dump(mdlx_project_data, opened_file, sort_keys=False)

        archiver = BinaryArchiver()
        archiver.create_bar(bar_json_file=project_json_file, destination=source_dir)

        return source_dir / mdlx_file_name

    @staticmethod
    def _package_fx(source_dir: Path, keyblade_name: str) -> Path:
        pax_file = child_with_extension(source_dir, ".pax")
        if pax_file is None:
            raise GeneratorException("No pax file found for effects")

        wave_file = child_with_extension(source_dir, ".wd")
        if wave_file is None:
            raise GeneratorException("No wave file found for effects")

        seb_file = child_with_extension(source_dir, ".seb")
        if seb_file is None:
            raise GeneratorException("No seb file found for effects")

        fx_file_name = f"{keyblade_name}.a.us"
        fx_project_data: StrDict = {
            "OriginalFileName": fx_file_name,
            "Motionset": 0,
            "Entries": [
                {
                    "FileName": pax_file.name,
                    "InternalName": "w_ex",
                    "TypeId": 18,
                    "LinkIndex": 0,
                },
                {
                    "FileName": wave_file.name,
                    "InternalName": "wave",
                    "TypeId": 32,
                    "LinkIndex": 0,
                },
                {
                    "FileName": seb_file.name,
                    "InternalName": f"{seb_file.stem}",
                    "TypeId": 31,
                    "LinkIndex": 0,
                },
            ],
        }
        project_json_file = source_dir / f"{fx_file_name}.json"
        with open(project_json_file, "w", encoding="utf-8") as opened_file:
            json.dump(fx_project_data, opened_file, sort_keys=False)

        archiver = BinaryArchiver()
        archiver.create_bar(bar_json_file=project_json_file, destination=source_dir)

        return source_dir / fx_file_name

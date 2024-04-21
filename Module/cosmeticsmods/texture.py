import gzip
import os
import random
import shutil
import string
from pathlib import Path
from typing import Any, Optional, Callable

import numpy as np
import yaml
from PIL import Image
from numpy import ndarray

from Class import settingkey
from Class.openkhmod import Asset
from Class.seedSettings import SeedSettings
from Module import version, appconfig
from Module.cosmeticsmods.image import rgb_to_hsv, hsv_to_rgb
from Module.resources import resource_path

VANILLA = "vanilla"
RANDOM = "random"
_HUE_INDEX = 0
_SATURATION_INDEX = 1
_VALUE_INDEX = 2
_ALPHA_INDEX = 3

MaskCondition = Callable[[tuple[int, int]], bool]
ColorCondition = Callable[[Optional[float]], bool]

# In most cases, the difference between 90-180 is pretty minimal (various degrees of blue-green), and including all of
# them makes the random colors feel a bit too biased to blue-green. We'll keep 120 as our "green" and 180 as our "cyan"
# but remove 90 and 150.
available_random_hues: list[int] = [0, 30, 60, 120, 180, 210, 240, 270, 300, 330]


def _default_color_condition(color: Optional[float]) -> bool:
    return color is not None


class HsvaConditions:
    """Conditions for matching hue/saturation/value/alpha color components."""

    def __init__(
            self,
            description: str,
            hue_condition: ColorCondition,
            saturation_condition: ColorCondition,
            value_condition: ColorCondition,
            alpha_condition: ColorCondition
    ):
        self.description = description
        self.hue_condition = hue_condition
        self.saturation_condition = saturation_condition
        self.value_condition = value_condition
        self.alpha_condition = alpha_condition

    def matches(
            self,
            hue: Optional[float],
            saturation: Optional[float],
            value: Optional[float],
            alpha: Optional[float]
    ) -> bool:
        return self.hue_condition(hue) \
            and self.saturation_condition(saturation) \
            and self.value_condition(value) \
            and self.alpha_condition(alpha)


class PixelMatchingConditions:
    """Conditions for matching pixels."""

    def __init__(self, masks: list[Optional[ndarray]], hsva_conditions: Optional[HsvaConditions]):
        super().__init__()
        self.mask_conditions: list[Optional[MaskCondition]] = []
        for mask in masks:
            self.mask_conditions.append(_make_mask_condition(mask))
        self.hsva_conditions = hsva_conditions

    def matches(
            self,
            x: int,
            y: int,
            group_index: int,
            hue: Optional[float],
            saturation: Optional[float],
            value: Optional[float],
            alpha: Optional[float],
    ) -> bool:
        mask_condition: Optional[MaskCondition] = None
        if group_index in range(len(self.mask_conditions)):
            mask_condition = self.mask_conditions[group_index]
        if mask_condition is not None:
            coordinates = (x, y)
            return mask_condition(coordinates)
        else:
            hsva_conditions = self.hsva_conditions
            if hsva_conditions is None:
                return False
            else:
                return hsva_conditions.matches(hue=hue, saturation=saturation, value=value, alpha=alpha)


class RecolorDefinition:
    """Defines how to recolor a portion of an image."""

    def __init__(
            self,
            conditions: PixelMatchingConditions,
            new_hue: int,
            new_saturation: Optional[int] = None,
            value_offset: Optional[int] = None
    ):
        """
        new_hue is [0 - 360]
        new_saturation is [0 - 100] or None
        value_offset is [-100 - 100] or None
        """
        super().__init__()
        self.conditions = conditions
        self.new_hue = new_hue / 360.0
        self.new_saturation: Optional[float] = None
        self.value_offset: float = 0.0
        if new_saturation is not None:
            self.new_saturation = new_saturation / 100.0
        if value_offset is not None:
            self.value_offset = value_offset / 100.0 * 256.0


def make_matching_conditions(
        masks: list[Optional[ndarray]],
        hue_range: Optional[tuple[int, int]],
        saturation_range: Optional[tuple[int, int]],
        value_range: Optional[tuple[int, int]]
) -> PixelMatchingConditions:
    """
    Creates a PixelMatching object given masks and hue/saturation/value ranges.

    hue range [0 - 360] or None (can wrap around if desired, i.e. can go from 330 to 30)
    saturation range [0 - 100] or None
    value range [-100 - 100] or None
    """
    descriptions: list[str] = []

    hue_condition: Optional[ColorCondition] = None
    if hue_range is not None:
        hue_start, hue_end = hue_range
        hue_condition = _hue_in_range_condition(hue_start, hue_end)
        descriptions.append(f"h {hue_start}-{hue_end}")

    saturation_condition: Optional[ColorCondition] = None
    if saturation_range is not None:
        saturation_start, saturation_end = saturation_range
        saturation_condition = _saturation_in_range_condition(saturation_start, saturation_end)
        descriptions.append(f"s {saturation_start}-{saturation_end}")

    value_condition: Optional[ColorCondition] = None
    if value_range is not None:
        value_start, value_end = value_range
        value_condition = _value_in_range_condition(float(value_start), float(value_end))
        descriptions.append(f"v {value_start}-{value_end}")

    hsva_conditions: Optional[HsvaConditions] = None
    if hue_condition is not None or saturation_condition is not None or value_condition is not None:
        hue_condition = hue_condition if hue_condition is not None else _default_color_condition
        saturation_condition = saturation_condition if saturation_condition is not None else _default_color_condition
        value_condition = value_condition if value_condition is not None else _default_color_condition
        hsva_conditions = HsvaConditions(
            description=", ".join(descriptions),
            hue_condition=hue_condition,
            saturation_condition=saturation_condition,
            value_condition=value_condition,
            alpha_condition=_default_color_condition
        )
    return PixelMatchingConditions(masks=masks, hsva_conditions=hsva_conditions)


def recolor_image(rgb_array: ndarray, recolor_definitions: list[RecolorDefinition], group_index: int) -> ndarray:
    """Applies recoloring(s) configured in recolor_definitions to the image represented by rgb_array"""
    hsv_array = rgb_to_hsv(rgb_array)

    x_dimension, y_dimension, _ = hsv_array.shape
    for x in range(x_dimension):
        for y in range(y_dimension):
            hue: Optional[float] = hsv_array[x, y, _HUE_INDEX]
            saturation: Optional[float] = hsv_array[x, y, _SATURATION_INDEX]
            value: Optional[float] = hsv_array[x, y, _VALUE_INDEX]
            alpha: Optional[float] = hsv_array[x, y, _ALPHA_INDEX]
            for recolor_definition in recolor_definitions:
                matches = recolor_definition.conditions.matches(
                    x=x,
                    y=y,
                    group_index=group_index,
                    hue=hue,
                    saturation=saturation,
                    value=value,
                    alpha=alpha,
                )
                if matches:
                    hsv_array[x, y, _HUE_INDEX] = recolor_definition.new_hue

                    new_saturation = recolor_definition.new_saturation
                    if new_saturation is not None:
                        hsv_array[x, y, _SATURATION_INDEX] = new_saturation

                    hsv_array[x, y, _VALUE_INDEX] = hsv_array[x, y, _VALUE_INDEX] + recolor_definition.value_offset

                    break

    return hsv_to_rgb(hsv_array)


class TextureRecolorSettings:

    def __init__(self, raw_settings: dict[str, dict[str, str]]):
        super().__init__()
        self.raw_settings = raw_settings

    def settings_for_model(self, model_id: str) -> dict[str, str]:
        """Returns the settings for the specified model_id, creating an empty set if needed."""
        if model_id in self.raw_settings:
            return self.raw_settings[model_id]
        else:
            settings = {}
            self.raw_settings[model_id] = settings
            return settings

    def setting_for_area(self, model_id: str, area_id: str) -> str:
        """Returns the setting for the specified area_id of the specified model_id, returning VANILLA if missing."""
        model_settings = self.settings_for_model(model_id)
        if area_id in model_settings:
            return model_settings[area_id]
        else:
            return VANILLA

    def put_setting(self, model_id: str, area_id: str, setting: str):
        """Applies the specified setting for the specified area_id of the specified model_id."""
        self.settings_for_model(model_id)[area_id] = setting


class TextureRecolorizer:

    def __init__(self, settings: SeedSettings):
        super().__init__()
        self.settings = settings
        self.recolor_settings = TextureRecolorSettings(settings.get(settingkey.TEXTURE_RECOLOR_SETTINGS))

    @staticmethod
    def load_recolorable_models() -> list[dict[str, Any]]:
        """Returns a list of all recolorable models configured in the project."""
        recolors_path = Path(resource_path("static/recolors"))
        recolor_templates: list[Path] = []
        if recolors_path.is_dir():
            for file in os.listdir(recolors_path):
                _, extension = os.path.splitext(file)
                if extension == ".yml":
                    recolor_templates.append(recolors_path / file)

        result: list[dict[str, Any]] = []
        for recolor_template_path in recolor_templates:
            with open(recolor_template_path) as recolor_template_file:
                models = yaml.safe_load(recolor_template_file)
                if models is not None:
                    result.extend(models)

        return result

    @staticmethod
    def mask_file_to_mask(mask_file_path: Path) -> ndarray:
        """
        Decodes a mask file into ndarray [y, x] where the value is True for any pixels that are part of the mask.
        """
        with gzip.open(mask_file_path) as mask_file:
            first_line = mask_file.readline().decode()
            y_dimension_str, x_dimension_str = first_line.split(",")
            y_dimension = int(y_dimension_str)
            x_dimension = int(x_dimension_str)
            mask = np.zeros((y_dimension, x_dimension), dtype="bool")
            for y in range(y_dimension):
                line = mask_file.readline().decode()
                for x in range(x_dimension):
                    if line[x] != ' ':
                        mask[y, x] = True
            return mask

    @staticmethod
    def conditions_from_colorable_area(colorable_area: dict[str, Any]) -> PixelMatchingConditions:
        """Returns color conditions defined by properties of the specified colorable_area."""
        mask_files: Optional[list[str]] = colorable_area.get("mask_files")
        masks: list[Optional[ndarray]] = []
        if mask_files is not None:
            for mask_file_str in mask_files:
                mask_file_path = Path(resource_path(mask_file_str))
                if mask_file_path.is_file():
                    masks.append(TextureRecolorizer.mask_file_to_mask(mask_file_path))
                else:
                    masks.append(None)

        hue_start: Optional[int] = colorable_area.get("hue_start")
        hue_end: Optional[int] = colorable_area.get("hue_end")
        hue_range: Optional[tuple[int, int]] = None
        if hue_start is not None and hue_end is not None:
            hue_range = (hue_start, hue_end)

        saturation_start: Optional[int] = colorable_area.get("saturation_start")
        saturation_end: Optional[int] = colorable_area.get("saturation_end")
        saturation_range: Optional[tuple[int, int]] = None
        if saturation_start is not None and saturation_end is not None:
            saturation_range = (saturation_start, saturation_end)

        value_start: Optional[int] = colorable_area.get("value_start")
        value_end: Optional[int] = colorable_area.get("value_end")
        value_range: Optional[tuple[int, int]] = None
        if value_start is not None and value_end is not None:
            value_range = (value_start, value_end)

        return make_matching_conditions(
            masks=masks,
            hue_range=hue_range,
            saturation_range=saturation_range,
            value_range=value_range
        )

    def recolor_textures(self) -> list[Asset]:
        """Returns a list of mod assets (if any) that recolor textures based on settings."""
        assets: list[Asset] = []

        if not self.settings.get(settingkey.RECOLOR_TEXTURES):
            return assets

        base_path = appconfig.extracted_data_path() / "kh2"
        if not base_path.is_dir():
            print(f"Could not find extracted data at {base_path} - not recoloring textures")
            return assets

        recolorable_models = self.load_recolorable_models()
        if len(recolorable_models) == 0:
            print("Could not find any recolor templates - not recoloring textures")
            return assets

        recolors_cache_folder = Path("cache/texture-recolors")
        if recolors_cache_folder.is_dir():
            if not self.settings.get(settingkey.RECOLOR_TEXTURES_KEEP_CACHE):
                shutil.rmtree(recolors_cache_folder)

        for model in recolorable_models:
            model_id: str = model["id"]

            model_version: int = model.get("version", 1)
            model_version_suffix = ""
            if model_version > 1:
                model_version_suffix = f"-v{model_version}"

            available_image_group_ids: list[str] = _available_group_ids()
            model_cache_folder = recolors_cache_folder / model_id

            for recolor in model["recolors"]:
                colorable_areas: list[dict[str, Any]] = recolor["colorable_areas"]

                recolor_definitions: list[RecolorDefinition] = []
                chosen_filename_hues: list[str] = []

                for colorable_area in colorable_areas:
                    chosen_hue = self._choose_hue(model_id=model_id, colorable_area=colorable_area)
                    if chosen_hue < 0:  # Keep it vanilla
                        chosen_filename_hues.append("v")
                        continue

                    chosen_filename_hues.append(str(chosen_hue))

                    recolor_definition = RecolorDefinition(
                        conditions=self.conditions_from_colorable_area(colorable_area),
                        new_hue=chosen_hue,
                        new_saturation=colorable_area.get("new_saturation"),
                        value_offset=colorable_area.get("value_offset")
                    )
                    recolor_definitions.append(recolor_definition)

                image_groups: list[list[str]] = recolor["image_groups"]
                for index, group in enumerate(image_groups):
                    # Each group gets a unique ID
                    group_id = available_image_group_ids.pop(0)

                    if len(recolor_definitions) == 0:
                        # Everything was vanilla for this group, can save a little time and space by doing nothing
                        # (but we still need the pop above to make sure the group IDs still line up)
                        continue

                    combined_hues = "-".join(chosen_filename_hues)
                    _, image_ext = os.path.splitext(group[0])
                    destination_file_name = f"{model_id}{model_version_suffix}-{group_id}-{combined_hues}{image_ext}"
                    destination_path = model_cache_folder / destination_file_name

                    asset: Asset = {
                        "platform": "pc",
                        "name": group[0]
                    }
                    if len(group) > 1:
                        asset["multi"] = [{"name": image} for image in group[1:]]
                    asset["method"] = "copy"
                    asset["source"] = [
                        {"name": f"{destination_path.absolute()}"}
                    ]
                    assets.append(asset)

                    if destination_path.is_file():
                        if version.debug_mode():
                            print(f"Already generated texture recolor for {destination_path}")
                        continue

                    if version.debug_mode():
                        print(f"Generating texture recolor for {destination_path}")

                    destination_path.parent.mkdir(parents=True, exist_ok=True)

                    # Just use the first one as the canonical representation
                    with Image.open(Path(base_path) / group[0]) as original_image:
                        image_array = np.array(original_image.convert("RGBA"))
                        recolored_array = recolor_image(image_array, recolor_definitions, group_index=index)
                        with Image.fromarray(recolored_array, "RGBA") as new_image:
                            new_image.save(destination_path)

        return assets

    def _choose_hue(self, model_id: str, colorable_area: dict[str, Any]) -> int:
        """Returns the hue to use for the colorable area, or -1 to leave vanilla."""
        recolor_settings = self.recolor_settings
        area_setting = recolor_settings.setting_for_area(model_id, colorable_area["id"])
        if area_setting == VANILLA:
            return -1
        elif area_setting == RANDOM:
            if "new_saturation" in colorable_area:
                # Want to leave the opportunity there for it to "roll vanilla" which wouldn't otherwise be possible
                # with the application of a new saturation
                return random.choice([-1] + available_random_hues)
            else:
                return random.choice(available_random_hues)
        else:
            return int(area_setting)


def _make_mask_condition(mask: Optional[ndarray]) -> Optional[MaskCondition]:
    if mask is None:
        return None
    else:
        # NOTE: The bool() function call is to convert the numpy bool_ type to normal bool
        return lambda coordinates: bool(mask[coordinates[0], coordinates[1]])


def _hue_in_range_condition(hue_start: float, hue_end: float) -> ColorCondition:
    start_ratio = hue_start / 360.0
    end_ratio = hue_end / 360.0
    if start_ratio > end_ratio:
        return lambda hue_value: hue_value >= start_ratio or hue_value <= end_ratio
    else:
        return lambda hue_value: start_ratio <= hue_value <= end_ratio


def _saturation_in_range_condition(saturation_start: float, saturation_end: float) -> ColorCondition:
    start_ratio = saturation_start / 100.0
    end_ratio = saturation_end / 100.0
    return lambda saturation_value: start_ratio <= saturation_value <= end_ratio


def _value_in_range_condition(value_start: float, value_end: float) -> ColorCondition:
    # Of note: looks like value isn't a 0-1 like the others, just seems to go 0-256?
    adjusted_start = value_start / 100.0 * 256.0
    adjusted_end = value_end / 100.0 * 256.0
    return lambda value_value: adjusted_start <= value_value <= adjusted_end


def _available_group_ids() -> list[str]:
    # Gives us a-z, aa-az, ba-bz, and so on - should be more than enough
    ascii_characters = string.ascii_lowercase
    result: list[str] = [c for c in ascii_characters]
    for c in ascii_characters:
        result.extend(f"{c}{c2}" for c2 in ascii_characters)
    return result

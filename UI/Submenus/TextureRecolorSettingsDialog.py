import json
import os
import string
import textwrap
import time
from pathlib import Path
from typing import Any

import numpy
from PIL import Image
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QDialog, QMenuBar, QMenu, QComboBox, QSpinBox, QLabel, QVBoxLayout, QHBoxLayout, \
    QInputDialog, QLineEdit

from Class import settingkey
from Class.seedSettings import SeedSettings
from Module import texture, appconfig
from Module.cosmetics import CosmeticsMod
from Module.texture import TextureRecolorSettings, TextureRecolorizer, recolor_image, RecolorDefinition
from UI.Submenus.SubMenu import KH2Submenu


_model_tags_by_category_name = {
    "Characters": "character",
    "Heartless": "heartless",
    "Nobodies": "nobody",
    "Environment": "environment",
    "Effects": "effects",
}


class TextureRecolorSettingsDialog(QDialog):

    def __init__(self, seed_settings: SeedSettings):
        super().__init__()
        self.setWindowTitle("Texture Recolor Settings")

        self.seed_settings = seed_settings
        self.texture_recolor_settings = TextureRecolorSettings(seed_settings.get(settingkey.TEXTURE_RECOLOR_SETTINGS))

        self.base_path = CosmeticsMod.extracted_data_path() / "kh2"
        if not self.base_path.is_dir():
            # Really shouldn't be able to get here without something weird going on, just note it and return
            print(f"Could not find extracted data at {self.base_path}")
            return

        all_models = TextureRecolorizer.load_recolorable_models()
        if len(all_models) == 0:
            # Also really shouldn't be possible since these are bundled with the generator
            print(f"No recolorable models found")
            return

        menu_bar = QMenuBar()
        presets_menu = QMenu("Presets")
        presets_menu.addAction("All Vanilla", self._all_vanilla_preset)
        presets_menu.addAction("All Random", self._all_random_preset)
        presets_menu.addAction("Randomize Party Members Only", self._random_party_only)
        presets_menu.addSeparator()
        presets_menu.addAction("Open Preset Folder", self._open_preset_folder)
        presets_menu.addAction("Save Settings as New Preset", self._save_preset)
        presets_menu.addSeparator()
        presets_folder = self._texture_recolors_presets_folder()
        if presets_folder.is_dir():
            for file in os.listdir(presets_folder):
                preset_name, extension = os.path.splitext(file)
                if extension == ".json":
                    presets_menu.addAction(preset_name, self._make_apply_preset(preset_name))
        menu_bar.addMenu(presets_menu)

        category_menu = QMenu("Category")
        category_menu.addAction("All in Category to Vanilla", self._all_in_category_to_vanilla)
        category_menu.addAction("All in Category to Random", self._all_in_category_to_random)
        menu_bar.addMenu(category_menu)

        model_menu = QMenu("Model")
        model_menu.addAction("All in Model to Vanilla", self._all_in_model_to_vanilla)
        model_menu.addAction("All in Model to Random", self._all_in_model_to_random)
        menu_bar.addMenu(model_menu)

        category_picker = QComboBox()
        category_picker.setToolTip("Chooses a category of items to choose for recoloring.")
        category_picker.setMinimumWidth(200)
        self.category_picker = category_picker
        model_picker = QComboBox()
        model_picker.setToolTip("Chooses which model to recolor.")
        model_picker.setMinimumWidth(200)
        self.model_picker = model_picker
        area_picker = QComboBox()
        area_picker.setToolTip("Chooses which area to recolor.")
        area_picker.setMinimumWidth(200)
        self.area_picker = area_picker
        setting_picker = QComboBox()
        setting_picker_tooltip_text = textwrap.dedent('''
            Chooses how to color the selected color area of the selected model.

            Vanilla - do not recolor this area
            Randomized - choose a random color for this area (different for every seed)
            Custom - use a specific color for this area (based on the Color Hue field)
        ''')
        setting_picker.setToolTip(setting_picker_tooltip_text)
        self.setting_picker = setting_picker
        hue_picker = QSpinBox()
        hue_picker_tooltip_text = textwrap.dedent('''
            Chooses the color hue (0-360) to use to color the selected color area of the selected model.

            Only applicable when the color Setting is Custom.

            General estimates of hue values:
            0 - Red
            60 - Yellow
            120 - Green
            180 - Cyan
            240 - Blue
            270 - Purple
            330 - Pink
        ''')
        hue_picker.setToolTip(hue_picker_tooltip_text)
        hue_picker.setRange(0, 355)
        hue_picker.setSingleStep(5)
        self.hue_picker = hue_picker
        base_image = QLabel()
        base_image.setScaledContents(True)
        base_image.setFixedSize(320, 320)
        self.base_image = base_image
        recolored_image = QLabel()
        recolored_image.setScaledContents(True)
        recolored_image.setFixedSize(320, 320)
        self.recolored_image = recolored_image

        category_picker.addItems(_model_tags_by_category_name.keys())
        category_picker.currentIndexChanged.connect(self._category_changed)
        model_picker.currentIndexChanged.connect(self._model_changed)
        area_picker.currentIndexChanged.connect(self._update_ui_for_selected_area)

        setting_picker.addItems(["Vanilla", "Randomized", "Custom"])
        setting_picker.currentIndexChanged.connect(self._setting_changed)

        hue_picker.valueChanged.connect(self._setting_changed)

        main = QVBoxLayout()
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(menu_bar)

        submenu_layout = KH2Submenu("Texture Recolor Settings", seed_settings)
        submenu_layout.start_column()
        submenu_layout.start_group()
        submenu_layout.add_labeled_widget(category_picker, "Category")
        submenu_layout.add_labeled_widget(model_picker, "Model")
        submenu_layout.add_labeled_widget(area_picker, "Area")
        submenu_layout.end_group("Area to Color")
        submenu_layout.end_column()

        submenu_layout.start_column()
        submenu_layout.start_group()
        submenu_layout.add_labeled_widget(setting_picker, "Setting")
        submenu_layout.add_labeled_widget(hue_picker, "Color Hue")
        submenu_layout.end_group("Color to Use")
        submenu_layout.end_column()
        submenu_layout.finalizeMenu()

        main.addWidget(submenu_layout)

        images_layout = QHBoxLayout()
        images_layout.setContentsMargins(16, 0, 16, 16)

        base_image_layout = QHBoxLayout()
        base_image_layout.setContentsMargins(8, 8, 8, 8)
        base_image_layout.addWidget(base_image)
        images_layout.addWidget(KH2Submenu.make_styled_frame(base_image_layout, 2, "Original Texture Sample"))
        preview_image_layout = QHBoxLayout()
        preview_image_layout.setContentsMargins(8, 8, 8, 8)
        preview_image_layout.addWidget(recolored_image)
        images_layout.addWidget(KH2Submenu.make_styled_frame(preview_image_layout, 3, "Recolored Preview"))
        main.addLayout(images_layout)

        self.setLayout(main)

        self.all_models = TextureRecolorizer.load_recolorable_models()
        self._category_changed()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._new_random_color)
        self.timer.start(5000)

    def _category_changed(self):
        selected_category = _model_tags_by_category_name[self.category_picker.currentText()]

        sorted_model_names: list[str] = []
        models_by_name: dict[str, dict[str, Any]] = {}
        for model in self.all_models:
            if selected_category not in model["tags"]:
                continue
            name = model["name"]
            sorted_model_names.append(name)
            models_by_name[name] = model
        sorted_model_names.sort()
        self.model_names = sorted_model_names
        self.models_by_name = models_by_name

        self.model_picker.clear()
        self.model_picker.addItems(sorted_model_names)
        self._model_changed()

    def _model_changed(self):
        selected_model = self._selected_model()

        area_names: list[str] = []
        recolors_by_area_name: dict[str, dict[str, Any]] = {}
        for recolor in selected_model["recolors"]:
            for colorable_area in recolor["colorable_areas"]:
                area_name = colorable_area["name"]
                area_names.append(area_name)
                recolors_by_area_name[area_name] = recolor
        area_names.sort()
        self.area_names = area_names
        self.recolors_by_area_name = recolors_by_area_name

        self.area_picker.clear()
        self.area_picker.addItems(area_names)
        self._update_ui_for_selected_area()

    def _setting_changed(self):
        selected_setting = self.setting_picker.currentIndex()
        if selected_setting == 0:
            setting_string = texture.VANILLA
            self.hue_picker.setEnabled(False)
        elif selected_setting == 1:  # Random
            setting_string = texture.RANDOM
            self.hue_picker.setEnabled(False)
        else:  # Custom
            chosen_hue = self.hue_picker.value()
            setting_string = str(chosen_hue)
            self.hue_picker.setEnabled(True)

        self.texture_recolor_settings.put_setting(
            model_id=self._selected_model()["id"],
            area_id=self._selected_colorable_area()["id"],
            setting=setting_string
        )
        self._update_preview()

    def _update_preview(self):
        selected_area = self._selected_colorable_area()
        recolor = self.recolors_by_area_name[selected_area["name"]]
        # Just pick one of the images to show as the preview
        image_groups: list[list[str]] = recolor["image_groups"]
        full_path = self.base_path / image_groups[0][0]
        with Image.open(full_path) as base_image:
            self.base_image.setPixmap(base_image.toqpixmap())

        setting = self.texture_recolor_settings.setting_for_area(
            model_id=self._selected_model()["id"],
            area_id=selected_area["id"]
        )
        if setting == texture.VANILLA:
            with Image.open(full_path) as base_image:
                self.recolored_image.setPixmap(base_image.toqpixmap())
            return
        elif setting == texture.RANDOM:
            available_random_hues = texture.available_random_hues
            conditions = TextureRecolorizer.conditions_from_colorable_area(selected_area)
            chosen_hue = available_random_hues[int(time.time()) % len(available_random_hues)]
            new_saturation = selected_area.get("new_saturation")
            value_offset = selected_area.get("value_offset")
            recolor_definitions = [RecolorDefinition(conditions, chosen_hue, new_saturation, value_offset)]
        else:  # Custom
            custom_hue = self.hue_picker.value()
            conditions = TextureRecolorizer.conditions_from_colorable_area(selected_area)
            new_saturation = selected_area.get("new_saturation")
            value_offset = selected_area.get("value_offset")
            recolor_definitions = [RecolorDefinition(conditions, custom_hue, new_saturation, value_offset)]

        with Image.open(full_path) as source_image:
            image_array = numpy.array(source_image)
        with Image.fromarray(recolor_image(image_array, recolor_definitions), "RGBA") as recolored_image:
            self.recolored_image.setPixmap(recolored_image.toqpixmap())

    def _selected_model(self) -> dict[str, Any]:
        selected_model_name = self.model_names[self.model_picker.currentIndex()]
        return self.models_by_name[selected_model_name]

    def _selected_colorable_area(self) -> dict[str, Any]:
        selected_area_name = self.area_names[self.area_picker.currentIndex()]
        recolor = self.recolors_by_area_name[selected_area_name]
        colorable_area = next((x for x in recolor["colorable_areas"] if selected_area_name == x["name"]), None)
        return colorable_area

    def _update_ui_for_selected_area(self):
        setting = self.texture_recolor_settings.setting_for_area(
            model_id=self._selected_model()["id"],
            area_id=self._selected_colorable_area()["id"]
        )
        if setting == texture.VANILLA:
            self.setting_picker.setCurrentIndex(0)
            self.hue_picker.setEnabled(False)
        elif setting == texture.RANDOM:
            self.setting_picker.setCurrentIndex(1)
            self.hue_picker.setEnabled(False)
        else:
            self.setting_picker.setCurrentIndex(2)
            self.hue_picker.setValue(int(setting))
            self.hue_picker.setEnabled(True)
        self._update_preview()

    @staticmethod
    def _texture_recolors_presets_folder() -> Path:
        return Path(appconfig.PRESET_FOLDER).absolute() / "texture-recolors"

    @staticmethod
    def _open_preset_folder():
        os.startfile(TextureRecolorSettingsDialog._texture_recolors_presets_folder())

    def _save_preset(self):
        preset_name, ok = QInputDialog.getText(
            self,
            'Make New Preset', 'Enter a name for your preset...',
            QLineEdit.EchoMode.Normal
        )
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        preset_name = ''.join(c for c in preset_name if c in valid_chars)
        if ok:
            presets_folder = self._texture_recolors_presets_folder()
            presets_folder.mkdir(parents=True, exist_ok=True)
            with open(presets_folder / f"{preset_name}.json", "w", encoding="utf-8") as preset_file:
                json.dump(self.texture_recolor_settings.raw_settings, preset_file, indent=4, sort_keys=True)

    def _all_vanilla_preset(self):
        self._apply_setting_to_models(self.all_models, texture.VANILLA)

    def _all_random_preset(self):
        self._apply_setting_to_models(self.all_models, texture.RANDOM)

    def _all_in_category_to_vanilla(self):
        self._apply_setting_to_models([model for _, model in self.models_by_name.items()], texture.VANILLA)

    def _all_in_category_to_random(self):
        self._apply_setting_to_models([model for _, model in self.models_by_name.items()], texture.RANDOM)

    def _all_in_model_to_vanilla(self):
        self._apply_setting_to_models([self._selected_model()], texture.VANILLA)

    def _all_in_model_to_random(self):
        self._apply_setting_to_models([self._selected_model()], texture.RANDOM)

    def _random_party_only(self):
        for recolorable_model in self.all_models:
            model_id = recolorable_model["id"]
            recolors = recolorable_model["recolors"]
            tags = recolorable_model["tags"]
            setting = texture.VANILLA
            if "party" in tags:
                setting = texture.RANDOM
            for recolor in recolors:
                for colorable_area in recolor["colorable_areas"]:
                    area_id = colorable_area["id"]
                    self.texture_recolor_settings.put_setting(model_id, area_id, setting)
        self._update_ui_for_selected_area()

    def _apply_setting_to_models(self, recolorable_models: list[dict[str, Any]], setting: str):
        for recolorable_model in recolorable_models:
            model_id = recolorable_model["id"]
            recolors = recolorable_model["recolors"]
            for recolor in recolors:
                for colorable_area in recolor["colorable_areas"]:
                    area_id = colorable_area["id"]
                    self.texture_recolor_settings.put_setting(model_id, area_id, setting)
        self._update_ui_for_selected_area()

    def _make_apply_preset(self, preset_name: str):
        return lambda: self._apply_preset(preset_name)

    def _apply_preset(self, preset_name: str):
        preset_file_path = self._texture_recolors_presets_folder() / f"{preset_name}.json"
        if preset_file_path.is_file():
            with open(preset_file_path, encoding="utf-8") as preset_file:
                loaded_settings: dict[str, dict[str, str]] = json.load(preset_file)

        live_settings = self.texture_recolor_settings
        for model_id, model_settings in loaded_settings.items():
            for area_id, setting in model_settings.items():
                live_settings.put_setting(model_id, area_id, setting)
        self._update_ui_for_selected_area()

    def _new_random_color(self):
        selected_setting = self.setting_picker.currentIndex()
        if selected_setting == 1:
            self._update_preview()

    def closeEvent(self, e):
        self.timer.stop()

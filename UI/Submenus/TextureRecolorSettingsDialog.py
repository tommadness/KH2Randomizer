import json
import os
import random
import shutil
import string
import textwrap
import time
from pathlib import Path
from typing import Any

import numpy
from PIL import Image
from PySide6.QtWidgets import QDialog, QMenuBar, QMenu, QComboBox, QSpinBox, QLabel, QVBoxLayout, QHBoxLayout, \
    QInputDialog, QLineEdit, QFileDialog, QMessageBox

from Class import settingkey
from Class.seedSettings import SeedSettings
from Module import appconfig
from Module.cosmeticsmods import texture
from Module.cosmeticsmods.texture import TextureRecolorSettings, TextureRecolorizer, recolor_image, RecolorDefinition, \
    TextureConditionsLoader
from UI.Submenus.SubMenu import KH2Submenu
from UI.qtlib import button

_model_tags_by_category_name = {
    "Characters": "character",
    "Heartless": "heartless",
    "Nobodies": "nobody",
    "Environment": "environment",
    "Effects": "effects",
    "Interface": "interface",
}


class TextureRecolorSettingsDialog(QDialog):

    def __init__(self, seed_settings: SeedSettings):
        super().__init__()
        self.setWindowTitle("Texture Recolor Settings")

        self.seed_settings = seed_settings
        self.texture_recolor_settings = TextureRecolorSettings(seed_settings.get(settingkey.TEXTURE_RECOLOR_SETTINGS))
        self.conditions_loader = TextureConditionsLoader()

        self.base_path = appconfig.extracted_game_path("kh2")
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
        presets_menu.addAction("Randomize Most Relevant", self._randomize_baseline)
        presets_menu.addSeparator()
        custom_presets_menu = QMenu("Load a Preset")
        presets_menu.addMenu(custom_presets_menu)
        self.custom_presets_menu = custom_presets_menu
        self._rebuild_custom_presets_menu()
        presets_menu.addAction("Open Preset Folder", self._open_preset_folder)
        presets_menu.addAction("Import Preset", self._import_preset)
        presets_menu.addAction("Save Settings as New Preset", self._save_preset)
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

        base_images: list[QLabel] = []
        for _ in range(8):
            base_image = QLabel()
            base_image.setScaledContents(True)
            base_image.setFixedSize(160, 160)
            base_images.append(base_image)
        self.base_images = base_images

        recolored_images: list[QLabel] = []
        for _ in range(8):
            recolored_image = QLabel()
            recolored_image.setScaledContents(True)
            recolored_image.setFixedSize(160, 160)
            recolored_images.append(recolored_image)
        self.recolored_images = recolored_images

        category_picker.addItems(_model_tags_by_category_name.keys())
        category_picker.currentIndexChanged.connect(self._category_changed)
        model_picker.currentIndexChanged.connect(self._model_changed)
        area_picker.currentIndexChanged.connect(self._update_ui_for_selected_area)

        setting_picker.addItems(["Vanilla", "Randomized", "Custom"])
        setting_picker.currentIndexChanged.connect(self._setting_changed)

        hue_picker.valueChanged.connect(self._setting_changed)

        reroll_button = button("Refresh Preview(s) (can take awhile)", self._update_preview)

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

        submenu_layout.start_column()
        submenu_layout.start_group()
        submenu_layout.add_option(settingkey.RECOLOR_TEXTURES_INCLUDE_EXTRAS)
        submenu_layout.add_option(settingkey.RECOLOR_TEXTURES_KEEP_CACHE)
        submenu_layout.add_option(settingkey.RECOLOR_TEXTURES_COMPRESS)
        submenu_layout.pending_group.addWidget(reroll_button)
        submenu_layout.end_group("Other")
        submenu_layout.end_column()
        submenu_layout.finalizeMenu()

        main.addWidget(submenu_layout)

        base_image_layout = QHBoxLayout()
        base_image_layout.setContentsMargins(8, 8, 8, 8)
        for base_image in base_images:
            base_image_layout.addWidget(base_image)
        preview_image_layout = QHBoxLayout()
        preview_image_layout.setContentsMargins(8, 8, 8, 8)
        for recolored_image in recolored_images:
            preview_image_layout.addWidget(recolored_image)
        main.addWidget(KH2Submenu.make_styled_frame(base_image_layout, 2, "Original Texture(s)"))
        main.addWidget(KH2Submenu.make_styled_frame(preview_image_layout, 3, "Recolored Preview(s)"))

        self.setLayout(main)

        self.all_models = TextureRecolorizer.load_recolorable_models()
        self._category_changed()

    def _rebuild_custom_presets_menu(self):
        menu = self.custom_presets_menu
        menu.clear()
        presets_folder = TextureRecolorSettings.texture_recolors_presets_folder()
        if presets_folder.is_dir():
            for file in os.listdir(presets_folder):
                preset_name, extension = os.path.splitext(file)
                if extension == ".json":
                    menu.addAction(preset_name, self._make_apply_preset(preset_name))

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

    def _update_preview(self):
        model_id = self._selected_model()["id"]
        recolor = self.recolors_by_area_name[self._selected_colorable_area()["name"]]

        colorable_areas: list[dict[str, Any]] = recolor["colorable_areas"]
        recolor_definitions: list[RecolorDefinition] = []
        random_hue_index = int(time.time())
        for colorable_area in colorable_areas:
            area_id = colorable_area["id"]
            setting = self.texture_recolor_settings.setting_for_area(model_id=model_id, area_id=area_id)

            if setting == texture.VANILLA:
                continue
            elif setting == texture.RANDOM:
                available_random_hues = texture.available_random_hues
                random_hue_count = len(available_random_hues)
                chosen_hue = available_random_hues[random_hue_index % random_hue_count]
                random_hue_index = random_hue_index + random.randint(0, random_hue_count)
            else:  # Custom
                chosen_hue = int(setting)

            conditions = self.conditions_loader.conditions_from_colorable_area(
                model_id=model_id,
                area_id=area_id,
                colorable_area=colorable_area
            )
            new_saturation = colorable_area.get("new_saturation")
            value_offset = colorable_area.get("value_offset")
            recolor_definitions.append(RecolorDefinition(conditions, chosen_hue, new_saturation, value_offset))

        image_groups: list[dict[str, Any]] = recolor["image_groups"]
        preview_images: list[bool] = recolor.get("previews", [True] * len(image_groups))

        preview_count = len(self.base_images)

        for index in range(preview_count):
            self.base_images[index].clear()
            self.recolored_images[index].clear()

        current_preview = 0
        for group_index in range(len(image_groups)):
            if not preview_images[group_index]:
                continue

            group = image_groups[group_index]
            group_images: list[str] = group["images"]

            full_path = self.base_path / group_images[0]
            with Image.open(full_path) as base_image:
                self.base_images[current_preview].setPixmap(base_image.toqpixmap())

            with Image.open(full_path) as source_image:
                image_array = numpy.array(source_image.convert("RGBA"))
            recolored_array = recolor_image(image_array, recolor_definitions, group_index=group_index)
            with Image.fromarray(recolored_array, "RGBA") as recolored_image:
                self.recolored_images[current_preview].setPixmap(recolored_image.toqpixmap())

            current_preview = current_preview + 1

            if current_preview == preview_count:
                break

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

    @staticmethod
    def _open_preset_folder():
        os.startfile(TextureRecolorSettings.texture_recolors_presets_folder())

    def _import_preset(self):
        file_dialog = QFileDialog(self)
        outfile_name, _ = file_dialog.getOpenFileName(self, filter="Texture Recolor Preset (*.json)")
        if outfile_name:
            outfile = Path(outfile_name)
            preset_name = outfile.stem
            shutil.copy2(outfile, TextureRecolorSettings.texture_recolors_presets_folder())
            self._rebuild_custom_presets_menu()
            response = QMessageBox.question(
                self,
                "Presets",
                f"Preset [{preset_name}] imported.\n\nUse it now?",
                QMessageBox.Yes, QMessageBox.No
            )
            if response == QMessageBox.Yes:
                self._apply_preset(preset_name)

    def _save_preset(self):
        preset_name, ok = QInputDialog.getText(
            self,
            'Make New Preset', 'Enter a name for your preset...',
            QLineEdit.EchoMode.Normal
        )
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        preset_name = ''.join(c for c in preset_name if c in valid_chars)
        if ok:
            presets_folder = TextureRecolorSettings.texture_recolors_presets_folder()
            presets_folder.mkdir(parents=True, exist_ok=True)
            with open(presets_folder / f"{preset_name}.json", "w", encoding="utf-8") as preset_file:
                json.dump(self.texture_recolor_settings.raw_settings, preset_file, indent=4, sort_keys=True)
            self._rebuild_custom_presets_menu()

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

    def _randomize_specific_tag(self, target_tag: str):
        for recolorable_model in self.all_models:
            model_id = recolorable_model["id"]
            recolors = recolorable_model["recolors"]
            tags = recolorable_model["tags"]
            if target_tag not in tags:
                continue
            for recolor in recolors:
                for colorable_area in recolor["colorable_areas"]:
                    area_id = colorable_area["id"]
                    self.texture_recolor_settings.put_setting(model_id, area_id, texture.RANDOM)
        self._update_ui_for_selected_area()

    def _randomize_baseline(self):
        self._randomize_specific_tag(target_tag="baseline")

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
        preset_file_path = TextureRecolorSettings.texture_recolors_presets_folder() / f"{preset_name}.json"
        if preset_file_path.is_file():
            with open(preset_file_path, encoding="utf-8") as preset_file:
                loaded_settings: dict[str, dict[str, str]] = json.load(preset_file)

        live_settings = self.texture_recolor_settings
        for model_id, model_settings in loaded_settings.items():
            for area_id, setting in model_settings.items():
                live_settings.put_setting(model_id, area_id, setting)
        self._update_ui_for_selected_area()

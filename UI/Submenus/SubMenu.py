import os
import random
from typing import Optional

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDoubleSpinBox, QFrame, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QListWidget,
    QPushButton, QSpinBox, QWidget, QVBoxLayout, QAbstractItemView, QRadioButton
)

import Class.seedSettings
from Class.seedSettings import MultiSelectTristate, ProgressionChainSelect, SeedSettings, Toggle, IntSpinner, FloatSpinner, SingleSelect, MultiSelect
from Module.resources import resource_path

class ProgressionWidget(QWidget):
    def __init__(self, settings, setting_name):
        super().__init__()
        self.settings = settings
        self.setting_name = setting_name
        setting: ProgressionChainSelect = Class.seedSettings.settings_by_name[setting_name]

        self.world_options = setting.progression.get_world_options()

        self.full_layout = QVBoxLayout()

        self.world_name_layout = QHBoxLayout()
        self.world_cp_name_layout = QHBoxLayout()
        self.world_cp_value_layout = QHBoxLayout()

        # make a combo box for worlds
        self.world_select = QComboBox()
        self.world_select.addItems(self.world_options)
        # self.world_select.lineEdit().setReadOnly(True)
        self.world_select.currentIndexChanged.connect(lambda index: self._change_visibility(self.world_options[index]))
        self.world_name_layout.addWidget(self.world_select)

        self.tier2_selects = {}
        self.tier3_selects = {}
        for w in self.world_options:
            self.tier3_selects[w] = []
            world_cp_select_labels = []
            for w_cp_index in range(setting.progression.get_num_cp_for_world(w)):
                world_cp_select_labels.append(setting.progression.get_cp_label_for_world(w,w_cp_index))
                spin_box = QSpinBox()
                spin_box.setRange(0,7)
                spin_box.setSingleStep(1)
                spin_box.setValue(setting.progression.get_cp_for_world(w,w_cp_index))
                spin_box.valueChanged.connect(lambda value, world=w,world_cp=w_cp_index: self._change_setting(world,world_cp,value))
                # spin_box.lineEdit().setReadOnly(True)
                self.tier3_selects[w].append(spin_box)
                self.world_cp_value_layout.addWidget(spin_box)
            world_cp_select_box = QComboBox()
            world_cp_select_box.addItems(world_cp_select_labels)
            world_cp_select_box.setCurrentIndex(0)
            world_cp_select_box.currentIndexChanged.connect(lambda index,world=w: self._change_visibility_again(world,index))
            # world_cp_select_box.lineEdit().setReadOnly(True)
            self.tier2_selects[w] = world_cp_select_box
            self.world_cp_name_layout.addWidget(world_cp_select_box)
    
        world_name_widget = QWidget()
        world_name_widget.setLayout(self.world_name_layout)
        world_cp_name_widget = QWidget()
        world_cp_name_widget.setLayout(self.world_cp_name_layout)
        world_cp_value_widget = QWidget()
        world_cp_value_widget.setLayout(self.world_cp_value_layout)
        self.full_layout.addWidget(world_name_widget)
        self.full_layout.addWidget(world_cp_name_widget)
        self.full_layout.addWidget(world_cp_value_widget)

        self.world_select.setCurrentIndex(1)
        self.world_select.setCurrentIndex(0)

        self.setLayout(self.full_layout)
    
    def _change_setting(self,world,world_cp,value):
        setting: ProgressionChainSelect = Class.seedSettings.settings_by_name[self.setting_name]
        setting.progression.set_cp_for_world(world,world_cp,value)
        self.settings.set(self.setting_name,setting.progression.get_compressed())

    def _change_visibility(self,selected_world):
        for w in self.tier2_selects:
            self.tier2_selects[w].setVisible(w==selected_world)
        self._change_visibility_again(selected_world,0)

    def _change_visibility_again(self,selected_world,selected_cp_index):
        # only change visibility of tier 3
        for w in self.tier3_selects:
            for s in self.tier3_selects[w]:
                s.setVisible(False)
        self.tier3_selects[selected_world][selected_cp_index].setVisible(True)


class KH2Submenu(QWidget):

    def __init__(self, title: str, in_layout="vertical", settings: SeedSettings = None):
        super().__init__()

        self.title = title
        self.settings = settings
        self.widgets_and_settings_by_name = {}

        if in_layout == "vertical":
            self.menulayout = QVBoxLayout()
        if in_layout == "horizontal":
            self.menulayout = QHBoxLayout()

        self.pending_column: Optional[QVBoxLayout] = None
        self.pending_group: Optional[QVBoxLayout] = None

        self.tristate_groups = {}
        self.tristate_backgrounds = {}

        self.random_header_styles = [
            'background: #4d0d0e; color: #ff8080;',  # reds
            'background: #685901; color: #fff34b;',  # yellows
            'background: #04641b; color: #31f626;',  # greens
            'background: #032169; color: #63c6f5;',  # blues
            'background: #422169; color: #c663f5;',  # purples
        ]
        self.next_header_style = random.randint(0, len(self.random_header_styles) - 1)

    def start_column(self):
        self.pending_column = QVBoxLayout()
        self.pending_column.setContentsMargins(0, 0, 0, 0)

    def end_column(self, stretch_at_end=True):
        if stretch_at_end:
            self.pending_column.addStretch()
        column_widget = QWidget()
        column_widget.setLayout(self.pending_column)
        self.menulayout.addWidget(column_widget)
        self.menulayout.addSpacing(8)
        self.pending_column = None

    def start_group(self):
        self.pending_group = QVBoxLayout()
        self.pending_group.setContentsMargins(8, 0, 8, 0)

    def end_group(self, title=''):
        group = QVBoxLayout()
        group.setContentsMargins(0, 0, 0, 0)

        header_style_choice = self.next_header_style % len(self.random_header_styles)
        self.next_header_style = self.next_header_style + 1

        if title != '':
            title_label = QLabel(title)
            title_label.setContentsMargins(8, 8, 8, 8)
            title_label.setProperty('cssClass', 'groupHeader')
            title_label.setStyleSheet(self.random_header_styles[header_style_choice])
            group.addWidget(title_label)

        group.addLayout(self.pending_group)

        frame = QFrame()
        if title == '':
            frame.setContentsMargins(0, 8, 0, 8)
        else:
            frame.setContentsMargins(0, 0, 0, 8)
        frame.setProperty('cssClass', 'settingsFrame')
        frame.setLayout(group)

        self.pending_column.addWidget(frame)
        self.pending_group = None

    def _add_option_widget(self, label_text: str, tooltip: str, option):
        label = QLabel(label_text)
        if tooltip != '':
            label.setToolTip(tooltip)

        if self.pending_column:
            if isinstance(option, QCheckBox):
                option.setText(label_text)

                layout = QVBoxLayout()
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(option)

                layout_widget = QWidget()
                layout_widget.setProperty('cssClass', 'layoutWidget')
                layout_widget.setLayout(layout)
                if self.pending_group:
                    self.pending_group.addWidget(layout_widget)
                else:
                    self.pending_column.addWidget(layout_widget)
            elif isinstance(option, QListWidget):
                layout = QVBoxLayout()
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(option, alignment=Qt.AlignLeft)

                layout_widget = QWidget()
                layout_widget.setProperty('cssClass', 'layoutWidget')
                layout_widget.setLayout(layout)
                if self.pending_group:
                    self.pending_group.addWidget(layout_widget)
                else:
                    self.pending_column.addWidget(layout_widget)
            else:
                layout = QHBoxLayout()
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(label)
                layout.addWidget(option, alignment=Qt.AlignRight)

                layout_widget = QWidget()
                layout_widget.setProperty('cssClass', 'layoutWidget')
                layout_widget.setLayout(layout)
                if self.pending_group:
                    self.pending_group.addWidget(layout_widget)
                else:
                    self.pending_column.addWidget(layout_widget)
        else:
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(label, stretch=1)
            layout.addWidget(option, stretch=2, alignment=Qt.AlignLeft)

            layout_widget = QWidget()
            layout_widget.setProperty('cssClass', 'layoutWidget')
            layout_widget.setLayout(layout)
            self.menulayout.addWidget(layout_widget)

    def add_option(self, setting_name: str):
        setting = Class.seedSettings.settings_by_name[setting_name]

        if isinstance(setting, Toggle):
            widget = self.make_check_box(setting_name)
        elif isinstance(setting, IntSpinner):
            widget = self.make_int_spin_box(setting_name)
        elif isinstance(setting, FloatSpinner):
            widget = self.make_double_spin_box(setting_name)
        elif isinstance(setting, SingleSelect):
            widget = self.make_combo_box(setting_name)
        elif isinstance(setting, MultiSelect):
            widget = self.make_multi_select_list(setting_name)
        elif isinstance(setting, MultiSelectTristate):
            widget = self.make_multi_select_tristate_list(setting_name)
        elif isinstance(setting, ProgressionChainSelect):
            widget = ProgressionWidget(self.settings,setting_name)
        else:
            print('Unknown setting type')
            return

        if setting.tooltip != '':
            widget.setToolTip(setting.tooltip)

        self._add_option_widget(setting.ui_label, setting.tooltip, widget)
        self.widgets_and_settings_by_name[setting_name] = (setting, widget)

    def set_option_visibility(self, name: str, visible: bool):
        (_, widget) = self.widgets_and_settings_by_name[name]

        if isinstance(widget, QWidget):
            # Most option widgets have a direct parent (containing the label and widget)
            # that can have its visibility toggled
            widget.parentWidget().setVisible(visible)
        elif isinstance(widget, list) and len(widget) > 0:
            # The multi-select buttons are represented as a list but they're contained within a parent widget as well
            widget[0].parentWidget().setVisible(visible)

    def make_multiselect_tristate(self, setting_name: str) -> (MultiSelectTristate, list[QGroupBox]):
        setting = Class.seedSettings.settings_by_name[setting_name]

        if not isinstance(setting, MultiSelectTristate):
            print('Expected a MultiSelectTristate for ' + setting_name)
            return

        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)

        widgets = []
        selected_keys = self.settings.get(setting_name)
        partial_keys = []
        if isinstance(selected_keys[0], list):
            partial_keys = selected_keys[1]
            selected_keys = selected_keys[0]
        for index, choice_key in enumerate(setting.choice_keys):
            randomize_button = QRadioButton("Rando")
            vanilla_button = QRadioButton("Vanilla")
            junk_button = QRadioButton("Junk")
            if choice_key in selected_keys:
                randomize_button.setChecked(True)
            elif choice_key in partial_keys:
                vanilla_button.setChecked(True)
            else:
                junk_button.setChecked(True)

            randomize_button.toggled.connect(lambda state: self._update_multi_tristate_buttons(setting))
            vanilla_button.toggled.connect(lambda state: self._update_multi_tristate_buttons(setting))
            junk_button.toggled.connect(lambda state: self._update_multi_tristate_buttons(setting))

            self.tristate_groups[choice_key] = (randomize_button, vanilla_button, junk_button)

            top_layout = QHBoxLayout()
            world_label = QLabel(setting.choice_values[index])
            top_layout.addWidget(world_label)

            bottom_layout = QHBoxLayout()
            bottom_layout.setContentsMargins(4, 0, 4, 0)
            label = QLabel()
            icon = QIcon(resource_path(dir_path + '/' + setting.choice_icons[choice_key]))
            pixmap = icon.pixmap(icon.actualSize(QSize(32, 32)))
            label.setPixmap(pixmap)
            bottom_layout.addWidget(label)
            button_layout = QHBoxLayout()
            button_layout.addWidget(randomize_button)
            button_layout.addWidget(vanilla_button)
            button_layout.addWidget(junk_button)
            bottom_layout.addLayout(button_layout)

            vertical = QVBoxLayout()
            vertical.setContentsMargins(4, 4, 4, 4)
            vertical.addLayout(top_layout)
            vertical.addLayout(bottom_layout)
            self.tristate_backgrounds[choice_key] = world_label

            widget = QWidget()
            widget.setStyleSheet('background-color: #232629')
            widget.setLayout(vertical)
            widgets.append(widget)

        self.widgets_and_settings_by_name[setting_name] = (setting, widgets)
        self._update_multi_tristate_buttons(setting)

        return setting, widgets

    def make_multiselect_buttons(self, setting_name: str) -> (MultiSelect, list[QPushButton]):
        setting = Class.seedSettings.settings_by_name[setting_name]

        if not isinstance(setting, MultiSelect):
            print('Expected a MultiSelect for ' + setting_name)
            return

        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)

        widgets = []
        selected_keys = self.settings.get(setting_name)
        for index, choice_key in enumerate(setting.choice_keys):
            button = QPushButton(setting.choice_values[index])
            button.setIconSize(QSize(36, 36))
            button.setIcon(QIcon(resource_path(dir_path + '/' + setting.choice_icons[choice_key])))
            button.setCheckable(True)
            if choice_key in selected_keys:
                button.setChecked(True)
            button.toggled.connect(lambda state: self._update_multi_buttons(setting))

            widgets.append(button)

        self.widgets_and_settings_by_name[setting_name] = (setting, widgets)

        return setting, widgets

    def add_multiselect_buttons(self, setting_name: str, columns: int, group_title: str, tristate=False):
        grid = QGridLayout()
        grid.setAlignment(Qt.AlignTop)
        if tristate:
            setting, widgets = self.make_multiselect_tristate(setting_name)
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setSpacing(4)
        else:
            setting, widgets = self.make_multiselect_buttons(setting_name)

        for index, choice_key in enumerate(setting.choice_keys):
            button = widgets[index]
            grid.addWidget(button, index // columns, index % columns)
        if columns == 1:
            grid.addWidget(QLabel(''))

        if self.pending_column:
            if self.pending_group:
                self.pending_group.addLayout(grid)
            else:
                self.pending_column.addLayout(grid)
        else:
            group_box = QGroupBox(group_title)
            group_box.setLayout(grid)
            self.menulayout.addWidget(group_box)

    def addHeader(self, label_text):
        label = QLabel(label_text)
        label.setProperty('cssClass', 'header')
        if self.pending_group:
            self.pending_group.addWidget(label)
        elif self.pending_column:
            self.pending_column.addWidget(label)
        else:
            self.menulayout.addWidget(label)

    def finalizeMenu(self):
        self.menulayout.addStretch(1)
        self.setLayout(self.menulayout)

    def getName(self):
        return self.title

    def disable_widgets(self):
        for name in self.widgets_and_settings_by_name:
            (setting, widget) = self.widgets_and_settings_by_name[name]
            if isinstance(setting, Toggle):
                widget.setDisabled(True)
            elif isinstance(setting, IntSpinner):
                widget.setDisabled(True)
            elif isinstance(setting, FloatSpinner):
                widget.setDisabled(True)
            elif isinstance(setting, SingleSelect):
                widget.setDisabled(True)
            elif isinstance(setting, MultiSelect):
                if isinstance(widget, QListWidget):
                    # widget.setDisabled(True)                    
                    widget.setSelectionMode(QAbstractItemView.NoSelection)
                elif isinstance(widget, list):
                    for index, key in enumerate(setting.choice_keys):
                        widget[index].setDisabled(True)
            elif isinstance(setting, MultiSelectTristate):
                if isinstance(widget, list):
                    for index, key in enumerate(setting.choice_keys):
                        widget[index].setDisabled(True)

    def update_widgets(self):
        for name in self.widgets_and_settings_by_name:
            (setting, widget) = self.widgets_and_settings_by_name[name]

            if isinstance(setting, Toggle):
                widget.setCheckState(Qt.Checked if self.settings.get(name) else Qt.Unchecked)
            elif isinstance(setting, IntSpinner):
                widget.setValue(self.settings.get(name))
            elif isinstance(setting, FloatSpinner):
                widget.setValue(self.settings.get(name))
            elif isinstance(setting, SingleSelect):
                index = setting.choice_keys.index(self.settings.get(name))
                widget.setCurrentIndex(index)
            elif isinstance(setting, MultiSelect):
                if isinstance(widget, QListWidget):
                    selected_keys = self.settings.get(name)
                    for index, key in enumerate(setting.choice_keys):
                        selected = key in selected_keys
                        widget.item(index).setSelected(selected)
                elif isinstance(widget, list):
                    selected_keys = self.settings.get(name)
                    for index, key in enumerate(setting.choice_keys):
                        selected = key in selected_keys
                        widget[index].setChecked(selected)
            elif isinstance(setting, MultiSelectTristate):
                if isinstance(widget, list):
                    selected_keys = self.settings.get(name)
                    if isinstance(selected_keys[0],list):
                        # we have the updated settings
                        enabled_locs = selected_keys[0]
                        vanilla_locs = selected_keys[1]
                    else:
                        # we have the updated settings
                        enabled_locs = selected_keys
                        vanilla_locs = []

                    for index, key in enumerate(setting.choice_keys):
                        selected = key in enabled_locs
                        vanil_selected = key in vanilla_locs
                        rando,vanil,junk = self.tristate_groups[setting.choice_keys[index]]
                        if selected:
                            rando.setChecked(True)
                        elif vanil_selected:
                            vanil.setChecked(True)
                        else:
                            junk.setChecked(True)

    def make_combo_box(self, name: str):
        setting: SingleSelect = Class.seedSettings.settings_by_name[name]
        keys = setting.choice_keys
        combo_box = QComboBox()
        combo_box.addItems(setting.choice_values)
        combo_box.setCurrentIndex(keys.index(self.settings.get(name)))
        combo_box.currentIndexChanged.connect(lambda index: self.settings.set(name, keys[index]))
        return combo_box

    def make_check_box(self, name: str):
        check_box = QCheckBox()
        check_box.setCheckState(Qt.Checked if self.settings.get(name) else Qt.Unchecked)
        check_box.stateChanged.connect(lambda state: self.settings.set(name, state == Qt.Checked))
        return check_box

    def make_int_spin_box(self, name: str):
        setting: IntSpinner = Class.seedSettings.settings_by_name[name]
        spin_box = QSpinBox()
        spin_box.setRange(setting.min, setting.max)
        spin_box.setSingleStep(setting.step)
        spin_box.setValue(self.settings.get(name))
        spin_box.valueChanged.connect(lambda value: self.settings.set(name, value))
        line = spin_box.lineEdit()
        line.setReadOnly(True)
        return spin_box

    def make_double_spin_box(self, name: str):
        setting: FloatSpinner = Class.seedSettings.settings_by_name[name]
        spin_box = QDoubleSpinBox()
        spin_box.setDecimals(1)
        spin_box.setRange(setting.min, setting.max)
        spin_box.setSingleStep(setting.step)
        spin_box.setValue(self.settings.get(name))
        spin_box.valueChanged.connect(lambda value: self.settings.set(name, value))
        line = spin_box.lineEdit()
        line.setReadOnly(True)
        return spin_box

    def make_multi_select_list(self, name: str):
        setting: MultiSelect = Class.seedSettings.settings_by_name[name]
        list_widget = QListWidget()
        list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        list_widget.addItems(setting.choice_values)

        for selected in self.settings.get(name):
            if selected in setting.choice_keys:
                index = setting.choice_keys.index(selected)
                list_widget.item(index).setSelected(True)

        list_widget.itemSelectionChanged.connect(lambda: self._update_multi_list(setting, list_widget))
        return list_widget

    def make_multi_select_tristate_list(self, name: str):
        return None
        # setting: MultiSelectTristate = Class.seedSettings.settings_by_name[name]
        # list_widget = QListWidget()
        # list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        # list_widget.addItems(setting.choice_values)

        # for selected in self.settings.get(name):
        #     if selected in setting.choice_keys:
        #         index = setting.choice_keys.index(selected)
        #         list_widget.item(index).setSelected(True)

        # list_widget.itemSelectionChanged.connect(lambda: self._update_multi_tristate_list(setting, list_widget))
        # return list_widget

    def _update_multi_list(self, setting: MultiSelect, widget: QListWidget):
        choice_keys = setting.choice_keys
        selected_keys = []
        for index in widget.selectedIndexes():
            selected_keys.append(choice_keys[index.row()])
        self.settings.set(setting.name, selected_keys)

    def _update_multi_tristate_list(self, setting: MultiSelectTristate, widget: QListWidget):
        return None
        # choice_keys = setting.choice_keys
        # selected_keys = []
        # for index in widget.selectedIndexes():
        #     selected_keys.append(choice_keys[index.row()])
        # self.settings.set(setting.name, [selected_keys,[]])

    def _update_multi_buttons(self, setting: MultiSelect):
        (_, buttons) = self.widgets_and_settings_by_name[setting.name]
        choice_keys = setting.choice_keys
        selected_keys = []
        for index, button in enumerate(buttons):
            if button.isChecked():
                selected_keys.append(choice_keys[index])
        self.settings.set(setting.name, selected_keys)

    def _update_multi_tristate_buttons(self, setting: MultiSelectTristate):
        (_, buttons) = self.widgets_and_settings_by_name[setting.name]
        choice_keys = setting.choice_keys
        selected_keys = []
        partial_keys = []
        for index, button in enumerate(buttons):
            rando, vanil, junk = self.tristate_groups[choice_keys[index]]
            choice_group = self.tristate_backgrounds[choice_keys[index]]
            if rando.isChecked():
                selected_keys.append(choice_keys[index])
                choice_group.setStyleSheet("QLabel {background-color: #04641b}")
            elif vanil.isChecked():
                choice_group.setStyleSheet("QLabel {background-color: gray}")
                partial_keys.append(choice_keys[index])
            else:
                choice_group.setStyleSheet("QLabel {background-color: {QTMATERIAL_PRIMARYCOLOR}}")
        self.settings.set(setting.name, [selected_keys, partial_keys])

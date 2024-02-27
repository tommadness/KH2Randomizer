from typing import Optional

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDoubleSpinBox, QFrame, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QListWidget,
    QPushButton, QSpinBox, QWidget, QVBoxLayout, QAbstractItemView, QScrollArea, QLayout
)

import Class.seedSettings
from Class.seedSettings import WorldRandomizationTristate, ProgressionChainSelect, SeedSettings, Toggle, IntSpinner, \
    FloatSpinner, SingleSelect, MultiSelect
from List.configDict import locationType
from Module.resources import resource_path
from UI import theme
from UI.Submenus.ProgressionWidgets import ProgressionWidget

header_styles = [
    f"background: {theme.KhMediumRed}; color: {theme.KhLightRed};",
    f"background: {theme.KhMediumYellow}; color: {theme.KhLightYellow};",
    f"background: {theme.KhMediumGreen}; color: {theme.KhLightGreen};",
    f"background: {theme.KhMediumBlue}; color: {theme.KhLightBlue};",
    f"background: {theme.KhMediumPurple}; color: {theme.KhLightPurple};",
]
frame_styles = [
    f"background: {theme.KhDarkRed};",
    f"background: {theme.KhDarkYellow};",
    f"background: {theme.KhDarkGreen};",
    f"background: {theme.KhDarkBlue};",
    f"background: {theme.KhDarkPurple};",
]


class KH2Submenu(QWidget):

    def __init__(self, title: str, settings: SeedSettings):
        super().__init__()

        self.title = title
        self.settings = settings
        self.widgets_and_settings_by_name = {}
        self.groups_by_id: dict[str, QWidget] = {}

        self.menulayout = QHBoxLayout()
        self.pending_column: Optional[QVBoxLayout] = None
        self.pending_group: Optional[QVBoxLayout] = None

        self.tristate_combo_boxes: dict[str, QComboBox] = {}

        self.next_header_style = len(title) % len(header_styles)

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

    def end_group(self, title='', group_id=''):
        header_style_choice = self.next_header_style % len(header_styles)
        self.next_header_style = self.next_header_style + 1

        group = QVBoxLayout()
        group.setContentsMargins(0, 0, 0, 0)

        frame = self.make_styled_frame(self.pending_group, header_style_choice=header_style_choice, title=title)

        self.pending_column.addWidget(frame)
        self.pending_group = None

        if group_id != '':
            self.groups_by_id[group_id] = frame

    def add_labeled_widget(self, widget: QWidget, label_text: str, tooltip: str = ""):
        label = QLabel(label_text)
        if tooltip != '':
            label.setToolTip(tooltip)
        else:
            widget_tooltip = widget.toolTip()
            if widget_tooltip != '':
                label.setToolTip(widget_tooltip)

        if self.pending_column:
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(label)
            layout.addWidget(widget, alignment=Qt.AlignRight)

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
            layout.addWidget(widget, stretch=2, alignment=Qt.AlignLeft)

            layout_widget = QWidget()
            layout_widget.setProperty('cssClass', 'layoutWidget')
            layout_widget.setLayout(layout)
            self.menulayout.addWidget(layout_widget)

    def _add_option_widget(self, label_text: str, tooltip: str, option):
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
                self.add_labeled_widget(option, label_text=label_text, tooltip=tooltip)
        else:
            self.add_labeled_widget(option, label_text=label_text, tooltip=tooltip)

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
        elif isinstance(setting, WorldRandomizationTristate):
            widget = None  # Handled elsewhere
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

    def set_group_visibility(self, group_id: str, visible: bool):
        if group_id in self.groups_by_id:
            widget = self.groups_by_id[group_id]
            widget.setVisible(visible)

    def make_multiselect_tristate(self, setting_name: str) -> (WorldRandomizationTristate, list[QGroupBox]):
        setting = Class.seedSettings.settings_by_name[setting_name]

        if not isinstance(setting, WorldRandomizationTristate):
            print('Expected a WorldRandomizationTristate for ' + setting_name)
            return

        widgets = []
        selected_keys = self.settings.get(setting_name)
        partial_keys = []
        if isinstance(selected_keys[0], list):
            partial_keys = selected_keys[1]
            selected_keys = selected_keys[0]
        for index, choice_key in enumerate(setting.choice_keys):
            combo_box = QComboBox()
            combo_box.addItems(["Randomized", "Vanilla", "Junk"])

            if choice_key in selected_keys:
                combo_box.setCurrentIndex(0)
            elif choice_key in partial_keys:
                combo_box.setCurrentIndex(1)
            else:
                combo_box.setCurrentIndex(2)

            combo_box.currentIndexChanged.connect(lambda: self._update_multi_tristate_buttons(setting))

            self.tristate_combo_boxes[choice_key] = combo_box

            top_layout = QHBoxLayout()
            world_label = QLabel(setting.choice_values[index])
            if choice_key == locationType.Level:
                world_label.setText("Levels (Sora's Heart)")
            top_layout.addWidget(world_label)

            bottom_layout = QHBoxLayout()
            bottom_layout.setContentsMargins(4, 0, 4, 0)
            label = QLabel()
            icon = QIcon(resource_path(setting.choice_icons[choice_key]))
            pixmap = icon.pixmap(icon.actualSize(QSize(32, 32)))
            label.setPixmap(pixmap)
            bottom_layout.addWidget(label)
            button_layout = QHBoxLayout()
            button_layout.addWidget(combo_box)
            bottom_layout.addLayout(button_layout, stretch=1)

            vertical = QVBoxLayout()
            vertical.setContentsMargins(4, 0, 4, 0)
            vertical.addLayout(top_layout)
            vertical.addLayout(bottom_layout)

            widget = QWidget()
            widget.setContentsMargins(0, 0, 0, 8)
            widget.setStyleSheet("QWidget { background-color: transparent; }")
            widget.setFixedWidth(250)
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

        widgets = []
        selected_keys = self.settings.get(setting_name)
        for index, choice_key in enumerate(setting.choice_keys):
            button = QPushButton(setting.choice_values[index])
            button.setProperty("cssClass", "toggle")
            button.setIconSize(QSize(36, 36))
            button.setIcon(QIcon(resource_path(setting.choice_icons[choice_key])))
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

        scroll_child = QWidget()
        scroll_child.setLayout(self.menulayout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(scroll_child)
        scroll_area.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.addWidget(scroll_area)

        self.setLayout(layout)

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
            elif isinstance(setting, WorldRandomizationTristate):
                if isinstance(widget, list):
                    for index, key in enumerate(setting.choice_keys):
                        widget[index].setDisabled(True)

    def update_widget(self, name: str):
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
        elif isinstance(setting, WorldRandomizationTristate):
            if isinstance(widget, list):
                selected_keys = self.settings.get(name)
                if isinstance(selected_keys[0], list):
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
                    combo_box = self.tristate_combo_boxes[setting.choice_keys[index]]
                    if selected:
                        combo_box.setCurrentIndex(0)
                    elif vanil_selected:
                        combo_box.setCurrentIndex(1)
                    else:
                        combo_box.setCurrentIndex(2)
        elif isinstance(setting, ProgressionChainSelect):
            setting.progression.set_uncompressed(self.settings.get(name))
            widget._update_spinboxes()

    def update_widgets(self):
        for name in self.widgets_and_settings_by_name:
            self.update_widget(name)

    @staticmethod
    def make_styled_frame(layout: QLayout, header_style_choice: int, title: str = "") -> QFrame:
        group = QVBoxLayout()
        group.setContentsMargins(0, 0, 0, 0)

        if title != '':
            title_label = QLabel(title)
            title_label.setContentsMargins(8, 8, 8, 8)
            title_label.setProperty('cssClass', 'groupHeader')
            title_label.setStyleSheet(header_styles[header_style_choice])
            group.addWidget(title_label)

        group.addLayout(layout)

        frame = QFrame()
        if title == '':
            frame.setContentsMargins(0, 8, 0, 8)
        else:
            frame.setContentsMargins(0, 0, 0, 8)
        frame.setProperty('cssClass', 'settingsFrame')
        frame_style = frame_styles[header_style_choice]
        frame.setStyleSheet('QFrame[cssClass~="settingsFrame"], QWidget[cssClass~="layoutWidget"], QLabel, QCheckBox {' + frame_style + '}')
        frame.setLayout(group)

        return frame

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

    def _update_multi_list(self, setting: MultiSelect, widget: QListWidget):
        choice_keys = setting.choice_keys
        selected_keys = []
        for index in widget.selectedIndexes():
            selected_keys.append(choice_keys[index.row()])
        self.settings.set(setting.name, selected_keys)

    def _update_multi_buttons(self, setting: MultiSelect):
        (_, buttons) = self.widgets_and_settings_by_name[setting.name]
        choice_keys = setting.choice_keys
        selected_keys = []
        for index, button in enumerate(buttons):
            if button.isChecked():
                selected_keys.append(choice_keys[index])
        self.settings.set(setting.name, selected_keys)

    def _update_multi_tristate_buttons(self, setting: WorldRandomizationTristate):
        (_, buttons) = self.widgets_and_settings_by_name[setting.name]
        choice_keys = setting.choice_keys
        selected_keys = []
        partial_keys = []
        for index, _ in enumerate(buttons):
            combo_box = self.tristate_combo_boxes[choice_keys[index]]
            selected_index = combo_box.currentIndex()
            if selected_index == 0:
                selected_keys.append(choice_keys[index])
            elif selected_index == 1:
                partial_keys.append(choice_keys[index])
            self._update_multi_tristate_visual(combo_box)
        self.settings.set(setting.name, [selected_keys, partial_keys])

    @staticmethod
    def _update_multi_tristate_visual(combo_box: QComboBox):
        current_index = combo_box.currentIndex()
        text_color = "white"
        if current_index == 0:
            background_color = theme.SelectionColor
            border_color = theme.SelectionBorderColor
        elif current_index == 1:
            background_color = theme.KhMediumPurple
            border_color = theme.KhLightPurple
        else:
            background_color = "#00000a"
            border_color = background_color
            text_color = "#999999"
        stylesheet = f"QComboBox {{ border: 1px solid {border_color}; background-color: {background_color}; color: {text_color};}}"
        stylesheet += f" QComboBox QAbstractItemView {{ background-color: {theme.BackgroundPrimary}; }}"
        combo_box.setStyleSheet(stylesheet)

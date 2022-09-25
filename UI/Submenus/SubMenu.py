import os
from typing import Optional

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDoubleSpinBox, QFrame, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QListWidget,
    QPushButton, QSpinBox, QWidget, QVBoxLayout, QAbstractItemView
)

import Class.seedSettings
from Class.seedSettings import SeedSettings, Toggle, IntSpinner, FloatSpinner, SingleSelect, MultiSelect
from Module.resources import resource_path


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

    def start_column(self):
        self.pending_column = QVBoxLayout()

    def end_column(self, stretch_at_end=True):
        if stretch_at_end:
            self.pending_column.addStretch()
        frame = QFrame()
        frame.setLayout(self.pending_column)
        self.menulayout.addWidget(frame)
        self.menulayout.addSpacing(8)
        self.pending_column = None

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
                layout_widget.setLayout(layout)
                self.pending_column.addWidget(layout_widget)
            elif isinstance(option, QListWidget):
                layout = QVBoxLayout()
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(label)
                layout.addWidget(option, alignment=Qt.AlignLeft)

                layout_widget = QWidget()
                layout_widget.setLayout(layout)
                self.pending_column.addWidget(layout_widget)
            else:
                layout = QHBoxLayout()
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(label)
                layout.addWidget(option, alignment=Qt.AlignRight)

                layout_widget = QWidget()
                layout_widget.setLayout(layout)
                self.pending_column.addWidget(layout_widget)
        else:
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(label, stretch=1)
            layout.addWidget(option, stretch=2, alignment=Qt.AlignLeft)

            layout_widget = QWidget()
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

    def add_multiselect_buttons(self, setting_name: str, columns: int, group_title: str):
        setting, widgets = self.make_multiselect_buttons(setting_name)

        grid = QGridLayout()
        grid.setAlignment(Qt.AlignTop)

        for index, choice_key in enumerate(setting.choice_keys):
            button = widgets[index]
            grid.addWidget(button, index // columns, index % columns)
        if columns == 1:
            grid.addWidget(QLabel(''))

        if self.pending_column:
            label = QLabel(group_title)
            tooltip = setting.tooltip
            if tooltip != '':
                label.setToolTip(tooltip)
            self.pending_column.addWidget(label)
            self.pending_column.addLayout(grid)
        else:
            group_box = QGroupBox(group_title)
            group_box.setLayout(grid)
            self.menulayout.addWidget(group_box)

    def addHeader(self, label_text):
        label = QLabel(label_text)
        label.setProperty('cssClass', 'header')
        if self.pending_column:
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

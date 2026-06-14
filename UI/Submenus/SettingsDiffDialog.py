from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QColor, QBrush
from PySide6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QLabel, QPushButton
)

import Class.seedSettings as seed_settings_module
from Class.seedSettings import SeedSettings, SettingGroup
from Module.resources import resource_path
from UI import presets, theme


def _human_readable(setting, value) -> str:
    entries = setting.spoiler_log_entries(value)
    return " | ".join(str(v) for v in entries.values())


def _compute_diff(current: SeedSettings, preset_json: dict) -> list[tuple[SettingGroup, str, str, str]]:
    """Returns list of (group, label, preset_value, current_value) for settings that differ."""
    preset_settings = SeedSettings()
    preset_settings.apply_settings_json(preset_json)

    diffs = []
    for key, setting in SeedSettings.filtered_settings(include_private=False).items():
        current_val = current.get(key)
        preset_val = preset_settings.get(key)

        if current_val == preset_val:
            continue

        try:
            current_str = _human_readable(setting, current_val)
            preset_str = _human_readable(setting, preset_val)
        except Exception:
            current_str = str(current_val)
            preset_str = str(preset_val)

        diffs.append((setting.group, setting.standalone_label, preset_str, current_str))

    diffs.sort(key=lambda d: (d[0].value, d[1]))
    return diffs


class SettingsDiffDialog(QDialog):

    def __init__(self, parent: Optional[QWidget], current_settings: SeedSettings):
        super().__init__(parent)
        self.current_settings = current_settings
        self.setWindowTitle("Compare Settings to Preset")
        self.setWindowIcon(QIcon(resource_path("Module/icon.png")))
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)

        self._all_presets: list[presets.SettingsPreset] = (
            presets.list_bundled_presets() + presets.list_user_presets()
        )

        self.preset_combo = QComboBox()
        for p in self._all_presets:
            label = f"[Bundled] {p.display_name}" if p.bundled else p.display_name
            self.preset_combo.addItem(label)
        self.preset_combo.currentIndexChanged.connect(self._refresh_diff)

        self.status_label = QLabel()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Setting", "Preset Value", "Current Value"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {theme.BackgroundDark};
                alternate-background-color: {theme.BackgroundPrimary};
                color: white;
                gridline-color: {theme.BackgroundPrimary};
                border: none;
            }}
            QTableWidget::item {{
                padding: 4px 8px;
                border: none;
            }}
            QTableWidget::item:selected {{
                background-color: {theme.SelectionColor};
                border: 1px solid {theme.SelectionBorderColor};
                color: white;
            }}
            QHeaderView::section {{
                background-color: {theme.KhMediumBlue};
                color: {theme.KhLightBlue};
                padding: 4px 8px;
                border: none;
                font-family: KHMenu;
                font-size: 14px;
            }}
        """)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)

        combo_layout = QHBoxLayout()
        combo_layout.addWidget(QLabel("Compare against preset:"))
        combo_layout.addWidget(self.preset_combo, stretch=1)

        layout = QVBoxLayout()
        layout.addLayout(combo_layout)
        layout.addWidget(self.status_label)
        layout.addWidget(self.table)
        layout.addWidget(close_button, alignment=Qt.AlignRight)
        self.setLayout(layout)

        if self._all_presets:
            self._refresh_diff(0)
        else:
            self.status_label.setText("No presets found.")

    def _refresh_diff(self, index: int):
        if index < 0 or index >= len(self._all_presets):
            return

        preset = self._all_presets[index]
        try:
            preset_json = preset.settings_json()
        except Exception as e:
            self.status_label.setText(f"Could not load preset: {e}")
            self.table.setRowCount(0)
            return

        diffs = _compute_diff(self.current_settings, preset_json)

        self.table.setRowCount(0)
        if not diffs:
            self.status_label.setText("Current settings match the selected preset exactly.")
            return

        self.status_label.setText(f"{len(diffs)} setting(s) differ from the selected preset.")

        group_bg = QBrush(QColor(theme.KhMediumPurple))
        group_fg = QBrush(QColor(theme.KhLightPurple))

        last_group: Optional[SettingGroup] = None
        for group, label, preset_val, current_val in diffs:
            if group != last_group:
                header_row = self.table.rowCount()
                self.table.insertRow(header_row)
                group_item = QTableWidgetItem(group.value)
                group_item.setTextAlignment(Qt.AlignCenter)
                font = group_item.font()
                font.setBold(True)
                group_item.setFont(font)
                group_item.setBackground(group_bg)
                group_item.setForeground(group_fg)
                self.table.setItem(header_row, 0, group_item)
                self.table.setSpan(header_row, 0, 1, 3)
                last_group = group

            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(label))
            self.table.setItem(row, 1, QTableWidgetItem(preset_val))
            self.table.setItem(row, 2, QTableWidgetItem(current_val))

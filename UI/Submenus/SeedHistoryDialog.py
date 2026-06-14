from datetime import datetime, timezone
from typing import Optional, Callable

from PySide6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton,
    QLabel, QMessageBox, QListWidgetItem
)
from PySide6.QtGui import QIcon

from Module import seedHistory
from Module.resources import resource_path


def _format_timestamp(iso_str: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_str)
        local_dt = dt.astimezone()
        return local_dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return iso_str


class SeedHistoryDialog(QDialog):

    def __init__(self, parent: Optional[QWidget], on_load_settings: Callable[[str, dict], None]):
        super().__init__(parent)
        self.on_load_settings = on_load_settings
        self.setWindowTitle("Seed History")
        self.setWindowIcon(QIcon(resource_path("Module/icon.png")))
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)

        self._entries: list[dict] = []

        self.list_widget = QListWidget()
        self.list_widget.currentRowChanged.connect(self._on_selection_changed)
        self.list_widget.itemDoubleClicked.connect(self._load_selected)

        self.detail_label = QLabel()
        self.detail_label.setWordWrap(True)

        self.load_button = QPushButton("Load Settings")
        self.load_button.clicked.connect(self._load_selected)
        self.load_button.setEnabled(False)

        self.delete_button = QPushButton("Delete Entry")
        self.delete_button.clicked.connect(self._delete_selected)
        self.delete_button.setEnabled(False)

        clear_button = QPushButton("Clear All History")
        clear_button.clicked.connect(self._clear_all)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        button_layout.addWidget(clear_button)
        button_layout.addWidget(close_button)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select and entry and click Load Settings to restore those settings."))
        layout.addWidget(self.list_widget)
        layout.addWidget(self.detail_label)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self._refresh_list()

    def _refresh_list(self):
        self._entries = seedHistory.load_history()
        self.list_widget.clear()
        for entry in self._entries:
            ts = _format_timestamp(entry.get("timestamp", ""))
            seed_name = entry.get("seed_name", "(unknown)")
            self.list_widget.addItem(f"{ts}  —  {seed_name}")

        no_entries = len(self._entries) == 0
        self.detail_label.setText("No history entries." if no_entries else "")
        self._on_selection_changed(self.list_widget.currentRow())

    def _on_selection_changed(self, row: int):
        has_selection = 0 <= row < len(self._entries)
        self.load_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)

    def _load_selected(self):
        row = self.list_widget.currentRow()
        if 0 <= row < len(self._entries):
            entry = self._entries[row]
            seed_name = entry.get("seed_name", "")
            settings = entry.get("settings", {})
            self.on_load_settings(seed_name, settings)
            self.accept()

    def _delete_selected(self):
        row = self.list_widget.currentRow()
        if 0 <= row < len(self._entries):
            entry = self._entries[row]
            seed_name = entry.get("seed_name", "(unknown)")
            reply = QMessageBox.question(
                self,
                "Delete Entry",
                f"Delete history entry for seed '{seed_name}'?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                seedHistory.delete_history_entry(row)
                self._refresh_list()

    def _clear_all(self):
        if not self._entries:
            return
        reply = QMessageBox.question(
            self,
            "Clear History",
            "Clear all seed history? This cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            seedHistory.clear_history()
            self._refresh_list()

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Module import appconfig

HISTORY_FILE = os.path.join(appconfig.AUTOSAVE_FOLDER, "seed-history.json")
MAX_HISTORY_ENTRIES = 50


def load_history() -> list[dict[str, Any]]:
    path = Path(HISTORY_FILE)
    if not path.is_file():
        return []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []


def _save_history(entries: list[dict[str, Any]]):
    path = Path(HISTORY_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def save_seed_to_history(seed_name: str, settings_json: dict[str, Any]):
    entries = load_history()
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "seed_name": seed_name,
        "settings": settings_json,
    }
    entries.insert(0, entry)
    if len(entries) > MAX_HISTORY_ENTRIES:
        entries = entries[:MAX_HISTORY_ENTRIES]
    _save_history(entries)


def delete_history_entry(index: int):
    entries = load_history()
    if 0 <= index < len(entries):
        entries.pop(index)
        _save_history(entries)


def clear_history():
    _save_history([])

from types import SimpleNamespace

import pytest

from Class.exceptions import ExternalExecutableException, RandomizerExceptions
from Module.version import EXTRACTED_DATA_UPDATE_VERSION, LOCAL_UI_VERSION
from UI.worker import GenerateModWorker


def test_local_ui_version_remains_at_latest_public_release():
    assert LOCAL_UI_VERSION == "3.3.0-beta"
    assert EXTRACTED_DATA_UPDATE_VERSION == "3.0.1"


def test_external_executable_exception_is_a_randomizer_exception():
    assert ExternalExecutableException in RandomizerExceptions


def test_custom_cosmetics_invalid_executable_raises_dedicated_exception(monkeypatch, tmp_path):
    custom_file = tmp_path / "custom-cosmetics.txt"
    custom_file.write_text("not executable")
    extra_data = SimpleNamespace(custom_cosmetics_executables=[str(custom_file)])

    monkeypatch.setattr("UI.worker.platformutils.is_windows", lambda: False)
    monkeypatch.setattr("UI.worker.os.access", lambda path, mode: False)

    with pytest.raises(
        ExternalExecutableException,
        match=r"custom-cosmetics\.txt is not executable.*chmod \+x.*\.sh or \.exe",
    ):
        GenerateModWorker.run_custom_cosmetics_executables(extra_data)

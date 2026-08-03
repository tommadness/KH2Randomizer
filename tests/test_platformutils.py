import os
from pathlib import Path

import pytest

from Class.exceptions import GeneratorException
from Module import platformutils


def test_application_data_directory_uses_xdg_home(monkeypatch, tmp_path):
    monkeypatch.setattr(platformutils, "is_linux", lambda: True)
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    assert platformutils.application_data_directory() == tmp_path / "kh2randomizer"


def test_initialize_application_data_directory_changes_linux_cwd(monkeypatch, tmp_path):
    original_cwd = Path.cwd()
    monkeypatch.setattr(platformutils, "is_linux", lambda: True)
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    try:
        result = platformutils.initialize_application_data_directory()
        assert result == tmp_path / "kh2randomizer"
        assert Path.cwd() == result
    finally:
        os.chdir(original_cwd)


def test_path_from_config_value_translates_wine_z_drive(monkeypatch):
    monkeypatch.setattr(platformutils, "is_windows", lambda: False)

    assert platformutils.path_from_config_value(r"Z:\home\user\OpenKH") == Path("/home/user/OpenKH")


def test_openkh_tool_launcher_prefers_native(monkeypatch, tmp_path):
    monkeypatch.setattr(platformutils, "is_windows", lambda: False)
    native = tmp_path / "OpenKh.Command.Bar"
    native.write_text("tool")
    monkeypatch.setattr(os, "access", lambda path, mode: path == native)

    assert platformutils.openkh_tool_launcher(tmp_path, "OpenKh.Command.Bar") == [str(native)]


def test_openkh_tool_launcher_uses_dotnet_before_wine(monkeypatch, tmp_path):
    monkeypatch.setattr(platformutils, "is_windows", lambda: False)
    monkeypatch.setattr(platformutils.shutil, "which", lambda command: "/usr/bin/dotnet" if command == "dotnet" else None)
    dll = tmp_path / "OpenKh.Command.Bar.dll"
    dll.write_text("tool")
    (tmp_path / "OpenKh.Command.Bar.exe").write_text("tool")

    assert platformutils.openkh_tool_launcher(tmp_path, "OpenKh.Command.Bar") == [
        "dotnet", "--roll-forward", "LatestMajor", str(dll)
    ]


def test_openkh_tool_launcher_reports_missing_runtime(monkeypatch, tmp_path):
    monkeypatch.setattr(platformutils, "is_windows", lambda: False)
    monkeypatch.setattr(platformutils.shutil, "which", lambda command: None)
    (tmp_path / "OpenKh.Command.Bar.exe").write_text("tool")

    with pytest.raises(GeneratorException, match="no way to run"):
        platformutils.openkh_tool_launcher(tmp_path, "OpenKh.Command.Bar")

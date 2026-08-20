from Module import appconfig


def test_openkh_folder_accepts_linux_config_directory(tmp_path):
    (tmp_path / "mods-manager.yml").write_text("installedModsPath: /tmp/mods\n")

    assert appconfig.is_openkh_folder(tmp_path)


def test_openkh_folder_accepts_mods_manager_in_apps(tmp_path):
    apps_path = tmp_path / "Apps"
    apps_path.mkdir()
    (apps_path / "OpenKh.Tools.ModsManager").write_text("tool")

    assert appconfig.is_openkh_folder(tmp_path)


def test_openkh_folder_rejects_unrelated_directory(tmp_path):
    assert not appconfig.is_openkh_folder(tmp_path)

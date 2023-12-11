import os
import textwrap
from pathlib import Path
from typing import Optional
from urllib import request
from zipfile import ZipFile

import tomlkit
import yaml
from PySide6.QtWidgets import (QDialog, QLineEdit, QGridLayout, QPushButton, QFileDialog, QLabel, QVBoxLayout,
                               QComboBox, QHBoxLayout, QMessageBox, QSpacerItem)

from UI import theme

DIALOG_TITLE = 'LuaBackend Hook Setup'
HOOK_DLL_NAME_MAIN = 'DBGHELP.dll'
HOOK_DLL_NAME_PANACEA = 'LuaBackend.dll'
LUA_DLL_NAME = 'lua54.dll'
BACKEND_CONFIG_FILE_NAME = 'LuaBackend.toml'
MOD_MANAGER_EXE_FILE_NAME = 'OpenKh.Tools.ModsManager.exe'
MOD_MANAGER_CONFIG_FILE_NAME = 'mods-manager.yml'
# Note - we choose to target a specific known version so that we know exactly what files we'll find and their format
#      - there's definite tradeoff here since we could get out of date, but this way is at least under our control
BACKEND_DOWNLOAD_URI = 'https://github.com/Sirius902/LuaBackend/releases/download/v1.7.2-hook/DBGHELP.zip'


class LuaBackendSetupDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.openkh_path: Optional[Path] = None
        self.pc_release_path: Optional[Path] = None
        self.hook_dll_path: Optional[Path] = None
        self.lua_dll_path: Optional[Path] = None
        self.config_file_path: Optional[Path] = None
        self.config_file_configured = False

        self.setWindowTitle(DIALOG_TITLE)
        self.setMinimumWidth(800)

        grid = QGridLayout()
        row = 0

        help_text = textwrap.dedent(f'''
        <span>
        KH2 Randomizer (the PC version) relies on Lua scripting, either via
        <a href="https://github.com/Sirius902/LuaBackend" style="color: {theme.LinkColor}">LuaBackend Hook</a> or
        <a href="https://github.com/TopazTK/LuaFrontend" style="color: {theme.LinkColor}">LuaFrontend</a>. This screen
        helps you get set up with the LuaBackend Hook option. This includes applying extra configuration to allow Lua
        scripts to be packaged in mods, making many common Lua scripts easily installable, updatable, and easy to turn
        on and off.
        </span>
        <br><br>
        <span>
        To proceed, choose the location of your OpenKH tools, choose which mode you use to mod the game, and
        choose Check Configuration. This will check the status of the various files needed for LuaBackend Hook.
        From there, you can choose to download/install the appropriate files, or if you already have the files
        installed, you can choose Apply Configuration to apply the necessary configuration only.
        </span>
        ''').strip()
        help_text_label = QLabel(help_text)
        help_text_label.setOpenExternalLinks(True)
        help_text_label.setWordWrap(True)
        grid.addWidget(help_text_label, row, 0, 1, 3)

        row = row + 1
        grid.addItem(QSpacerItem(0, 32), row, 0, 1, 3)

        row = row + 1
        openkh_path_field = QLineEdit()
        openkh_path_field.setToolTip('The location where OpenKH tools are installed.')
        openkh_path_field.textChanged.connect(self._openkh_path_changed)
        self.openkh_path_field = openkh_path_field
        openkh_path_button = QPushButton('Browse')
        openkh_path_button.clicked.connect(self._choose_openkh_path)
        grid.addWidget(QLabel('OpenKH location'), row, 0)
        grid.addWidget(openkh_path_field, row, 1)
        grid.addWidget(openkh_path_button, row, 2)

        row = row + 1
        mode_field = QComboBox()
        mode_tooltip = textwrap.dedent('''
        Which mode you use for modding the game (patching vs. mod loader).
        This affects the name of LuaBackend Hook's DLL file.
        ''').strip()
        mode_field.setToolTip(mode_tooltip)
        mode_field.addItems(['Panacea (Mod Loader)', 'Patch / Fast Patch'])
        mode_field.currentIndexChanged.connect(self._mod_mode_changed)
        self.mode_field = mode_field
        grid.addWidget(QLabel('Mod mode'), row, 0)
        grid.addWidget(mode_field, row, 1, 1, 2)

        row = row + 1
        validate = QPushButton('Check Configuration')
        self.validate = validate
        validate.setEnabled(False)
        validate.clicked.connect(self._validate_clicked)
        grid.addWidget(validate, row, 0, 1, 3)

        row = row + 1
        hook_dll_status = QLabel('')
        self.hook_dll_status = hook_dll_status
        grid.addWidget(QLabel('Hook DLL Status'), row, 0)
        grid.addWidget(hook_dll_status, row, 1)

        row = row + 1
        config_file_status = QLabel('')
        self.config_file_status = config_file_status
        grid.addWidget(QLabel('Configuration File Status'), row, 0)
        grid.addWidget(config_file_status, row, 1)

        row = row + 1
        lua_dll_status = QLabel('')
        self.lua_dll_status = lua_dll_status
        grid.addWidget(QLabel('Lua DLL Status'), row, 0)
        grid.addWidget(lua_dll_status, row, 1)

        row = row + 1
        install_files = QPushButton('Download/Install/Configure')
        install_files.setToolTip('Downloads, installs, and configures the necessary LuaBackend Hook files.')
        install_files.clicked.connect(self._install_clicked)
        install_files.setEnabled(False)
        self.install_files = install_files

        apply_configuration = QPushButton('Apply Configuration')
        apply_configuration.setToolTip('Applies configuration to LuaBackend Hook for OpenKH Mods Manager integration.')
        apply_configuration.clicked.connect(self._apply_configuration_clicked)
        apply_configuration.setEnabled(False)
        self.apply_configuration = apply_configuration

        button_bar = QHBoxLayout()
        button_bar.addWidget(install_files)
        button_bar.addWidget(apply_configuration)
        grid.addLayout(button_bar, row, 0, 1, 3)

        box = QVBoxLayout()
        box.addLayout(grid)
        self.setLayout(box)

        self._reset_validated_state()

    def _choose_openkh_path(self):
        output = QFileDialog.getExistingDirectory()
        if output is not None and output != '':
            self.openkh_path_field.setText(output)

    def _openkh_path_changed(self):
        openkh_path = self._path_or_none(self.openkh_path_field.text())
        self.validate.setEnabled(openkh_path is not None and openkh_path.is_dir())
        self._reset_validated_state()

    def _mod_mode_changed(self):
        self._reset_validated_state()

    def _reset_validated_state(self):
        self.pc_release_path: Optional[Path] = None
        self.hook_dll_path: Optional[Path] = None
        self.lua_dll_path: Optional[Path] = None
        self.config_file_path: Optional[Path] = None
        self.config_file_configured = False
        self.hook_dll_status.setText('(Not checked yet)')
        self.config_file_status.setText('(Not checked yet)')
        self.lua_dll_status.setText('(Not checked yet)')
        self.install_files.setEnabled(False)
        self.apply_configuration.setEnabled(False)

    def _validate_clicked(self):
        self._reset_validated_state()

        openkh_path = self._path_or_none(self.openkh_path_field.text())

        mods_manager_exe_file = openkh_path / MOD_MANAGER_EXE_FILE_NAME
        if not mods_manager_exe_file.is_file():
            message = QMessageBox(text='OpenKH Mods Manager not found. Ensure the OpenKH tools location is correct.')
            message.setWindowTitle(DIALOG_TITLE)
            message.exec()
            return

        mods_manager_yml_file = openkh_path / MOD_MANAGER_CONFIG_FILE_NAME
        if not mods_manager_yml_file.is_file():
            message = QMessageBox(text='OpenKH Mods Manager setup wizard has not been run.')
            message.setWindowTitle(DIALOG_TITLE)
            message.exec()
            return

        with open(mods_manager_yml_file,encoding='utf-8') as file:
            raw_yaml = yaml.safe_load(file)

        pc_release_path = self._path_or_none(raw_yaml['pcReleaseLocation'])
        if pc_release_path is None:
            text = textwrap.dedent('''
            OpenKH Mods Manager has not been configured for the PC game version.
            Either your OpenKH tools are out of date or you may need to re-run the setup wizard in Mods Manager.
            ''').strip()
            message = QMessageBox(text=text)
            message.setWindowTitle(DIALOG_TITLE)
            message.exec()
            return

        if not pc_release_path.is_dir():
            text = textwrap.dedent('''
            OpenKH Mods Manager has been configured for the PC game version, but the PC game location is missing.
            You may need to re-run the setup wizard in Mods Manager.
            ''').strip()
            message = QMessageBox(text=text)
            message.setWindowTitle(DIALOG_TITLE)
            message.exec()
            return

        self.openkh_path = openkh_path
        self.pc_release_path = pc_release_path
        self.install_files.setEnabled(True)

        hook_dll_path = pc_release_path / self._target_hook_dll_name()
        hook_dll_found = hook_dll_path.is_file()
        if hook_dll_found:
            self.hook_dll_path = hook_dll_path
            self.hook_dll_status.setText('Found {}'.format(self._target_hook_dll_name()))
        else:
            self.hook_dll_status.setText('Not found')

        config_file_path = pc_release_path / BACKEND_CONFIG_FILE_NAME
        config_file_found = config_file_path.is_file()
        if config_file_found:
            self.config_file_path = config_file_path

            with open(config_file_path,encoding='utf-8') as config_file:
                raw_toml = tomlkit.load(config_file)

            self.config_file_configured = self._has_matching_script_path(raw_toml)
            if self.config_file_configured:
                self.config_file_status.setText('Found and configured')
                self.apply_configuration.setEnabled(False)
            else:
                self.config_file_status.setText('Found, not yet configured')
                self.apply_configuration.setEnabled(True)
        else:
            self.config_file_status.setText('Not found')
            self.apply_configuration.setEnabled(False)

        lua_dll_path = pc_release_path / LUA_DLL_NAME
        lua_dll_found = lua_dll_path.is_file()
        if lua_dll_found:
            self.lua_dll_path = lua_dll_path
            self.lua_dll_status.setText('Found {}'.format(LUA_DLL_NAME))
        else:
            self.lua_dll_status.setText('Not found')

    def _install_clicked(self):
        try:
            target_zip_path = Path('DBGHELP-tmp.zip')
            request.urlretrieve(BACKEND_DOWNLOAD_URI, target_zip_path)

            with ZipFile(target_zip_path) as zip_file:
                if HOOK_DLL_NAME_MAIN not in zip_file.namelist():
                    message = QMessageBox(text='Downloaded LuaBackend Hook zip file is malformed.')
                    message.setWindowTitle(DIALOG_TITLE)
                    message.exec()
                    return

                pc_release_path = self.pc_release_path
                target_hook_dll_name = self._target_hook_dll_name()
                target_hook_zip_info = zip_file.getinfo(HOOK_DLL_NAME_MAIN)
                target_hook_zip_info.filename = target_hook_dll_name
                zip_file.extract(target_hook_zip_info, pc_release_path)

                zip_file.extract(LUA_DLL_NAME, pc_release_path)

                # If the user is choosing to download and install, just overwrite their config file.
                # Trying to be too cute caused a lot of headache because users were likely on an older format of the
                # config file, and we downloaded a new version of everything else.
                # If they already had a custom configuration set up, they'll just have to redo it.
                zip_file.extract(BACKEND_CONFIG_FILE_NAME, pc_release_path)
                self.config_file_path = pc_release_path / BACKEND_CONFIG_FILE_NAME
                self._do_apply_configuration()

            os.remove(target_zip_path)

            self._validate_clicked()

            message = QMessageBox(text='Downloaded, installed, and configured successfully.')
            message.setWindowTitle(DIALOG_TITLE)
            message.exec()
        except Exception as error:
            message = QMessageBox(text=str(repr(error)))
            message.setWindowTitle(DIALOG_TITLE)
            message.exec()

    def _apply_configuration_clicked(self):
        try:
            self._do_apply_configuration()

            message = QMessageBox(text='Configuration applied successfully.')
            message.setWindowTitle(DIALOG_TITLE)
            message.exec()
        except Exception as error:
            message = QMessageBox(text=str(repr(error)))
            message.setWindowTitle(DIALOG_TITLE)
            message.exec()

    def _do_apply_configuration(self):
        with open(self.config_file_path,encoding='utf-8') as config_file:
            raw_toml = tomlkit.load(config_file)

        target_path = self._mod_scripts_path()

        existing_script_list = raw_toml['kh2']['scripts']
        existing_script_list.append({'path': str(target_path), 'relative': False})
        with open(self.config_file_path, mode='w',encoding='utf-8') as config_file:
            tomlkit.dump(raw_toml, config_file)

        self._validate_clicked()

    def _target_hook_dll_name(self):
        mode_index = self.mode_field.currentIndex()
        if mode_index == 1:
            return HOOK_DLL_NAME_MAIN
        else:
            return HOOK_DLL_NAME_PANACEA

    def _has_matching_script_path(self, raw_toml: dict) -> bool:
        existing_script_list: list = raw_toml['kh2']['scripts']
        target_path = self._mod_scripts_path()
        for existing_script in existing_script_list:
            existing_script_path = Path(existing_script['path'])
            if existing_script_path == target_path and not existing_script['relative']:
                return True
        return False

    def _mod_scripts_path(self):
        return self.openkh_path / 'mod' / 'kh2' / 'scripts'

    @staticmethod
    def _path_or_none(string: str) -> Optional[Path]:
        if string:
            return Path(string)
        else:
            return None

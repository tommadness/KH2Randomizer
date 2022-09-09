import textwrap

from PySide6.QtWidgets import QListWidget, QHBoxLayout, QPushButton, QFileDialog

from Class import settingkey
from Class.seedSettings import SeedSettings
from Module.cosmetics import CustomCosmetics
from UI.Submenus.SubMenu import KH2Submenu


class CosmeticsMenu(KH2Submenu):

    def __init__(self, settings: SeedSettings, custom_cosmetics: CustomCosmetics):
        super().__init__(title='Cosmetics', settings=settings, in_layout='horizontal')

        self.custom_cosmetics = custom_cosmetics

        self.start_column()
        self.addHeader('Visuals')
        self.add_option(settingkey.COMMAND_MENU)
        self.end_column()
        self.start_column()
        self.addHeader('Music')
        self.add_option(settingkey.BGM_OPTIONS)
        self.add_option(settingkey.BGM_GAMES)
        self.end_column(stretch_at_end=False)

        self.start_column()
        self.addHeader('External Randomization Executables')

        custom_list = QListWidget()
        custom_list_tooltip = textwrap.dedent('''
        File(s) that will be executed every time a seed is generated. Used to integrate with external mods that require
        running a Randomize.exe file (or similar) to randomize their contents.
        ''').strip()
        custom_list.setToolTip(custom_list_tooltip)
        self.pending_column.addWidget(custom_list)
        self.custom_list = custom_list

        button_layout = QHBoxLayout()
        add_button = QPushButton('Add')
        remove_button = QPushButton('Remove')
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        self.pending_column.addLayout(button_layout)

        self.end_column()

        self.finalizeMenu()

        self._reload_custom_list()
        add_button.clicked.connect(self._add_custom)
        remove_button.clicked.connect(self._remove_selected_custom)

    def _reload_custom_list(self):
        self.custom_list.clear()
        for file in self.custom_cosmetics.external_executables:
            self.custom_list.addItem(file)

    def _add_custom(self):
        file_dialog = QFileDialog()
        outfile_name, _ = file_dialog.getOpenFileName(self, filter='Executables (*.exe *.bat)')
        if outfile_name != '':
            self.custom_cosmetics.add_custom_executable(outfile_name)
        self._reload_custom_list()

    def _remove_selected_custom(self):
        index = self.custom_list.currentRow()
        if index >= 0:
            self.custom_cosmetics.remove_at_index(index)
            self._reload_custom_list()
